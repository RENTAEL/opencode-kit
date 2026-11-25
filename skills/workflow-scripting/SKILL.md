---
name: workflow-scripting
description: "The workflow engine runs a script in the shape of Claude Code's Workflow tool in a detached process that journals every call in `<taskDir>/orch.db`. A step can be a GPT worker (opencode), which runs under the agent profile its `agentType` names, or a Claude worker (`claude -p`..."
---
# Workflow Scripting

## Purpose

The workflow engine runs a script in the shape of Claude Code's Workflow tool in a detached process that journals every call in `<taskDir>/orch.db`. A step can be a GPT worker (opencode), which runs under the agent profile its `agentType` names, or a Claude worker (`claude -p`), which runs with the user's default Claude Code permissions and hooks off whatever its `agentType`, so a Claude step's prompt must state its access limits. Both return structured results. The session that starts a run stays in the loop: write a script for one phase, start it, wait, read the small result, decide, start the next.

Defers to `workflow-agentic` for choosing models and efforts per role and for dispatching a single worker by hand with `oc_run`.

## Which Engine

| The work                                                      | Use                             |
| ------------------------------------------------------------- | ------------------------------- |
| Claude-only, inside one Claude Code session                   | Claude Code's own Workflow tool |
| Any GPT step (a cross-provider review, a GPT verifier)        | this engine                     |
| Must survive the session, host sleep or a closed usage window | this engine                     |
| One worker                                                    | `oc_run`                        |

## Starting, Waiting, Reading

Every run lives in a task directory (absolute path; its `orch.db` is created when missing) and keeps its files in `<taskDir>/workflows/<runId>/`: `script.js`, `args.json`, `engine.log`, `result.json`, `calls/<label>.md` (text replies), `ci/` (failed CI logs), `posts/`.

Tools (OpenCode `conductor` agent; deferred `wf_*` tools in Claude Code):

```
wf_start({ taskDir, scriptPath, args: { ... }, cwd })                  // or script (text)
wf_wait({ taskDir, runIds: ['review-docs-3f9a1c2e'], until: 'all', timeoutSeconds: 3600 })
wf_stop({ taskDir, runId })
wf_start({ taskDir, resume: 'review-docs-3f9a1c2e' })                // optionally with scriptPath or script
```

The same from a shell (`<cookbook>` is the cookbook checkout whose `dist/` is installed):

```bash
node <cookbook>/dist/modules/wf/cli.js run --task "$TASK" --script "$SCRIPT" --args-file args.json --cwd "$WT"
node <cookbook>/dist/modules/wf/cli.js wait --task "$TASK" --run <id> [--run <id>] --until any --timeout 3600
node <cookbook>/dist/modules/wf/cli.js status --task "$TASK" --run <id>
node <cookbook>/dist/modules/wf/cli.js run --task "$TASK" --resume <id> --wait --timeout 3600
node <cookbook>/dist/modules/wf/cli.js stop --task "$TASK" --run <id>
```

Exit codes of `wait` and `run --wait`: 0 every run completed, 1 one failed, stopped or was interrupted, 3 one paused, 124 timed out, 2 usage error, 70 other error. In Claude Code, `wf_wait` with a long timeout moves to the background after 120 s and its notification carries the whole summary; a backgrounded `wait` through Bash notifies with the exit code only, so read `status` afterwards.

A summary holds: status, current phase, context spent against the budget, calls per phase (completed, running, failed), every call that ended null with its failure kind (`budget`, `stopped`, `structured-output`, `usage-limit`, `context-overflow`, `api-unreachable`, `unclassified`) and error, and the result clipped, with the path to `result.json`.

| Status        | Meaning                                                                                 | Next                                                                             |
| ------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `running`     | its engine is working                                                                   | wait                                                                             |
| `completed`   | the script returned                                                                     | read the result                                                                  |
| `failed`      | the script threw, or a call was refused or a primitive failed (`error` says which)      | fix the cause, then resume (a new script with `scriptPath` replaces the old one) |
| `paused`      | a provider's usage window reopens more than 6 hours away (`pauseReason`, `resumeAfter`) | resume after `resumeAfter`; the run never switches provider                      |
| `stopped`     | stopped on request                                                                      | resume to continue                                                               |
| `interrupted` | its engine process is gone (killed, host restart)                                       | resume                                                                           |

Resume replays every completed call from the journal, adopts workers still running (or reads the ones that ended meanwhile), and runs failed calls again. A changed call (new prompt or options) runs live; unchanged ones replay.

## Script Shape

Plain JavaScript. The only export is `export const meta = { ... }`, a literal object of data; top-level `await` and a top-level `return` of the result (JSON) are allowed. No imports.

```js
export const meta = {
  name: 'docs-check', // kebab-case; runs are named <name>-<8 hex>
  description: 'Two critics on the docs',
  phases: [{ title: 'Review', detail: 'GPT and Claude critics' }],
  contextBudget: 8000000, // optional: context tokens all calls may spend
  concurrency: { openai: 4 }, // optional: replaces the default cap of a provider
}

const SCHEMA = {
  type: 'object',
  properties: { issues: { type: 'array', items: { type: 'string' } } },
  required: ['issues'],
  additionalProperties: false,
}

phase('Review')
const [gpt, claude] = await parallel([
  () =>
    agent(`Review the docs under ${args.dir} for accuracy.`, {
      label: 'review/gpt',
      model: 'openai/gpt-5.6-sol',
      agentType: 'reviewer',
      effort: 'high',
      schema: SCHEMA,
    }),
  () =>
    agent(
      `Review the docs under ${args.dir} for accuracy. You are read-only: run no tests, edit no tracked file, and write only scratch files.`,
      {
        label: 'review/claude',
        model: 'claude-opus-5-5',
        agentType: 'reviewer',
        effort: 'high',
        schema: SCHEMA,
      }
    ),
])
log(
  `gpt ${gpt === null ? 'failed' : gpt.issues.length}, claude ${claude === null ? 'failed' : claude.issues.length}`
)
return { gpt, claude, spent: contextBudget.spent() }
```

