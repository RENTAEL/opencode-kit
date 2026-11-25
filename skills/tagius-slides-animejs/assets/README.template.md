# {{TITLE}}

A self-contained animated slide deck built with [anime.js v4](https://animejs.com/). The bundle runs entirely offline.

## Run

```sh
python3 run.py
```

The default port is `8000`. Override with `SLIDES_PORT`:

```sh
SLIDES_PORT=9000 python3 run.py
```

Your browser will open at `http://127.0.0.1:8000/index.html`.

## Controls

| Key | Action |
|---|---|
| `→` / `Space` / `PageDown` | Next slide |
| `←` / `PageUp` | Previous slide |
| `F` | Toggle fullscreen |
| `G` | Toggle grid / overview |
| `S` | Toggle speaker notes |
| `Esc` | Close panels / exit fullscreen |

Click the overlay buttons for the same actions with the mouse.

## Files

- `index.html` — entry point.
- `slides/slide-XX.html` — per-slide fragments (loaded on demand).
- `assets/anime.esm.min.js` — vendored anime.js v4 (no network needed).
- `assets/overlay.{css,js}` — overlay UI.
- `assets/slides.css` — 16:9 canvas + design tokens.
- `assets/visuals/` — mirrored project assets.
- `backup.pdf` — PDF backup (produced by `slides-grab-export`).

## Accessibility

The deck respects `prefers-reduced-motion`. When the user has reduced-motion preferences enabled, entrance animations and slide transitions short-circuit to instant state changes.
