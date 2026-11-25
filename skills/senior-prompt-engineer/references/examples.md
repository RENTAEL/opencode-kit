# Before -> After: Prompt Transformations

Concrete demonstrations of turning a raw request into a senior-level Spec, one
per domain. Use these as canonical few-shot references when transforming prompts.

---

## General (email)
**Raw:** "write an email about a project delay"
**Spec:**
> ROLE: You are a project manager with strong stakeholder communication skills.
> GOAL: Inform a senior exec the deadline is unachievable and keep their trust. Success = clear, calm, solution-oriented, no defensiveness.
> CONTEXT: Unforeseen technical delays hit a key dependency; audience is a busy VP who wants the point fast.
> METHOD: Lead with the revised date, then cause, then plan.
> OUTPUT: Email; subject line; < 200 words; scannable.
> CONSTRAINTS: Professional, accountable, no jargon; propose a revised timeline + next steps; don't over-apologize; don't use "limited access" filler.

---

## App building
**Raw:** "build me a to-do app"
**Spec:**
> ROLE: Senior full-stack engineer who ships clean, maintainable MVPs.
> GOAL: A working to-do app a solo user can actually use. Success = add/edit/complete/delete tasks persist across reloads; responsive; no console errors.
> CONTEXT: Personal productivity; single user; no backend required.
> INPUTS: Stack = HTML/CSS/JS (or React if preferred); localStorage for persistence.
> METHOD: Scaffold -> data layer -> CRUD -> UI -> empty/loading/error states -> polish.
> OUTPUT: Runnable files + run instructions; modular code; comments on non-obvious logic.
> CONSTRAINTS: Accessible, mobile-first, input validation, no invented libraries; dark theme unless told otherwise (ASSUMPTION - confirm).

---

## Website / landing page
**Raw:** "make a landing page for my startup"
**Spec:**
> ROLE: Senior conversion-focused web designer/developer.
> GOAL: Landing page that drives <primary CTA>. Success = clear hook, single obvious CTA, mobile-perfect.
> CONTEXT: <product, audience, brand voice, colors/logo>.
> INPUTS: Reference sites: <links>; assets: <logo/images>.
> OUTPUT: Sections = hero (hook + subhead + CTA), value props, social proof, features, FAQ, footer; semantic responsive HTML/CSS.
> CONSTRAINTS: Minimal modern style; accessible (contrast, alt text); lightweight; meta title/description.
> METHOD: Offer 3 distinct visual directions before building.

---

## UI / UX
**Raw:** "design a dashboard"
**Spec:**
> ROLE: Senior product designer.
> GOAL: Dashboard for <user> to <primary task> at a glance.
> CONTEXT/INPUTS: Key metrics = <list>; brand = <palette/type>; reference = <product>.
> OUTPUT: Layout with clear hierarchy (what to see first); components; states (loading/empty/error); responsive breakpoints.
> CONSTRAINTS: Clean/minimal; specify dark or light (ASK if unknown); WCAG contrast; keyboard + focus states.

---

## Presentation
**Raw:** "make a deck about our Q3 results"
**Spec:**
> ROLE: Executive communications designer.
> GOAL: Get leadership to <decision/action> from Q3 results.
> CONTEXT: Audience = execs, 10 min slot; data = <source>.
> OUTPUT: ~8 slides; one idea per slide; headline = the takeaway; visuals/charts over paragraphs; speaker notes carry detail; .pptx, 16:9.
> CONSTRAINTS: Skimmable; no text-walls; sourced numbers; brand theme <colors/fonts>.
> METHOD: Narrative arc = hook -> results -> insight -> implication -> ask.

---

## Research
**Raw:** "tell me about the EV market"
**Spec:**
> ROLE: Market research analyst.
> GOAL: Decision-useful view of <EV market, region, 2023-2025>.
> METHOD: Use live search; break costs/TCO down step by step; surface non-obvious/contrarian insights.
> OUTPUT: Exec summary + sections OR comparison table; confidence flags; cited sources.
> CONSTRAINTS: Fact vs. inference labeled; flag gaps; no fabrication.

---

## Pattern to copy
For any raw request: pick the domain, run the Gap Finder, fill ROLE / GOAL+success / CONTEXT / INPUTS / METHOD / OUTPUT / CONSTRAINTS (+ ASSUMPTIONS or clarifying questions), then execute and self-check.
