/*
 * Overlay + slide-loader runtime for slides-animejs.
 *
 * ISOLATION REWRITE (2026-05-12):
 *   Each slide is rendered inside its own `<iframe srcdoc>` so its inline
 *   `<style>` block (which routinely targets global selectors like html, body,
 *   :root, h1, .slide) cannot leak into the host document. This eliminates the
 *   cascading-breakage bug where each new navigation accumulated more global
 *   rules and re-styled every previously loaded slide.
 *
 *   Transitions: parent animates the iframe element itself (transform + opacity).
 *   Entrance animations and per-slide custom timelines run INSIDE the iframe via
 *   a bootstrap script appended to the srcdoc. The iframe exposes:
 *     - window.__slideEntered(i)   parent calls after transition completes
 *     - window.__slideExited()     parent calls before transition starts
 *   The bootstrap cancels any prior per-slide timeline (return shape:
 *   `{ cancel: () => void }`) so background intervals/timers do not leak.
 *
 *   Anime.js v4 notes:
 *     - waapi.animate(...).then(cb)  for transition completion (v4 API; .finished is undefined)
 *     - waapi.animate uses WAAPI fill:'forwards' by default → reset inline style
 *       on the iframe element before re-animating to avoid leftover transforms.
 */

import { waapi } from "./anime.esm.min.js";

const SLIDES = window.__SLIDES__ ?? [];
const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const SLIDE_W = 720;
const SLIDE_H = 405;
const IDLE_MS = 2500;
const ENTER_MS = 280;

const frame      = document.getElementById("slideFrame");
const overlay    = document.getElementById("overlay");
const gridView   = document.getElementById("gridView");
const notesPanel = document.getElementById("notesPanel");

let current = 0;
let currentStep = 0;
let idleTimer = null;
let transitioning = false;

const iframes = new Map();
const loadPromises = new Map();

function getCurrentSteps() {
  const ifr = iframes.get(current);
  try { return Number(ifr?.contentWindow?.__getSlideSteps?.() || 0); }
  catch (e) { return 0; }
}

function callStep(n, dir) {
  const ifr = iframes.get(current);
  try { ifr?.contentWindow?.__advanceStep?.(n, dir); }
  catch (e) { /* noop */ }
}

function tryAdvanceStep(dir) {
  const total = getCurrentSteps();
  if (total <= 0) return false;
  const next = currentStep + dir;
  if (next < 0 || next > total) return false;
  currentStep = next;
  callStep(currentStep, dir);
  return true;
}

function fitSlide() {
  const scale = Math.min(window.innerWidth / SLIDE_W, window.innerHeight / SLIDE_H);
  frame.style.transform = `scale(${scale})`;
}

