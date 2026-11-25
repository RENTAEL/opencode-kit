---
name: workflow-git-cli
description: "Local git work stays in the native Git CLI, and every remote GitHub operation goes through the `gh` CLI, which authenticates once through `gh auth login` (it keeps the token in the system keychain when one is available, otherwise in `~/.config/gh/hosts.yml`). The one GitHub to..."
---
# Git CLI Workflow

## Purpose

Local git work stays in the native Git CLI, and every remote GitHub operation goes through the `gh` CLI, which authenticates once through `gh auth login` (it keeps the token in the system keychain when one is available, otherwise in `~/.config/gh/hosts.yml`). The one GitHub tool is `github_ci_wait`, and it only waits for CI: one call replaces a polling loop.

## GitHub Execution Policy

- Use `gh` for every remote GitHub operation: pull requests, checks, workflow runs and job logs, reviews and review threads, comments, issues, merges, workflow dispatch. See GitHub Remote Operations below for the exact commands.
- Wait for CI with `github_ci_wait`, never with `gh pr checks --watch`, `gh run watch` or a sleep loop.
- Pass `--repo <owner>/<repo>` whenever the working directory might not be the target repository (a worktree of another project, a sibling checkout, a task directory). Commands run inside the target checkout infer it.
- Check the authenticated account once per session with `gh auth status`. Several repositories on one machine can belong to different organizations; a 404 on a repository that exists usually means the account lacks access, not that the path is wrong.
- Shape output with `--json <fields>` and `--jq`, and cap log reads with `tail`/`grep`. A raw `gh run view --log` is tens of thousands of lines.

## Daily Flow

1. Inspect current state.
2. Sync main, then create or switch branch.
3. Review changes with diff/status.
4. Stage intentionally.
5. Commit with focused message.
6. Push branch and set upstream.

## Branch Naming

```
feat/<ticket>
feat/<ticket-1>-<ticket-2>
feat/<feature-name>
```

Examples:

- `feat/ORG-245` - single ticket
- `feat/ORG-242-ORG-244` - multi-ticket
- `feat/quiz` - large feature spanning many tickets

Use `feat/` prefix for all branches. The ticket ID is sufficient - no need to repeat the description in the branch name.

## Branch Per Ticket

Use one branch per JIRA ticket by default.

Before starting work on a new ticket:

```bash
git checkout main
git pull
git checkout -b feat/ORG-123
```

If the repository has app-scoped migration scripts (for example `apps/api`), run the migration command from the owning app workspace:

```bash
cd apps/<app-owning-typeorm>
yarn migration:run
```

If the branch already exists because you are expanding existing work, switch to it instead of creating a new branch.

## Branch Per Pull Request

**Before any PR-related work - analysis, code review, or implementation - check out the PR branch first.**

This applies to:

- Reviewing a pull request (code review)
- Analyzing PR changes or answering questions about a PR
- Fixing issues raised in PR review comments
- Continuing work on an existing PR

Why: Tools like `codebase_find_definition`, `codebase_trace_calls`, and file reads operate on the local working tree. If you are on `main` while reviewing a PR branch, tool results will reflect `main` - not the code under review. This leads to incorrect analysis, missed changes, and invalid review comments.

Check out a PR by number:

```bash
gh pr checkout <PR_NUMBER>
```

Verify you are on the correct branch:

```bash
git branch --show-current
git log --oneline -n 3
```

After checkout, confirm the branch is up to date with the remote:

```bash
git pull
```

If the PR is from a fork or you only need to read (not push), `gh pr checkout` still works - it creates a local tracking branch automatically.

A dispatched run under a read-only agent profile never switches or creates a branch, because the checkout it works in may be the owner's. `pr-reviewer` checks out the head detached with `gh pr checkout <PR_NUMBER> --detach`, which needs no `git pull`, and confirms that `git rev-parse HEAD` equals `gh pr view <PR_NUMBER> --json headRefOid --jq .headRefOid`. `reviewer` and `researcher` cannot run `gh pr checkout` at all: they review the checkout or worktree their brief names and read the pull request with `gh pr view` and `gh pr diff`.

**Rule:** Never start PR review or PR-related analysis without first checking out the PR branch. If you catch yourself reading PR diffs while on `main`, stop and checkout the correct branch before continuing.

