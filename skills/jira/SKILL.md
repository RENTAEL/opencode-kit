---
name: jira
description: "Bridge natural language to a Jira CLI. Portable across users, projects, instances, and auth models ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never hardcode project keys, usernames, servers, tenant hostnames, or board IDs."
---
# Jira CLI

Bridge natural language to a Jira CLI. Portable across users, projects, instances, and auth models ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never hardcode project keys, usernames, servers, tenant hostnames, or board IDs.

A user may have **more than one Jira instance** configured on their machine (e.g. an on-prem/Server/DC instance alongside a separate Cloud tenant), each requiring a different tool and reachable through a different local alias or shell function. Work phases in order for each request. Skip only phases marked optional when their precondition is unmet.

## Phase 0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Pick the right CLI / instance (multi-instance setups only)

Skip this phase entirely if only one Jira CLI is configured ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â go straight to Prerequisites below.

If more than one is configured:

1. **Detect what's available** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check for both tools before assuming: `command -v jira`, `command -v acli`, and any wrapper shell functions/aliases the user has defined for each instance. List candidates rather than guessing a name: `alias | grep -i jira` and `declare -f | grep -i jira` (or `type -a` per candidate name) to surface anything ending in or containing `jira` (e.g. a `*jira` naming pattern like `ckjira`/`workjira`). If that turns up more than one, ask the user which maps to which instance rather than assuming from the name alone. Do not hardcode specific alias names in the skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they are user-chosen and machine-specific.
2. **Match the request to an instance** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use whatever the user's project/team/board convention already implies (explicit project key prefix, current repo, or a stated instance name). If ambiguous and more than one instance plausibly applies, ask once rather than guessing which instance a write should land on.
3. **Auth model determines the tool, not preference** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is a hard technical constraint, not a style choice:
   - An instance that accepts classic API-token **basic or bearer auth** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use `jira` (jira-cli). Config typically lives at a path set by `JIRA_CONFIG_FILE` or `~/.config/.jira/*.yml`; a multi-instance setup may keep one config file per instance and select between them via that env var or a wrapper function.
   - An instance whose Jira Cloud tenant **enforces OAuth** (classic token Basic/Bearer auth returns 401/403 regardless of token freshness ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is an org-wide Atlassian security policy on that tenant, not an expired-token problem) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ jira-cli's `--auth-type basic|bearer|mtls` cannot authenticate at all; use `acli` instead, which has a native OAuth 2.0 login flow. See `references/acli-jira.md`.
   - If unsure which category an instance falls into, `jira me` (or the equivalent auth-status check for the wrapper in use) failing with a 401/403 on a freshly verified token, or an error mentioning OAuth/Connect Session Auth, is the signal to switch tools rather than keep retrying token regeneration.
4. **Never mix command grammars** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â jira-cli and acli have different flag shapes for the same intent (positional issue key vs. `--key`, different flag names). Once you've picked a tool for this request, use only that tool's syntax for the rest of the exchange. jira-cli syntax is documented inline below and in `references/{examples,jql,formatting,transitions}.md`; acli syntax is documented in `references/acli-jira.md`.

## Prerequisites (fail fast)

```bash
command -v jira >/dev/null || { echo "jira CLI missing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â install ankitpokhrel/jira-cli"; exit 1; }
jira me >/dev/null 2>&1 || { echo "jira not authenticated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run: jira init"; exit 1; }
```

On failure: report the exact fix (`brew install jira-cli` / `jira init`) and STOP. Do not invent issue keys or statuses. If this instance is actually an OAuth-only Cloud tenant (see Phase 0), the fix is switching to `acli`, not retrying `jira init` with a new token.

Optional tools: `jq` (JSON field extract), `pandoc` (MarkdownÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢Jira wiki for descriptions/comments). If missing, prefer `--plain` text or pass simple plain text bodies.

The rest of this file (Phases 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4) documents **jira-cli** specifically. For **acli**, see `references/acli-jira.md`, which mirrors this same phase structure for that tool's command grammar.

## Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Resolve context

Establish **active issue key**, **project**, and **acting user** before writes.

1. **Issue key** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Prefer explicit key in the user message (`[A-Z][A-Z0-9]+-\d+`). Else parse current git branch (`feat/PROJ-123-ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`, `PROJ-123-ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`). Else search (Phase 2). Never invent keys.
2. **Project** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Explicit `-p KEY` / user text wins. Else default from config (`jira` uses `~/.config/.jira/.config.yml`, override with `JIRA_CONFIG_FILE`). For another project always pass `-p KEY` or JQL `project = KEY`.
3. **User** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `ME=$(jira me)` for "me" / "my". Assignees accept email or exact display name; self-assign: `jira issue assign KEY "$(jira me)"`.
4. **Session memory (optional)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â If a memory tool exists, read/write active key as `JIRA_ACTIVE_KEY`. If none, keep the key in conversation only. Do not require serena/openmemory.

