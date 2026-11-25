---
name: likec4-skill
description: "Produce **valid C4 diagrams in the LikeC4 DSL** from a verbal description or a codebase, and validate them with the CLI before delivery. References are split by concern ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read only what the task needs, **before** writing that part; do not guess syntax."
---
# LikeC4 C4 Diagrams

Produce **valid C4 diagrams in the LikeC4 DSL** from a verbal description or a
codebase, and validate them with the CLI before delivery. References are split
by concern ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read only what the task needs, **before** writing that part; do
not guess syntax.

Everything here is verified against the pinned LikeC4 version (see
`references/setup-and-validation.md` for the pin and upgrade procedure).

## Hard rules (only two)

1. **Validate before delivering.** Run `likec4 validate <dir>` on the project
   and deliver only on exit 0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bare directory, never `--file` (that reports on
   the filtered subset and exits 0 while the project is broken). Exit 0 is
   necessary, not sufficient: a `with { }` in a deployment view and a missed
   relationship `extend` both compile clean and render wrong. No CLI available
   at all ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ do the documented self-check and disclose it. Procedure and the
   full list: `references/setup-and-validation.md`.
2. **Never invent DSL syntax.** If unsure, open the relevant reference; if
   still unsure, consult https://likec4.dev/dsl/.

## Setup (first thing, once per session)

**The pinned version is the single line in `scripts/likec4-version`, next to this
file.** Read it, then build every command from it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the number is not written
anywhere else, so it can never go stale:

```bash
PIN="$(cat <this-skill-folder>/scripts/likec4-version)"
LC4="npx -y likec4@$PIN"
```

**Always that pin, never a locally installed `likec4`.** Every construct in this
skill is verified against it; other versions disagree silently ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they reject
syntax documented here, or exit 0 on models this one rejects. The pin works in
any environment with Node 22+ and network (first run downloads, then cached).
For projects the user keeps, recommend `npm install --save-dev likec4@$PIN`.
Details and the error catalogue: `references/setup-and-validation.md`.

## Task ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ what to read

| Task in front of you | Read |
| --- | --- |
| System Context / Landscape ("who uses it, what it talks to") | `references/levels/l1-context.md` |
| Containers ("what runs inside", tech choices) | `references/levels/l2-container.md` |
| Components (inside one container) | `references/levels/l3-component.md` |
| Code level ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â classes/interfaces of one component | `references/levels/l4-code.md` |
| Data flow / scenario / sequence (login, checkout, pipeline) | `references/levels/flows-dynamic.md` |
| A flow with a branch, retry, error path, or "as a sequence diagram" | `references/levels/flows-dynamic.md` (`alt`/`opt`/`loop`/`try`, `variant sequence`) |
| Infrastructure / "where does it run" | `references/levels/deployment.md` |
| Any cross-cutting DSL question (spec, model, FQN, extend) | `references/syntax-core.md` |
| Choosing what a view shows ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `include`/`exclude`, `where` filters on tags/metadata, `with` overrides | `references/predicates.md` |
| Colors, shapes, icons, legend, layout | `references/styling.md` |
| Given a repo / source code | `references/code-to-diagram.md` |
| Install, validate, format, errors, preview/export/CI, CLI flags | `references/setup-and-validation.md` |
| Config file, several models in one repo, `import` across projects | `references/project-config.md` |

## Scale the structure to the task

- **Small ask** (one system, quick context/container picture): start from
  `templates/minimal/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 3 files (`spec.c4`, `model.c4`, `views.c4`). Do not
  build a multi-folder project for this.
- **Real system** (2+ levels, several systems, deployment, flows): use the
  `templates/full/` layout ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â copy the files and rename content:

```
architecture/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ spec.c4                 # the ONLY specification block: all kinds
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ model/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ landscape.c4        # top-level systems + actors
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ <system>.c4         # one file per system, via extend <system> { ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ }
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ externals.c4        # externalSystem elements
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ deployment/prod.c4      # nodes + instanceOf (kinds stay in spec.c4)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ views/
    ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ context.c4          # Level 1 (view index)
    ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ <system>-views.c4   # Level 2/3 views with drill-down
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ dynamic-flows.c4    # dynamic + deployment views
```

Grow by adding files (new system ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new `model/<s>.c4`), keep model separate
from views, and keep the specification in one file. All `.c4` files under the
folder merge into one model automatically.

Templates use **built-in theme colors only** (in-scope = `primary`, external =
`gray` via the `externalSystem` kind, person = `indigo`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no custom colors,
no tags. This keeps the C4 convention and adapts to light/dark themes.

## Workflow

1. **Scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â identify the system, actors, externals; pick levels. Defaults:
   Context + Container; Component only for a non-trivial container; a dynamic
   view for each key scenario (recommended); deployment when infra matters;
   Level 4 only on explicit request or clear justification
   (`references/levels/l4-code.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â default substitute is a source link).
   Repo as input ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢
   `references/code-to-diagram.md`. Genuinely ambiguous scope ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask one
   question; otherwise proceed and state assumptions.
2. **Set up** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â copy the matching template, run the `LC4` line above.
3. **Model, then views** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â write model files, then views with drill-down
   (`view of`, `navigateTo`), reading the level file for each diagram you
   produce.
4. **Validate, then format** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `$LC4 validate <dir>`; fix `Line N:` errors
   (catalogue in `setup-and-validation.md`) until exit 0. Then `$LC4 format
   <dir>` and re-validate, so the files match the canonical style the user's
   own tooling produces.
5. **Deliver** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â show the file tree, the validation result, and how to view
   the diagrams (`$LC4 start <dir>`; export/CI options in
   `setup-and-validation.md`).

## Quality bar (check before delivery)

- [ ] `likec4 validate` exit 0 (or disclosed self-check), stderr clean.
- [ ] `likec4 format <dir> --check` exit 0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â files are in canonical form.
- [ ] Every element has a description; every container/component a
      `technology`; every relationship a directed label (what + how).
- [ ] Every view has a `title`; ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ ~20 elements per view ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â split crowded views.
- [ ] Levels connect: Context ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Container ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Component via `view of` /
      `navigateTo`.
- [ ] No silent failure: if the model uses a deployment view or an `extend` on a
      relationship, confirm the result (`$LC4 export json <dir> --skip-layout`)
      ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â both compile clean when wrong.