## Command Playbook

### 1) Inspect current state

```bash
git status
git branch --show-current
git log --oneline -n 5
```

### 2) Create or switch branch

```bash
git checkout main
git pull
git checkout -b feat/ORG-123
```

For app-scoped migrations:

```bash
cd apps/<app-owning-typeorm>
yarn migration:run
```

When continuing existing work:

```bash
git checkout feat/ORG-123
git pull
```

### 3) Review current work

```bash
git diff
git diff --staged
git status --short
```

Use `git diff` before staging and `git diff --staged` before committing.

### 4) Stage changes deliberately

Prefer path-based staging:

```bash
git add src/modules/example/example.module.ts
git add src/modules/example/services/example-api.service.ts
```

Stage everything only when intentional:

```bash
git add --all
```

Notes:

- `git add --all` respects ignore rules.
- `git add .` also respects ignore rules, but is path-scoped from current directory.

### 5) Commit

```bash
git commit -m "feat: add issue link removal tool"
```

Before commit, verify exactly what is staged:

```bash
git diff --staged
```

### 6) Push

First push for a branch:

```bash
git push -u origin $(git branch --show-current)
```

Next pushes:

```bash
git push
```

## GitHub Remote Operations

Every command below runs inside the target checkout, or takes `--repo <owner>/<repo>`. `{owner}` and `{repo}` inside `gh api` paths are filled in by `gh` from the current repository.

### Read a pull request

```bash
gh pr view <n> --json title,body,author,headRefName,baseRefName,headRefOid,mergeable,mergeStateStatus,additions,deletions,files
gh pr diff <n> --name-only
gh pr diff <n>                       # the whole diff; scope it with `-- <path>` style filtering through grep when it is large
gh pr list --state open --json number,title,headRefName,author --jq '.[] | [.number,.headRefName,.author.login,.title] | @tsv'
```

### Waiting for CI, bound to the head commit

A check result belongs to one commit; an unpushed fix leaves green checks on an older commit and nothing else would reveal it. Wait with `github_ci_wait`: pass the repository checkout as an absolute `cwd`, exactly one target, and `timeoutMinutes` (at most 180).

| What you wait for                                 | Arguments                            | Notes                                                                                                |
| ------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| A pull request whose branch you have checked out  | `pr: <n>`                            | Its head must equal your local branch; a push that has not landed yet keeps it pending for 2 minutes |
| A pull request you have not checked out           | `pr: <n>, head: "<sha>"`             | A reviewer or a merge from the base checkout names the head it means                                 |
| The push run of a commit (build, migrate, deploy) | `sha: "<merge sha>", workflow: "CI"` | Waits for the workflow to start, however long; `checks: ["Deploy API Dev"]` narrows it to named jobs |
| One workflow run                                  | `run: <run-id>`                      | For a commit with several runs of one workflow, such as dispatched deploys                           |

The result's first line is `CI PASS|FAIL|TIMEOUT|NO CHECKS|HEAD MISMATCH|STOPPED <target> waited <duration>` and the second counts the checks by conclusion. Every caller handles all six results, by these exact names:

- `CI PASS`: every counted check passed. `skipped` counts as passing, and line 2 names the skipped checks; a skip is fine only when the workflow skips that job by design for this change (for example a deploy job that runs only when an image was built), so say which case it is.
- `CI FAIL`: the result lists each failed check with its page, the end of up to 5 failed job logs and the `gh run rerun <run-id> --failed` command. Read more of a log with `gh run view <run-id> --log-failed | tail -n 120` only when the excerpt is not enough. Fail-fast is the default; `failFast: false` waits for every check.
- `CI HEAD MISMATCH`: 2 minutes into the wait, the pull request head is still not the commit you meant. Push, or pass the right `head`, then wait again. Only a `pr` target produces it.
- `CI NO CHECKS`: no check ran on the head within 5 minutes, which is never a pass, and an empty check list cannot show why. Proceed outside the CI gate only when both hold, and say why in your report; otherwise report BLOCKED:
  - every changed file (`gh pr diff <n> --name-only`, or `git diff --name-only <sha>^ <sha>` for a commit) falls outside the `on: paths` / `on: paths-ignore` filters of the repository's workflows that run for this event, read from `.github/workflows/` at the head;
  - `gh workflow list --all --json name,state` shows the workflow you expected as `active`, not disabled.

  Only a `pr` target and a plain `sha` target produce it; a `workflow` or `run` target waits for its jobs until the timeout.

