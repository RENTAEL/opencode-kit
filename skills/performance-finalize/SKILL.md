---
name: performance-finalize
description: "Terminal step of the performance workflow. Summarizes the bottlenecks found, the optimizations applied, and the verification outcome; confirms correctness with the user; records `task-completed` only after the user accepts the results box (state is marked complete only after t..."
---
# Performance Finalize ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Completion & Commit Guidance (task-completed)

Terminal step of the performance workflow. Summarizes the bottlenecks found, the optimizations applied, and the verification outcome; confirms correctness with the user; records `task-completed` only after the user accepts the results box (state is marked complete only after the gate response); and owns the commit guidance. No new analysis ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â finalization is inline-legal. State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads it on entry and writes results on exit.

Related steps: all performance subskills (`/owflow:performance-analyze` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-spec` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-plan` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-implement` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-verify`). This is the terminal skill: its Exit-Gate acceptance is where the goal-performance wrapper's loop ends.

## Entry Gate

Resolve the argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). The argument may be:

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/performance/` (e.g., `2026-10-02-api-latency`); resolve to its path.
- **Description** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â anything else (free text) is treated as a new performance task description: ask via `question` whether to start a fresh standard task at this step (mid-pipeline bootstrap) or route through `/owflow:performance <description>`; on decline, print the blocked block and STOP.
- If the argument is **missing**, the path does **not exist**, or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):

1. Steps that must be completed first (in order), each with its command:
   - Codebase & bottleneck analysis (`codebase-analysed`, `bottlenecks-identified`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-analyze <task-path>`
   - Requirements, specification & conditional audit (`spec-written`, `spec-audited`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-spec <task-path>`
   - Implementation planning (`plan-created`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-plan <task-path>`
   - Implementation (`implementation-done`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-implement <task-path>`
   - Verification & issue resolution (`options-chosen`, `verification-done`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:performance-verify <task-path>`
2. List available performance-task identifiers (directories under `.owflow/tasks/performance/`) to resume from, if any.
3. Hint: `Run /owflow:performance <description> to start a task from scratch, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill | Where verified                                                              | Produced by                              |
| ----------------------- | --------------------------------------------------------------------------- | ---------------------------------------- |
| State file exists       | `<task-path>/orchestrator-state.yml`                                        | `/owflow:performance <desc>`             |
| Verification done       | `verification-done` in `completed_phases` + `verification/implementation-verification.md` exists | `/owflow:performance-verify <task-path>` |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `task-completed`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard performance task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No performance task found at <path>. Run /owflow:performance <description> to start a task from scratch.` and STOP.
2. **Skip/resume**: if `task.status` is `completed`, report the existing finalization (the results box from the Finalization step below) and STOP.
3. **Prerequisite check (presence and content)**: `verification-done` in `completed_phases` AND `verification/implementation-verification.md` exists. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP:
   - Steps that must be completed first: verification (`verification-done`).
   - `Run /owflow:performance-verify <task-path> first` (or the command for the earliest missing earlier step).
   - If no task exists yet: `Run /owflow:performance <description> to start a task from scratch.`

## Execute

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â finalization is inline-legal (creating the summary, updating metadata, and presenting results are direct steps; no agents involved).

### Finalization (`task-completed`, inline)

1. **Inventory results** (state-only; no new files): bottlenecks from `performance_context.bottleneck_priorities` and `performance_context.phase_summaries.bottleneck_analysis`; optimizations from `performance_context.phase_summaries.implementation` and `implementation/work-log.md`; verification outcome from `verification_context.last_status` and `verification/implementation-verification.md`.
2. **Present the results box** (the workflow-level box ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â single box, not two):

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ PERFORMANCE WORKFLOW COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <task name>

**Bottlenecks found** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [P0/P1/P2/P3 counts]
**Optimizations applied** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [count + key ones]
**Verification** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [final verdict]
**Estimated improvement** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [range from the analysis]

**Artifacts**

- `analysis/performance-analysis.md`
- `implementation/work-log.md`
- `verification/implementation-verification.md`
```

3. **Do NOT write `task-completed` yet** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the Exit Gate below owns the write, and it happens only after the user answers the results-acceptance question (Accept, or explicit proceed-with-issues). State is marked complete only after the gate response; writing it here would make the Adjust option a dead end (the completed task short-circuits on re-entry).
4. **Prepare (do not print yet) the commit guidance** (owned by this skill): a conventional commit message template referencing the task name, and the artifact set that belongs in the commit. It is printed on Accept, together with the closing guidance.

## State Update Convention (per step)

Apply after EVERY step above:

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â update `orchestrator-state.yml` as soon as the step completes, appending ONLY the step slug actually performed (`task-completed`) plus that step's fields. `task-completed` is the one slug written **only after the user answers the Exit-Gate acceptance question (Accept, or explicit proceed-with-issues)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never before the gate. Never batch multiple steps into one end-of-skill write.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if finalization fails, do NOT append `task-completed` to `completed_phases`; instead append it to `orchestrator.failed_phases` and increment `auto_fix_attempts["task-completed"]`.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-performance.yml`. Fix any reported issue immediately before proceeding.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run to confirm the full state matches everything performed in this session.

## Recovery

| Step                      | Max Attempts | Strategy     |
| ------------------------- | ------------ | ------------ |
| Completion (`task-completed`) | 0        | Summary only |

## Exit Gate

Present results, get user confirmation, then close the workflow (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill. **This acceptance is where the goal-performance wrapper's loop ends** (Accept = the wrapper proceeds to its own wrapper Exit Gate; any other option ends the loop with the standard handoff block).

### Results box

The results box from the Finalization step above IS the workflow-level results box ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â present it here as-is (single box, not two).

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â record `task-completed` (state write below), then print the closing guidance: the commit message template, the artifact set, and the next steps.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-run the affected earlier step (e.g., `/owflow:performance-implement <task-path>` for additional optimizations, or `/owflow:performance-verify <task-path>` for another verification round), then re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through bottleneck findings, optimization rationale, and measurement caveats in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:performance-finalize <task-path>`) and end.

**On Accept only**, perform the state write: append `task-completed` to `completed_phases` and set `task.status: completed`; bump `orchestrator.updated`; do NOT write a finalize slot under `performance_context.phase_summaries` (the template has no such slot ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â finalization is state-only). On failure: append `task-completed` to `failed_phases`, increment `auto_fix_attempts["task-completed"]`. Then re-read state + run `verify_template`. On **Adjust / Discuss / Stop here**, perform NO state write ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the workflow stays resumable.

### Next steps (after Accept)

The workflow is finished; no further owflow step is required. All follow-ups are `optional` (post-completion work, none advance phases):

- Run the application and verify the improvements manually; consider profiling with runtime tools to measure actual impact; monitor production metrics after deployment.
- Address remaining P2/P3 bottlenecks if needed.
- `/owflow:standards-update "<lesson learned>"` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â captures optimization patterns as project standards; does not advance phases.
- Commit the changes using the provided message template; open a PR. (Manual steps outside owflow.)

Then STOP.
