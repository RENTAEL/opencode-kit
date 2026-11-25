---
name: oc-chained-pr
description: "oc-chained-pr"
---
# Chained PR

## Intent

- **Goal:** Split oversized work into chained PR review slices.
- **Limits:** Split by behavior, migration, or evidence unit, not file type; tests and docs ride with the slice they prove. Never chain to hide broken tests, missing evidence, or mixed behavior fixes.
- **Fails if:** a slice cannot be understood, verified, or rolled back alone; base branches or dependency order are undefined before implementation.

## Context

- **Reads:** review-size evidence; `oc-commits` review-splitting guidance when available (stay aligned).
- **Never reads:** none.
- **Persona:** delivery planner.
- **Scope:** workflows naming `oc-chained-pr`, only when evidence shows one PR is hard to review safely.

## Expectations

- **Scenarios:** WHEN ordering, ownership, or a size exception is unclear THEN stop for a human decision.
- **Done means:** strategy, slice order with base branches, expected files or size, per-slice verification, rollback boundary, any approved size exception.
- **Quality needs:** none beyond repository conventions.
