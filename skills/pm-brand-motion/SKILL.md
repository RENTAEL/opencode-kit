---
name: pm-brand-motion
description: "Product-manager workflow skill for brand motion content: runs the brand-motion shell pipeline (checks docs, prints preamble, generates brand-motion assets) and guides the PM through brand motion planning and execution."
---

# PM Brand Motion

Product-manager skill for planning and executing brand motion work.

## Preamble (run first)

```bash
# Print the preamble / check prerequisites
bash "<skill-dir>/scripts/pm-brand-motion.sh" --preamble
```

If the product docs folder does not exist, create it:

```bash
mkdir -p docs/02-产品设计
```

## Workflow

1. **Check brand motion docs** — look for `docs/02-产品设计/品牌动态.md`. If missing, create the file with the brand motion plan.
2. **Define the motion** — describe the brand's key motion (visual, narrative, or campaign motion) in concrete terms.
3. **Generate assets** — run the generator script for brand motion copy and visuals.
4. **Record decisions** — write decisions into the brand motion doc with dates.

## Output

- `docs/02-产品设计/品牌动态.md` — the living brand motion plan.
- Generated motion assets in the docs assets folder.

## Guardrails

- Do not overwrite existing brand motion decisions without approval.
- Keep the product's existing terminology.
