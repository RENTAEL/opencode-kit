---
name: migration-implement
description: "Work phase of the migration workflow. Executes `implementation/implementation-plan.md` task group by task group through isolated per-group delegation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **normal lane only, no quick lane** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and records the execution in state. The delegation ow..."
---
# Migration Implement ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Plan Execution & Work Log (migration-executed)

Work phase of the migration workflow. Executes `implementation/implementation-plan.md` task group by task group through isolated per-group delegation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **normal lane only, no quick lane** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and records the execution in state. The delegation owns checkboxes, the work log, incremental tests, standards discovery, and its own user-confirmed failure handling; this shell owns the state write.

## Entry Gate

### 1. Argument resolution

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/migrations/` (e.g., `2026-01-12-framework-upgrade`); resolve to its path.
- Missing argument, a path that does **not exist**, or no identifier match ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block (part 3), then STOP. Never guess or auto-pick a task.

### 2. Prerequisites

| Required for this skill | Where verified                                                          | Produced by                          |
| ----------------------- | ----------------------------------------------------------------------- | ------------------------------------ |
| State file exists       | `<task-path>/orchestrator-state.yml`                                    | `/owflow:migration <description>` (dispatcher init) or mid-pipeline bootstrap |
| Plan created            | `plan-created` in `completed_phases` **and** `implementation/implementation-plan.md` exists | `/owflow:migration-plan <task-path>` |
| Spec present            | `implementation/spec.md` exists (the executor's input contract)          | `/owflow:migration-spec <task-path>` |

### 3. Blocked output

1. Steps that must be completed first (in order), each with its command:
   - Implementation planning (`plan-created`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-plan <task-path>`
   - Strategy specification (`strategy-specified`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-spec <task-path>` (if also missing)
   - Target state planning (`target-planned`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-target <task-path>` (if also missing)
   - Current-state analysis (`state-analysed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-analyze <task-path>` (if also missing)
   - State initialization ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration <description>` (new task)
2. List available migration-task identifiers (directories under `.owflow/tasks/migrations/`) to resume from, if any.
3. Hint: `Run /owflow:migration <description> to start a migration task from scratch, or pass a task path/identifier to resume.`

Then STOP ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never guess or auto-pick a task.

### 4. Missing-state bootstrap

When the only unmet prerequisite is the state file, use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "No task exists at this path. Create a fresh standard migration task and start at `migration-executed`?" with **Create task** / **Decline**.

- **On confirm**: create `.owflow/tasks/migrations/YYYY-MM-DD-task-name/` + `orchestrator-state.yml` from the migration template with `orchestrator.entry_point: "migration-implement (mid-pipeline bootstrap)"`, `orchestrator.started_phase: migration-executed`, `completed_phases: []`, `task.title`/`task.description` from the argument. Run `verify_template` (`orchestrator-state-migration.yml`) immediately. Creates state ONLY ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `implementation/implementation-plan.md` still blocks, so bootstrapping never skips upstream work.
- **On decline**: print `No migration task found at <path>. Run /owflow:migration <description> to start a migration task from scratch.` and STOP.

### 5. Skip/resume ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â artifacts before state

- `implementation/work-log.md` exists but `migration-executed` is missing ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ **adopt**: append `migration-executed`, backfill `phase_summaries.implement.summary` and `migration_outputs.work_log` where still null.
- `migration-executed` is present but `implementation/work-log.md` is missing ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ **drop** `migration-executed` from `completed_phases` and re-run.
- Both artifact and slug exist ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ report the existing execution summary and route to the Exit Gate.
- A partially executed plan (unchecked groups remain) is NOT complete: resume with `/owflow:migration-implement <task-path>` so the per-group execution picks up the uncompleted groups.

### 6. Conditional activation

Not applicable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `migration-implement` has no activation condition; it runs whenever its prerequisites are met.

### 7. Recovery

| Step                          | Max Attempts | Strategy                                                                                                        |
| ----------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| Plan execution (`migration-executed`) | 5    | Fix syntax/import errors and re-run the failed group's tests; prompt the user on repeated failure. **Never auto-rollback ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rollback requires explicit user confirmation** |

## Execute

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md). The per-group execution applies its own test-driven order and continuous standards discovery.

| Direction | Artifact                            | Producer                                                             |
| --------- | ----------------------------------- | -------------------------------------------------------------------- |
| Consumed  | `implementation/implementation-plan.md` | `migration-plan` (approved plan with per-group rollback steps)   |
| Consumed  | `implementation/spec.md`            | `migration-spec` (approved specification)                            |
| Produced  | `implementation/work-log.md`        | per-group delegation to `task-group-implementer` (**Task tool**, normal lane only) |

### Plan Execution (`migration-executed`)

> **ANTI-PATTERN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never execute the plan's task groups inline. "The groups are straightforward" is NOT a reason to skip delegation.**

1. **Execute the plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-group delegation** (normal lane only; migration has no quick lane). For each task group in order: prepare context (task path, task description, the `implementation/spec.md` + `implementation/implementation-plan.md` paths, `migration_context.*` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â type, strategy, risk level, breaking changes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and accumulated `phase_summaries` from analyze ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plan), delegate the group via the **Task tool** to `task-group-implementer`, then process its report: mark the group's checkboxes in `implementation/implementation-plan.md`, append the work-log entry to `implementation/work-log.md`, and run the group's incremental tests before moving on. Apply lazy standards loading per group; after the last group, run the full test suite once.
2. **No post-continuation glue block** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the per-group execution's return is not a handoff to be glued: do NOT "re-read state to confirm you are the orchestrator", do NOT add a numbered phase marker, do NOT auto-proceed to verification. The monolith's post-continuation block existed only because the monolith owned the state writes; here the per-step write below is the only continuation.
3. **State write**: append `migration-executed` to `completed_phases`; set `phase_summaries.implement.summary`, `migration_outputs.work_log: "implementation/work-log.md"`; bump `orchestrator.updated`. On failure (per-group execution fails after its retries, user stops): do NOT append; append `migration-executed` to `failed_phases` and increment `auto_fix_attempts["migration-executed"]`; partial progress stays in `implementation/work-log.md`. Then re-read state + run `verify_template`.

## State Update Convention (per step)

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â update `orchestrator-state.yml` as soon as the step completes, appending ONLY the step slug actually performed (`migration-executed`) plus that step's fields. Never batch or defer to the end of the skill.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a failed or abandoned step is NOT appended to `completed_phases`; append its slug to `orchestrator.failed_phases` and increment `auto_fix_attempts["<slug>"]`.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-migration.yml`. Fix any reported issue immediately.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run.

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ MIGRATION IMPLEMENT COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <task name>

**Task groups** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [completed / total]
**Files changed** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [count + key files, 1-2 lines]
**Tests** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [incremental results + full-suite status from the executor]
**Work log** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `implementation/work-log.md`
**Rollback readiness** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [per-group checkpoints completed / deferred items]

**Artifacts**

- implemented migration changes
- `implementation/work-log.md`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the implementation matches the plan; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-work the affected task groups (fix code, re-run their tests), update state and the work log, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through implementation decisions, files changed, or deferred items in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:migration-implement <task-path>`) and end.

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:migration-verify <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` next: runs the verification options gate, the reused verifier, and the 4 migration compatibility checks. Remaining after: fix (only when verification finds issues) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.

**Other options**:

- `/owflow:goal-migration <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` shortcut: runs all remaining phases in one loop (verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix when needed ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize)

Then STOP.