- `CI TIMEOUT`: CI has not settled; the result names the checks still pending, any that already failed, and any named in `checks` that never appeared together with the checks that did run (a misspelt name waits until the timeout). It ends with `To keep waiting, call again on the same target with waitStartedAt: "<iso>"`. Continue with that `waitStartedAt`, or act on the timeout as the caller's instructions say.
- `CI STOPPED`: the call was cancelled; nothing is known, and it is never a pass. It also ends with the `waitStartedAt` to continue with.

Passing back `waitStartedAt` continues one wait series: the 2-minute head-mismatch and 5-minute no-checks windows and the waited time on line 1 count from the series start, while `timeoutMinutes` counts from the call. Without it, every call starts a new series, and a run of short calls never reaches `CI HEAD MISMATCH` or `CI NO CHECKS`.

How long one call may run depends on the harness:

- **OpenCode:** make one call with `timeoutMinutes` sized to the expected CI time. It holds your turn until CI settles. Work that runs elsewhere meanwhile (an async review run, a deploy) keeps going, but your own next step starts after the result, so order the steps that way.
- **Claude Code, interactive:** make one call sized the same way. A call that runs longer than about two minutes is moved to a background task, and the whole result arrives later as a task notification. Carry on with other work, and do not call `github_ci_wait` again for the same target while that wait runs.
- **`claude -p` worker:** the process exits when its turn ends, so a call moved to a background task is lost with it and its notification never arrives. Never make a call longer than 1 minute. Call with `timeoutMinutes: 1`; after each `CI TIMEOUT`, call again on the same target with `timeoutMinutes: 1` and the `waitStartedAt` the first result printed, until a result other than `CI TIMEOUT` arrives. The `timeoutMinutes` your instructions give for the wait is then the budget of the whole series: once line 1's waited time passes it, the last `CI TIMEOUT` is the wait's timeout, handled as those instructions say.

To read checks once without waiting, for example in a review summary, compare the heads first and then read the commit's checks:

```bash
LOCAL=$(git rev-parse HEAD)
REMOTE=$(gh pr view <n> --json headRefOid --jq .headRefOid)
[ "$LOCAL" = "$REMOTE" ] && echo "head matches" || echo "HEAD MISMATCH local=$LOCAL remote=$REMOTE"
gh pr checks <n>                     # exit 0 all passed, 1 a check failed, 8 checks still pending
gh api repos/{owner}/{repo}/commits/<sha>/check-runs --jq '.check_runs[] | [.name,.status,.conclusion] | @tsv'
```

### Workflow runs and job logs

```bash
gh run list --branch <branch> --event push --commit <sha> --json databaseId,workflowName,status,conclusion,headSha
gh run view <run-id> --json jobs --jq '.jobs[] | [.name,.status,.conclusion] | @tsv'
gh run view <run-id> --log-failed | tail -n 120     # only the failed steps, capped
gh run view <run-id> --job <job-id> --log | grep -nE 'Error|FAIL|ÃƒÂ¢Ã…â€œÃ¢â‚¬â€' | head -n 60
```

Re-run only the failed jobs of a run, on the same commit:

```bash
gh run rerun <run-id> --failed
```

Dispatch a workflow and find the run it started:

```bash
gh workflow run <workflow-file>.yml --ref <branch> -f environment=dev -f api_image_tag=<tag>
gh run list --workflow <workflow-file>.yml --limit 3 --json databaseId,status,createdAt,headSha
```

### Create and merge

```bash
gh pr create --base <base> --head <branch> --title "<conventional title>" --body-file <path-to-body.md>
gh pr view <n> --json mergeable,mergeStateStatus   # CLEAN merges; DIRTY needs a rebase; BLOCKED means a required check or review is missing
gh pr merge <n> --squash --delete-branch --match-head-commit <sha that passed>
gh pr view <n> --json mergeCommit --jq .mergeCommit.oid
```

