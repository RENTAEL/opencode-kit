# `presentation_plan.md` Schema

The canonical slide-by-slide plan. Parsed by `scripts/build.py`; edited by the orchestrator across phases 1–7; mirrored design tokens land in `CLAUDE.md` and `AGENTS.md`.

---

## Full template

```markdown
# Presentation: <title>

- Author: <name>
- Audience: <technical | general | mixed | academic | sales>
- Length: <N slides | M minutes>
- Tone: <formal | playful | mixed>
- Academic: <yes | no>
- Memes allowed: <yes | no>
- Palette: <palette name from ui-ux-pro-max>
- Style: <bento | minimal | brutalism | glass | …>
- Fonts: <display / body>

## Design tokens
```yaml
bg: "#0b0c10"
fg: "#f5f5f7"
surface: "#16181f"
muted: "#a8acb8"
accent: "#7c5cff"
accent-2: "#ffd166"
font-display: "Inter"
font-body: "Inter"
```

## Slides

### Slide 1 — <slide title>
- **Purpose**: <one-line statement of why this slide exists>
- **Key message**: <one-sentence claim the audience should leave with>
- **Content**:
  - bullet, paragraph description, or diagram sketch
  - second bullet
- **Visuals**: `visuals/foo.svg`, `visuals/from-pptx/slide-01/img3.png`
- **Animation hints**: `entrance: fade-up`, `transition-in: slide-right`
- **Meme**: none | `visuals/memes/slide-01.png` (template: drake)
- **Notes**: speaker notes — paragraph or bullets, will appear in the on-screen notes panel
- **Status**: draft | reviewed | finalized

### Slide 2 — <title>
…
```

---

## Field-by-field reference

### Front matter

| Field | Required | Used by |
|---|---|---|
| `# Presentation:` | yes | sets `<title>` in `index.html` and `README.md`. |
| `- Author:` | recommended | shown on the title slide if the slide HTML references it. |
| `- Audience:` | yes (phase 1 gate) | informs `scientific-brainstorming` brief; gates `scientific-slides`. |
| `- Length:` | yes | informs slide count, time-allocation guidance. |
| `- Tone:` | recommended | informs `ui-ux-pro-max` style, gates `meme-factory`. |
| `- Academic:` | yes | gates `scientific-slides`; defaults memes to `no` unless user opts in. |
| `- Memes allowed:` | yes (defaults `no`) | hard gate on `meme-factory` invocation. |
| `- Palette:` | filled in phase 4 | name only; the hex values live in `## Design tokens`. |
| `- Style:` | filled in phase 4 | also mirrored to `style: <id>` in `slides-draft/slide-outline.md`. |
| `- Fonts:` | filled in phase 4 | recorded for resume; the actual font families live in `## Design tokens`. |

### `## Design tokens`

YAML block. Keys map directly to CSS variable names: `<key>` → `--<key>` in `slides.css`. Kebab-case is preserved (`accent-2` → `--accent-2`).

Recommended (used by `slides.css` and overlay):
- `bg`, `fg`, `surface`, `muted`, `accent`, `accent-2`
- `font-display`, `font-body`

Any extra keys are appended to `:root { ... }` automatically — useful for one-off accent tokens or per-deck custom variables.

### `### Slide N — title`

`N` must be 1-based and contiguous (1, 2, 3, …). The `—` (em dash) separator is preferred but `-` and `--` are accepted.

| Field | Type | Notes |
|---|---|---|
| **Purpose** | string | One line. Used by orchestrator only — not rendered in the slide. |
| **Key message** | string | One sentence. Used by orchestrator only. |
| **Content** | nested bullets | Author content. The slide HTML carries the actual rendered text; this field is the spec from which the draft is generated in phase 6. |
| **Visuals** | comma- or backtick-separated paths | Each path is project-relative (e.g. `visuals/foo.svg`). Validated by `validate_bundle.py`. |
| **Animation hints** | comma-separated `key: value` (backticks optional) | Parsed by `scripts/build.py` into a dict. Recognized keys: `entrance` (one of `fade-up`, `fade-down`, `slide-left`, `slide-right`, `scale-in`, `reveal`, `fade`), `transition-in`, `stagger` (ms). |
| **Meme** | `none` or `<path>` | When non-`none`, the file must exist (typically `visuals/memes/slide-NN.png`). |
| **Notes** | free text | Rendered in the on-screen speaker-notes panel (toggle with `S`). Plain text; markdown not parsed. |
| **Status** | `draft` \| `reviewed` \| `finalized` | Drives `Status: draft` data attributes in the manifest. `validate_bundle.py` does not block on this; phase 9 QA surfaces drafts to the user. |

---

## Parsing rules (used by `build.py`)

1. The title line (`# Presentation: ...`) is the first match — anything before it is ignored.
2. Front matter is the bullet list (`- Key: value`) between the title and the first `## Slides` heading. The `## Design tokens` block is recognized inside this region by its heading.
3. The design-tokens YAML lives in a fenced ` ```yaml ` block immediately under `## Design tokens`. Keys are stripped of surrounding quotes and whitespace.
4. Each `### Slide N — title` opens a new slide block. The block ends at the next `### Slide` heading or end-of-file.
5. Field bullets (`- **Field**: value`) are parsed greedily; sub-bullets indented under `**Content**:` become content lines.
6. Free-form continuation lines (indented two-space prose under `**Notes**:`, `**Purpose**:`, or `**Key message**:`) are appended to the field with a single space separator.
7. Slides are sorted by their `N` index — out-of-order slides in the source still emit a contiguous bundle.

---

## Example: the minimal 3-slide deck

See `examples/minimal/presentation_plan.md` for a runnable example. The same plan with no design tokens still builds — the bundle falls back to the defaults in `assets/slides.css`.
