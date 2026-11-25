# Sub-skill Compatibility Notes

This document captures verified contracts and known gaps between `slides-animejs` and every skill it orchestrates. It is the output of the M1 compatibility verification pass and the operational source of truth when the spec and reality disagree.

Each section lists:

- **Skill** — name and the path of the SKILL.md that was inspected.
- **Confirmed contracts** — what the skill does that matches our assumptions.
- **Deviations** — where the skill behaves differently from spec §4 / §19, and how `slides-animejs` works around it.
- **Action items** — concrete adjustments the orchestrator (or `build.py`) must perform.

---

## CRITICAL BUGS FIXED (2026-05-12) — must not regress

### Bug A: `.slide { opacity: 0 }` kills content on active slides

**Symptom:** All slides appear completely white / blank in the browser. Navigation may work but content is invisible.

**Root cause:** `slides.css` declares `.slide { opacity: 0 }` to hide inactive slide containers. `build.py` wraps each slide fragment in `<section class="slide" data-i="N">`. The slide HTML from slides-grab-design uses `<div class="slide">` as its root element. When injected as `host.innerHTML = html`, the nested `<div class="slide">` also matches `.slide { opacity: 0 }`. The outer `<section class="slide.is-active">` gets `opacity: 1` but the inner `<div class="slide">` stays at `opacity: 0` — invisible.

**Fix (applied to `assets/slides.css` and canonical skill asset):**
```css
/* WRONG — matches both outer container and inner slide HTML */
.slide { opacity: 0; }
.slide.is-active { opacity: 1; }

/* CORRECT — only the direct child of .slide-frame is the container */
.slide-frame > .slide { opacity: 0; pointer-events: none; ... }
.slide-frame > .slide.is-active { opacity: 1; pointer-events: auto; }
```

**Rule:** Never use `.slide { opacity: 0 }` without the `.slide-frame > ` parent prefix.

---

### Bug B: Frame dimensions 1280×720 mismatch with authoring canvas 720×405

**Symptom:** Slide content renders in the top-left ~56% of the frame. Large blank area on right and bottom. Content appears physically small relative to the browser window even in fullscreen.

**Root cause:** `slides.css` originally declared `--slide-w: 1280px; --slide-h: 720px` and `overlay.js` used `SLIDE_W = 1280; SLIDE_H = 720`. But slides-grab-design authors at `720px × 405px`. The `.slide-frame` was 1280×720 and the slide content (720×405) only filled 56% of it — the rest was empty background.

The "1280×720 at 1pt = 1.778px" rationale in the original TL;DR §1 was incorrect: that conversion only applies when authoring in CSS `pt` units. slides-grab-design authors in CSS `px` at 720×405px, not in `pt`.

**Fix (applied to both `assets/slides.css` and `assets/overlay.js`):**
```css
/* slides.css */
--slide-w: 720px;
--slide-h: 405px;
```
```js
// overlay.js
const SLIDE_W = 720;
const SLIDE_H = 405;
```

**Rule:** `--slide-w / --slide-h` must always match the actual authoring canvas used by slides-grab-design: **720px × 405px**. `overlay.js` `SLIDE_W / SLIDE_H` must match.

---

### Bug C: Draft slides had `[data-anim] { opacity: 0 }` — correct for build, wrong for draft viewer

**Symptom:** All slide content invisible in `slides-draft/viewer.html` — appears white. Only an issue in the draft review phase, not the final bundle.

**Root cause:** Draft slides authored with `[data-anim] { opacity: 0 }` to simulate entrance animations. The `slides-grab edit` editor and `viewer.html` do not run the anime.js entrance system, so all `[data-anim]` elements stay hidden.

**Fix:** Strip `[data-anim] { opacity: 0 }` from draft slide CSS. Keep `data-anim` attributes on elements (build.py uses them). The bundle's overlay.js adds opacity via WAAPI at entrance time.

**Post-build post-processing must NOT re-add `[data-anim] { opacity: 0 }` to bundle slides.**

---

## TL;DR — Top deviations to handle in `build.py` and the orchestrator

