---
name: goal-development
description: "Autonomous mode for development tasks. Initializes (or resumes) the task, then invokes every required `dev-*` subskill back-to-back via the Skill tool, pausing at gates between subskills. Shares `orchestrator-state.yml` with assisted mode (`/owflow:development`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â..."
---
# Orchestrated Development Wrapper

Autonomous mode for development tasks. Initializes (or resumes) the task, then invokes every required `dev-*` subskill back-to-back via the Skill tool, pausing at gates between subskills. Shares `orchestrator-state.yml` with assisted mode (`/owflow:development`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tasks can mix both modes freely.

Gates follow the shared contract in [Gate Contract](../orchestrator-framework/references/gate-contract.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â orchestrated mode exception: each subskill's own Exit Gate acceptance question IS the loop gate (Accept = continue to the next subskill).

## Entry Gate

Identical to the dispatcher ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â complete ALL of its entry-gate steps first:

1. Read the [Dispatcher & Handoff Pattern](../orchestrator-framework/references/dispatcher-handoff.md) and the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md).
2. Detect prior work context: research folder path or `--research=<path>` flag (same detection and state setup as the development dispatcher ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `../development/SKILL.md` Entry Gate). Dev-bugfix tasks (`.owflow/tasks/development/` entries with `entry_point: "dev-bugfix"`) need no special handling ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they are standard development tasks; route from the first missing slug.
3. Initialize (new task) or resume (task path): create task directory + `orchestrator-state.yml` with `verify_template` validation, discover `.owflow/docs/INDEX.md` project docs, write command flags to `options.*`. On resume, find the first step slug NOT in `completed_phases` (validate artifacts; `--from=<step-slug>` overrides).
4. Create ONE task item via `TaskCreate` per subskill in the upcoming loop (subject: `"<step names>: <subskill>"`, e.g. `"Analysis: dev-analyze"`); update statuses as the loop progresses.

**Output**:

```
ÃƒÂ°Ã…Â¸Ã…Â¡Ã¢â€šÂ¬ Orchestrated Development

Task: [description]
Directory: [task-path]
Loop: dev-analyze ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [dev-tdd-red] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ dev-spec ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ dev-plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ dev-implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ dev-verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ dev-finalize
```

---

## The Loop

For each subskill in sequence (skipping conditionals below), execute:

1. **Announce**: 1-line phase banner.
2. **Invoke**: Skill tool with `name: "<subskill>"` and `prompt: "<task-path> [flags relevant to that subskill]"`. The subskill owns its Entry Gate, delegation, and state updates.
3. **Verify handback**: after the skill returns, re-read `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm the expected step slugs were appended to `completed_phases` (per the Sequence and Conditionals table). If a subskill stopped early (entry check failed), STOP the loop and relay its routing message to the user.
4. **Gate (subskill's Exit Gate is the loop gate)**: each subskill presents its results box and fires its own results-acceptance `question` before its handoff hint (Orchestrated-mode exception, [Gate Contract](../orchestrator-framework/references/gate-contract.md)). [Rule 5 of the Dispatcher & Handoff Pattern](../orchestrator-framework/references/dispatcher-handoff.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "subskills only SUGGEST the next command" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is superseded for Accept: when the user answers **Accept** to the subskill's Exit Gate question pointing at the next subskill in this loop, treat that as "continue to the next subskill" and invoke it. Any other answer (Adjust / Discuss / Stop / other options picked) ends the loop the same way a rejected gate would.
   - **Exception**: no separate gate between `dev-analyze` and `dev-tdd-red` when the red gate activates ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â these two run back-to-back (mirrors the AUTO-CONTINUE of the classic orchestrator). A gate still applies between analysis and spec.

### Sequence and Conditionals

| Order | Subskill      | Run when (from state)                                    |
| ----- | ------------- | -------------------------------------------------------- |
| 1     | dev-analyze   | Always                                                   |
| 2     | dev-tdd-red   | `task_characteristics.has_reproducible_defect: true`     |
| 3     | dev-spec      | Analysis complete (`gap-analysed` in `completed_phases`) |
| 4     | dev-plan      | `implementation/spec.md` exists                          |
| 5     | dev-implement | Spec + plan exist                                        |
| 6     | dev-verify    | `implementation-done` completed                          |
| 7     | dev-finalize  | `verification-done` completed; honors `e2e_enabled`/`user_docs_enabled` internally |

**Interruptible**: at any gate the user may answer "stop" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the standard handoff block (next command + `/owflow:development <task-path>` resume hint) and end the session. The task resumes later in either mode.

---

## Exit Gate

When dev-finalize completes (`task.status: completed`):

1. Mark the final task item completed via `TaskUpdate`.
2. Present the workflow results box:

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DEVELOPMENT WORKFLOW COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <task name>

**Steps** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [executed step slugs]
**Verification** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [final verification outcome]
**Artifacts** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [task directory artifact summary]
**Commit message** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [template]
```

3. Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options: **Accept** (print follow-up suggestions: `/owflow:reviews-pragmatic <task-path>`, `/owflow:standards-update "<lesson>"`, commit/PR, then end) / **Adjust** (re-open the relevant `/owflow:dev-*` skill) / **Discuss** (walk through the summary) / **Stop here** (print the resume command and end).

Then end. No further owflow phase commands are required.

---

## Loop Rules

- **Delegate, never inline**: the wrapper only sequences ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all phase work happens inside subskills. If you catch yourself implementing/analyzing outside a subskill, STOP and invoke the subskill instead.
- **State is the truth**: gates and routing read `orchestrator-state.yml`, not memory. Re-read after every subskill returns.
- **Same state schema as assisted mode**: `completed_phases` step slugs (`codebase-analysed` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `task-completed`) are identical; resume works across modes.

## Command Integration

Invoked via:

- `/owflow:goal-development [description] [--e2e] [--user-docs] [--research=PATH]` (new)
- `/owflow:goal-development [task-path] [--from=<step-slug>]` (resume)

Alternative: `/owflow:development` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â same task in assisted mode (one subskill per invocation, fresh context each phase).
