# Workflow Playbook — Phases 0–10

The operational playbook for `slides-animejs`. Each phase has explicit **enter when**, **do**, **ask**, **write**, **exit when** rules. The orchestrator reads `CLAUDE.md` first; if a `## Current phase` block exists, summarize state in two lines and ask: "Continue from phase X, or jump to phase Y?".

> All file paths in this document are relative to the user's working directory. The skill never writes outside `./visuals/`, `./presentation/`, `CLAUDE.md`, `AGENTS.md`, `presentation_plan.md`, and (optionally) `./slides-draft/`.

---

## Phase 0 — Bootstrap

**Enter when**: the skill is triggered.

**Do**:
0. **Dependency preflight.** Verify the sub-skills this pipeline orchestrates are available before committing the user to the workflow.
   - **Hard-required** (block if any missing): `slides-grab-plan`, `slides-grab-design`, `slides-grab-export`, `ui-ux-pro-max`, `scientific-brainstorming`, `anime.js-best-practices`, and the **Context7 MCP** server.
   - **Conditional** (warn only, needed for one feature each): `pptx` (PPTX input), `scientific-slides` (academic decks), `meme-factory` (memes allowed), `playwright-cli` (QA screenshots).
   - **Detection**: a skill is present if it appears in the agent's available-skills list, or `ls ~/.claude/skills/<name>` resolves; plugin-cached skills count as present when listed even if not under `~/.claude/skills/`. Context7 is present if its `mcp__claude_ai_Context7__*` tools are callable.
   - **Behavior**: print a short checklist (present / missing). If a **hard-required** skill or Context7 is missing, stop and tell the user how to install it (skills: drop into `~/.claude/skills/<name>/` or install the owning plugin; Context7: enable the MCP server), then halt phase 0. If only **conditional** skills are missing, warn that the matching feature will be skipped/degraded and continue.
1. Verify the working directory. Print: "Working in `<cwd>`. The bundle will go in `./presentation/`."
2. Create `./visuals/` if it doesn't exist. Add `./visuals/.gitkeep` if the user has a git repo.
3. Resolve anime.js v4 via Context7:
   - Call `mcp__claude_ai_Context7__resolve-library-id` with `anime.js`.
   - Call `mcp__claude_ai_Context7__query-docs` on the resolved ID for the API surfaces: `animate`, `waapi.animate`, `createTimeline`, `stagger`, `splitText`, `spring`, `cubicBezier`, easings.
   - If Context7 fails, fall back to `references/animejs-condensed.md` (which is a curated snapshot of `anime.js-best-practices`).
4. Run `python3 ~/.claude/skills/slides-animejs/scripts/fetch_animejs.py` — vendors `anime.esm.min.js` into the skill's `assets/vendor/`. Idempotent; safe to call repeatedly.
5. Initialize or update both `CLAUDE.md` and `AGENTS.md` from `assets/claude.md.template` / `assets/agents.md.template`. Substitute `{{PHASE_ID}}` = `0`, `{{PHASE_STATUS}}` = `bootstrap complete`, `{{ANIMEJS_SNAPSHOT}}` = the condensed reference.

**Ask**: nothing.

**Write**: `CLAUDE.md`, `AGENTS.md`, `./visuals/` (if absent), `~/.claude/skills/slides-animejs/assets/vendor/anime.esm.min.js`.

**Exit when**: dependency preflight passed (no hard-required skill missing) AND anime.js reference is captured AND the bundle is vendored.

---

## Phase 1 — Intake

**Enter when**: phase 0 done.

**Do**:
1. Detect input type:
   - If the user provided a `.pptx` path → run `python3 ~/.claude/skills/slides-animejs/scripts/extract_pptx.py <path> --visuals-dir visuals --manifest intake-manifest.json`. Read the manifest into the orchestrator's context. Surface any warnings (especially EMF/WMF) to the user.
   - If the user provided a Markdown outline or free text → capture as the seed for `presentation_plan.md`.
   - If neither → ask for a topic + audience + length triple as the minimum viable input.
2. Use `AskUserQuestion` to fill any missing front-matter fields (audience, length, tone, academic, palette preference, memes allowed). Cap at 3 questions per turn; default-and-move-on when the user is silent on optional preferences.
3. Seed `presentation_plan.md` with the front matter and a stub `### Slide N — <draft title>` block per slide.

**Verbatim ask** (when audience/tone/etc. are missing):

