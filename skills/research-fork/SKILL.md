---
name: research-fork
description: "Utility skill for the research workflow. Copies an existing research task directory (`.owflow/tasks/research/<name>`) **wholesale** into a new task so it can **diverge from the previously run one** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. re-run synthesis or the optional chain (brainstorm ÃƒÂ¢..."
---
# Research Fork ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Task Divergence Copy (utility, no phases)

Utility skill for the research workflow. Copies an existing research task directory (`.owflow/tasks/research/<name>`) **wholesale** into a new task so it can **diverge from the previously run one** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. re-run synthesis or the optional chain (brainstorm ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ converge ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ design) with different choices while the original stays intact.

The copy is verbatim ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every artifact, including outputs of steps after the fork point (the source keeps them too; the resumed step overwrites its outputs). The fork's `orchestrator-state.yml` is then trimmed: `completed_phases` cut at the **fork point** (a completed step slug), so the fork **continues from the point onwards**. The fork then continues at full fidelity from the fork point with every research subskill.

**The task path is the only required input.** A bare `/owflow:research-fork <task-path>` is answered by a short guided setup: the skill reads the source research, then asks up to three questions ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â intent, fork point, name ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each pre-filled with suggestions drawn from that research, and confirms the resulting plan before copying. Every question is skipped when its input is already supplied: a quoted description answers the intent question, `--from=<slug>` the fork point, `--name="..."` the name. Nothing is ever guessed silently ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â suggestions are proposals, the user answers.

Copy mechanics live in the deterministic `fork_task` tool (delegation anti-pattern does not apply ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is a file-copy utility, NOT research work; never perform the copy with bash `cp` yourself). State lives in `orchestrator-state.yml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill reads source state on entry; the tool writes the forked state.

This is NOT a pipeline step: it creates a task, stops at its Exit Gate, and never chains into other skills. Fork anytime ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â including on `task.status: completed` tasks (`research-completed` is trimmed from the fork's `completed_phases`).

## Entry Gate

Resolve the `task-path-or-identifier` argument BEFORE anything else (see [Gate Contract](../orchestrator-framework/references/gate-contract.md)):

- **Path** (absolute or project-relative) to the task directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use as-is.
- **Identifier** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact directory name inside `.owflow/tasks/research/` (e.g., `2026-09-26-my-research`); resolve to its path.
- Any remaining free text in the argument is the **intent description** (see Guided setup Q1). It never participates in path resolution.
- If no path/identifier is present ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Which research task should be forked?" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â listing the directory names under `.owflow/tasks/research/` as options (free-form path also accepted), then re-route. If the given argument does **not exist** or matches **no identifier** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print:

```
BLOCKED ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no research task found at <arg>.

Quick way out:
  /owflow:research-fork <task-path-or-identifier> ["<what this fork should explore>"]

Available research tasks:
<list directory names under .owflow/tasks/research/, one per line, if any>
```

then STOP (never guess or auto-pick a task). For a fresh research question instead: `/owflow:research <question>`.

### Prerequisites

| Required for this skill | Where verified                                             | Produced by                                    |
| ----------------------- | ---------------------------------------------------------- | ---------------------------------------------- |
| State file exists       | `<task-path>/orchestrator-state.yml`                       | `/owflow:research <question>` or `/owflow:research-quick` |
| Forkable research       | at least one completed step in `completed_phases`           | any research subskill                          |

1. **Read `orchestrator-state.yml`** from the task path. Missing / unreadable ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print the blocked block (as above, plus quality gate: forkable research needs at least one completed step ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run `/owflow:research-plan <task-path>`, then `/owflow:research-gather <task-path>`, then `/owflow:research-synthesize <task-path>` first) and STOP.

## Orient (read the source ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â suggestions depend on it)

The guided setup is only as good as what the agent actually read. Before asking anything, gather just enough of the source to name its angles, its decisions, and its loose ends:

1. From state: `task.title`, `research_context.research_question`, `scope.included` / `.excluded`, `research_context.phase_summaries.*` (especially `converge.decision_areas[].area|chosen_approach` and `converge.deferred_ideas`), `research_context.confidence_level`.
2. From artifacts, when they exist: the conclusions / open questions / limitations sections of `outputs/research-report.md` and `analysis/synthesis.md`, and the alternatives in `outputs/solution-exploration.md`. Read headings and the decision-relevant parts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is orientation, not a re-run of the research.
3. Build the **fork-point list**: every slug in `completed_phases` (state is the truth ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-read it, don't trust memory), **excluding `research-completed`** (nothing diverges after completion), in pipeline order, each with the human step name from the [dispatcher routing table](../research/SKILL.md#routing-table-completed_phases--next-subskill):

   | Fork point slug            | Step name                    | Re-runs from                          |
   | -------------------------- | ---------------------------- | ------------------------------------- |
   | `brief-written`            | Brief                        | research-plan                         |
   | `plan-created`             | Plan & sources               | research-gather                       |
   | `findings-gathered`        | Findings gathering           | research-synthesize                   |
   | `synthesis-complete`       | Synthesis & research report  | optional chain (brainstorm / design) / finalize |
   | `alternatives-generated`   | Solution alternatives        | research-converge                     |
   | `approaches-chosen`        | Approach convergence         | research-design / finalize            |
   | `design-generated`         | High-level design            | research-finalize                     |

4. `--from=<slug>` given ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validate it against that list ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mismatch ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print:

```
BLOCKED ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <slug> is not a completed fork point of <task-name>.

