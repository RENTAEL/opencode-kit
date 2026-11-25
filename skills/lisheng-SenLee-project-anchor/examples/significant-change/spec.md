# Change Spec: Idempotent Job Retry

## Requirements

### REQ-001 — Stable retry identity

Retries of one logical job execution use the same idempotency key.

### REQ-002 — Duplicate side-effect suppression

If the first external write committed but its response was lost, a retry must not create a second external effect.

## Scenario: ambiguous timeout after commit

**GIVEN** an external write committed successfully

**WHEN** the response is lost and the job retries

**THEN** the retry reuses the original idempotency key and the external system observes one logical effect.

## Acceptance Criteria

- [ ] Retry identity is stable for one logical execution.
- [ ] A committed write followed by a timeout does not duplicate the effect.
- [ ] Existing non-writing jobs preserve current behavior.
