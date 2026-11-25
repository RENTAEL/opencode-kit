# Slide Design Rules

The fixed surface every slide is authored against — canvas, type scale, color contract, accessibility contract, and performance contract. `scripts/build.py` enforces the design tokens in `slides.css`; `overlay.js` enforces the runtime contract.

---

## Virtual canvas

| Property | Value | Reason |
|---|---|---|
| Logical + render canvas | **720 px × 405 px** | Matches `slides-grab-design`. Authoring all slides at this size keeps the slides-grab pipeline compatible AND the iframe-srcdoc host matches without rescaling. |
| Aspect ratio | **16 : 9** | Locked. Letterbox / pillarbox when the viewport differs (handled by flex centering on `.stage`). |
| Scaling | `scale = min(window.innerWidth / 720, window.innerHeight / 405)` | Applied to `.slide-frame` via `transform: scale(...)`. The iframe inside the frame is also 720 × 405. |
| Coordinate units | CSS `px` (authored) | Author with `px` values throughout — the runtime scale gives full-window rendering without per-slide math. |
| Footer safe-zone | **26 px** at `bottom: 0` | The `.slide-footer` band (logo + slide number) is reserved. Author all content with at least **38 px of bottom padding** (or inner-column padding) so nothing collides with the footer at the rendered viewport. |

`scripts/build.py` does not touch `--slide-w` / `--slide-h`; only the *color* + *typography* tokens are user-overridable from `presentation_plan.md`.

---

## Type scale

CSS variables declared in `slides.css`; override-able per deck if the design tokens specify them.

| Token | Default | Role |
|---|---|---|
| `--t-display` | `84px` | Title slide hero (`.slide.is-title h1`). |
| `--t-h1` | `56px` | Slide title (`.slide h1`). |
| `--t-h2` | `36px` | Section header. |
| `--t-body` | `22px` | Bullets, paragraphs. |
| `--t-caption` | `16px` | Footnotes, sources. |

