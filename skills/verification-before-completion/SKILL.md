---
name: verification-before-completion
description: "Claiming work is complete without verification is dishonesty, not efficiency."
---
# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ [Run test command] [See: 34/34 pass] "All tests pass"
ÃƒÂ¢Ã‚ÂÃ…â€™ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Write ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Run (pass) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Revert fix ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Run (MUST FAIL) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Restore ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Run (pass)
ÃƒÂ¢Ã‚ÂÃ…â€™ "I've written a regression test" (without red-green verification)
```

**Build:**
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ [Run build] [See: exit 0] "Build passes"
ÃƒÂ¢Ã‚ÂÃ…â€™ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Re-read plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Create checklist ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Verify each ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Report gaps or completion
ÃƒÂ¢Ã‚ÂÃ…â€™ "Tests pass, phase complete"
```

**Agent delegation:**
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Agent reports success ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Check VCS diff ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Verify changes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Report actual state
ÃƒÂ¢Ã‚ÂÃ…â€™ Trust agent report
```

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ redirect ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
