---
name: backprop
description: "Plan-then-execute fixes code, forgets. SDD fixes code AND edits spec so recurrence impossible. That edit = backprop."
---
# backprop ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bug ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ spec

Plan-then-execute fixes code, forgets. SDD fixes code AND edits spec so recurrence impossible. That edit = backprop.

Analysis protocol ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â writes nothing itself (read-only grants). Consumers: spec skill BACKPROP mode (records Ãƒâ€šÃ‚Â§B/Ãƒâ€šÃ‚Â§V, commits SPEC.md) + build skill resume (test + fix, commits code). See HANDOFF.

## WHEN

- Test fail at build skill verification.
- User bug report.
- Post-mortem after production incident.
- Check skill flags VIOLATE w/ root cause found.

## THREE STEPS

1. **TRACE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read failure output / report. Find exact file:line of wrong behavior. Name root cause, one telegraph sentence.
2. **ANALYZE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â three questions: new Ãƒâ€šÃ‚Â§V catches bug class? (most common: yes). Ãƒâ€šÃ‚Â§I wrong ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â spec claims shape code can't deliver? (sometimes). Ãƒâ€šÃ‚Â§T wrong ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â built wrong thing? (rare but real).
3. **PROPOSE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â draft spec change. Never skip Ãƒâ€šÃ‚Â§B; Ãƒâ€šÃ‚Â§V/Ãƒâ€šÃ‚Â§I/Ãƒâ€šÃ‚Â§T case-by-case.
   ```
   Ãƒâ€šÃ‚Â§B row: B<next>|<date>|<root cause>|V<N>
   Ãƒâ€šÃ‚Â§V line: V<N>: <testable rule that would have caught it>
   ```

## HANDOFF ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â two commits, cross-cited

Protocol output = drafted delta. Writes split per write-ownership (spec = sole SPEC.md mutator; build = code writer):

1. **Spec commit** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â spec skill BACKPROP mode applies Ãƒâ€šÃ‚Â§B (+ Ãƒâ€šÃ‚Â§V, Ãƒâ€šÃ‚Â§T) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ auto-commit `backprop Ãƒâ€šÃ‚Â§B.<n>(+) + Ãƒâ€šÃ‚Â§V.<N>(+): <one-line cause>`. SPEC.md only. Record lands even when fix deferred.
2. **Code commit** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â build skill (resume or operator-dispatched): invariant w/o test = lie ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ add failing test first, name cites invariant (`TestV<N>_RefundIdempotent`), watch fail. Fix code. New test ! pass; full suite ! no regression. Commit `T<n>: <goal>` citing new Ãƒâ€šÃ‚Â§B/Ãƒâ€šÃ‚Â§V.

## WORKED EXAMPLE

Input: `refund job double-charged customer on retry`

1. TRACE: payment service retried on 5xx, no idempotency key ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ charge reversed twice. Cause: `refund(ctx, amount)` not check prior charge state.
2. ANALYZE: recurrence class? yes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every retry-able money-mutation in payment service exposed; future endpoints hit same trap ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new Ãƒâ€šÃ‚Â§V.
3. PROPOSE:
   ```
   Ãƒâ€šÃ‚Â§B row: B<n>|2026-04-20|refund retry double-charged, no idempotency check|V<N>
   Ãƒâ€šÃ‚Â§V line: V<N>: every refund ! idempotency key check before charge reversal
   ```
4. HANDOFF spec commit: `backprop Ãƒâ€šÃ‚Â§B.<n>(+) + Ãƒâ€šÃ‚Â§V.<N>(+): refund retry double-charge` (SPEC.md only).
5. HANDOFF code commit via build skill: `TestV<N>_RefundIdempotent` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â refund twice w/ same key ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1 reversal posted; watch fail. Add idempotency-key column; check before `charge.reverse()`. Test pass, suite no regression ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commit `T<n>: refund idempotency` citing Ãƒâ€šÃ‚Â§B.<n> + Ãƒâ€šÃ‚Â§V.<N>.

## GOOD INVARIANT

- Testable in code (grep-able or assert-able).
- Scoped to behavior, not file.
- Positive where possible (`! hold` over `not forbid`).
- Cites Ãƒâ€šÃ‚Â§I surface where applies.

Bad: `V<N>: code should be correct.`
Good: `V<N>: every pg_query ! params via driver, not string concat.`

## WHEN NOT Ãƒâ€šÃ‚Â§V

- Mechanical typo, no class (`i++` vs `i--` in throwaway).
- One-time migration fix.
- Root cause external dep ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ upgrade dep, note in Ãƒâ€šÃ‚Â§C.

Still append Ãƒâ€šÃ‚Â§B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â records failure mode considered. Future same-class bug ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Ãƒâ€šÃ‚Â§B grep shows precedent.

## OUTPUT

Ãƒâ€šÃ‚Â§B entry (always) + Ãƒâ€šÃ‚Â§V (usually) drafted for spec skill; test + code fix land via build skill. Two commits, cross-cited: spec commit names Ãƒâ€šÃ‚Â§B/Ãƒâ€šÃ‚Â§V, code commit cites them. No dashboards, no log files ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SPEC.md + git = full history.