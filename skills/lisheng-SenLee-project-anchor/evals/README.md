# Lightweight skill eval cases

`prompts.csv` is a small regression set for the most important invocation boundaries.

It is intentionally not a full evaluation harness. Use it to check that the skill:

- triggers for repository governance, significant changes, long-running drift control, retry diagnosis, and completion reconciliation;
- does not trigger for trivial edits or unrelated explanation tasks.

Grow this file only when real usage exposes a meaningful false positive, false negative, or workflow regression.
