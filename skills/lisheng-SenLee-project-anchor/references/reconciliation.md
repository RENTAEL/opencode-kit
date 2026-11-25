# Final reconciliation

Perform this before closing a significant change.

## Intent
- Is the original goal achieved?
- Did scope drift?
- Are non-goals respected?

## Spec
- Is every major requirement implemented?
- Are edge cases handled?
- Does the spec describe delivered behavior rather than an abandoned plan?

## Boundaries and invariants
- Did the change cross a product boundary?
- Are relevant invariants still true?
- Should a new invariant/test be added?

## Implementation and verification
- Do tests verify important behavior rather than incidental implementation?
- Are failure, concurrency, lifecycle, and persistence cases covered where relevant?
- For major requirements and invariants, can you identify verification evidence that actually covers them rather than only a green command result?
- Did test success hide a semantic mismatch with the spec?
- Are there unresolved decision-relevant failure diagnoses or open questions in `tasks.md`?

## Execution alignment
- Did the implementation drift away from the original goal or core anchors during execution?
- If scope or design changed, was that change explicitly reconciled into the active change instead of silently becoming the new goal?
- Does the final implementation match the authoritative proposal/spec/design rather than stale execution-state notes?

## Completion gate
- Is required scope implemented and are acceptance criteria accounted for?
- Is important behavior/invariant coverage evidenced, not merely a green command?
- Is any unresolved blocker or open question still relevant to correctness or intended scope?
- If any answer prevents confident completion, do not close the change yet.

## Architecture and ADR
- Does architecture documentation describe the actual system?
- Was a durable architecture decision introduced or superseded?

## Convergence

Aim for:

`Intent = Spec = Implementation = Tests/Verification = Current Truth`

Then update current truth and archive the active change.
