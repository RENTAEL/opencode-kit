# Presentation: slides-animejs Pattern Tour

- Author: slides-animejs
- Audience: technical
- Length: 5 slides
- Tone: playful
- Academic: no
- Memes allowed: no
- Palette: Midnight Studio (example default — swap freely)
- Style: minimal
- Fonts: Inter / Inter

## Design tokens

Palette is fully user-customizable. These tokens are the example default; each
slide redeclares them inline in its `:root` (iframe slides do not load
`slides.css`), so recolouring the deck = change these values here AND in the
slides' `:root` blocks. Nothing about the layout/animation patterns depends on
the specific colours.

```yaml
bg: "#0b0c1a"
surface: "#181a2d"
fg: "#f5f5f7"
muted: "#a8acb8"
accent: "#7c5cff"
accent-2: "#ffd166"
font-display: "Inter, system-ui, sans-serif"
font-body: "Inter, system-ui, sans-serif"
```

## Slides

### Slide 1 — Title (entrance + signature idle)
- **Purpose**: Demonstrate the title archetype: entrance choreography + one signature idle.
- **Key message**: A title slide should arrive, then quietly breathe.
- **Content**:
  - Eyebrow, headline, subtitle. Inline SVG mark.
  - Signature idle: the accent ring breathes (scale + opacity) via `__slideTL[0]`.
- **Visuals**: `visuals/spark.svg`
- **Animation hints**: `entrance: scale + fade-up`, `idle: breathing ring`
- **Meme**: none
- **Notes**: The idle is the memory anchor — keep it subtle.
- **Status**: finalized

### Slide 2 — Section divider
- **Purpose**: Demonstrate the section-divider archetype (big number + label on an accent field).
- **Key message**: Dividers orient the audience between sections.
- **Content**:
  - Oversized section number, section title, thin rule.
  - Baseline idle: the number drifts a few pixels.
- **Visuals**:
- **Animation hints**: `entrance: fade-up`, `idle: drift`
- **Meme**: none
- **Notes**: One accent colour fills the field; text stays high-contrast.
- **Status**: finalized

### Slide 3 — Two-column content (idle + footer safe-zone)
- **Purpose**: Demonstrate a two-column layout, staggered entrance, baseline idle, and the footer safe-zone.
- **Key message**: Most content slides are a column of points beside a supporting visual.
- **Content**:
  - Left: three bullet points (staggered entrance).
  - Right: inline-SVG diagram with a gentle breathing idle.
  - Footer reserved (≥38px bottom padding).
- **Visuals**:
- **Animation hints**: `entrance: fade-up + stagger`, `idle: breathing nodes`
- **Meme**: none
- **Notes**: Content clears the 26px footer band.
- **Status**: finalized

### Slide 4 — Step protocol (PowerPoint-style click-advance)
- **Purpose**: Demonstrate `__slideSteps` / `__slideStep` click-advance with per-step idle.
- **Key message**: Reveal one idea at a time; each reveal gets its own micro-animation.
- **Content**:
  - Three reveal cards. ArrowRight advances 1..3 within the slide before moving on.
  - Active card highlighted; per-step idle on the active card only.
- **Visuals**:
- **Animation hints**: `steps: 3`, `idle: per-step`
- **Meme**: none
- **Notes**: Parent calls step 0 on enter (base state). `__slideTL[3]` cancel cleans up.
- **Status**: finalized

### Slide 5 — Closing
- **Purpose**: Demonstrate a clean closing archetype.
- **Key message**: End on the recap and a thank-you.
- **Content**:
  - Thank-you headline, one-line recap, inline SVG mark.
  - Signature idle reused from the title for bookend symmetry.
- **Visuals**: `visuals/spark.svg`
- **Animation hints**: `entrance: scale + fade-up`, `idle: breathing ring`
- **Meme**: none
- **Notes**: Bookends the title slide.
- **Status**: finalized