Merge only after `github_ci_wait` returned `CI PASS` for that pull request, and pass the head it waited on (your local branch head, or the `head` you named) to `--match-head-commit`, so a push that landed after the wait makes `gh` refuse the merge instead of merging unchecked code. `CI FAIL`, `CI TIMEOUT`, `CI HEAD MISMATCH` and `CI STOPPED` are not a pass, and a repository without required status checks would let a merge through on any of them (a pull request whose Terraform lint had failed was merged exactly that way). `CI NO CHECKS` is handled as in "Waiting for CI, bound to the head commit".

Write the body to a file first and pass `--body-file`; multi-line bodies passed inline through `--body` break on quoting. Merging a pull request that is the base of another open pull request closes the downstream one; recreate it against the default branch with `gh pr create`.

### Review threads

Review threads, their resolution state and their node ids come from GraphQL; the REST comment id is not the thread id:

```bash
gh api graphql -f owner=<owner> -f repo=<repo> -F number=<n> -f query='
query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ pullRequest(number:$number){
  reviewThreads(first:100){ nodes{ id isResolved isOutdated path line
    comments(first:50){ nodes{ databaseId author{login} body createdAt } } } } } } }'
```

Reply in a thread (by the REST id of any comment in it), then resolve or reopen it by the thread's node id:

```bash
gh api repos/{owner}/{repo}/pulls/<n>/comments/<comment-database-id>/replies -f body='*resolver:* Addressed in <sha> ...'
gh api graphql -f threadId=<thread-node-id> -f query='mutation($threadId:ID!){ resolveReviewThread(input:{threadId:$threadId}){ thread { isResolved } } }'
gh api graphql -f threadId=<thread-node-id> -f query='mutation($threadId:ID!){ unresolveReviewThread(input:{threadId:$threadId}){ thread { isResolved } } }'
```

### Submit a review with inline comments

`gh pr review` cannot attach inline comments; submit one review through the reviews endpoint:

```bash
gh api repos/{owner}/{repo}/pulls/<n>/reviews --method POST --input review.json
```

```json
{
  "commit_id": "<head sha the review is about>",
  "event": "COMMENT",
  "body": "*reviewer:* ...",
  "comments": [{ "path": "apps/api/src/...", "line": 42, "side": "RIGHT", "body": "..." }]
}
```

- `event` is `APPROVE`, `REQUEST_CHANGES` or `COMMENT`. GitHub rejects the first two with 422 on a pull request the authenticated user authored (`gh api user --jq .login` against the PR author); use `COMMENT` there.
- `line` with `side: "RIGHT"` is the line number in the new file at the head; `side: "LEFT"` is the line in the old file at the merge base. It is neither the diff-hunk offset nor a local line count, and it must be a `+` line (RIGHT) or a `-` line (LEFT) inside a hunk of `gh pr diff`; anything else is rejected with 422. Derive it by walking each hunk from its `@@ -old,len +new,len @@` header, advancing the new-line counter on `+` and context lines and the old-line counter on `-` and context lines.
- A finding that cannot be anchored to a diff line goes into the review body.

### Comments and issues

```bash
gh pr comment <n> --body-file <path>
gh issue view <n> --json title,body,labels,comments
gh issue list --state open --search "<text>" --json number,title --jq '.[] | [.number,.title] | @tsv'
gh issue comment <n> --body '<text>'
gh issue close <n> --comment '<text>'
gh api repos/{owner}/{repo}/issues/comments/<comment-id> --method PATCH -f body='<new text>'
gh api repos/{owner}/{repo}/issues/comments/<comment-id> --method DELETE
```

## Gitignore Hygiene

### Check if a file is ignored

```bash
git check-ignore -v path/to/file
```

### Stop tracking a file that should be ignored

```bash
git rm --cached path/to/file
```

Then add the pattern to `.gitignore` and commit that change.

### Local-only ignore (do not commit)

Use `.git/info/exclude` for machine-specific entries.

## Workspace Noise Filtering

When summarizing `git status` or preparing commits, treat local-generated junk as noise unless explicitly requested.

Common examples:

- `**/node_modules/`
- build artifacts (`dist/`, `build/`, `.turbo/`, coverage outputs)
- IDE/editor files (`.idea/`, `.vscode/`, `.DS_Store`)

