# Genre notes

Apply on top of the core rules when the user names a genre, or when the source clearly matches one. Keep these short. Do not invent new output sections.

## Marketing / product copy

Goal: clear value, not brochure fog.

- Keep persuasion. Cut empty claims. Every claim needs a number, name, or concrete detail already in the source. Otherwise cut it.
- One primary benefit early. One clear CTA. Multiple CTAs dilute.
- Kill: seamless, end-to-end, best-in-class, AI-powered (say what the AI does), empower, unlock, supercharge, game-changer.
- Contractions are fine if they match the brand voice.
- Sentence limits still apply. Punchy is not the same as vague.

## Technical docs / READMEs / runbooks

Goal: a tired operator cannot misread the step.

- Procedural sections: imperative, max 20 words, condition before command.
- Descriptive sections: max 25 words, no imperative.
- No contractions. Keep "that".
- Warnings: command or condition first, risk second.
- Untouchables stay exact.

## Blog (technical or general)

Goal: readable narrative without AI scaffolding.

- Hook in the first 50 words: problem or surprising fact, not a definition.
- Prefer prose over bullet spam when two or three sentences read better.
- Explain why before a code block. Show a short example when a claim needs proof.
- Delete "In this post we will…" and "In conclusion…".
- Contractions are fine.

## Specs / RFCs / design docs

Goal: precise and testable.

- Prefer must/can over should/may.
- Ambiguous words (fast, lightweight, scalable): demand numbers from the source or flag them in Cuts/Findings.
- Expand acronyms on first use.
- Passive voice is fine when the system is the actor and the object matters: "The request is validated against the schema."
- Structure beats style. Use lists and tables over narrative when requirements must be checked one by one.

## AI-generated text (any genre)

Always on when the source reads like a model default.

- Run the AI-slop kills in `SKILL.md` first.
- Collapse synonym rotation.
- Remove positivity without evidence.
- Prefer stance and specifics over both-sides hedging.
