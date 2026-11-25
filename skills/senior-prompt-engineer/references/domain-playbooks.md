# Domain Playbooks

What a **senior-level Spec must contain** for each domain the user builds in.
When a request lands in one of these domains, make sure the Spec covers the
checklist. When a mistake recurs in a domain, add/adjust rules here (and in
LEARNINGS.md) so the default improves permanently.

---

## App building
Spec must define:
- **Users & core jobs:** who uses it, top 3-5 user tasks, primary user flow.
- **Feature list, scoped:** MVP vs. later; explicitly out-of-scope items.
- **Tech stack:** language/framework, state management, storage/DB, auth, hosting; or "recommend a stack and justify."
- **Data model:** key entities, fields, relationships; persistence (local vs. server).
- **Architecture:** components/modules, file structure, separation of concerns.
- **UI/UX:** see the UI/UX playbook below; responsive by default.
- **Non-functionals:** accessibility, performance, error handling, empty/loading/error states, security (no secrets in client, input validation).
- **Quality bar:** clean modular code, comments where non-obvious, no invented libraries/APIs, runnable, with setup/run instructions.
- **Acceptance criteria:** what "works" means (features actually function, not just render).
Always decompose: scaffold -> data layer -> core features -> UI -> states/polish. Verify each step.

## Websites / landing pages
Spec must define:
- **Goal & primary CTA:** what the visitor should do; conversion intent.
- **Audience & brand:** voice, colors, logo, existing assets or design language.
- **Sections:** hero (hook + subhead + CTA), value props, social proof, features, pricing, FAQ, footer - only those that fit the goal.
- **Design direction:** style (minimal, bold, editorial...), typography, spacing, imagery; reference sites if any.
- **Responsiveness & accessibility:** mobile-first, semantic HTML, alt text, contrast.
- **Performance & SEO:** lightweight assets, meta title/description, headings hierarchy.
- **Constraints:** frameworks allowed, length, tone, must-nots.
Offer 2-3 distinct visual directions for anything subjective before committing (ToT).

## UI / UX design
Spec must define:
- **Users, context, and the primary task** the design serves.
- **Design system:** color palette (state light/dark default explicitly), typography scale, spacing, components, iconography.
- **Layout & hierarchy:** what the eye should hit first; information density.
- **Interaction & states:** hover/active/focus, loading/empty/error/success, transitions/micro-interactions.
- **Accessibility:** contrast ratios, keyboard nav, focus states, ARIA where needed, touch targets.
- **Responsiveness:** breakpoints and behavior.
- **References:** example screens or products to echo the vibe.
Default to clean, modern, minimal; be specific about theme (do not guess light vs. dark - ask or state the assumption).

## Presentations / slides
Spec must define:
- **Audience & objective:** who's in the room, the one decision/action you want.
- **Narrative arc:** hook -> problem -> insight -> solution -> proof -> ask.
- **Slide count & per-slide structure:** one idea per slide; headline as the takeaway; supporting points minimal.
- **Density rule:** concise bullets or visuals, NOT paragraphs; speaker notes carry detail.
- **Visual style:** template/theme, colors, fonts, chart style, imagery.
- **Data:** which numbers, sourced; charts over tables where clearer.
- **Format:** file type (.pptx/Slides/HTML), aspect ratio, length.
Common failure to avoid: text-heavy slides. Default to visual, skimmable, one-idea-per-slide.

## Code / refactoring
Spec must define:
- **Exact task & scope:** file(s)/functions in scope; what not to touch.
- **Language/version, style guide, dependencies allowed.**
- **Behavior contract:** inputs, outputs, edge cases, error handling.
- **Constraints:** performance, security, no fabricated APIs, match existing patterns.
- **Verification:** tests to run/write; example I/O; "explain reasoning for non-trivial logic."
Use chain-of-thought for debugging (read code -> locate fault -> explain cause -> fix -> verify). Decompose large changes.

## Research / analysis
Spec must define:
- **Precise question & scope** (time range, geography, segment).
- **Sources & recency:** require citations; use live search for anything time-sensitive; note the training-cutoff risk.
- **Depth & angle:** ask for non-obvious/contrarian insights, not just the obvious; break TCO/cost breakdowns down step by step.
- **Output format:** exec summary + structured sections or comparison table + confidence flags.
- **Guardrails:** distinguish fact vs. inference; flag gaps; no fabrication.

## Data analysis
Spec must define:
- **The dataset & privacy** (never paste sensitive/confidential data into external tools).
- **The question / hypothesis** and the metrics that answer it.
- **Method:** cleaning steps, transformations, which analysis/chart.
- **Output:** tables/pivots/charts + a short plain-language insight (context -> insight -> impact).
- **Guardrails:** state assumptions, show the steps, don't over-claim correlation as causation.
