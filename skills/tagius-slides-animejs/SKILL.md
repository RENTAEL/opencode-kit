---
name: tagius-slides-animejs
description: "A meta-skill that turns raw input (free text, a topic + audience + length brief, an outline, or a `.pptx`) into a self-contained, browser-served, 16:9, full-screen slide deck animated with [anime.js v4](https://animejs.com/). The output is a `./presentation/` folder the user r..."
---
# slides-animejs

A meta-skill that turns raw input (free text, a topic + audience + length brief, an outline, or a `.pptx`) into a self-contained, browser-served, 16:9, full-screen slide deck animated with [anime.js v4](https://animejs.com/). The output is a `./presentation/` folder the user runs with `python3 run.py` and views in any browser. An overlay layer provides prev/next, fullscreen, a grid view, slide counter, progress bar, and speaker notes.

## What this skill does

It orchestrates other skills across an interactive, eleven-phase workflow:

1. **Bootstrap** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fetch the latest anime.js v4 reference (Context7 + `anime.js-best-practices`), initialize `CLAUDE.md` and `AGENTS.md` in the user's project.
2. **Intake** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â detect input (text, `.pptx`, outline, folder of materials) and capture audience / length / tone / academic flag / palette preference / meme allowance.
3. **Content brainstorm** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `scientific-brainstorming` (and, for academic decks, `scientific-slides` for structural guidance only) to draft slide-by-slide content into `presentation_plan.md`.
4. **Content Q&A** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â loop with the user on each slide until content is locked.
5. **Design brainstorm** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â call `ui-ux-pro-max` to pick palette, typography, and style; commit tokens to the plan and memory.
6. **Visual assets** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â audit `./visuals/`, generate/fetch SVGs, optionally produce sparse memes via `meme-factory`, and pause to let the user drop in their own assets.
7. **Static draft via slides-grab** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â synchronize with `slides-grab-plan` (style approval), then run `slides-grab-design` to author `slide-XX.html` files at the 720ÃƒÆ’Ã¢â‚¬â€405 px final-viewport canvas (slidegrab is the review/authoring stage; the viewport is the source of truth).
8. **Draft feedback** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â collect feedback, iterate on plan + slide HTML.
9. **Animation build** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run `scripts/build.py` to produce the `./presentation/` bundle (vendored `anime.esm.min.js`, design-token CSS, slide manifest, overlay, server).
10. **QA preview** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the run command; optional `playwright-cli` screenshot pass for layout regressions.
11. **Handoff** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â auto-run `slides-grab-export` to produce a PDF backup, print final instructions.

The workflow is interactive with explicit checkpoints. The skill never builds the final animated bundle without explicit user go-ahead. A skill re-invocation reads `CLAUDE.md` and offers to resume from the recorded phase.

## Locked decisions (binding)

These are user-confirmed and must not be relitigated:

1. Skill name: **`slides-animejs`**.
2. Output bundle path: **`./presentation/`** in the user's project, sibling of `presentation_plan.md` and `./visuals/`.
3. Memory files: write **both `CLAUDE.md` and `AGENTS.md`** in the user's project (mirrored content) for cross-agent compatibility.
4. anime.js: **always vendor locally** as `assets/anime.esm.min.js`. No CDN mode. Bundle is fully offline.
5. PDF backup: `slides-grab-export` runs **automatically** at phase 10 (handoff) and writes `./presentation/backup.pdf`.
6. PPTX back-conversion is **not supported** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â HTML + anime.js is the only output format.

## File layout produced in the user's project

The bundle lives in `./presentation/` (sibling of `presentation_plan.md`, `CLAUDE.md`/`AGENTS.md`, and `./visuals/`). The user runs `cd presentation && python3 run.py` and the browser opens at `http://localhost:8000`. Full tree, asset templates, and script inventory: see `references/skill-internals.md`.

## How to operate this skill

When invoked, the orchestrator:

1. Reads any pre-existing `CLAUDE.md` in the working directory. If a `## Current phase` block exists, summarize state in two lines and ask: "Continue from phase X, or jump to phase Y?".
2. Otherwise, enters **phase 0 (Bootstrap)** and follows `references/workflow.md` step-by-step.

Each phase has explicit **enter / do / ask / write / exit** rules ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `references/workflow.md` for the verbatim operational playbook.

### Hard rules

- 16:9 full viewport; the browser window IS the slide. No "card on a page" layout. Letterbox/pillarbox when the window aspect deviates.
- Animate only `transform` and `opacity`. Respect `prefers-reduced-motion`.
- Vendor anime.js locally; the bundle must run offline.
- Memes appear sparingly (max ~1 per 6 slides) and never on academic decks unless the user explicitly opts in.
- Pause at phase 5 to instruct the user to drop assets into `./visuals/`. Do not auto-fill silently.
- Never run phase 9 (final animation build) without explicit user go-ahead.
- Keep `CLAUDE.md` and `AGENTS.md` in sync (rewrite atomically on every phase transition).
- Run the phase-0 dependency preflight (`references/workflow.md`) first: block if a hard-required sub-skill or Context7 MCP is missing; warn-and-degrade for missing optional skills.

## Sub-skills orchestrated

Content: `scientific-brainstorming`, `scientific-slides` (academic only). Design: `ui-ux-pro-max`. Static authoring: `slides-grab-plan`, `slides-grab-design`, `slides-grab-export`. Animation: `anime.js-best-practices` (+ Context7). Intake: `pptx`. Extras: `meme-factory` (sparse), `playwright-cli` (optional QA).

Per-skill purpose + gotchas: `references/skill-internals.md`. Exact call contracts: `references/subskill-integration.md`. Verified spec deviations: `references/compatibility-notes.md`. Required-vs-optional preflight: `references/workflow.md` phase 0.

## References (load on demand)

| File | When to read |
|---|---|
| `references/workflow.md` | Always ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the operational playbook for phases 0ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“10. |
| `references/animejs-condensed.md` | Phase 0; refreshed via Context7. Cite during animation authoring. |
| `references/animejs-patterns.md` | Phases 6ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“9 when picking entrance / exit / transition recipes. |
| `references/slide-design-rules.md` | Phases 6ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“9 for 16:9 rules, type scale, contrast, reduced-motion handling. |
| `references/presentation-plan-schema.md` | Any time `presentation_plan.md` is created or edited. |
| `references/subskill-integration.md` | When orchestrating a specific sub-skill call. |
| `references/compatibility-notes.md` | Whenever a sub-skill's actual behavior diverges from the spec. |
| `references/skill-internals.md` | Bundle tree, asset templates, and `scripts/` inventory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when building/validating the bundle. |

## Quick-reference invariants

- Slide canvas: **720 px ÃƒÆ’Ã¢â‚¬â€ 405 px ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the final 16:9 viewport, and the source of truth.** `overlay.js` scales `.slide-frame` to the window via `min(innerW/720, innerH/405)` (uniform scale + letterbox). slides-grab authors at this same canvas only to ease the review step; if the two ever diverge, the viewport wins.
- Animations: WAAPI-first; `prefers-reduced-motion` short-circuits both the auto-animator and per-slide custom timelines.
- Per-slide custom timelines: `window.__slideTL[n] = (root) => ({ cancel })` (namespaced; `cancel` runs on slide exit to stop intervals/timelines and reset DOM).
- Server: stdlib `http.server` on port 8000 (override with `SLIDES_PORT`).
- Bundle is idempotent ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-running `scripts/build.py` overwrites the bundle without touching plan or drafts.

### Runtime model (full detail in `references/workflow.md` + `references/slide-design-rules.md`)

- **iframe isolation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each slide loads in its own `<iframe srcdoc>` with `<base href="/">`, so slide HTML may use `html`/`body`/`:root`/bare-element selectors freely without polluting other slides. The parent animates the iframe element (transform + opacity) for transitions and calls `__slideEntered(i)` / `__slideExited()` on the iframe window.
- **Step protocol** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a slide may set `window.__slideSteps = K` + `window.__slideStep = (n, dir) => void` for PowerPoint-style click-advance (parent steps 0..K within the slide before navigating).
- **Footer safe-zone** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a 26 px footer band sits at the bottom; every slide reserves ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 38 px bottom padding (or pads inner columns).
- **Idle animations** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every slide gets a subtle baseline idle; make 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 slides per deck "signature" with a topic-anchored idle that becomes a memory anchor.
- **SVG gotcha** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never apply CSS `transform: scale()` to a `<g transform="translate()">` (it replaces the attribute and collapses the group); animate inner shape coords (`cx`/`cy`/`x`/`y`) or use `transform-box: fill-box`.

## End-of-skill checklist before declaring success

- [ ] `presentation_plan.md` exists with the canonical schema.
- [ ] `CLAUDE.md` and `AGENTS.md` are in sync and reflect the current phase.
- [ ] `./visuals/` exists; every slide that references an asset resolves to a file.
- [ ] `./presentation/` builds, validates, and opens in the browser with all overlay features functional.
- [ ] `./presentation/backup.pdf` exists.
- [ ] Reduced-motion fallback verified by toggling the OS setting (or `prefers-reduced-motion: reduce` in DevTools).
- [ ] User has been handed the run command and the bundle path.
