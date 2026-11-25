---
name: dev-spec
description: "Work phase of the development workflow. Resolves technical decisions, gathers requirements, creates the specification via delegation, refines it with diagrams, then offers an independent specification audit."
---
# Dev Spec ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Requirements, Specification & Audit (spec-written, spec-audited)

Work phase of the development workflow. Resolves technical decisions, gathers requirements, creates the specification via delegation, refines it with diagrams, then offers an independent specification audit.

Supports a **quick mode** (`--quick`, or any description argument with no existing task): a condensed prelude that bootstraps a standard development task (state file, standards discovery, quick analysis) and then writes the condensed specification directly on the fly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no specification-creator subagent. After the Exit Gate, the pipeline continues with `/owflow:dev-plan` (normal or `--quick`). The task is a regular development task, resumable by any dev-* subskill.

## Entry Gate

Resolve the argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). The argument may be:

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/development/` (e.g., `2026-01-12-my-task`); resolve to its path.
- **Description** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â anything else (quoted free text, e.g. `"Add a logout button to the navbar"`) is treated as a new task description for quick bootstrap.

Route by argument kind and flags:

| Situation                                                     | Route                                                                        |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Task path/identifier, no `--quick`, state + analysis exist    | Normal specification below                                                    |
| Task path/identifier, `--quick`, analysis done (spec missing) | Quick prelude step 3 only (condensed spec), then audit offer / Exit Gate      |
| Task path/identifier, `--quick`, analysis missing             | Quick bootstrap/prelude for the missing pieces, then condensed spec           |
| Description argument, `--quick` (or no argument after prompt) | Quick bootstrap (create task + condensed prelude + condensed spec)            |
| Description argument, no `--quick`                            | Ask via `question`: quick spec-only task / full pipeline (blocked block below) / cancel |
| Missing argument                                              | Prompt for input (path, identifier, or description), then re-route            |

If the path does **not exist** or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):

1. Steps that must be completed first (in order), each with its command:
   - Codebase & gap analysis (`codebase-analysed`, `gap-analysed`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:dev-analyze <task-path>`
   - TDD red gate (`tdd-red-proven`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when a reproducible defect was detected during analysis ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:dev-tdd-red <task-path>`
2. List available dev-task identifiers (directories under `.owflow/tasks/development/`) to resume from, if any.
3. Hint: `Run /owflow:development <description> to start a task from scratch, /owflow:dev-spec --quick "<description>" for a quick spec-only task, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill    | Where verified                                                                              | Produced by                                        |
| -------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| State file exists          | `<task-path>/orchestrator-state.yml`                                                        | `/owflow:development <desc>` or quick bootstrap    |
| Analysis done              | `gap-analysed` in `completed_phases` + `analysis/gap-analysis.md` exists                    | `/owflow:dev-analyze <task-path>` or quick prelude |
| TDD red gate (conditional) | `tdd-red-proven` in `completed_phases` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â required only when `has_reproducible_defect: true` | `/owflow:dev-tdd-red <task-path>`                  |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ quick bootstrap when invoked with `--quick` or a description argument (see Quick Mode), otherwise mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `spec-written`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard development task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No development task found at <path>. Run /owflow:development <description> to start a task from scratch, or /owflow:dev-spec --quick "<description>" for a quick spec-only task.` and STOP.
2. **Skip/resume**: if both `spec-written` and `spec-audited` are in `completed_phases`, report existing results and route to the Exit Gate. If only `spec-written` is complete: when `options.spec_audit_enabled: false` (quick task ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â audit skipped by design), report the existing spec summary and route to the Exit Gate; otherwise skip to the spec audit.
3. **Conditional activation (routing guard ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â both modes)**: if `task_context.task_characteristics.has_reproducible_defect` is `true` AND `tdd-red-proven` is NOT in `completed_phases` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (quick mode does NOT bypass a proven-defect red gate; the quick TDD lane for bug-shaped work is `/owflow:dev-bugfix`):
   - Steps that must be completed first: TDD red gate (`tdd-red-proven` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â required because a reproducible defect was detected); if analysis (`codebase-analysed`, `gap-analysed`) is also missing, start there.
   - `Run /owflow:dev-tdd-red <task-path> first (or /owflow:dev-analyze <task-path> if analysis is also missing).`
4. **Prerequisite check**: `gap-analysed` in `completed_phases` and `analysis/gap-analysis.md` exists. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run the Quick prelude for the missing pieces (when `--quick` or the user chooses quick), otherwise print the blocked block, then STOP:
   - Steps that must be completed first: codebase & gap analysis (`codebase-analysed`, `gap-analysed`).
   - `Run /owflow:dev-analyze <task-path> first.`
   - If no task exists yet: `Run /owflow:development <description> to start a task from scratch, or /owflow:dev-spec --quick "<description>" for a quick spec-only task.`

## Quick Mode (condensed prelude ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ spec on the fly)

Quick mode produces the same artifacts as the early pipeline phases ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just condensed into one pass inside this skill. It does NOT introduce a second state format: the task gets a standard `orchestrator-state.yml` and standard artifacts, so every other dev-* subskill can pick it up afterwards.

### Quick bootstrap (no state file, description argument)

1. **Create Task Directory**: `.owflow/tasks/development/YYYY-MM-DD-task-name/` (3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 kebab-case words from the description).
2. **Initialize State**: create `orchestrator-state.yml` from the development template with `task.title` / `task.description` from the description, `task.status: in_progress`, and `orchestrator.entry_point: "dev-spec --quick"`. Bug-shaped descriptions (symptom + expected vs actual) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ suggest `/owflow:dev-bugfix "<description>"` instead (TDD red gate discipline, same standard state) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â unless the user insists on proceeding here.
   - **CRITICAL**: use the `verify_template` tool immediately after creation to check YAML validity against `orchestrator-state-development.yml`.
3. **Discover project documentation**: read `.owflow/docs/INDEX.md` (if exists) and extract the Project Documentation file paths into `project_context.project_doc_paths` (matching the development dispatcher's initialization).
4. If `.owflow/docs/` does not exist, proceed without standards and note the graceful-fallback hint in the completion message: `"No AI SDLC standards found. Consider running /owflow:flow-init to initialize project documentation and coding standards."`

### Quick prelude (one condensed pass)

**MANDATORY order ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â standards before analysis, analysis before spec:**

1. **Standards discovery** (skip when `project_context.standards_applied` already lists the applicable standards): identify applicable standards from INDEX.md by task keywords (e.g., "API" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ api/error-handling, "form" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validation/accessibility) and **READ each applicable standard file** with the Read tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reading INDEX.md alone is NOT sufficient. Record the paths in `project_context.standards_applied` (extra state field).
2. **Brief codebase analysis** (skip when `gap-analysed` is already in `completed_phases`): explore the affected areas (Glob, Grep, Read) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â enough to identify affected files/modules, existing patterns, and constraints that inform the spec. Write `analysis/quick-analysis.md` (affected files, approach sketch, standards referenced). Extract a 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“2 sentence summary into `phase_summaries.quick_analysis`.
3. **Condensed requirements pass (gap-driven ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no fixed question rounds)**: extract the REQUIRED spec topics from evidence first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **User Journey** (discovery/access, personas, workflow fit), **Existing Code Reuse** (similar features, UI components, backend patterns ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â found during the brief analysis), **Visual Assets** (check `analysis/visuals/` regardless of the answer; skip visual processing for non-UI tasks when none found). On an existing task, reuse the analysis clarifications (`analysis/clarifications.md`, gap-analysis scope decisions) as already-gathered evidence. Only where a genuine gap or ambiguity would change the spec's scope or architecture, ask ONE consolidated `question` round (2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 targeted questions, confirmable-assumption framing "I assume X ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is that correct?", multi-select where positions co-exist); when multiple valid architectural approaches surface, present them in the same round and record the choice in `task_context.architecture_decision`. Never write TBDs or open questions into the condensed spec ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â decide, or ask; anything unresolvable is recorded as an explicit assumption in the spec's scope section. Save the gathered context to `analysis/requirements.md` (condensed: description, evidence-based journey/reuse/visuals findings, any Q&A, requirements, scope boundaries, standards referenced).
4. **Condensed spec ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â written directly, NO delegation**: write `implementation/spec.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â goal, scope (in/out), requirements, applicable standards with key guidelines, verification criteria. Then run the Quick diagram gate below. This REPLACES the `specification-creator` delegation in Execute below (quick mode is the only exception to the delegation anti-pattern). Mark `spec-written` complete (`phase_summaries.specification` summary).

### Quick diagram gate (optional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â part of the condensed spec)

1. Use `question`: "Add diagrams to the condensed spec?" Options:
   - **Add diagrams** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Skill tool - `diagrams-mermaid` on `implementation/spec.md` (content-preserving, same rules as the normal Diagram Refinement).
   - **Skip** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the spec stays prose-only.
2. A declined or failed diagram refinement is NOT a failure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â note it in `phase_summaries.specification` and continue.

The TDD red gate is NOT bypassed by quick mode: when `has_reproducible_defect: true` and `tdd-red-proven` is missing, the routing guard in the Entry Gate fires in both modes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the quick TDD lane for bug-shaped work is `/owflow:dev-bugfix`, not a silent skip. `spec-audited` is SKIPPED in quick mode ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `options.spec_audit_enabled: false`; Exit Gate acceptance substitutes for the audit, and `/owflow:reviews-spec-audit <task-path>` remains available as a standalone later option.

Then continue with the **Exit Gate** below.

## Execute (normal runs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â delegated specification)

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md).

