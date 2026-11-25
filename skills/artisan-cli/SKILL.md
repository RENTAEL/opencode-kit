---
name: artisan-cli
description: "This skill is a reference, not a workflow ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the workflow packs (`/artisan-scan`, `/artisan-serve`, `/artisan-scaffold`, `/artisan-implement`, `/artisan-architect`, `/artisan-status`) tell you *when* to run what. Load this one when you need exact flags, config ..."
---
> `artuml` may not be on PATH in some shells. If any `artuml` command fails with "not found", silently retry it as `npx --yes artisan-uml-cli <command> (or pnpm dlx artisan-uml-cli <command>)`. Never report Artisan as not installed.

# artuml CLI reference

This skill is a reference, not a workflow ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the workflow packs (`/artisan-scan`, `/artisan-serve`, `/artisan-scaffold`, `/artisan-implement`, `/artisan-architect`, `/artisan-status`) tell you *when* to run what. Load this one when you need exact flags, config paths, or file semantics.

## Commands

Run in the project root (the directory that owns `.artisan/`).

| Command | Notes |
|---------|-------|
| `artuml scan [--src DIR]` | parse code ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.artisan/`; merges with prior diagram (ids stable); seeds `config.json`; editor copy requires network only on first install |
| `artuml serve [--port N]` | live editor at `localhost:4173` (default); autosave PUTs to `diagram.json`; spawn with `ARTISAN_NO_BROWSER=1` to skip opening a browser |
| `artuml diff [--json] [--peek]` | human changes since AI last looked. Consuming: advances `last-ai.json`. `--peek`: prints the same report, advances nothing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use in status-style checks |
| `artuml impl-diff` | diagram vs actual code (read-only); missing-from-code ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ implement, code-not-in-diagram ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask human |
| `artuml mark-ai` | call after the AGENT edits the diagram (CLI edits or last-resort direct edit): queues its changes as amber `pending` refs for human review AND records them as AI-known ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â then the next `diff` never misreports them as human changes |
| `artuml ack [keys...]` | human confirmed pending changes (or the editor's "Mark seen" button) |
| `artuml reject [keys...]` | human reverted pending AI changes |
| `artuml status` | tree sizes + unseen human changes (shown as a peek, always non-consuming) + first pending refs |
| `artuml add/edit/remove node\|member\|edge ...` | surgical CLI edits (human-attributed). See `artuml help edit` |
| `artuml editor` / `artuml app` | build/open embedded editor |
| `artuml help [topic]` | topics: scan, serve, diff, impl-diff, mark-ai, ack, status, add, edit, remove, editor |

## Config

Two JSON files, deep-merged ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **project wins over global** over built-in defaults:

| File | Scope | Written by |
|------|-------|-----------|
| `.artisan/config.json` | this project | `scan` seeds it with defaults if missing; edit freely |
| `~/.config/artuml/config.json` | the machine | you, by hand |

Keys: `askBeforeRemove` (default `true` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â scaffold/implement must prompt before removing code), `autoServe` (default `false` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when `true`, every `artuml` command ensures the editor server is running on port 4173).

Read config as `JSON.parse(fs.readFileSync('.artisan/config.json'))` with a fallback to the global file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or just look it up before deciding; do not create config files outside `artuml scan`.

## `.artisan/` files

| File | Role |
|------|------|
| `diagram.json` | source of truth; the editor autosaves here |
| `diagram.puml` | PlantUML mirror for quick reading |
| `last-ai.json` | baseline of what the AI last consumed/produced ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `diff` compares against it |
| `last-human.json` | baseline of what the human last acked ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `mark-ai` compares against it |
| `pending.json` | amber refs awaiting human review (AI + human edits both) |
| `config.json` | settings (see Config) |
| `impl-diff.json` | last impl-diff summary badge; also embedded in `diagram.html` |
| `diagram.html`, `editor/` | self-contained editor |

## Language support

The scanner speaks **C#** only today (Unity-friendly). Work in whatever stack
the project actually has for code edits; only the automatic diagram extraction
is C#-only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a new language plugs into the CLI's shared extractor
(`lib/extract.mjs`).

## Rules of engagement

- Only `diff` (without `--peek`) consumes the human-change report. `--peek` and `status` never change state.
- AI diagram edits ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run `artuml mark-ai` right after.
- Direct edits to `diagram.json` are a last resort ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â prefer `add`/`edit`/`remove` and the editor.
