---
name: eval-harness-first
description: Build the evaluation harness that gates every fine-tuning run â€” golden sets, per-failure-mode graders, judge calibration, and base-model baselines. Use when starting a fine-tuning effort, when converting traces into an eval set, or when calibrating a judge against human labels.
---
# Eval Harness First

The Phase 0 gate for the whole plugin:
`finetuning-method-selection` and every downstream
skill assume this harness exists before a training
config gets written. The harness is not a run-end
side artifact ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it is the data-curation engine. The
same labeled traces that build the goldens feed
training data, minus an explicit holdout.

**Input:** production/agent traces if they exist, or
a task spec if they don't, plus labelers willing to
grade ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥100 examples.
**Output format:** the `eval/` directory below ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
goldens, graders, drift suite, and the base-model
baseline that later phases gate on.

## The Gate

No eval harness, no fine-tune. Skip to a training
config and there is nothing to measure against,
nothing to catch regressions, and no labeled data
to train on. The flywheel:

1. **Collect traces** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â production/agent spans, or
   synthetic tasks if none exist yet.
2. **Error analysis** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â open coding on ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥100 traces,
   axial coding into 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“8 failure buckets.
3. **One grader per bucket** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â deterministic first;
   calibrated LLM-judge only for genuinely
   subjective criteria.
4. **Prioritize** by frequency ÃƒÆ’Ã¢â‚¬â€ severity ÃƒÆ’Ã¢â‚¬â€ value.
5. **The labeled traces feed dataset curation, minus
   an explicit holdout.** Every `eval/goldens.jsonl`
   ID stays excluded from training data by ID.
6. **Train.**
7. **Re-run the same harness** on the checkpoint ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
   not a different, looser one.
8. **Drift detection feeds back to step 2** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â new
   production failure modes re-open error analysis.

Steps 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 build the harness; steps 5ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“8 are why it
must exist first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it is both the training data
source and the checkpoint's exit gate.

## Building Goldens

- **From traces, when they exist:** run error
  analysis ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â open coding on ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥100 real traces (read
  them, tag failures in your own words, no fixed
  taxonomy yet), then axial coding to collapse those
  tags into 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“8 named failure buckets. Fewer than 4
  means the coding pass was too shallow; more than 8
  means buckets need merging. **Exception:**
  single-failure-surface tasks (e.g. strict-schema
  extraction) may land at 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“2 buckets with per-field
  sub-metrics inside one grader ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't invent
  artificial splits with no evidence behind them.
- **Synthetic, when traces don't exist yet:**
  dimension-based generation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â enumerate the axes
  that matter (task type, difficulty, edge case,
  persona) and sample the cross-product; free-
  generated prompts cluster around whatever's
  easiest to write.
- **Goldens are versioned like code** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â commit
  `eval/goldens.jsonl`, diff it in review, tag it per
  release. It doubles as the CI regression suite.

## Graders

One grader per failure bucket from error analysis ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
not one for the whole eval set. A single blended
score hides which bucket regressed.

- **Deterministic first.** Regex, schema validation,
  or execution checks are cheaper, reproducible, and
  need no calibration.
- **LLM-judge only for genuinely subjective
  criteria** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tone, faithfulness, "which response
  is better" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â where no deterministic check can
  express it.
- **Binary pass/fail over Likert.** A 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 or 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“10
  scale is noisier to calibrate and harder to apply
  consistently; collapse to pass/fail.
- **Drift-suite MMLU-style scoring: prefer logprob
  over generate-and-extract** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a tight token budget
  makes generate-and-extract parse-brittle for models
  that preamble, conflating format compliance with
  the knowledge being measured. Templates for all
  four grader shapes and this scoring note:
  `references/grader-templates.md`.

## Judge Calibration Is a Prerequisite

Any bucket routed to an LLM-judge needs calibration
before its verdicts count for anything beyond
exploration ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a hard prerequisite, not a
nice-to-have. **N/A when no bucket routes to a
judge** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an all-deterministic harness has nothing
to calibrate; state that rather than leaving this
section unaddressed.

- Label ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥100 items, split **train**/**dev**/**sealed
  test** (report once, no re-touching after).
- Report **TPR and TNR**, not one blended accuracy
  number ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a judge can hit 90% by always saying
  "pass" on a skewed set.
- **Pin the judge to a fixed model snapshot** and
  recalibrate on judge-model change, quarterly
  regardless.
- **The judge must come from a different model family
  than the model under test.**
- A judge that misses the agreed TPR/TNR bar ships
  **advisory-only** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â flags for human review, never
  gates a promotion. Full protocol, bias correction,
  and recalibration checklist:
  `references/judge-calibration.md`.

## The Baseline

Before Phase 1 (method selection) starts, run the
full harness ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â goldens plus the capability-drift
suite ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â against the unmodified base model. This is
the number every later checkpoint gets compared
against.

`eval/baseline-<model>.json` is the gate token. No
baseline file, no comparison basis for
`checkpoint-promotion` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a checkpoint that "looks
better" against nothing measured isn't a finding.

## Directory Contract

```
eval/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ goldens.jsonl          # labeled traces + synthetic goldens, versioned
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ graders/                # one module per failure bucket
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ schema_compliance.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ exact_match.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ rubric_judge.py
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ drift-suite.yaml        # frozen benchmarks + 200-500 domain-adjacent items
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ baseline-<model>.json   # gate token: harness + drift suite vs the base model
runs/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ <run-id>/
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ results.json         # per-run harness output, one per checkpoint
```

`eval/` persists across runs and lives outside
`runs/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the fixed measuring stick, not a run
artifact. `runs/` is disposable; `eval/` is not.
Never let a run script write into `eval/`. **Canonical
location:** every per-trace `results.json` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the
Phase 0 baseline included ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â lives at
`runs/<run-id>/results.json`, never under
`eval/runs/...`; an instruction requesting the
latter is wrong, not this contract.

### Phase 0 Exit Checklist

Before `finetuning-method-selection`, confirm:

1. ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥100 traces open-coded; 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“8 failure buckets (N/A
   floor for synthetic goldens on a single-failure-
   surface task ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see the Building Goldens exception;
   bucket count then comes from post-baseline error
   analysis instead).
2. `eval/goldens.jsonl` committed and versioned.
3. One grader per bucket, deterministic first.
4. Judges calibrated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â TPR/TNR, snapshot pinned,
   different family (**N/A when no bucket routes to
   an LLM-judge**; state that explicitly).
5. `eval/drift-suite.yaml` frozen.
6. `eval/baseline-<model>.json` written.

Missing any of the six (or its stated N/A)? Not
Phase 0 complete ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `/finetune` checks the baseline
file before a run.

## Related Skills

General-purpose evaluation guidance (dashboards, A/B
testing, non-fine-tuning harnesses) lives in the
`llm-application-dev` plugin's `llm-evaluation`
skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill covers only the fine-tuning
coupling: goldens that double as training data, and
the baseline that gates a checkpoint.

- `finetuning-method-selection` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â routes here first.
- `dataset-curation` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â formats these traces into
  training rows.
- `trace-to-training-data` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â turns graded traces into
  training examples.
- `checkpoint-promotion` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â consumes
  `baseline-<model>.json`, re-runs this harness on
  each candidate checkpoint.

## References

- `references/grader-templates.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â runnable grader
  examples per shape, plus a `drift-suite.yaml`
  example and MMLU logprob-scoring note.
- `references/judge-calibration.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the
  calibration protocol, including the all-
  deterministic N/A path.