**Scope**: normal runs only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â quick mode writes the condensed spec directly (see Quick Mode) and skips this section.

### Technical & Architecture Clarification (before `spec-written`, inline, conditional)

- Complex task with multiple approaches ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `question` for 3-5 technical questions.
- Multiple valid architectural approaches ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ present 2-3 via `question`; the chosen approach is passed to specification-creator.
- Save to `analysis/technical-clarifications.md` (conditional).
- Skip if: simple task, `risk_level: low`, no multiple approaches detected.

### Requirements Gathering (part of `spec-written`, inline)

1. `question` for specification requirements ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â adaptive count based on description length: brief (<30 words) 6-8; standard (30-100 words) 4-6; detailed (>100 words) 2-3. Frame as confirmable assumptions ("I assume X, is that correct?").
2. REQUIRED questions (always include): **User Journey** (discovery/access, personas, workflow fit), **Existing Code Reuse** (similar features, UI components, backend patterns), **Visual Assets** (mockups/wireframes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `analysis/visuals/`).
3. Check `analysis/visuals/` for assets regardless of the answer; note findings for subagent context (skip visual processing for non-UI tasks when none found).
4. Save to `analysis/requirements.md`: initial description, all Q&A rounds, similar features, visual insights, functional requirements, reusability opportunities, scope boundaries, technical considerations.

