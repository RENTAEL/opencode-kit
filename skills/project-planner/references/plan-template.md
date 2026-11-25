# PLAN.md Template

Fill this structure exactly. Everything in `[brackets]` gets replaced; section headers stay as-is so the format is predictable across projects.

```markdown
# [Project Name]

[One or two sentence description of what this is and who it's for.]

## Problem & Success Criteria

**Problem:** [What's broken/missing that this solves.]
**Success criteria:** [Concrete, checkable definition of "this works." Not vibes — a specific observable outcome.]
**Explicit non-goals:** [What this is deliberately NOT trying to do, to keep scope honest.]

## Constraints (locked in during grilling)

| Constraint | Value |
|---|---|
| Scale/users | [...] |
| Deployment target | [...] |
| Budget | [...] |
| Timeline | [...] |
| Team | [solo / team size] + [skill level with chosen stack] |
| Data/compliance | [...] |

## Research Summary

[3-6 bullets: what the research phase found. Dominant architecture patterns for this problem class, what production teams are actually using right now, and the top 1-2 failure modes to design around from the start.]

## Tech Stack Decision

For each major component:

**[Component, e.g. "Backend framework"]:** [Chosen tool]
- Rejected: [Alternative] — [why it lost, one sentence]
- Rejected: [Alternative] — [why it lost, one sentence]
- Why this one: [one to two sentences, grounded in the constraints table above, not just "it's popular"]

[Repeat for each major stack decision: language/runtime, framework, database, deployment/infra, key libraries for anything non-trivial like auth, LLM integration, etc.]

## Architecture Overview

[Plain-language description of how the pieces fit together and the data/control flow between them. Use a simple text diagram or Mermaid block if it clarifies more than prose would — don't force one if the architecture is simple enough to describe in 3 sentences.]

## Phases

Each phase below depends ONLY on earlier phases, never later ones. Each is independently runnable and testable before moving to the next. Each phase section is written to stand alone — if you split this file into separate issues, each section has everything needed on its own.

---

### Phase 1: [Name]

**Depends on:** None (starting point)
**Goal:** [What this phase produces — a concrete, observable artifact or capability, not "set things up."]

**Tasks:**
1. [Concrete task]
2. [Concrete task]
3. [...]

**Starter code:**

\`\`\`[language]
// [file path this belongs in]
// [minimal real setup/imports — this part is complete and correct]

// Why this approach: [brief note on why this pattern/tool was chosen over alternatives, grounded in research]

function [meaningfulName](...) {
  // TODO: [what needs to happen here]
  // Hint: [the approach/algorithm/API to look at, not the answer itself]
  // Learn: [pointer to the specific docs page, concept, or reference the user should read to implement this]
}
\`\`\`

**Definition of Done (verify before moving on):**
1. Run: `[exact command]`
2. Expected result: [specific, observable — an output value, a status code, a file that exists, a log line]
3. If it doesn't match: [what to check first]. Fix, rerun, repeat until the expected result actually happens — don't move to Phase 2 on a guess that it probably works.

**Watch out for:** [1-2 pitfalls specifically relevant to this phase, pulled from research]

---

### Phase 2: [Name]

**Depends on:** Phase 1
[... same structure ...]

---

[Continue for all phases. Typical projects land somewhere between 4 and 10 phases — resist cramming multiple independently-testable units into one phase just to shorten the list, and resist splitting a single cohesive unit of work into artificially many phases.]

## Splitting into issues

Each phase above is written to be copy-pasted as a standalone issue/ticket. When starting implementation:
1. Copy one "### Phase N" section as the issue body.
2. Title it `[Phase N] [Name]`.
3. Note the dependency line in the issue so whatever tracker is in use can sequence them correctly.
4. Work phase by phase, verifying the Definition of Done before opening the next issue.

## Alternatives Considered

[Any architecture-level alternative that was seriously considered and rejected outright, not just per-component tool choices already covered above — e.g. "considered a different overall approach (X) instead of the chosen approach (Y)" — with the reasoning for the whole-project direction chosen.]
```

## Notes on filling this in

- The Tech Stack Decision section must include what was **rejected** and why — a plan that only states the winner without the tradeoff reasoning is not useful when the user hits a wall later and wonders whether they should've chosen differently.
- Definition of Done sections need a real command and a real expected output, specific to that project — never a generic "write tests for this."
- Code blocks are stubs. If a phase doesn't naturally need a code stub (e.g., a pure infra/setup phase), it's fine to omit the code block and keep the Tasks + Definition of Done.
