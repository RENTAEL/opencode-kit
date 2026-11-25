---
name: oc-domain
description: "Offer an ADR only when all three are true; otherwise skip it:"
---
# Domain Modeling

## Intent

- **Goal:** Actively build and sharpen the project's domain model while designing: challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallise.
- **Limits:** `CONTEXT.md` is a glossary and nothing else: no implementation details, not a spec, scratch pad, or decision log. Create files lazily: `CONTEXT.md` when the first term is resolved, `docs/adr/` when the first ADR is needed. Offer ADRs sparingly.
- **Fails if:** A term conflict or code contradiction goes unchallenged, resolved terms are batched instead of captured inline, or an ADR is offered without all three ADR criteria.

## Context

- **Reads:** `CONTEXT.md` (or `CONTEXT-MAP.md` plus per-context `CONTEXT.md`), `docs/adr/`, and the code the user describes.
- **Never reads:** none.
- **Persona:** Precise domain-language partner.
- **Scope:** Changing the model, not just consuming it. Merely reading `CONTEXT.md` for vocabulary is a one-line habit any skill can do and is not this skill.

## Expectations

- **Scenarios:**
  - WHEN a term conflicts with `CONTEXT.md` THEN call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which is it?"
  - WHEN a term is vague or overloaded THEN propose a precise canonical term: "You're saying 'account' ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do you mean the Customer or the User?"
  - WHEN domain relationships are discussed THEN stress-test them with invented edge-case scenarios that force precise boundaries.
  - WHEN the user states how something works THEN check the code and surface contradictions: "Your code cancels entire Orders, but you just said partial cancellation is possible ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which is right?"
  - WHEN a term is resolved THEN update `CONTEXT.md` right there using [CONTEXT-FORMAT.md](./assets/CONTEXT-FORMAT.md).
- **Done means:** Resolved terms are in `CONTEXT.md`; qualifying decisions are offered as ADRs in [ADR-FORMAT.md](./assets/ADR-FORMAT.md) format.
- **Quality needs:** Glossary entries are implementation-free and canonical.

## Method

Offer an ADR only when all three are true; otherwise skip it:

1. **Hard to reverse** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the cost of changing your mind later is meaningful.
2. **Surprising without context** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â there were genuine alternatives and you picked one for specific reasons.

File layout. Single context:

```
/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ CONTEXT.md
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ docs/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ adr/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡       ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ 0001-event-sourced-orders.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡       ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ 0002-postgres-for-write-model.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ src/
```

A root `CONTEXT-MAP.md` means multiple contexts; the map points to each:

```
/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ CONTEXT-MAP.md
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ docs/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ adr/                          ÃƒÂ¢Ã¢â‚¬Â Ã‚Â system-wide decisions
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ src/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ordering/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ CONTEXT.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ docs/adr/                 ÃƒÂ¢Ã¢â‚¬Â Ã‚Â context-specific decisions
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ billing/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡       ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ CONTEXT.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡       ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ docs/adr/
```

## Attribution

Original skill by Matt Pocock from <https://github.com/mattpocock/skills>.
