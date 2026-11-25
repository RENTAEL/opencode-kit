---
name: handoff
description: "Compress session state to a compact document. The next session picks up exactly where this one left off."
---
# /supergraph:handoff

Compress session state to a compact document. The next session picks up exactly where this one left off.

Announce: "ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¦ /supergraph:handoff ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â compacting session state..."

## Steps

### 1. Capture current state

Gather live state ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not rely on memory:

```bash
git status --short
git log --oneline -10
```

Read active plan file (if any) from `docs/supergraph/plans/`.

### 2. Write handoff document

Save to `$TMPDIR/supergraph-handoff-<YYYY-MM-DD>.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â NOT in the workspace (avoids accidental commits).

```markdown
# Supergraph Handoff ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <YYYY-MM-DD>

## Goal
[One sentence: what we were trying to accomplish]

## Status
[In-progress / Blocked / Ready for next phase]

## Active Plan
Path: [docs/supergraph/plans/<slug>.md]
Current task: Task N ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [description]
Remaining tasks: [list with Status values]

## What Was Done
- [Completed task summaries ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â brief, no code]

## What Is Left
- [Remaining tasks, in order]
- [Any stuck tasks and why]

## Blockers / Open Questions
- [List ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or "none"]

## Key Files Changed
- [path] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [what changed, one line]

## Git State
Branch: [branch name]
Last commit: [hash] [message]
Uncommitted: [list or "none"]

## Environment Context
[Copy from plan's Environment Context section]

## Suggested Skills for Next Session
1. /supergraph:scan (always first)
2. /supergraph:execute plan <slug> (continue tasks)
   or /supergraph:tdd (if resuming single task)
3. /supergraph:fix ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /supergraph:verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /supergraph:review

## Notes
[Anything non-obvious a fresh agent needs to know]
```

Rules for content:
- Reference artifacts by **path or URL only** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never duplicate code or file content
- Keep the document under 150 lines
- No session-specific context (e.g., "as I said earlier") ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â self-contained

### 3. Report handoff location

```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ /supergraph:handoff complete
- Document: $TMPDIR/supergraph-handoff-<date>.md
- Status: [current status]
- Resume: /supergraph:scan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ read handoff doc ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /supergraph:execute plan <slug>
```

## Rules

- Never save to workspace ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always `$TMPDIR`
- References only, no content duplication
- Under 150 lines ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â force brevity
- Always include "Suggested Skills" so the next session has a clear entry point
