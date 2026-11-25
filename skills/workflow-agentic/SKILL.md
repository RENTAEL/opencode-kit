---
name: workflow-agentic
description: "This skill teaches agents how to drive local OpenCode 2 and claude runs via the `oc_*` tools - dispatching consultations, multi-model fanout, continuing sessions across turns, and reading back results. It is the replacement for the previous Docker + Temporal \"Open Cloud\" model..."
---
# Agentic Workflow

## Purpose

This skill teaches agents how to drive local OpenCode 2 and claude runs via the `oc_*` tools - dispatching consultations, multi-model fanout, continuing sessions across turns, and reading back results. It is the replacement for the previous Docker + Temporal "Open Cloud" model: there is no control plane, no containers, no environment lifecycle. For an opencode model the orchestrator spawns a session runner on the host, a small Node process that drives the user's shared OpenCode background service through OpenCode 2's session API, and reads from the local SQLite store.

Load this skill when:

- Dispatching a consultation to a different model (thinking partner, adversarial review)
- Running multi-model fanout (ask 2-3 models the same question and synthesize)
- Continuing a prior conversation by `sessionId`
- Finding past work via `oc_search_sessions`
- Designing a command that spawns child opencode runs
- Dispatching, continuing or looking up a named agent of a stream (see Named Agents and the Roster)

## Mental Model

```
You (orchestrator on the host)
  |
  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ session runner, model X   (sync, blocks until reply)
  |
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ session runner, model Y   (async, returns runId + sessionId immediately)
      session runner, model Z   (async, runs in parallel; you wait or poll)
```

Key facts:

- **No environments, no containers.** Each opencode run is a child process on the host: the session runner (`node dist/modules/opencode/session-runner.js <spec.json>`) connects to the user's shared OpenCode background service (starting it with `opencode service start` when none is running), creates or resumes the session, sends the prompt or the slash command, and writes OpenCode 2's session events to the run log. Because the session lives on the same service as the TUI, it can be followed live from a separate terminal with `opencode -s <sessionId>`. The flip side: restarting, stopping or upgrading the service ends every in-flight run, and a service a run started keeps that run's environment for as long as it lives. It needs `node` (override with `NODE_BIN`) next to `opencode` (`OPENCODE_BIN`). Same credential store, same SQLite (`opencode.db`, override with `OPENCODE_DB`), same models as your interactive opencode.
- **Sessions are the durable handle.** Every run produces (or continues) a session. The session id is stable - pass it back on later runs to continue the conversation, even across reboots.
- **Multiple parallel runs to the same DB are safe.** OpenCode handles concurrent SQLite access. The same protection applies whether you spawn two terminals manually or fanout via `oc_run` mode=async.
- **There is no run queue.** Sync runs block the orchestrator. Async runs are independent OS processes - they run in parallel and you collect them with `oc_get_run_status`.
- **Parent process death does not lose data.** If the orchestrator dies mid-run, the conversation up to the last written part is still in SQLite. Reconnect, read the session, continue.

## Tools Reference

| Tool                 | Purpose                                                                                                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `oc_run`             | Spawn a session runner (opencode models) or `claude -p` (claude models), sync or async. Returns the reply (sync) or a handle.                                                                     |
| `oc_get_run_status`  | Poll an async run by `runId`: status, failure kind, the usage-limit window that refused it, context size, exit code, sessionId, and the full reply once finished (log tail while running/failed). |
| `oc_find_run`        | Look up the async run dispatched under a `label`. Recovers a lost `runId`; no reply or log tail.                                                                                                  |
| `oc_stop_run`        | Stop a running async run: verifies pid identity, SIGTERM then SIGKILL to the process group, marks it `stopped`.                                                                                   |
| `oc_wait_runs`       | Block until every listed async run is terminal or a timeout elapses; one status row per run (failure kind, context size, usage-limit window), no replies.                                         |
| `oc_get_session`     | Read message parts from a session. Defaults to the tail (latest N parts).                                                                                                                         |
| `oc_list_sessions`   | List recent local sessions (most recently updated first).                                                                                                                                         |
| `oc_search_sessions` | Substring search across session titles and message contents.                                                                                                                                      |

No environment, project-config, or exec tools exist - those were tied to the removed control plane.

## Dispatching Runs

### Synchronous (default - thinking-partner pattern)

```
oc_run(
  prompt: "Hello",
  model: "openai/gpt-5.5",
  agent: "researcher"
)
```

Returns the reply text + sessionId + exitCode. Use for:

- One-shot consultations
- Sequential challenge runs where each prompt depends on the previous reply
- Anywhere you would otherwise immediately `oc_get_session` to read the result

### Asynchronous (fanout pattern)

```
handleA = oc_run(prompt: "...", model: "openai/gpt-5.5", agent: "researcher",     mode: "async")
handleB = oc_run(prompt: "...", model: "openai/gpt-5.6-sol", agent: "researcher", mode: "async")
```

Returns `{ runId, pid, logPath, sessionId, label }` immediately; `sessionId` is hydrated from the run's first log event and may still read `(pending)` in that first return, in which case read it later from `oc_get_run_status`. The runner process runs in the background. Use for:

- Multi-model adversarial consultation (fanout to 2-3 models in parallel)
- Long-running work that the user wants to fire and forget
- Anywhere you want to dispatch and then continue doing other work

#### Labeling a dispatch

Pass `label` when the dispatch must be recoverable without its `runId` - typically a long-running worker:

```
oc_run(prompt: "...", model: "openai/gpt-5.5", agent: "implementer", mode: "async", label: "plan/assembly/1")
# later, after losing the runId (crash between dispatch and bookkeeping):
oc_find_run(label: "plan/assembly/1")
```

The record, label included, is persisted before the child process is spawned, and duplicate detection happens inside that same locked registry write, so two dispatchers cannot both claim one label. Labels are one-shot: a label that was ever used is rejected whatever the earlier run's status, so give every retry its own attempt suffix and each attempt stays findable. A label works on a sync run too.

#### Every run is registered and linked to its caller

A sync run is an async run the caller waits for: both are registered before the child is spawned, both write a log to the same directory, and a sync result carries its `Run ID` and `Log` path, so `oc_get_run_status` and `oc_find_run` read either kind. Aborting a sync call stops the run the way `oc_stop_run` does: an opencode child interrupts its session on the background service instead of leaving it running there.

Every record also stores `mode` (`sync` or `async`) and `caller`, the session that dispatched the run. Under OpenCode that is the calling session's id and the exact tool-call id. Under Claude Code it is the `CLAUDE_CODE_SESSION_ID` the MCP server was started with (MCP sends no id for the call itself). Together with each record's own `sessionId`, this links a session to the runs it started and to their sessions in any mix of harnesses, for example Claude Code ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ GPT review ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Claude. An opencode run's log holds the events of its subagent sessions as well as its own.

### Reasoning effort (`variant`)

`variant` sets the model's reasoning effort on an **opencode** run. OpenCode 2 has no `--variant` flag: effort is a `#variant` suffix on the model reference (`openai/gpt-5.6-sol#xhigh`). The `variant` argument takes one of `minimal`, `low`, `medium`, `high`, `xhigh`, `max` and the tool translates it into that suffix, so these two dispatches are the same:

```
oc_run(prompt: "<review brief>", model: "openai/gpt-5.6-sol", agent: "reviewer", variant: "high", mode: "async")
oc_run(prompt: "<review brief>", model: "openai/gpt-5.6-sol#high", agent: "reviewer", mode: "async")
```

Passing both a `#` suffix and `variant`, or an empty variant, is a validation error.

What it is worth, measured on `openai/gpt-5.6-sol` with one fixed prompt:

| variant                 | reasoning tokens |
| ----------------------- | ---------------- |
| omitted (model default) | 110              |
| `minimal`               | 221              |
| `xhigh`                 | 1034             |
| `max`                   | 1472             |

Three facts that decide how to use it:

- **Omitting it is not neutral.** The default sits at the bottom of the ladder, so a review
  dispatched without a variant is a low-effort review.
