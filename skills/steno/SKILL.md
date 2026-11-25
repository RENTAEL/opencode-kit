---
name: steno
description: "Audience: human reviewer scanning prose for facts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not a token-optimised model. Plain words, readable symbols; LLM-facing register ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ telegraph skill (same skill pack)."
---
# steno ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â human-facing terse text

Audience: human reviewer scanning prose for facts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not a token-optimised model. Plain words, readable symbols; LLM-facing register ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ telegraph skill (same skill pack).

## SKIM TEST

Top criterion: fact appears in first sentence or bold-lead bullet of each block. Skim fails ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ rewrite first clause to state the fact ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not retain dense form, not cut further words. Compression subordinate: a word that aids the skim stays. Reviewer would slow on a symbol ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use the word.

Self-check every paragraph/bullet:

- First clause states the fact (subject + verb ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 8 words).
- Subject and verb both visible ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â symbol-chain fragments fail.
- Anti-test: cover everything after first clause; core fact still readable.

## SCOPE

Human-facing terse prose for non-author reviewers ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â readers scan facts, benefit from compression w/o telegraph-symbol load.

Applies (not exhaustive):

- GitHub issues & PRs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â titles, bodies (incl. PR desc refresh on merge).
- Commit-message bodies, incl. PR squash/merge release-note sections (subjects = per-skill fixed templates, preserve verbatim).
- READMEs & user-facing docs where compression aids scan.

Not:

- Code, snippets, backticked text.
- Conventional Commits title prefix (`type(area):`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fixed format.
- Error strings, log lines.
- External-facing copy (marketing, landing pages).

## SENTENCE SHAPE

Every prose sentence or bullet body:

1. **Lead-first** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â subject + verb open the sentence; topic-shift & qualifier clauses ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ tail. Subject past first clause ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skim fails.
2. **Visible subject-verb** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â subject explicit or imperative (`Add X.` OK). No symbol-chain fragments: `auth ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mw ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ handler` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `Auth middleware runs before the handler.`
3. **No hidden copulas** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â elide `is`/`are` only when fragment unambiguous. Drop copula in `X ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Y` only when Y reads as predicate, not apposition.
4. **ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1 participial phrase per sentence** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nesting kills first-clause readability.
5. **Cite at tail** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â end sentence w/ spec citation (`Ãƒâ€šÃ‚Â§V.<n>`, `Ãƒâ€šÃ‚Â§T.<n>`) or issue/PR ref (`#123`); not open or build sentence on cite. Write "Spell out symbols per the symbol-set invariant", not "The symbol-set invariant says to spell out symbols".

Verb-headed fragments fine. Lists > paragraphs. One idea per line in lists. Break long sentences before cutting words.

## SYMBOLS

Safe for GitHub readers:

```
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢   leads to / becomes / produces
ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥   at least
ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤   at most
&   and
|   or (in lists, not prose)
Ãƒâ€šÃ‚Â§   spec citation (`Ãƒâ€šÃ‚Â§V.<n>`, `Ãƒâ€šÃ‚Â§T.<n>`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â refs into SPEC.md only
```

No other symbols ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â math operators beyond this set ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ write the word; mirrors telegraph symbol policy.

## ACRONYMS

Spell out full term on first use, acronym in parentheses: spec-driven development (SDD). Common web/protocol acronyms exempt (use bare from first occurrence): `API`, `URL`, `JSON`, `HTTP`, `JWT`. Spell out domain acronyms unique to the repo or skill pack on first use.

## PRESERVE VERBATIM

- Code blocks, snippets, backticked text.
- Paths, URLs, `#123` issue/PR refs.
- Identifiers: function names, vars, env vars, flags.
- Numbers, versions, dates, SHAs.
- Error strings; SQL, regex, JSON, YAML.
- Quoted user-facing copy.
- `Resolves #N` / `Fixes #N` / `Closes #N` trailers ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact form.

## SHAPES

- **Bullets > paragraph** when listing > 2 items.
- **Definition list** for term/explanation pairs: `` - `--dry-run` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print actions, do not execute. ``
- **List > table** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â avoid markdown tables in human-facing docs; use bullets or definition lists whenever possible. Reserve tables for comparing > 2 options across > 2 axes where a list cannot carry the structure (per clarity-standard invariant).
- **Headers + fragments** > full sentences in issue/PR bodies (see release-commit example below).

## EXAMPLES

**Issue body** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Anti fails rule 1 (lead-first): reader scans 14 words before the fact.

> When a user tries to log in with an email address that contains uppercase letters, the system fails to find their account because the lookup is being done in a case-sensitive manner, which is not the expected behavior for email addresses.

Good ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â first sentence states fact + condition; second states cause + fix direction:

> Login fails when email has uppercase letters. Lookup is case-sensitive ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â should be case-insensitive for emails.

**PR body** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Anti fails SKIM TEST: 8 filler words precede the fact.

> This pull request basically just adds some additional logging to the auth middleware so that we can debug issues more easily in production environments. It also includes a small refactor of the token validation logic.

Good ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â first fragment states both items; each bullet opens with a verb:

> ## Summary
>
> Add auth middleware logging for prod debugging. Refactor token validation.
>
> ## Changes
>
> - Log `userId`, `path`, `latency` on every authed request
> - Extract `validateToken()` from middleware into `auth/token.go`

**Release commit body** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Anti fails rule 4: nested participials, 47 words before the expiry fact.

> This change implements a new authentication system using JWT tokens which replaces the previous session-based authentication that was being used. Users will now be able to log in and receive a token that they can use to make authenticated requests, and these tokens will expire after a period of 24 hours.

Good ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 4-word first sentence states the replacement; 3-word second states the constraint:

> ## Summary
>
> JWT auth replaces sessions. Tokens expire 24h.
>
> ## Changes
>
> - JWT generation & validation
> - `/auth/refresh` endpoint
> - Middleware reads `Authorization: Bearer <jwt>`
>
> ## Breaking
>
> - Session cookies dropped ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â clients must send `Authorization` header.

## BOUNDARIES

Literal phrasing w/ readable symbols (per SCOPE) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â idiom adds parsing cost & ambiguity. Within scope, not:

- idiom ("moves the needle", "low-hanging fruit", "boil the ocean").
- word-level metaphor ("earns its keep", "bite", "smell").
- colloquialism ("gotcha", "ish", "yeah", "kinda").
- culture-loaded shorthand (sports, military, film references).

Exclusions:

- Colloquial sentence structure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â allowed where it aids reviewer flow; register applies at word level.
- Domain-load-bearing named ops (`backprop`, `telegraph-encode`, `socratic`, `steno`).
- Established tech vocab doubling as metaphor (`drift`, `bottleneck`, `leak`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â allowed when standard term in context.

## OPERATOR CHOICE

When the operator asks you to decide, state the choice in one sentence, list options plainly (one line each), recommend one option in one sentence. Do not end w/ prose "or keep going?" question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â same-turn choice is a gate, not a sentence. Matches decision-gate invariant posture: AskUserQuestion gates irrecoverable branches; prose trailing-question gate is ambiguous signal, not a gate.