Rules:

- Do not stage or commit noise paths by default.
- In status summaries, call out noise once in a short note and keep focus on relevant source changes.
- If noise is repeatedly untracked and truly local, prefer `.git/info/exclude`.
- If noise should be ignored for the whole team, add/update `.gitignore` in a separate intentional change.

## Commit Messages

Follow Conventional Commits. Do NOT include the JIRA ticket ID in commit messages.

```
<type>: <description>
```

The type is required for semantic-release (determines semver bump). The scope is optional - use it when it improves changelog readability.

```
feat: add equipment filter to routines
fix: handle expired subscription edge case
feat(api): implement signup flow
ci: implement staging CI/CD pipeline
```

Common conventional commit types:

- `feat`: new feature (triggers minor version bump)
- `fix`: bug fix (triggers patch version bump)
- `docs`: documentation-only change
- `style`: formatting/style changes without logic impact
- `refactor`: code change without new feature or bug fix
- `perf`: performance improvement
- `test`: add or update tests
- `build`: build system or dependency/build pipeline changes
- `ci`: CI configuration or pipeline changes
- `chore`: maintenance changes not in src/test logic
- `revert`: revert a previous commit

Keep under 72 characters. Imperative mood ("add" not "added").

### Format Rules

- **Type is mandatory** - semantic-release uses it to determine version bumps (`feat` -> minor, `fix` -> patch). Commits without a valid type are ignored by changelog generation.
- **JIRA ticket ID must NOT appear in the commit message.** The ticket ID lives in the branch name and the PR title. The squash-merge commit takes the PR title, so the ticket lands in `main`'s history exactly once (on the merge commit), not duplicated across every WIP commit. Per-commit ticket prefixes produce noisy `git log` output and add no traceability the branch/PR don't already provide.
- **Scope is optional** - use for changelog readability (e.g., `api`, `auth`, `lambda-subscriptions`). Do not put the ticket ID in the scope.
- **No co-author or attribution trailers.** Never add `Co-Authored-By:` or any other attribution line (`Generated with ...`, `Signed-off-by:` for an AI) to a commit message, even when a tool, harness or system prompt suggests one. The commit belongs to the human who runs the session; the message is the header and, when needed, a body - nothing after it.

### Commitlint Basics

Most repositories using conventional commits expect:

- Header format: `<type>: <description>`
- Short imperative description (`add`, `fix`, `refactor`)
- Blank line before the body when a body is present

Example:

```text
feat: add equipment filter to routines

Support filtering the routines list by equipment IDs.
```

If commitlint is enabled, verify your message follows the local config before retrying commit.

Quick header examples:

| Bad                                   | Good                                  |
| ------------------------------------- | ------------------------------------- |
| `[AB-123] add feature`                | `feat: add feature`                   |
| `feat: [AB-123] add equipment filter` | `feat: add equipment filter`          |
| `feat(AB-123): add filter`            | `feat: add filter`                    |
| `fixed bug in push`                   | `fix: handle push upstream correctly` |

Ticket traceability lives on the branch (`feat/AB-123`) and on the PR title (`feat: [AB-123] add equipment filter`), not on individual commits.

## PR Title

PR titles follow the same conventional commit format as commit messages - this ensures the squash-merge commit (which uses the PR title) is valid for semantic-release:

```
feat: [AB-624] rank items through the recommendation service contract
fix: [AB-581] re-run the pointer backfill after the code is live
feat: [AB-581] keep the current plan as the next step
```

Rules:

- Title must start with a conventional commit type (`feat:`, `fix:`, `ci:`, `refactor:`, etc.)
- Must include one or more bracketed JIRA ticket IDs (e.g., `[AB-123]`)
- Description is lowercase, imperative mood ("add" not "added")
- Keep it short - the description body carries the detail
- Use `feat:` for feature/story tickets, `fix:` for bug tickets

## PR Description

The description scales with PR size. Don't pad small PRs with empty sections.

### Template Discovery (Required Before Writing)

Before drafting PR body content, check for a repository template using repository-relative paths (not absolute machine paths).

1. Resolve repo root: `git rev-parse --show-toplevel`
2. Check template candidates in this order:
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - `.github/pull_request_template.md`
   - `.github/PULL_REQUEST_TEMPLATE/*.md`

