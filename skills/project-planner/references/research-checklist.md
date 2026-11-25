# Research Checklist

Use this when the domain is unfamiliar or you're not confident you'd naturally cover all the high-leverage angles. Skip categories that genuinely don't apply — don't pad searches for the sake of hitting a number.

## 1. Prior art
- "[problem] open source project"
- "[problem] github" — look at what real repos actually chose, not just what they claim in the README
- "how does [comparable product] work" for any commercial equivalent

## 2. Architecture patterns
- "[domain] architecture patterns 2026"
- Identify the 2–3 dominant approaches. For each: what it optimizes for, what it costs you (complexity, latency, ops burden).
- If the project touches LLMs/ML: check current patterns for the specific sub-problem (e.g. RAG pipeline design, agent orchestration, fine-tuning vs prompting vs retrieval) rather than generic "AI architecture."

## 3. Current tooling landscape
- "[category] best tools 2026" and cross-check against "[tool A] vs [tool B]"
- Check for version-specific breaking changes or deprecations — a tool that was standard 18 months ago may have a new canonical successor.
- For anything cloud/infra related: check current pricing tiers and free-tier limits, not assumed ones — they change.

## 4. Failure modes and postmortems — the highest-leverage category
- "[tool/pattern] postmortem"
- "[tool/pattern] common mistakes"
- "[tool/pattern] at scale problems"
- "why not to use [tool]" — read the strongest counterarguments, not just marketing
- This category is what turns a plan from "looks right" into "actually survives contact with reality." Never skip it.

## 5. Benchmarks and comparisons
- When 2+ tools are viable for the same job, find a head-to-head: "[tool A] vs [tool B] benchmark"
- Prefer independent benchmarks and engineering blog posts over vendor comparison pages.

## 6. Constraints specific to the user's likely context
- If the user's history/preferences suggest DevOps/Cloud/MLOps interest, don't force those angles onto every project — but if the project naturally touches infra, deployment, or automation, research the current standard there specifically (e.g. current IaC tooling, container orchestration norms, CI/CD patterns) rather than defaulting to generic advice.

## Synthesis, not transcription
After research, you should be able to state, for each major decision point: the 2–3 real options, the tradeoff between them, and which one production teams are actually converging on right now — with a one-sentence reason. If you can't state that, the research isn't done yet.
