---
name: ponytail-review
description: "Review diffs for unnecessary complexity. One line per finding: location, what to cut, what replaces it. The diff's best outcome is getting shorter."
---
Review diffs for unnecessary complexity. One line per finding: location, what
to cut, what replaces it. The diff's best outcome is getting shorter.

## Format

`L<line>: <tag> <what>. <replacement>.` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or `<file>:L<line>: ...` for
multi-file diffs.

Tags:

- `delete:` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hand-rolled thing the standard library ships. Name the function.
- `native:` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â dependency or code doing what the platform already does. Name the feature.
- `yagni:` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â same logic, fewer lines. Show the shorter form.

## Examples

ÃƒÂ¢Ã‚ÂÃ…â€™ "This EmailValidator class might be more complex than necessary, have you
considered whether all these validation rules are needed at this stage?"

ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `L12-38: stdlib: 27-line validator class. "@" in email, 1 line ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â real validation is the confirmation mail.`

ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 deps.`

ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `repo.py:L88: yagni: AbstractRepository with one implementation. Inline it until a second one exists.`

ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `L52-71: delete: retry wrapper around an idempotent local call. Nothing replaces it.`

ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `L30-44: shrink: manual loop builds dict. dict(zip(keys, values)), 1 line.`

## Scoring

End with the only metric that matters: `net: -<N> lines possible.`

If there is nothing to cut, say `Lean already. Ship.` and stop.

## Boundaries

Complexity only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â correctness bugs, security holes, and performance go to a
normal review pass, not this one. A single smoke test or `assert`-based
self-check is the ponytail minimum, not bloat ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never flag it for deletion.
Does not apply the fixes, only lists them.
"stop ponytail-review" or "normal mode": revert to verbose review style.
