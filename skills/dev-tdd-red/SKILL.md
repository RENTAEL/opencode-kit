---
name: dev-tdd-red
description: "Work phase of the development workflow. Writes a failing test proving the defect exists, before any implementation. Only runs when the gap analysis detected a reproducible defect."
---
# Dev TDD Red ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â TDD Red Gate (tdd-red-proven)

Work phase of the development workflow. Writes a failing test proving the defect exists, before any implementation. Only runs when the gap analysis detected a reproducible defect.

## Entry Gate

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/development/` (e.g., `2026-01-12-my-task`); resolve to its path.
- If the argument is **missing**, the path does **not exist**, or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):
  1. Steps that must be completed first (in order), each with its command:
     - Codebase & gap analysis (`codebase-analysed`, `gap-analysed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:dev-analyze <task-path>`
  2. List available dev-task identifiers (directories under `.owflow/tasks/development/`) to resume from, if any.
  3. Hint: `Run /owflow:development <description> to start a task from scratch, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill        | Where verified                                                                                         | Produced by                      |
| ------------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| State file exists              | `<task-path>/orchestrator-state.yml`                                                                   | `/owflow:development <desc>`     |
| Analysis done                  | `gap-analysed` in `completed_phases`                                                                   | `/owflow:dev-analyze <task-path>`|
| Defect is reproducible         | `task_context.task_characteristics.has_reproducible_defect: true`                                      | `/owflow:dev-analyze <task-path>`|

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `tdd-red-proven`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard development task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No development task found at <path>. Run /owflow:development <description> to start a task from scratch.` and STOP.
2. **Skip/resume**: if `tdd-red-proven` is in `completed_phases`, report the existing `implementation/tdd-red-gate.md` results and route to the Exit Gate.
3. **Conditional activation**: read `task_context.task_characteristics.has_reproducible_defect`. If `false` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No reproducible defect detected ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â TDD red gate not required.` and suggest `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:dev-spec <task-path>` (required next phase: turns analysis into a user-approved specification; remaining plan plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize), then STOP.
4. **Prerequisite check**: `gap-analysed` must be in `completed_phases`. If not ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP:
   - Steps that must be completed first: codebase & gap analysis (`codebase-analysed`, `gap-analysed`).
   - Run `/owflow:dev-analyze <task-path> first.`
   - If no task exists yet: `Run /owflow:development <description> to start a task from scratch.`

## Execute

Direct execution (no delegation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is a targeted, single-test task):

1. Read `analysis/clarifications.md`, `analysis/gap-analysis.md`, and the affected files identified by the analysis to understand the defect.
2. Write ONE focused test that reproduces the defect (correct test framework for the project ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check existing test setup).
3. Run the test. **It MUST fail** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a failing result proves the defect exists. If it passes unexpectedly, the defect is not reproduced: revise the test or report the mismatch via `question`.

**Critical**: Do NOT fix anything. Do NOT write implementation code. The test failing is the deliverable.

## State Update Convention (per step)

1. **On success** (test fails as expected, red gate proven): immediately append `tdd-red-proven` to `completed_phases` and set `task_context.tdd_red_passed: true`; bump `orchestrator.updated`.
2. **On failure or abandoned retries** (test framework issues, imports that could not be resolved): do NOT append to `completed_phases`; append `tdd-red-proven` to `orchestrator.failed_phases` and increment `auto_fix_attempts["tdd-red-proven"]`; document the blocker in `task_context.gaps`.
3. **On user-chosen skip** (via `question` after repeated failures): record the skip with the failure reason in `task_context.gaps` and set `task_context.tdd_red_passed: false` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no `completed_phases` entry, no `failed_phases` entry (it was a deliberate decision, not a failure).
4. **Timestamp + validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` on every write; after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-development.yml`. Fix any reported issue immediately.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run.

Retry rule: on repeated failures (test framework issues, imports) retry up to 2 times (rewrite test, fix setup). Still failing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `question`: continue trying, or skip TDD with the failure documented in state (per rule 3).

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ TDD RED GATE COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <task name>

**Test** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <test name> (`<test file path>`)
**Result** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ÃƒÂ¢Ã‚ÂÃ…â€™ FAILED as expected ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â defect reproduced
**Failure** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <1-line key failure output proving the defect>

**Artifacts**
- `implementation/tdd-red-gate.md`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the failing test faithfully reproduces the defect; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â revise the test (different conditions, better assertion), re-run, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through the reproduction reasoning (defect path, why the test fails) in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:dev-tdd-red <task-path>`) and end.

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:dev-spec <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` next: turns analysis plus this red test into a user-approved specification (the test becomes the acceptance criterion for the fix). Remaining after: plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.

**Other options**:

- `/owflow:goal-development <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` shortcut: runs all remaining phases in one loop (spec ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize)

Then STOP.
