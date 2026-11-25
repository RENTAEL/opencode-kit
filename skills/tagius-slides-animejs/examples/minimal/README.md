# Minimal example — "slides-animejs Pattern Tour"

A complete, runnable 5-slide deck produced by the `slides-animejs` pipeline. Each
slide is a hallmark archetype, so the deck doubles as a copy-paste reference for
the runtime conventions (iframe isolation, entrance, idle, step protocol, footer
safe-zone). It is a simplified, palette-neutral distillation of a real deck —
no project-specific media or branding.

## The five archetypes

| # | Archetype | Teaches |
|---|-----------|---------|
| 1 | Title | Entrance choreography (`data-anim` + `data-anim-from`) + one signature idle (breathing SVG ring via `__slideTL[0]`). |
| 2 | Section divider | Big number + label on a single accent field; baseline drift idle (`__slideTL[1]`). |
| 3 | Two-column content | `grid` layout, staggered entrance, breathing-node idle, footer safe-zone (`__slideTL[2]`). |
| 4 | Step protocol | PowerPoint-style click-advance: `__slideSteps = 3` + `__slideStep(n, dir)` with per-step idle; cleanup via `__slideTL[3]`. |
| 5 | Closing | Recap + thank-you; reuses the title idle for bookend symmetry (`__slideTL[4]`). |

## Layout

```
examples/minimal/
├── presentation_plan.md     ← canonical plan (parsed by scripts/build.py)
├── visuals/
│   └── spark.svg            ← self-contained inline mark (title + closing)
├── slides-draft/            ← authored slide fragments (iframe-era conventions)
│   ├── slide-01.html … slide-05.html
└── presentation/            ← built bundle (overwritten on every build)
    ├── index.html
    ├── README.md
    ├── run.py
    ├── assets/
    │   ├── anime.esm.min.js (vendored, copied from skill assets/vendor/)
    │   ├── overlay.css
    │   ├── overlay.js       (iframe slide loader — identical to the canonical asset)
    │   ├── slides.css       (parent-frame tokens from this plan)
    │   └── visuals/spark.svg
    └── slides/
        └── slide-01.html … slide-05.html
```

## Re-build from the example

From this directory:

```sh
python3 ~/.claude/skills/slides-animejs/scripts/build.py
python3 ~/.claude/skills/slides-animejs/scripts/validate_bundle.py
```

The build is idempotent — repeat runs overwrite `./presentation/` without touching
`presentation_plan.md` or `slides-draft/`.

## Run

```sh
cd presentation && python3 run.py
```

The browser opens at `http://127.0.0.1:8000/index.html`. The deck is fully
offline — anime.js is vendored locally; the SVG and HTML fragments are served by
the bundled `run.py`.

## Controls (mirror `assets/README.template.md`)

| Key | Action |
|---|---|
| `→` / `Space` / `PageDown` | Next step / slide |
| `←` / `PageUp` | Previous step / slide |
| `Home` / `End` | First / last slide |
| `F` | Toggle fullscreen |
| `G` | Toggle grid overview |
| `S` | Toggle speaker notes |
| `Esc` | Close panels / exit fullscreen |

On slide 4, `→` advances the in-slide steps (1→2→3) before moving to slide 5.

## How theming works (and stays customizable)

Each slide is rendered in its own `<iframe srcdoc>` for CSS isolation, and **iframe
slides do not load `slides.css`** — so every slide declares its palette inline in
its own `:root` block. To recolour the deck, change the tokens in
`presentation_plan.md` *and* the matching `:root` values in `slides-draft/*.html`.
Nothing about the layout or animation patterns depends on the specific colours;
the dark "Midnight Studio" palette here is just a default, deliberately *not* tied
to any institution's brand.

(`slides.css` still receives the plan's tokens for the parent frame / overlay
chrome — that is what `build.py`'s token injection targets.)

## What this example demonstrates

- **iframe-era slide conventions** — inline `:root`, `data-anim` entrance, real
  `window.__slideTL[index]` idle handles that return `{ cancel }`, and one slide
  using the `__slideSteps` / `__slideStep` step protocol.
- **SVG-safe idle** — idles animate inner shapes (`<circle>` with
  `transform-box: fill-box`), never a `<g transform>` (which a CSS `scale` would
  clobber).
- **Footer safe-zone** — every slide reserves the 26px footer band (≥38px bottom
  padding) so content never collides with the footer.
- **Self-contained, license-clean assets** — one inline SVG mark, no raster media,
  no branding. Swap in your own visuals under `visuals/`.

## Modifying the example

1. Edit `presentation_plan.md` (front matter, tokens, or per-slide blocks).
2. Edit `slides-draft/slide-XX.html` to change layout / content / animation.
   Keep each slide's `__slideTL[N]` index equal to its 0-based position.
3. Re-run `build.py`.
4. Reload the browser.
