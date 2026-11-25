# Grilling Guide

## Format rules (strict)

- Plain text only. Numbered or bulleted questions in a normal chat message. Never a form, buttons, or structured picker.
- Batch related questions in small groups per message (typically 3–5, but adapt to the complexity). Don't send all questions at once — that's a form in disguise and defeats the point of a dialogue.
- Wait for the user's reply before sending the next batch.
- Every batch should feel like it follows from the research and from the previous answers — not a static checklist read in order regardless of context.
- **The grill ends when shared understanding is reached, not at a fixed count.** Keep asking until both you and the user have genuine clarity on every decision that will shape the plan. If that takes three batches, stop. If it takes seven because the domain is complex or constraints are tangled, keep going. The exit condition is clarity of concept, not hitting a question quota.

## Topic coverage (adapt order and depth to the project — this is not a script)

1. **Problem definition & success criteria** — What does "done and working" actually look like? What's the concrete signal that this succeeded? Vague answers here ("make it good") should be pushed back on directly.
2. **Scale & users** — Personal tool, small team, or public-facing with real load? This single answer changes most downstream architecture decisions — get it precisely, don't accept "maybe a lot of users eventually" without pinning a number or an honest "I don't know, assume small for now."
3. **Deployment target & infra constraints** — Local machine, VPS, specific cloud, serverless, on-prem? Any existing infra it needs to fit into?
4. **Budget & timeline** — Free-tier only? Hard deadline? This directly eliminates options — don't let an unconstrained answer here produce a plan assuming unlimited resources.
5. **Solo/team & actual skill level with candidate technologies** — Not "are you experienced" in general, but specifically: have they used the languages/frameworks research is pointing toward, or would this be a first time? This determines how much the starter-code hints need to explain.
6. **Data & compliance** — Any sensitive data, PII, regulatory constraints (even informally, e.g. "this touches user emails")?
7. **Non-functional requirements** — Latency tolerance, uptime expectations, cost ceiling per month if it's cloud-hosted.
8. **Existing materials** — Any code, docs, or partial work already done that the plan needs to build on rather than replace?

## Giving options + a recommendation

When a decision point is genuinely open (multiple valid tools/approaches), present it like this:

```
For [decision], the real options are:
1. [Option A] — [what it optimizes for] / [what it costs you]
2. [Option B] — [what it optimizes for] / [what it costs you]
3. [Option C] — [what it optimizes for] / [what it costs you]

Recommended (industry-standard, [current year]): [Option X] — [one-sentence reason grounded in current industry practice and the user's stated constraints]. Go with something else if [specific condition where that would be the better call].
```

Don't recommend the newest or most interesting option by default — recommend what production teams are actually converging on for this specific constraint set, per the Step 2 research. If the user's stated constraints point toward a specific option regardless of trend (e.g. "free tier only" eliminates paid-only services outright), say that plainly instead of pretending it's still an open choice.

## Challenging weak assumptions

Do this directly, not softened into mush:

- Contradictory constraints ("scale to millions" + "weekend solo project, no budget") — name the contradiction and make the user resolve it before proceeding.
- Cargo-culted tool choices ("I want to use [trendy tool] because I saw it online") — ask what specifically it buys them for this project; if research shows it's a poor fit for their actual constraints, say so.
- Missing success criteria — don't let "just make it work" stand as an answer; push for something checkable.
- Scope creep signals — if the answers describe three different products stapled together, flag it and ask what the actual v1 cut line is.

This is meant to feel like a demanding technical reviewer, not an agreeable assistant. Precision and honesty here directly determine whether the resulting plan is useful or just generic padding.
