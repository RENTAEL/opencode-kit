# anime.js v4 — Condensed Reference

Curated v4 reference for `slides-animejs`. Source: the `anime.js-best-practices` skill (validated November 2025) plus runtime cache of the Context7 docs fetched at phase 0 (`mcp__claude_ai_Context7__resolve-library-id` + `query-docs`).

> **Invariants (must always hold):** durations and delays are **milliseconds** (not seconds); the default WAAPI easing is `linear` (not `ease`); animate only `transform` and `opacity`; honor `prefers-reduced-motion: reduce`.

---

## Two engines, one package

```js
import { waapi, animate, createTimeline, stagger, splitText } from "animejs";
```

| Engine | Import | When to use |
|---|---|---|
| **WAAPI** | `waapi.animate(targets, params)` | Default for CSS transforms / opacity. Hardware-accelerated. ~3 KB if subpath-imported. Use this for entrance + transition animations in `slides-animejs`. |
| **JS engine** | `animate(targets, params)` | Animating JS objects, Canvas/WebGL, SVG path morphing, ≥500 targets, or anything that needs `onUpdate` / extensive callbacks. |

Both share the same parameter shape — easings, keyframes, stagger, callbacks — so switching engines is mostly a rename.

### Subpath imports (smaller bundles)

```js
import { waapi } from "animejs/waapi";       // ~3 KB
import { animate } from "animejs/animation";
import { stagger, random } from "animejs/utils";
import { splitText } from "animejs/text";
```

---

## Targets and properties

Targets: CSS selector string, DOM element, array of elements, NodeList, or (for the JS engine) plain JavaScript object.

Animatable properties:
- **CSS transforms** — `translateX`, `translateY`, `translateZ`, `rotate`, `rotateX/Y/Z`, `scale`, `scaleX/Y`, `skew`, `skewX/Y`.
- **CSS properties** — `opacity`, `width`, `height`, `margin`, `padding`, `borderRadius`, `backgroundColor`, `color`. **Avoid layout properties in `slides-animejs`** — they trigger reflow and cost frame time. Stick to `transform` + `opacity`.
- **CSS custom properties** — `'--my-var'` (with the leading `--`).
- **SVG attributes** — `cx`, `cy`, `r`, `fill`, `stroke`, `strokeDashoffset`, `points`, `d`.

### Value forms

```js
waapi.animate(".x", {
  translateX: 250,            // absolute
  width: "100%",              // with units
  translateY: "+=50",         // relative
  opacity: [0, 1],            // from → to
  scale: (el, i) => 1 + i * 0.1,  // function per target
  rotate: [
    { value: 90, duration: 400 },
    { value: 0, duration: 400 }
  ],                          // keyframes
  duration: 600,              // ms
  ease: "outExpo"
});
```

---

## Easings

Pattern: `{in|out|inOut}{Quad|Cubic|Quart|Quint|Sine|Expo|Circ|Back|Elastic|Bounce}`, plus `linear` and `steps(n)`.

```js
waapi.animate(".x", { translateX: 200, ease: "outExpo" });
waapi.animate(".x", { translateX: 200, ease: "inOutQuad" });
animate(".x", { translateX: 200, ease: cubicBezier(0.7, 0.1, 0.5, 0.9) });
animate(".x", { scale: 1.2, ease: spring({ stiffness: 90, damping: 14 }) });
animate(".x", { scale: 1.2, ease: spring({ bounce: 0.25, duration: 800 }) });
```

For UI: `outExpo`, `outQuad`, `outCubic` are the safest defaults. `outBack` and `outElastic` for personality. Avoid `linear` for UI motion — it feels mechanical.

---

## Stagger

Time staggering (WAAPI):

```js
import { waapi, stagger } from "animejs";

waapi.animate(".item", {
  translateY: [50, 0],
  opacity: [0, 1],
  delay: stagger(100)         // 100 ms between each
});
```

Options:

```js
stagger(80, { from: "center" });       // ripple from center index
stagger(80, { from: 3 });              // ripple from index 3
stagger(80, { from: "edges" });        // ripple inward
stagger(50, { grid: [10, 10], from: "center" });  // grid stagger
stagger(50, { grid: [10, 10], axis: "y" });
stagger(100, { ease: "outQuad" });     // ease the stagger curve
```

Value staggering (**JS engine only**, not WAAPI):

```js
animate(".bar", { height: stagger([100, 200, 150, 250]) });
```

---

## Timelines (JS engine)

