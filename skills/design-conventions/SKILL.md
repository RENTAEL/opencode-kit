---
name: design-conventions
description: "**Purpose:** Keep skill operations one tool family. **Pattern:** Use `skill` to load and `skill_edit` to create or replace reusable `SKILL.md`. Use `learn` for durable local memory. Do not use removed `skill_read` or `skill_edit_reference`."
---
## Internal Acronyms
- None.

## Definitions
- **Skill**: Reusable agent guidance loaded by `skill` tool.
- **Local memory**: Durable local fact stored by `learn`; not a reusable skill.
- **Reference**: Companion file inside skill, read through `skill` `reference` arg.

## Naming Rules
### Skill Tool Names
**Purpose:** Keep skill operations one tool family.
**Pattern:** Use `skill` to load and `skill_edit` to create or replace reusable `SKILL.md`. Use `learn` for durable local memory. Do not use removed `skill_read` or `skill_edit_reference`.

### Skill Reference Names
**Purpose:** Keep companion files linked to main skill.
**Pattern:** Pass relative reference path in `skill` `reference` arg. Pass `references[]` to `skill_edit`.

---

**IMPORTANT**: Edit this `design-conventions` skillwhenever new naming conventions or domain terms are introduced.
