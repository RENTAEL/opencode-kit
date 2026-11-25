---
name: explain
description: "Inverse of `telegraph` skill. Human-facing. Reads SPEC.md, expands one citation ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plain English w/ cited context. Zero writes."
---
# explain ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â decompress spec into prose

Inverse of `telegraph` skill. Human-facing. Reads SPEC.md, expands one citation ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plain English w/ cited context. Zero writes.

## LOAD

1. Read `SPEC.md`. Missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "no spec, nothing to explain." Bail.
2. Parse `$ARGUMENTS`:
   - `Ãƒâ€šÃ‚Â§T.n` / `Ãƒâ€šÃ‚Â§V.n` / `Ãƒâ€šÃ‚Â§B.n` / `Ãƒâ€šÃ‚Â§I.<key>` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ that row
   - `Ãƒâ€šÃ‚Â§G` / `Ãƒâ€šÃ‚Â§C` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ full section
   - `--next` or empty ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ lowest-numbered Ãƒâ€šÃ‚Â§T row w/ status `.`
3. `.spec/spec-renumber-map.json` exists (written by reorganize skill per Ãƒâ€šÃ‚Â§V renumber permission) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ on `Ãƒâ€šÃ‚Â§V.<n>` arg, walk `old:V<n> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new:V<m>` chain newest-first to end, resolve result against current SPEC.md. Map read, never mutated (read-only-diagnostic invariant). Absent ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ arg resolves directly.
4. Citation absent ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ list valid ids in target section. Bail.

## EXPAND

1. Quote raw telegraph line(s) verbatim in code block.
2. Restate in plain English ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full sentences, no telegraph symbols, no fragments.
3. Pull cited siblings:
   - Ãƒâ€šÃ‚Â§T ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ expand every Ãƒâ€šÃ‚Â§V and Ãƒâ€šÃ‚Â§I it cites.
   - Ãƒâ€šÃ‚Â§V ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ list Ãƒâ€šÃ‚Â§T tasks citing it, Ãƒâ€šÃ‚Â§B bugs referencing it.
   - Ãƒâ€šÃ‚Â§B ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ expand broken Ãƒâ€šÃ‚Â§V and fixing Ãƒâ€šÃ‚Â§T.
   - Ãƒâ€šÃ‚Â§I ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ name constraining Ãƒâ€šÃ‚Â§V invariants.
   - Ãƒâ€šÃ‚Â§G / Ãƒâ€šÃ‚Â§C ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no cross-cites; prose only.
4. Close w/ one line: what reader should now understand.

## OUTPUT SHAPE

```
## Ãƒâ€šÃ‚Â§T.<n> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â add auth middleware

> T<n>|.|add auth mw|V<n>,I.api

In plain English: this task adds an authentication middleware that runs before
every request reaches its handler.

Cited invariants:
- Ãƒâ€šÃ‚Â§V.<n> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every request must pass an auth check before the handler runs.

Cited interfaces:
- Ãƒâ€šÃ‚Â§I.api ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â POST /x returns 200 with {id:string}; the middleware must not
  change this shape.

Status: not started (`.`).

Bottom line: implement a middleware that enforces Ãƒâ€šÃ‚Â§V.<n> without altering Ãƒâ€šÃ‚Â§I.api.

## Hint

Ãƒâ€šÃ‚Â§T.<n> is pending ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â typical next step is item 1 to start work, or item 2 if you want to read the cited invariant first.

## Next

1. invoke the build skill Ãƒâ€šÃ‚Â§T.<n> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â start implementation
2. invoke the explain skill Ãƒâ€šÃ‚Â§V.<n> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read the cited invariant in prose
```

## MECHANIZE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â script-candidate scan

Recipe end ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ before the `## Next` block, scan this run for a mechanization candidate. Candidate = any of:

- ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit exactly one `## Next` item naming the observed pattern + proposed script mode; none ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no item. Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants). Route by cwd:

- dev repo (this skill pack) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new Ãƒâ€šÃ‚Â§T row
- consumer repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.opencode/check-extras` row

## OUTPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Next" block

Heading `## Next`; 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `invoke the <skill-name> skill [args]`). Optional `## Hint` (ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 3 lines) precedes when item selection needs hidden state (closed-vs-pending row implications, citation-form edge cases). Read-only ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ items are follow-ups: `invoke the build skill Ãƒâ€šÃ‚Â§T.n` only for `.` rows; closed `x` rows ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `invoke the explain skill --next` or `invoke the check skill`.

Closed Ãƒâ€šÃ‚Â§T row (terminal state) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tail of output:

```
Status: complete (`x`).

Bottom line: Ãƒâ€šÃ‚Â§V.<n> is enforced by the middleware shipped under Ãƒâ€šÃ‚Â§T.<n>.

## Hint

Closed rows are historical. `run 1` skips to live work; `run 2` audits whether the closed task drifted out of code.

## Next

1. invoke the explain skill --next ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read the next pending Ãƒâ€šÃ‚Â§T row
2. invoke the check skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â audit whether the closed task still holds
```

"Bottom line" stays ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â summarizes citation, never directs action. Action only in Next; pre-action context in optional Hint.

## NON-GOALS

- Zero writes. No SPEC.md edits, no code edits.
- No code reads. Spec-only (spec-vs-code ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the check skill).
- No telegraph in output. Prose is the whole point.
- One id per call. Loop for multiple.