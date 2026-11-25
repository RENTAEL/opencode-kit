---
name: verify
description: "Requires healthy `index_status` for `CBM_PROJECT` (see `references/codebase-memory-contract.md`); then `codebase-memory-mcp` `detect_changes`, `trace_path`, recipes `cycles/hubs/bridges/test-gaps`. Block on degraded/new cycle/unapproved hub/missing tests."
---
# /supergraph:verify

Requires healthy `index_status` for `CBM_PROJECT` (see `references/codebase-memory-contract.md`); then `codebase-memory-mcp` `detect_changes`, `trace_path`, recipes `cycles/hubs/bridges/test-gaps`. Block on degraded/new cycle/unapproved hub/missing tests.

Fresh verification gate before completion claims.

**Iron Law:** `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`

## When to Use

Before saying/implying: done, fixed, passing, clean, ready, complete, works, verified, successful.
Also: before marking `Status: completed`, committing, PR'ing, accepting agent reports, moving to next phase.

## Usage

`/supergraph:verify` | `tests` | `lint` | `build` | `plan auth-login task 2` | `claim "login fixed"`

## Evidence Mapping

| Claim | Required fresh evidence |
|---|---|
| Tests pass | `$TEST_CMD` exits 0, zero failures |
| Lint clean | `$LINT_CMD` exits 0, zero errors |
| Build succeeds | `$BUILD_CMD` exits 0 |
| Bug fixed | Original failing symptom/test now passes |
| Regression covered | RED failed before fix, GREEN passes after |
| TDD complete | RED failure valid, GREEN passes, refactor verified |
| Task completed | Acceptance criteria met + verification commands pass |
| Agent completed | Diff inspected + independent tests/lint |
| Review passed | Reviewer + graph review + tests/lint pass |
| Ready to merge | Tests + lint + build + review PASS |

## Steps

### 0. Announce
"ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ /supergraph:verify ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verifying [claim] with fresh evidence..."

### 1. Identify Claim
Map claim to required proofs from evidence mapping.

### 2. Select Plan Context (if applicable)
0 plans ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skip | 1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use | >1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask | `plan <slug>` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ match.

### 3. Get Commands
Read from plan `## Environment Context` or `.supergraph-env` (set by `/supergraph:scan`). Missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP, run scan first.
No command can prove claim ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP: "Required check is unknown."

### 3b. Serena sweep (optional): See `serena/SKILL.md:Setup` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `get_diagnostics_for_file` per touched file; STOP on type errors before test suite. Skip if `SERENA_ACTIVE=false` or unavailable.

### 4. Run Fresh Verification (NOW ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no reuse of old output unless freshness guard passes)
For agent output: `git diff --stat && git diff --name-only`.
Then run relevant tests/lint/build locally.
**Freshness guard (dedup suite, preserves Iron Law):** Reuse of immediately prior evidence is allowed **only if** `HEAD_SHA` unchanged and `git diff --name-only HEAD` unchanged and last `PASS` timestamp `<120s` ago (same commit). Otherwise **must rerun** ` $TEST_CMD`/`$LINT_CMD` fresh NOW. Guard respects `CBM_INDEXED_AT` TTL from `/supergraph:scan` but never skips verification before merge/PR ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if `HEAD_SHA` changed, reuse is invalid.

### 5. Read Output
Check: exit code, failure count, error count, warnings. Don't confuse lint ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  build, targeted ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  suite.

### 6. Report Evidence

**Pass:**
```markdown
## Verification Evidence
- Claim: [claim] | Command: `[command]` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ exit 0 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ PASS
- Evidence: [output summary] | Timestamp: [now]
```

**Fail:**
```markdown
## Verification Failed
- Claim: [claim] | Command: `[command]` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ exit [N] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ FAIL
- Failure: [summary] | Next: /supergraph:fix
```

Cannot verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ say so explicitly. No completion language.

### 7. Update Plan Status
Only after evidence passes: `in_progress` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `completed`.
If failed ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ keep status or mark `stuck` if retries exhausted.

**For user-facing confirmation:** Announce task/plan completion in the user's language.
If plan context exists, show: "Task N completed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [user-facing summary]"

### 8. Report
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ /supergraph:verify complete
- Claim: [claim] | Evidence: [command] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ PASS|FAIL
- Next: [recommendation]
```

## Anti-Patterns ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Block These
- "should work" / "seems fixed" / "probably passes" / "looks good"
- Trusting agent reports without independent check
- Stale command output | No acceptance criteria check
- Commit/PR without fresh tests+lint+build+review evidence
- Hiding skipped checks behind positive wording

## Evidence Rules
Evidence before claims, always. Fresh only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â old runs don't count.
Read output before reporting. No positive language without proof.
Agent output requires independent verification.
