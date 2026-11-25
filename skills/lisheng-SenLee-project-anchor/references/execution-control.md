# Execution control for significant changes

Use this only when a significant change is long-running, multi-step, failure-prone, interrupted/resumed, or at meaningful risk of drifting. It is not a per-tool-call protocol.

## Purpose

The active change defines the intended future state. Execution control keeps the current implementation task pointed at that state while work is underway.

`proposal/spec/design -> compact execution state -> implementation -> seam refresh -> verification -> reconciliation`

## Execution State

Keep these fields in `tasks.md`:

- `Goal`: a reference to the authoritative goal.
- `Core Anchors`: links to the small set of constraints, specs, invariants, boundaries, or ADRs that must stay true.
- `Active Slice`: the one coherent implementation slice currently in focus.
- `Next`: the next concrete action within or immediately after that slice.
- `Deferred` (optional): known later work that should not compete for current attention.

Do not copy whole requirements into execution state. If execution state conflicts with an authoritative document, the authoritative document wins and execution state must be corrected.

## Significant seams

Refresh execution state only at useful boundaries, such as:

- a major implementation slice completed;
- a new fact changes the plan or invalidates an assumption;
- verification fails and the approach must change;
- scope is about to expand across modules or product boundaries;
- work resumes after interruption, context reset, or handoff;
- implementation appears complete and is about to enter final reconciliation.

At a seam, ask:

1. Is the original goal still the goal?
2. Are the core anchors still respected?
3. What changed, became verified, or became uncertain?
4. Is the active slice still the right focus, and is the recorded `Next` still the best next action?

Keep the refresh short. Do not create a new artifact for every seam.

## Working-set control

Keep one coherent active slice in focus at a time. If another concern is real but not needed for the current slice, put it in `Deferred` and return to it later.

Do not impose fixed limits on files, requirements, or subtasks. Split only when competing concerns are causing context switching or loss of focus. `Deferred` is a parking area, not a backlog duplicate; keep only items useful for preventing accidental scope switching.

## Diagnosis-carrying retry

Avoid repeating a failed approach without learning from it. Record a failed attempt only when it changes a future decision.

Use this shape when useful:

```text
Attempt: <what was tried>
Result: <observable failure>
Diagnosis: <why the attempt was insufficient>
Do not repeat: <approach or assumption now ruled out>
Next: <new approach>
```

Do not materially repeat a failed approach unless new evidence or a changed hypothesis justifies it.

Do not turn progress notes into a raw execution log.

## Verification evidence

Verification should connect a verifier to what it actually covers:

```text
Verifier: <test / command / review>
Covers: <requirement / invariant / failure mode / lifecycle or concurrency case>
Result: <PASS|FAIL + decision-relevant note>
```

A green suite is useful but does not by itself prove that the intended requirement or invariant was exercised.

## Completion gate

Do not equate code-complete or green tests with change-complete. A significant change can close only when required scope/acceptance criteria are accounted for, important behavior has meaningful verification coverage, correctness-affecting blockers/open questions are resolved, and final reconciliation is complete.

This is a final gate, not another workflow stage or artifact.

## Boundaries

This control layer is intentionally lightweight:

- no private chain-of-thought capture;
- no full transcript or tool history;
- no checkpoint on every model/tool iteration;
- no duplicate source of truth;
- no new long-lived current-truth document;
- no requirement to use it for trivial changes.

Its job is only to keep significant implementation work aligned until final reconciliation.
