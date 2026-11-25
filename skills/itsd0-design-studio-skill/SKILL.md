---
name: itsd0-design-studio-skill
description: "Turn a brief into **single-file HTML artifacts** driven by a **DESIGN.md brand contract**, verified by four gates, delivered as real handoff-ready files."
---
# Design Studio

Turn a brief into **single-file HTML artifacts** driven by a **DESIGN.md brand contract**, verified by four gates, delivered as real handoff-ready files.

## Quick start

```bash
# brand ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ contract (skip when a DESIGN.md already exists)
python3 scripts/extract.py https://brand.example --out .

# no brand? three candidates, rendered side by side, one image, one decision
python3 scripts/directions.py --brief "AI infrastructure for autonomous agents" --sheet sheet.png

# build from the seed, then run all four gates
python3 scripts/lint.py index.html && python3 scripts/verify.py index.html
python3 scripts/contract.py index.html && python3 scripts/score.py index.html
```

## Workflow checklist

- [ ] **0 Ãƒâ€šÃ‚Â· Preflight** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find `DESIGN.md`, read the artifact contract
- [ ] **1 Ãƒâ€šÃ‚Â· Brief** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â product, audience, kind, must-keep facts, three experience dials
- [ ] **2 Ãƒâ€šÃ‚Â· Direction** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â extract the brand, or compare three candidates and let the user pick
- [ ] **3 Ãƒâ€šÃ‚Â· Plan** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â name the sections/slides before writing HTML
- [ ] **4 Ãƒâ€šÃ‚Â· Build** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â start from the seed, paste patterns, customize every schematic
- [ ] **5 Ãƒâ€šÃ‚Â· Gate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â lint ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ contract ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ score; fix until clean
- [ ] **6 Ãƒâ€šÃ‚Â· Deliver** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one-line summary, then offer `handoff`
- [ ] **7 Ãƒâ€šÃ‚Â· Review** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when asked to audit an artifact

## Workflow

### 0 Ãƒâ€šÃ‚Â· Preflight

- Read `references/artifact-contract.md` (always) and `references/deck-contract.md` when the artifact is a deck.
- Look for `DESIGN.md` (and `tokens.css`) in the working directory. If found, read both before writing anything.

### 1 Ãƒâ€šÃ‚Â· Brief