- **A variant the model does not offer fails the run.** OpenCode 2 reports it as an error instead of
  falling back to the default, and the `variant` argument is closed to the six names above, so a typo
  is a validation error instead of a silent downgrade. Never route around that by editing config to
  pass an arbitrary string.
- **It is rejected with a claude model.** The claude CLI has no equivalent flag, and accepting the
  argument would mean pretending the effort was raised.

Spend it where a missed defect is expensive: adversarial review, a hard design decision, a unit
whose failure mode is silent. It buys depth with latency and with the provider's usage window, which
is the scarce resource in any long multi-agent run, so `max` on routine work is how a five-hour window
disappears before the work that needed it.

The dispatch is described by a spec file, never by argv, so the prompt stays out of process
listings. It sits next to the run's log as `<uuid>.spec.json` and holds the prompt, the
model with its variant, the agent, the command and the session id, so what a run was actually
dispatched with is recoverable from disk rather than from memory; the log header lists the runner
script and that spec path.

### Continuing a session

Pass `sessionId` to continue an existing conversation:

```
oc_run(
  prompt: "Challenge me on the design I just proposed.",
  model: "openai/gpt-5.5",
  agent: "researcher",
  sessionId: "ses_..."   # from a prior run
)
```

The model sees the full prior conversation and can reference anything from earlier turns.

### Switching models mid-thread

The session is model-agnostic WITHIN its runtime, not across runtimes. An opencode session (`ses_*`) can be continued by any opencode model on any turn:

```
oc_run(prompt: "...", model: "openai/gpt-5.5", agent: "researcher",     sessionId: "ses_...")
oc_run(prompt: "...", model: "openai/gpt-5.6-sol", agent: "researcher", sessionId: "ses_...")
```

The new model sees the same conversation history. Use this when you want a second opinion partway through an existing thread.

Sessions do NOT cross the opencode/claude boundary: an opencode session cannot be continued by a claude model, and a claude session (UUID id) cannot be continued by an opencode model - `oc_run` rejects the mismatch as a validation error. A claude session can be continued by another claude model; pass the same `cwd` as the original run so the CLI finds the transcript.

### Running a slash command

Pass `command` to invoke an existing command instead of a freeform prompt. `prompt` becomes the command's `$ARGUMENTS`. It works for both runners: an opencode run executes it through the session command API (`session.command`), a claude run prepends `/name ` to the prompt:

```
oc_run(
  command: "pair-program",
  prompt: "opus",
  model: "openai/gpt-5.5",
  agent: "orchestrator"
)
```

