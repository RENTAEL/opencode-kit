# slides-animejs — internals reference

Bundle layout, sub-skill contracts (summary), scripts, and asset templates. Read when building/validating the bundle or orchestrating a specific sub-skill. `SKILL.md` links here to stay concise.

## File layout produced in the user's project

```
<project>/
├── presentation_plan.md          ← canonical slide-by-slide plan
├── CLAUDE.md                     ← memory: phase, tokens, anime.js refs (mirrored to AGENTS.md)
├── AGENTS.md                     ← mirror of CLAUDE.md
├── visuals/                      ← all media (created if absent)
│   ├── from-pptx/                ← auto-extracted (if PPTX intake)
│   ├── memes/                    ← auto-generated (sparse)
│   └── (user-curated assets)
└── presentation/                 ← runnable bundle (built by scripts/build.py)
    ├── index.html                ← entry point
    ├── README.md                 ← quick-start
    ├── run.py                    ← local server launcher (stdlib only)
    ├── backup.pdf                ← PDF backup from slides-grab-export
    ├── assets/
    │   ├── anime.esm.min.js      ← vendored (copied from skill assets/vendor/)
    │   ├── overlay.css
    │   ├── overlay.js
    │   ├── slides.css            ← 720×405 viewport + design tokens
    │   └── visuals/              ← mirrored ../visuals
    └── slides/
        ├── slide-01.html
        └── ...
```

The user runs `cd presentation && python3 run.py`; the browser opens at `http://localhost:8000`.

## When to use which sub-skill

| Sub-skill | Used for | Notes |
|---|---|---|
| `pptx` | Reading PPTX input (text, notes, media). | Chained with our `scripts/extract_pptx.py`. EMF/WMF flagged for replacement. |
| `scientific-brainstorming` | Per-slide content ideation. | Always constrained to the per-slide schema. |
| `scientific-slides` | Structural guidance for academic talks only. | Never invoke its Nano Banana Pro path. |
| `ui-ux-pro-max` | Palette, typography, style language. | Parse Markdown output via `-f markdown`. |
| `slides-grab-plan` | Style approval + outline structure. | We write `slide-outline.md` ourselves from `presentation_plan.md`. |
| `slides-grab-design` | Static slide HTML at the 720×405 viewport canvas. | `build.py` strips wrappers and injects `data-anim`. |
| `slides-grab-export` | Phase-10 PDF backup. | Auto-runs at handoff. |
| `anime.js-best-practices` | v4 idioms, WAAPI-first patterns, easing/stagger recipes. | Pair with Context7 docs. |
| `meme-factory` | Sparse comic relief. | Block when `Academic: yes` and user did not opt in. |
| `playwright-cli` | Optional QA screenshot pass. | Graceful degradation if not installed. |

See `subskill-integration.md` for exact contracts and `compatibility-notes.md` for verified deviations from the spec.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/build.py` | Build the `./presentation/` bundle from `presentation_plan.md` + slides-grab output. |
| `scripts/extract_pptx.py` | Wrap `pptx` skill output into our per-slide `{text, notes, media[]}` shape. |
| `scripts/fetch_animejs.py` | Download + vendor anime.js v4 ESM into `assets/vendor/`. |
| `scripts/validate_bundle.py` | Post-build validation (image srcs resolve, manifest sane, timelines named correctly). |

## Assets (templates copied into the user's `./presentation/`)

| Asset | Purpose |
|---|---|
| `assets/run.py` | Local server launcher (stdlib only). |
| `assets/index.html` | HTML shell with overlay markup (`{{TITLE}}`/`{{SLIDES_JSON}}` placeholders). |
| `assets/slides.css` | 720×405 viewport + design tokens. |
| `assets/overlay.css` | Overlay chrome styles (auto-hide, grid view, notes panel). |
| `assets/overlay.js` | iframe slide loader, transitions (WAAPI), keyboard, fullscreen, grid, notes, step protocol. |
| `assets/slide-fragment.template.html` | Per-slide skeleton with `data-anim`, step-protocol, footer, and idle conventions. |
| `assets/README.template.md` | User-facing quick-start in the bundle. |
| `assets/claude.md.template` | `CLAUDE.md` template for the user's project. |
| `assets/agents.md.template` | Mirror of `claude.md.template`. |
| `assets/vendor/anime.esm.min.js` | Vendored anime.js v4 ESM (+ `version.json`); `build.py` copies to bundle `assets/`. |
