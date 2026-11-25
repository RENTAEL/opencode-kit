---
name: smart-git-commit
description: "Produces gold-standard Git commits: tested, atomic, secure, documented, and traceable. Follow every phase below in order. Never skip phases unless the user explicitly says so."
---
# Smart Git Commit Skill

Produces gold-standard Git commits: tested, atomic, secure, documented, and
traceable. Follow every phase below in order. Never skip phases unless the
user explicitly says so.

<!-- line-limit: 500 -->

---

## Phase 0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Read Project Rules

Check for CLAUDE.md, .gitmessage, .git/COMMIT_TEMPLATE at repo root.
If found, those rules override this skill's defaults.

```bash
cat CLAUDE.md 2>/dev/null && echo "ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Found CLAUDE.md"
cat .gitmessage 2>/dev/null && echo "ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Found .gitmessage"
```

Show what rules were loaded before proceeding.

---

## Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Diff Analysis

Run full diff analysis before touching `git add`:

```bash
git status
git diff --stat          # which files, how many lines
git diff                 # full diff for small changesets
git log --oneline -5     # recent commit context
```

Categorize every changed file:

| Path pattern | Category |
|-------------|----------|
| `src/` `lib/` `app/` | feature/fix/refactor |
| `tests/` `*.test.*` | test |
| `docs/` `*.md` | docs |
| `package.json` deps | chore |
| `.github/` `Makefile` | tooling |

If files span more than one category ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flag for atomic split in Phase 4.
Read `references/atomic-patterns.md` if split is needed.

---

## Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Security Scan (Never Skip)

Run the automated security scanner:

```bash
bash scripts/scan-secrets.sh
```

- **Exit 0** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ show "ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ Clean" and continue
- **Exit 1** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **HARD STOP**. Show findings. Do not proceed until clean.

If secrets found:
1. `git reset HEAD <file>` to unstage
2. Replace with env var or placeholder
3. Add to `.gitignore` if needed
4. Rotate exposed credentials if already pushed

Read `references/security-rules.md` for the full pattern list.

---

## Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Test Gate (Never Skip)

Auto-detect and run the project's test suite:

```bash
bash scripts/detect-test-runner.sh
```

- **status = "pass"** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ show test count and continue
- **status = "fail"** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **HARD STOP**. Fix failures first, then commit fix + feature together.
- **status = "not_found"** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ warn user, ask if they want to proceed anyway

Supported runners: npm test, pytest, cargo test, go test, make test,
rspec, mix test, gradle, ctest.

---

## Phase 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Atomic Split Decision

If Phase 1 found multiple concerns:

```bash
bash scripts/split-commits.sh
```

Show the proposed split plan. Execute each commit group in sequence
(Phases 5-7 repeat per group).

If single concern: proceed directly to Phase 5.

Read `references/atomic-patterns.md` for splitting strategies.

---

## Phase 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Commit Message Construction

Use the **5-part format** for every commit. No exceptions.

```
<type>(<scope>): <imperative summary ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â max 72 chars>

CONTEXT: <what state existed BEFORE this change ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â past tense>
CHANGE:  <exactly what was done ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â present tense, specific>
WHY:     <business or technical reason ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not obvious from the code>
IMPACT:  <what this enables/unblocks, or "No breaking changes">

<footers>
```

### Summary line rules

- **Imperative mood**: "add" not "added", "fix" not "fixing"
- **No period** at end
- **Under 72 characters**
- **Types**: `feat` `fix` `perf` `security` `refactor` `test` `docs` `chore` `hotfix` `revert` `release`

### Field rules

| Field | Rule | Good | Bad |
|-------|------|------|-----|
| CONTEXT | Past tense, describes the gap | "Auth tokens had no expiry" | "There was a bug" |
| CHANGE | Present tense, specific | "Adds 15-min sliding expiry with refresh rotation" | "Fixed the token thing" |
| WHY | Not obvious from code | "Required for SOC2 compliance" | "To improve security" |
| IMPACT | Downstream effect | "Enables audit logging of token refresh events" | "Things are better now" |

### Example

```
fix(payments): prevent double-charge on Stripe webhook retry

CONTEXT: Stripe delivered webhooks twice under high load due to 30s
         application timeout, causing duplicate charges.
CHANGE:  Adds idempotency_key (order_id + unix_ts hash) to all Stripe
         charge requests.
WHY:     Stripe's API natively deduplicates on idempotency keys ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â simpler
         than Redis-based deduplication.
IMPACT:  Eliminates billing support tickets for duplicate charges.

Closes #301
```

Read `references/message-examples.md` for 15 full examples.

---

## Phase 6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Issue and Ticket Linking

Auto-detect from branch name:

```bash
git branch --show-current | grep -oE '[0-9]+'
```

Check for open issues:

```bash
gh issue list --state open 2>/dev/null | head -20
```

Use the correct footer keyword:

| Footer | Intent |
|--------|--------|
| `Closes #N` | Fully resolves (auto-closes on merge) |
| `Fixes #N` | Bug fix (same as Closes) |
| `Refs #N` | Related but does not close |
| `Part of #N` | One commit in a larger effort |

If no issue found, ask user before proceeding.

---

## Phase 7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Execute Commits

Stage selectively ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never `git add .` blindly:

```bash
git add <specific files or directories>
git diff --cached --stat   # verify before committing
git commit -m "<subject>" \
  -m "CONTEXT: ...
CHANGE:  ...
WHY:     ...
IMPACT:  ..." \
  -m "<footers>"
git show --stat HEAD       # confirm after
```

---

## Phase 8 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Push Strategy

Never push directly to `main` or `develop`. Always push to feature branch:

```bash
git push origin HEAD
git push --set-upstream origin <branch>   # if new branch
```

Show commits being pushed:

```bash
git log --oneline origin/main..HEAD
```

---

## Phase 9 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PR Creation

If on a feature branch after push:

```bash
bash scripts/create-pr.sh
```

- Always creates as **draft** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user promotes when ready
- Show PR URL after creation

---

## Phase 10 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Release Tagging

Triggers on: "release", "ship", "version bump", "tag this"

```bash
bash scripts/generate-changelog.sh
```

Then:
1. Read current version from `package.json`, `pyproject.toml`, `Cargo.toml`
2. Bump version in the appropriate file
3. Commit: `chore(release): bump version to vX.Y.Z` (with 5-part format)
4. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. Push: `git push && git push --tags`

Read `references/release-workflow.md` for full semver guide.

---

## Quick Reference

| Scenario | Start at Phase |
|----------|---------------|
| Single clean commit | Phase 1 |
| Secret found | Phase 2 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix first |
| Tests failing | Phase 3 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix first |
| Mixed concerns in diff | Phase 4 |
| Already staged, need msg | Phase 5 |
| Need to push + open PR | Phase 8 |
| Release / version bump | Phase 10 |
| Hotfix on main | Phase 0 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ check rules |