1. **Slide canvas: 720px × 405px (not 1280×720).** `slides-grab-design` produces slide HTML at **720px × 405px**. `slides.css` must declare `--slide-w: 720px; --slide-h: 405px` and `overlay.js` must use `SLIDE_W = 720; SLIDE_H = 405`. See Bug B above.
2. **slide-grab-design emits full HTML documents, not fragments.** `build.py` must strip `<html>`/`<head>`/`<body>` wrappers and lift the inner content into a `<section class="slide">`. Style and script tags inside `<head>` should be preserved (moved to the bundle's `index.html` head or kept inline at the top of each fragment).
3. **`slides-grab-plan` style-approval gate.** The skill refuses to write the outline before a style is approved. The orchestrator runs `slides-grab list-styles` (or honors the user's earlier `ui-ux-pro-max` selection), gets explicit approval, and writes `slide-outline.md` containing `style: <id>` in its meta. Our `presentation_plan.md` continues to exist; `slide-outline.md` is a derived view that lives in the slides-grab workspace.
4. **anime.js v4 prefers WAAPI.** `anime.js-best-practices` strongly recommends `waapi.animate(...)` for all CSS-transform animations. The spec's `assets/overlay.js` sketch uses `animate(...)` from the JS engine; the production overlay must use `waapi.animate(...)` for entrance/transition animations and reserve `animate(...)` for value tweens, complex timelines, or `onUpdate`-driven work. `createTimeline()` from the JS engine is still used for orchestrated per-slide timelines.
5. **`ui-ux-pro-max` does not return YAML/JSON tokens.** Output is an ASCII box or Markdown (`-f markdown`). We parse the Markdown report (or use `--persist`, which writes `design-system/MASTER.md`) and extract the palette + typography into the `## Design tokens` YAML block of `presentation_plan.md`.
6. **`scientific-slides` defaults to Nano Banana Pro image generation.** Its `references/presentation_structure.md`, `references/talk_types_guide.md`, and `references/slide_design_principles.md` are the only sections we consume. Never invoke `generate_slide_image.py` or `slides_to_pdf.py` from within our workflow.
7. **`pptx` does not expose a one-shot per-slide-with-media extraction.** `markitdown` returns flat Markdown; `scripts/office/unpack.py` returns OOXML. `scripts/extract_pptx.py` (ours) chains both — markdown for text/notes, unpacked `ppt/media/` for binary assets, and a slide-index pass that walks `ppt/slides/slide*.xml` to map text → notes → media references back to slide numbers.
8. **EMF / WMF media from PPTX.** Browsers cannot render these. `extract_pptx.py` converts via LibreOffice (`soffice --convert-to png`) when available, otherwise drops a placeholder and surfaces the issue to the user.
9. **slides-grab assets folder.** slides-grab expects `<slides-dir>/assets/` for local images and videos. We mirror project `./visuals/` into that folder during draft generation, and the bundler later re-mirrors it into `presentation/assets/visuals/`.
10. **Per-slide custom timelines.** Spec §11 declares `window.__slide_N_tl`. Risk: collisions on re-load. We namespace under `window.__slideTL[n] = (root) => {...}` and `overlay.js` invokes `window.__slideTL?.[i]?.(slideEl)`.

---

## pptx

- **SKILL.md**: `/Users/tagius/Documents/ai-folder/20260429-ai-slide-labsem/.agents/skills/pptx/SKILL.md`
- **Confirmed contracts**:
  - `python -m markitdown <file>.pptx` returns slide text and speaker notes as Markdown.
  - `python scripts/office/unpack.py <file>.pptx <out-dir>` produces an unpacked OOXML tree including `ppt/media/` (raster images, embedded media).
  - `python scripts/thumbnail.py <file>.pptx` returns thumbnail grids — handy for the intake summary we present to the user.
- **Deviations**:
  - No single command returns `{slides: [{text, notes, media[]}]}`. Our shim (`scripts/extract_pptx.py`) reconstructs that shape.
  - Media files are named opaquely (`image1.png`, `image2.emf`, …) — the shim resolves per-slide references by parsing `ppt/slides/_rels/slideN.xml.rels`.
  - LibreOffice (`soffice`) is required for EMF/WMF → PNG conversion. The shim detects its presence and degrades gracefully when missing.
- **Action items**:
  - `scripts/extract_pptx.py` writes `./visuals/from-pptx/slide-NN/<basename>.<ext>` and emits a JSON manifest the orchestrator reads.
  - Surface EMF/WMF placeholders to the user with the affected slide numbers and ask them to provide replacements.

---

## scientific-brainstorming

- **SKILL.md**: `/Users/tagius/.agents/skills/scientific-brainstorming/SKILL.md`
- **Confirmed contracts**:
  - Conversational ideation skill with five phases (context → divergent → connect → critique → synthesis).
  - Domain-agnostic enough to handle non-academic talks.
- **Deviations**:
  - Open-ended; will not naturally constrain itself to "per-slide content suggestions for a deck of N slides" unless we ask. The orchestrator's invocation prompt must include: target slide count, desired output shape (slide-1 → slide-N bullets), and the persona of the audience.
- **Action items**:
  - When invoking, hand the skill a structured brief: `topic`, `audience`, `length (N slides)`, `tone`, and the request to emit one bullet block per slide matching the `presentation_plan.md` schema.

---

## scientific-slides

- **SKILL.md**: `/Users/tagius/Documents/ai-folder/20260429-ai-slide-labsem/.agents/skills/scientific-slides/SKILL.md`
- **Confirmed contracts**:
  - Rich structural guidance for academic talk types (conference / seminar / defense / grant / journal club).
  - `references/presentation_structure.md`, `references/talk_types_guide.md`, `references/slide_design_principles.md`, and `references/data_visualization_slides.md` contain the structural rules we want.
  - Citation strategy guidance (use 8–15 papers, cite 3–5 intro, 3–5 discussion) is reusable verbatim.
- **Deviations**:
  - The skill's *default* execution path produces slides via Nano Banana Pro (`scripts/generate_slide_image.py`) and emits PDFs via `slides_to_pdf.py`. We must not invoke either.
  - The skill recommends PPTX / Beamer as alternatives — also not applicable to our HTML+AnimeJS output.
- **Action items**:
  - In the orchestrator's phase-2 invocation, explicitly limit the ask to: "Provide structural guidance for a <talk-type>, <length>-minute talk to <audience>. Do not generate slides." Cite the relevant reference files when summarizing into `presentation_plan.md`.

---

## ui-ux-pro-max

- **SKILL.md**: `/Users/tagius/.agents/skills/ui-ux-pro-max/SKILL.md`
- **Confirmed contracts**:
  - CLI: `python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system [-p "Project"] [-f markdown]`.
  - Returns: pattern, style label, palette (with role assignments), typography (header/body pair), effects (shadows/radius/blur), anti-patterns.
  - `--persist` writes `design-system/MASTER.md` and (with `--page`) `design-system/pages/<page>.md` in the *current working directory*.
- **Deviations**:
  - No YAML/JSON output. Markdown is the most structured option (`-f markdown`).
  - Stacks supported include `react-native`, `react`, `next.js`, etc., but not "HTML+CSS slide deck" specifically — we treat the output as CSS-token guidance regardless of stack.
- **Action items**:
  - Phase 4 invokes the CLI from the user's project directory (so `--persist` writes into `./design-system/`).
  - `scripts/build.py` reads `./design-system/MASTER.md` and converts the palette/typography into the CSS variables in `slides.css`. A small regex/Markdown-table parser is sufficient.
  - Fallback: if `--persist` is unwanted, the orchestrator parses the Markdown report inline and writes the tokens directly into `presentation_plan.md`'s `## Design tokens` YAML block.

---

## slides-grab-plan

- **SKILL.md**: `/Users/tagius/.claude/skills/slides-grab-plan/SKILL.md`
- **Confirmed contracts**:
  - Produces `slide-outline.md` with a `style: <id>` field in the meta section, and must get explicit user approval before moving to the design stage.
  - Style picker uses `slides-grab list-styles` and optionally `slides-grab preview-styles`.
- **Deviations**:
  - Does NOT silently consume an externally supplied outline. The flow expects a fresh, in-skill conversation that ends with explicit user approval.
  - Output filename is `slide-outline.md`, not `presentation_plan.md`. They are conceptually similar but the schemas differ (outline is sparser).
- **Action items**:
  - The orchestrator, when entering phase 6, runs `slides-grab list-styles`, picks 2–3 styles that match the `ui-ux-pro-max` recommendation, and asks the user to approve one (matching slides-grab's own style-approval contract).
  - We then write `slide-outline.md` ourselves from `presentation_plan.md` (mapping every `## Slide N — title` to an `## Slide N` block with the key message and content notes) and place the approved `style: <id>` in its meta section.
  - We do *not* run the planning skill in its conversational mode when our `presentation_plan.md` is already authoritative. We invoke only when the user wants to use slides-grab's planner as the primary content authoring tool — currently not the default path.

---

## slides-grab-design

- **SKILL.md**: `/Users/tagius/.claude/skills/slides-grab-design/SKILL.md`
- **Confirmed contracts**:
  - Produces `<slides-dir>/slide-XX.html` files and a `viewer.html` for review.
  - Slide canvas is **720px × 405px** (matches the final viewport; see Bug B).
  - Local assets go under `<slides-dir>/assets/` and are referenced as `./assets/<file>`.
  - Body type minimum 14pt, hard floor 10pt.
  - Uses Lucide icons by default. Validation: `slides-grab validate --slides-dir <path>`.
  - Generates bespoke imagery via `slides-grab image --prompt "..."`, complex diagrams via `slides-grab tldraw`.
- **Deviations** (significant):
  - **Canvas size**: spec §9 says 1920×1080. The **source of truth is the final 720×405 px viewport** (`slides.css` declares `--slide-w: 720px; --slide-h: 405px;`, overlay.js uses `SLIDE_W=720, SLIDE_H=405`). slides-grab-design authors at this same 720×405 canvas to match — it is a review/authoring convenience, not the authority. See Bug B for the history of the earlier 1280×720 mismatch.
  - **Fragment vs document**: slides-grab emits standalone slide HTML files that may include their own `<html>`, `<head>`, and `<style>` blocks. `build.py` strips wrappers and hoists inline `<style>`; each slide is then loaded in its own `<iframe srcdoc>` (full CSS isolation), so global selectors in the fragment are safe.
  - **No `data-anim` injection by default**: slides-grab won't add animation hints. `build.py` runs a post-processor that adds `data-anim` to top-level elements (title, hero image, bullet items) using simple selectors, OR the orchestrator instructs slides-grab during generation to tag them — both paths are supported.
  - **Image generation**: slides-grab's bundled image generators (`god-tibo-imagen`, `codex`, `nano-banana`) require external creds. We treat them as optional. Our visuals workflow (phase 5) primarily uses user-supplied assets from `./visuals/`, meme-factory output, and inline SVG; slides-grab image generation is an opt-in fallback.
- **Action items**:
  - 720×405 px is the canvas in `slides.css` (scale by `min(vw / 720, vh / 405)`).
  - `scripts/build.py` implements the wrapper-stripping pass and the `data-anim` auto-tagger.
  - Mirror `./visuals/` into `<slides-dir>/assets/` before invoking slides-grab-design.

---

## slides-grab-export

- **SKILL.md**: `/Users/tagius/.claude/skills/slides-grab-export/SKILL.md`
- **Confirmed contracts**:
  - PDF export is fully supported and headlessly callable: `slides-grab pdf --slides-dir <path> --output <name>.pdf`.
  - PNG export: `slides-grab png --slides-dir <path> --output-dir <path>/out-png --resolution 2160p` (supports `--slide-mode card-news`).
  - PPTX export is marked experimental / unstable.
- **Deviations**:
  - None for our needs. PDF is the canonical phase-10 backup path.
- **Action items**:
  - Phase 10's `handoff` step invokes `slides-grab pdf` and saves the result to `./presentation/backup.pdf` (per locked decision §23.5).
  - We do not call PPTX export — locked decision §23.6 forbids PPTX as a deliverable.

---

## anime.js-best-practices

- **SKILL.md**: `/Users/tagius/.agents/skills/anime.js-best-practices/SKILL.md`
- **Confirmed contracts**:
  - Anime.js v4 confirmed (`version: 1.3.0` of the skill; covers v4 API surface in depth).
  - Exports: `animate`, `waapi.animate`, `createTimeline`, `stagger`, `splitText`, `utils`, `spring`, `cubicBezier`, `svg`, draggable, scroll observer.
  - Bundle: full module `animejs` (~10 KB), WAAPI subpath `animejs/waapi` (~3 KB).
  - Mandates `prefers-reduced-motion` handling and a planning workflow.
- **Deviations**:
  - Strong recommendation: use `waapi.animate(...)` for CSS-transform animations rather than `animate(...)`. Spec §10's overlay sketch uses `animate(...)` — production overlay rewrites to `waapi.animate` for entrance/transition and uses `animate(...)` only where required (value tweens, callbacks-heavy work).
  - WAAPI uses milliseconds and `linear` default easing — easy to misread spec timings as seconds. Internal docs and code must consistently use milliseconds.
- **Action items**:
  - `references/animejs-condensed.md` and `references/animejs-patterns.md` emphasize the WAAPI-first pattern.
  - `assets/overlay.js` uses `waapi.animate` for slide transitions and entrance staggers; `createTimeline` from the JS engine is used for orchestrated per-slide timelines.
  - `references/slide-design-rules.md` includes a `prefers-reduced-motion` rule that short-circuits the `data-anim` auto-runner and per-slide custom timelines.

---

## Context7 (anime.js library docs)

- **Tools**: `mcp__claude_ai_Context7__resolve-library-id`, `mcp__claude_ai_Context7__query-docs`.
- **Confirmed contracts**:
  - Tools are present in this environment (verified at session start).
  - Will be probed at bootstrap (phase 0): resolve `anime.js` → fetch API reference snapshot → cache into `references/animejs-condensed.md` (regenerated on bootstrap).
- **Deviations**:
  - Cannot pre-verify the library entry exists without invoking the tool. If resolution fails at runtime, we fall back to `anime.js-best-practices` plus the cached snapshot.
- **Action items**:
  - `scripts/fetch_animejs.py` performs both the package vendor (download the v4 ESM bundle) and the Context7 docs cache (if reachable). The cache is informational; the source of truth at runtime is the vendored `anime.esm.min.js`.

---

## meme-factory

- **SKILL.md**: `/Users/tagius/.agents/skills/meme-factory/SKILL.md`
- **Confirmed contracts**:
  - URL pattern: `https://api.memegen.link/images/{template}/{top}/{bottom}.png`.
  - Returns a downloadable raster (PNG / JPG / WEBP / GIF). No API key.
  - Templates: `buzz`, `drake`, `success`, `fine`, `fry`, `changemind`, `distracted`, `mordor`, …
- **Deviations**:
  - None for our needs. URL is canonical.
- **Action items**:
  - When phase 5 elects to add a meme, the orchestrator builds the URL, downloads with `curl -fsSL` (or Python `urllib.request`) to `./visuals/memes/slide-NN.png`, and records the file path in `presentation_plan.md`.
  - Cache check: if `./visuals/memes/slide-NN.png` exists, skip regeneration (idempotency rule).
  - Hard block: `meme-factory` is never invoked when `Academic: yes` and `Memes allowed: no` in the plan front matter.

---

## playwright-cli (optional QA)

- **SKILL.md**: `/Users/tagius/.agents/skills/playwright-cli/SKILL.md`
- **Confirmed contracts**:
  - Command-line tool available as `playwright-cli` or `npx playwright-cli`.
  - Can navigate (`goto`), screenshot (`screenshot --filename=...`), and resize (`resize 1920 1080`).
- **Deviations**:
  - Optional dependency; if absent, phase 9 still works — the user simply opens the deck in their browser.
- **Action items**:
  - Phase 9's optional QA pass shells `playwright-cli` per slide URL (`http://127.0.0.1:8000/index.html#N`) and saves `presentation/qa/slide-NN.png`. The orchestrator inspects the screenshots, surfaces layout issues to the user, and links back into phase 7 if anything is broken.

---

## Verification status (M1 todo mirror)

- [x] `pptx` — markdown + unpack chain confirmed; EMF/WMF handling documented.
- [x] `slides-grab-plan` — style-approval gate documented; we write outline ourselves.
- [x] `slides-grab-design` — 720×405px canvas, wrapper-strip required, `data-anim` injection documented.
- [x] `slides-grab-export` — PDF/PNG callable headlessly.
- [x] `ui-ux-pro-max` — markdown output; parse into design tokens.
- [x] `anime.js-best-practices` — v4 confirmed; WAAPI-first noted.
- [x] `scientific-brainstorming` — constrain prompt to per-slide schema.
- [x] `scientific-slides` — structural-only consumption; never invoke Nano Banana Pro.
- [x] `meme-factory` — URL fetch confirmed.
- [x] Context7 — probe at runtime; fallback to best-practices skill.
- [x] `playwright-cli` — optional; available in this environment.

All gaps have documented workarounds. No blocking incompatibility found.
