---
name: pm-iteration
description: "Product-manager workflow skill for iteration tracking: drives the PM iteration loop (update iteration doc, check progress, report status) using the project's docs/03-迭代记录 folder and iteration script."
---

# PM Iteration

Product-manager skill for running and tracking product iterations.

## Preamble

```bash
# Run the iteration preamble and status check
bash "<skill-dir>/scripts/pm-iteration.sh" --preamble
```

## Workflow

1. **Locate the iteration record** — `docs/03-迭代记录/迭代记录.md` (create if missing).
2. **Update status** — reflect current iteration progress (done / in progress / blocked).
3. **Report** — summarize per-iteration achievements, risks, and next steps.
4. **Close or continue** — if the iteration is complete, mark it closed and open the next one.

## Conventions

- Keep one section per iteration, dated.
- Use the same status vocabulary as the project's other PM docs.
- Never invent metrics that are not in the docs.