### agent(prompt, options)

| Option      | Rule                                                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `label`     | required; path-like (`AB-1/review/2`); unique among the run's calls; names the journal row and the registry label `wf/<runId>/<label>/<n>`             |
| `model`     | required; `openai/...` runs on opencode, `claude-*` on `claude -p`; `anthropic/...` is refused                                                         |
| `agentType` | required; one of `implementer`, `reviewer`, `pr-reviewer`, `researcher` (never `orchestrator`); enforced on a GPT step only, recorded on a Claude step |
| `effort`    | required for a Claude step (`low` to `max`); optional for GPT (the opencode variant, `minimal` to `max`)                                               |
| `schema`    | optional JSON Schema, an object at the top level, strict ajv; the call returns the validated object                                                    |
| `phase`     | optional; defaults to the last `phase()`                                                                                                               |
| `cwd`       | optional absolute directory; defaults to the run's                                                                                                     |
| `command`   | optional slash command name; the prompt becomes its arguments                                                                                          |

Anything else (`variant`, `isolation`, `disallowedTools`) is refused. Without `schema` the call returns the reply text. A worker that fails for good, or completes without a reply, makes `agent()` resolve to `null`; check every result. A refusal (a bad option, an uncapped provider, a schema that does not compile) or a failed host primitive ends the run, also inside `parallel`.

What the engine does per call, so the script does not: a Claude worker gets `--json-schema`, `--effort` and hooks off; a GPT worker gets the schema through `submit_result` and one resume with a nudge when it ends without a result; a usage limit closes that provider until the reset (other providers keep working) and resumes the worker's session after it; a context overflow reruns fresh once; an unreachable API backs off and reruns.

### Other globals

- `parallel(thunks)`: starts every thunk at once; a thunk that throws resolves to null.
- `pipeline(items, stage1, stage2, ...)`: each item flows through the stages with no barrier; a stage gets `(previousValue, item, index)`.
- `phase(title)`, `log(message)`: events in `orch.db`, shown by `status`.
- `args`: the run's args, frozen.
- `contextBudget.total`, `.spent()`, `.remaining()`: context tokens (input plus cache read and write, summed over every request of every call). Once spent, new calls resolve to null with failure kind `budget`. Not Workflow's `budget`, which counts output tokens of a turn; a script using `budget` fails.
- `git.head({ cwd?, ref? })` returns a sha; `git.worktree({ cwd? })` returns `{ path, branch, head, isLinked }`. `git.worktree` is a guard: it looks at the worktree again on every execution and is never replayed, so check it before every worker that commits and branch only on its `isLinked` and `branch`. Build prompts from `git.head`, which replays.
- `ci.wait({ cwd?, repo?, pr, head?, timeoutMinutes? })` waits for the pull request's checks on `head` (else the local branch it is from): `{ state: 'passed' | 'failed' | 'timeout' | 'no-checks' | 'head-mismatch', head, expectedHead, checks, failing: [{ name, conclusion, logPath }] }`.
- `review.post({ cwd?, repo?, pr, key, body })` posts a pull request comment; `thread.reply({ cwd?, repo?, pr, key, commentId, body })` replies in a review comment's thread. Both return `{ url }`, post once per `key` across resumes (found again by a marker) and refuse a new body under a used key.

Every call, primitives included, is journaled and replays on resume (apart from `git.worktree`), so a script takes the same path again: `Date`, `Math.random` and `Intl.DateTimeFormat` throw; pass the time or a seed in `args`. A schema checks each answer's form, not that its ids are unique or that it answers every open item: check that in the script right after the call, before anything uses the ids (a label built from a duplicated id ends the run).

### Model and profile per role

Reviewers and verifiers on GPT (`openai/gpt-5.6-sol`, `effort: 'high'`, `xhigh` only where a missed defect is expensive), `agentType: 'reviewer'` or `'pr-reviewer'`. Research and recon on Sonnet (`claude-sonnet-5-5`, `agentType: 'researcher'`). Implementation and fixes on the implementer tier (`claude-opus-5-5`, `agentType: 'implementer'`). The `agentType` of a Claude step is a label, not a boundary: a Claude worker can do whatever the user's Claude Code permissions allow, so its prompt must state the limit (a Claude reviewer's prompt says it is read-only, runs no tests, edits no tracked file and writes only scratch files, as in the example above). A provider needs a cap: defaults `openai` 6 and `anthropic` 4; anything else must be named in `meta.concurrency`.

## Anti-Patterns

- Omitting `agentType`, `model`, or a Claude step's `effort`, expecting a default
- Treating an `agent()` result as non-null without a check
- Using `budget` (Workflow's) instead of `contextBudget`
- Having a worker post to GitHub, merge, or touch a ticket tracker or chat inside a run; post through `review.post` and `thread.reply`, and keep merge, tickets and chat outside
- Switching a provider when a run pauses on a usage window instead of resuming after `resumeAfter`
- Polling `status` in a loop instead of one `wf_wait` with a long timeout
- Starting a fourth review round because the third left findings open
