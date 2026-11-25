---
name: starfleet-tasks
description: "Task handling in the fleet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â capture-first, mandatory lifecycle, dashboard rules, reports. Commands/comms/concurrency core lives in the **`starfleet`** skill."
---
# starfleet-tasks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â task capture, dashboard, reports

Task handling in the fleet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â capture-first, mandatory lifecycle, dashboard rules,
reports. Commands/comms/concurrency core lives in the **`starfleet`** skill.

## Task capture

Record a task in the dashboard, optionally commission a ship. **This only commands ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
never execute the task yourself.** No direct file access to
`dashboard/topics/*.md`.

### The one-liner

```sh
starfleetctl task capture --title "<title>" \
    [--desc "<what needs doing>"] \
    [--slug "<override>"] \
    [--assign [<ship>]] \
    [--category <cat>] \
    [--no-push]
```

- `--assign` (no name) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ routes to the flagship, which delegates or executes it
- `--assign <ship>` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ that specific ship
- Without `--assign` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ recorded as open, no ship

## Managing existing tasks

```sh
starfleetctl task assign <slug> [<ship>] [--no-push]   # re-assign
starfleetctl task unassign <slug> [--no-push]          # clear assignment
starfleetctl task status <slug> <status> [--no-push]   # set status
starfleetctl task rm <slug> [--no-push]                # delete a task topic
starfleetctl task purge [--no-push]                    # delete ALL done tasks
starfleetctl task orphans [--json]                     # tasks assigned to vanished ships
```

## Working a task (mandatory cycle)

When you **take on / work a task**, the following applies to every session:

1. **Capture-first.** Every non-trivial task lands in the dashboard **first** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â even a
   task you were handed over comms or that you'll finish immediately. There is no "just
   do it without a task": capture it (`task capture`), attach to it, and move it through
   the lifecycle below. Trivial one-off work (a quick reply, a status update) is "working"
   via `comms status working --note "<what>"`, not a full task.
2. **TASK-LIFECYCLE (begin ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ log/progress ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ done).** Drive the dashboard status,
   the work-log, and your board status together with the lifecycle commands:
   ```sh
   starfleetctl task begin <slug>                     # status=in-progress + comms working
   starfleetctl task log <slug> "<what you did>"      # timestamped work-log entry
   starfleetctl task progress <slug> <0-100> [note]   # progress + log + comms working
   starfleetctl task done <slug>                      # status=done + comms idle
   ```
   `task begin` on a task assigned to *you* sets in-progress and flips your board to
   `working`; use it the moment you start, keep the log/progress current as you go, and
   `task done` when finished.
3. **Board status reflects reality.** `task begin`/`progress`/`done` already keep your
   board status in sync. For work outside a task, call
   `starfleetctl comms status <working|blocked|idle> "<what you're doing>"` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the fleet board
   must always show where you are. A `working`/`building` status with **no task and no note**
   is flagged **unattached** (you get a loud hint + the board shows a warning badge); attach to
   a task or add a `--note`, never silently work unattached.
4. **Finish = report.** When a task is complete, submit a structured report
   (`starfleetctl reports submit "<Title>" --body ... --task-ref <slug>`) **and** notify
   the commissioning ship via comms. "Done" is not done until both exist.
5. **Questions you must ask back** (ambiguity, missing info, decisions needed):
   - Record the open questions **in the task itself** (`dashboard topic write <slug> <file>`
     + `dashboard topic commit <slug>`), so the praetor/assigner can answer asynchronously.
   - Then submit a report whose **subject explicitly says questions need answering**
     (e.g. `"Task <slug>: RÃƒÆ’Ã‚Â¼ckfragen mÃƒÆ’Ã‚Â¼ssen beantwortet werden"` / "questions need answers"), and **list the questions in the report body**.
   - Do **not** block the session waiting on the console ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â route questions through comms
     and continue with whatever part of the task you can already do.

> **Interrupted tasks.** If a ship dies mid-task (heartbeat expiry), a periodic
> `sweep-stale` marks its open tasks **interrupted** (assignment kept). A returning ship
> resumes such a task with `task begin <slug>`.

## Dashboard

The dashboard is the cross-session "what's in flight" index.

> **ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â RULE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â CLI only, never raw files.** All dashboard access goes through the
> `starfleetctl dashboard` / `starfleetctl task` subcommands. **NEVER** use file tools
> (`Read`/`Edit`/`Write`/`Glob`/`Grep`) on `dashboard/topics/*.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
> not even to "just look". Direct file access is a **rule violation** (a fleet agent
> once read the dashboard files directly instead of using starfleetctl; it is how the
> cross-session index gets clobbered). If you want to read a topic, use
> `dashboard topic show <slug>`; to list them, `dashboard topic list --json`; to modify,
> `dashboard topic write <slug> <file>` + `dashboard topic commit <slug>`.

### Topic file format (frontmatter)

Topic files in `dashboard/topics/<slug>.md` use YAML-ish frontmatter:

```yaml
---
title: "My Task"
category: active       # "active" or "parked"; defaults to "active" when missing
kind: "task"           # optional; marks it as a schedulable task
status: "open"         # active only: open/assigned/done/...
assigned-to: "ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â"       # ship name or "ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â"
tags: "starfleet"      # optional, comma-separated
---
```

Only `title` is required ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `category` defaults to `active`, all other fields
are optional. This is intentional for hand-written topics: you can drop in a
minimal file and it shows up in the active list automatically.

**List topics always via `dashboard topic list --json`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â there is **no**
`dashboard list` subcommand; `dashboard list` is the wrong/invalid command and
returns `dashboard: unknown command: list`.

| Command | Purpose |
|---|---|
| `dashboard show` | Render the whole dashboard (Active + Parked) from the topic files |
| `dashboard topic list --json` | List all topics (JSON, for filtering) |
| `dashboard topic list` | List all topics (human-readable) |
| `dashboard topic new <slug>` | Create a topic |
| `dashboard topic write <slug> <file>` | Write topic content |
| `dashboard topic commit <slug>` | Commit + push topic |

## Reports

Submit and query structured fleet reports (test results, build summaries, CI
status, etc.) via CLI or web UI. Each report has a title, optional subtitle,
Markdown body, tags, a dashboard task reference, and file attachments.

### Key commands

```sh
starfleetctl reports submit "Title" \
    --subtitle "one-liner" \
    --body "Markdown body text" \
    --body-file path/to/log \
    --tags "ci,build" \
    --task-ref xlibre/some-task \
    --attachment path/to/file

starfleetctl reports list                          # newest first
starfleetctl reports list --ship Enterprise        # by ship
starfleetctl reports list --tag ci --json          # filter + JSON
starfleetctl reports show <id>
starfleetctl reports delete <id>
```

ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â **WARNING**: The title is the **first positional argument**, not a `--title`
flag! Using `--title ...`/`--help`/`--` as the first argument is now **rejected**
with a usage error (no junk report is created), so never pass any `-`-prefixed
value as the title.

`--body-file -` reads the body from **stdin** (e.g.
`starfleetctl reports submit "Title" --body-file - < log.txt`).

Attachments are uploaded to the filestore (`file put` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/api/store/<name>`).
See `doc/reports.md` for full reference and web UI walkthrough.