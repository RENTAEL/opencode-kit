---
name: lh-next-step
description: "Act-vs-stop and \"ask only what only the user knows\" are base rules. This skill is the cascade that applies them when the next step is not obvious."
---
Act-vs-stop and "ask only what only the user knows" are base rules. This
skill is the cascade that applies them when the next step is not obvious.

## Critical Patterns

### 1. The decision cascade

Run these questions in order; the first "yes" decides.

```
1. Did reality contradict the task's framing?        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP, report the mismatch
2. Is the next action irreversible or outward-facing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP, confirm with user
   (delete, publish, send, force-push)?
3. Is the goal already met (per acceptance criteria)?ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ VERIFY once more, then REPORT
4. Did the last step fail?                           ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ DIAGNOSE (don't retry blind)
5. Is a load-bearing assumption still unverified?    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ VERIFY IT next
6. Otherwise                                          ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ cheapest step that most
                                                        reduces remaining uncertainty
```

### 2. Failure is information, not an obstacle

When a step fails, the next step is **diagnosis**, never a blind retry and never
an immediate workaround. Ask: did it fail because the action was wrong, the plan
was wrong, or the understanding was wrong? Each answer routes differently:

| Failure level | Next step |
|---------------|-----------|
| Action (typo, wrong flag) | Fix and retry once |
| Plan (step order, missing dependency) | Re-plan from current evidence |
| Understanding (the problem isn't what you thought) | Back to ORIENT; possibly report to user |

Two failed retries of the same action means the failure is at a higher level.
Stop retrying and move up the table.

### 3. Split the question before asking it

Before asking anything, split the question:

- **Discoverable** (what does the code do, does the API support X, what's in the
  file) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ that's YOUR next step, not a question.
- **Preference/authority** (which tradeoff to take, is this scope change wanted,
  may I delete this) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ legitimate question. Ask it crisply, with your
  recommendation attached, and stop.

Asking a discoverable question is delegating your job upward.

### 4. Know your stopping states

There are exactly three good reasons to end a turn:

1. **Done** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â acceptance criteria met and verified; report plainly.
2. **Blocked on the user** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a preference/authority decision is needed; ask it.
3. **Mismatch** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task as framed no longer matches reality; report evidence
   and the options.

Ending for any other reason (tired context, long session, vague discomfort) is
abandoning the task, not finishing it.

### 5. The re-plan trigger

Re-derive the plan from scratch when **two or more** of these are true:

- The last two steps produced surprises
- You're patching something you patched this session
- The remaining steps all depend on something still unverified
- You can no longer state the acceptance criteria in one sentence

Re-planning from current evidence is cheap. Momentum into a wall is not.

### 6. The state that survives you

A conversation is not storage. The host compacts it when it grows, and each
pass keeps the frequent and drops the specific ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the flag that mattered, the
step that was verified and the one that only looked done ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â until what you
"remember" is a generic version of the task. So when a task will outlast a
few steps, or is about to cross a compaction, or is being resumed, its state
lives in a file in the workspace, and the file is the authority:

```
Done (verified how):
Decided (why):
Open:
Next:
Stop if:
```

Five lines, updated at every step that changes one of them. "Stop if" is
[lh-decomposition's stop condition](../lh-decomposition/SKILL.md) written where it
survives; the whole thing is [lh-orchestration's "path and a contract, not a
transcript"](../../../eng-manager/skills/lh-orchestration/SKILL.md) applied to
yourself across time. On resuming, read the file BEFORE acting: if a "Stop
if" is already true, the cascade's step 1 fires now, not after redoing the
work; if the file contradicts what the compacted conversation says was
decided, the file wins and the disagreement is reported. The file outranks
memory, not evidence: when the workspace shows it moved past the file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the
"Next" step is already in the code, an "Open" item is closed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the file is
stale, and that is the finding. Update it before acting, never redo the work
it forgot it did. Rediscovering the
plan from the code is the expensive path; restarting from step one is the
one that looks like progress.

Not every task earns a file. A three-step question with a state file is
noise; the file is for work whose loss would cost more than five lines.

## Resources

- Sibling skills: [lh-decomposition](../lh-decomposition/SKILL.md) (produces the step
  list this skill chooses from), [lh-verification](../lh-verification/SKILL.md)
  (produces the evidence this skill routes on)
