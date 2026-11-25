---
name: research-converge
description: "Work phase of the research workflow. Interactive convergence: presents the brainstorming alternatives for each decision area ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one area, one dedicated `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and records the chosen combination in state (state-only; no new artifacts). Con..."
---
# Research Converge ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Per-Area Decisions (approaches-chosen)

Work phase of the research workflow. Interactive convergence: presents the brainstorming alternatives for each decision area ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one area, one dedicated `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and records the chosen combination in state (state-only; no new artifacts). Conditional optional phase ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â runs only when brainstorming ran. There is no auto-continue from brainstorm: this skill's Entry Gate re-checks the artifact. State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads it on entry and writes results on exit.

Related phases: `/owflow:research-brainstorm` (produces `outputs/solution-exploration.md`, which this skill parses), `/owflow:research-design` (consumes the chosen combination as `selected_approach`), `/owflow:research-finalize` (the route when design is off).

## Entry Gate

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/research/` (e.g., `2026-09-26-my-research`); resolve to its path.
- If the argument is **missing**, the path does **not exist**, or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP (never guess or auto-pick a task):
  1. Steps that must be completed first (in order), each with its command:
     - Research brief & plan (`brief-written`, `plan-created`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-plan <task-path>`
     - Parallel findings fan (`findings-gathered`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-gather <task-path>`
     - Synthesis & research report (`synthesis-complete`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-synthesize <task-path>`
     - Solution alternatives (`alternatives-generated`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/owflow:research-brainstorm <task-path>`
  2. List available research-task identifiers (directories under `.owflow/tasks/research/`) to resume from, if any.
  3. Hint: `Run /owflow:research <question> to start a task from scratch, or pass a task path/identifier to resume.`

### Prerequisites

| Required for this skill | Where verified                                                                             | Produced by                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| State file exists       | `<task-path>/orchestrator-state.yml`                                                        | `/owflow:research <question>` or `/owflow:research-quick` |
| Foundation complete     | `synthesis-complete` in `completed_phases` + `analysis/synthesis.md` exists                 | `/owflow:research-synthesize <task-path>`                          |
| Alternatives exist      | `alternatives-generated` in `completed_phases` + `outputs/solution-exploration.md` exists   | `/owflow:research-brainstorm <task-path>`                          |

1. **Read `orchestrator-state.yml`** from the task path. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mid-pipeline bootstrap ([Missing-state Bootstrap](../orchestrator-framework/references/gate-contract.md), starting slug `approaches-chosen`): `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create a fresh standard research task starting at this step, or decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No research task found at <path>. Run /owflow:research <question> to start a task from scratch.` and STOP.
2. **Prerequisite check**: `synthesis-complete` AND `alternatives-generated` must be in `completed_phases`, and `outputs/solution-exploration.md` must exist. If missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block, then STOP:
   - `Run /owflow:research-brainstorm <task-path> first` (or the command for the earliest missing earlier step: `/owflow:research-plan`, `/owflow:research-gather`, or `/owflow:research-synthesize`).
3. **Skip/resume (per-area partial resume)**: if `approaches-chosen` is in `completed_phases`, validate every `phase_summaries.converge.decision_areas` entry carries `chosen_approach` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all resolve ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ report the existing chosen combination and route to the Exit Gate; any area unresolved ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ re-ask ONLY the unresolved areas below. Also ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â even WITHOUT the slug ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip any area whose `decision_areas` entry already carries `chosen_approach`; only unresolved areas are ever asked.

## Input / Output Artifacts

| Artifact                                       | Normal mode (full lane)                                                | Quick mode (`research-quick`)                                                                          |
| ---------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Consumed: `outputs/solution-exploration.md`    | parsed for decision areas + alternatives                                | identical ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when the optional chain runs after a quick pass, the exploration file was produced by research-brainstorm |
| Produced: none (state-only)                    | decisions recorded inline per area                                      | same mechanics ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â research-quick never converges inline                                                     |
| State write                                    | `approaches-chosen`; `phase_summaries.converge {summary, decision_areas, deferred_ideas}` (per-area partial writes) | same slug and fields                                                          |

## Execute (direct interactive ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-area convergence)

**Read first**: the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-area convergence is direct interactive work (like dev-verify's interactive phases); no agents involved.

> **ANTI-PATTERN**: Do NOT present all decision areas in a single summary table and ask one combined "do you agree?" question. Each area MUST get its own detailed presentation and its own question call.
>
> **ANTI-PATTERN**: Do NOT show full alternatives/pros/cons for the first area and then shortcut remaining areas to just a recommendation line + question. EVERY area gets the SAME level of detail ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all alternatives with descriptions, pros, and cons. No exceptions.

**Per-area handling** (the two guards above apply to EVERY area, including partial resumes):

1. Read `outputs/solution-exploration.md`
2. For each decision area sequentially, output ALL of the following (steps a-d) BEFORE calling question:
   a. **Area header**: area name and why this decision matters (1-2 sentences of context)
   b. **Alternatives detail**: For EVERY alternative in this area, show:
      - Name and description (2-3 sentences)
      - Pros (bullet list)
      - Cons (bullet list)
   c. **Recommendation**: which alternative is recommended and why (1 sentence)
   d. **question**: this area's alternatives as options (mark recommended with "(Recommended)") + "Need more info" option
      e. If user picks ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ record choice (write the per-area partial state immediately ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see State Update Convention), move to next area
      f. If "Need more info" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ present the detailed trade-off analysis for the requested alternative, then re-ask

> **SELF-CHECK before each question**: Did you output the alternatives with pros/cons for THIS area? If you only showed a recommendation line without listing all alternatives and their pros/cons, STOP and output the full detail before asking.

3. After all areas resolved, present a brief summary of the chosen combination (this summary moves into the Exit-Gate results box below ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the boundary to design/finalize stays explicit, no AUTO-CONTINUE)
4. **GATE CHECK**: Verify that question was called for EACH decision area. If any decision area was skipped for any reason (e.g., output file missing, read failure), STOP and resolve before continuing. Do NOT mark the convergence complete without user convergence on all decision areas.

### Close (`approaches-chosen`)

1. **State write**: append `approaches-chosen` to `completed_phases` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ONLY after the LAST unresolved area resolves; update `phase_summaries.converge {summary, decision_areas, deferred_ideas}` (deferred ideas recorded when the exploration documents them); bump `orchestrator.updated`. On failure: append `approaches-chosen` to `failed_phases`, increment `auto_fix_attempts["approaches-chosen"]`. Then re-read state + run `verify_template` (see State Update Convention).

## State Update Convention (per step)

Apply after EVERY step above:

1. **Write immediately ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per area**: as each decision area resolves, record the `chosen_approach` into that area's entry in `phase_summaries.converge.decision_areas` immediately (never batch all areas into one end-of-skill write ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the per-area write is what makes partial resume work). The `approaches-chosen` slug is appended ONLY after the LAST unresolved area resolves.
2. **Timestamp** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set `orchestrator.updated` to the current UTC timestamp on every write.
3. **Failures** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if a question cannot fire (read failure, tool failure) or an area could not resolve, do NOT append `approaches-chosen` to `completed_phases`; instead append it to `orchestrator.failed_phases` and increment `auto_fix_attempts["approaches-chosen"]`. A deliberate "stop here" at an area question is NOT a failure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the area simply stays unresolved and partial resume picks it up on the next run.
4. **Validate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after every write, re-read the file to confirm values, then run the `verify_template` tool with `filePath: <task-path>/orchestrator-state.yml`, `templateName: orchestrator-state-research.yml`. Fix any reported issue immediately before proceeding.
5. **Final check** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â before the Exit Gate, one consolidated re-read + `verify_template` run to confirm the full state matches everything performed in this session.

## Recovery

| Step                            | Max Attempts | Strategy                                    |
| ------------------------------- | ------------ | -------------------------------------------- |
| Converge (`approaches-chosen`)  | 1            | Re-read exploration file, re-present areas   |

## Exit Gate

Present results, get user confirmation, then hand off (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)). Never auto-invoke the next skill. The chosen-combination summary (step 3 above) is folded into the results box.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ RESEARCH CONVERGE COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <research question>

**Decision areas** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [N areas resolved]
**Chosen combination** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [area: choice, one line per area]
**Deferred ideas** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [one line each / none]
**Design decision** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [feeds into design as `selected_approach` / no design planned]

**Artifacts**

- none (state-only) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â decisions live in `phase_summaries.converge.decision_areas` of `orchestrator-state.yml`; `outputs/solution-exploration.md` stays the shared record
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the per-area decisions are good; continue.
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-open a specific area: re-present that ONE area with full detail and re-ask its question (other areas untouched), update state, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â walk through a specific area's trade-offs in more depth; then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:research-converge <task-path>`) and end. Note: unresolved areas re-ask on the next run (per-area partial resume).

### Next steps (after Accept)

- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-design <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when the user wants high-level design: Part A asks design preferences, Part B delegates the solution-designer with the chosen combination as `selected_approach`, Part D refines diagrams. Remaining after: finalize.
- `ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /owflow:research-finalize <task-path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when no design is wanted: inventories the research outputs and completes the task (`research-completed`). Remaining after: none.

Then STOP.