Hard rules:
- **Body floor: 14 px on the virtual canvas** (matches slides-grab's 14 pt rule). Never go below.
- Line height 1.2–1.5 for body, 1.0–1.2 for display / headings.
- Headlines bold (600+), body regular (400).
- Use size for hierarchy. Color and weight reinforce, they do not replace, size.

---

## Color contract

Tokens that `build.py` overrides from `presentation_plan.md`:

| Token | Role | Default |
|---|---|---|
| `--bg` | Slide background. | `#0b0c10` |
| `--surface` | Card / panel surface (when used). | `#16181f` |
| `--fg` | Primary text. | `#f5f5f7` |
| `--muted` | Captions / secondary text. | `#a8acb8` |
| `--accent` | Primary accent (CTAs, links, callouts). | `#7c5cff` |
| `--accent-2` | Secondary accent (used sparingly). | `#ffd166` |
| `--font-display` | Display / heading font family. | `"Inter", system-ui, sans-serif` |
| `--font-body` | Body font family. | `"Inter", system-ui, sans-serif` |

Contrast rules:
- **Body text vs background ≥ 4.5 : 1** (WCAG AA), preferred 7 : 1 (AAA).
- **Captions vs background ≥ 3 : 1**. Never lighter than `--muted`.
- **Functional color** (error red, success green) must pair with an icon or label — never communicate state by color alone.
- **One color dominates**: 60–70 % visual weight on `--bg`, 20–30 % on `--fg`, ~10 % on `--accent`. `--accent-2` only as occasional emphasis.

---

## Layout primitives

`slides.css` ships with conservative defaults on `.slide`:

```css
.slide {
  padding: 64px 80px;            /* breathing room */
  display: flex;
  flex-direction: column;
  gap: 24px;                     /* between header / body / footer */
}

.slide.is-title {
  align-items: center;
  justify-content: center;
  text-align: center;
}
```

Recommended layouts (apply via class on the slide root):

| Layout | Best for | Notes |
|---|---|---|
| Title (`.slide.is-title`) | Opener, section dividers, closer. | Display-size headline, optional eyebrow + subtitle. |
| Two-column | Talking points beside a figure. | Use `display: grid; grid-template-columns: 1fr 1fr; gap: 48px`. |
| Hero-figure + caption | A single dominant image / chart. | `<img>` at `width: 100%; max-height: 80%`. Caption below. |
| Bento (≥ 3 panels) | Comparisons, taxonomies. | `display: grid; grid-template-columns: repeat(...);`. Limit to ≤ 6 cells. |
| Stat callout | Big-number slides. | `<span class="stat">95%</span>` at `--t-display` size + small label. |

Add only what the content needs. **Cardless layouts** beat decorated cards by default — let whitespace, alignment, scale, and contrast carry hierarchy.

---

## Accessibility contract

Honored by `overlay.js` and enforced visually by `slides.css`.

- **`prefers-reduced-motion: reduce`** — auto-animator skipped; per-slide `window.__slideTL` skipped; entrance becomes an instant set of `opacity: 1; transform: none`. `slides.css` media query backs this up with `!important` overrides on `[data-anim]`.
- **Keyboard parity** with every mouse action — overlay buttons mirror the keys (`←`/`→`/`Space`/`Home`/`End`/`F`/`G`/`S`/`Esc`).
- **`aria-label`** on every overlay button (already in `index.html`).
- **Focus rings** visible on `.ov-btn:focus-visible` and `.grid-cell:focus-visible`.
- **Speaker-notes panel** content is announced by screen readers (no `aria-hidden` on it).
- **Color independence** — never communicate state with color alone (see Color contract above).

---

## Performance contract

- **Transform + opacity only** in `data-anim` and per-slide timelines (enforced by `references/animejs-patterns.md` "Don't do these").
- **`will-change: transform, opacity`** declared on the iframe slide host. Browsers re-evaluate on each transition.
- **Lazy slide load** — `overlay.js` creates an `<iframe srcdoc>` for `slides/slide-XX.html` on first navigation; subsequent navigations reuse the iframe element. The bundle never inlines all slides into `index.html`.
- **Cap ~50 simultaneous animations per slide.** If a slide needs more (rare), split it into two slides.
- **Animation cleanup** — every per-slide `__slideTL[i]` must return `{ cancel }`; the bootstrap calls it on `__slideExited` so background `setInterval`s and timelines do not leak across slides.

---

## Iframe isolation contract (binding)

Each slide loads inside its own `<iframe srcdoc>`. This is the only structural guarantee that lets slides author CSS freely without polluting the host.

| Slide authors MAY | Slide authors MUST NOT |
|---|---|
| Use `html`, `body`, `:root`, `*`, `h1`, `.slide` as global selectors. | Reference parent-window globals other than the documented `__slide*` hooks. |
| Declare an inline `<style>` block at the top of the fragment. | Use `position: fixed` (the iframe IS the viewport). |
| Load assets via `./assets/...` relative paths (resolved by `<base href="/">`). | Animate SVG `<g>` elements that have an SVG `transform` attribute via CSS transform — the CSS transform replaces the attribute. Animate inner shapes (`circle`/`rect`/`path`) with `transform-box: fill-box` instead. |
| Declare `window.__slideTL[N] = (root) => ({ cancel })` for idle animations. | Run `setInterval` / `setTimeout` without storing the handle and clearing it in `cancel`. |
| Declare `window.__slideSteps = K` + `window.__slideStep` for click-advance. | Mutate `__slideTL` for slides other than their own. |

---

## Idle animation guideline

Static slides feel dead. Every slide should declare at least one subtle idle motion:

- **Baseline**: breathing scale on a key icon, drifting opacity on background dots, gently pulsing accent dots (1.5–3 s loops, low amplitude). Should not compete with the speaker.
- **Signature** (2–3 per deck): a distinctive topic-anchored motion — token chips jitter on the tokens slide, lever pulse on a cost slide, traveling pulse along link lines on a graph slide. These are memory anchors: pick the slides whose mental model you want the audience to retain.

Implement signatures inside `window.__slideTL[N]` using `animate(...)` with `loop: true`. Always return `{ cancel }` so `__slideExited` can stop the loop.

---

## Step protocol (PowerPoint-style click-advance)

When a slide benefits from staged reveals — comparison cards, poll-style questions, multi-part lists — declare:

```html
<script type="module">
  window.__slideSteps = 4;                  // 1..4 internal steps
  window.__slideStep  = (n, dir) => {       // n = 0..4, dir = +1 / -1
    document.querySelectorAll('.card').forEach((el, i) => {
      el.classList.toggle('is-active', i === n - 1);
      el.classList.toggle('is-done',   i <  n - 1);
    });
  };
</script>
```

Step 0 is the base state (slide just entered, nothing revealed yet). The parent overlay drives steps 1..K via ArrowRight; ArrowLeft reverses; after step K, the next ArrowRight advances to the next slide. The bootstrap calls `__slideStep(0, 1)` automatically on slide enter.

---

## Don't ship these (from compatibility-notes lessons)

| Anti-pattern | Why |
|---|---|
| Aggressive full-bleed gradient backgrounds | Reads as AI slop. Use a single bg color or subtle texture. |
| Generic 3 × 2 icon-plus-blurb grids | Same. Vary layouts. |
| Left-border accent cards on every slide | Visual clutter. Pick one motif and reserve it. |
| Inter / Roboto / Arial as the display font on every deck | Generic. Borrow from `ui-ux-pro-max`'s font pairings. |
| Body text < 14 pt on the virtual canvas | Unreadable in person; fails phase-9 QA. |
| Same layout for every slide | Boring. Mix title slides, hero figures, bento, two-column. |
| Text-only slides for the whole deck | Every slide needs at least one visual anchor. |
| Auto-cycling content that advances without user input | Use the **step protocol** (`__slideSteps` + `__slideStep`) instead, so the speaker controls the pace. Auto-advancing polls / carousels rob the speaker of timing. |
| Content rendered under the 26 px footer band | Reserve 38 px of bottom padding on every slide and inner column. Verified in phase-9 QA screenshots. |
| `setInterval` / `setTimeout` inside a slide that does not return `{ cancel }` | The timer leaks across slide changes, wastes CPU, and visually drifts when the user navigates back. |
| CSS `transform` on an SVG `<g transform="translate(...)">` | The CSS transform replaces the SVG attribute → group collapses to origin. Animate inner shapes positioned via `cx`/`cy`/`x`/`y` instead. |