function buildSrcdoc(fragmentHtml) {
  // Bootstrap script runs entrance animations + per-slide timeline INSIDE iframe.
  // `<base href="/">` ensures relative paths in slide HTML (./assets/...) resolve
  // against the server root, matching how slides resolved when injected inline.
  //
  // Step protocol (PowerPoint-style click-advance):
  //   A slide may set `window.__slideSteps = N` (1..N internal steps) and
  //   `window.__slideStep = (n, dir) => void` to handle step transitions.
  //   Parent calls __slideStep(n, dir) as the user presses ArrowRight/ArrowLeft.
  //   Step 0 = base (slide just entered, no steps revealed yet).
  //   Parent advances to next slide only after step counter exceeds __slideSteps.
  const bootstrap = `
<script type="module">
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const variants = {
  up:    { ty: 20 },
  down:  { ty: -20 },
  left:  { tx: -28 },
  right: { tx: 28 },
  scale: { s: 0.94 },
  fade:  {},
};
function startTransform(v) {
  const parts = [];
  if (v.ty != null) parts.push('translateY(' + v.ty + 'px)');
  if (v.tx != null) parts.push('translateX(' + v.tx + 'px)');
  if (v.s  != null) parts.push('scale(' + v.s + ')');
  return parts.join(' ') || 'none';
}
function runEntrance() {
  const items = document.querySelectorAll('[data-anim]');
  if (RM) {
    items.forEach(el => { el.style.opacity = '1'; el.style.transform = 'none'; });
    return;
  }
  const groups = new Map();
  items.forEach(el => {
    const from = el.dataset.animFrom || 'up';
    if (!groups.has(from)) groups.set(from, []);
    groups.get(from).push(el);
  });
  let order = 0;
  for (const [from, els] of groups) {
    const v = variants[from] || variants.up;
    els.forEach((el) => {
      const start = { opacity: 0, transform: startTransform(v) };
      const end   = { opacity: 1, transform: 'none' };
      el.animate([start, end], {
        duration: 380,
        delay: (order++) * 45,
        easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
        fill: 'forwards',
      });
    });
  }
}
function killTL() {
  try { window.__currentTL?.cancel?.(); } catch (e) { /* noop */ }
  window.__currentTL = null;
}
function runTL(i) {
  if (window.__slideTL && typeof window.__slideTL[i] === 'function') {
    try { window.__currentTL = window.__slideTL[i](document); }
    catch (e) { console.warn('slideTL[' + i + '] error', e); }
  }
}
window.__getSlideSteps = () => Number(window.__slideSteps || 0);
window.__advanceStep   = (n, dir) => {
  if (typeof window.__slideStep === 'function') {
    try { window.__slideStep(n, dir); } catch (e) { console.warn('slideStep error', e); }
  }
};
window.__slideEntered = (i) => {
  killTL();
  runEntrance();
  runTL(i);
  // Initialise to step 0 (base state, before any user click within the slide).
  if (typeof window.__slideStep === 'function') {
    try { window.__slideStep(0, 1); } catch (e) { /* noop */ }
  }
};
window.__slideExited  = () => {
  killTL();
  document.querySelectorAll('[data-anim]').forEach(el => {
    el.getAnimations?.().forEach(a => a.cancel());
    el.style.opacity = '';
    el.style.transform = '';
  });
};
</script>
`.trim();
  return `<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8">
<base href="/">
<style>
  html, body { margin: 0; padding: 0; width: ${SLIDE_W}px; height: ${SLIDE_H}px; overflow: hidden; background: transparent; }
  [data-anim] { opacity: 0; }
</style>
</head><body>
${fragmentHtml}
${bootstrap}
</body></html>`;
}

function loadSlide(i) {
  if (iframes.has(i)) return loadPromises.get(i);
  const promise = (async () => {
    const html = await fetch(`slides/${SLIDES[i].file}`).then(r => r.text());
    const ifr = document.createElement("iframe");
    ifr.className = "slide";
    ifr.dataset.i = i;
    ifr.setAttribute("title", SLIDES[i].title || `Slide ${i + 1}`);
    ifr.setAttribute("tabindex", "-1");
    ifr.setAttribute("loading", "eager");
    // Listen for load before resolving (so __slideEntered is defined).
    const loaded = new Promise(res => ifr.addEventListener("load", res, { once: true }));
    ifr.srcdoc = buildSrcdoc(html);
    frame.appendChild(ifr);
    iframes.set(i, ifr);
    await loaded;
    return ifr;
  })();
  loadPromises.set(i, promise);
  return promise;
}

function resetStyle(ifr) {
  ifr.style.transform = "";
  ifr.style.opacity = "";
}

async function goTo(i, dir = 1) {
  if (i < 0 || i >= SLIDES.length) return;
  if (transitioning) return;
  if (i === current && frame.querySelector(".slide.is-active")) return;
  transitioning = true;

  const next = await loadSlide(i);
  const prev = frame.querySelector("iframe.slide.is-active");

  if (REDUCED_MOTION) {
    if (prev && prev !== next) {
      prev.classList.remove("is-active");
      resetStyle(prev);
      prev.contentWindow?.__slideExited?.();
    }
    resetStyle(next);
    next.classList.add("is-active");
    current = i;
    currentStep = 0;
    next.contentWindow?.__slideEntered?.(i);
    updateChrome();
    transitioning = false;
    return;
  }

  if (prev && prev !== next) {
    prev.contentWindow?.__slideExited?.();
    // Reset before re-animating so prior commits don't compound.
    resetStyle(prev);
    waapi.animate(prev, {
      opacity: [1, 0],
      translateX: [0, dir * -60],
      duration: ENTER_MS,
      ease: "outQuad",
    }).then(() => {
      prev.classList.remove("is-active");
      resetStyle(prev);
    });
  }

  resetStyle(next);
  next.classList.add("is-active");
  current = i;
  currentStep = 0;
  waapi.animate(next, {
    opacity: [0, 1],
    translateX: [dir * 60, 0],
    duration: ENTER_MS,
    ease: "outQuad",
  }).then(() => {
    resetStyle(next);
    next.contentWindow?.__slideEntered?.(i);
    transitioning = false;
  });

  updateChrome();
}

