# Change Tasks: Idempotent Job Retry

## Plan

- [x] Understand current retry path
- [x] Finalize spec and design
- [x] Implement persisted idempotency key
- [x] Add retry tests
- [x] Run verification
- [ ] Reconcile and update current truth
- [ ] Archive change

## Execution State

### Goal

See [`proposal.md#goal--outcome`](proposal.md#goal--outcome).

### Core Anchors

- [`spec.md#req-001--stable-retry-identity`](spec.md#req-001--stable-retry-identity)
- [`spec.md#req-002--duplicate-side-effect-suppression`](spec.md#req-002--duplicate-side-effect-suppression)
- Preserve existing non-writing job behavior.

### Active Slice

Reconcile the implemented retry path and verification evidence against the final spec before closing the change.

### Next

Confirm current architecture documentation describes idempotency-key ownership and then update it only if needed.

### Deferred (optional)

Scheduler-wide deduplication ideas are out of scope for this change.

## Progress Notes

- Attempt: generate an idempotency key inside each retry attempt.
- Result: the ambiguous-timeout test produced two external effects.
- Diagnosis: retry identity changed between attempts.
- Do not repeat: per-attempt key generation for one logical execution.
- Next: persist the key at execution-claim time and reuse it on retry.

## Verification Evidence

- Verifier: `test_retry_reuses_idempotency_key`
- Covers: REQ-001 stable retry identity
- Result: PASS

- Verifier: `test_timeout_after_commit_does_not_duplicate_effect`
- Covers: REQ-002 ambiguous timeout after committed external write
- Result: PASS

- Verifier: existing non-writing job regression suite
- Covers: backward compatibility constraint
- Result: PASS

## Open Questions

None affecting correctness or intended scope.
