---
name: lh-bug-reporting
description: "A finding others can't reproduce doesn't exist yet. Before reporting, shrink it: fewest steps, most specific starting state, one variable at a time removed until removing anything makes the bug vanish. The report carries: numbered steps from a known state ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ E..."
---
## Critical Patterns

### 1. The report IS the reproduction

A finding others can't reproduce doesn't exist yet. Before reporting, shrink
it: fewest steps, most specific starting state, one variable at a time removed
until removing anything makes the bug vanish. The report carries: numbered
steps from a known state ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ EXPECTED vs. ACTUAL (both concrete) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ evidence
(output, screenshot, failing test) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ environment/build ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ frequency (always?
intermittent? ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â say which honestly). A failing automated test is the best
report format there is: it reproduces itself.

### 2. Severity is user impact; priority is the team's call

Keep them separate and be honest in both directions: severity = what happens
to users (data loss > money wrong > blocked flow > wrong-but-recoverable >
cosmetic) ÃƒÆ’Ã¢â‚¬â€ how many hit it. Priority = when the team fixes it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that's a
product decision you INFORM, not one you own. Inflating severity to win
attention burns your credibility exactly like the boy who cried critical;
underplaying it to be agreeable ships data loss. Report the impact, recommend,
let the team decide.

### 3. Route it right: bug, design gap, or improvement

Three different findings, three different owners:

| Finding | Test | Goes to |
|---------|------|---------|
| Bug | Behavior contradicts the spec/contract | [senior-dev](../../../senior-dev/AGENTS.md) with the repro |
| Design gap | The spec never said what happens here (unspecified state/flow) | [ux-ui](../../../ux-ui/AGENTS.md) as a five-states question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not a bug against the dev |
| Improvement | Works as specified, but the spec produces a bad experience | Product conversation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â labeled as opinion, not defect |

Filing a design gap as a dev bug poisons the peer relationship AND fixes
nothing: the dev can't implement an answer nobody has given.

### 4. Blameless language, cause-curious follow-up

The report describes the PRODUCT, never the author: "checkout double-charges
on double-click", not "you forgot to disable the button". When you've read the
code and suspect the cause, offer it as a lead ("looks like the handler isn't
debounced ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â your call"), clearly separated from the observed facts. And for
bugs that made it far (production, release candidate), ask the blameless
question with the dev: what would have caught this earlier? ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the answer is
usually a missing test level or a spec gap, and THAT's the real fix.

### 5. Verify the fix with the original repro ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â then trap it forever

A fix is verified when the EXACT original reproduction no longer reproduces
(not when the code looks right, not when a different path works ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â you saw
it, nothing less). Then sweep the neighbors: the same mistake often lives in
sibling flows (found it in edit? check create and delete). Close the loop with
the regression test that would have caught it, placed at the right level per
[lh-test-design](../lh-test-design/SKILL.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a verified fix without its test is a
bug on layaway.

### 6. Contested findings get evidence, not escalation

"Works on my machine" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ reproduce in a neutral environment, diff the two, the
difference IS the finding. "That's by design" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fine: show the design saying
so; if it does, reroute as improvement (row 3 above); if it doesn't, it's a
design gap (row 2). Disagreement resolves the peer way ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â once, with evidence,
then commit ([peer contract (`senior-dev`)](../../../senior-dev/AGENTS.md)) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and your
finding log stays honest either way.

## Resources

- Sibling skills: [lh-flow-hunting](../lh-flow-hunting/SKILL.md) (where findings come
  from), [lh-test-design](../lh-test-design/SKILL.md) (where confirmed bugs go to
  live as tests)
- The evidence bar for every claim here:
  [generalist/lh-verification](../../../generalist/skills/lh-verification/SKILL.md)
