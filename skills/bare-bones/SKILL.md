---
name: bare-bones
description: "Use this skill for a writing task, not for every user response."
---
# Bare-Bones Writing

Use this skill for a writing task, not for every user response.

## Modes

- **Edit:** Return the revised text. Preserve meaning, uncertainty, conditions, exceptions, numbers, versions, warnings, attribution, and technical names.
- **Audit:** Name each pattern, quote the affected text, and give a short fix. Do not rewrite, score, infer authorship, or invent evidence.
- **Strict STE:** Use only when the user asks for ASD-STE100 or strict Simplified Technical English. Read `references/checklist.md`. State that full compliance requires the official dictionary and human review.

For general prose, preserve the writer's vocabulary, cadence, humor, bluntness, and genuine uncertainty. Make the minimum effective edit. Do not flatten the text into polished generic prose.

For technical prose, use short direct sentences, active voice when the actor matters, one term per concept, and concrete facts. Keep code, commands, identifiers, paths, quoted errors, product names, and configuration keys exact.

## Remove

- throat-clearing and repeated conclusions
- unsupported importance claims and unnamed authority
- marketing adjectives without measurements
- synonym rotation for the same concept
- nominalizations when a direct verb is clearer
- dramatic fragments, binary contrast formulas, and decorative formatting
- filler such as "it is worth noting" or "in order to"

Do not remove a hedge that expresses real confidence or possibility. Do not replace a precise domain term with a vague plain word.

## Output

Return only the edited text unless the user asks for an explanation. For an audit, list findings first. If the source already meets the request, say so without forcing changes.

Before delivery, compare the result with the source fact by fact. Restore any lost condition, actor, qualifier, number, exception, warning, or attribution.

Adapted from wilmai/ste, danyuchn/asd-ste100-skill, mshojaei77/adhd-friendly-ste-technical-writer, and petergyang/no-ai-slop (MIT).
