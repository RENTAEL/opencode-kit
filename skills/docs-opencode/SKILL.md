---
name: docs-opencode
description: "Reference for OpenCode 2.0.21, so questions about configuration, CLI, agents, tools, providers and extensibility can be answered without searching the web. Most opencode.ai/docs pages and the upstream `dev` branch still describe 1.x; v2 documentation lives under `https://openc..."
---
# OpenCode Platform Reference (2.0.21)

## Purpose

Reference for OpenCode 2.0.21, so questions about configuration, CLI, agents, tools, providers and extensibility can be answered without searching the web. Most opencode.ai/docs pages and the upstream `dev` branch still describe 1.x; v2 documentation lives under `https://opencode.ai/v2/docs/`. When this file and a 1.x page disagree, this file wins.

## Architecture

- One shared background server per user account owns sessions, configuration, integrations, permissions and tool execution. Every local client (TUI, `opencode mini`, `opencode run`, desktop, web) connects to it. `--standalone` starts a private server instead; `--server <url>` targets a specific one.
- `opencode service start|restart|status|stop|get|set|unset` manages the service. `opencode service set disabled true` makes private servers the default.
- The server exposes an OpenAPI HTTP API (`opencode serve`, default password from `OPENCODE_PASSWORD` or `OPENCODE_SERVER_PASSWORD`). `@opencode/client` is the TypeScript client. `opencode pair` prints one-time links (valid 5 minutes, single use) that sign a browser or app in.
- Providers go through the AI SDK, with the model catalogue from models.dev. Storage is SQLite (`opencode.db`).
- Configuration is scoped to a location (a directory plus its project). Changes reload without restart; `opencode reload` forces it, and running sessions continue with fresh services at the next step boundary.

## Paths and storage

`opencode debug paths [db|home|data|config|cache|state|tmp|bin|log|repos]` prints them. Defaults follow XDG: config `~/.config/opencode`, data `~/.local/share/opencode`. `OPENCODE_CONFIG_DIR` overrides the config directory and `OPENCODE_DB` the database path (relative values resolve under the data directory, `:memory:` is allowed).

- Sessions live in the `session_v2` and `session_message` tables of `opencode.db`.
- Credentials live in the `credential` table of the same database. `auth.json` is no longer the store: a one-time migration imports it only when an existing v1 database is upgraded, a fresh install imports nothing, and later edits to it are never read. Write a credential with `/connect`, `opencode auth login` (the secret prompt needs a terminal) or `opencode auth import`.
- `opencode session export|import` moves sessions as JSON (`export --sanitize` redacts).

## Configuration

JSON or JSONC, files named `opencode.json` or `opencode.jsonc`, schema `https://opencode.ai/config.json`. `{env:NAME}` and `{file:path}` are substituted in the text before parsing.

### Loading order (later overrides earlier)

1. Well-known remote config (organization manifests, authenticated by an integration credential)
2. Global config directory (`opencode.json[c]` plus its `agents/`, `commands/`, `plugins/`, `skills/` subdirectories)
3. File named by `OPENCODE_CONFIG`
4. `opencode.json[c]` files found walking up from the working directory (nearest wins)
5. Project `.opencode/` directories (config files and the same subdirectories)
6. Inline JSON in `OPENCODE_CONFIG_CONTENT`

`OPENCODE_DISABLE_PROJECT_CONFIG` (or `OPENCODE_CONFIG_PROJECT_DISABLE`) skips project config. `~/.claude`, `~/.agents` and their project counterparts `.claude/`, `.agents/` are read for skills only. Run `opencode debug config` to list the active sources and `opencode debug agents` to list agents.

### Native keys

Native keys are plural. The v1 singular keys are still accepted and normalized on load (see Migration from 1.x), but write the native ones.

