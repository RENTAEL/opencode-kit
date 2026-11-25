---
name: lh-crisis-mode
description: "rules applied to normal work just institutionalizes panic"
---
## When to Use

- Production is down, degraded, or doing something scary to data
- The demo/launch/deadline is hours away and something critical broke
- A "quick fix" cascade has made things worse and heads are hot
- NOT for regular bugs with no clock running ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that's normal work; crisis
  rules applied to normal work just institutionalizes panic

## Critical Patterns

### 1. Stabilize first, understand later

In a crisis the first move is almost never the root-cause fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's the
TOURNIQUET: rollback, feature-flag off, failover, rate-limit, static page.
Ask "what's the fastest way to stop the bleeding?" separately from "what
happened?" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mixing them costs users while you satisfy curiosity. Root cause
is tomorrow's luxury; today has one KPI: minutes of impact. (Exception: if
the tourniquet could destroy evidence or data, snapshot FIRST ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â thirty
seconds of copying beats a week of forensic archaeology.)

### 2. Triage by blast radius, ruthlessly

Three questions, in order: Is data being lost or corrupted? (stop THAT above
all ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â downtime is recoverable, corruption compounds.) Who is affected and how
badly? Is it spreading? Fix ordering follows blast radius, not annoyance,
not whoever shouts loudest, not what's intellectually interesting. Say what
you're explicitly NOT doing yet, so the queue is a decision instead of an
accident. Two roles exist from minute one, even if one person holds both: the
lead who decides, and the voice who tells stakeholders ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â on a fixed cadence ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
what is known, what isn't, and what happens next; silence reads as chaos. And
if the incident is a BREACH, the tourniquet competes with evidence
preservation and disclosure duties: snapshot first, then
[security](../../../security/AGENTS.md) owns the timeline and the disclosure
clock, and you own keeping the service alive around it.

### 3. One change at a time, everything written down

Panic-shotgunning (restart + config change + deploy + cache flush,
simultaneously) guarantees you won't know what worked ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and usually adds a
second incident to the first. Under MAXIMUM pressure the discipline gets
MORE strict, not less: one hypothesis ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ one change ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ observe ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ log it with a
timestamp (a running note: what we saw, what we tried, what happened). The
log keeps the room honest, onboards helpers in one read, and writes the
postmortem for free. This is
[co-debugging](../../../senior-dev/skills/lh-pairing/SKILL.md) at 2x speed, not
a different sport.

### 4. The demo-tomorrow variant: shrink the surface, don't heroize the fix

When the clock is a demo, not an outage: cut scope to what MUST work, walk
that path end-to-end three times, and freeze everything else (no drive-by
fixes after the last full walkthrough ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the untested improvement at 2am is
how demos die). Prepare the fallback deliberately: recorded run, canned data,
a "here's what I'd show" narrative. A smaller demo that works beats a full
demo that might ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the audience remembers the crash, never the missing
feature.

### 5. Crisis authority is borrowed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â spend it honestly

Incidents suspend the normal peer ceremony: someone (you, if you're leading)
makes fast calls without consensus, and that's correct ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â FOR the duration.
The debt gets repaid after: decisions taken under fire are re-reviewed in
daylight ([one-way doors (`lh-tradeoffs`)](../../../architect/skills/lh-tradeoffs/SKILL.md) that
got jumped get their analysis retroactively), hacks get DEBT-tagged
([lh-code-health](../../../senior-dev/skills/lh-code-health/SKILL.md)), and the
temporary dictatorship ends when the fire does. A team where every day is an
emergency has a leadership problem wearing an engineering costume.

### 6. The postmortem is the payment for the incident

Blameless, mechanism-focused, within days while memory is fresh: timeline
(from the log you kept), root cause chain (keep asking "and why was THAT
possible?" past the human to the system ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a person "being careless" is never
a root cause, a missing guardrail is), impact honestly stated, and 2-3
prevention actions that actually get owners and dates. Then the
[qa](../../../qa/AGENTS.md) question: what test/alert/limit would have caught
this earlier? An incident you fully paid for makes the system stronger;
an unexamined one is a rerun with a bigger audience.

## Resources

- Sibling skills: [lh-first-principles](../lh-first-principles/SKILL.md) (when the
  diagnosis resists), [lh-zero-to-one](../lh-zero-to-one/SKILL.md) (the parachutes
  that make crises survivable are installed there)
- Failure routing outside crises: [generalist/lh-next-step](../../../generalist/skills/lh-next-step/SKILL.md)
- The machinery this skill relies on ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rollback, flags, alerts, SLOs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is
  built and owned by [devops](../../../devops/AGENTS.md); this skill flies the
  plane, that agent installed the parachutes