### Specification Creation (part of `spec-written`, subagent)

**ANTI-PATTERN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never write spec.md yourself in a normal run. "The task is simple" is NOT a reason to skip delegation. (Quick mode is the ONLY exception ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â its prelude step 4 writes the condensed spec directly and skips this section.)**

Task tool - `specification-creator`. Pass: task_path, task_description, task_characteristics, requirements_path (`analysis/requirements.md`), project_context_paths (INDEX.md + `project_doc_paths` from state), risk_level, relevant `phase_summaries`, research/quick context if present in state. Output: `implementation/spec.md`.

### Diagram Refinement (part of `spec-written`, Skill, content-preserving)

Skill tool - `diagrams-mermaid` on `implementation/spec.md` (the skill writes the diagrams into the file and themes them github-dark by default). Add diagrams that clarify scope and communication without replacing prose: `flowchart` (primary functional path), `sequenceDiagram` (key interaction), optional architecture view (`flowchart` with subgraphs, if module structure is in scope). Missing context ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ add an explicit open questions section instead of inventing entities.

### Specification Audit (`spec-audited`, recommended)

1. `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Run specification audit? (Recommended)" with "Yes, run audit (Recommended)" first. User may skip.
2. If yes: Task tool - `spec-auditor`. Pass: task_path, spec_path. Output: `verification/spec-audit.md`. Display verdict (pass/pass-with-concerns/fail), issue counts by severity, top critical findings.

## State Update Convention (per step)

Apply after EVERY phase/step above:

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â update `orchestrator-state.yml` as soon as the step completes, appending ONLY the step slug actually performed plus that step's fields. Never batch multiple steps into one end-of-skill write:
   - After Part A (if it ran): set `task_context.tech_clarified`, `task_context.architecture_decision`.
   - After Parts BÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“D (`spec-written` complete): append `spec-written` to `completed_phases`; set `phase_summaries.specification`; bump `orchestrator.updated`.
   - After Part E (only when the audit ran): append `spec-audited` to `completed_phases`; set `options.spec_audit_enabled: true` and the audit verdict in `phase_summaries.specification`; bump `orchestrator.updated`. When the user skipped the audit, set `options.spec_audit_enabled: false` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no `spec-audited` entry.
   - In quick mode, ALSO append the prelude slugs on their individual completions (never batched): `codebase-analysed` and `gap-analysed` after the quick analysis (quick analysis covers both; note the condensation in `phase_summaries.codebase_analysis` / `phase_summaries.gap_analysis`), then `spec-written` after the condensed spec (summary in `phase_summaries.specification`). The audit skip sets `options.spec_audit_enabled: false` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no `spec-audited` entry.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the spec creation or audit fails and cannot be recovered, do NOT append to `completed_phases`; append the corresponding step slug (`spec-written` or `spec-audited`) to `orchestrator.failed_phases` and increment `auto_fix_attempts["<slug>"]`.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-development.yml`. Fix any reported issue immediately before proceeding.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run to confirm the full state matches everything performed in this session.

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DEV SPEC COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <spec title>