| Key                                       | Type              | Notes                                                                                                                                                                              |
| ----------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                                   | string or object  | `provider/model` or `provider/model#variant`, or `{providerID, model, variant?}`                                                                                                   |
| `default_agent`                           | string            | Default primary agent (built-in default is `build`)                                                                                                                                |
| `agents`                                  | object            | Agent overrides and definitions                                                                                                                                                    |
| `commands`                                | object            | Slash commands, `{template, description?, agent?, model?, subagent?}`                                                                                                              |
| `permissions`                             | array             | Ordered `{action, resource, effect}` rules                                                                                                                                         |
| `plugins`                                 | array             | Strings or `{package, options}`                                                                                                                                                    |
| `providers`                               | object            | Provider definitions and overlays                                                                                                                                                  |
| `mcp`                                     | object            | `{timeout?, servers}`                                                                                                                                                              |
| `skills`                                  | array of strings  | Extra directories or http(s) URLs to discover skills from                                                                                                                          |
| `instructions`                            | array of strings  | Extra instruction files, paths or URLs                                                                                                                                             |
| `references`                              | object            | Named local paths or Git repositories offered as external context                                                                                                                  |
| `compaction`                              | object            | `{auto, buffer, keep: {tokens}}` (no `prune`)                                                                                                                                      |
| `formatter`, `lsp`                        | boolean or object | Enable built-ins or override per name (`command`, `extensions`, `environment`/`env`, `disabled`)                                                                                   |
| `websearch`                               | false or object   | `{provider}`, provider id or `random`                                                                                                                                              |
| `shell`                                   | string            | Default shell for terminal and the shell tool                                                                                                                                      |
| `update`                                  | string            | `disable`, `notify` or `auto`                                                                                                                                                      |
| `share`                                   | string            | `manual`, `auto` or `disabled`                                                                                                                                                     |
| `snapshots`                               | boolean           | Snapshots behind undo and revert                                                                                                                                                   |
| `tool_output`                             | object            | `{max_lines, max_bytes}` (default 2,000 lines, 51,200 bytes): one global cut for skill loads, shell output (tail kept), MCP and plugin tool results; no per-tool or per-agent form |
| `watcher`, `worktree`, `media`, `warming` | object            | Watcher ignore list, worktree directory defaults, media processing, keep-warm requests (default false)                                                                             |
| `username`, `enterprise`                  | string, object    | Display and telemetry identity, enterprise sharing URL                                                                                                                             |
| `experimental`                            | object            | `portable_shell_scanner`, `subagent_depth` (default 1), `policies`                                                                                                                 |

### Permissions

Rules are an ordered array of `{action, resource, effect}`; `effect` is `allow`, `ask` or `deny`. Wildcards: `*` matches any run of characters, `?` one character. Matching takes the last rule whose action and resource both match, so put the catch-all first. Agent rules are appended after the global ones. `~` and `$HOME` expand in path resources (`read`, `edit`, `external_directory`).

```json
{
  "permissions": [
    { "action": "*", "resource": "*", "effect": "ask" },
    { "action": "shell", "resource": "git *", "effect": "allow" },
    { "action": "shell", "resource": "rm *", "effect": "deny" },
    { "action": "edit", "resource": "src/**/*.ts", "effect": "allow" }
  ]
}
```

Action names follow the tools: `shell`, `edit` (also covers `write` and `patch`), `read`, `grep`, `glob`, `webfetch`, `websearch`, `subagent`, `question`, `skill`, `external_directory`, `browser`. Agent defaults: everything allowed, `external_directory` asks, and `.env` and `.env.*` reads ask (`.env.example` is allowed). `--auto` (on `run`, `mini` and the TUI) approves every request that is not explicitly denied. `experimental.policies` holds `{action: "provider.use" | "permission", resource, effect: allow|deny}` rules that gate configured resources, and `enabled_providers`/`disabled_providers` migrate into them.

### Migration from 1.x

The loader normalizes v1 config and reports a diagnostic for what it cannot carry over:

