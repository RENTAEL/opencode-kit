---
name: research-plan
description: "Work phase of the research workflow. Creates the research brief, delegates methodology selection and gathering-strategy planning to the `research-planner` agent, and writes the research plan. State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads it on ent..."
---
# Research Plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Brief, Methodology & Plan (brief-written, plan-created)

Work phase of the research workflow. Creates the research brief, delegates methodology selection and gathering-strategy planning to the `research-planner` agent, and writes the research plan. State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads it on entry and writes results on exit.

## Entry Gate

Resolve the argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). The argument may be:

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/research/` (e.g., `2026-09-26-my-research`); resolve to its path.
- **Research question** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â anything else (free text, e.g. `"evaluate caching strategies for our API"`) is treated as a new research question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the routing table asks first.

Route by argument kind:

| Situation                                                     | Route                                                                        |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Task path/identifier, state + question present                | Full lane below (brief step ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plan step)                                     |
| Research question                                             | Ask via `question`: full pipeline through the dispatcher / quick fused task via `/owflow:research-quick "<question>"` / cancel |
| Missing argument                                              | Prompt for input (path, identifier, or research question), then re-route     |

If the path does **not exist** or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):

1. Steps that must be completed first (in order), each with its command:
   - State initialization (`task.*`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research <question>`
2. List available research-task identifiers (directories under `.owflow/tasks/research/`) to resume from, if any.
3. Hint: `Run /owflow:research <question> to start a task from scratch, /owflow:research-quick "<question>" for a quick fused task, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill               | Where verified                                        | Produced by                                        |
| ------------------------------------- | ---------------------------------------------------- | ------------------------------------------------- |
| State file exists                     | `<task-path>/orchestrator-state.yml`                 | `/owflow:research <question>` (dispatcher init)    |
| Research question resolved (resume)   | `research_context.research_question` non-null in state | brief step (`brief-written`)                     |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ a question argument follows the routing table (ask first). Otherwise mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `brief-written`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard research task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No research task found at <path>. Run /owflow:research <question> to start a task from scratch, or /owflow:research-quick "<question>" for a quick fused task.` and STOP.
2. **Content check (resume)**: `research_context.research_question` must be non-null. If null (state exists, question never recorded), prompt via `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "What is your research question?" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and let the brief step record it in state.

## Input / Output Artifacts

| Artifact                                                              | Normal mode (full lane)                                                           | Quick mode (`research-quick`)                                                                |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Consumed: state (`research_context.research_question`, `.research_type`, `.project_doc_paths`) | input                                                                           | same ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â quick bootstrap already records them (condensed brief)                                  |
| Consumed: `references/research-methodologies.md`                      | read before delegation                                                              | read by research-quick directly (no delegation)                                                |
| Produced: `planning/research-brief.md`                                | inline (brief step)                                                                 | inline ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â condensed brief, identical path                                                       |
| Produced: `planning/research-plan.md`, `planning/sources.md`           | delegated to `research-planner` (plan step)                                         | written directly inline (the ONLY exception to the planner-delegation anti-pattern)            |
| State write                                                           | `brief-written`, `plan-created` slugs; `methodology`, `sources`, `phase_summaries.plan` | same slugs and fields, condensation-noted                                                     |

3. **Skip/resume** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â artifacts before state. If the file exists but its slug is missing, adopt it (append the slug, backfill still-null fields) instead of re-running:
   - `planning/research-brief.md` exists ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ append `brief-written` if missing, then skip the brief step.
   - `planning/research-plan.md` AND `planning/sources.md` exist ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ append `plan-created` if missing, backfill `methodology` / `sources` / `phase_summaries.plan` when still null, report the existing plan summary, and route to the Exit Gate.
   - A slug whose artifact is missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ drop the slug and re-run that step.

## Execute (full lane ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â inline brief, delegated planning)

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md) and the [Dispatcher & Handoff Pattern](../orchestrator-framework/references/dispatcher-handoff.md).

### Brief (`brief-written`, inline)

**Artifacts**: `planning/research-brief.md`
**Resume check**: if `planning/research-brief.md` exists, adopt it (append `brief-written` if that slug is missing) and skip to the plan step.

1. Parse research question (from command or prompt user)
2. Classify research type. If `research_context.research_type` is already one of `technical`, `requirements`, `literature`, `mixed` (the dispatcher or `goal-research` wrote it from `--type`), keep that value. The template placeholder `"technical | requirements | literature | mixed"` is not a classification ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â auto-detect from keywords in that case. This skill's own command does not take `--type`.
3. Determine scope (included, excluded, constraints)
4. Define success criteria
5. Create research brief
6. Update state: set `research_context.research_type`, `research_question`, `scope`
7. **Discover project documentation**: Read `.owflow/docs/INDEX.md` (if exists), extract ALL file paths from the "Project Documentation" section ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â includes predefined docs AND any user-added project docs. Store as `research_context.project_doc_paths` in state.

**State write**: append `brief-written` to `completed_phases` (the brief step's fields above go in with it); bump `orchestrator.updated`. On failure: append `brief-written` to `failed_phases`, increment `auto_fix_attempts["brief-written"]`. Then re-read state + run `verify_template` (see State Update Convention).

### Plan (`plan-created`, delegated)

**Artifacts**: `planning/research-plan.md`, `planning/sources.md`
**Resume check**: if `planning/research-plan.md` AND `planning/sources.md` exist, adopt them (append `plan-created` if that slug is missing; backfill `methodology`, `sources`, and `phase_summaries.plan` when still null) and skip to the Exit Gate.

> **ANTI-PATTERN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never write the research plan yourself. "The question is simple" is NOT a reason to skip delegation.**

1. **Read `references/research-methodologies.md` NOW using the Read tool** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â research type classification, methodology selection, gathering strategies (the reference lives in this skill's own folder).
2. **INVOKE NOW**: Task tool - `research-planner` subagent (never the Skill tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is an agent). Pass (Pattern 7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â accumulated context): task_path, research_brief_path, research_type, research_question, scope, project_doc_paths (from state). Output: `planning/research-plan.md`, `planning/sources.md`.
3. **Plan parsability**: the plan SHOULD keep a `## Gathering Strategy` section (categories + count). `research-gather` parses that section; if the planner omitted it, do NOT hand-author the section in a full-lane run ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â note the omission in `phase_summaries.plan` and let gather fall back to its default 4 categories.
4. **State write**: append `plan-created` to `completed_phases`; update `research_context.methodology`, `sources`, `phase_summaries.plan`; bump `orchestrator.updated`. On failure: append `plan-created` to `failed_phases`, increment `auto_fix_attempts["plan-created"]`. Then re-read state + run `verify_template`.