```js
import { createTimeline, stagger } from "animejs";

const tl = createTimeline({ defaults: { duration: 800, ease: "outExpo" } });

tl.add(".box-1", { translateX: 250 })
  .add(".box-2", { translateY: 100 }, "-=400")  // start 400 ms before previous ends
  .add(".box-3", { scale: 1.5 }, "+=200");      // start 200 ms after previous ends
```

Labels:

```js
const tl = createTimeline();
tl.add(".intro", { opacity: [0, 1] })
  .label("afterIntro")
  .add(".content", { translateY: [50, 0] }, "afterIntro")
  .add(".sidebar", { translateX: [-100, 0] }, "afterIntro+=200");
```

Controls (every animation/timeline has these):

```js
tl.play(); tl.pause(); tl.reverse(); tl.restart(); tl.seek(500); tl.complete();
tl.playbackRate = 2;
```

In `slides-animejs`, per-slide custom timelines are registered as:

```html
<script type="module">
  import { createTimeline, stagger } from "../assets/anime.esm.min.js";
  window.__slideTL ??= {};
  window.__slideTL[4] = (root) => {                 // 0-based slide index
    const tl = createTimeline({ defaults: { ease: "outExpo" } });
    tl.add(root.querySelector(".title"), { opacity: [0, 1], translateY: [40, 0], duration: 700 })
      .add(root.querySelectorAll(".bullet"), { opacity: [0, 1], translateX: [-30, 0], delay: stagger(120), duration: 500 }, "-=300");
  };
</script>
```

`overlay.js` calls `window.__slideTL?.[i]?.(slideEl)` after the entrance auto-animator finishes.

---

## Text animation with splitText

**Always use `splitText()`** for character / word / line animations — never split text manually. It handles accessibility (`aria-label`), whitespace, and returns ready-to-animate element arrays.

```js
import { waapi, splitText, stagger } from "animejs";

const { chars, words, lines } = splitText(".text", {
  chars: true, words: true, lines: true,
  accessible: true,
  includeSpaces: true,
  // Optional wrappers (per surface):
  chars: { wrap: "span", class: "char" },
  words: { wrap: "clip" },   // 'clip' adds overflow:hidden for reveal effects
  lines: { wrap: "div" }
});

waapi.animate(chars, {
  translateY: [-20, 0],
  opacity: [0, 1],
  delay: stagger(50),
  duration: 600,
  ease: "outExpo"
});
```

---

## Callbacks

```js
animate(".x", {
  translateX: 200,
  onBegin: (a) => {/* ... */},
  onUpdate: (a) => {/* receive a.progress, a.currentTime */},
  onComplete: (a) => {/* ... */},
  onLoop: (a) => {/* ... */}
});

// Promise interface
await animate(".step-1", { opacity: [0, 1] }).then();
```

WAAPI animations have a `.finished` Promise (matches the native Web Animations API):

```js
const anim = waapi.animate(".x", { opacity: [0, 1], duration: 400 });
anim.finished.then(() => console.log("done"));
```

---

## Reduced motion

```js
const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (REDUCED_MOTION) {
  element.style.opacity = "1";
  element.style.transform = "none";
} else {
  waapi.animate(element, { opacity: [0, 1], translateY: [24, 0], duration: 600 });
}
```

In `slides-animejs`, `overlay.js` checks this once at module load and short-circuits both the auto-animator and per-slide custom timelines when reduced motion is requested.

---

## Performance checklist (used by phase 9 QA)

- [ ] Animations animate only `transform` and `opacity`.
- [ ] `will-change` is set only during the active transition window (handled by `.slide.is-active` rules).
- [ ] Animations are cancelled (`anim.cancel()` / `tl.complete()`) when slides are removed or navigated away.
- [ ] Stagger keeps per-frame cost bounded (≤ 50 simultaneous animations per slide).
- [ ] `prefers-reduced-motion: reduce` is honored.

---

## Common bugs

| Symptom | Cause | Fix |
|---|---|---|
| Animation invisible / "instant" | Duration is `0.6` instead of `600` (CSS habit). | Use **milliseconds**. |
| Linear easing feels mechanical | WAAPI default is `linear`. | Set `ease: "outExpo"` (or similar). |
| Layout jumps mid-animation | Animating `width` / `height` / `top` / `left`. | Switch to `transform`. |
| Memory leak on slide reload | Old animations not cancelled. | Call `anim.cancel()` in cleanup, or use the engine's `getAnimations()` to clear. |
| Custom `__slideTL` runs on wrong slide | Index drift after re-ordering. | Use the namespaced form `window.__slideTL[n]` where `n` is the build-time slide index. |