- `permission` and `tools` become `permissions` rules; action names `bash`, `task`, `write`, `patch` map to `shell`, `subagent`, `edit`, `edit`.
- `plugin` becomes `plugins` (tuples become `{package, options}`); `provider` becomes `providers` (`npm` becomes `package: "aisdk:<npm package>"`, `api` becomes `settings.baseURL`); `agent` and `mode` become `agents`; `command` becomes `commands`; `reference` becomes `references`; `small_model` becomes the `title` agent's model; `autoupdate` becomes `update`.
- `compaction.reserved` becomes `buffer`, `preserve_recent_tokens` becomes `keep.tokens`; `prune` and `tail_turns` are dropped.
- `todowrite` and `todoread` tools no longer exist.
- Dropped as unsupported: top-level `logLevel`, `server`, `subagent_depth`, `layout`; experimental `batch_tool`, `openTelemetry`, `primary_tools`, `continue_loop_on_deny`, `disable_paste_summary`; provider `whitelist`/`blacklist`/`id`.
- Model references are `{providerID, model, variant?}` once decoded; the string form is `provider/model#variant`.

## Agents

Modes: `primary` (selectable), `subagent` (started by the `subagent` tool or an `@mention`), `all`.

Built-ins: `build` (default primary), `general` (subagent, cannot ask questions or spawn subagents), `explore` (read-only subagent: grep, glob, read, webfetch, websearch), and hidden `compaction`, `title`, `summary`. Subagent nesting depth defaults to 1 (`experimental.subagent_depth`).

Agent fields: `model`, `request` (`headers`, `body`), `system`, `description`, `mode`, `hidden`, `color` (`#RRGGBB`), `steps`, `disabled`, `permissions`. Define them under `agents`, or as markdown in `agents/**/*.md` of any config directory: the body is the system prompt, the file path (minus `agents/` and `.md`) is the name, and `modes/*.md` files become primary agents. A markdown file with v1 keys (`tools`, `permission`, `temperature`, `prompt`) is migrated; native frontmatter uses the keys above.

## Tools

Built-in: `shell`, `read`, `edit`, `write`, `patch`, `grep`, `glob`, `webfetch`, `websearch`, `question`, `skill`, `subagent`, plus `execute` (Code Mode) and the `opencode` namespace (`session_rename`, `session_move`, `models`, `list_mcp_resources`, `read_mcp_resource`). There is no `list`, `multiedit`, `todowrite` or `todoread`. A built-in browser plugin owns the `browser_*` tool names.

### Code Mode

Tools registered with `codemode: true` (the default for plugin tools, MCP tools and the `opencode` and `browser` namespaces) are not sent to the model individually. The model gets one `execute` tool that runs JavaScript in a confined interpreter (no imports, filesystem or timers; `fetch` available) and calls them as `tools.<namespace>.<name>(input)`, discovering the catalogue through instructions or a `search` function. Tools registered with `codemode: false` stay on the provider's native tool list; all the file, shell, web, question, skill and subagent built-ins are native. An MCP server opts out with `"codemode": false` in its config.

## Providers and models

- `opencode auth login <provider> [--method api-key]`, `auth list`, `auth logout <provider> [account]`, `auth switch <provider> <account>`, `auth export|import` manage integrations and credentials; the TUI equivalent is `/connect`. Credentials come from the `credential` table, from environment variables a provider declares in `env`, or from well-known manifests.
- Pick a model with `--model provider/model#variant`; the `#variant` suffix is the reasoning-effort or option variant (there is no `--variant` flag). `opencode models` lists available models (no `--verbose`); limits and costs come from `opencode api model.list`.
- Custom provider under `providers`:

```json
{
  "providers": {
    "myprovider": {
      "name": "My Provider",
      "package": "aisdk:@ai-sdk/openai-compatible",
      "env": ["MY_KEY"],
      "settings": { "baseURL": "https://api.example.com/v1", "timeout": 600000 },
      "headers": { "x-team": "eng" },
      "models": {
        "my-model": {
          "name": "My Model",
          "limit": { "context": 200000, "output": 32000 },
          "variants": [{ "id": "high", "settings": { "reasoningEffort": "high" } }]
        }
      }
    }
  }
}
```

