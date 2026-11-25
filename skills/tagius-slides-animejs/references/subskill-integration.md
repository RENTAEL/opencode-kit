# Sub-skill Integration Contracts

Operational contracts for every skill `slides-animejs` orchestrates. For verified deviations from the spec, see `references/compatibility-notes.md`. This file is the day-to-day reference for "how do I invoke X and what do I do with the result?".

---

## `pptx`

- **Use for**: PPTX intake — text per slide, speaker notes, embedded media.
- **Invoke**: chain `python -m markitdown <file>.pptx` (for text) with the pptx skill's `scripts/office/unpack.py` (for OOXML media). Both are wrapped by our `scripts/extract_pptx.py`.
- **Pass in**: path to the source `.pptx`.
- **Expect out**: an `intake-manifest.json` with shape
  ```json
  {
    "title": "<from core.xml or filename>",
    "slides": [
      {"index": 1, "text": "...", "notes": "...",
       "media": ["visuals/from-pptx/slide-01/image1.png", ...]},
      ...
    ],
    "warnings": [...]
  }
  ```
- **Place media**: `./visuals/from-pptx/slide-NN/<basename>.<ext>`. EMF / WMF auto-converted to PNG via `soffice` if installed; otherwise the original is kept and a warning is emitted.
- **Compat risks**: see compatibility-notes §pptx.

### Example invocation

```sh
python3 ~/.claude/skills/slides-animejs/scripts/extract_pptx.py \
  <input>.pptx \
  --visuals-dir visuals \
  --manifest intake-manifest.json
```

---

## `scientific-brainstorming`

- **Use for**: Per-slide content ideation (phase 2).
- **Invoke**: `Skill(skill="scientific-brainstorming")` with a structured brief.
- **Pass in**: topic, audience, target slide count N, tone, any draft material.
- **Expect out**: a structured brainstorm where every slide block matches the `presentation_plan.md` schema (`Purpose`, `Key message`, `Content`, …).
- **Constrain the prompt** — open-ended brainstorming explodes scope. Always pin the output shape and the slide count.

### Example brief

> Brainstorm content for a `<length>`-slide talk on `<topic>` to `<audience>` (`<tone>` tone).
>
> Emit exactly `<N>` slide blocks. Each block must match the schema in `references/presentation-plan-schema.md` — at minimum: title, Purpose (one line), Key message (one sentence), Content (3–5 bullets), Visuals (suggested), Animation hints (entrance preference), Notes (1–3 sentence speaker notes).
>
> Stop after slide `<N>`. Do not propose alternative formats.

---

## `scientific-slides`

- **Use for**: Structural guidance for academic decks only (phase 2 when `Academic: yes`).
- **Invoke**: `Skill(skill="scientific-slides")` with an explicit "structural guidance only" constraint.
- **Pass in**: talk type (conference / seminar / defense / grant / journal club), target time, audience.
- **Expect out**: structural recommendations — story arc, time allocation, citation density, figure-caption norms.
- **Do NOT** let it run its Nano Banana Pro slide-generation path or its PPTX / Beamer output path. Our output is HTML + AnimeJS only.

### Example brief

> Provide structural guidance for a `<talk-type>`, `<duration>`-minute talk on `<topic>` to `<audience>`.
>
> **Do not generate slides.** Provide:
> 1. Recommended story arc (Hook / Context / Problem / Approach / Results / Implications / Closure) with time allocation.
> 2. Slide-type checklist for this talk type.
> 3. Citation density guidance (number of refs in intro / discussion).
>
> Reference the relevant sections of `references/presentation_structure.md` and `references/talk_types_guide.md` in your answer so I can cite them in `presentation_plan.md`.

---

## `ui-ux-pro-max`

- **Use for**: Palette, typography, style language (phase 4).
- **Invoke**: shell out to its Python CLI from the user's project directory (so any `--persist` output lands in `./design-system/`).
- **Pass in**: keyword query — topic + audience + tone + density preferences.
- **Expect out**: Markdown report containing pattern, style, palette (3–6 colors with roles), typography pair, effects (shadows/radius/blur), anti-patterns.

### Example invocation

```sh
python3 ~/.agents/skills/ui-ux-pro-max/scripts/search.py \
  "<topic> <audience> <tone>" \
  --design-system \
  -f markdown \
  -p "<plan.title>"
```

### Parsing into design tokens

Look for the palette section (typically a Markdown table with role → hex). Map roles to our tokens:

| ui-ux-pro-max role | `presentation_plan.md` token |
|---|---|
| Background / Surface | `bg`, `surface` |
| Text / Foreground | `fg` |
| Muted / Secondary text | `muted` |
| Primary / Accent | `accent` |
| Secondary / Accent 2 | `accent-2` |
| Display font | `font-display` |
| Body font | `font-body` |

Write the resolved values into the `## Design tokens` YAML block.

---

## `slides-grab-plan`

- **Use for**: Style approval gate + outline structure (phase 6 entry).
- **Invoke**: shell out to `slides-grab` directly — we do not let the planning skill run its full conversational flow because `presentation_plan.md` is already authoritative.

### Procedure

1. `slides-grab list-styles` — list bundled style IDs.
2. Pick a 2–3-style shortlist informed by `ui-ux-pro-max`'s style label.
3. Ask the user to approve one.
4. Write `./slides-draft/slide-outline.md` ourselves from `presentation_plan.md`. The meta section must include `style: <id>`. Each `## Slide N` block carries the key message and content notes.

