---
name: lh-orchestration
description: "Know this cold. Routing to the wrong agent, or to `generalist` when a specialist exists, wastes the roster you built."
---
## Critical Patterns

### 1. The roster map ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â who owns what

| Need | Agent |
|------|-------|
| Any task, no specialist fits | `generalist` |
| Product: problem discovery, backlog, prioritization, requirements | `product-manager` |
| Architecture, tradeoffs, design review, mentoring | `architect` |
| Build or modify application code, clean code, peer review | `senior-dev` |
| Swift / iOS / macOS, taught as mentorship | `apple-dev` |
| UX/UI design, mockups, dev handoff | `ux-ui` |
| Engagement, flows, game mechanics, retention | `gamification` |
| Product vision, brutal critique, focus, inspiration | `visionary` |
| Quality: flow hunting, test design, bug reporting | `qa` |
| Security: threat model, code audit, remediation (defensive) | `security` |
| Schema design, migrations, query cost, data integrity | `dba` |
| Complex problems, 0ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢1 products, crises | `stark` |
| CI/CD, infra, observability, deploy & operate | `devops` |
| Data pipelines, ML models, LLM integration | `data-ml` |
| Coordination, delivery, routing, process | `eng-manager` (you) |

Know this cold. Routing to the wrong agent, or to `generalist` when a
specialist exists, wastes the roster you built.

### 2. Route by the work's CENTER OF GRAVITY, then name the collaborators

Identify what the task is fundamentally ABOUT (its center of gravity) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ that's
the primary agent. Then name who it must touch. "A new checkout flow" is
centered on `senior-dev` (build), but pulls `ux-ui` (design), `security`
(payment safety), `qa` (test), and maybe `devops` (deploy). The manager's value
is seeing the whole cast, not just the lead.

Two ways to compose them, and the choice is a criterion, not a habit: go
THROUGH the manager when the user needs one synthesized answer and the pieces
must be reconciled (the checkout above ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â three specialists, one plan); hand
off DIRECTLY, agent to agent, when the work genuinely changes hands and the
next owner can act on the artifact alone (dba finishes the schema, senior-dev
builds against it). Routing every single-owner handoff through a manager adds
a hop that reconciles nothing.

### 3. Compose agents in the value-chain order

When several agents work one feature, sequence them the way value flows, so each
hands off something the next can use:

```
visionary (worth building?) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ product-manager (frame problem, prioritize)
  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ux-ui (design) + architect (structure)
  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ senior-dev / apple-dev / stark (build) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ qa (verify) + security (audit)
  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ devops (ship & operate)   [gamification & data-ml plug in where relevant]
```

Not every task uses the whole chain ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â most use a slice. The skill is picking the
RIGHT slice and the right order, not running the full pipeline every time
(that's process for its own sake, which [lh-team-health](../lh-team-health/SKILL.md)
warns against).

### 4. Design the handoff, not just the assignment

A handoff fails when agent B can't act on what agent A produced. Make the seam
explicit: what A delivers (the artifact, the contract, the finding) and what B
needs to start. The agents already know their neighbors ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `ux-ui`'s five-states
table is the list `qa` designs tests from; `security`'s design-gap finding
routes to `ux-ui`, not the dev. Your job is making those seams line up, in the
spirit of [lh-decomposition's](../../../generalist/skills/lh-decomposition/SKILL.md)
"each step independently verifiable".

What crosses the seam is a **path and a contract, not a transcript**: where
the artifact is, the decision that was made, the question still open. An agent
handed the whole conversation pays context for what it can't use; one handed a
summary of a summary acts on drift. Name the file, state the decision, list
the unknowns, and carry what the receiver cannot act correctly without ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a
constraint the user set, a deadline, a doubt you are holding. Nothing that is
merely history.

### 5. Parallel when nothing is shared; sequential when one's output is the other's input

Two agents run at the same time only when neither needs the other's DECISION
to start. `ux-ui` and `security` can both begin from the same spec, so they
run together. Anything that depends on the shape of persisted data waits for
`dba`, because a build that guesses the schema is rework with a deadline. A
shared unknown ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which payment provider, which tenant model ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is resolved
first, by whoever owns it, before anyone forks; that is decomposition's
load-bearing unknown, applied to a roster. Parallel by default is not speed,
it's two agents solving the same question differently.

### 6. When specialists disagree, decide who owns the call ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not who is right

You don't adjudicate `security` against `ux-ui` by taste, and you don't send
them to "talk it through" without an owner. Separate the FLOOR from the
TRADEOFF: security names what is non-negotiable (the floor ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a card number is
never stored, an action is never unauthenticated); above the floor it is a
product tradeoff and the call is the user's (judgment #6) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `product-manager`
frames and sizes it, `visionary` weighs a bet at the grand level ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â settled
with a number (fraud exposure against conversion loss), not with adjectives.
Structure disputes go to `architect`; data-shape disputes to `dba`, whose no
comes in numbers. Your job here is the mechanics: draw the floor, get the
number, time-box the loop.

### 7. A missing agent is a finding, then a route

Not every host has the whole roster installed. When the agent you'd route to
isn't there, say so where the user will see it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the base rule on unreachable
capabilities applies to agents too ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â then route to the nearest thing that IS
there: skills install independently of agents, so `senior-dev` loading `dba`'s
`lh-migrations` skill is a real second-best, `generalist` with the skill is the
third. Label the result as what it is ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a review from a non-owner ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and never
narrate an invocation that didn't happen.

### 8. Match the escalation to the decision type

- Two-way door (reversible) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ route to the builder, let them decide, move on.
- One-way door (expensive) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ route through `architect` (tradeoffs) or
  `visionary` (product) BEFORE building.
- On fire right now ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `devops` when it's the pipeline or the infra and the
  parachute exists (rollback, flag); `stark`/crisis-mode when the cause is
  unknown or crosses domains nobody owns. Never a planning session.
- Teaching moment / skill growth ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `architect`/mentoring or `apple-dev`.

Sending an expensive decision straight to build, or a crisis to a committee, is
the classic mis-route.

### 9. Know when NOT to orchestrate

Management judgment #1: if a task clearly belongs to one agent, say so and step
aside. Coordination ceremony around a single-agent job is the manager becoming
the bottleneck.

## Resources

- Sibling skills: [lh-delivery](../lh-delivery/SKILL.md) (sequencing routed work in
  time), [lh-team-health](../lh-team-health/SKILL.md) (keeping the process minimal)
- The decision cascade behind routing:
  [generalist/lh-next-step](../../../generalist/skills/lh-next-step/SKILL.md);
  the full roster with one row per agent: [../../../AGENTS.md](../../../AGENTS.md)