Model fields: `modelID`, `family`, `name`, `compatibility` (`reasoningField`, `maxTokensField`, `requireReasoning`, ...), `package`, `settings`, `headers`, `body`, `capabilities`, `variants[]`, `cost` (USD per million tokens, tiered by context size), `limit`, `disabled`.

## MCP

```json
{
  "mcp": {
    "servers": {
      "local-one": {
        "type": "local",
        "command": ["npx", "-y", "pkg"],
        "environment": { "K": "{env:K}" },
        "cwd": "."
      },
      "remote-one": {
        "type": "remote",
        "url": "https://host/mcp",
        "headers": {},
        "oauth": { "scope": "x" }
      }
    },
    "timeout": { "startup": 30000, "catalog": 30000, "execution": 120000 }
  }
}
```

Per-server extras: `disabled`, `codemode`, `timeout`, `protocol` (`legacy` default, `auto`, `2026-07-28`), remote `oauth` (object or `false`). v1 `mcp.<name>` entries are still migrated. CLI: `opencode mcp list|add|auth|logout` (`add context7 --url <url> [--header K=V]`, or `add name [--global] [--env K=V] -- <command...>`).

## Skills

Markdown with frontmatter `name`, `description`, optional `metadata`. Discovered as `{*.md,**/SKILL.md}` under `skill/` and `skills/` in any config directory, under `~/.claude/skills`, `~/.agents/skills` and their project equivalents, and under each path or http(s) URL in the `skills` key. The id is the parent directory name (or the file name for a loose `.md`). `metadata.opencode/autoinvoke` toggles automatic invocation. The model loads a skill through the `skill` tool.

## Custom commands

Markdown files in `{command,commands}/**/*.md` of a config directory (nested path becomes the name, `a/b.md` is `/a/b`), or entries under `commands`. The file must open with a `---` fenced YAML frontmatter block; a file whose header lacks the fences is not parsed and the command silently does not exist.

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-sonnet-5-5#high
subagent: false
---

Run the full test suite for $1 with a coverage report.
```

Frontmatter: `description`, `agent`, `model`, `subagent` (`subtask` is a deprecated alias). Body placeholders: `$ARGUMENTS`, `$1`, `$2` (the last placeholder takes the remaining words), and `` !`cmd` `` for shell output. When the body has no placeholder and arguments were given, they are appended. A command whose agent has `mode: subagent`, or with `subagent: true`, runs in a child session. `opencode run` cannot invoke commands (no `--command`); they go through the server's `session.command` endpoint (`opencode api`). Built-in commands include `init` and `review`.

## Instructions

`AGENTS.md` is read from the global config directory and from every directory between the working directory and the project root (or home). `CLAUDE.md` is not read. The `instructions` key adds more files, globs or URLs.

## Plugins

Plugins are configured in `plugins` and auto-discovered from `plugin/` and `plugins/` in config directories (use `plugins/`). An entry is a package name, an absolute or relative directory, or `{package, options}`; a leading `-` removes an entry (`"-name"`). A local directory resolves its entrypoint to `server.js`, then `index.js`; a path that points at a file is dropped with a warning. `opencode plugin list|add|check|update|remove` manages package plugins in the global config.

The v1 plugin function and `@opencode-ai/plugin` do not run. A v2 plugin default-exports a definition with a stable `id` and a `setup(ctx)`; `setup` registers hooks and may return a cleanup function:

```ts
import { Plugin } from '@opencode/plugin'
import { Schema } from 'effect'

