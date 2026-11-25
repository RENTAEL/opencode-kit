---
name: lh-verification
description: "The base context already says verify before agreeing, reproduce before fixing, and falsify once. This skill is the method behind those rules."
---
The base context already says verify before agreeing, reproduce before
fixing, and falsify once. This skill is the method behind those rules.

## Critical Patterns

### 1. The evidence ladder

Every claim stands on one of these rungs. Know which one, and never phrase a
lower rung as a higher one.

| Rung | What it is | Phrase it as |
|------|------------|--------------|
| 4. Observed | You ran it and watched the actual behavior | "X works ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â I ran it, output was ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦" |
| 3. Tested | An automated check passed | "Tests pass for X" (name them) |
| 2. Read | You read the code and it looks correct | "X should work ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â based on reading ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦" |
| 1. Recalled | Memory / training / pattern-matching | "X is likely ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â I haven't verified" |

Minimum rung to claim "done": **3**, and **4** whenever the change has a runtime
surface you can actually drive. Rung 2 is a hypothesis. Rung 1 is a lead.

### 2. Reproduce before fixing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the four steps

Before touching code to fix a bug:

1. Make the bug happen and capture the failure (error, wrong output, failing test)
2. Form the hypothesis of the cause
3. Apply the fix
4. Make the bug NOT happen using the exact reproduction from step 1

If you can't do step 1, say so explicitly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the "fix" is a hypothesis and must be
labeled as one.

### 3. Falsify once, then quote what survived

The check you expected to pass is weak evidence; the check you feared is
strong. Pick the one designed to **break** the claim ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the edge case, the input
you didn't design for ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and then anchor the report to the specific observable:
the line of output, the test name and count, the HTTP status, the screenshot.
If you can't quote it, you haven't verified it.

### 4. Verification debt is allowed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â silent debt is not

Sometimes verifying fully is too expensive right now. That's a legitimate
tradeoff ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â but it must be declared: "I did X; verified A and B; C is unverified
because ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦". The failure mode is not skipping verification, it's skipping it
silently.

## Resources

- Sibling skills: [lh-decomposition](../lh-decomposition/SKILL.md) (makes steps
  verifiable by construction), [lh-next-step](../lh-next-step/SKILL.md) (uses
  verification results to choose what's next)