function updateChrome() {
  const idxEl   = document.getElementById("slideIdx");
  const totalEl = document.getElementById("slideTotal");
  const fill    = document.getElementById("progressFill");
  const notes   = document.getElementById("notesBody");
  if (idxEl)   idxEl.textContent   = String(current + 1);
  if (totalEl) totalEl.textContent = String(SLIDES.length);
  if (fill)    fill.style.width    = `${((current + 1) / SLIDES.length) * 100}%`;
  if (notes)   notes.textContent   = SLIDES[current]?.notes ?? "";
  highlightGridActive();
}

function showOverlay() {
  overlay.classList.remove("is-idle");
  document.body.style.cursor = "default";
  if (idleTimer) clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    overlay.classList.add("is-idle");
    document.body.style.cursor = "none";
  }, IDLE_MS);
}

function toggleFullscreen() {
  if (document.fullscreenElement) document.exitFullscreen?.();
  else document.documentElement.requestFullscreen?.();
}

function closePanels() {
  gridView.classList.add("hidden");
  notesPanel.classList.add("hidden");
}

function buildGrid() {
  gridView.innerHTML = "";
  SLIDES.forEach((s, i) => {
    const cell = document.createElement("div");
    cell.className = "grid-cell";
    cell.setAttribute("role", "button");
    cell.setAttribute("tabindex", "0");
    cell.dataset.i = i;
    const title = s.title && s.title.trim() ? s.title : `Slide ${i + 1}`;
    cell.innerHTML = `
      <div class="grid-thumb"><span class="grid-num">${i + 1}</span></div>
      <div class="grid-title">${title}</div>
    `;
    const jump = () => {
      gridView.classList.add("hidden");
      goTo(i, i >= current ? 1 : -1);
    };
    cell.addEventListener("click", jump);
    cell.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); jump(); }
    });
    gridView.appendChild(cell);
  });
}

function highlightGridActive() {
  gridView.querySelectorAll(".grid-cell").forEach((c) => {
    c.classList.toggle("is-active", Number(c.dataset.i) === current);
  });
}

function toggleGrid()  { gridView.classList.toggle("hidden"); if (!gridView.classList.contains("hidden")) highlightGridActive(); }
function toggleNotes() { notesPanel.classList.toggle("hidden"); }

window.addEventListener("resize", fitSlide);
fitSlide();
buildGrid();

addEventListener("keydown", (e) => {
  showOverlay();
  if (["ArrowRight", " ", "PageDown"].includes(e.key)) {
    e.preventDefault();
    if (!tryAdvanceStep(1)) goTo(current + 1, 1);
  }
  else if (["ArrowLeft", "PageUp"].includes(e.key)) {
    e.preventDefault();
    if (!tryAdvanceStep(-1)) goTo(current - 1, -1);
  }
  else if (e.key === "f" || e.key === "F")  toggleFullscreen();
  else if (e.key === "g" || e.key === "G")  toggleGrid();
  else if (e.key === "s" || e.key === "S")  toggleNotes();
  else if (e.key === "Escape") { closePanels(); if (document.fullscreenElement) document.exitFullscreen?.(); }
  else if (e.key === "Home")   goTo(0,                -1);
  else if (e.key === "End")    goTo(SLIDES.length - 1, 1);
});

addEventListener("mousemove", showOverlay);
addEventListener("click",     showOverlay);

document.getElementById("btnPrev")?.addEventListener("click",  () => { if (!tryAdvanceStep(-1)) goTo(current - 1, -1); });
document.getElementById("btnNext")?.addEventListener("click",  () => { if (!tryAdvanceStep(1))  goTo(current + 1,  1); });
document.getElementById("btnFull")?.addEventListener("click",  toggleFullscreen);
document.getElementById("btnGrid")?.addEventListener("click",  toggleGrid);
document.getElementById("btnNotes")?.addEventListener("click", toggleNotes);

showOverlay();
if (SLIDES.length) goTo(0, 1);