Pass the agent the command pins (see Agent Profiles): a run the pin switched to another agent fails. A project command, one a repository keeps in its own `.opencode/commands` (such as a project's own review command), resolves only when `cwd` is that repository, a directory inside it or one of its worktrees; a worktree has only the commands the repository commits. Failure modes: a command that does not exist in the project or the global config fails the opencode run with "Command not found"; a `sessionId` that does not exist fails it with `runner.session-not-found` (OpenCode itself would silently start a new session under that id, and a caller continuing a conversation must never get an empty one). OpenCode 2's own `run` command cannot execute a slash command and passes `/name ...` to the model literally, which is why the runner drives the session API instead.

### Working directory

Pass `cwd` to set the spawned opencode's **project root**. Required when the consultant should be "in" a different project than the orchestrator:

```
oc_run(
  prompt: "...",
  model: "openai/gpt-5.5",
  agent: "researcher",
  cwd: "/Users/you/IdeaProjects/other-project"
)
```

Omit to use the orchestrator's current working directory.

#### What `cwd` affects

`cwd` determines which directory opencode treats as its project root for the duration of that run:

- **Session storage default project** - the run's session is recorded as belonging to `cwd`.
- **`.opencode/` overrides** - opencode loads project-local `opencode.json`, `agents/`, `commands/`, and `skills/` from `cwd/.opencode/`. A pair-program partner started in `~/IdeaProjects/project-a` picks up that repository's local commands; the same partner started in `~/IdeaProjects/project-b` does not.
- **File-watcher root** - opencode's automatic file change detection scopes to `cwd`.
- **Project context** - the agent's initial system context describes the project at `cwd`.

#### What `cwd` does NOT affect

`cwd` is NOT a sandbox. Within what its agent profile allows, the spawned opencode agent can target any absolute path in any other repo on the host with its own `shell`, `read`, `edit`, `grep` and `glob` tools. If you want the agent to also help with files in a sibling repo, just tell it in the prompt:

```
oc_run(
  prompt: "I'm in ~/IdeaProjects/project-a, but the bug repro is in ~/IdeaProjects/project-b/apps/api-rest/src/main.ts. Read that file and tell me what's wrong.",
  model: "openai/gpt-5.5",
  agent: "researcher",
  cwd: "/Users/you/IdeaProjects/project-a"
)
```

The agent reads `main.ts` in the other repo via its `read` tool, then continues its work in the `cwd` repo. The `cwd` choice only decides which project's `.opencode/` overrides and session bookkeeping apply, not which files the agent can touch; the profile decides that.

#### `cwd` does not stick across calls on the same session

Each `oc_run` invocation gets a fresh `cwd` argument; the session id only continues the conversation, not the working directory. If you set `cwd: "/Users/you/projects/foo"` on the first dispatch and then omit it on the second, the second call runs with the orchestrator's current `cwd`, NOT `/foo`. The conversation history is intact but the second run's project root, `.opencode/` overrides, and session-storage bookkeeping flip to wherever the orchestrator happens to be.

When you intend the partner to stay rooted in one repo for the duration of a thread, pass the same `cwd` value on every dispatch in that thread. The pair-program command bakes this into Step 2 (resolve cwd once) and reports it back to the user so subsequent dispatches can reuse it.

## Agent Profiles

Every opencode dispatch names the agent profile it runs as, with `agent` on `oc_run`. The profile is the worker's access boundary, not its brief. A dispatched run is non-interactive: the session runner approves a permission request for that one call (what `opencode run --auto` does) and cancels a question with feedback to continue on stated assumptions, so an action left at `ask` runs, and only a `deny` rule keeps a tool out. Each profile in the cookbook's `opencode.json` starts from `* deny` and allows only the whole tools its job needs; a denied tool is not even sent to the model. The table lists the five profiles `oc_run` accepts. The config's other agents are not dispatch profiles: `conductor` is the interactive agent that holds `wf_*` and runs workflow scripts, and OpenCode's built-in `build`, `plan` and `general` are disabled.

| Profile        | Dispatch it for                                                                                                                                           | It may                                                                                                                                                      | It may not                                                              |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `implementer`  | implementation and fix workers                                                                                                                            | read, edit, run any shell command (checks, tests, commits, pushes), load any skill, use `codebase_*`                                                        | dispatch (`oc_*`), the web, ask questions, start subagents              |
| `reviewer`     | review rounds, free-form reviews of a diff, document or design                                                                                            | read, grep, use `codebase_*` and `markdown_*`, run any shell command, edit files, load any skill, report with `submit_result`                               | dispatch (`oc_*`), `check_run`, the web, ask questions, start subagents |
| `pr-reviewer`  | a project's own review command that pins it                                                                                                               | what `reviewer` may, plus `github_ci_wait`                                                                                                                  | what `reviewer` may not                                                 |
| `researcher`   | recon, diagnosis, pair-program and adversarial-consult partners, any read-only consultation                                                               | what `reviewer` may, plus `webfetch` and `websearch`                                                                                                        | what `reviewer` may not                                                 |
| `orchestrator` | a run that needs the full surface: an execute command's handoff, a worker that must itself dispatch, cookbook plugin work that calls the tool being built | read, edit, run any shell command, load any skill, start subagents, ask questions, use `codebase_*`, `markdown_*`, `check_run`, `github_ci_wait` and `oc_*` | `wf_*`, the web and the other plugin tools                              |

A profile's rules name whole tools and never a command, a path or a skill. The profile exists to keep the plugin tools a job does not need out of the worker's context, not to sandbox it, so the read-only profiles have the whole shell, the edit tool and every skill, and the brief is what keeps them read-only: read and grep, run no tests, make no git write and no `gh` write, and write only scratch files. Scratch files are paths under `/tmp`, `/private/tmp`, the macOS temp folders (`/var/folders`), a `scratchpad` directory, and `~/.agent-roster`, where a named agent keeps its memory file (see Named Agents and the Roster). A pr-reviewer's brief adds the detached checkout (`git checkout --detach`, `gh pr checkout --detach`) and the `gh api` calls that post its review. The GitHub token in the environment can write whatever a profile says, so a brief that matters states its limits in one sentence.

- **A missing profile fails the run.** An opencode `oc_run` without `agent` is a validation error, and a profile the installed config lacks fails the run as `runner.agent-not-found` (reinstall the cookbook's `opencode.json` and reload the service).
- **A command dispatch passes the agent the command pins.** A command's `agent:` frontmatter switches the session to that agent before its prompt is sent, so the runner reads the session back and fails a run the pin switched, as `runner.command-switched-profile`, after its first request. A project's own review command pins `pr-reviewer`; every other cookbook command pins `orchestrator`.
- **No agent carries a model.** The dispatcher's `model` and `variant` are what the run uses, also through a command pin.
- **A claude session can run a profile, a claude worker does not.** `claude --agent <name>` starts an interactive session with that profile's tool list (generated into `src/agents/` from `opencode.json`), and a command that sets `context: fork` and `agent:` runs as that profile's subagent. A command with `agent:` alone does not switch in Claude Code, so start the session with `--agent`.
- **The claude runtime does not apply a profile yet.** `agent` is accepted with a claude model and recorded, but the worker runs with the user's default Claude Code permissions, so a Claude reviewer's brief must state the read-only profile in one sentence.

Why reviewers run no tests: a reviewer that re-runs a suite spends its usage window reading test output the orchestrator already has from CI, and in a flaky suite it then chases failures that have nothing to do with the diff. A worker brief also states whether the worker may query a shared deployed database (dev, staging, production); without an explicit grant from the human, it may not, not even a read-only row count. Local and per-test databases are not deployed databases. One investigation worker counted rows on dev, staging and production unasked. Three more rules for every worker brief, all learned from dead sessions: keep tool outputs small (`git diff --stat`, `--name-only`, path-scoped diffs, ranged reads, never a whole multi-branch diff; a reviewer session died twice with a provider `server_error` right after a very large read); reply with one line while writing the real output to a file (see `replyMaxChars`); and run or poll long commands in the foreground. A claude worker under `claude -p` exits when its turn ends, so a turn that ends "waiting for the notification" of a background task loses that task: in one run such a worker exited with nothing pushed.

## Polling Async Runs

After dispatching with `mode: "async"`, wait for the whole batch in one call:

```
oc_wait_runs(runIds: [<runId>, <runId>], timeoutSeconds: <expected duration of the work>)
```

It returns once every run is terminal, or when the timeout elapses with a timed-out flag and the current statuses. Size the timeout to the expected duration of the work. It reports progress on every poll, so the transport does not see a silent call **while the host is awake**; a sleeping host freezes the waiter along with everything else, and the wait then dies on a transport idle timeout while the run itself is merely paused. A wait that died is not a run that died: re-attach once the host is awake, never re-dispatch. In Claude Code a wait longer than about two minutes is moved to a background task and its result arrives later as a task notification, so do not issue a second wait for the same runs. Replies are not included; read them per run afterwards. Fall back to polling a single run only when you need one intermediate look:

```
oc_get_run_status(runId: <runId>)
```

Returns:

- `status` - running / completed / failed
- `processAlive` - whether the PID is still in the OS process table
- `sessionId` - extracted from the run's log (may be `(none extracted yet)` until the runner writes its `runner.started` line, which comes once the runner has reached the background service and the session exists)
- `exitCode` - present once completed/failed (the runner exits 0 when completed, 1 when failed, 130 when stopped)
- `Failure` and `Error` - for a failed run, its kind (`context overflow`, `usage limit`, `API unreachable`) and the provider's error
- `Usage limit` - the quota window that refused the run and when it resets. A claude run also gives the window's length and the share used; an opencode run gives only the provider's error type and the reset time (see Recovering a worker killed by a usage limit)
- `Context` - peak and last context tokens of the run, and the peak's share of the model window, flagged past 60%
- the full assistant reply parsed from the run log once the run is finished (no truncation)
- log tail (bytes from the end of the run's log file) while the run is still running or after a failure

Poll approximately every 180 seconds. Long-running agent work rarely changes state often enough for more frequent polling to add useful information.

Every status read also reports `Last log write`. A run whose process is alive but whose log has been silent for far longer than its steps take is either hung or frozen with a sleeping host, and the two look identical from the registry. Check the host first (macOS: `pmset -g log | grep -E "Sleep|Wake" | tail -20`; a lid closed at the moment the log went silent explains everything, and the periodic keep-alive wakes do not count as awake). If the host was awake, the run is hung: stop it with `oc_stop_run` and treat it as a dead worker. If the host slept, the worker is fine and continues when the host wakes; stop and resume it only if its provider session timed out meanwhile. For long runs on a laptop, offer the human an opt-in keep-awake (`caffeinate -dimsu &`, pid recorded, killed at the end) and say plainly that closing the lid pauses every worker.

### Stopping a run

```
oc_stop_run(runId: <runId>)
```

Verifies the recorded pid still belongs to the run (pid plus the start time captured at dispatch), sends SIGTERM to the whole process group so the CLI's tool subprocesses go with it, waits a grace period, escalates to SIGKILL, and marks the record `stopped`. For an opencode run the SIGTERM makes the session runner interrupt the session through the service's API and write its final `runner.finished` line with status `stopped`; the shared background service keeps running. That status wins over the `failed` the exit would otherwise be classified as, whichever process observes the exit. A run that already finished is reported as such and nothing is signaled. The tool refuses when identity cannot be verified rather than risk signaling an unrelated process that reused the pid; inspect that pid by hand.

After stopping a worker that was editing files, read its journal and compare it with `git status` in its working directory before re-prompting the same session: the kill may have landed mid-edit.

### When the run is done

When `status` is `completed` or `failed`, read the session via `oc_get_session(sessionId, isFromEnd=true, limit=15)` to get the assistant's final reply. The log file is useful for diagnosing crashes (stderr appears there) and holds the run's events, but the structured conversation lives in SQLite.

## Reading Results

### From a sync run

`oc_run` (sync mode) returns the assistant reply inline. No follow-up read needed for short consultations.

Pass `replyMaxChars` when the run is a worker that was told to reply with one line and write its real output to a file: the reply is truncated to that many characters with a marker saying where the full text lives (the run log and the session), so a worker that ignores the protocol cannot flood your context. Omit it for consultations, where the reply is the point.

### From an async run, or from any session by id

For a finished async run, `oc_get_run_status` returns the reply parsed from the run log; it takes the same `replyMaxChars` cap as a sync `oc_run`, and every worker read should pass it. For the conversation itself, or for a reply longer than the cap that you do need in full, read the session:

```
oc_get_session(sessionId: <id>, isFromEnd: true, limit: 15)
```

- `isFromEnd: true` (default) - return the MOST RECENT N parts. The assistant reply at the tail is always included.
- `isFromEnd: false` - return parts from the START of the session. Use when you need the original prompt or early-turn context (session archaeology).

For long sessions with tool calls and reasoning, the assistant's actual text reply is the last `text` part. With `isFromEnd: true, limit: 15` you reliably get the tail including the reply.

For a full conversation dump (rare - this is expensive in tokens), set `isFromEnd: false` and increase `limit` up to 50000.

### Anti-pattern: dumping the whole session when you only need the tail

If you only need the final answer, do NOT explicitly set `isFromEnd: false` with a huge limit - that dumps every turn including all prior context. The default (`isFromEnd: true, limit: 500`) already returns the tail; for very short replies a `limit: 15` is plenty.

## Model Selection

### Available Models

Only the model IDs in this table are supported.

| Model ID                     | Provider  | Runtime  | Strengths                                     |
| ---------------------------- | --------- | -------- | --------------------------------------------- |
| `openai/gpt-5.3-codex-spark` | OpenAI    | opencode | Codex line, fast agentic coding               |
| `openai/gpt-5.5`             | OpenAI    | opencode | Strong reasoning, balanced                    |
| `openai/gpt-5.5-fast`        | OpenAI    | opencode | Fast 5.5 (costs more; see below)              |
| `openai/gpt-5.6-luna`        | OpenAI    | opencode | 5.6 family, luna profile                      |
| `openai/gpt-5.6-luna-fast`   | OpenAI    | opencode | Fast luna (costs more; see below)             |
| `openai/gpt-5.6-sol`         | OpenAI    | opencode | 5.6 family, sol profile                       |
| `openai/gpt-5.6-sol-fast`    | OpenAI    | opencode | Fast sol (costs more; see below)              |
| `openai/gpt-5.6-terra`       | OpenAI    | opencode | 5.6 family, terra profile                     |
| `openai/gpt-5.6-terra-fast`  | OpenAI    | opencode | Fast terra (costs more; see below)            |
| `claude-fable-5-1`           | Anthropic | claude   | Frontier reasoning, hardest problems          |
| `claude-mythos-5`            | Anthropic | claude   | Fable-class sibling (approved orgs only)      |
| `claude-opus-5-5`            | Anthropic | claude   | Strong reasoning, balanced                    |
| `claude-sonnet-5-5`          | Anthropic | claude   | Balanced capability and speed                 |
| `claude-haiku-4-5`           | Anthropic | claude   | Fast and cheap, smoke tests                   |
| `kimi-code-plan-global/k3`   | Moonshot  | opencode | Personal projects only, variants low/high/max |

`claude-fable-5-1` and `claude-opus-5-5` answered a one-word probe through `oc_run` on 2026-09-22. Two OpenAI facts, also from 2026-09-22, shape the table:

- **The `-fast` variants cost more than their base models.** Never pick one to save money or as a default; use it only when the human asks for it.
- **No `openai/gpt-5.4` id is in the table** (`gpt-5.4`, `gpt-5.4-fast`, `gpt-5.4-mini`, `gpt-5.4-mini-fast`) because a Codex login through a ChatGPT account rejects them: `The 'gpt-5.4' model is not supported when using Codex with a ChatGPT account.` The base and `-fast` ids were re-checked on 2026-09-26 after they had worked earlier; older ids fall off the credential this way over time.

The model table is the single place model ids live. Other skills and commands name a role ("the strongest model of the implementer provider") and resolve it here, so a new model changes one table instead of every document.

The model id picks the runtime: provider-prefixed ids dispatch an OpenCode 2 session (through the session runner), bare claude ids (or the aliases `fable`, `opus`, `sonnet`, `haiku`) dispatch the `claude` CLI. Any other un-prefixed id is a validation error - `oc_run` never silently routes to a default runner.

#### The long-context suffix

A claude model's one-million-token context variant is addressed by suffixing the id: `claude-opus-5-5[1m]`. Reach for it when a worker's binding constraint is context rather than capability - a unit that reads a long specification section plus several modules. It is priced above the standard window (a one-word probe billed $0.28), so it is a deliberate choice per role, not a default.

Resuming a long-lived session is where the long window gets expensive: every turn re-feeds the whole history as cache reads. One implementer fix round on a `[1m]` session billed $18.83: 51,201 output tokens and 34,153 thinking tokens, against 23,229,193 cache-read tokens and 593,937 cache-creation tokens. The cache reads were the bill. So a small, self-contained follow-up (a documentation fix, a one-file correction whose context fits in the brief) goes to a fresh standard-window session with a brief that carries what it needs, not to a resume of the long session; one such fix ran in 202 seconds. Resume a long worker session only for a usage-limit death mid-task or a missing report, and only under the rotation threshold (see Rotating a long-lived session). Anthropic spend also has an organization-level monthly cap, which has killed runs mid-flight; a run that dies without a session-limit message and without an error trace is worth checking against it before re-dispatching.

The claude CLI rejects an unknown model id with `[claude-code:unrecognized_model]` and produces no reply, so a typo fails loudly rather than falling back. Confirm a variant exists by dispatching a one-word probe and checking that a reply came back at all; `ephemeral_1h_input_tokens` in the usage block is the long-context configuration's fingerprint.

Claude runs use the user's existing `claude` CLI auth and inherit the global `~/.claude/settings.json` permissions - no extra setup. Note the runtime split for session tooling: claude sessions are UUID-identified JSONL transcripts under `~/.claude/projects/`, so `oc_get_session` / `oc_list_sessions` / `oc_search_sessions` cannot read them (they reject UUID session ids with an explicit error). Read a claude reply from the sync result, or - for async runs - from `oc_get_run_status`, which returns the full assistant reply parsed from the run log once the run finishes (no truncation; the raw log tail appears only while running or after a failure).

### Selection Heuristics

| Task type                                                                                                           | Recommended model                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Orchestration, planning, decision making, partner                                                                   | the strongest tier of each provider (`claude-fable-5-1`, the newest `openai/gpt-5.6-*` profile); decisions are where cheap models cost the most |
| Implementation from a good spec or ticket                                                                           | the strongest tier of the implementer provider (`claude-fable-5-1`); a mid-tier implementer is paid back in review rounds                       |
| Code review, document review, re-checks, cohesion review                                                            | the strongest tier of the provider that did not implement the work: `openai/gpt-5.6-sol` for Claude's work, `claude-fable-5-1` for GPT's        |
| Recon, read-only code mapping                                                                                       | `claude-sonnet-5-5` (mid-tier); never the smallest tier, which assumes instead of reading                                                       |
| Mechanical reading (run this command, read this log for this pattern), nothing to infer                             | `claude-haiku-4-5` with fully explicit instructions; never for recon, review or implementation                                                  |
| Blank-line-only edits through a helper that refuses every other change, each batch corrected by a stronger reviewer | `claude-haiku-4-5` as the editor, `sonnet` as the reviewer (procedure in `develop-code-spacing`)                                                |
| Quick fixes, simple tasks                                                                                           | `openai/gpt-5.5` at the default variant, or `claude-sonnet-5-5`                                                                                 |
| Pair-programming thinking-partner                                                                                   | the strongest tier of the other provider (`openai/gpt-5.6-sol` or newer)                                                                        |
| Multi-model consultation (adversarial)                                                                              | Mix profiles and providers (e.g. `openai/gpt-5.5` + `openai/gpt-5.6-sol` + `claude-fable-5-1`)                                                  |
| Smoke testing                                                                                                       | `claude-haiku-4-5`, or `openai/gpt-5.5` at the default variant                                                                                  |

### Effort is part of model selection

The model id picks the reasoner; `variant` picks how hard it thinks. A strong model at the default
variant is not the strong-model choice the table above describes.

| Role                                                                                    | Variant                        |
| --------------------------------------------------------------------------------------- | ------------------------------ |
| Every opencode run, reviews included (code, document, adversarial, cohesion, re-checks) | `high`; none on a Claude model |

Use `high` for everything on opencode, reviews included. `xhigh` and `max` are never a default and never chosen by an agent or a command on its own; they are used only on a run where the human names them. Name the variant on every opencode dispatch, re-checks included. An omitted variant is the bottom of the ladder whatever the fix touched: in one multi-round run all 26 re-checks omitted it. A claude run takes no variant (see Reasoning effort), so its model is the only effort lever.

### Model is mandatory on every call

Always pass `model` explicitly on every `oc_run` call, and `agent` with it (see Agent Profiles). There is no platform default and no environment-level default - the CLI's own default is unstable and applied silently. The explicit `model` argument is the contract.

This applies to:

- Initial consultations
- Continuation calls (`sessionId` is set)
- Async fanout children
- Retries

When the user requests a specific model, use exactly that ID. Do not substitute "close enough" alternatives.

## Concurrency Model

### Sync runs

`oc_run` (sync) blocks the orchestrator until opencode exits. Sequential by definition - the next call cannot start until this one returns.

### Async runs

`oc_run` (async) returns immediately. The opencode process is detached - it survives the orchestrator's death and runs to completion in the background.

Two async runs against different models run in parallel:

```
a = oc_run(prompt: "...", model: "openai/gpt-5.5", agent: "researcher",     mode: "async")
b = oc_run(prompt: "...", model: "openai/gpt-5.6-sol", agent: "researcher", mode: "async")
# poll both until both complete
```

Two async runs against the same `sessionId` are unsafe - they would interleave writes to the same conversation. Don't do that. Always use a fresh session (omit `sessionId`) for each async fanout child, OR run them sequentially against the same session.

### Worktree contention

Multiple parallel consultations on the same working directory are fine for reads. If you fanout to 3 models that all edit the same files, you get the same conflict you would get from 3 humans editing concurrently. For multi-implementer fanout, use git worktrees (see `workflow-git-worktree`). For pure consultation (the common case), it's a non-issue.

## Session Continuity

### What sessions are

Every run produces a session - a conversation with full message history (user prompts, assistant responses, tool calls, tool results). Opencode sessions live in `~/.local/share/opencode/opencode.db` (override with `OPENCODE_DB`; the `session_v2` and `session_message` tables) and are identified by an opaque id (e.g. `ses_abc...`). Claude sessions live as JSONL transcripts under `~/.claude/projects/` and are identified by a UUID; they never appear in the SQLite store, so the `oc_get_session` / `oc_list_sessions` / `oc_search_sessions` tools are opencode-only.

### Continuing a conversation

```
first  = oc_run(prompt: "Hello",   model: "openai/gpt-5.5", agent: "researcher")
second = oc_run(prompt: "Why?",    model: "openai/gpt-5.5", agent: "researcher", sessionId: first.sessionId)
```

The second call sees the full prior conversation.

### Switching models mid-thread

```
first  = oc_run(prompt: "Outline a plan.",         model: "openai/gpt-5.5", agent: "researcher")
second = oc_run(prompt: "Challenge that outline.", model: "openai/gpt-5.6-sol", agent: "researcher", sessionId: first.sessionId)
```

The new model sees the same conversation. The previous model's reply is part of the history.

### Recovering prior context

```
sessions = oc_search_sessions(query: "PROJ-123")
messages = oc_get_session(sessionId: sessions[0].id, isFromEnd: true, limit: 50)
# or resume:
oc_run(prompt: "Continue where we left off.", model: "openai/gpt-5.5", agent: "researcher", sessionId: sessions[0].id)
```

### Browsing recent sessions

```
oc_list_sessions(limit: 20)
```

Sorted by last-updated descending. Returns title, directory, timestamps.

## Long-Running Worker Resilience

Async workers on the claude runtime can die mid-task from plan usage limits, and any long-lived session eventually exhausts its context window. Both are recoverable when the dispatch was set up for it - and expensive re-work when it was not.

### Require a progress journal from every long async worker

A worker that dies after 30 minutes of multi-file work leaves either an explained tree (journal present) or an archaeology project (no journal). Make the journal part of the dispatch prompt itself, as the FIRST instruction:

```
FIRST ACTION: create your progress journal at <scratchpad>/<unit>-journal.md and
append one line after EVERY completed step (files done, decisions made, test
status). A usage limit can kill you mid-task - the journal is what makes your
work resumable and reviewable if that happens.
```

- The journal lives at a path the orchestrator can read and git ignores.
- One line per completed step is enough; the goal is "what is done, what remains", not prose.
- On worker death, the orchestrator reads the journal BEFORE deciding anything: it distinguishes "port finished, only verification remained" (orchestrator finishes solo) from "died mid-unit" (resume the worker).

### Recovering a worker killed by a usage limit

Symptom (claude runtime): the async run ends with exit code 1 and the extracted reply is only `You've hit your session limit Ãƒâ€šÃ‚Â· resets <time>` - no report, no error trace. The conversation up to the death is intact in the session.

Symptom (opencode runtime, OpenAI): exit code 1, and the run log ends with a `runner.finished` line of status `failed` whose error has type `provider.quota` (or `provider.rate-limit`), HTTP status 429 and the message `The usage limit has been reached`; the same error is on the `session.execution.failed` event. The 429 may be on the error itself or only inside its response body (`status_code`); both count. OpenCode 2 drops the response headers, but the codex backend's refusals repeat them inside the body, and then the `Usage limit` field (`oc_get_run_status` and `oc_wait_runs`) names the window that refused (`primary`, 300 minutes, or `secondary`, 10080 minutes, the weekly one), the share of it used, the reason (`workspace_member_credits_depleted`, for example) and the reset time; this is the form seen on real refusals since 2026-10-01. Without the repeated headers the field carries only the error type from the body (`usage_limit_reached`) and the reset time from its `resets_at`. If the body has no `resets_at`, the field is absent and the failure kind is still `usage limit`; read the log tail for the provider's message.

When the field names the window, act on it. When it carries only `usage_limit_reached`, decide by the reset time. The 5-hour window is 300 minutes long and the weekly one 10080, so a reset more than five hours away can only be the weekly window. This is an inference from the window lengths, not something the log states:

| Reset time in the `Usage limit` field | Window                                                                | Remedy                                                                                                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| within five hours                     | the 5-hour window, or a weekly window that happens to reset that soon | wait: arm a background wait for the reset time plus a margin                                                                                                                        |
| more than five hours away             | the weekly window                                                     | pause every dispatch to that provider and report to the human with the reset time: the reset can be days away, and the remedy (a weekly reset the account holder applies) is theirs |

A claude run still names its window: the `Usage limit` field reads it from the rate-limit events (`five_hour` or `seven_day`, with its length, the used percentage and the reset time), and the same two remedies apply.

Waiting is the remedy. Never move a review to the implementer's own provider to dodge the wait: an exhausted reviewer window means the review waits for its reset, however long that is.

For the 5-hour window, arm the wait instead of asking anyone or polling the provider; work that does not need that provider continues meanwhile. At the reset, probe with a one-word sync run on the same provider (`openai/gpt-5.5` at the default variant, never a `-fast` variant) before re-dispatching real work. The probe proves availability, not quota for a long run, so the first real dispatch may still fail once and is then rescheduled.

A Claude orchestrator and Claude workers on the same account hit the same limit in the same minute; the durable state (journals) is what survives, and the orchestrator recovers first, then resumes the workers.

Recovery once the limit resets (or the plan is upgraded): resume the SAME session so the worker keeps its full context - do not re-dispatch the original brief:

```
oc_run(
  prompt: "Your session limit has been lifted - continue exactly where your journal left off. Per the journal, <done summary>; remaining: <steps>. Keep journaling every step. Same rules: <the 2-3 load-bearing rules from the original brief>.",
  model: "claude-fable-5-1",
  agent: "implementer",
  sessionId: "<the dead run's sessionId>",
  cwd: "<same cwd as the original dispatch>"
)
```

- Restate the journal's state in the resume prompt (done vs remaining) - it re-anchors the worker and catches journal/tree drift immediately.
- Repeat the non-negotiable rules from the brief (its git rules, source-of-truth paths, verify commands). Cheap insurance against post-resume drift.
- Read the session's last-run peak context first (see Rotating a long-lived session). Past the threshold, dispatch a fresh session with the brief plus the journal instead: a resume at that size costs more than the context it saves.
- If the worker died BETWEEN units (work complete, report unwritten), resuming the same session with "write the report now" is usually the cheapest correct move: the worker has the context and the resume takes minutes. Reconstruct the report from the tree and the journal only when the session is gone.

### Rotating a long-lived session before and after overflow

Symptom: exit code 1 with failure kind `context overflow`. In an opencode run log that is a `runner.finished` line (and a `session.execution.failed` event) whose error has type `provider.invalid-request` and a message or body using one of OpenCode's context-overflow phrases ("prompt is too long", "exceeds the context window", "maximum context length" and the like); OpenCode 2 no longer names the error `ContextOverflowError`. For a claude run it is `Prompt is too long` as the result: the accumulated conversation no longer fits the model's window. Observed on an OpenAI session at about 370k tokens, and on a claude implementer resumed for its fourth fix round at 977k of 1M.

An opencode run with this cookbook's config compacts instead of failing when it reaches its threshold (the model's input limit minus `compaction.buffer`, 20k, and at most 750k for a Claude model; `gpt-5.5` and `gpt-5.6-*` under a ChatGPT login compact at 440k, the largest request they are known to serve, and `gpt-5.4` and `gpt-6-*` at 902k), and on a provider overflow; it fails only when the history is too large even to compact. The compaction writes a handoff on the session's own model through the cookbook's compaction plugin, and a handoff that fails to generate fails the compaction instead of falling back to a stock summary. A claude run in `-p` mode never compacts. Either way a compacted worker carries a lossy summary of its own reading, so rotation below stays the plan.

Rotate before that point, not after it. Before resuming any session, read the peak context of its last run: the `Context` field of `oc_get_run_status` and `oc_wait_runs` reports it for every async run.

Rotate instead of resuming when the peak is past the threshold for the runtime: 500k on a 1M claude window, 250k on an OpenAI session. The thresholds leave room for the largest growth one run showed (a claude fix round added up to 200k, an OpenAI re-check round up to 58k) and keep the per-turn re-read, which is the bill, below half a million tokens.

Recovery, whether proactive or after the overflow: rotate - start a FRESH session (omit `sessionId`) and re-pay the onboarding once:

```
oc_run(
  prompt: "<full onboarding briefing - fresh session, predecessor overflowed; same role> + <the current consultation>",
  model: "openai/gpt-5.6-sol",
  agent: "researcher",
  cwd: "..."
)
```

- Keep the onboarding briefing reusable (the same block every rotation needs) rather than reconstructing it from memory each time.
- In the first post-rotation prompt, carry over only the durable state the new session must know (role, project layout, standing rules, what was already verified) - not the dead session's conversational history.
- Do not fight the overflow by trimming the next prompt; the accumulated session is what no longer fits, and the very next run will fail the same way.

## Named Agents and the Roster

A named agent is a role that outlives any one session: a charter, a memory file and a history of runs, carried by a chain of fresh sessions. Its identity is its name, never a session id. Keeping one session alive as "the agent" is the expensive way to do it: every turn re-reads the whole history (see The long-context suffix), and the session dies with its window anyway.

### Layout

```
~/.agent-roster/<stream>/roster.md     every agent of the stream: name, purpose, agent profile, model, variant, cwd, status
~/.agent-roster/<stream>/<agent>.md    one agent's memory: charter, state, runs
```

`<stream>` is one line of work. The folder sits beside `~/.claude`, outside every repository: memory files describe work in progress and none of it belongs in a commit. The first coordinator of a stream creates the folder and both files from the templates below.

A claude worker can write its memory file only when `~/.agent-roster` is listed in `permissions.additionalDirectories` of `~/.claude/settings.json`. Under `defaultMode: acceptEdits` a `claude -p` run cannot ask, so an edit outside the listed directories is denied and the worker's State is lost: the first run on 2026-10-04 lost its State that way and the coordinator had to recover it from the Write call in the run log. Bash writes are not affected, which is why such a worker can still look healthy.

`roster.md`:

```markdown
# <stream> agents

Coordinator: the interactive session that dispatches every agent below and owns this file.

| Agent           | Purpose                                    | Profile      | Model              | Variant        | cwd       | Memory             | Status |
| --------------- | ------------------------------------------ | ------------ | ------------------ | -------------- | --------- | ------------------ | ------ |
| example-tooling | Builds one tooling module                  | orchestrator | claude-opus-5-5    | (claude: none) | /abs/path | example-tooling.md | active |
| reviewer        | Reviews one round, fresh session per round | reviewer     | openai/gpt-5.6-sol | high           | /abs/path | none               | active |
```

`<agent>.md`:

```markdown
# <agent>

## Charter

- Purpose: <one sentence>
- Works in: <cwd>; may write: <paths and systems>
- Never: <the hard limits>
- Escalate to the coordinator when: <conditions>

## State

- Last completed: <step>
- Open: <items>
- Decisions: <decision> - <why>
- Next: <step>

## Runs

| #   | Label | Run ID | Session ID | Model | Started | Outcome | Context peak |
| --- | ----- | ------ | ---------- | ----- | ------- | ------- | ------------ |
```

### Who writes what

- The coordinator owns `roster.md`, every Charter and the Runs table. It adds a Runs row when it dispatches (number, label, run id, model, start time) and completes it when the run ends (session id, outcome, context peak from `oc_get_run_status`).
- The agent owns its State. It updates State after every completed step, which makes State its progress journal (see Require a progress journal), and once more before it finishes. It never edits Charter or Runs.
- A stateless agent (a reviewer that gets a fresh session per round) has a roster row and no memory file.

### Dispatching a named agent

1. Read `roster.md` and the agent's memory file. Dispatch the agent under the profile its roster row names on every run, so its access does not change between sessions (see Agent Profiles); every dispatch profile may edit the memory files under `~/.agent-roster`.
2. Start a fresh session by default. Resume the last run's session only for a usage-limit death, a missing report or a transient provider error, and only when its context peak is under the rotation threshold for its runtime (see Rotating a long-lived session).
3. Label the run `<stream>/<agent>/<n>`, where `<n>` is the next Runs row number. Labels are one-shot, so a retry is a new row with a new number.
4. Open the brief with the memory pointer, then give the task:

```
You are the <agent> agent of <stream>. FIRST read ~/.agent-roster/<stream>/<agent>.md.
Its Charter binds you. Its State is where your predecessor stopped: verify it against
reality (git, and the systems it names) before you continue. Update State after every
completed step and before you finish. Do not edit Charter or Runs.
Task: <the task>
```

5. Record the Runs row, wait for the run (`oc_wait_runs`, or the completion notification of an async run), complete the row and read the State the agent left.

To find an agent's ids later, read the last Runs row; `oc_find_run(label)` recovers a lost run id, and `oc_get_run_status` gives that run's session id and context peak. Claude Code's in-process subagents are not named agents: their ids end with the session that spawned them.

Retire an agent by setting its roster status to `retired` with the reason; keep its memory file as the record.

## Inter-Agent Communication

### Parent-child via async fanout

The orchestrator can spawn child runs asynchronously and synthesize their outputs:

```
# Dispatch in parallel
gpt = oc_run(prompt: "<briefing + question>", model: "openai/gpt-5.5", agent: "researcher",     mode: "async")
sol = oc_run(prompt: "<briefing + question>", model: "openai/gpt-5.6-sol", agent: "researcher", mode: "async")

# Poll both
while True:
  s_gpt = oc_get_run_status(runId: gpt.runId)
  s_sol = oc_get_run_status(runId: sol.runId)
  if s_gpt.status != "running" and s_sol.status != "running":
    break
  sleep(180)

# Read both
out_gpt = oc_get_session(sessionId: s_gpt.sessionId, isFromEnd: true, limit: 30)
out_sol = oc_get_session(sessionId: s_sol.sessionId, isFromEnd: true, limit: 30)
# synthesize
```

### Thinking-partner pattern (sync, one persistent session)

Cheaper and simpler than multi-model when you only need one consultant. Acquire one session and consult it repeatedly:

```
hello = oc_run(prompt: "Hello", model: "openai/gpt-5.5", agent: "researcher")
session = hello.sessionId

# onboard once
oc_run(prompt: "Read these files in full: ...", model: "openai/gpt-5.5", agent: "researcher", sessionId: session)

# challenge as often as needed
oc_run(prompt: "Pressure-test X. Three things to verify, keep it tight.", model: "openai/gpt-5.5", agent: "researcher", sessionId: session)
```

Notes:

- Be terse in challenge prompts. Send the proposal + "three things to verify, don't restate my plan." A consultant that re-explains your framing burns turns.
- Long sessions accumulate hundreds of parts. Use `isFromEnd: true, limit: 15` for the reply; don't dump the whole session.

## Working With Multiple Partners

The thinking-partner pattern scales to a panel of partners you keep alive for a whole work session and consult repeatedly - the model behind the `adversarial-consult` command. Reach for a panel when you expect several significant design decisions and want more than one independent perspective on each; for a single decision, one-shot fanout (above) is enough.

### One persistent session per partner

Bootstrap each partner once with the same briefing, record its session id, and reuse that id for every later consultation. The session ids are the panel handles - they survive the orchestrator dying (see Session Continuity), so a panel can be resumed later via `oc_search_sessions`.

A persistent session is not immortal: after enough substantial consultations it overflows the model's context window and every further run on it fails (see Long-Running Worker Resilience for the rotation recovery). Keep the bootstrap briefing in a reusable form from the start - the session WILL need rotating eventually, and the briefing is what a rotation costs.

```
gpt = oc_run(prompt: "<shared briefing>", model: "openai/gpt-5.5", agent: "researcher",     mode: "async")
sol = oc_run(prompt: "<shared briefing>", model: "openai/gpt-5.6-sol", agent: "researcher", mode: "async")
# record gpt.sessionId and sol.sessionId - reuse them for the rest of the session
```

One partner, one session. Never share a session id across two parallel async runs - interleaved writes corrupt the conversation (see Concurrency Model).

### Choose complementary models

A panel earns its cost only if the members reason differently. Mix profiles and providers so each catches what the others miss - for example a systematic edge-case/correctness model (`openai/gpt-5.5`) alongside a different-profile model (`openai/gpt-5.6-sol`) or a cross-provider perspective (`claude-fable-5`). Two instances of the same model give you one perspective at double the cost.

### Consultation patterns

**N-way challenge (default).** Send the same position and framing to every partner in parallel (async), then synthesize. Identical framing is what makes the replies comparable.

| Partners agree                          | Partners diverge                                                                                                           |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Strong signal - proceed with confidence | Genuine complexity - identify what each partner optimizes for (correctness vs simplicity, local vs global) before deciding |

When every partner independently flags the same problem - even while proposing different fixes - the approach almost certainly has a real flaw. Revise before implementing.

**Arbiter (tiebreaker).** When you and one partner deadlock after ~2 rounds, hand the full debate (your position, their pushback, your counter) to a different partner as arbiter. Use sync mode - you are waiting on one decision.

### Skill mirroring

Tell each partner to load the same skills the primary agent loaded (`Load the language-cpp skill before answering.`) so the panel applies the same conventions you do. Put this in the consultation prompt, not the briefing.

### Synthesis discipline

- **Send in parallel, read sequentially.** Dispatch to all partners at once, but digest replies one at a time so the first does not bias how you weigh the next. Read each from the tail: `oc_get_session(sessionId, isFromEnd: true, limit: 30)`.
- **Do not weight partners equally by default.** One may catch a surface issue while another finds the structural flaw underneath it. Read every reply fully before acting.
- **Present a position, then ask for challenge.** Never open with "what should we do?"; open with "I propose X because Y - challenge this." Specific proposals backed by concrete evidence (call sites, file paths, line numbers) produce surgical feedback; abstract questions produce generic answers.

## Orchestrator Checklist

When designing a multi-agent workflow:

1. **Pick a model once and pass it explicitly on every call.** No defaults, no inheritance.
2. **Use async mode for parallelism, sync mode for sequential dependence.** Mixing them in one workflow is fine.
3. **Wait on async runs with `oc_wait_runs`**, one call per batch with a timeout sized to the work. Poll `oc_get_run_status` only for a single intermediate look, no more often than approximately every 180 seconds.
4. **Read replies with `oc_get_session(isFromEnd: true)`** - don't dump the whole session.
5. **Handle partial failure.** When one fanout child fails, still read the others and report what succeeded.
6. **Use a fresh session per async fanout child.** Don't share `sessionId` across parallel runs.
7. **State is durable.** If the orchestrator crashes, sessions and async run records survive. Pick up where you left off.
8. **Dispatch every worker under the agent profile of its role and give it a small-outputs rule** in its brief (see Agent Profiles), and label every async dispatch with an attempt suffix so retries stay findable.
9. **Treat a silent run as possibly frozen, not hung**, until the host's power log says the host was awake.
10. **Read a session's peak context before resuming it**, and rotate past the threshold instead (see Rotating a long-lived session).

## Debugging Runs

### Check async run status

```
oc_get_run_status(runId: <id>)
```

Returns status, processAlive, sessionId, exitCode, and the full assistant reply once the run is finished (a raw log tail is shown instead while running or after a failure). A record still marked `running` is reconciled on every read. The runner's own completion evidence, read from this run's log, is checked first and settles the status whatever the process is doing: for opencode runs the session runner's final `runner.finished` line (its status is `completed`, `failed` or `stopped`), or failing that a `session.execution.succeeded` event; for claude runs the terminal `result` event. A `session.execution.failed` or `session.step.failed` event alone settles nothing, because the session may retry after it. Without evidence, the process is identified by pid plus the OS-reported start time captured at dispatch: a dead pid, or a live one whose start time differs because the OS reused it, marks the run `failed`; a verified live worker keeps it `running`; when identity cannot be checked (no pid or start time recorded, `ps` unavailable) the record is left as is rather than guessed, and `processAlive` reports `unknown`.

### Read run output

```
oc_get_session(sessionId: <id>, isFromEnd: true, limit: 30)
```

Reasoning, tool calls, and text parts. The assistant's textual reply is the last `text` part.

### Find past work

```
oc_search_sessions(query: "<keyword>")
```

Matches against session titles and message content. Useful for `oc_search_sessions(query: "PROJ-123")` to find prior work on a ticket.

### Common Failure Modes

| Symptom                                                                                                                                                                              | Likely cause                                                                                                                                                                                    | Fix                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `opencode` not found                                                                                                                                                                 | Binary not on PATH for the orchestrator's environment                                                                                                                                           | Set `OPENCODE_BIN` env var to the absolute path, or symlink into /usr/local/bin                                                                                                                                                                                                                                                                       |
| Opencode run fails at once, stderr says `node` (or the `NODE_BIN` path) is not found                                                                                                 | The session runner runs under `node`, and `node` is not on PATH for the orchestrator's environment (the plugin host may be the compiled opencode binary, so it does not borrow its own runtime) | Set `NODE_BIN` to the absolute path of a Node 24 binary, or put `node` on PATH                                                                                                                                                                                                                                                                        |
| Async run never completes                                                                                                                                                            | The session runner crashed, or the background service went down, before the runner wrote its final line                                                                                         | Read log tail via `oc_get_run_status` for stderr. Status is settled from the runner's own evidence first (the runner's `runner.finished` line or a `session.execution.succeeded` event for opencode, the result event for claude); PID liveness only decides between running and failed when there is no evidence                                     |
| Status says `completed` with `exit 0` seconds after dispatch, while `processAlive` is `yes` and `Last log write` is seconds ago                                                      | The registry classified an early runner event as terminal. Observed on a claude run marked ended five seconds after dispatch while it was still streaming                                       | Do not trust the status, and do not re-dispatch, which would duplicate the worker. Poll a signal the registry is not involved in instead: a commit landing on the unit's branch, a review thread resolving, the report file appearing                                                                                                                 |
| A wait fails with the transport reporting no response or progress for thousands of seconds                                                                                           | The host slept, so the waiter stopped polling too. The run itself is merely paused                                                                                                              | The wait's death says nothing about the run. Re-attach with `oc_get_run_status` or an independent signal once the host is awake; never re-dispatch on a dead waiter                                                                                                                                                                                   |
| `sessionId` is `(none extracted yet)`                                                                                                                                                | The session runner has not written its `runner.started` line yet (it reaches the background service first)                                                                                      | Poll again; sessionId is hydrated from the first lines of the log                                                                                                                                                                                                                                                                                     |
| Model not found                                                                                                                                                                      | Provider credentials missing or model id wrong                                                                                                                                                  | Run `/connect` or `opencode auth login` to verify the provider is connected; check id against the table above                                                                                                                                                                                                                                         |
| Session continuity fails                                                                                                                                                             | Wrong sessionId, or session was on a different machine                                                                                                                                          | `oc_search_sessions` to find the right id; sessions are local to the host that produced them                                                                                                                                                                                                                                                          |
| Claude run exits 1, reply is only "You've hit your session limit Ãƒâ€šÃ‚Â· resets <time>"                                                                                                    | Plan usage limit killed the worker mid-task                                                                                                                                                     | Wait for the reset (or plan upgrade), then resume the SAME session with a continue-from-journal prompt - see Long-Running Worker Resilience                                                                                                                                                                                                           |
| Run exits 1 with failure kind `context overflow` (an opencode `provider.invalid-request` carrying an overflow phrase)                                                                | The long-lived session's accumulated conversation no longer fits the model's context window                                                                                                     | Rotate: fresh session, re-pay onboarding once - see Long-Running Worker Resilience                                                                                                                                                                                                                                                                    |
| Claude run exits 1; its result event reads `"result":"Prompt is too long"` with `"is_error":true` and `"terminal_reason":"blocking_limit"`, while its `subtype` still says `success` | A resumed claude session's history no longer fits the window; observed on the fourth resume of one implementer, at 977k of 1M                                                                   | Never resume it again; its next turn fails at once. Check the tree for half-applied work (a temporary revert from a deletion proof, an unpushed commit), then dispatch a fresh session with the brief, the journal and the current task - see Long-Running Worker Resilience                                                                          |
| `~/.local/share/opencode/opencode.db` (or the path in `OPENCODE_DB`) missing                                                                                                         | OpenCode hasn't been run on this host yet                                                                                                                                                       | Run `opencode` interactively once to bootstrap the database                                                                                                                                                                                                                                                                                           |
| No way to know a provider's remaining usage window before dispatching                                                                                                                | Not exposed by the current tools                                                                                                                                                                | Wanted: a usage tool for both runtimes and an `oc_run` guard that refuses dispatch on an exhausted window; until then read the reset time from a failed run's log tail. An agent's context fill is in its run log (see Rotating a long-lived session)                                                                                                 |
| Opencode run exits 1, log tail says `The usage limit has been reached` (429)                                                                                                         | One of the provider's two usage windows is exhausted; OpenCode 2 gives no headers, so which one is not stated                                                                                   | Read the reset time from the run's `Usage limit` field; the window itself is not in the log. Within five hours: arm a wait for the reset time plus margin, probe with a one-word cheap run, re-dispatch. More than five hours away (the weekly window): pause that provider's dispatches and report to the human - see Long-Running Worker Resilience |
| Opencode run exits 1 with `server_error` from the provider, no failure kind in the status                                                                                            | Transient provider failure, sometimes after a very large tool output early in the session                                                                                                       | Retry the same session once when it is under the rotation threshold (otherwise rotate at once); if it fails the same way, rotate to a fresh session and tell the worker to keep tool outputs small                                                                                                                                                    |
| Process alive, log silent for a long time, run never ends                                                                                                                            | Either a real hang or a sleeping host                                                                                                                                                           | Check the host power log first; if awake, `oc_stop_run` and re-dispatch under the role's agent profile - see Agent Profiles                                                                                                                                                                                                                           |
| Orchestrator and its Claude workers die within the same minute                                                                                                                       | Shared account, one usage limit                                                                                                                                                                 | Recover the orchestrator from its durable state first, then resume workers from their journals                                                                                                                                                                                                                                                        |

## Anti-Patterns

- Omitting `model` on `oc_run` and relying on the CLI default (silent drift; pass explicit `model` on every call)
- Dispatching a review without a `variant` and calling it a deep review (the model default is the bottom of the effort ladder)
- Putting `max` on every dispatch (it spends the provider's usage window on work that did not need it)
- Substituting a "close enough" model when the user requested a specific one (if it's unavailable, surface that; do not silently swap)
- Polling async runs with repeated `oc_get_run_status` calls, or a shell loop on a pid, when `oc_wait_runs` can wait for the whole batch in one call (every poll is a tool result in the orchestrator's context); when you do poll, no more often than approximately every 180 seconds
- Sharing a `sessionId` across two parallel async runs (interleaved writes to the same conversation)
- Calling `oc_get_session` with a huge limit when you only need the tail (use `isFromEnd: true, limit: 15`)
- Restating your own framing in challenge prompts to a thinking partner (wastes turns; state the proposal and ask for specific pushback, with "don't restate my plan")
- Using bash + raw `opencode run` from a tool when `oc_run` exists (the tool surfaces sessionId reliably, runs slash commands, and fails a missing session instead of silently starting a new one; bash output parsing is fragile)
- Dispatching a long multi-file async worker without requiring a progress journal (a usage-limit death then leaves an unexplained working tree instead of a resumable one)
- Re-dispatching the original brief on a fresh session after a usage-limit death, instead of resuming the dead worker's session while it is under the rotation threshold (throws away the worker's accumulated context and re-does paid work)
- Continuing to prompt a session that just failed with a context overflow (a `provider.invalid-request` overflow error on opencode, `Prompt is too long` on claude) (the accumulated history is what no longer fits; every further run fails identically until you rotate)
- Resuming any session without first reading its last run's peak context from the run log (rotation after the overflow costs a dead run; rotation before it costs nothing)
- Reading a claude result event's `subtype: success` as a finished run without checking `is_error` and `result`
- Dispatching a worker under a broader profile than its role needs, such as a review or recon as `orchestrator` (it pays for every tool definition on every request and is held back by nothing; use the role's profile)
- Declaring a run hung without checking whether the host slept (a closed laptop lid freezes every worker and looks identical in the run status)
- Letting a worker print a whole multi-branch diff or read a huge file in one call (large outputs have preceded provider `server_error` deaths; use `--stat`, `--name-only`, scoped diffs, ranged reads)
- Issuing a second `oc_wait_runs` for runs whose first wait Claude Code moved to a background task (the result arrives as a notification)
- Trusting a terminal status that contradicts its own evidence (`completed` while `processAlive` is `yes` and the log is still being written); poll an independent signal instead
- Re-dispatching a worker because the wait died. The waiter and the run fail independently, and a duplicate worker on the same branch is worse than a lost wait
- Asking the human what to do about a usage limit that resets within five hours when the reset time is in the run's `Usage limit` field (schedule the retry, keep working on what the other provider can do)

## Quick Reference: Common Workflows

### Single consultation, single task

```
MODEL = "openai/gpt-5.5"
out = oc_run(prompt: "...", model: MODEL, agent: "researcher")
# read out.sessionId, out.reply (returned inline)
```

### Sequential multi-step on one thread

```
MODEL = "openai/gpt-5.5"
r1 = oc_run(prompt: "Step 1...", model: MODEL, agent: "researcher")
r2 = oc_run(prompt: "Step 2...", model: MODEL, agent: "researcher", sessionId: r1.sessionId)
r3 = oc_run(prompt: "Step 3...", model: MODEL, agent: "researcher", sessionId: r2.sessionId)
```

### Parallel multi-model consultation

```
a = oc_run(prompt: "...", model: "openai/gpt-5.5", agent: "researcher",     mode: "async")
b = oc_run(prompt: "...", model: "openai/gpt-5.6-sol", agent: "researcher", mode: "async")
# poll both via oc_get_run_status; when both done, read sessions
ra = oc_get_session(sessionId: <a's sessionId>, isFromEnd: true, limit: 30)
rb = oc_get_session(sessionId: <b's sessionId>, isFromEnd: true, limit: 30)
# synthesize
```

### Resume a prior conversation

```
hits = oc_search_sessions(query: "<ticket key>")
oc_run(prompt: "Continue...", model: "openai/gpt-5.5", agent: "researcher", sessionId: hits[0].id)
```

### Thinking-partner thread (single session, repeated challenges)

```
hello = oc_run(prompt: "Hello", model: "openai/gpt-5.5", agent: "researcher")
session = hello.sessionId
oc_run(prompt: "Read these files: ...",                            model: "openai/gpt-5.5", agent: "researcher", sessionId: session)
oc_run(prompt: "Pressure-test X. Three things to verify...",       model: "openai/gpt-5.5", agent: "researcher", sessionId: session)
# switch mid-thread without losing context:
oc_run(prompt: "Same question, second opinion.",                   model: "openai/gpt-5.6-sol", agent: "researcher", sessionId: session)
```
