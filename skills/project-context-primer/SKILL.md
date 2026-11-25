---
name: project-context-primer
description: "**Always run first** when:"
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, yeni bir konuÃƒâ€¦Ã…Â¸ma veya agent oturumu baÃƒâ€¦Ã…Â¸ladÃƒâ€žÃ‚Â±Ãƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±nda projenin baÃƒâ€žÃ…Â¸lamÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±
  hÃƒâ€žÃ‚Â±zla yÃƒÆ’Ã‚Â¼klemek iÃƒÆ’Ã‚Â§in kullanÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±r. Mimari kararlar, kurallar, bilinen tuzaklar ve
  mevcut gÃƒÆ’Ã‚Â¶rev durumu yÃƒÆ’Ã‚Â¼klenerek agent "boÃƒâ€¦Ã…Â¸ sayfa" modunda deÃƒâ€žÃ…Â¸il, tam baÃƒâ€žÃ…Â¸lamla ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â±r.
  Kod yazmadan ÃƒÆ’Ã‚Â¶nce MUTLAKA ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmalÃƒâ€žÃ‚Â±dÃƒâ€žÃ‚Â±r ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bu, yeniden iÃƒâ€¦Ã…Â¸ yapmanÃƒâ€žÃ‚Â±n en ucuz ÃƒÆ’Ã‚Â¶nlemidir.

  NE ZAMAN: Her yeni konuÃƒâ€¦Ã…Â¸manÃƒâ€žÃ‚Â±n ilk adÃƒâ€žÃ‚Â±mÃƒâ€žÃ‚Â± olarak. HÃƒâ€žÃ‚Â°ÃƒÆ’Ã¢â‚¬Â¡BÃƒâ€žÃ‚Â°R ZAMAN atlanmaz.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    "Context Loaded" ÃƒÆ’Ã‚Â¶zet bloÃƒâ€žÃ…Â¸u ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â proje adÃƒâ€žÃ‚Â±, stack, gÃƒÆ’Ã‚Â¼ncel gÃƒÆ’Ã‚Â¶rev, yÃƒÆ’Ã‚Â¼klenen bilgiler.
-->

# Project Context Primer Skill

## When to Trigger

**Always run first** when:
- Starting a new conversation about this project
- A subagent is spawned to work on a module
- Picking up work after a gap of more than a day
- Someone says "can you help with this project?" without any context

## Step-by-Step Process

### 1. Load the Knowledge Index

Read `.agent/knowledge/INDEX.md` first.

The INDEX.md file contains rows in this format:
```
| Date | Type | Topic (linked) | One-line summary |
```

- Scan all rows for entries relevant to today's task
- For each relevant row, follow the link and read the full `.agent/knowledge/<slug>.md` file
- Pay special attention to entries of type `decision` and `gotcha` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â these prevent the most costly mistakes
- Extract the slug from the link: `[topic](./auth/token-refresh.md)` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ slug is `auth/token-refresh`

**If INDEX.md does not exist**, output this exact warning and proceed:
```
ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Knowledge base not initialized (.agent/knowledge/INDEX.md missing).
This means no architectural decisions, conventions, or gotchas have been recorded yet.
Action: Use the `knowledge-base-update` skill at the end of this session to start building it.
```

### 2. Load the Project README

Read `README.md` (or `docs/README.md` if present).

Extract and internalize:
- What the project does (one sentence)
- Tech stack (language, framework, major libraries)
- How to run it locally
- How to run tests

### 3. Load Active Task Context

Check for these files in order and read whichever exist:

```
.agent/CURRENT_TASK.md       ÃƒÂ¢Ã¢â‚¬Â Ã‚Â What is being worked on right now
.agent/OPEN_QUESTIONS.md     ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Decisions not yet made
```

> **Note:** Architectural decisions and past decisions are stored in `.agent/knowledge/` (via `knowledge-base-update` skill),
> not in a separate DECISIONS_LOG. The INDEX.md (Step 1) is your decisions history.

If `.agent/CURRENT_TASK.md` exists, treat it as ground truth for your current mission.
If it does not exist, ask the user what today's task is before proceeding.

### 4. Scan Project Structure

Run a shallow directory listing (top 2 levels) to understand layout:

```
src/
  components/
  services/
  utils/
docs/
tests/
.agent/
```

Note any non-standard folders and check `.agent/knowledge/` for explanations.

### 5. Check for Active Conventions

Read `.agent/rules/` if it exists. These are hard constraints ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not suggestions.

Common rule files to look for:
- `code-style.md`
- `commit-messages.md`
- `test-coverage.md`
- `no-secrets.md`

### 6. Produce a Context Summary

Before doing any task work, output a brief summary in this format:

```
## Context Loaded

**Project:** <name> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <one-line description>
**Stack:** <languages, frameworks>
**Current Task:** <what we're doing today, from CURRENT_TASK.md or user>
**Relevant Knowledge Entries Loaded:** <list of slugs>
**Active Rules:** <list or "none found">
**Open Questions:** <any blockers or undecided things>
**Ready to proceed:** Yes / No (explain if No)
```

Only after producing this summary should you begin the actual task.

## Rules

- **Never skip this skill** on a new session. A 2-minute scan saves hours of rework.
- **Don't assume.** If the README contradicts a knowledge entry, flag it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't silently pick one.
- **Update CURRENT_TASK.md** at the end of each session with what was done and what's next.
- **If context is missing**, ask the user the minimum questions needed to fill the gaps before starting.

## Maintaining CURRENT_TASK.md

At the end of every session, update `.agent/CURRENT_TASK.md`:

```markdown
# Current Task

## What We're Building
<description>

## Status
<In Progress | Blocked | Review Needed | Done>

## Last Session Summary
<date> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <what was done>

## Next Steps
1. <next action>
2. <next action>

## Blockers
- <anything preventing progress>
```
