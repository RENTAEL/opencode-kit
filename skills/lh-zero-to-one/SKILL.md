---
name: lh-zero-to-one
description: "Before building anything, name the assumption that kills the product if false, and test it with the cheapest experiment that can ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the method (ranking assumptions by \"how dead is the idea if this is false\", fake doors, concierge versions, five-person prototype..."
---
## Critical Patterns

### 1. Kill the riskiest assumption first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and it's usually not technical

Before building anything, name the assumption that kills the product if
false, and test it with the cheapest experiment that can ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the method
(ranking assumptions by "how dead is the idea if this is false", fake doors,
concierge versions, five-person prototypes) lives in
[product-manager's `lh-discovery`](../../../product-manager/skills/lh-discovery/SKILL.md)
and is not restated here. The builder's half is the part that bites builders:
the riskiest assumption is rarely "can we build it" (you can) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's "will
anyone want it", "does the data exist", "will the third party allow it" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and
building the whole machine to test the first domino is the classic 0ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢1 death.
Know what result of that test means STOP rather than iterate, and write it
down before running it.

### 2. Walking skeleton: end-to-end ugly beats half-built pretty

First construction milestone is always the thinnest possible END-TO-END slice:
real input ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ real processing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ real output, everything hardcoded that can be.
One screen, one path, real data flowing. A walking skeleton finds the
integration surprises (auth, deploys, data shape, the API that lies) in week
one, while a beautifully-layered half-build finds them the week before launch.
Then every iteration thickens the skeleton ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's always shippable, just
increasingly less embarrassing.

### 3. Spend your innovation tokens on ONE thing

Everything that isn't your product's differentiator gets the most boring,
known, hosted option available (auth, payments, DB, hosting: solved problems
ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â buy, don't build). Novelty budget goes entirely to the thing users come
FOR. A startup dying with a brilliant custom infrastructure and a mediocre
product is the most preventable death in engineering ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and the most common.

### 4. The MVP cut: one loop, whole and lovable

Scope v1 to the product's ONE core loop (per the visionary's
[one-sentence rule (`lh-brutal-critique`)](../../../visionary/skills/lh-brutal-critique/SKILL.md)):
the user can complete the core action, feel the value, and come back ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â with
empty/error states designed ([five states (`lh-ux-flows`)](../../../ux-ui/skills/lh-ux-flows/SKILL.md)
still apply; minimum is not a synonym for broken). Everything else ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â settings,
admin, the second persona, integrations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â goes to the parking lot with names
attached. The cut itself follows [visionary/lh-focus](../../../visionary/skills/lh-focus/SKILL.md)
#4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â scope first, quality never ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and when the cut is contested, route it there.

### 5. Promotion is a conversation, not a moment the demo worked

Judgment #5 says the rules change by phase; this is the transition nobody
schedules. The crime is silent promotion: the demo that becomes production
because the demo worked. When a prototype graduates, hold the explicit
conversation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what gets rewritten (usually: auth, data layer, error
handling), what gets tests ([qa](../../../qa/AGENTS.md) enters here), what
keeps its debt with a note ([lh-code-health](../../../senior-dev/skills/lh-code-health/SKILL.md)
owns the note). Two one-way doors hide in a v1 and both get their owners
before promotion: the schema underneath it is [dba](../../../dba/AGENTS.md)'s
call (a prototype's table becomes production's model by accident), and the
security floor ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PII, secrets, authorization ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is
[security](../../../security/AGENTS.md)'s, because "we'll threat-model later"
is the sentence before the breach. Ask where the real data will live: a prototype keeps its
data beside its code, and promotion is the day personal data starts landing
in the repository. Budget rule of thumb: promotion costs
about as much as the prototype did ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â plan for it or plan to pay triple later.

### 6. Instrument from day one ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â v1's job is to LEARN

A v1 without telemetry is a message in a bottle. Before launch, wire the
minimum: did they reach the core action? complete it? return? where did they
drop? (activation + retention, per
[gamification/lh-engagement](../../../gamification/skills/lh-engagement/SKILL.md)).
Plus the parachutes: feature flags on anything risky, one-command rollback,
backups restored-once-to-prove-it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the machinery is
[devops](../../../devops/AGENTS.md)'s to build, the doctrine is judgment #6.
The whole point of shipping early is the learning, so don't ship blind.

## Resources

- Sibling skills: [lh-first-principles](../lh-first-principles/SKILL.md) (when the
  0ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢1 hits a wall), [lh-crisis-mode](../lh-crisis-mode/SKILL.md) (launch day
  surprises)
- Handoffs as it matures: [senior-dev](../../../senior-dev/AGENTS.md) (the
  living codebase), [architect/lh-tradeoffs](../../../architect/skills/lh-tradeoffs/SKILL.md)
  (the one-way doors met along the way)
