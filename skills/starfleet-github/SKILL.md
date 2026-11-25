---
name: starfleet-github
description: "GitHub PR/CI/backport workflow via `starfleetctl github`. Comms/task core lives in the **`starfleet`** and **`starfleet-tasks`** skills; flagship-PR conventions for the xserver repos follow the workspace PR-workflow rules."
---
# starfleet-github ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â GitHub interaction

GitHub PR/CI/backport workflow via `starfleetctl github`. Comms/task core lives in
the **`starfleet`** and **`starfleet-tasks`** skills; flagship-PR conventions for the
xserver repos follow the workspace PR-workflow rules.

## PR-branch ownership

Every clone pushes to the **same GitHub PR branch** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â claim it before mutating:

```bash
starfleetctl github pr claim <pr#> "what"             # claim PR branch
starfleetctl github pr claim --release <pr#>          # release claim
```

**Isolation: machine erzeugt Clone/Worktrees IMMER ÃƒÆ’Ã‚Â¼ber das Tooling**, nie roh per
`git worktree`/`git clone`:
- `starfleetctl github pr checkout <pr#>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â isolierter Agent-Clone fÃƒÆ’Ã‚Â¼r Reparatur/Review
  (git gibt den Clone-Pfad aus; der geht 1:1 in `github pr amend-push <pfad>`).
- `starfleetctl github pr mk-agent-clone <branch> [name]` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â benannter agent-owned Clone.
- Allgemeine, nicht-PR temporÃƒÆ’Ã‚Â¤re Worktrees: `starfleetctl worktree add|list|remove|prune`
  (siehe `starfleet-sessions`-Skill).
- Mutierende Work im selben Clone mit `starfleetctl with-clone-lock <cmd...>` serialisieren.

## Read-only

| Subcommand | Purpose |
|---|---|
| `github pr view <pr#>` | PR metadata via gh |
| `github pr ci <pr#\|URL>` | CI status classified by conclusion |
| `github pr file-on-branch <branch> <path>` | Fetch a file from any branch/tag/commit |
| `github pr wait-green <pr#>` | Poll CI checks until all pass/fail/timeout |
| `github pr job-logs <pr#>` | Download CI job logs for failure analysis |
| `github pr show-branch-file <ref> <path>` | Print file at any ref via GitHub API (deprecated, use file-on-branch) |
| `github backport applies <path> <grep-ERE> [release...]` | Check applicability across release lines |

## Mutating

| Subcommand | Purpose |
|---|---|
| `github pr comment <pr#> <body-file>` | Post PR comment |
| `github pr label <pr#> add\|remove` | Add/remove labels |
| `github pr set-body <pr#> <body-file>` | Replace PR body |
| `github pr checkout <pr#>` | Isolated clone for PR repair |
| `github pr amend-push <clone-dir>` | Amend + force-push |
| `github pr make <commits>` | Submit PR from commits |
| `github backport commit <release> <commit>` | One-shot backport |

## Quick reference

```bash
starfleetctl github pr make <commit> [<commit> ...]   # submit PR from incubator
starfleetctl github pr mk-agent-clone <branch> [name] # agent-owned clone
starfleetctl github pr claim <pr#> "what"              # claim PR branch
starfleetctl github pr claim --release <pr#>           # release claim
starfleetctl github backport commit <release> <commit> # one-shot backport
starfleetctl with-clone-lock <cmd...>                  # serialize mutating work
```

## Known limitations

- `github backport commit` path-remap uses project config for prefix/behavior.