Rules:

- If a template exists, use it as the base structure and keep required headings.
- Fill only relevant sections; remove placeholder text.
- If multiple templates exist in `.github/PULL_REQUEST_TEMPLATE/*.md`, choose the best matching one for the change scope.
- If no template exists, use the size-based format rules below.

### Small PRs (< 50 lines changed)

Summary + Related Tickets. Skip everything else.

```markdown
## Summary

Change `POST /v1/quizzes/{quizId}/generate` to `GET /v1/quizzes/{quizId}/questions?profileId=uuid`. The endpoint is a read operation - not a create - so GET is semantically correct.

## Related Tickets / Issues

- [ORG-245](https://example.atlassian.net/browse/ORG-245)
```

### Medium PRs (50ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“400 lines changed)

Add Changes (grouped by area) and How to Test.

```markdown
## Summary

Unify `dailyTimeCommitment` field naming across all DTOs and responses, correct enum values, move `goalId` from profile entity to routine generation request body.

## Changes

- Renamed `DailyGoal` enum to `DailyTimeCommitment` with values 5, 15, 25
- Unified field name to `dailyTimeCommitment` across create, update, and response DTOs
- Added `goalId` as required field in `POST /routines/generate` request body
- Removed `goalId` / `goal` relation from `ProfileEntity` (+ schema migration dropping the column)

## Related Tickets / Issues

- [ORG-194](https://example.atlassian.net/browse/ORG-194)

## How to Test

- `yarn migration:run` to apply the migration
- `yarn test` - all 215 tests pass
```

### Large PRs (400+ lines changed)

Full template. Include Implementation Deviations when deviating from spec, and Notes for Reviewers for cross-cutting concerns or deferred scope.

```markdown
## Summary

[1-2 sentences - what changed and why]

## Changes

[Grouped by area with bold sub-headers. Each bullet is a concrete change, not a vague description.]

**Quiz entities**: `QuizEntity`, `QuestionEntity`, ...
**Quiz generate** (`POST /quizzes/:quizId/generate`): dynamically selects questions per category...

## Implementation Deviations from Spec

| Deviation                                | Rationale                                                        |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `GET /v1/subscription/offerings` removed | FE fetches offerings directly from the billing SDK on-device     |
| `billing_app_user_id` column omitted     | Spec defines it as `= account.id` - redundant copy adds no value |

## Related Tickets / Issues

- [ORG-151](https://example.atlassian.net/browse/ORG-151) - GET /v1/subscription
- [ORG-153](https://example.atlassian.net/browse/ORG-153) - feature_limits infrastructure and guards

## How to Test

- `yarn migration:run` then `yarn seed:run` to populate data locally
- `yarn test` - all tests pass
- Test endpoints via Swagger at `/api-docs`

## Notes for Reviewers

[Cross-cutting concerns, deferred scope with ticket links, decisions reviewers should weigh in on.]
```

## PR Rules

- One concern per PR - if the diff touches unrelated areas, split it
- Keep PRs reviewable - aim for under 400 lines of diff; if larger, explain why in Notes for Reviewers
- PR title must follow conventional commit format with JIRA ticket ID: `feat: [AB-123] description`
- Don't pad small PRs with empty template sections - Summary + Related Tickets is enough
- When deviating from spec, document the deviation AND the rationale in the table
- When deferring scope, link the follow-up ticket so reviewers know it's tracked
- Self-review the diff before requesting review
- For paginated database-backed query work, `How to Test` should include evidence that paginated/filtering behavior is verified through endpoint or repository tests

## Resolving Review Threads

When acting as the PR resolver after feedback has been left, follow this sequence for every review comment thread:

1. Process comments one-by-one (do not batch-resolve without per-thread replies).
2. Reply in-thread before resolving, with body prefixed exactly: `*resolver:* `.
3. Explicitly state disposition:
   - addressed (implemented now)
   - partially addressed (what changed vs what remains)
   - not addressed (clear rationale)
4. When addressed, include concrete proof (commit SHA, file path, or test command/results) so reviewers can verify quickly.
5. Resolve the thread only after the resolver reply is posted.
6. Leave the thread open if work is deferred, intentionally rejected, or still in progress.