### Outline meta block format

```markdown
---
style: <id>
title: <plan.title>
---

## Slide 1
- key message: <one sentence>
- content:
  - <bullet>
  - <bullet>
- visuals: <comma-separated paths>

## Slide 2
…
```

This matches what `slides-grab-design` reads.

---

## `slides-grab-design`

- **Use for**: Generating `slide-XX.html` files (phase 6).
- **Invoke**: `Skill(skill="slides-grab-design")` after the outline is in place.
- **Pass in**: pointer to `./slides-draft/slide-outline.md` and the constraint that entrance elements must be tagged with `data-anim` + `data-anim-from`.
- **Expect out**: `./slides-draft/slide-XX.html` files authored at the 720×405 final-viewport canvas. slides-grab is used here only for the draft/review stage — the 720×405 viewport (see `slides.css` / `overlay.js`) is the source of truth, and slidegrab authors at it to match, not the reverse.

### Constraint prompt

> Read `./slides-draft/slide-outline.md` (style `<id>` is already approved).
>
> Generate one slide HTML file per slide block. Save to `./slides-draft/slide-XX.html`.
>
> Per slide, you MUST:
> 1. Author at the 720 × 405 canvas — this is the final presentation viewport (slides-grab happens to share it).
> 2. Use only CSS variables from `assets/slides.css` for colors (`var(--bg)`, `var(--fg)`, `var(--accent)`, `var(--accent-2)`).
> 3. Add `data-anim` to elements that should animate on entrance.
> 4. Pick `data-anim-from="up|down|left|right|scale|fade"` per element (default: `up`).
> 5. Reference local assets as `./assets/<file>` (we mirror `./visuals/` into `./slides-draft/assets/` before invoking you).
> 6. Use Lucide icons by default. Avoid emoji as icons unless the deck tone explicitly calls for them.
>
> After generation, run `slides-grab validate --slides-dir ./slides-draft` and fix anything it flags.

### Wrapper handling

`slides-grab-design` may emit standalone HTML documents (`<!DOCTYPE>`, `<html>`, `<head>`, `<body>`). `scripts/build.py` strips wrappers and hoists `<head><style>` blocks. No action required from the orchestrator.

---

## `slides-grab-export`

- **Use for**: PDF backup (phase 10, locked decision §23.5).
- **Invoke**: shell out.

### Example

```sh
slides-grab pdf --slides-dir slides-draft --output presentation/backup.pdf
```

If `slides-grab` is not installed globally, the orchestrator falls back to a headless playwright-cli pass:

```sh
playwright-cli open http://127.0.0.1:8000/index.html
# ... navigate through all N slides ...
playwright-cli pdf --filename presentation/backup.pdf
```

PPTX and Figma export are experimental and **not used** by this skill (per locked decision §23.6).

---

## `anime.js-best-practices`

- **Use for**: v4 idioms, WAAPI-first patterns, easing / stagger recipes.
- **Invoke**: `Skill(skill="anime.js-best-practices")` during phase 0 (cache the snapshot) and phase 8 (during build, if reviewing a custom timeline).
- **Pass in**: a list of effects you plan to use.
- **Expect out**: code patterns and warnings.
- **Consumed by**: `references/animejs-condensed.md` and `references/animejs-patterns.md`.

---

## `meme-factory`

- **Use for**: Sparse comic relief (phase 5).
- **Invoke**: direct URL construction — no skill call needed.
- **Pass in**: template ID, top text, bottom text (URL-encoded with `_` for spaces).
- **Expect out**: a downloadable PNG / JPG / WEBP / GIF URL.

### URL form

```
https://api.memegen.link/images/<template>/<top>/<bottom>.png
```

Templates we use most: `drake`, `success`, `fine`, `fry`, `changemind`, `distracted`, `mordor`, `buzz`.

### Download + idempotency

```python
from pathlib import Path
import urllib.request

dst = Path(f"visuals/memes/slide-{n:02d}.png")
if not dst.exists():
    dst.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dst)
```

The orchestrator must hard-block invocation when `Academic: yes` and the user did not explicitly opt in.

---

## `playwright-cli`

- **Use for**: Optional phase-9 QA screenshot pass.
- **Invoke**: CLI commands; graceful no-op if absent.

### Example pass

```sh
playwright-cli open http://127.0.0.1:8000/index.html
playwright-cli resize 1920 1080
for i in $(seq 0 $((N-1))); do
  playwright-cli screenshot --filename=presentation/qa/slide-$(printf "%02d" $((i+1))).png
  playwright-cli press ArrowRight
done
playwright-cli close
```

Inspect the screenshots and surface layout / overflow issues. The orchestrator may consult an image-aware subagent for the visual diff if the deck is large.

---

## Context7 (anime.js docs)

- **Use for**: Pulling the *current* anime.js v4 reference at phase 0.
- **Invoke**: the two MCP tools `mcp__claude_ai_Context7__resolve-library-id` and `mcp__claude_ai_Context7__query-docs`.

### Example

```
resolve-library-id: anime.js
  → /<id>

query-docs: id=<id>, topic="animate, waapi, stagger, splitText, createTimeline, easings, spring, prefers-reduced-motion"
```

Cache the curated snapshot into `references/animejs-condensed.md` (the file we ship is already a hand-curated baseline — Context7 refresh only enriches it). If resolution fails, the shipped curated file is the source of truth.
