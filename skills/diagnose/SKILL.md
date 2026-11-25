---
name: diagnose
description: "Systematic debugging. Never guess and patch ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â build a feedback loop, prove the hypothesis, fix once."
---
# /supergraph:diagnose

Systematic debugging. Never guess and patch ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â build a feedback loop, prove the hypothesis, fix once.

Announce: "ÃƒÂ°Ã…Â¸Ã‚ÂÃ¢â‚¬Âº /supergraph:diagnose ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â building feedback loop..."

## Setup

**Read `.supergraph-env` for test/lint commands (if exists):**
```bash
[ -f .supergraph-env ] && source .supergraph-env
```
This sets `$TEST_CMD`, `$FOCUSED_TEST_CMD`, `$LINT_CMD`. If absent, detect from project config (package.json ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ jest/vitest, pubspec.yaml ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flutter test, etc.) same as `/supergraph:scan`.

## Phases

### Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Build Feedback Loop

Before touching any code, establish a fast, deterministic way to observe the bug.

```bash
# Identify the smallest command that shows the failure
$TEST_CMD --grep "<failing test name>"   # focused test run
# or
<minimal repro command>
```

**Goal:** failure visible in < 5 seconds. If not, slim down the repro.
Do NOT skip this phase. Debugging without a feedback loop is guessing.

### Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Reproduce Cleanly

- Run the feedback loop 3 times ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm it fails consistently
- Capture exact error output, stack trace, exit code
- Note any flakiness ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ treat as separate bug before continuing
- Add a failing regression test if one doesn't exist:
  ```
  test("<bug description>", () => { ... }) // RED
  ```

### Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Hypothesize (3-5 ranked theories)

List falsifiable hypotheses, ordered most-to-least likely:

```
1. [Most likely] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [reason] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [how to falsify]
2. [Second]      ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [reason] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [how to falsify]
3. [Third]       ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [reason] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [how to falsify]
```

Rules:
- Each hypothesis must be falsifiable (observable test to disprove it)
- No implementation yet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only theories
- Use graph context if available:
  ```
  search_graph(project=CBM_PROJECT, name_pattern=<suspect>)
  trace_path(project=CBM_PROJECT, direction="inbound")
  trace_path(project=CBM_PROJECT, direction="outbound")
  ```

### Phase 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Instrument (one variable at a time)

Test hypothesis #1 first. Change ONE thing to observe ONE signal:

- Add targeted log/assertion near the suspect code
- Run feedback loop ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ confirm or refute
- Remove instrumentation after each test ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never accumulate debug logs
- If refuted ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ move to hypothesis #2
- Stop when hypothesis is confirmed

**Rule:** Never change the code under test and the instrumentation simultaneously.

### Phase 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Fix + Regression Test

Once root cause is confirmed:

1. Write/update the regression test first (stays RED)
2. Apply minimal fix
3. Run feedback loop ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ GREEN
4. Run full test suite ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no regressions
5. Run lint: `$LINT_CMD`

Minimal fix means: fix the cause, not the symptom. If the fix touches a hub node ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ get user approval first.
If search/trace returns empty, label graph evidence unavailable and fall back to
Serena/filesystem evidence. Use the validated `test-gaps` recipe for missing tests.

### Phase 6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Cleanup + Post-mortem

- Remove all debug instrumentation and temp files
- Update CONTEXT.md if bug revealed a hidden domain invariant
- One-sentence post-mortem:
  ```
  Root cause: [X]
  Fix: [Y]
  Prevented recurrence by: [regression test / invariant documented]
  ```
- Checkpoint:
  ```bash
  git add [exact files]
  git commit -m "fix: <description>"
  ```

## Report

```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ /supergraph:diagnose complete
- Root cause: [confirmed hypothesis]
- Fix: [what changed]
- Regression test: [test name / path]
- Tests: PASS | Lint: PASS
- Next: /supergraph:fix (if more issues) or /supergraph:verify
```

## Rules

- Never skip Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â feedback loop is mandatory
- Never change two variables simultaneously in Phase 4
- Never commit without a regression test
- If hypotheses exhausted with no match ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ stop, report to user with all observations
