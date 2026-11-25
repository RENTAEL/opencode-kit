---
name: research-synthesize
description: "Work phase of the research workflow. Delegates pattern synthesis and evidence-based reporting to the research-synthesizer agent (`analysis/synthesis.md` + `outputs/research-report.md`). This is the research-foundation boundary: the Exit Gate is the pause between the foundation..."
---
# Research Synthesize ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Synthesis & Research Report (synthesis-complete)

Work phase of the research workflow. Delegates pattern synthesis and evidence-based reporting to the research-synthesizer agent (`analysis/synthesis.md` + `outputs/research-report.md`). This is the research-foundation boundary: the Exit Gate is the pause between the foundation and the optional-phase decision. State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads it on entry and writes results on exit.

Related phases: `/owflow:research-gather` (produces the merged findings); the optional chain (`research-brainstorm` / `research-design`) and `/owflow:research-finalize` follow, per the user's choice.

## Entry Gate

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/research/` (e.g., `2026-09-26-my-research`); resolve to its path.
- If the argument is **missing**, the path does **not exist**, or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):
  1. Steps that must be completed first (in order), each with its command:
     - Research brief & plan (`brief-written`, `plan-created`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-plan <task-path>`
     - Parallel findings fan (`findings-gathered`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-gather <task-path>`
  2. List available research-task identifiers (directories under `.owflow/tasks/research/`) to resume from, if any.
  3. Hint: `Run /owflow:research <question> to start a task from scratch, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill              | Where verified                                                                 | Produced by                          |
| ------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------ |
| State file exists                    | `<task-path>/orchestrator-state.yml`                                           | `/owflow:research <question>` or `/owflow:research-quick` |
| Findings exist                       | `findings-gathered` in `completed_phases` + `analysis/findings/` has per-category files | `/owflow:research-gather <task-path>` (or the quick lane's condensed gather) |
| Research question recorded           | `research_context.research_question` non-null in state                          | `/owflow:research-plan <task-path>`   |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `synthesis-complete`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard research task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No research task found at <path>. Run /owflow:research <question> to start a task from scratch.` and STOP.
2. **Content check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â findings present**: the per-category files under `analysis/findings/` must exist (artifacts before state ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â drop the `findings-gathered` entry and route back to `/owflow:research-gather <task-path>` when they do not).
3. **Skip/resume**: if `analysis/synthesis.md` AND `outputs/research-report.md` both exist, adopt them ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â append `synthesis-complete` if it is missing, backfill `research_outputs.synthesis` and `research_outputs.research_report` when those fields are still null, report the existing summaries, and route to the Exit Gate. Either file missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ re-run below (drop a stale `synthesis-complete` entry first).

## Input / Output Artifacts

| Artifact                                       | Normal mode (full lane)                                                                        | Quick mode (`research-quick`)                                             |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Consumed: `analysis/findings/*.md`             | all per-category files (the gather contract)                                                     | same ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â quick-lane findings feed the inline synthesis                                        |
| Consumed: `research-synthesizer` agent (Task tool) | 1 delegated call                                                                             | n/a ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â synthesis is ALWAYS inline in the quick lane (the ONLY exception to this delegation)  |
| Produced: `analysis/synthesis.md`              | delegated (patterns, cross-references, gaps)                                                     | written directly inline                                                                     |
| Produced: `outputs/research-report.md`         | delegated (report + per-finding confidence)                                                      | written directly inline                                                                     |
| State write                                    | `synthesis-complete`; `confidence_level`, `phase_summaries.synthesize`, `research_outputs.synthesis` + `.research_report` | same slug and fields, condensation-noted                     |

## Execute (delegated synthesis)

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md).

> **ANTI-PATTERN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never write synthesis.md or research-report.md yourself. "The findings are few" is NOT a reason to skip delegation. (The quick lane is the ONLY exception ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â research-quick synthesizes inline and skips this section.)**

1. **INVOKE NOW**: Task tool - `research-synthesizer` subagent (never the Skill tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is an agent). Pass (Pattern 7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â accumulated context): task_path, findings_directory_path, research_question, research_type, methodology (from state).

**Synthesizer produces**:

- Pattern analysis and cross-references ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `analysis/synthesis.md`
- Comprehensive research report answering research question ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `outputs/research-report.md`
- Confidence levels for each finding
- Documented gaps and uncertainties

> **SELF-CHECK on both artifacts**: after the Task tool returns, verify `analysis/synthesis.md` AND `outputs/research-report.md` exist (synthesis documents gaps; report carries confidence per finding). If missing: **STOP. Re-invoke the research-synthesizer with corrected context.** If the second attempt also fails, use `question` to report the failure and ask whether to retry (after targeted re-gathering if the gaps require it) or stop. There is no continue-without-synthesis path ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every later step reads these artifacts. On stop, record the failure per the State Update Convention and print the resume command.

### Post-synthesis decision re-cap (direct, condensable)

The synthesizer's key outcomes are surfaced to the user here before the Exit Gate (decisions from subagents must go to the user ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never silently skipped): overall `confidence_level`, top patterns, documented gaps. Extract a 1-2 sentence summary into `phase_summaries.synthesize`.

### Close (`synthesis-complete`)

1. **State write**: append `synthesis-complete` to `completed_phases`; update `research_context.confidence_level`, `phase_summaries.synthesize`; set `research_outputs.synthesis` and `research_outputs.research_report`; bump `orchestrator.updated`. On failure: append `synthesis-complete` to `failed_phases`, increment `auto_fix_attempts["synthesis-complete"]`. Then re-read state + run `verify_template` (see State Update Convention).

## State Update Convention (per step)

Apply after EVERY step above:

1. **Write immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â update `orchestrator-state.yml` as soon as the step completes, appending ONLY the step slug actually performed (`synthesis-complete`) plus that step's fields. Never batch multiple steps into one end-of-skill write.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the step fails or its retries are abandoned, do NOT append to `completed_phases`; instead append the step's slug to `orchestrator.failed_phases` and increment `auto_fix_attempts["synthesis-complete"]`.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-research.yml`. Fix any reported issue immediately before proceeding.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run to confirm the full state matches everything performed in this session.

## Recovery

| Step                              | Max Attempts | Strategy                              |
| --------------------------------- | ------------ | ------------------------------------- |
| Synthesize (`synthesis-complete`) | 2            | Request targeted re-gathering for gaps |

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ RESEARCH SYNTHESIZE COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <research question>

**Type** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [research type]
**Confidence** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [confidence level from state]
**Key patterns** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [2-3 one-line pattern highlights from synthesis]
**Gaps** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [documented gaps and uncertainties, 1 line]

**Artifacts**

- `analysis/synthesis.md`
- `outputs/research-report.md`
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â synthesis and report are good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-run the affected part with the user's corrections (targeted re-gathering for gaps, then re-synthesize), update state and artifacts, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through specific findings or confidence levels in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:research-synthesize <task-path>`) and end.

### Next steps (after Accept)

Research foundation complete (initialized, planned, gathered, synthesized). Continue to optional-phase evaluation?

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-brainstorm <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when the user wants solution alternatives brainstormed. Remaining after: converge ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ design (when wanted) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.
- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-design <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â design-only branch (no brainstorming), seeded from the research report. Remaining after: finalize.
- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-finalize <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when neither is wanted: inventories the outputs and completes the task. If the foundation alone was the goal, this is the route ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task stays resumable.

Then STOP.
