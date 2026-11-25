---
name: research-design
description: "Work phase of the research workflow. Creates the high-level architecture design from the selected solution approach ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or, when brainstorming did not run, seeded from the research-report recommendations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â as two artifacts (`outputs/high-level-d..."
---
# Research Design ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â High-Level Design (design-generated)

Work phase of the research workflow. Creates the high-level architecture design from the selected solution approach ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or, when brainstorming did not run, seeded from the research-report recommendations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â as two artifacts (`outputs/high-level-design.md`, `outputs/decision-log.md`), then refines diagrams via the `diagrams-mermaid` Skill. Optional phase ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â runs when the user chooses it: invoking this skill IS the decision to design (no enablement flag in state). The design-only branch (brainstorming not run) is owned here: `selected_approach` is seeded from the research report. State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads it on entry and writes results on exit.

Related phases: `/owflow:research-brainstorm` + `/owflow:research-converge` (produce the chosen combination consumed as `selected_approach`), `/owflow:research-finalize` (always next). The design-techniques reference lives in this skill's own folder (`references/design-techniques.md`).

## Entry Gate

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/research/` (e.g., `2026-09-26-my-research`); resolve to its path.
- If the argument is **missing**, the path does **not exist**, or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):
  1. Steps that must be completed first (in order), each with its command:
     - Research brief & plan (`brief-written`, `plan-created`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-plan <task-path>`
     - Parallel findings fan (`findings-gathered`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-gather <task-path>`
     - Synthesis & research report (`synthesis-complete`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-synthesize <task-path>`
     - Chosen approaches (`approaches-chosen`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-brainstorm <task-path>` + `/owflow:research-converge <task-path>` (only when brainstorming ran)
  2. List available research-task identifiers (directories under `.owflow/tasks/research/`) to resume from, if any.
  3. Hint: `Run /owflow:research <question> to start a task from scratch, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill | Where verified                                                                                                                             | Produced by                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| State file exists       | `<task-path>/orchestrator-state.yml`                                                                                                        | `/owflow:research <question>` or `/owflow:research-quick` |
| Design input ready      | brainstorm ran ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `approaches-chosen` in `completed_phases`; OR brainstorm did not run ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `outputs/research-report.md` exists with recommendations | `/owflow:research-converge <task-path>` (or `/owflow:research-synthesize <task-path>`) |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `design-generated`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard research task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No research task found at <path>. Run /owflow:research <question> to start a task from scratch.` and STOP.
2. **Prerequisite check**: `synthesis-complete` must be in `completed_phases`. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block (`ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-synthesize <task-path>`, or the earliest missing earlier step), then STOP.
3. **Design input (branch resolution)**:
   - `approaches-chosen` in `completed_phases` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ brainstorm ran; the chosen combination from `phase_summaries.converge.decision_areas` is `selected_approach`.
   - `approaches-chosen` in `completed_phases` but `phase_summaries.converge.decision_areas` has no `chosen_approach` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ convergence never resolved its areas: `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-converge <task-path>`, then STOP.
   - `alternatives-generated` in `completed_phases` but `approaches-chosen` absent ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the brainstorm chain is incomplete: `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-converge <task-path>`, then STOP. Do NOT seed from the research report while alternatives exist.
   - Neither slug present ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ brainstorming has not produced alternatives. Ask via `question`: "Brainstorming hasn't run ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â seed the design from the research report, or brainstorm first?" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ seed from report (design-only branch): state `Brainstorming did not run ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â seeding the design from research-report recommendations.`, validate `outputs/research-report.md` exists (missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-synthesize <task-path>`, then STOP) and proceed; ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ brainstorm first: `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-brainstorm <task-path>`, then STOP.
4. **Skip/resume**: if `design-generated` is in `completed_phases`, validate BOTH `outputs/high-level-design.md` AND `outputs/decision-log.md` exist; either missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ re-run Parts B-D below; both present ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ report the existing design summary and route to the Exit Gate.

## Input / Output Artifacts

| Artifact                                       | Normal mode (full lane)                                                   | Quick mode (`research-quick`)                                                                        |
| ---------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Consumed: `phase_summaries.converge.decision_areas` (chosen combination) | becomes `selected_approach` when brainstorm ran                       | same fields ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when the optional chain runs after a quick pass, converge ran as the normal subskill        |
| Consumed: `outputs/research-report.md`         | design-only branch seed (`selected_approach` from recommendations)           | identical ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â research-quick produces the same report artifact                                              |
| Produced: `outputs/high-level-design.md`, `outputs/decision-log.md` | delegated to `solution-designer`, refined via `diagrams-mermaid` Skill | NOT produced in the quick pass ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â design always runs as this skill after the quick lane                    |
| State write                                    | `design-generated`; `phase_summaries.design {summary, architecture_style, decisions_count}`, `research_outputs.high_level_design` + `.decision_log` | same (this skill never runs inside a quick pass)               |

## Execute (Part A direct + Part B delegated + Part C direct + Part D Skill)

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md).

**Read `references/design-techniques.md` NOW using the Read tool** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â MADR format, ADR guidance, decision documentation patterns (own-folder reference).

### Part A ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Design Direction (direct)

