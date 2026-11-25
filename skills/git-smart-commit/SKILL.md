---
name: git-smart-commit
description: "Split pending working-tree changes into atomic, well-scoped conventional commits. Always propose a commit plan to the user via `submit_plan` before touching the index. Only execute after explicit user approval. **Never push.**"
---
# git-smart-commit

Split pending working-tree changes into atomic, well-scoped conventional commits.
Always propose a commit plan to the user via `submit_plan` before touching the
index. Only execute after explicit user approval. **Never push.**

---

## 1. Audit the working tree

Run these commands to understand what is pending:

```bash
git status --porcelain
git diff --cached --stat
git diff --stat
git log --oneline -5
```

If nothing is pending (clean tree), report it and stop.

---

## 2. Identify untracked files that should NOT be touched

Run `git ls-files --others --exclude-standard` to list untracked files.

**Critical safety rule:** never stage, commit, or delete an untracked file
unless you are confident it was produced by this session. When in doubt,
include it in the plan proposal but flag it with `ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â untracked ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify
before staging`. The `submit_plan` approval step is your safety net:
the user will see and can reject.

**Files to silently skip (do not even propose):**

- `.env`, `.env.local`, `.env.*` (secrets)
- `*.log`, `*.pid`, crash dumps
- `node_modules/`, `vendor/`, `__pycache__/`, `.terraform/`
- IDE/editor config (`.vscode/`, `.idea/`) unless the project tracks them
- OS noise (`.DS_Store`, `Thumbs.db`)
- Binary files / archives unless clearly project assets

If unsure whether a file was session-created, **flag it in the plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not
assume**.

---

## 3. Analyze each changed file

For each modified, added, or renamed file, read its diff (or full content for
new files) to understand **what** changed and **why**. Categorize:

| Change nature          | Conventional type | Typical scope inference       |
| ---------------------- | ----------------- | ----------------------------- |
| New feature / API      | `feat`            | Package, module, or component |
| Bug fix                | `fix`             | Broken package/area           |
| Internal restructuring | `refactor`        | Package/area refactored       |
| Performance            | `perf`            | Hot path location             |
| Docs / comments only   | `docs`            | Doc area (README, package)    |
| Tests only             | `test`            | Tested package                |
| Build/CI/deps          | `build` or `ci`   | Tooling area                  |
| Maintenance, chores    | `chore`           | Rare ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â avoid overuse          |
| Revert                 | `revert`          | What is being reverted        |

---

## 4. Group into atomic commits

Group files that belong together ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a single logical change. Heuristics
(apply judgment, not rigidly):

- **Same feature/fix**: files changed for the same reason go together
- **Same package/directory**: changes tightly coupled by import graph
- **Change-type boundaries**: a `feat` and a `refactor` in the same package
  that are separable ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ two commits
- **Test files** paired with the code they test ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ same commit
- **Generated files** (golden, mocks) paired with their source ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ same commit
- **Docs-only changes** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ separate commit unless trivial inline doc fixes
  alongside code

If two groups are interdependent (commit A won't compile without commit B),
keep them as one commit.

Each group must be independently buildable after `git add` and `git commit`
(files within the group must form a coherent unit, though cross-group
dependencies are acceptable since they're applied sequentially).

---

## 5. Craft the commit messages

For each group, produce a conventional commit message following these rules:

**Format:** `type(scope): short description`

- **type** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â from the table in step 3
- **scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only if it adds clarity. Omit for cross-cutting changes or when
  the scope would be the entire repo. Good scopes: `auth`, `ci`, `engine`,
  `renderer`, `tui`. Bad scopes: `misc`, `various`, the repo name itself.
- **short description** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â imperative mood, lowercase, no trailing period,
  max 72 characters total (type+scope+description).

**Body:** omit by default. A body is **only** justified when:

- The _why_ of the change is non-obvious from the diff and title alone
- It documents a **BREAKING CHANGE** (required footer: `BREAKING CHANGE: <description>`)

A body must **never** be a list of changed files or a re-statement of the
diff. If the title says it, the body doesn't repeat it.

**Breaking changes:** append `!` after type/scope:

- `feat(api)!: drop legacy endpoint` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ requires `BREAKING CHANGE:` footer.

**Examples:**

| Diff summary                                           | Message                                       |
| ------------------------------------------------------ | --------------------------------------------- |
| Added JWT middleware in auth package                   | `feat(auth): add JWT middleware`              |
| Fixed nil pointer in renderer                          | `fix(renderer): handle nil template data`     |
| Extracted validation to separate file, no logic change | `refactor(engine): extract validation step`   |
| Updated README with install instructions               | `docs: update install instructions in README` |
| Added table-driven tests for config parser             | `test(config): add table-driven parser tests` |
| Renamed `UserID` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `UserIdentifier` everywhere         | `refactor!: rename UserID to UserIdentifier`  |
| Changed default port, bump go.mod dep                  | `chore: update default port and go modules`   |

---

## 6. Propose the plan

Build a Markdown commit plan with this exact structure and submit it via
`submit_plan`:

```markdown
# Commit Plan

## Summary

- N atomic commit(s) from M changed file(s)
- Tree currently: [clean | staged files | working-tree changes]

## Commits

### 1. `type(scope): description`

| File            | Status   |
| --------------- | -------- |
| path/to/file.go | modified |
| path/to/new.go  | new ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â   |

### 2. `type(scope): description`

| File | Status |
| ---- | ------ |
| ...  | ...    |

## Safety Notes

- [Any untracked files that need manual review]
- [Any files intentionally excluded]
- [Breaking change warnings if any]
```

Show the full commit message (title + body if any) for each commit. Flag
untracked files with `ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â` and explain why they were included or excluded.

---

## 7. Execute (only after plan approval)

Once the user approves the plan, execute commits **sequentially** (order
matters when commits build on each other):

```bash
# For each commit group in order:
git add <files...>          # only the files in this group
git commit -m "<message>"   # use the exact message from the plan
```

After all commits complete, run `git status` and `git log --oneline -5` to
confirm the result.

**Never `git push`.** The user handles that separately.

---

## Guardrails

- Never delete or `git rm` files that were not explicitly created during this
  session. If a file should be removed, flag it in the plan for human review.
- Never commit secrets (`.env`, credentials, API keys). Scan diffs for
  suspicious patterns.
- Never amend or rewrite existing commits. Only create new ones.
- Never run `git push`, `git push --force`, or any remote operation.
- If `git commit` fails (hooks, conflicts), stop and report the error. Do not
  try to work around it.
- If the plan groups changes in a way the user disagrees with, accept their
  regrouping and re-propose. Don't argue.
- The plan is the contract ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not add, remove, or reorder files during
  execution unless the user explicitly requests it.
