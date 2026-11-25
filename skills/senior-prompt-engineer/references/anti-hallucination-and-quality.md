# Anti-Hallucination & Pre-Delivery Quality

Apply before delivering any result. Accuracy and safety of the final output are
your responsibility (human-in-the-loop).

---

## Reduce hallucinations
1. **Permission to fail (highest impact):** instruct "if it's not in the provided context / you're not sure, say 'I don't know' - do not fabricate."
2. **Ground in sources:** answer only from provided material when facts matter (RAG-style); quote/point to the source.
3. **Constrain output:** "use only data in the given document; do not cite outside numbers; if external data is needed, flag it as a gap."
4. **Confidence scores:** request 0-100 confidence per key claim; re-check anything below ~90; verify high-stakes numbers independently.
5. **Chain of thought / verification step:** have the model reason, then verify its own claims and math.
6. **Use tools/search** for anything time-sensitive or factual - models are frozen at a training cutoff.
7. **Decompose** complex asks so each step is checkable.

## Reduce bias & handle ethics
- Ask for multiple/diverse perspectives; avoid confirmation bias (don't just echo the user's belief).
- Use neutral, inclusive language; check for gender/cultural bias.
- Explicitly ask for ethical concerns/risks on sensitive topics.
- Never paste confidential/private data into external tools; respect privacy.
- Don't present AI output verbatim as original where that matters; paraphrase and cite.

---

## Pre-delivery quality checklist
Before handing over, verify the output against the Spec:
- [ ] Meets the **Goal** and the **success criteria**.
- [ ] Fits the requested **audience, tone, and format** exactly.
- [ ] Honors every **constraint** (length, do-nots, scope).
- [ ] No **fabricated** facts, APIs, libraries, citations, or data.
- [ ] Claims are **verifiable / sourced**; uncertainties flagged.
- [ ] For code: runs, handles edge cases, has loading/empty/error states, no secrets client-side, includes run instructions.
- [ ] For decks: one idea per slide, skimmable, not text-walls.
- [ ] For UI: responsive, accessible, correct theme (dark/light as specified).
- [ ] Assumptions (if any) are **stated** so the user can correct them.
- [ ] Ran a **self-critique** pass and fixed the top issue.

If anything fails, fix it before delivering. If a real gap remains, say so plainly rather than papering over it.
