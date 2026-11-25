---
name: fix
description: "Plan-aware auto-fix loop. Ensure tests pass, lint clean, format applied, graph risks handled."
---
# /supergraph:fix

Plan-aware auto-fix loop. Ensure tests pass, lint clean, format applied, graph risks handled.

## Usage

`/supergraph:fix` | `/supergraph:fix plan auth-login` | `/supergraph:fix plan auth-login task 2`

## Steps

### 0. Announce
"ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â§ /supergraph:fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â starting auto-fix loop..."

### 1. Select Plan Context

0 plans ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skip | 1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use | >1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask | `plan <slug>` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ match.
Read `## Environment Context`, fix scoped task or all in-progress/stuck tasks.

### 2. Get Commands

Read from plan `## Environment Context` or `.supergraph-env` (set by `/supergraph:scan`). Missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP, run scan first.
Missing command ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skip phase, report as `SKIP`.

### 3. Get Changed Files
`git diff --name-only && git diff --cached --name-only`. Reindex `CBM_PROJECT` if stale (`index_status`ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢`index_repository`, see `references/codebase-memory-contract.md`) via `codebase-memory-mcp`.

### 3b. Serena pre-loop (optional): See `serena/SKILL.md:Setup`. If scan not run, call `initial_instructions`; `get_diagnostics_for_file` per changed file to catch type errors early. Skip if `SERENA_ACTIVE=false` or unavailable.

### 4. Auto-Fix Loop (max 3 iterations)

At iteration start: "ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â§ Fix iteration N/3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â running tests..."

| Phase | Action |
|---|---|
| Reproduce | Smallest failing cmd + expected vs actual |
| Tests | Targeted tests else `$TEST_CMD`; fix source. **Dedup:** if same `HEAD_SHA` and last `PASS <120s` and `git diff` unchanged, reuse evidence; else rerun fresh (respects `verify` freshness guard) |
| Serena fix | `get_diagnostics_for_file` + `replace_symbol_body`/`rename_symbol` (see `serena/SKILL.md`) |
| Format+Lint | `$FORMAT_CMD`ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢`$LINT_CMD`; rerun lint if formatted |
| Graph | Reindex `CBM_PROJECT` if stale (`index_status`ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢`index_repository`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â respect `scan: TTL 10m` (skip `index_repository` if fresh per `.supergraph-env`), then `codebase-memory-mcp` recipes `cycles/test-gaps/complexity/cross-boundary` |
| Decide | All cleanÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢break else continue |

### 5. Update Plan Status (if plan exists)

- Succeeded ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `Status: completed`
- Failed after 3 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `stuck` + append STUCK log
- Never mark completed if tests or lint fail

### 5.1 Review/Fix Circuit

Use the durable ledger and review package for every repair cycle:

- For **rounds 1-3**, resume the original implementer with the smallest failing evidence and re-review only changed scope.
- For **rounds 4-5**, use a fresh stronger implementation pass, then run a scoped independent review.
- After five rounds, trigger the **circuit-breaker**, stop automatic repair, and record the ruling, unresolved evidence, and next human decision in the finish report and `ledger.md`.
- A passing test does not erase a review finding; retain the report and update only the affected artifact.

### 6. Report

```
## Auto-Fix Report
- Iterations: N/3 | Tests: PASS|FAIL|SKIP | Lint: PASS|FAIL|SKIP | Format: PASS|SKIP
- Graph: PASS|WARNING|CRITICAL | Plan status: updated|none
- Issues: [list or "none"]
Next: /supergraph:verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /supergraph:review
```

## Rules

- Max 3 fix iterations
- Never commit broken code
- Never use `git add -A`
- Never hide failures by weakening tests
- Prefer source fixes over test edits
- CRITICAL graph findings: fix or escalate
- Warnings: fix or report
- Prefer `mcp__serena__replace_symbol_body` for body fixes and `mcp__serena__rename_symbol` for renames when Serena is available
