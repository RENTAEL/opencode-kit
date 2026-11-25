# LEARNINGS - self-correcting memory (SEED TEMPLATE)

> This is the committed SEED that ships with the repo. **Do not write personal
> learnings here.** On first run the skill copies this file to `LEARNINGS.md`,
> which is git-ignored and stays LOCAL to each user's machine. That way every
> clone starts from the same clean seed and then grows its own private memory -
> the file does not develop universally in the public repo.

The working file (`LEARNINGS.md`) is the skill's memory. **Read it at the start
of every run** and apply every relevant rule. **Append to it whenever the user
says the output was wrong, not what they expected, or asks to try again.** Keep
it deduplicated and ordered with the highest-value / most-recent rules near the
top of each section.

## How to add a lesson
Use this exact block format so entries stay consistent and machine-readable:

```
### [YYYY-MM-DD] <short title>
- Domain: <app | website | ui-ux | presentation | code | writing | research | data | general>
- Trigger/context: <what the user asked; what situation this applies to>
- Mistake: <what went wrong in the output>
- Root cause (prompting gap): <what the Spec under-specified or wrongly assumed>
- Rule to apply next time: <the concrete corrective instruction>
```

Rules:
1. Before adding, scan for an existing similar rule. If found, **sharpen/merge** it instead of duplicating.
2. If a mistake is domain-wide (not a one-off), also update `references/domain-playbooks.md`.
3. Prefer rules that are specific and testable ("default dark theme unless asked") over vague ones ("make UI better").
4. Keep this file lean; prune stale or contradicted rules.

---

## Global rules (apply to all domains)
<!-- Seeded starters distilled from the source courses. Extend over time. -->

### [seed] Always resolve the Gap Finder before building
- Domain: general
- Trigger/context: any underspecified request
- Mistake: producing generic output because audience/format/constraints were assumed
- Root cause (prompting gap): skipped clarification and stated no assumptions
- Rule to apply next time: fill the Gap-Finder checklist; ask a focused question batch OR state assumptions explicitly before producing anything.

### [seed] Never invent facts, APIs, libraries, or data
- Domain: general
- Trigger/context: factual answers and code
- Mistake: confident but fabricated details (hallucinated endpoints/benchmarks)
- Root cause (prompting gap): no grounding constraint; no permission to say "unknown"
- Rule to apply next time: use only provided/verifiable inputs; verify via tools/search when time-sensitive; flag gaps; give permission to say "I don't know."

---

## App building
<!-- Append learned rules here. -->

## Websites / landing pages
<!-- Append learned rules here. -->

## UI / UX design
<!-- Append learned rules here. -->

## Presentations / slides
<!-- Append learned rules here. -->

## Code / refactoring
<!-- Append learned rules here. -->

## Writing / content
<!-- Append learned rules here. -->

## Research / analysis
<!-- Append learned rules here. -->