Valid fork points: <comma-separated slugs from completed_phases, minus research-completed>
Valid fork points are completed step slugs only. Re-run:
  /owflow:research-fork <task-path> --from=<step-slug>
```

then STOP. Never fall through to the question.

## Guided setup (ask what the argument did not answer)

Three questions, in this order. **Ask only the unanswered ones** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each input source short-circuits its question. Every question is a `question` call; WAIT for the answer before the next. Ask no question whose answer is already in the argument, and never invent a user's intent silently.

### Q1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Intent: "What should this fork explore?"

- **Answered by** a quoted description in the argument ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use it verbatim, skip the question.
- **Otherwise ask**, with 3-4 divergence angles derived from what Orient read, marked "(Recommended)" on the one you judge most useful, each description naming the evidence it comes from:
  - re-synthesize with a different lens (e.g. another technology, a cost/constraint focus, a different scope) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â from the report's open questions or low `confidence_level`
  - explore a deferred idea ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â from `converge.deferred_ideas`
  - revisit a chosen approach with an alternative ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â from `converge.decision_areas[].area|chosen_approach` and the alternatives in `solution-exploration.md`
  - narrow or widen the scope ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â from `scope.included` / `.excluded`
- Free-form answers are welcome and common ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not push the user toward your options.

### Q2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Fork point: "Where should the fork diverge?"

- **Answered by** `--from` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validated in Orient, skip the question.
- **Otherwise ask**, one option per fork point in pipeline order, each description = what the fork keeps and re-runs: `"keeps up to <slug> (<step name>); re-runs <next-step command>"`, plus `"(drops N later steps)"` when N > 0. Recommend the latest completed step whose re-run matches the intent ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `synthesis-complete` when the intent re-thinks the findings, `approaches-chosen` when it re-opens a chosen approach, `design-generated` when it only reshapes the design, `plan-created` / `findings-gathered` when it changes the sources or scope, `brief-written` for a full restart with a different question. Mark that option "(Recommended)"; every other option stays selectable.

### Q3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Name: "Short descriptive name for the fork?"

- **Answered by** `--name="..."` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ that string is the name source, skip the question.
- **Otherwise ask** with 2-3 slug candidates you derived from the intent (recommended first, marked "(Recommended)"); free-form is fine.

**Derive slugs yourself** (you are the LLM; no code derives names): from the name source ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the intent text, or the chosen candidate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â extract 3-5 key words (Task Name Generation, [Orchestrator Patterns Ãƒâ€šÃ‚Â§5](../orchestrator-framework/references/orchestrator-patterns.md)) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ lowercase kebab-case, 3-5 words of `[a-z0-9]`, no date prefix. Example: "compare caching strategies" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `compare-caching-strategies`. The final directory is `YYYY-MM-DD-<slug>` (fork execution date).

### Q4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Plan confirmation (before anything is written)

Skip only when intent, fork point, and name were ALL supplied by the argument (description + `--from` + `--name`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nothing was left to confirm. Otherwise print the fork plan and ask:

```
Fork plan
  Source:      <source-name> (task untouched)
  Intent:      <one line, from Q1 or the description argument>
  Fork point:  <slug> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <step name>
  Keeps:       <kept slugs> (verbatim)
  Re-runs:     <first step after the fork point>
  New task:    YYYY-MM-DD-<slug>
```

`question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Create this fork?" with options: **Create the fork** (Recommended) / **Change something** (user names what ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-open only that question, keep the other answers) / **Cancel** (print the resume command and end without writing anything). On Cancel: nothing has been copied ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not create the directory.

