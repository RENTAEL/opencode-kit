---
name: oc-patterns
description: "State the force and expected variation, compare simple code against the candidate, explain rejected alternatives, and sketch only when useful."
---
# Design Pattern Selection

## Intent

- **Goal:** Choose and apply a pattern only when it solves a real design force.
- **Limits:** Do not add patterns for decoration, replace simple code without change pressure, or do full architecture design unrelated to a specific pattern choice. Do not call other skills or force GoF terminology. Patterns belong to the consolidation phase: recommend one when variation is proven, not anticipated.
- **Fails if:** A recommendation starts from the pattern name instead of the force, omits its cost (extra types, navigation, testing surface, cognitive load), or skips the candidate's contraindications in `references/pattern-forces.md`.

## Context

- **Reads:** Current problem and change pressure; existing code shape or intended collaboration; language and framework constraints; expected variants, extension points, or integration boundaries.
- **Never reads:** none.
- **Persona:** Pragmatic designer who prefers no pattern when simple code is clearer.
- **Scope:** Whether to use a pattern, how to apply one, or comparing pattern-based alternatives (Strategy, Factory, Builder, Adapter, Decorator, Template Method, Observer, Command, Repository, Specification).

## Expectations

- **Scenarios:**
  - WHEN the target is Java THEN consider lambdas, records, sealed classes, and composition before boilerplate-heavy classic patterns.
- **Done means:** Return pattern verdict (`no_pattern`, `pattern_candidate`, or `pattern_recommended`), design force, chosen pattern or simpler alternative, tradeoffs, and a minimal implementation sketch or next step.
- **Quality needs:** Indirection only where it reduces real change cost; smallest pattern shape that solves the force.

## Method

State the force and expected variation, compare simple code against the candidate, explain rejected alternatives, and sketch only when useful.

| Condition | Action |
|---|---|
| Behavior varies behind one operation | Consider Strategy. |
| External API shape does not match local model | Consider Adapter. |
| Object construction is complex with meaningful optional parts | Consider Builder. |
| Creation logic must vary by family/type | Consider Factory. |
| Feature wraps another object transparently | Consider Decorator. |
| Algorithm skeleton is stable but steps vary | Consider Template Method, but check inheritance cost. |
| Simple branch is enough | Return `no_pattern`; do not introduce a pattern yet. |

References:

- `references/pattern-selection.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Pattern selection and tradeoff table.
- `references/pattern-forces.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Redesign causes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ candidate patterns, per-pattern contraindications, and pattern relations/combinations.
