# Change Proposal: Idempotent Job Retry

## Goal / Outcome

A retried job must not create duplicate external side effects after the first successful commit.

## Context / Problem

The current runner can retry after an ambiguous timeout. A second attempt may repeat an already-committed external write.

## Scope

- Persist an idempotency key per logical job execution.
- Reuse the same key across retries of that execution.
- Verify duplicate delivery is suppressed.

## Non-Goals

- Redesigning the scheduler.
- Changing job ordering semantics.
- Adding distributed locking to unrelated job types.

## Constraints

- Existing successful jobs must remain readable.
- Retry behavior must remain backward compatible for jobs without external writes.

## Verification

Automated tests must cover the ambiguous-timeout retry path and prove only one external effect is committed.

## Done When

The behavior in `spec.md` is implemented, verified, reconciled, and reflected in current-truth documentation where needed.