If the fork-name check later reports `NAME_TAKEN`, suggest a 1-word variation and re-ask via `question`. If it reports `INVALID_NAME`, fix the slug (pattern + message tell you what broke) and retry the same source name without re-prompting unless the fix needs more than casing/spacing.

## Execute (utility pass ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tool does the copy)

1. Call the `fork_task` tool with:
   - `taskRoot`: `.owflow/tasks`
   - `source`: the resolved task path (or identifier)
   - `slug`: your derived slug
   - `from`: the chosen fork point slug
   - `intent`: the one-line intent (omit the key when the user gave none)
2. **Tool-agnostic failure handling** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â any tool output starting with `INVALID_SOURCE`, `UNKNOWN_STEP`, `NAME_TAKEN`, or `INVALID_NAME` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix per the output's Hint (re-ask name on `NAME_TAKEN`/`INVALID_NAME`; re-derive fork point on the rest) and re-call the tool. Any other failure ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ print it and STOP.
3. **Validate the forked state** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run the `verify_template` tool on the FORK's `orchestrator-state.yml` (`filePath: <fork-path>/orchestrator-state.yml`, `templateName: orchestrator-state-research.yml`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â belt-and-braces over the tool's own structural check. Any report ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix per the hint, re-run.
4. **Present the fork summary**:

```
Fork created:            <fork-path>
Forked from:             <source-name> (task untouched)
Intent:                  <one line, or 'n/a'>
Fork point:              <slug> (<step name>)
Copied:                  everything from the source (verbatim)
State trimmed:           completed_phases cut at <slug> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â resumes at the step after <slug>
```

## Fork mechanics reference (what the tool does)

1. Copies the whole source task directory recursively into `<taskRoot>/research/YYYY-MM-DD-<slug>/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all artifacts, verbatim.
2. Rewrites only the copied `orchestrator-state.yml`: `orchestrator.completed_phases` sliced up to and including the fork point, `orchestrator.started_phase: null`, `orchestrator.entry_point: "research-fork"`, `orchestrator.task_path` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fork dir, `task.status: in_progress`, `task.title` suffixed `(fork of <source-name>)`, and `orchestrator.options.fork_information` stamped `{forked_from, fork_point, forked_at, intent}` (`intent` only when given) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â merged into any pre-existing `options`.
3. Everything else ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `research_context`, `research_outputs`, timestamps ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is carried verbatim from the source; the resumed step overwrites its own outputs.

Validation errors surfaced by the tool: `INVALID_NAME` (slug pattern), `INVALID_SOURCE` (no research task directory / no parseable state file), `UNKNOWN_STEP` (fork point not in `completed_phases`, or `research-completed` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nothing diverges after completion), `NAME_TAKEN` (fork directory already exists).

## Exit Gate

Utility skill: confirm-or-revise only ([Confirm-or-Revise Exception](../orchestrator-framework/references/confirm-or-revise-exception.md)) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no pipeline next-steps, no auto-chaining.

### Results box

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ RESEARCH FORK COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <fork name>

**Source** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <source-name> (task untouched)
**Intent** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <one line, or n/a>
**Fork point** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <fork-point slug> (<step name>)
**Copied** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full source directory (verbatim)
**State trim** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â completed_phases cut at <fork-point slug>
**Fork directory** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `<fork-path>`

**Fork state**

- `orchestrator-state.yml` (completed_phases trimmed at <fork-point slug>, status in_progress, `options.fork_information` stamped)
- all source artifacts, verbatim

**Next ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¸** `/owflow:research <fork-path>` (resume the fork; it routes to the first step after the fork point)
```

### Results-acceptance question

Use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Are these results correct?" with options:

- **Confirm** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the fork is good; end the skill (print the Next ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¸ command one more time for convenience).
- **Revise** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user specifies what to change (wrong fork point / wrong name / wrong intent): DELETE the fork directory ONLY with explicit user confirmation in that same message (`rm -rf` is destructive-hook protected for non-whitelisted agents ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run it only after the user re-confirms), or re-fork under a different name; then re-present the results box.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the resume command (`/owflow:research-fork <task-path>`) and end.

## Integration

- The fork is a normal research task from here on: `/owflow:research <fork-path>` routes it, `/owflow:goal-research <fork-path>` chains it, optional-chain choice gates apply as usual.
- Forking a FORK works ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the title suffix chains (`(fork of <fork-name>)`) and `options.fork_information.forked_from` records the immediate parent.
- The description argument also matches the dispatcher's convention of free text narrowing scope, so `/owflow:research-fork <task> explore the cost angle` behaves like `/owflow:development <task> Implement only phase 1`.
- Development and migration tasks are NOT forkable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill is research-only by design.
