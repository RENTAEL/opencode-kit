---
name: rpi
description: "Parse the first word of the input as the keyword (`implement all [plan]` / `implement phase N [plan]` is the shape there). `plan`, `review`, and `implement` accept a path to a `.rpi/` document as context; `implement` with no path uses the most recent `.rpi/plans/*.md` (confirm..."
---
# rpi ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Research, Plan, Review, Implement

Parse the first word of the input as the keyword (`implement all [plan]` / `implement phase N [plan]` is the shape there). `plan`, `review`, and `implement` accept a path to a `.rpi/` document as context; `implement` with no path uses the most recent `.rpi/plans/*.md` (confirm with the user). Unknown or missing keyword ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ show the table and ask.

| Keyword | Reference |
|---------|-----------|
| `research <topic>` | [research](references/research.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â explore solutions with the user |
| `plan <description \| doc path>` | [plan](references/plan.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â TDD-structured implementation plan |
| `review <plan \| artifact>` | [review](references/review.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â findings list + verdict |
| `grill <topic>` | [grill](references/grill.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â relentless interview until fully aligned |
| `implement [all \| phase N] [plan path]` | [implement](references/implement.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â orchestrate subagents through a plan's checklist |
| `handoff [focus]` | [handoff](references/handoff.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â summarize session for another agent |
| `pickup [path]` | [pickup](references/pickup.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â resume from a handoff |
| `write` | [write](references/write.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â save output to `.rpi/` |
