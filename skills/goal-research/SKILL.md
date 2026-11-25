---
name: goal-research
description: "Autonomous mode for research tasks. Initializes (or resumes) the task, then invokes every required `research-*` subskill back-to-back via the Skill tool, pausing at gates between subskills. Shares `orchestrator-state.yml` with assisted mode (`/owflow:research`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚..."
---
# Orchestrated Research Wrapper

Autonomous mode for research tasks. Initializes (or resumes) the task, then invokes every required `research-*` subskill back-to-back via the Skill tool, pausing at gates between subskills. Shares `orchestrator-state.yml` with assisted mode (`/owflow:research`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tasks can mix both modes freely.

Gates follow the shared contract in [Gate Contract](../orchestrator-framework/references/gate-contract.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â orchestrated mode exception: each subskill's own Exit Gate acceptance question IS the loop gate (Accept = continue to the next subskill).

## Input / Output Artifacts

| Artifact                            | Normal mode (this wrapper)                                                  | Quick mode (`research-quick`)                                                                |
| ----------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Consumed: argument (question / path)| research question (new task) or task path/identifier (resume)                 | n/a ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this wrapper never starts a quick run; a completed quick pass just skips rows 2-3            |
| Consumed/produced: all task artifacts| owned entirely by the invoked subskills (none here ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â delegate, never inline) | same ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the subskills run at full fidelity after a quick pass                                       |
| State write                         | `orchestrator.task_ids` (task items) + `orchestrator.updated` only            | none additional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â state was already written by the quick pass                                      |

## Entry Gate

Identical to the research dispatcher ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â complete ALL of its entry-gate steps first (see `../research/SKILL.md` Entry Gate):

1. Read the framework reference files NOW, exactly as the research dispatcher's Step 1: the [Dispatcher & Handoff Pattern](../orchestrator-framework/references/dispatcher-handoff.md), the [Delegation Rules](../orchestrator-framework/references/delegation-rules.md), and the [Orchestrator Patterns](../orchestrator-framework/references/orchestrator-patterns.md).
2. Resolve the argument the same way the research dispatcher does: task path or identifier (a directory, or a directory name under `.owflow/tasks/research/`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **resume mode** (read `orchestrator-state.yml`, validate expected artifacts for `completed_phases`; find the first step slug NOT in `completed_phases`, with `--from=<slug>` overriding); a research question (free text) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new task; nothing provided ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask via `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "What is your research question?" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â then WAIT. Missing state file ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print `No research task found at <path>. Run /owflow:research <question> to start from scratch.` and STOP.
3. Initialize (new task) exactly as the dispatcher: create `.owflow/tasks/research/YYYY-MM-DD-task-name/` + `orchestrator-state.yml` from the research template ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `task.title` / `task.description` from the question, `task.status: in_progress`, `orchestrator.task_path`, `orchestrator.entry_point: "research"`. **CRITICAL**: use the `verify_template` tool immediately after creation to check YAML validity against `orchestrator-state-research.yml`. No project-docs discovery at this layer ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the `research-plan` brief step owns it.
4. Command flags: `--type=TYPE` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `research_context.research_type`. Subskills read it from there. This wrapper never forwards quick runs. The optional brainstorm/design chain has no flags ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the chain decision is asked at the gate after synthesis (row 4 below) or made by manually invoking the optional subskills.
5. Create ONE task item via `TaskCreate` per subskill in the upcoming loop (subject: `"<step name>: <subskill>"`, e.g. `"Brief + plan: research-plan"`), then set the execution order with `TaskUpdate addBlockedBy` (plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ gather ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ synthesize ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ optional chain (gate question) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize). On resume, refresh the already-evidenced items instead of re-creating them. Update statuses as the loop progresses.

**Output**:

```
ÃƒÂ°Ã…Â¸Ã…Â¡Ã¢â€šÂ¬ Orchestrated Research

Task: [research question]
Directory: [task-path]
Loop: research-plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ research-gather ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ research-synthesize ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [research-brainstorm] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [research-converge] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [research-design] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ research-finalize (chain asked at the gate)
```

---

## The Loop

For each subskill in sequence, execute ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skipping any row whose condition is not met (a row whose slug is already in `completed_phases` counts as done):

1. **Announce**: 1-line step banner.
2. **Invoke**: Skill tool with `name: "<subskill>"` and `prompt: "<task-path> [flags relevant to that subskill]"`. The subskill owns its Entry Gate, delegation, and state updates.
3. **Verify handback**: after the skill returns, re-read `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm the expected step slugs were appended to `completed_phases` (per the Sequence and Conditionals table). A user-chosen skip of `research-brainstorm` or `research-design` appends no slug ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the gate answer itself settles the decision, and the loop continues to the next selected row (or to finalize). Do not treat a skipped optional subskill as an early stop. If a subskill stopped early (entry check failed), STOP the loop and relay its routing message to the user.
4. **Gate (subskill's Exit Gate is the loop gate)**: each subskill presents its results box and fires its own results-acceptance `question` before its handoff hint (Orchestrated-mode exception, [Gate Contract](../orchestrator-framework/references/gate-contract.md)). [Rule 5 of the Dispatcher & Handoff Pattern](../orchestrator-framework/references/dispatcher-handoff.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "subskills only SUGGEST the next command" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is superseded for Accept: when the user answers **Accept** to the subskill's Exit Gate question pointing at the next subskill in this loop, treat that as "continue to the next subskill" and invoke it. Any other answer (Adjust / Discuss / Stop / other options picked) ends the loop the same way a rejected gate would.
   - **Exception**: the per-area convergence `question`s `research-converge` fires (one area, one question) are part of that subskill's own decision flow ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they are NOT the loop gate and are NEVER auto-accepted or answered by this wrapper. There is exactly ONE gate definition per subskill hop; the wrapper adds NO second consecutive `question`.
   - **Condensed lane**: this wrapper never starts a quick run. A task already started with `/owflow:research-quick` enters the loop with `brief-written` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `synthesis-complete` already recorded, so those rows are skipped like any other completed slug. An interrupted quick pass (those slugs missing) is not finished condensed here ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the user runs `/owflow:research-quick <task-path>` for that.

### Sequence and Conditionals

| Order | Subskill           | Run when (from state)                                                                                             |
| ----- | ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| 1     | research-plan      | Always (new task or partial foundation)                                                                                 |
| 2     | research-gather    | `plan-created` completed (parses `## Gathering Strategy`, or falls back to 4 default categories; existing findings count as done) |
| 3     | research-synthesize| `findings-gathered` completed                                                                                       |
| 4     | chain decision     | `synthesis-complete` completed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the wrapper asks via `question`: brainstorm ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ converge ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ design, design-only, or straight to finalize |
| 5     | research-brainstorm| User chose brainstorming at the gate (invoking/sequencing the skill IS the decision)                                 |
| 6     | research-converge  | `alternatives-generated` completed (brainstorm ran)                                                                 |
| 7     | research-design    | User chose design ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after `approaches-chosen`, or the design-only branch (seeded from the research report)           |
| 8     | research-finalize  | Foundation complete + optional chain settled (every step the user chose to run is recorded)                          |

A completed quick pass already recorded `brief-written` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `synthesis-complete`, so rows 2-3 are skipped as already done and the loop continues at row 4 (the chain decision). This wrapper never starts a quick run.

The optional chain is the user's choice ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â asked at the gate (row 4) or made by manually invoking the optional subskills. There is no enablement flag in state:

- Brainstorm chosen ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `research-brainstorm` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `research-converge` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ design (if chosen) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.
- Design-only chosen ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skip the brainstorm + converge rows ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `research-design` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ finalize.
- Neither chosen ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ all conditional rows are skipped ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `research-finalize`.

`research-completed` already in `completed_phases` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the task is TERMINAL: skip the Loop and present the wrapper Exit Gate.

**Interruptible**: at any gate the user may answer "stop" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the standard handoff block (next command + `/owflow:research <task-path>` resume hint) and end the session. The task resumes later in either mode.

---

## Exit Gate

When research-finalize completes (`task.status: completed`):

1. Mark the final task item completed via `TaskUpdate`.
2. Present the workflow results box:

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ RESEARCH WORKFLOW COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <research question>

**Steps** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [executed step slugs, e.g. brief-written ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plan-created ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ findings-gathered ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ synthesis-complete ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ alternatives-generated ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ approaches-chosen ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ design-generated ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ research-completed]
**Confidence** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [research_context.confidence_level]
**Decisions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [count of ADRs in the decision log, if design ran]
**Artifacts** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [artifact inventory: outputs/research-report.md always; outputs/solution-exploration.md / outputs/high-level-design.md / outputs/decision-log.md conditionally]
```

3. Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options: **Accept** (print follow-up suggestions: clear context, then `/owflow:development <task-path>` to build on this research, `/owflow:standards-update "<lesson>"` if a standard surfaced, then end) / **Adjust** (re-open the relevant `/owflow:research-*` skill with the corrections) / **Discuss** (walk through the research summary) / **Stop here** (print the resume command `/owflow:research <task-path>` and end).

Then end. No further owflow phase commands are required.

---

## Loop Rules

- **Delegate, never inline**: the wrapper only sequences ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all step work happens inside subskills. If you catch yourself researching/authoring outside a subskill, STOP and invoke the subskill instead.
- **State is the truth**: gates and routing read `orchestrator-state.yml`, not memory. Re-read after every subskill returns.
- **Same state schema as assisted mode**: `completed_phases` step slugs (`brief-written` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `research-completed`) are identical; resume works across modes.
- **Wrapper writes almost nothing**: step slugs, summaries, and outputs belong to the subskills ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this wrapper writes ONLY `orchestrator.task_ids` (task items) and `orchestrator.updated` (timestamps).

## Command Integration

Invoked via:

- `/owflow:goal-research [question] [--type=TYPE]` (new)
- `/owflow:goal-research [task-path] [--from=<slug>]` (resume)

Alternative: `/owflow:research` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â same task in assisted mode (one subskill per invocation, fresh context each step).
