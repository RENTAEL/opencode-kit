# anime.js Patterns for `slides-animejs`

The curated recipe set the bundler and runtime support. Pattern names referenced from `presentation_plan.md` `Animation hints` and from per-slide `data-anim-from` map to these.

> **Convention:** all entrance / exit / transition recipes use **WAAPI** (`waapi.animate`). Per-slide orchestrated timelines use the **JS engine** (`createTimeline`). See `references/animejs-condensed.md` for the engine selection rule.

---

## Entrance recipes (auto-animator)

`overlay.js` reads `data-anim` on slide root descendants and dispatches by `data-anim-from`:

| `data-anim-from` | Keyframes | Suggested for |
|---|---|---|
| `up` (default) | `opacity: [0, 1]`, `translateY: [24, 0]` | Bullets, body paragraphs. |
| `down` | `opacity: [0, 1]`, `translateY: [-24, 0]` | Top-of-slide labels, eyebrow text. |
| `left` | `opacity: [0, 1]`, `translateX: [-32, 0]` | Icons next to titles, sidebar elements. |
| `right` | `opacity: [0, 1]`, `translateX: [32, 0]` | Right-aligned callouts, secondary captions. |
| `scale` | `opacity: [0, 1]`, `scale: [0.94, 1]` | Big numbers, hero images, badges. |
| `fade` | `opacity: [0, 1]` | Footnotes, watermarks, anything where motion would be noisy. |

Defaults applied to every variant: `duration: 600`, `ease: "outCubic"`, `delay: stagger(80)`.

Slide-level overrides:
- `<section class="slide" data-anim-stagger="120">` changes the stagger for that slide.
- Mix variants in one slide — the auto-animator groups by `data-anim-from` and runs each group's stagger independently.

---

## Slide transition (forward / backward)

Handled in `overlay.js` `goTo(i, dir)`. Defaults:

```js
// outgoing slide
waapi.animate(prev, {
  opacity: [1, 0],
  translateX: [0, dir * -120],
  duration: 420,
  ease: "outQuad"
});

// incoming slide
waapi.animate(next, {
  opacity: [0, 1],
  translateX: [dir * 120, 0],
  duration: 480,
  ease: "outQuad"
});
```

The slight asymmetry (480 in, 420 out) gives the incoming slide a hair more "weight" — the trick is borrowed from MD motion's "exit faster than enter" guideline. Override per-deck by editing `overlay.js` once after building if a different feel is wanted.

---

## Reveal patterns

### Word-by-word reveal (clip + `splitText`)

```html
<h1 class="reveal">Anime.js v4 in three slides</h1>
<script type="module">
  import { waapi, splitText, stagger } from "../assets/anime.esm.min.js";
  window.__slideTL ??= {};
  window.__slideTL[0] = (root) => {
    const { words } = splitText(root.querySelector(".reveal"), {
      words: { wrap: "clip" }
    });
    waapi.animate(words, {
      translateY: ["100%", "0%"],
      delay: stagger(100),
      duration: 800,
      ease: "outExpo"
    });
  };
</script>
```

The `wrap: "clip"` option adds `overflow: hidden` to each word wrapper so the rise looks like text emerging from below.

### Wave on characters

```js
const { chars } = splitText(".wave", { chars: true });
waapi.animate(chars, {
  translateY: -15,
  delay: stagger(40, { from: "center" }),
  duration: 400,
  loop: true,
  alternate: true,
  ease: "inOutSine"
});
```

Use sparingly — looping animations distract from speaker narration. Best for the title slide if the deck has a playful tone.

---

## Stagger choices

- **Lists / bullets**: `stagger(80)` (matches the auto-animator default).
- **Grids / bento layouts**: `stagger(50, { grid: [cols, rows], from: "center" })`.
- **Decorative ripples**: `stagger(40, { from: "edges" })`.
- **Lots of items (> 12)**: drop to `stagger(40)` and cap total entrance to ~800 ms so the slide settles before the speaker starts talking.

---

## Spring physics (use sparingly)

```js
import { animate, spring } from "animejs";

animate(".badge", {
  scale: [0, 1],
  ease: spring({ stiffness: 120, damping: 12 })
});
```

Spring eases require the JS engine. Reserve for hero elements that benefit from organic overshoot (large stat callouts, "look at me" badges). Never for whole-slide entrances — the unpredictability of spring duration makes timing slides hard.

---

## Per-slide custom timelines

When you need precise orchestration across multiple groups:

```html
<script type="module">
  import { createTimeline, stagger } from "../assets/anime.esm.min.js";
  window.__slideTL ??= {};
  window.__slideTL[2] = (root) => {
    const tl = createTimeline({ defaults: { ease: "outExpo" } });
    tl.add(root.querySelector(".eyebrow"), { opacity: [0, 1], translateY: [-12, 0], duration: 400 })
      .add(root.querySelector("h1"), { opacity: [0, 1], translateY: [24, 0], duration: 600 }, "-=200")
      .add(root.querySelectorAll(".bullet"), { opacity: [0, 1], translateX: [-30, 0], delay: stagger(120), duration: 500 }, "-=300")
      .add(root.querySelector("img"), { opacity: [0, 1], scale: [0.96, 1], duration: 700 }, "-=400");
  };
</script>
```

The `n` in `window.__slideTL[n]` is the **0-based slide index**. `overlay.js` invokes it after the auto-animator runs, so timelines layer on top of the basic `data-anim` entrance — or you can omit `data-anim` entirely and let the timeline drive everything.

`prefers-reduced-motion: reduce` short-circuits both the auto-animator and `window.__slideTL` — slides snap to their final visual state with no animation.

---

## Don't do these

| Pattern | Why to avoid |
|---|---|
| Animating `width` / `height` / `top` / `left` | Triggers layout; janky. Use `transform`. |
| Looping entrance animations | Distracts from speaker; never seen in good decks. |
| Spring physics on > 3 elements per slide | Unpredictable timing collisions. |
| Duration > 1000 ms for entrance | Slows pace; audience attention drifts. |
| Linear easing on UI motion | Feels mechanical. Use `outExpo` / `outCubic` / `outQuad`. |
| Animating decorative-only elements | If removing the animation doesn't reduce comprehension, drop it. |
