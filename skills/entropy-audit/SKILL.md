---
name: entropy-audit
description: "Run a structured entropy audit and output a deterministic cleanup plan."
---
# Skill: entropy-audit

Run a structured entropy audit and output a deterministic cleanup plan.

## When to Use

- User asks to clean the project or audit technical debt.
- After major feature delivery, refactor, or migration.
- When code/docs drift and structural inconsistency increase maintenance cost.

## When Not to Use

- Feature implementation requests.
- Incident debugging unrelated to codebase health.
- Architecture redesign not driven by entropy reduction.

## Operating Rules

1. Do not apply code changes directly.
2. Generate **one artifact only**: `CLEANING_PLAN.md`.
3. Every recommendation must be evidence-backed.
4. Favor low-risk, high-impact actions.

## Execution Workflow

### Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Repository Observation

- Map modules and ownership boundaries.
- Detect entropy markers: `TODO`, `FIXME`, `DEPRECATED`, stale comments,
  duplicated patterns, orphan files, unused exports.

### Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Coherence and Drift Analysis

- Compare README/JSDoc/contracts against actual function signatures and flows.
- Identify naming/style divergence within related folders.
- Detect over-complex code blocks that can be simplified safely.

### Step 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Safety Classification

For each candidate action, classify:

- **Confidence**: `high` / `medium` / `low`
- **Risk**: `low` / `medium` / `high`
- **Blast radius**: local / module / cross-module

If confidence is low or blast radius is wide, route to **Deferred / Investigate**.

### Step 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Plan Construction

Write `CLEANING_PLAN.md` using the template below.

## Required `CLEANING_PLAN.md` Template

```markdown
# Cleaning Plan

## Scope

- Audited directories:
- Exclusions:
- Audit timestamp:

## Audit Score

- Overall health score: X/10
- Summary rationale:

## Priority Actions

### [P1] <short title>

- ID:
- Category:
- Evidence:
- Proposed change:
- Expected gain:
- Risk level:
- Regression guard:

## Polishing Actions

### [P2] <short title>

- ID:
- Category:
- Evidence:
- Proposed change:
- Expected gain:
- Risk level:
- Regression guard:

## Risk Review

- High-risk items:
- Potential side effects:
- Recommended sequencing:

## Validation Checklist

- [ ] Static validation (lint/typecheck)
- [ ] Test coverage impact reviewed
- [ ] Behavior-sensitive paths revalidated
- [ ] Docs updated with code changes

## Deferred / Investigate

### [D1] <short title>

- Why deferred:
- What evidence is missing:
- Suggested next verification:
```

## Quality Bar

- No vague recommendations.
- No recommendation without file/symbol-level evidence.
- No deletion proposal without explicit regression guard.
- Keep actions small, composable, and review-friendly.
