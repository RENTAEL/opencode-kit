---
name: starfleet-sessions
description: "Spawning and managing ships, isolated worktrees, and the fleet web console. Comms/task core lives in the **`starfleet`** and **`starfleet-tasks`** skills."
---
# starfleet-sessions ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ship sessions, worktrees, web console

Spawning and managing ships, isolated worktrees, and the fleet web console.
Comms/task core lives in the **`starfleet`** and **`starfleet-tasks`** skills.

## Ship sessions

| Subcommand | Purpose |
|---|---|
| `run [--flagship\|--name <id>] [--client claude\|opencode]` | Start an AI ship session |
| `session list` | List running detached sessions |
| `session attach <id>` | Attach terminal to a detached session |
| `session stop <id>` | Kill a detached session + release ship name |

Background ships never prompt on their console (see the starfleet-instructions working
practices) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hand them a task via the dashboard/comms, not as extra CLI args.

**Rule: `session stop` is only for detached ships.** Check the launch type first
(`starfleetctl session list`). Only `background` and `auto` ships may be stopped ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a ship
launched with launch type `terminal` has a human at that console and must be left running;
report it via comms so the praetor can stop it by hand. This includes respawns of a stuck
console ship: no autonomous `session stop`.

## Git worktrees

**Rule: Worktrees & agent clones werden IMMER ÃƒÆ’Ã‚Â¼ber starfleetctl verwaltet, nie direkt
`git worktree` / `git clone` / `mkdir` in einen Repo-Nachbarn.**

| Subcommand | Purpose |
|---|---|
| `worktree add <repo-path> [name] [--from <ref>] [--branch <existing-branch>]` | Create an isolated per-task worktree |
| `worktree list [repo-path]` | List worktrees (all, or for one repo) |
| `worktree remove <repo-path> <name> [--force] [--keep-branch]` | Remove worktree (and its `wt/<name>` branch unless `--keep-branch`) |
| `worktree prune [repo-path]` | Prune stale worktree entries |
| `github pr checkout <pr#> [name]` | Isolated agent clone/worktree for a **specific PR** (repair/review) |
| `github pr mk-agent-clone <branch> [name]` | Agent-owned clone for a PR branch |

**Mechanics (starter):**
```bash
starfleetctl worktree add  _WORK_/xserver-master/sources/xlibre/xserver mytask        # -> _WORK_/worktrees/xserver/mytask, branch wt/mytask (from origin/HEAD)
starfleetctl worktree add  _WORK_/starfleetctl/sources/starfleetctl myfix --from master
starfleetctl worktree list _WORK_/xserver-master/sources/xlibre/xserver
starfleetctl worktree remove _WORK_/xserver-master/sources/xlibre/xserver mytask      # cleans wt/mytask too
```

**Why starfleet tooling and not raw `git worktree`:**
- Standardized location `_WORK_/worktrees/<repo-basename>/<name>` (inside the workspace/`_WORK_`, cleaned up consistently), default branch `wt/<name>`, and `remove` also drops the branch ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â so no orphan state accumulates across ships.
- `github pr checkout` / `mk-agent-clone` wire the clone to the PR branch correctly (and are what PR repair/review skills expect back: `github pr amend-push <clone-dir>` takes the printed clone dir).
- Concurrent **mutating** git operations on a shared clone are serialized separately via
  `starfleetctl with-clone-lock <cmd...>` (flock on `<gitdir>/mpbt-clone.lock`, same lock `ws-commit`
  uses) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â wrap push/amend/ws-commit-style ops that run inside a shared checkout.
- Raw `git worktree`/manual clones bypass all of this ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ unknown locations, orphan branches, and
  races with other ships. For anything temporary: `worktree ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`; for PR work: `github pr ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`.