Capture: product, audience, goal, artifact kind (landing / prototype / dashboard / deck / mobile / agent), must-keep facts (real numbers, names, copy) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **and the three experience dials**: density (airy Ãƒâ€šÃ‚Â· regular Ãƒâ€šÃ‚Â· compact), expressiveness (restrained Ãƒâ€šÃ‚Â· assured Ãƒâ€šÃ‚Â· bold), motion (still Ãƒâ€šÃ‚Â· standard Ãƒâ€šÃ‚Â· lively). Ask **only** for missing essentials, in one round. Facts you cannot know become labeled placeholders (`[REPLACE Ãƒâ€šÃ‚Â· label]`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never invent statistics or quotes. For `agent` artifacts also capture: the agent's real domain, its real tool names (e.g. `SENTRY_LIST_ISSUES`), and which actions are destructive (need approval).

### 2 Ãƒâ€šÃ‚Â· Direction & design system

**Never pick a direction blind, and never let one become the house style.**

- **Brand exists** (URL, screenshot, brand assets): `python3 scripts/extract.py <url|screenshot>` writes `DESIGN.md` + `tokens.css` from the *rendered* page. Review what it measured and correct the roles by hand ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the extractor infers, it does not decide.
- **No brand**: derive three candidates and let the user pick.

  ```bash
  python3 scripts/directions.py --brief "AI infrastructure for autonomous agents" --sheet sheet.png
  ```

  It prints three candidates (palette, type, density, and *why* each fits) and renders them side by side into `sheet.png`. Show the sheet, ask which one, then bind that candidate's tokens **verbatim**.
- **A reference grammar fits** (eighteen offline entries in `references/library/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `design-studio library` lists them): copy its `:root` block and component recipes instead of inventing a system.
- Bind palette and fonts **verbatim** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never improvise hex values from a direction's label.

### 3 Ãƒâ€šÃ‚Â· Plan before pixels

- **Landing / prototype**: 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6 sections with flagship rhythm (`hero-stage` with `.app-window` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `bento-telemetry` hairline schematics ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `bento-architecture` *or* `indexed-showcase` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `compare` *or* `pricing` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `cta`). State the section list before writing HTML.
- **Deck**: slide count by format (5ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“10 min ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  6; 15 min ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  8ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“10; 20ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“30 min ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  12ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“18). No 3+ same-theme slides in a row; 8+ slides need one `hero dark` and one `hero light`.
- **Dashboard**: classify the monitored domain, then define specific KPI names and plausible values ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no "Metric A / Metric B".
- **Agent**: pick one screen type ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `thread`, `run-detail`, `approval`, `activity` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and define the real tool names and which actions are destructive.
- **Mobile**: one screen = one job. Pick the screen and the single decision it supports.

### 4 Ãƒâ€šÃ‚Â· Build

- Start from the seed for the kind: `assets/prototype-seed.html`, `dashboard-seed.html`, `agent-seed.html`, `mobile-seed.html`, `deck-seed.html` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â copy it to `index.html`.
- Paste from `assets/ui-patterns.html` (states), `agent-ux-patterns.html` (tool call ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ eval receipt) and `section-skeletons.html` (11 page sections). Customize every `.bento-visual` SVG, `.app-window` pane and `.dag-grid` to the brief's exact domain ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â zero filler.
- Imagery: fetch the real asset, copy it in, set intrinsic `width`/`height`. Otherwise keep a labeled placeholder and disclose it. Never hotlink.
- Motion per `references/motion.md`; states per `references/ux-flows.md`; charts per `references/data-viz.md`.
- Keep the seeds' 920px breakpoint and, for decks, the navigation script intact.

### 5 Ãƒâ€šÃ‚Â· Gate, then fix

1. `python3 scripts/lint.py index.html` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix every P0; fix any contrast `ÃƒÂ¢Ã…â€œÃ¢â‚¬â€`.
2. `python3 scripts/verify.py index.html` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â renders at 390/768/1440. Fix every P0 (`overflow-x`, `overflow-element`, `text-clipped`, `contrast-text`, `runtime-error`, `min-content-overflow`) and the P1 tap targets, tight fits and focus styles.
3. `python3 scripts/contract.py index.html` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â token drift against `DESIGN.md` is a P0. Skip only when the project has no contract.
4. `python3 scripts/score.py index.html` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix any failed check; 2/4 is the floor on distance from the default.
5. Walk the P0 checklist in `references/quality-gates.md`, then the judgement steps in `references/critique.md`.
6. Screenshot: `python3 scripts/verify.py --screenshot .shots index.html`, then apply the soul test to the image.

### 6 Ãƒâ€šÃ‚Â· Deliver & iterate

- One short summary: file name plus what it contains. Nothing after.
- Offer `python3 scripts/handoff.py index.html` when the work continues in a framework.
- Revisions: surgical edits to the same file, never a wholesale regeneration. Re-run the gates.

### 7 Ãƒâ€šÃ‚Â· Review mode (audit requests)

1. `lint.py` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `verify.py` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `contract.py` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `score.py`, each with `--json` for the report.
2. `python3 scripts/review.py index.html --out review.md` produces the publishable review document (findings table, scorecard, screenshots).
3. Walk `references/critique.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â claim, hierarchy, accent, surface, evidence, states, rhythm, distance, handoff.
4. Report findings as a table ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â severity Ãƒâ€šÃ‚Â· id Ãƒâ€šÃ‚Â· where Ãƒâ€šÃ‚Â· fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â P0 first.
5. Fix surgically, re-run the gates, show the before/after contrast line when it changed.

## Gotchas

- **A prose table cannot shrink below its longest word.** `width: 100%` does not save it. Put every table in `.tablewrap { overflow-x: auto; min-width: 0 }` and give the table `min-width: 520px` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â otherwise the page scrolls sideways on the platform whose font fallback is wider.
- **`1fr` means `minmax(auto, 1fr)`.** A grid child with a long string stops the track shrinking. Use `minmax(0, 1fr)` and `min-width: 0` on the children.
- **Headless Chrome clamps its window to ~500px.** `--window-size=390` does not give you a 390px layout. Render inside an iframe of the exact width ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that is what `verify.py` does.
- **`color-mix()` serialises as `color(srgb ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦)`**, and `oklch()` stays `oklch()`. A contrast checker that only parses `rgb()` silently skips every mixed token.
- **`var()` inside a shorthand hides its longhands.** `outline: 2px solid var(--accent)` reads as `outline: ""` and `outlineStyle: ""`. Parse the declaration text, not the computed property.
- **The accent is inherited.** Counting `color === accent` counts every descendant. Count elements that *own* the text or fill with it.
- **A flex item's `min-width: auto` blocks shrinking.** A scroll container inside a flex row needs `min-width: 0`, not just `overflow: auto`.
- **A direction everyone uses becomes the new default.** Cream + teal + serif is the current one. `score.py` measures the distance ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 2/4 is the floor, 3/4 is good.
- **`scrollIntoView()` breaks embeds.** It scrolls the parent document, not the artifact. Use `container.scrollTo()`.
- **Placeholders are the point of a template.** Only a deliverable fails the placeholder check; `data-artifact="seed"` says which is which.

## Non-negotiables

1. **One self-contained file.** `index.html` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one `<style>` block, no external CSS/JS, inline SVG for charts, system-first fonts. Real images are copied in and referenced relatively.
2. **One token block.** Standard names in a single `:root` (`--bg`, `--surface`, `--surface-2`, `--fg`, `--muted`, `--border`, `--accent`, `--accent-on`, `--font-display`, `--font-body`, `--font-mono`). No raw hex outside it; derive tones with `color-mix()`.
3. **DESIGN.md is the brand contract.** Read it before writing HTML. Never invent tokens ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use the closest existing token.
4. **No AI-slop, and a product stage when the brand allows it.** No purple/indigo defaults, no trust gradients, no emoji icons, no left-accent cards, no invented metrics. No bare text-only hero, no three-icon feature row ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every landing page carries a hero product stage (`.app-window`/`.term`/live schematic) and schematic bento or indexed features. An existing `DESIGN.md` always wins; see `references/artifact-contract.md`.
5. **Accent budget: at most 2 visible uses per screen.** Links demote to `--fg` when a CTA shares the screen. Bind `--accent-on` so primary buttons keep WCAG contrast.
6. **Anchor every section.** `data-design-id="kebab-slug"` on each top-level `<section>`; decks use `data-screen-label="01 Cover"`.
7. **No `scrollIntoView()`** anywhere.
8. **Deliver with a one-line summary** naming the file. Never paste the full HTML into chat.

## Load what you need, when you need it

| Read this | When |
|---|---|
| `references/artifact-contract.md` | Always, before the first line of HTML |
| `references/quality-gates.md` | Before delivery ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the P0/P1 checklist |
| `references/deck-contract.md` | The artifact is a deck |
| `references/agent-ux.md` | The artifact is an agent screen |
| `references/critique.md` | Reviewing, or judging an artifact that passes the gates |
| `references/copy.md` | Writing errors, empty states, CTAs or onboarding copy |
| `references/ux-flows.md` | Any stateful surface needs loading/empty/error states |
| `references/data-viz.md` | The artifact contains a chart or KPI row |
| `references/ui-patterns.md` | A component's states are unclear |
| `references/motion.md` | Anything animates |
| `references/design-md.md` | Authoring or repairing a `DESIGN.md` |
| `references/directions.md` | You need the eight curated directions in detail |
| `references/library/<id>.md` | You are binding that grammar ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read one, not all |
| `assets/design-md.template.md` | Starting a contract from scratch |
| `assets/section-skeletons.html` | Planning the section list |
| `assets/ui-patterns.html` Ãƒâ€šÃ‚Â· `assets/agent-ux-patterns.html` | Pasting ready component states |
| `tests/run_tests.py` Ãƒâ€šÃ‚Â· `tests/compose.py` | Changing the gates or the seeds |

Tools: `lint.py` (source), `verify.py` (render), `contract.py` (brand), `score.py` (craft), `extract.py` (brand ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ contract), `directions.py` (candidates), `handoff.py` (framework spec), `review.py` (review document), `benchmark.py` (published comparison), `ds.py` (all of them, `design-studio <command>`), `mcp_server.py` (the same eight tools over MCP). `pngread.py` is the internal PNG reader used by `extract.py` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not run by hand.

## When not to use

- **React / Vue / Next.js / Svelte component work inside an existing app.** This makes single-file HTML artifacts, not framework components. Finish the artifact, then `design-studio handoff` to produce the spec another agent implements.
- **Multi-page apps with routing or backend logic** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â keep this as the design step, then hand off.
- **Formal accessibility certification** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the gates are a professional baseline, not an audit.
