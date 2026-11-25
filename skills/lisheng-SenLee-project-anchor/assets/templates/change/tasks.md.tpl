# Change Tasks: {{CHANGE_TITLE}}

## Plan

- [ ] Understand relevant current truth and code
- [ ] Finalize spec
- [ ] Finalize design
- [ ] Initialize execution state from authoritative change docs
- [ ] Implement
- [ ] Add/update tests
- [ ] Run verification
- [ ] Reconcile intent/spec/code/tests/docs
- [ ] Update current truth
- [ ] Archive change

## Execution State
Keep this compact and operational. Link authoritative facts instead of copying them.

### Goal
Link `proposal.md#goal--outcome` or another authoritative goal.

TBD

### Core Anchors
Link only the constraints/specs/invariants/ADRs that must remain true during implementation.

TBD

### Active Slice
What one coherent implementation slice is in focus now? Keep unrelated work out of the working set.

TBD

### Next
What is the next concrete action within or immediately after this slice?

TBD

### Deferred (optional)
Known work that matters later but should not compete for attention now. Omit or leave empty when unnecessary.


## Progress Notes
Keep this concise. Record only decisions, blockers, or failure diagnoses that materially change how the task should continue.

For a decision-relevant failed attempt, prefer:

- Attempt: what was tried
- Result: what failed
- Diagnosis: why it failed
- Do not repeat: what this rules out
- Next: the changed approach

## Verification Evidence
Record what was actually covered, not only which command was run.

For each high-signal check, prefer:

- Verifier: test / command / review
- Covers: requirement / invariant / failure mode / lifecycle or concurrency case
- Result: pass / fail + decision-relevant note

TBD

## Open Questions
TBD