**Where checkouts may (only) live:** mpbt-managed clones (`_WORK_/<solution>/sources/**`),
starfleet worktrees (`_WORK_/worktrees/<repo>/<name>`), and PR/agent clones from `github pr checkout` /
`mk-agent-clone`. **Never** `git checkout`/`git clone` into the workspace root (clobbers the
agent-config checkout), into `_WORK_/tmp`, or into ad-hoc directories next to a repo.

**Toplevel guard (before ANY mutating git command):**
```bash
git rev-parse --show-toplevel   # must equal the INTENDED repo, e.g. ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦/_WORK_/xserver-master/sources/xlibre/xserver
```
The workspace root itself is a git repo (agent-config) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `git checkout <xserver-branch>` there
switches/creates branches in the **wrong** repo (footgun: `wip/*`, `wt/*`, `xserver/*` refs have
landed there), and `worktree add` run from the root creates a worktree **of the workspace repo**.
Always pass the explicit repo path to `worktree add` and verify the printed destination is under
`_WORK_/worktrees/<repo>/<name>`.

**Primary clone is passive:** branch switching / rebase / amend / force-push prep happen only in your
own worktree or PR clone, never in the shared mpbt clone (other ships build/read there; a visible
`[wt/ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦]`/`[wip/ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦]` branch in the *wrong* repo is a red flag).

## Web console & setup

| Subcommand | Purpose |
|---|---|
| `web start/stop/restart/autostart` | Fleet web console (mobile-first) |
| `genesis-init [dir]` | Bootstrap a workspace from nothing |
| `self-install` | Clone/pull + build + symlink starfleetctl |
| `sop install-starfleet` | Install/update SOP fragments and skills |

## Deployment

```bash
# Phase A: genesis (from an existing binary)
starfleetctl genesis-init .

# Phase B: bootstrap (from the committed script)
./starfleet-bootstrap
```

Everything under `.starfleet-ai/` is gitignored. Re-run `./starfleet-bootstrap` anytime to update.

## Wichtige Erinnerung: Modell-Proxy niemals direkt killen

Bei Arbeiten am starfleetctl model-proxy NIEMALS den Prozess direkt mit `kill`, `pkill` oder `systemctl stop` beenden.
STETS den offiziellen Befehl verwenden: `./.starfleet-ai/bin/starfleetctl model-proxy restart`

**Warum:** Direktes Killen kann zu inkonsistenten ZustÃƒÆ’Ã‚Â¤nden fÃƒÆ’Ã‚Â¼hren, Ressourcen nicht korrekt freigeben und zu Problemen fÃƒÆ’Ã‚Â¼hren.
Der offizielle restart Befehl stellt sicher, dass alle Ressourcen korrekt behandelt werden.

Dies gilt besonders im Zusammenhang mit `session stop` - selbst wenn du eine ship session beenden mÃƒÆ’Ã‚Â¶chtest,
sollte der model-proxy nie direkt gekillt werden, sondern immer ÃƒÆ’Ã‚Â¼ber den offiziellen restart Befehl neu gestartet
werden, falls eine ÃƒÆ’Ã¢â‚¬Å¾nderung an der model-proxy Config oder am Code nÃƒÆ’Ã‚Â¶tig ist.

Die korrekte Vorgehensweise bei model-proxy ÃƒÆ’Ã¢â‚¬Å¾nderungen:
```sh
cd _WORK_/starfleetctl/sources/starfleetctl
make all                    # baut Binary neu
./starfleet-bootstrap       # deployed Binary + installiert Fragmente
./.starfleet-ai/bin/starfleetctl model-proxy restart  # startet Proxy mit neuer Config/Code neu
```

FÃƒÆ’Ã‚Â¼r reine Config-ÃƒÆ’Ã¢â‚¬Å¾nderungen (yaml) reicht `model-proxy restart` aus.
FÃƒÆ’Ã‚Â¼r Go-Code-ÃƒÆ’Ã¢â‚¬Å¾nderungen muss das Binary neu gebaut und deployed werden.
