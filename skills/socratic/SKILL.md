---
name: socratic
description: "caller passes:"
---
# socratic ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â parameterized intent gate

## CALLER CONTRACT

caller passes:

1. **mode-decision space** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mode names skill may return. e.g. `{file}`; `{NEW, DISTILL, BACKPROP, AMEND}`.
2. **convergence triple per mode** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `mode ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ required facts`. e.g. `BACKPROP ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {symptom, surface, recurrence-class}`; `AMEND ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {Ãƒâ€šÃ‚Â§-target, delta}`.
3. **intent string** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user's free-form input (typically `$ARGUMENTS`).

skill returns `(converged-mode, facts)` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â data only; not file, not commit, not write artifact. skill owns question selection, convergence check, escape hatch, teach overlay. caller owns draft, file-write, git ops, root-cause analysis. skill not know caller's artifact shape ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â checks fact presence per triple, not meaning.

## LOOP

1. ask 1 question
2. wait for answer
3. pick next question from pool or converge
4. converge ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ return `(mode, facts)`

every turn: 1 question. not batched. not checklist tone. not re-ask facts already supplied.

## QUESTION POOL

|category|fires when|shape|
|clarify|symptom vague|"what specifically ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â input ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ observed vs expected?"|
|scope|ask epic-shaped|"smallest change that removes the pain?"|
|boundary|unclear what stays untouched|"what works today that must keep working?"|
|success|no acceptance criterion|"how do we know it's fixed without re-asking you?"|
|frame|user names fix, not problem|"is that the problem, or your current guess at the solution?"|
|first-principle|mode NEW and no foundational claim stated|"name ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 1 foundational claim other invariants derive from ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what is this artifact, fundamentally?"|

pick by what's most missing.

NEW mode: fire first-principle probe explicitly, once ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not buried under clarify. user may decline ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ converge on remaining triple facts. record `first-principle-asked` in returned facts regardless of answer.

## TONE

interrogate problem, not user. probe statement, not judgment. not "are you sure?" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "what would falsify this?"

## CODE READS

reactive only. not grep repo pre-questions to "find the bug" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â undermines dialogue, duplicates caller's investigation. user cites `file:line`/symbol/path ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ read that target. user claims breakage w/o data ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ spot-check before next question.

shape: "looking at `<file>:<line>`, [observable fact] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â given that, [next question]". model verifies, user diagnoses. ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 2 reads/turn; broader sweep needed ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ stop dialogue, return control to caller.

## TEACH

overlay, not phase. answer reveals gap ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ surface distinction in 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“2 sentences, then next question. not lecture.

|trigger|distinction|
|fix named as problem|symptom vs cause vs solution|
|unfalsifiable success crit|verifiable = observable + bounded|
|scope conflated w/ ambition|smallest-change seam vs total redesign|
|breakage assumed w/o data|observed vs expected vs assumed|

## CONVERGENCE

converged iff some mode's triple fully present in dialogue history. ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 3 turns w/o convergence ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ offer escape: "enough for rough draft ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â return now and refine downstream, or keep going?"

## ESCAPE HATCH

"just file it" / "skip the questions" / "I know what I want" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ stop dialogue, not bypass gate: audit facts vs triples. gaps ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask once for missing piece or return `(mode, partial-facts)` + explicit `unmet-criteria` list so caller surfaces gaps in artifact (e.g. `## Unresolved` callout). gaps stay visible; user's "done thinking" honored.