## State Update Convention (per step)

Apply after EVERY step above:

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â update `orchestrator-state.yml` as soon as the step completes, appending ONLY the step slug actually performed (e.g. `brief-written`, `plan-created`) plus that step's fields. Never batch multiple steps into one end-of-skill write.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the step fails or its retries are abandoned, do NOT append to `completed_phases`; instead append the step's slug to `orchestrator.failed_phases` and increment `auto_fix_attempts["<slug>"]`.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-research.yml`. Fix any reported issue immediately before proceeding.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run to confirm the full state matches everything performed in this session.

## Recovery

| Step                        | Max Attempts | Strategy                                              |
| --------------------------- | ------------ | ----------------------------------------------------- |
| Brief (`brief-written`)     | 1            | Prompt user for clarification if question unclear     |
| Plan (`plan-created`)       | 2            | Expand search patterns, use fallback mixed methodology |

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ RESEARCH PLAN COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <research question>

**Type** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [research type]
**Methodology** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [methodology summary from state]
**Gathering categories** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [N categories in the plan's Gathering Strategy]

**Artifacts**

- `planning/research-brief.md`
- `planning/research-plan.md` (keeps the parsable `## Gathering Strategy` section)
- `planning/sources.md`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the brief/plan are good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-run only the affected step (brief or plan) with the user's corrections, update state and artifacts, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through a specific part (research type, methodology, gathering strategy) in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:research-plan <task-path>`) and end.

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-gather <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` next: launches the parallel `information-gatherer` fan and merges per-category findings (`findings-gathered`), then `research-synthesize` fuses synthesis + research report. Remaining after: optional chain (user choice) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.

Then STOP.
