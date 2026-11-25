---
name: dev-plan
description: "Work phase of the development workflow. Delegates planning to break the specification into task groups with dependencies, then refines the plan with an execution diagram."
---
# Dev Plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Implementation Planning (plan-created)

Work phase of the development workflow. Delegates planning to break the specification into task groups with dependencies, then refines the plan with an execution diagram.

Supports a **quick mode** (`--quick`, or any description argument with no existing task): a condensed prelude that bootstraps a standard development task (state file, standards discovery, quick analysis, condensed spec) and then writes the implementation plan directly on the fly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no planner subagent. After the Exit Gate, the pipeline can either stop there ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the plan alone may be enough ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or continue with `/owflow:dev-implement`. The task is a regular development task, resumable by any dev-* subskill.

## Entry Gate

Resolve the argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). The argument may be:

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/development/` (e.g., `2026-01-12-my-task`); resolve to its path.
- **Description** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â anything else (quoted free text, e.g. `"Add a logout button to the navbar"`) is treated as a new task description for quick bootstrap.

Route by argument kind and flags:

| Situation                                                        | Route                                        |
| ---------------------------------------------------------------- | -------------------------------------------- |
| Task path/identifier, state + spec exist                          | Normal planning below                        |
| Task path/identifier, `--quick`, state or spec missing            | Quick bootstrap/prelude for the missing pieces, then normal planning |
| Description argument, `--quick` (or no argument after prompt)     | Quick bootstrap (create task + condensed prelude), then normal planning |
| Description argument, no `--quick`                                | Ask via `question`: quick plan-only task / full pipeline (blocked block below) / cancel |
| Missing argument                                                  | Prompt for input (path, identifier, or description), then re-route |

If the path does **not exist** or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):

1. Steps that must be completed first (in order), each with its command:
   - Codebase & gap analysis (`codebase-analysed`, `gap-analysed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:dev-analyze <task-path>`
   - TDD red gate (`tdd-red-proven`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when a reproducible defect was detected ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:dev-tdd-red <task-path>`
   - Requirements, specification & audit (`spec-written`, `spec-audited`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:dev-spec <task-path>`
2. List available dev-task identifiers (directories under `.owflow/tasks/development/`) to resume from, if any.
3. Hint: `Run /owflow:development <description> to start a task from scratch, /owflow:dev-plan --quick "<description>" for a quick plan-only task, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill | Where verified                                       | Produced by                      |
| ----------------------- | ---------------------------------------------------- | -------------------------------- |
| State file exists       | `<task-path>/orchestrator-state.yml`                 | `/owflow:development <desc>` or quick bootstrap |
| Spec approved           | `implementation/spec.md` exists                      | `/owflow:dev-spec <task-path>` or quick prelude |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ quick bootstrap (see Quick Mode), otherwise mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `plan-created`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bootstrap a fresh standard task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print: `No development task found at <path>. Run /owflow:development <description> to start a task from scratch, or /owflow:dev-plan --quick "<description>" for a quick plan-only task.` and STOP.
2. **Skip/resume**: if `plan-created` is in `completed_phases`, report the existing plan summary and route to the Exit Gate.
3. **Prerequisite check**: `implementation/spec.md` exists (spec approved during `spec-written`). If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run the Quick prelude for the missing pieces (`--quick` or user chooses quick), otherwise print the blocked block, then STOP:
   - Steps that must be completed first: analysis (`codebase-analysed`, `gap-analysed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ TDD red gate (`tdd-red-proven`, only when a reproducible defect was detected) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ specification (`spec-written`).
   - `Run /owflow:dev-spec <task-path> first` (or `/owflow:dev-analyze <task-path>` if analysis is also missing).
   - If no task exists yet: `Run /owflow:development <description> to start a task from scratch, or /owflow:dev-plan --quick "<description>" for a quick plan-only task.`

## Quick Mode (condensed prelude ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plan on the fly)

Quick mode produces the same artifacts as the early pipeline phases ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just condensed into one pass inside this skill. It does NOT introduce a second state format: the task gets a standard `orchestrator-state.yml` and standard artifacts, so every other dev-* subskill can pick it up afterwards.

### Quick bootstrap (no state file, description argument)

1. **Create Task Directory**: `.owflow/tasks/development/YYYY-MM-DD-task-name/` (3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 kebab-case words from the description).
2. **Initialize State**: create `orchestrator-state.yml` from the development template with `task.title` / `task.description` from the description, `task.status: in_progress`, and `orchestrator.entry_point: "dev-plan --quick"`.
   - **CRITICAL**: use the `verify_template` tool immediately after creation to check YAML validity against `orchestrator-state-development.yml`.
3. **Discover project documentation**: read `.owflow/docs/INDEX.md` (if exists) and extract the Project Documentation file paths into `project_context.project_doc_paths` (matching the development dispatcher's initialization).
4. If `.owflow/docs/` does not exist, proceed without standards and note the graceful-fallback hint in the completion message: `"No AI SDLC standards found. Consider running /owflow:flow-init to initialize project documentation and coding standards."`

### Quick prelude (one condensed pass)

**MANDATORY order ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â standards before analysis, analysis before spec/plan:**

1. **Standards discovery**: identify applicable standards from INDEX.md by task keywords (e.g., "API" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ api/error-handling, "form" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validation/accessibility) and **READ each applicable standard file** with the Read tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reading INDEX.md alone is NOT sufficient. Record the paths in `project_context.standards_applied` (extra state field).
2. **Brief codebase analysis**: explore the affected areas (Glob, Grep, Read) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â enough to identify affected files/modules, existing patterns, and constraints that inform the plan. Write `analysis/quick-analysis.md` (affected files, approach sketch, standards referenced). Extract a 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“2 sentence summary into `phase_summaries.quick_analysis`.
3. **Condensed spec**: write `implementation/spec.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â goal, scope (in/out), requirements, applicable standards with key guidelines, verification criteria. Mark `spec-written` complete (`phase_summaries.specification` summary).
4. **Condensed plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â written directly, NO delegation**: write `implementation/implementation-plan.md` on the fly, keeping the executor-compatible shape (1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 task groups, `Dependencies:` per group, `- [ ] N.1 / N.2 / ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` steps, acceptance criteria per group) and applying these quality rules:
   - **Key discoveries first** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â open with 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 discoveries from the quick analysis, each with a `file:line` reference (pattern to follow, constraint to respect, existing component to reuse).
   - **"What We're NOT Doing"** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an explicit out-of-scope list to fence scope creep.
   - **Intent before implementation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each step names WHAT and WHY (intent) plus the touched interface or invariant (contract: route, signature, schema field, invariant). No code snippets unless the change is genuinely non-obvious.
   - **Verification split** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â acceptance criteria distinguish automated checks (specific test commands) from manual checks.
   - **No open questions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every decision is made before the plan is final; resolve ambiguities during the quick analysis (decide, or ask via `question`), never write TBDs.
   This REPLACES the `implementation-planner` delegation in Execute below (quick mode is the only exception to the delegation anti-pattern). Mark `plan-created` complete (`phase_summaries.planning` summary).

The TDD red gate is SKIPPED in quick mode (no `tdd-red-proven`), and `spec-audited` is skipped ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â plan approval at the Exit Gate substitutes for the audit.

Then continue with the **Post-Plan Diagram** gate below (both modes).

## Execute (full pipeline ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â delegated planning)

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md).

**ANTI-PATTERN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never write implementation-plan.md yourself in the full pipeline. "This is simple enough to plan inline" is NOT a reason to skip delegation. (Quick mode is the ONLY exception ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â its prelude step 4 writes the plan directly and skips this section.)**

Task tool - `implementation-planner`. Pass: task_path, task_description, task_characteristics, `phase_summaries` (specification, gap_analysis, codebase_analysis), research/quick context if present in state. Output: `implementation/implementation-plan.md`.

## Post-Plan Diagram (optional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â both modes)

1. **Diagram gate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `question`: "Add an execution diagram to the implementation plan?" Options:
   - **Add diagram** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run the refinement step below.
   - **Skip diagram** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the plan stays as-is; neither choice affects plan approval.
2. Only on **Add diagram** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Skill tool - `diagrams-mermaid` on `implementation/implementation-plan.md` (content-preserving): add a compact execution diagram (task-group dependency flow or phase/state view). Implementation steps remain authoritative; diagrams are explanatory. If refinement fails, note it and continue ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the plan itself is unaffected.

## State Update Convention (per step)

1. **On success** (implementation-plan.md written ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the diagram is optional and its absence does NOT block success): immediately append `plan-created` to `completed_phases`; write 1-2 sentence summary to `phase_summaries.planning`; bump `orchestrator.updated`.
   - In quick mode, ALSO append the prelude slugs on their individual completions (never batched into one end-of-skill write): `codebase-analysed` and `gap-analysed` after the quick analysis (quick analysis covers both; note the condensation in `phase_summaries.codebase_analysis` / `phase_summaries.gap_analysis`), `spec-written` after the condensed spec (summary in `phase_summaries.specification`), and `plan-created` after the condensed plan (written directly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no delegation).
2. **On failure** (planner fails in the full pipeline, or the quick-mode plan is incomplete): do NOT append to `completed_phases`; append `plan-created` to `orchestrator.failed_phases` and increment `auto_fix_attempts["plan-created"]`. A declined or failed diagram refinement is NOT a failure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â note it in `phase_summaries.planning` and proceed.
3. **Timestamp + validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` on every write; after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-development.yml`. Fix any reported issue immediately.
4. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run.

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DEV PLAN COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <task name>

**Task groups** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [N]
**Total steps** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [M]
**Dependencies** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [key ordering constraints, 1-2 lines]
**Complexity** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [estimated complexity]
**Entry point** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [quick bootstrap (`--quick`) / full pipeline]
**Diagram** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [added / skipped (optional)]

**Artifacts**
- `implementation/implementation-plan.md`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the plan is good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â regenerate the plan with the user's corrections (grouping, ordering, scope), update state, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through the plan structure (task groups, dependencies, step breakdown) in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:dev-plan <task-path>`) and end. The task is a regular development task; `/owflow:dev-implement <task-path>` (or `/owflow:development <task-path>`) continues the pipeline later.

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:dev-implement <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` next: executes the plan task group by task group via subagents (includes the TDD green gate when a red gate exists). Remaining after: verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize. If the plan alone was the goal, stop here ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task stays resumable.
- `/owflow:dev-implement --quick <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` condensed alternative: implements the plan directly in the main agent with standards instead of delegating to subagents.

**Other options**:

- `/owflow:goal-development <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` shortcut: runs all remaining phases in one loop (implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize)

Then STOP.
