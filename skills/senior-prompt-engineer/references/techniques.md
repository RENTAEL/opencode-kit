# Technique Library

The full toolkit distilled from the source courses and verified against current
best practices (Anthropic, OpenAI, promptingguide.ai, IBM). Pull the right tool
for the job; most strong prompts combine several.

---

## 1. Foundations

- **Garbage in, garbage out.** Output quality is capped by input quality. Fix the prompt first.
- **AI is not search.** Don't type keywords - write instructions. A prompt is a *program in natural language* and a *call to action*.
- **World-building / puzzle pieces.** The model fills unspecified gaps with the statistically most generic guess. The more concrete context you give, the more unique and correct the result. Everyone's AI output looks the same because they under-specify.
- **Steering vs. commanding.** "Summarize this" = commanding (model picks length/style/focus). "As an executive assistant, summarize this transcript in 4 bullets focused on decisions and owners, no filler" = steering. Always steer: specify length, focus, format, tone.
- **Clarity of thought is the meta-skill.** If you can't describe what you want clearly, no technique will save you. Think first, prompt second.

---

## 2. The core prompting techniques

### Zero-shot
No examples, no context - just ask. Fine for simple/creative one-offs; has a low ceiling for anything specific.

### Role / Persona prompting
Assign a specific identity + priorities + experience. This activates a specialized "lens."
- Weak: "You are a financial analyst."
- Strong: "You are a senior financial analyst with 10 years' experience; focus on risks, anomalies, and trends leadership must act on - not just reporting numbers."
Rules: be specific about *experience* not just title; describe what the role *cares about*; match the role to the task and to the audience.

### Few-shot (example-driven)
Show 2-5 labeled examples of input->output to teach the pattern/style/format. Best for consistent formatting, brand voice, classification, and edge cases.
- Use **varied, canonical** examples (not near-duplicates) so the model generalizes instead of copying.
- **Label/name** each example.
- Prefer **real** examples lightly adapted.
- Anthropic guidance: curate a small set of diverse, representative examples rather than dumping every edge case.

### Structured prompting (define the output shape)
Specify the exact format: sections, bullet counts, table columns, JSON schema, character/word limits, per-channel structure. Pair with few-shot for precision. Add per-field **constraints** ("subject line < 50 chars", "tweet < 280 chars").

### Chain of Thought (CoT)
Ask the model to reason step by step before answering. Reduces errors on math, logic, planning, debugging, root-cause. Trigger phrases: "think step by step", "work this out step by step to be sure it's right", "show your reasoning before the final answer." Modern reasoning models do this natively - turn on extended/thinking mode when available. You can also **prescribe the steps** for repeatable processes.

### Tree of Thought (ToT)
Explore multiple reasoning paths in parallel, evaluate, then converge on the best. Good for abstract/creative/complex problems (naming, plotlines, design directions, strategy). Pattern: "Imagine 3 experts each propose an approach, critique each other, discard weak branches, and synthesize the best solution."

### Task decomposition + Prompt chaining
Break a big task into ordered sub-tasks; each step's output feeds the next. Verify each step before moving on. This produces more accurate, controllable results than one mega-prompt and lets you think/steer as you go. Example chain: outline -> expand each section -> convert to final format.

### Meta-prompting
Use the AI to improve the prompt itself, or to generate a tool-specific prompt (e.g. ask a chat model to write an image/diffusion prompt). Also: "Rewrite my request as a senior prompt engineer would, then wait for my go-ahead." Most providers ship a built-in prompt improver.

### Self-evaluation / self-critique
After output, have the model score/critique it against explicit criteria and suggest the single most important fix, then apply it. Tip: for less biased critique, evaluate in a **fresh** context and don't tell it that it wrote the draft ("I wrote this - review it").

### Adversarial / "playoff" ensembling
Generate competing versions from different personas (e.g. engineer vs. PR vs. angry customer), have them critique each other, then merge the best. Leverages the model's strength at editing/critiquing over first-draft writing.

### Interview-style prompting
Instead of guessing all the context, tell the model the goal and ask it to **interview you** one question at a time until it has enough, then produce the result. Surfaces context you'd never have thought to include.

### Iterative refinement
Treat prompting as a conversation, not a one-shot. Refine ("shorter", "more formal", "add an example", "focus only on X"). Iterate, don't restart. When stuck, use the four moves in `frameworks.md` (revisit framework, split into shorter sentences, try analogous phrasing, add constraints).

---

## 3. Constraint / negative prompting (guardrails)

Tell the model what NOT to do and set bounds. Constraints are focus, not limits.
- Length: "under 300 words", "exactly 3 bullets."
- Content: "use only data in the provided report; do not cite external benchmarks; if external data is needed, flag it as a gap."
- Style: "no filler, no slang, don't start with 'Welcome' or 'The team discussed'."
- Scope: "diagnose only; no future recommendations."
Researchers rely heavily on do-not lists - they steer strongly.

---

## 4. Grounding, hallucinations, and honesty

- **Permission to fail:** "If it's not in the provided context, say 'I don't know' - do not make anything up." This is the single biggest hallucination reducer.
- **Confidence scores:** ask for a 0-100 confidence per claim; distrust low scores; verify high-stakes numbers.
- **Grounding:** provide the source material and instruct the model to answer only from it (RAG-style).
- **Tool use / search:** models are frozen at a training cutoff. For anything time-sensitive or factual, instruct it to search the web / use tools, and watch which sources it trusts.
- **Human in the loop:** you own accuracy and bias of the final output.
More in `anti-hallucination-and-quality.md`.

---

## 5. System vs. user prompts; context

- **System prompt** = persistent identity, rules, style (set the persona and guardrails here in API/agent setups).
- **User prompt** = the specific task.
- **Context** = everything else the model can see (history, memory, injected data). 99% of the time the model sees more than your visible prompt. Don't assume memory - repeat/summarize key facts in long or new sessions.
- **Context engineering:** curate tight, relevant, well-ordered context. Don't dump; don't bury the key info; state which source is authoritative.

---

## 6. Parameters (API settings)

- **Temperature** = randomness/determinism. Low (~0-0.3) for facts, code, structured output, classification. High (~0.7-1.0) for brainstorming, varied phrasing, creative work. If output is too random, lower it; too repetitive, raise it.
- Also relevant: top-p, max tokens, stop sequences.

---

## 7. Multimodal prompting

Same principles apply across text, image, audio, video, code. Be explicit about the input modality and the desired output modality. Examples: analyze an uploaded chart/diagram; "write a social post featuring this image"; generate/edit an image from a reference; transcribe + summarize audio. For image/diffusion models, front-load only the elements that matter (they bake in whatever you mention).

---

## 8. Efficiency & phrasing tips (from the courses)

- **Dictate long prompts by voice** - you'll include far more context than you'd type.
- **Emotional / stakes framing** can nudge quality ("take your time", "this is important, be precise") - use sparingly and pair with a confidence-score requirement rather than empty threats.
- **Analogous reframing:** if a direct ask feels flat ("write a marketing plan"), reframe as a story or comparable task to unlock richer output.
- **Save what works:** keep a prompt library of your best Specs and templates; reuse and adapt.

---

## 9. Agents (when building autonomous helpers)

To define an AI agent/persona reliably, specify: **Persona** (role) -> **Context** (situation) -> **Task + interaction rules** (what conversations to support, one step at a time) -> **Stop phrase** (a keyword that ends the loop) -> **Feedback** (summary + improvement areas at the end) -> **References** (any source material it must use). Two useful patterns: a *simulation* agent (role-plays a scenario with you) and an *expert-feedback* agent (critiques your work in a chosen domain).
