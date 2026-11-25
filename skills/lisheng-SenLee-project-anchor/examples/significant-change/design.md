# Change Design: Idempotent Job Retry

## Approach

Generate the idempotency key when the logical execution is claimed and persist it with execution state. Every retry reads and reuses that key.

## Affected Components

- execution persistence
- retry runner
- external-write adapter

## Data / Control Flow

```text
claim execution
    -> create/persist idempotency key
    -> perform external write(key)
    -> ambiguous timeout
    -> retry same execution
    -> read same key
    -> external write(key)
    -> external system deduplicates
```

## Failure Handling

If persistence of the key fails, do not perform the external write.

## Alternatives Considered

Generating a fresh key per retry was rejected because it cannot distinguish a retry from a new logical effect.
