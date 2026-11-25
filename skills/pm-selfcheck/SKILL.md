---
name: pm-selfcheck
description: "Product-manager self-check skill: run the bundled scripts/selfcheck.sh to verify a super-PM skill's documentation and repo layout are complete and consistent before finishing work."
---

# PM Self-Check

Self-check gate for super-PM skills: verify docs and repo layout are complete before declaring work done.

## Run

```bash
bash "<skill-dir>/scripts/selfcheck.sh"
```

The script checks:

- Required docs exist (e.g. `SKILL.md` present, `README.md` where expected).
- Referenced scripts exist and are executable.
- No obvious TODO/placeholder markers remain.

## When to use

- Before finishing a PM task.
- After creating or editing a super-PM skill.
- When a review flags missing artifacts.

## Rule

- If the self-check fails, fix the reported issue — do not bypass the check.