Thread resolution message examples:

- `*resolver:* Addressed in 24271b8 by switching SessionService to constructor injection for consistency with module patterns. Re-ran lint and session/xp tests.`
- `*resolver:* Not addressed in this PR (out of scope). Tracked in ORG-999 for follow-up.`

## Authoring Rule

- Do not set or override git author/committer identity from the LLM workflow.
- Do not run `git commit --author ...`.
- Do not change git identity config during task execution.
- Do not add `Co-Authored-By:` or any other attribution trailer to commit messages (see Format Rules).

## Never Commit

The following files must never be staged or committed:

- **Technical specifications** (`docs/backend-spec-*.md`, `docs/client-spec-*.md`, `docs/internal-spec-*.md`) - specs are reference documents maintained outside version control. They may be gitignored. Do not `git add -f` to bypass ignore rules.
- **Secrets** (`.env`, `credentials.json`, API keys, tokens) - verify these are in `.gitignore`.

If the user explicitly asks to commit a spec file, warn them that specs are excluded by convention and confirm before proceeding.

## Safe Defaults

- Prefer explicit path staging over blanket staging.
- Run both `git diff` and `git diff --staged` before commit.
- Keep one logical change per commit.
- Never commit secrets; verify `.env` and credential files are ignored.

## Anti-Patterns

- Committing without reviewing staged diff.
- Using `git add --all` in a dirty tree without checking `git status` first.
- Relying on `.gitignore` to untrack already tracked files.
- Force-pushing shared branches unless explicitly required.
- Reading green checks without comparing the local and remote head commits first.
- Treating a `skipped` check as a pass without saying why the skip is by design.
- Waiting for CI with `gh pr checks --watch`, `gh run watch` or a sleep loop instead of `github_ci_wait`.
- Calling `github_ci_wait` again for a target whose first wait Claude Code moved to a background task (the result arrives as a notification).
- Merging on anything but a `CI PASS` for that pull request, or treating `CI NO CHECKS` or `CI STOPPED` as a pass.
- Leaving the CI gate on `CI NO CHECKS` on the strength of an empty check list, without comparing the changed files with the workflows' path filters and confirming the expected workflow is enabled.
- A `claude -p` worker making a `github_ci_wait` call longer than 1 minute, or continuing a wait without the `waitStartedAt` the first result printed.
- Dumping `gh run view --log` or a whole large diff into the context instead of `--log-failed`, `--name-only` and capped reads.
- Committing technical specification files (`docs/*-spec-*.md`) - these are reference documents, not versioned source code.
- Using `git add -f` to bypass `.gitignore` rules without explicit user confirmation.

## Rules

- Branch before significant edits.
- Stage intentionally.
- Review unstaged and staged diffs.
- Commit small, focused changes.
- Prefer `type: description` commit headers with no scope.
- Never add `Co-Authored-By:` or any other attribution trailer to a commit message.
- Push with upstream on first publish.
- Every remote GitHub operation goes through `gh`; pass `--repo` when the working directory might not be the target.
- Read CI only after confirming the pull request head is the commit you mean.
- Wait for CI with `github_ci_wait`; merge only after its `CI PASS` for the pull request (or a `CI NO CHECKS` whose changed files the workflows' path filters exclude, with the expected workflow enabled), with `--match-head-commit`.

## Easter Eggs

These are silent, lightweight additions woven into normal PR output. Never announce them - they should feel like a discovery, not a feature.

### March 10 (Mario Day)

When creating or updating a PR on March 10 (local date), append a single italicised line to the very end of the PR description body:

```
_Happy Mario Day. Wahoo!_
```

Keep it subtle. One line only.

## Monorepo-Only Addendum (Turbo/workspaces + `apps/`/`packages/`)

Apply this section only when all are true:

- the target repository is a Turbo/workspace monorepo
- the repository has an `apps/` and/or `packages/` folder at root
- migration scripts are app-scoped

Run migrations from the app workspace, not from repo root unless root script exists:

```bash
cd apps/<app-owning-typeorm>
yarn migration:run
```

Example for a backend monorepo, where the Drizzle migrations live in their own `apps/script-migrations` app:

```bash
cd apps/script-migrations
pnpm migration:run
```