export default Plugin.define({
  id: 'example',
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: 'echo',
        options: { codemode: false },
        description: 'Echo text',
        input: Schema.Struct({ text: Schema.String }),
        execute: async ({ text }) => ({ content: text }),
      })
    })
    await ctx.tool.hook('execute.before', (event) => {
      if (event.tool === 'read') throw new Error('blocked')
    })
  },
})
```

- `ctx` groups domains: `agent`, `aisdk`, `command`, `event`, `integration`, `mcp`, `model`, `permission`, `provider`, `reference`, `session`, `shell`, `skill`, `storage`, `tool`, `vcs`, `websearch`, `worktree`, plus `options`, `location`, `rpc`.
- Transform hooks (`ctx.<domain>.transform(editor => ...)`) are synchronous, replayable edits; load data first and call `ctx.<domain>.reload()` when it changes. Runtime hooks (`ctx.tool.hook`, `ctx.session.hook("context" | "prompt" | "model.request" | "compaction" ...)`, `ctx.shell.hook("create.before")`, `ctx.permission.hook("evaluate")`) intercept live operations.
- Tool options: `codemode` (default true), `pinned`, `namespace`, `permission`. Use `codemode: false` for a tool that must appear natively in the model's tool list. The Effect flavour is `@opencode/plugin/effect`; TUI plugins use `@opencode/plugin/tui`.
- `ctx.storage` is durable JSON storage scoped by plugin id.

## CLI

`opencode [directory]` starts the TUI. Commands that talk to a server accept `--standalone` and `--server <url>`.

| Command                                      | Purpose                                                                                               |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `opencode run [message...]`                  | Non-interactive run through the shared service                                                        |
| `opencode mini`                              | Minimal interactive interface (`--replay`, `--replay-limit`, `--prompt`)                              |
| `opencode api <operation-id \| METHOD path>` | Call the server API: `--param k=v`, `--data`/`-d`, `--header`/`-H`, e.g. `opencode api model.list`    |
| `opencode auth`                              | `list`, `login`, `logout`, `switch`, `export`, `import`                                               |
| `opencode session`                           | `list`, `delete`, `export`, `import`                                                                  |
| `opencode mcp`, `opencode plugin`            | See MCP and Plugins                                                                                   |
| `opencode models`                            | List models                                                                                           |
| `opencode stats`                             | Usage (`--days`, `--year`, `--all`, `--project`, `--models`, `--tools`, `--cost`, `--full`, `--json`) |
| `opencode serve`                             | API and web server (`--hostname`, `--port`, `--cors`)                                                 |
| `opencode service`, `pair`, `reload`         | Background service, pairing links, config reload                                                      |
| `opencode debug`                             | `agents`, `config`, `paths`                                                                           |
| `opencode acp`                               | Agent Client Protocol server over stdio                                                               |
| `opencode upgrade [target]`, `uninstall`     | Update (`--method curl\|npm\|pnpm\|bun\|yarn\|vp\|brew`) and remove                                   |

`opencode run` flags: `--continue`/`-c`, `--session`/`-s <id>` (continues, or creates with that id), `--fork`, `--model`/`-m provider/model#variant`, `--agent`, `--file`/`-f` (repeatable), `--format default|json`, `--title`, `--thinking`, `--auto`, `--standalone`, `--server`. There is no `--variant`, `--dir`, `--pure` or `--command`; run it from the target directory. Global flags: `--log-level`, `--print-logs`, `--completions <shell>`, `--wizard`. Removed from 1.x: `agent create|list`, top-level `export|import` (now `session export|import`), `github install|run`, `models --verbose`.

## Environment variables

`OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, `OPENCODE_CONFIG_CONTENT`, `OPENCODE_DISABLE_PROJECT_CONFIG`, `OPENCODE_DB`, `OPENCODE_PASSWORD` / `OPENCODE_SERVER_PASSWORD`, `OPENCODE_DISABLE_AUTOUPDATE`, `OPENCODE_LOG_LEVEL`. Provider API keys use the names a provider lists in `env` (for example `ANTHROPIC_API_KEY`).

## Anti-patterns

- Applying 1.x documentation to 2.x: singular config keys, `permission` objects, `--variant`, `--command`, `--dir`, `auth.json`, `@opencode-ai/plugin`.
- Writing a command or agent markdown file without `---` fences around the frontmatter.
- Pointing `plugins` at a file instead of a directory.
- Registering a plugin tool without deciding `codemode`; it defaults to Code Mode and is then invisible as a native tool.
- Running the binary against the real user config while testing; set `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` and `XDG_CACHE_HOME` (or `OPENCODE_CONFIG_DIR` and `OPENCODE_DB`) to a scratch directory first.