Completion: you can name the target key and/or project, or you are about to search with an explicit JQL/filter plan.

## Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Read (prefer structured output)

| Goal | Command |
|------|---------|
| View one issue | `jira issue view KEY --plain` (human) or `jira issue view KEY --raw` (JSON) |
| List / search | `jira issue list [flags] --plain` or `--raw` |
| My open work | `jira issue list -a"$(jira me)" -s~Done --plain --columns key,status,summary,priority` |
| Recent | `jira issue list --history --plain` |
| Cross-project JQL | `jira issue list -q'project IS NOT EMPTY AND ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦' --plain` |
| Sprint issues | `jira sprint list --current --plain` (needs board in config) |
| Epics | `jira epic list --table --plain` |

**Rules**
- Use `--plain` or `--raw` in agents ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never the interactive TUI.
- There is **no** `--output json`. JSON is `--raw`.
- Default list is **project-scoped** to config project. Broaden with `-p` or `-q`.
- Paginate: `--paginate 0:50` (max 100/page).
- With `--raw` + `jq`, extract only needed fields. List items look like `{key, fields:{summary,status:{name},assignee:{displayName},issueType:{name},ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦}}`. View `--raw` uses standard Jira API issue JSON (`fields.status.name`, etc.).
- Do not dump full JSON into chat.

Common list flags: `-tType` `-sStatus` (repeatable; `-s~Done` = not Done) `-aAssignee` `-rReporter` `-yPriority` `-lLabel` `-q'JQL'` `--updated week`.

Deep JQL: load `references/jql.md` only if needed.

## Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Write (confirm first)

**Confirm with the user before any create, edit, comment, assign, transition, delete, or bulk change.** One confirmation can cover a stated batch. Reads need no confirmation.

Always pass non-interactive flags where available (`--no-input` on create/edit/comment).

| Action | Command |
|--------|---------|
| Create | `jira issue create -tTYPE -s"Summary" -b"Body" --no-input` (`-pKEY` if not default) |
| Edit | `jira issue edit KEY -s"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦" -b"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦" --no-input` |
| Comment | `jira issue comment add KEY "body"` or `--template -` / `--template FILE` |
| Assign | `jira issue assign KEY "email-or-name"` or `KEY "$(jira me)"` Ãƒâ€šÃ‚Â· unassign: `KEY x` |
| Transition | `jira issue move KEY "State Name"` |
| Delete | `jira issue delete KEY` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â extra explicit confirm |

### Formatting (descriptions / comments)

Jira wiki ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  Markdown. If body has headings, lists, or code and `pandoc` exists:

```bash
body=$(printf '%s\n' "$MARKDOWN" | pandoc -f gfm -t jira)
jira issue comment add KEY "$body" --no-input
# or: printf '%s\n' "$body" | jira issue comment add KEY --template -
```

Else use short plain text (no reliance on MD rendering). Details: `references/formatting.md`.

### Transitions (no `--list` flag)

`jira issue move` has **no** `--list`. Target state is the **transition name** for that workflow (instance-specific).

1. Read current status: `jira issue view KEY --plain` (or `--raw` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.fields.status.name`).
2. Prefer the exact state name the user asked for (quote spaces: `"In Progress"`).
3. On error, show the CLI error, suggest common names (`In Progress`, `Done`, `To Do`, `Backlog`) or ask the user for the exact workflow transition ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent transition IDs.
4. Optional: comment while moving: `jira issue move KEY "Done" --comment "ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"`.

Details: `references/transitions.md`.

## Phase 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Report

After each mutating command: state key, action, new status/assignee if known. On failure: paste the CLI error, what you tried, and the next safe step. Never claim success without a successful command exit.

## Anti-patterns

- Inventing issue keys, projects, or statuses
- Interactive TUI (`jira issue list` without `--plain`/`--raw`)
- `jira issue move KEY --list` (invalid flag)
- `--output json` (use `--raw`)
- Hardcoding one company's project/board/username into commands
- Bulk edit/delete without confirmation
- Dumping raw multi-issue JSON into the user chat
- Mixing jira-cli and acli flag syntax in the same command, or guessing acli flags by analogy to jira-cli (they differ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `references/acli-jira.md`)
- Retrying token regeneration against an OAuth-only Cloud tenant instead of switching tools (Phase 0)

## Examples

**User:** "my open tickets"
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `jira issue list -a"$(jira me)" -s~Done --plain --columns key,status,summary,priority --paginate 0:50`

**User:** "show ACME-42"
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `jira issue view ACME-42 --plain`

**User:** "comment on ACME-42: fixed in abc123" (after confirm)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ pandoc (if needed) then `jira issue comment add ACME-42 "ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦" --no-input`

**User:** "move ACME-42 to In Progress" (after confirm)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `jira issue move ACME-42 "In Progress"`

**User:** "bugs in project OPS filed by me last week"
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `jira issue list -pOPS -tBug -r"$(jira me)" --created week --plain --columns key,status,summary`

More: `references/examples.md`.
