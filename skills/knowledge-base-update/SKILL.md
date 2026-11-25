---
name: knowledge-base-update
description: "Activate this skill when any of the following occur:"
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, konuÃƒâ€¦Ã…Â¸ma sÃƒâ€žÃ‚Â±rasÃƒâ€žÃ‚Â±nda ÃƒÆ’Ã‚Â¶Ãƒâ€žÃ…Â¸renilen ÃƒÆ’Ã‚Â¶nemli bilgilerin kaybolmamasÃƒâ€žÃ‚Â± iÃƒÆ’Ã‚Â§in kullanÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±r.
  Mimari kararlar, proje kurallarÃƒâ€žÃ‚Â±, bug kÃƒÆ’Ã‚Â¶ken nedenleri, 3. parti servis tuzaklarÃƒâ€žÃ‚Â± veya
  tekrar araÃƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmasÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± istemediÃƒâ€žÃ…Â¸in her Ãƒâ€¦Ã…Â¸eyi yapÃƒâ€žÃ‚Â±landÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸ biÃƒÆ’Ã‚Â§imde .agent/knowledge/
  dizinine yazar. BÃƒÆ’Ã‚Â¶ylece gelecekteki agent'lar aynÃƒâ€žÃ‚Â± soruyu sÃƒâ€žÃ‚Â±fÃƒâ€žÃ‚Â±rdan araÃƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rmak zorunda kalmaz.

  NE ZAMAN: ÃƒÆ’Ã¢â‚¬â€œnemli bir karar alÃƒâ€žÃ‚Â±ndÃƒâ€žÃ‚Â±Ãƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±nda, sÃƒÆ’Ã‚Â¼rpriz bir bug ÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â¶zÃƒÆ’Ã‚Â¼ldÃƒÆ’Ã‚Â¼Ãƒâ€žÃ…Â¸ÃƒÆ’Ã‚Â¼nde,
            bir API davranÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â± belgelendiÃƒâ€žÃ…Â¸inde, yeni bir proje kuralÃƒâ€žÃ‚Â± oluÃƒâ€¦Ã…Â¸turulduÃƒâ€žÃ…Â¸unda.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    .agent/knowledge/<slug>.md + INDEX.md satÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±
-->

# Knowledge Base Update Skill

## When to Trigger

Activate this skill when any of the following occur:

- An architectural or tech-stack decision is made (and the *why* matters)
- A non-obvious bug is fixed (root cause + fix documented)
- A 3rd-party service/API has a quirk, limit, or gotcha discovered
- A project convention is established (naming, folder structure, patterns)
- A research question is answered after significant investigation
- A "we tried X and it failed because Y" moment happens

## Step-by-Step Process

### 1. Identify the Entry Type

Choose the category that best describes what was learned:

| Type | When to Use |
|------|------------|
| `decision` | Architecture, tech choices, trade-offs |
| `convention` | Naming rules, code patterns, folder structures |
| `bug` | Root cause + fix for a non-obvious problem |
| `gotcha` | 3rd-party quirk, env issue, edge case trap |
| `research` | Answer to a question requiring significant investigation |

### 2. Determine the File Path

Write to: `.agent/knowledge/<slug>.md`

- `slug` = kebab-case summary of the topic (e.g., `auth-token-refresh-strategy`)
- If an entry for this topic already exists, **update it** rather than creating a new file
- Group related topics under subfolders: `.agent/knowledge/auth/`, `.agent/knowledge/infra/`, etc.

### 3. Write the Entry

Use this exact template:

```markdown
---
type: <decision|convention|bug|gotcha|research>
topic: <Short human-readable title>
date: <YYYY-MM-DD>
tags: [<tag1>, <tag2>]
---

## Summary
<One or two sentences ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what was learned, bottom line up front>

## Context
<Why this came up. What problem were we solving?>

## Decision / Finding
<The actual content. Be specific. Include code snippets if helpful.>

## Rationale
<Why this choice over alternatives. What alternatives were rejected and why.>

## Consequences
<What does this affect going forward? What to watch out for?>

## References
- <File path, PR link, conversation snippet, or external URL>
```

### 4. Update the Index

After writing the entry, append a one-line summary to `.agent/knowledge/INDEX.md`:

```
| <date> | <type> | [<topic>](./<path>.md) | <one-line summary> |
```

If `INDEX.md` doesn't exist yet, create it with this header first:

```markdown
# Project Knowledge Base

| Date | Type | Topic | Summary |
|------|------|-------|---------|
```

### 5. Confirm to User

After writing, report:
- What was saved and where
- The one-line summary that was added to the index

## Rules

- **Never summarize vaguely.** "We decided to use X" is useless without *why*.
- **Include the anti-pattern.** If something was tried and rejected, document it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that's often the most valuable knowledge.
- **Keep entries atomic.** One topic per file. Don't bundle unrelated decisions.
- **Date is mandatory.** Future agents need to know how fresh this knowledge is.
- **If in doubt, write it.** The cost of a redundant entry is low. The cost of a missing one is re-doing the work.
