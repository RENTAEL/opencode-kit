---
name: git-hygiene
description: "Treat version-control state as user data. Mutate only the parts required by the requested git workflow."
---
# Git Hygiene

Treat version-control state as user data. Mutate only the parts required by the requested git workflow.

## Establish Authority

- Inspect status, staged and unstaged diffs, untracked files, current branch, upstream, and recent message conventions before mutation.
- Do not create or switch branches, stage, commit, fetch, pull, push, amend, rebase, or delete unless the user's request requires that action.
- Resolve exact targets and preserve unrelated or pre-existing work. Never use blanket staging when the worktree is mixed.

## Stage and Commit

1. Stage explicit files or hunks that form one logical change.
2. Inspect the staged diff for scope, debug artifacts, generated files, large binaries, submodule changes, credentials, tokens, private data, and unsafe configuration.
3. Keep commits atomic. Separate structural changes, behavior changes, generated output, and unrelated fixes when the workflow allows.
4. Follow repository message conventions. Use an imperative summary and explain non-obvious reasons, risks, or compatibility decisions in the body.
5. Report the resulting commit and anything deliberately left unstaged.

## Remote and History Safety

- Fetch, pull, merge, or push only when requested or when an explicitly authorized workflow cannot continue without it. Explain any new remote state before integrating it.
- Require explicit confirmation of the exact destructive command and impact before force push, hard reset, clean, checkout or restore that discards work, branch deletion, or shared-history rewrite.
- Prefer `--force-with-lease` over an authorized force push and `revert` over resetting shared history.
- Read both sides of conflicts and preserve both intents where compatible. Verify the semantic result after resolution.
- Offer recovery through `reflog`, a backup branch, stash, or patch before destructive recovery, but do not create or apply them without authority.