**Approach** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [architecture approach in 1 line]
**Scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [N included / M excluded]
**Audit** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ pass / ÃƒÂ¢Ã…Â¡Ã‚Â  pass-with-concerns / ÃƒÂ¢Ã‚ÂÃ…â€™ fail / skipped]: [0 critical / N major / N minor]
**Entry point** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [quick bootstrap (`--quick`) / full pipeline]

**Artifacts**

- `analysis/requirements.md`
- `implementation/spec.md`
- `verification/spec-audit.md` [conditional]
```

In quick mode the audit line reads `skipped (quick mode)` and `/owflow:reviews-spec-audit <task-path>` is the standalone later option.

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the specification is good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â regenerate the spec with the user's corrections (clarifications, scope boundaries, requirements), update state, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through a specific part of the spec (scope boundaries, architecture approach, audit findings) in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:dev-spec <task-path>`) and end.

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:dev-plan <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` next: breaks the approved spec into grouped, dependency-ordered task groups with test-driven steps. Remaining after: implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.
- `/owflow:dev-plan --quick <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` condensed alternative: writes the implementation plan directly on the fly instead of delegating to the planner subagent.

**Other options**:

- `/owflow:reviews-spec-audit <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â standalone spec re-audit; does not advance phases (verify results, then re-run `/owflow:dev-spec` adjustments if needed)
- `/owflow:goal-development <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `optional` shortcut: runs all remaining phases in one loop (plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ implement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize)

Then STOP.