> A few quick questions before I draft content:
>
> 1. **Audience** — technical, general, mixed, academic, or sales?
> 2. **Length** — how many slides, or how many minutes?
> 3. **Academic?** — should I borrow structural rules from `scientific-slides` (IMRAD, citations)?
>
> (I'll ask about tone, palette, and memes in a moment.)

**Write**: `presentation_plan.md` (seed), `./visuals/from-pptx/` if PPTX was provided.

**Exit when**: front matter complete and at least slide titles stubbed.

---

## Phase 2 — Content brainstorm

**Enter when**: phase 1 produced a stub plan.

**Do**:
1. Invoke `scientific-brainstorming` with a structured brief: `topic`, `audience`, `length`, `tone`, plus the explicit constraint: "Emit one bullet block per slide matching the `presentation_plan.md` schema in `references/presentation-plan-schema.md`. Stop at slide N."
2. If `Academic: yes`, also invoke `scientific-slides` with: "Provide structural guidance for a `<talk-type>`, `<length>`-minute talk to `<audience>`. Do not generate slides. Cite which sections of `references/presentation_structure.md` and `references/talk_types_guide.md` apply."
3. Update `presentation_plan.md` slide blocks with the drafted content. Mark every slide `Status: draft`.

**Ask**: nothing (this phase is generation, not Q&A).

**Write**: `presentation_plan.md` with every slide filled.

**Exit when**: all slides have draft content.

---

## Phase 3 — Content Q&A

**Enter when**: phase 2 produced a draft.

**Do**:
1. Print a short summary: "Brainstorm done. Here are the N slides: [1] title, [2] title, …. Which slides would you like to edit?"
2. Loop on user replies. Apply each edit to the relevant slide block in `presentation_plan.md`. Mark slides `Status: reviewed` once the user accepts them.
3. After every two edits, restate: "Current status: M reviewed / N total. Reply 'done' when content is locked."

**Verbatim ask**:

> Which slides would you like to edit, or reply 'looks good' / 'content locked' to move on.

**Write**: `presentation_plan.md` updates after each edit.

**Exit when**: user says "content is locked" / "looks good" / "design phase".

---

## Phase 4 — Design brainstorm

**Enter when**: content is locked.

**Do**:
1. Locate `ui-ux-pro-max` (typically `~/.agents/skills/ui-ux-pro-max/scripts/search.py`).
2. Run from the user's project directory:
   ```sh
   python3 ~/.agents/skills/ui-ux-pro-max/scripts/search.py "<topic> <audience> <tone>" --design-system -f markdown -p "<plan.title>"
   ```
3. Parse the Markdown report. Extract:
   - Palette name + role-tagged hex codes (3–6 colors).
   - Typography pair (display / body).
   - Style label (bento, minimal, glassmorphism, etc.).
4. Translate into the `## Design tokens` YAML block of `presentation_plan.md`:
   ```yaml
   bg: "#..."
   fg: "#..."
   accent: "#..."
   accent-2: "#..."
   font-display: "..."
   font-body: "..."
   ```
5. Mirror the tokens into the `## Captured design tokens` block of `CLAUDE.md` / `AGENTS.md`.

**Verbatim ask** (if the user did not state a brand preference earlier):

> I have a recommendation from `ui-ux-pro-max`: **<palette-name>** (bg `#…`, accent `#…`). Use this, or do you want something different (e.g. brand colors, a different mood)?

**Write**: `presentation_plan.md` (tokens), `CLAUDE.md` + `AGENTS.md` (tokens).

**Exit when**: tokens are committed to the plan.

---

## Phase 5 — Visual assets

**Enter when**: design tokens committed.

**Do**:
1. Audit `./visuals/` — list every file present.
2. For each slide, decide the visual treatment:
   - **Existing asset** — already in `./visuals/` and referenced in the plan.
   - **Inline SVG** — when a simple icon or diagram would do, generate it inline in the slide HTML (later phase).
   - **External SVG** — fetch from unDraw / Lucide / Tabler / SVGRepo. Save to `./visuals/<name>.svg`.
   - **Meme** — only on slides flagged for it (max ~1 per 6 slides; never if `Academic: yes` and the user did not opt in).
   - **None** — text-only slide is acceptable when content is dense.
3. For meme slots, build the URL `https://api.memegen.link/images/<template>/<top>/<bottom>.png` and download with `urllib.request` or `curl -fsSL` to `./visuals/memes/slide-NN.png`. Cache check: skip download if the file exists (idempotent).
4. Update each slide's `**Visuals**:` field in the plan.
5. **Pause** and instruct the user.

**Verbatim ask**:

> Visual audit done. I have what I need for slides X, Y, Z. For the others, drop any additional assets into `./visuals/` now (any format — PNG, JPG, SVG, MP4). Reply 'continue' when ready, or 'skip' if you want me to proceed without them.

**Write**: `./visuals/memes/`, `./visuals/<svg>.svg`, `presentation_plan.md` (Visuals fields).

**Exit when**: user replies 'continue' or 'skip' AND every slide that lists a visual resolves to a file.

---

## Phase 6 — Static draft via slides-grab

**Enter when**: visuals resolved.

**Do**:
1. Run `slides-grab list-styles` and present a 2–3-style shortlist informed by the `ui-ux-pro-max` style label. Get explicit user approval (this honors slides-grab-plan's style-approval gate).
2. Write `./slides-draft/slide-outline.md` ourselves from `presentation_plan.md`. The meta section must contain `style: <id>` (the approved style). Each `## Slide N` block in the outline carries the key message and content notes for one slide.
3. Mirror `./visuals/` into `./slides-draft/assets/` so slides-grab-design can reference local paths.
4. Invoke `slides-grab-design` with a constrained prompt:
   > Generate `slide-XX.html` files for each slide in `slide-outline.md`. Use `var(--accent)`, `var(--accent-2)`, `var(--fg)`, `var(--bg)` from `assets/slides.css` for colors. Tag entrance elements with `data-anim` and pick `data-anim-from="up|down|left|right|scale|fade"` per element. Author at the slides-grab native 720×405 px canvas. Reserve **38 px of bottom padding** on every slide and inner column so content does not collide with the 26 px footer band. Save under `./slides-draft/`.
   >
   > Each slide should declare at least one subtle idle animation via `window.__slideTL[N] = (root) => ({ cancel })` so static layouts feel alive. For 2–3 slides per deck, author a "signature" idle that visually anchors the slide's topic (token chips jitter, cost-lever pulse, etc.) — these become the memorable anchor visuals.
   >
   > Slides that benefit from staged reveals (polls, comparisons, multi-part lists) should expose the step protocol: `window.__slideSteps = K` and `window.__slideStep = (n, dir) => void`. Parent overlay drives steps 0..K via ArrowRight/ArrowLeft before moving to the next slide.
5. Run `slides-grab validate --slides-dir ./slides-draft` and fix any issues it surfaces.

**Verbatim ask** (once drafts exist):

> Static drafts generated at `./slides-draft/`. Open `./slides-draft/viewer.html` to review. Reply 'feedback: …' with edit requests, or 'looks good' to proceed to animation build.

**Write**: `./slides-draft/slide-outline.md`, `./slides-draft/slide-XX.html`, `./slides-draft/assets/`.

**Exit when**: drafts exist for every slide AND `slides-grab validate` passes.

---

## Phase 7 — Draft feedback

**Enter when**: static drafts exist.

**Do**: loop on user feedback. Two modes:
- **Per-slide HTML edit** — modify `./slides-draft/slide-NN.html` directly via the `Edit` tool. Re-run `slides-grab validate`.
- **Plan-level edit** (content or tokens) — modify `presentation_plan.md` and regenerate the affected slide via `slides-grab-design`.

**Verbatim ask** between rounds:

> Edits applied. Re-review at `./slides-draft/viewer.html`. Reply 'build the animated version' when ready, or 'feedback: …' for more changes.

**Write**: `./slides-draft/*.html`, `presentation_plan.md`.

**Exit when**: user says "build the animated version" / "build it" / "ship it".

---

## Phase 8 — Animation build

**Enter when**: explicit user go-ahead (this is the locked-decision §23 gate).

**Do**:
1. Confirm anime.js is vendored: `ls ~/.claude/skills/slides-animejs/assets/vendor/anime.esm.min.js`. If missing, re-run `fetch_animejs.py`.
2. Run the build:
   ```sh
   python3 ~/.claude/skills/slides-animejs/scripts/build.py \
     --plan presentation_plan.md \
     --slides-dir slides-draft \
     --visuals-dir visuals \
     --out presentation
   ```
3. Run validation:
   ```sh
   python3 ~/.claude/skills/slides-animejs/scripts/validate_bundle.py --bundle presentation
   ```
4. If validation reports blocking issues, fix them in `./slides-draft/*.html` or `presentation_plan.md` and rebuild. Loop until clean.

### Runtime invariants (set by the canonical `overlay.js` — do not relitigate)

- **CSS isolation**: each slide loads inside its own `<iframe srcdoc>`. Slide fragments may use global selectors (`html`, `body`, `:root`, `h1`, `.slide`, `.col-left`) freely — they only affect that iframe. Do NOT inject slide fragments inline into a shared `<section>` — that was the cascading-breakage regression of 2026-05-12.
- **Bootstrap hooks** injected into each srcdoc:
  - `__slideEntered(i)` — parent calls after enter transition completes; runs entrance + per-slide TL + initialises step protocol at step 0.
  - `__slideExited()` — parent calls before exit; cancels the TL's `{ cancel }` handle and resets entrance items so re-entry restarts cleanly.
  - `__getSlideSteps()` + `__advanceStep(n, dir)` — exposed for the step protocol.
- **Step protocol**: a slide may set `window.__slideSteps = K` and `window.__slideStep = (n, dir) => void`. Parent advances 0..K within the slide before moving on.
- **anime.js v4 quirks** to honour in per-slide timelines:
  - `anim.then(cb)` (NOT `anim.finished.then(cb)` — `.finished` is undefined on `WAAPIAnimation`).
  - `waapi.animate(...)` commits styles by default (`fill: 'forwards'`); reset inline `transform`/`opacity` when starting fresh.
  - When animating SVG, do NOT apply CSS `transform` (scale/translate) to a `<g>` that already has an SVG `transform="translate(...)"` attribute — the CSS transform replaces it. Animate inner shapes (`<circle>`, `<rect>`) with `transform-box: fill-box`, or position via `cx`/`cy`/`x`/`y` and animate inner cores.
- **Footer safe-zone**: 26 px reserved at the bottom of every slide. Author content with `padding-bottom: 38px` (or pad inner columns).
- **Idle animation guideline**: every slide should have at least one subtle idle motion. Mark 2–3 slides per deck as "signature memorable" with a distinctive topic-anchored animation.

**Ask**: nothing (silent build).

**Write**: `./presentation/` (entire bundle, overwritten).

**Exit when**: `validate_bundle.py` exits 0.

---

## Phase 9 — QA preview

**Enter when**: bundle exists and validates.

**Do**:
1. Print the run command:
   ```sh
   cd presentation && python3 run.py
   ```
2. Optionally run a `playwright-cli` screenshot pass:
   ```sh
   playwright-cli open http://127.0.0.1:8000/index.html
   for i in $(seq 0 $((N-1))); do
     playwright-cli press ArrowRight
     playwright-cli screenshot --filename=presentation/qa/slide-$(printf '%02d' $((i+1))).png
   done
   ```
   Inspect the screenshots; surface layout / overflow issues to the user.

**Verbatim ask**:

> Bundle is ready. Run `cd presentation && python3 run.py` and report any visual issues. Use the arrow keys / space to navigate, `G` for grid view, `S` for speaker notes, `F` for fullscreen.

**Exit when**: user is satisfied OR loops back to phase 7.

---

## Phase 10 — Handoff

**Do**:
1. Run the PDF backup (locked decision §23.5):
   ```sh
   slides-grab pdf --slides-dir slides-draft --output presentation/backup.pdf
   ```
   If `slides-grab` is not directly callable, fall back to: open the bundle in a headless browser via playwright-cli and use `playwright-cli pdf --filename presentation/backup.pdf`.
2. Print the final handoff message:

   > **Done.** Your animated deck is at `./presentation/`.
   >
   > - **Run it**: `cd presentation && python3 run.py`
   > - **PDF backup**: `./presentation/backup.pdf`
   > - **Plan**: `./presentation_plan.md`
   > - **Memory**: `./CLAUDE.md` (mirrored at `./AGENTS.md`)
   > - **Re-build**: edit slides in `./slides-draft/` then rerun the build script.

3. Update `CLAUDE.md` + `AGENTS.md`: `## Current phase` → `10 — handoff complete`.

**Exit**: end of workflow.

---

## Resume protocol

When the skill is re-invoked on an existing project:

1. Read `CLAUDE.md`. Locate the `## Current phase` block.
2. If phase ≥ 8 and `./presentation/` exists, ask: "Bundle already exists. Run preview, rebuild, or start a new revision (loops back to phase 7)?"
3. If phase < 8, ask: "Resume from phase `<N>`, or jump to a different phase?"
4. If `CLAUDE.md` is missing, treat as a fresh project — enter phase 0.

The resume question is always two-option-or-text-answer. Never force the user to type an exact phase ID.
