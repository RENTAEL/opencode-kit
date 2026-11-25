---
name: migration-fix
description: "Conditional work phase of the migration workflow. Activates only when the verification state fact says fixable issues remain. Runs the shared [Fix Loop Contract](../orchestrator-framework/references/fix-loop-contract.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â max 3 iterations, re-invoke `implemen..."
---
# Migration Fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conditional Issue Resolution (issues-resolved)

Conditional work phase of the migration workflow. Activates only when the verification state fact says fixable issues remain. Runs the shared [Fix Loop Contract](../orchestrator-framework/references/fix-loop-contract.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â max 3 iterations, re-invoke `implementation-verifier`, `fixes_applied` written immediately per iteration ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â with the migration deltas (compatibility verdict invalidation, data-integrity HALT). **Data-integrity problems are NEVER auto-fixed.**

## Entry Gate

### 1. Argument resolution

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/migrations/` (e.g., `2026-01-12-framework-upgrade`); resolve to its path.
- Missing argument, a path that does **not exist**, or no identifier match ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block (part 3), then STOP. Never guess or auto-pick a task.

### 2. Prerequisites

| Required for this skill | Where verified                                                                                          | Produced by                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| State file exists       | `<task-path>/orchestrator-state.yml`                                                                    | `/owflow:migration <description>` (dispatcher init) or mid-pipeline bootstrap |
| Verification done       | `verification-done` in `completed_phases` **and** `verification/implementation-verification.md` exists   | `/owflow:migration-verify <task-path>` |
| Fixable issues exist    | `verification_context.compatibility_status = failed` **or** (`verification_context.last_status != passed` and no recorded deliberate skip); the verification/compatibility reports list fixable critical/warning issues, **or** a deliberate skip is already recorded with `compatibility_status = passed` (settled ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â route forward) | `/owflow:migration-verify <task-path>` |

### 3. Blocked output

1. Steps that must be completed first (in order), each with its command:
   - Verification (`verification-done`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-verify <task-path>`
   - Migration execution (`migration-executed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-implement <task-path>` (if also missing)
   - Implementation planning (`plan-created`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-plan <task-path>` (if also missing)
   - Strategy specification (`strategy-specified`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-spec <task-path>` (if also missing)
   - Target state planning (`target-planned`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-target <task-path>` (if also missing)
   - Current-state analysis (`state-analysed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration-analyze <task-path>` (if also missing)
   - State initialization ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:migration <description>` (new task)
2. List available migration-task identifiers (directories under `.owflow/tasks/migrations/`) to resume from, if any.
3. Hint: `Run /owflow:migration <description> to start a migration task from scratch, or pass a task path/identifier to resume.`

Then STOP ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never guess or auto-pick a task.

### 4. Missing-state bootstrap

When the only unmet prerequisite is the state file, use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "No task exists at this path. Create a fresh standard migration task and start at `issues-resolved`?" with **Create task** / **Decline**.

- **On confirm**: create `.owflow/tasks/migrations/YYYY-MM-DD-task-name/` + `orchestrator-state.yml` from the migration template with `orchestrator.entry_point: "migration-fix (mid-pipeline bootstrap)"`, `orchestrator.started_phase: issues-resolved`, `completed_phases: []`, `task.title`/`task.description` from the argument. Run `verify_template` (`orchestrator-state-migration.yml`) immediately. Creates state ONLY ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `verification/implementation-verification.md` still blocks, so bootstrapping never skips upstream work.
- **On decline**: print `No migration task found at <path>. Run /owflow:migration <description> to start a migration task from scratch.` and STOP.

### 5. Skip/resume ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â artifacts before state

- `issues-resolved` is present with **non-empty** `verification_context.fixes_applied` **or a recorded approval in `verification_context.decisions_made`** (its state-resident marker) ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ report the existing fixes/decision and route to the Exit Gate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **except** when `compatibility_status != passed`, where part 6 activation keeps the failed check active and routes to `/owflow:migration-verify <task-path>`.
- `issues-resolved` is present with neither a non-empty `fixes_applied` nor a recorded approval ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ **drop** the slug and re-run ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never trust a bare slug.
- A deliberate skip recorded in `phase_summaries.fix.summary` + `decisions_made` ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ **settled for verifier issues**: report it and route to `/owflow:migration-finalize <task-path>` **only when `compatibility_status = passed`**; when `compatibility_status = failed`, the skip does not waive the failed check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â present the compatibility failure (data-integrity ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ HALT/rollback) and route to `/owflow:migration-verify <task-path>`; never re-open verifier issues.
- `issues-resolved` is absent while `verification/implementation-verification.md` + `verification-done` hold ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ normal entry; when `fixes_applied` is already non-empty from an interrupted run, report those fixes and resume the loop without re-applying them.
- Settled `verification_context.decisions_made` entries are reported, not re-asked.

### 6. Conditional activation

Read the **state facts** `verification_context.last_status` + `verification_context.compatibility_status` and the verification/compatibility reports. A recorded deliberate skip deactivates with `Fix deliberately skipped ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â issue resolution settled.` **only when `compatibility_status = passed`**; otherwise, when inactive ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `last_status = passed` **and** `compatibility_status = passed`, and the reports list no fixable critical/warning issues ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print exactly:

`No fixable issues ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â issue resolution not required.`

and route to `/owflow:migration-finalize <task-path>` (required next: operator guide when enabled, then task completion), then STOP. **No flag, no user choice** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the state facts decide activation.

### 7. Recovery

| Step                       | Max Attempts | Strategy                                                                                                       |
| -------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------- |
| Fix loop (`issues-resolved`) | 3 iterations | Contract, not a retry counter: fix-then-reverify; at 3 ask proceed-with-warnings or rollback. **Data integrity: HALT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never auto-fixed** |

## Execute

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md), the [Fix Loop Contract](../orchestrator-framework/references/fix-loop-contract.md), and [Issue Resolution](../orchestrator-framework/references/orchestrator-patterns.md) (Section 6).

| Direction | Artifact                                        | Producer                                                              |
| --------- | ----------------------------------------------- | --------------------------------------------------------------------- |
| Consumed  | `verification/implementation-verification.md`   | `implementation-verifier` via `migration-verify`                      |
| Consumed  | `verification/compatibility-test-results.md`    | `migration-verify` (data-integrity and rollback evidence)             |
| Produced  | migrated code fixes + state `fixes_applied`     | direct execution (this skill)                                         |
| Produced  | updated `verification/implementation-verification.md` | re-invoked `implementation-verifier` (**Skill**)                |

### User-Driven Fix Loop (`issues-resolved`)

1. **Display the detailed issue breakdown** grouped by category and severity (location, description, fixability).
2. **Present critical + warning issues as a numbered list.**
3. `question` per the [Fix Loop Contract](../orchestrator-framework/references/fix-loop-contract.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Which issues should I fix?" with exactly three options: **"Fix all fixable issues"** / **"Let me choose specific issues"** / **"Skip fixes, proceed as-is"**.
4. **Fix the selected issues directly** (the migrated code is this skill's artifact). **Immediately** after each fix, append it to `verification_context.fixes_applied` in state ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never deferred to the end; bump `orchestrator.updated`; re-read + `verify_template`. After fixes set `options.skip_test_suite: false` (code changed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the suite must re-run on re-verification) **and invalidate the stale compatibility verdict: `verification_context.compatibility_status: null`** (field-level fail-closed exception ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the 4 checks ran against pre-fix code; only `migration-verify` may set a new verdict).
5. `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Re-run verification to check fixes?" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **"Yes, re-run verification"** / **"No, proceed to next phase"**. On yes: Skill tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `implementation-verifier`; then **immediately** update `verification_context.reverify_count` **and refresh `verification_context.last_status` + `issues_found` from the verifier's structured return** (field-level re-verify exception ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the fix loop replaces the verification result), then return to step 1 (max 3 iterations). `compatibility_status` stays `null` (invalidated by the fixes) or `failed` and remains owned by `migration-verify`: when it is not `passed`, the loop's required next step is `/owflow:migration-verify <task-path>` (its re-verification re-runs the compatibility checks and settles the verdict) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never route a non-passed compatibility status to finalize. On "No", exit the loop to the Exit Gate, where the same required-next rule applies. Single-writer split: `migration-verify` owns `last_status`/`issues_found`/`compatibility_status`; this skill owns `fixes_applied`, `reverify_count`, `decisions_made`, plus the re-verify refresh of `last_status`/`issues_found` and the fail-closed invalidation of `compatibility_status`.
6. **Record each user decision** (specific selection, proceed-with-warnings, deliberate skip) in `verification_context.decisions_made`.

**Data Safety ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â HALT**: any data-integrity issue (from the verification report, a compatibility result, or discovered while fixing) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ HALT: never auto-fix data problems, never run a destructive data repair. Present the issue with the rollback option. **Rollback happens only on explicit user confirmation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no automatic rollback or revert ever.** A deliberate skip cannot waive a data-integrity failure or any non-passed compatibility check.

**Exit conditions (surfaced as results-box glyphs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never Exit-Gate state mutations)**:

- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ no critical issues remain ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ append `issues-resolved` and proceed.
- ÃƒÂ¢Ã…Â¡Ã‚Â  max 3 iterations reached ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Proceed with known issues?" / "Rollback": proceed ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ append `issues-resolved` with the approval recorded in `decisions_made`; rollback ÃƒÂ¢Ã¢â‚¬Â¡Ã¢â‚¬â„¢ do NOT append, record the decision, and HALT for user-confirmed rollback.
- ÃƒÂ¢Ã‚ÂÃ…â€™ data integrity ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ HALT immediately, recommend user-confirmed rollback; do NOT append `issues-resolved`; record `failed_phases` + increment `auto_fix_attempts["issues-resolved"]`.
- Deliberate skip ("Skip fixes, proceed as-is") ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ a user-chosen skip, not a failure: no `issues-resolved` slug, no failure entry; record the reason in `phase_summaries.fix.summary` + `decisions_made`. `migration-finalize` accepts this settled skip **only when `compatibility_status = passed`**; `compatibility_status = failed` remains an absolute finalize blocker (re-verify after fixes, or user-confirmed rollback).

## State Update Convention (per step)

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `fixes_applied` after every fix (never batched); `reverify_count`/`decisions_made` **and the `last_status`/`issues_found` refresh** right after each verifier run or decision; `issues-resolved` only when the loop settles successfully (ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦, or an approved ÃƒÂ¢Ã…Â¡Ã‚Â ). Never defer and never append on a deliberate skip.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a HALT or failed fix iteration is NOT appended to `completed_phases`; append `issues-resolved` to `orchestrator.failed_phases` and increment `auto_fix_attempts["issues-resolved"]`.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-migration.yml`. Fix any reported issue immediately.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run.

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ MIGRATION FIX COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <task name>

**Iterations** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [N of max 3]
**Fixes applied** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [count + 1-line list]
**Remaining issues** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [by severity / none]
**Re-verification** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ passed / ÃƒÂ¢Ã…Â¡Ã‚Â  passed_with_issues / ÃƒÂ¢Ã‚ÂÃ…â€™ failed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â N re-runs]
**Data integrity** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ no data issues / ÃƒÂ¢Ã‚ÂÃ…â€™ HALT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rollback recommended (user confirmation required)]
**Decisions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [proceed-with-warnings / deliberate skip / specific selection]

**Artifacts**

- migrated code fixes
- `verification/implementation-verification.md` (updated by re-verification runs)
- state `verification_context.fixes_applied`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the fixes (or the approved proceed-with-warnings / deliberate skip) are good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix additional selected issues and/or run another verification round within the max-3 contract, update state and the report, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through specific fixes, remaining issues, or the data-integrity HALT in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:migration-fix <task-path>`) and end.

### Next steps (after Accept)

Render ONLY the row whose condition matches the state:

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:migration-verify <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when `verification_context.compatibility_status != passed` (failed, or invalidated to null by applied fixes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a verifier-only re-run cannot settle compatibility): re-verification re-runs the 4 checks and owns `compatibility_status`. Remaining after: finalize.
- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:migration-finalize <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when `compatibility_status = passed` (after a ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ loop, an approved ÃƒÂ¢Ã…Â¡Ã‚Â , or a deliberate skip): closes the workflow (authors the operator guide when `options.docs_enabled` is true, then completes the task). Remaining after: none ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â workflow ends.

**Other options**:

- After a ÃƒÂ¢Ã‚ÂÃ…â€™ data-integrity HALT with **user-confirmed rollback only**: restore to the last known-good state per `analysis/rollback-plan.md`, then re-enter `/owflow:migration-verify <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional`, manual, never automatic.
- `/owflow:goal-migration <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` shortcut: runs the remaining phases in one loop (finalize)

Then STOP.
