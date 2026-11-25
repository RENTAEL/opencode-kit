---
name: ponytail-gain
description: "Use the Ponytail skill framework (external import by Dietrich Gebert, MIT) to gain or improve work across a codebase."
---
# Ponytail Gain

> External import of **Ponytail** by Dietrich Gebert and contributors, adapted from upstream v4.9.0 under MIT.

## Goal

Show Ponytail's published benchmark impact without pretending it measures the current repository.

## Output

Render this compact scoreboard:

```text
ponytail gain              upstream benchmark median Ãƒâ€šÃ‚Â· 5 tasks Ãƒâ€šÃ‚Â· 3 models

Lines of code   no-skill  100%
                ponytail    6ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“20%   down 80ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“94%
Cost            no-skill  100%
                ponytail   23ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“53%   down 47ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“77%
Speed           ponytail   3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6x faster
```

Then point repository-specific follow-up to `ponytail-debt` for counted deferrals and `ponytail-audit` for currently cuttable complexity.

## Rules

- These are upstream benchmark medians, not measurements of the current repository.
- Never invent a per-repo savings number: the unbuilt baseline does not exist.
- One-shot display only; do not change Ponytail mode or repository state.