1. Brainstorm ran: read the chosen combination from `phase_summaries.converge.decision_areas` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it becomes `selected_approach`.
2. Brainstorm did not run (design-only branch, resolved in Entry Gate step 3): read `outputs/research-report.md` recommendations and derive `selected_approach` from them; note the provenance (research-report recommendations, not convergence).
3. `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Any architectural constraints or preferences?" (free-form answer; empty means none). These `design_preferences` ride in the Part B context pass and are kept human-readable in `phase_summaries.design.summary` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the state template has NO dedicated `design_preferences` slot; that omission is deliberate (do NOT invent a template field).

### Part B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Design Generation (subagent)

> **ANTI-PATTERN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do NOT generate C4 architecture diagrams or ADRs inline. "The approach is obvious" is NOT a reason to skip delegation. The solution-designer agent has specialized architecture and MADR documentation capabilities.**

1. **INVOKE NOW**: Task tool - `solution-designer` subagent (never the Skill tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is an agent). Pass (Pattern 7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â accumulated context):
   - `task_path`, `synthesis_path` (`analysis/synthesis.md`), `research_report_path` (`outputs/research-report.md`)
   - `solution_exploration_path` (`outputs/solution-exploration.md`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when brainstorm ran
   - `selected_approach` (from convergence; on the no-brainstorm branch, seeded from research-report recommendations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â list the provenance in the prompt)
   - `design_preferences` (from Part A; omit when the user gave none)
   - Accumulated context: `research_type`, `research_question`, `confidence_level`, `phase_summaries`
   - `project_doc_paths` (from state)
   - MUST-contract: the designer writes BOTH `outputs/high-level-design.md` AND `outputs/decision-log.md`
2. > **SELF-CHECK**: After the Task tool returns, verify BOTH `outputs/high-level-design.md` and `outputs/decision-log.md` exist. If either is missing: **STOP. Do NOT proceed to Part D or the Exit Gate.** Re-invoke the designer with corrected context. If a second attempt also fails, use `question` to report the failure and ask whether to retry or skip design.

### Part C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Executive Summary (direct)

Read `outputs/high-level-design.md` and `outputs/decision-log.md`, then present the executive summary through the Exit-Gate results box below (architecture style and key components, decision count, key decision highlights 1 line each, integration points with the existing system if applicable) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no separate presentation round.

### Part D ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Diagram Refinement (Skill, content-preserving)

1. **INVOKE NOW**: Skill tool - `diagrams-mermaid` to refine visual communication in `outputs/high-level-design.md` (the skill writes the diagrams into the file and themes them github-dark by default).
2. Add diagrams that supplement (NOT replace) existing architecture content:
   - one architecture view (`flowchart` with subgraphs; nested subgraphs only if needed),
   - one interaction/state view (`sequenceDiagram` or `flowchart`) for the critical flow.
3. If minimum context for a diagram is missing, record explicit gaps in the document and avoid speculative components/relationships.

### Close (`design-generated`)

1. **State write**: append `design-generated` to `completed_phases` after the SELF-CHECK passes and Part D completes; update `research_context.phase_summaries.design {summary, architecture_style, decisions_count}` (keep the Part A preferences visible in `summary`); set `research_outputs.high_level_design` AND `research_outputs.decision_log`; bump `orchestrator.updated`. On failure: append `design-generated` to `failed_phases`, increment `auto_fix_attempts["design-generated"]`. Then re-read state + run `verify_template` (see State Update Convention).

## State Update Convention (per step)

Apply after EVERY step above:

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â update `orchestrator-state.yml` as soon as the step completes, appending ONLY the step slug actually performed (`design-generated`) plus that step's fields. Never batch multiple steps into one end-of-skill write.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the designer delegation fails or its retries are abandoned, do NOT append `design-generated` to `completed_phases`; instead append it to `orchestrator.failed_phases` and increment `auto_fix_attempts["design-generated"]`. A user-chosen skip via `question` after repeated failures is a deliberate decision, not a failure: record the reason in `phase_summaries.design.summary` and append neither `design-generated` nor a `failed_phases` entry. Then present the Exit Gate (results box notes the skip; next step is `/owflow:research-finalize <task-path>`).
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-research.yml`. Fix any reported issue immediately before proceeding.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run to confirm the full state matches everything performed in this session.

## Recovery

| Step                          | Max Attempts | Strategy                                       |
| ----------------------------- | ------------ | ----------------------------------------------- |
| Design (`design-generated`)   | 2            | Re-invoke solution-designer with adjusted context |

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill. A user-chosen skip still uses this Exit Gate; its results box says the step was skipped and why, and the next step is `/owflow:research-finalize <task-path>`.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ RESEARCH DESIGN COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <research question>

**Architecture style** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [style and key components]
**Decisions recorded** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [N architectural decisions in decision-log.md]
**Key highlights** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [1 line per key decision]
**Integration points** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [with the existing system, if applicable]
**Diagrams** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [refined by diagrams-mermaid / gaps recorded]

**Artifacts**

- `outputs/high-level-design.md`
- `outputs/decision-log.md`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the architecture and decision log are good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-invoke the designer with the user's corrections (changed constraints or preferences), update state and artifacts, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through the architecture style or specific architectural decisions in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:research-design <task-path>`) and end.

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-finalize <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `required` next: inventories all research outputs (including these design artifacts) and completes the task (`research-completed`). Remaining after: none ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â development starts from finalize's handoff (`ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:development <task-path>`).

Then STOP.
