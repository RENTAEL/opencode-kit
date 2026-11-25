---
name: develop-opencode-plugins
description: "Conventions for creating or extending the plugins in this repo. The plugins target OpenCode 2 (`@opencode/plugin@2.0.21`, zod 4) and also run under Claude Code through a stdio MCP server, so most code is written against a harness-neutral contract and adapted twice."
---
# OpenCode Plugin Development

## Purpose

Conventions for creating or extending the plugins in this repo. The plugins target OpenCode 2 (`@opencode/plugin@2.0.21`, zod 4) and also run under Claude Code through a stdio MCP server, so most code is written against a harness-neutral contract and adapted twice.

Two sides are easy to confuse:

- **The OpenCode-native surface**: `Plugin.define`, the setup `Context`, the tool, integration, session and event domains. These ship in `@opencode/plugin` and are the contract with the runtime.
- **This repo's house library**: everything under `src/modules/_core/` (`defineTool`, `BaseTool`, `defineModulePlugin`, `PluginError`, `Logger`, `CredentialStoreService`, `MarkdownBuilder`, and so on). These are our conventions on top of the native surface. They are not importable from `@opencode/plugin`.

The v2 types in `node_modules/@opencode/plugin/dist/promise/*.d.ts` are the source of truth for the native side; `plugin.d.ts` lists the `Context` domains, `tool.d.ts` the tool editor, `integration.d.ts` the `/connect` methods. The v2 source (tag `v2.0.21` of `anomalyco/opencode`) settles what the types do not. Do not write against v1 knowledge (`@opencode-ai/plugin`, `tool()`, `tool.schema`, the `Hooks` object, the `auth` block, `client.app.log`, `context.ask`); none of it exists here.

Bumping the plugin dependency: `pnpm add -E @opencode/plugin@<version>`, then `pnpm typecheck` through `check_run` before anything else.

## Official documentation

The docs track upstream and move faster than this skill: https://opencode.ai/docs/ (plugins, config, agents, commands, skills, CLI). They cover both major versions in places; when a docs example disagrees with the installed `.d.ts` files, the types win.

## How a plugin is loaded

Facts established by running the 2.0.21 binary, and the reason behind each house pattern:

- **A local plugin is a directory.** The config key is `plugins: [<dir>]`; OpenCode resolves `<dir>/server.js`, then `<dir>/index.js`. A file path entry is dropped with a warning. So each module's entry point is `src/modules/<name>/server.ts`, and `scripts/link-opencode.sh` writes every `dist/modules/*/` that contains a `server.js` into the global `opencode.json` (`pnpm symlink:opencode` builds first).
- **`setup(ctx)` runs once per location**, which is one project directory. `ctx.location.directory` is that directory, so a module instance is per project (`IModuleEnv.directory`). Never read `process.cwd()` in a tool; use `IToolContext.directory`.
- **Plugin tools default to Code Mode**, hidden behind one generic `execute` tool. `defineModulePlugin` registers every tool with `options: { codemode: false }` so each one is a direct tool with its exact name and JSON schema. Per-agent permission rules match tools by name, so Code Mode would leave them nothing to match.
- **No namespace**, so tool names stay unprefixed (`example_get_item`).
- **A built-in plugin owns names.** `@opencode/plugin-browser` registers the `browser_*` tools under the `browser` namespace, and a plugin tool whose effective name collides is silently dropped, with no error. A browser-automation module of this repo would therefore use a different prefix, such as `playwright_*`. Before naming a tool family, check it against OpenCode's built-in tool names and namespaces.
- **A thrown error becomes a tool error** carrying its message. That is the failure channel; there is no separate error result type.
- **Plugin tools get no runtime permission prompt in v2.** The tool context has no `ask`, and the host never checks permissions for plugin tools beyond hiding a tool that a matching `deny` rule covers. See Access control.

## Module layout

```
src/modules/<name>/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ server.ts            # OpenCode entry: default-exports a plugin
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ <name>.module.ts     # createXModule: builds services and the tool map (an IModule)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ config.ts            # module constants
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ services/            # business logic (API client, formatting, orchestration)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ tools/               # one file per tool
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ types/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ prompts/             # optional .txt templates (copied to dist by scripts/copy-assets.js)
```

`src/modules/check/` is the reference module: `server.ts` is one `defineModulePlugin` call, `check.module.ts` builds the services and the tool map, `tools/` has one tool per file, and `services/check-runner.service.spec.ts` shows the spec pattern. Copy its shape for a new module and change what the new module needs.

Shared infrastructure lives in `src/modules/_core/` (leading underscore).

A new module also needs an entry in the `MODULES` map in `src/modules/registry.ts`, `'<name>': { create: createXModule, isInClaudeCode: true }`, or it will not exist under Claude Code. The bridge loads only the entries flagged `isInClaudeCode`. OpenCode ignores the map and loads every `dist/modules/*/server.js`. Tool names must be unique across all modules; the bridge throws on a duplicate. Every agent in `opencode.json` starts from a deny-all rule, so a new tool family reaches no OpenCode agent until each agent that should use it gets an allow rule for it (see Access control); on the Claude Code side the `isInClaudeCode` flag is what exposes it.

## The house library

### Tool contract (`_core/tools/tool-definition.ts`)

A module builds tools against a harness-neutral shape. Neither host's types appear in module code.

```typescript
interface IToolContext {
  readonly directory: string // project directory the call runs for
  readonly signal: AbortSignal // pass into fetch and subprocess calls
  readonly progress: (title: string) => void // best-effort progress line
}

interface IToolDefinition<TInput extends z.ZodObject> {
  readonly description: string
  readonly input: TInput
  execute(args: z.output<TInput>, context: IToolContext): ToolOutput | Promise<ToolOutput>
}
```

`ToolOutput` is a string or `{ text, attachments? }`, where an attachment is `{ mime, url, filename? }` and `url` is a `data:` or `file://` URL. `input` must be a `z.object(...)` from zod 4. `defineTool` is the identity helper that infers the input type.

`progress` is the long-running-tool channel. In OpenCode it updates the running call; in the Claude Code bridge it becomes an MCP progress notification, which also keeps a quiet call from hitting Claude Code's idle timeout. Long-running tools (`oc_wait_runs`, a sync `oc_run`) call it on every step.

### Writing a tool

A tool is an object literal typed `IToolDefinition<typeof input>`. The annotation alone types `execute`'s arguments, so module code has no tool class, no `static create`, no `defineTool` and no `BaseTool`; the last two stay in `_core` only until the remaining class-based tools migrate. A tool with no module-instance dependency is a module-level constant named `<name>Tool`. From a hypothetical `example/tools/get-resource.tool.ts`:

```typescript
const input = z.object({
  name: z.string().describe('Resource name'),
  apiKey: z.string().describe('API key for the Example service'),
})

export const getResourceTool: IToolDefinition<typeof input> = {
  description:
    'Fetch one resource from the Example service by name. Returns its ID and status. ' +
    'Call example_list_resources first to find valid names.',
  input,
  execute: async ({ name, apiKey }) => {
    const result = await getResource(name, apiKey)

    return MarkdownBuilder.create()
      .text('[PASS] Resource found')
      .field('Name', result.name)
      .field('ID', result.id)
      .field('Status', result.status)
      .build()
  },
}
```

A tool that needs services is a factory `create<Name>Tool(deps)`, and the services reach `execute` by closure. Per-call values (`directory`, `signal`, `progress`, `caller`) come from `execute`'s second parameter. From a hypothetical `example/tools/login.tool.ts`:

```typescript
export const createLoginTool = (sessions: HttpSessionService): IToolDefinition<typeof input> => ({
  description:
    'Store a Bearer token in a named HTTP session. Every example_request with the same session name then sends it ' +
    'in the Authorization header. Optionally set a base URL so requests can use relative paths.',
  input,
  execute: async ({ token, tokenFile, baseUrl, session = DEFAULT_SESSION_NAME }, { directory }) => {
    sessions.login(session, await readToken(token, tokenFile, directory), baseUrl)
    const info = sessions.getSessionInfo(session)

    return MarkdownBuilder.create()
      .text('[PASS] Token stored in session')
      .field('Session', session)
      .field('Base URL', info.baseUrl ?? '(not set)')
      .field('Authenticated', String(info.authenticated))
      .build()
  },
})

const readToken = async (
  token: string | undefined,
  tokenFile: string | undefined,
  directory: string
): Promise<string> => {
  if (token !== undefined && tokenFile === undefined) {
    return token
  }
  if (token !== undefined || tokenFile === undefined) {
    throw new PluginError('Pass exactly one of token or tokenFile.', 'VALIDATION_ERROR')
  }

  const path = isAbsolute(tokenFile) ? tokenFile : resolve(directory, tokenFile)
  const fileToken = (await readFile(path, 'utf8')).trim()
  if (fileToken.length === 0) {
    throw new PluginError(`Token file ${path} is empty.`, 'VALIDATION_ERROR')
  }

  return fileToken
}
```

Rules for the tool body:

- One tool per `tools/<kebab>.tool.ts`, exporting only the tool. `const input = z.object(...)` sits at module level, and private helpers are non-exported arrows below the tool that take only the values they need.
- The zod schema is the only declaration of the input; no args interface restates it.
- Destructure the fields `execute` reads and write `?? DEFAULT` as a destructuring default (`session = DEFAULT_SESSION_NAME`). Two exceptions: a `.nullable()` field, because a default replaces only `undefined`, and a default that reads the context (`cwd ?? directory`), which stays in the body because a first-parameter default cannot see the second parameter. Rename a snake_case key while destructuring (`project_id: projectId`).
- `execute` is `async` only when it awaits. A body that only returns a service promise is a concise arrow (`execute: (args) => sites.get(args.site).issues.getIssue(args)`), and a synchronous body returns its value.
- Where a service takes a `(message: string) => void` callback, pass `progress` itself.
- Validation the schema cannot express stays in `execute` and throws `PluginError(..., 'VALIDATION_ERROR')`, like the token check in `readToken` above or a date-pattern check. A `.refine` after `.describe` drops the description.
- A tool that returns attachments returns `{ text, attachments }`.
- When a service method takes the parsed args as its contract, the schema lives in `types/<m>.types.ts` as `XInputSchema` with `type IXInput = z.infer<typeof XInputSchema>`, and the tool spreads it after its own routing fields: `z.object({ site: SiteSchema, ...GetIssueInputSchema.shape })` in `example/tools/get-issue.tool.ts`. Spread `.shape` rather than calling `.extend()`, which moves the added keys last in the JSON Schema.

Errors need no wrapper, because the two adapters are the boundary: OpenCode turns a thrown error into a tool error carrying its message, and the Claude Code bridge returns `<tool> failed: <message>`. Neither passes `PluginError.code` to the model. Throw a `PluginError` for an expected failure, let anything else propagate, and do not catch an error only to prefix or rewrap it. Read a caught `unknown` with `errorMessage(error)` from `_core/types/errors.ts`.

Rules for the input schema:

- Put `.describe()` on every field. The model reads them.
- The schema is zod 4 and is converted with `z.toJSONSchema`. OpenCode would convert a zod schema with its own bundled zod copy, which cannot see the `.describe()` texts registered in this package's zod registry, so the adapter hands OpenCode the JSON Schema through the standard-schema `jsonSchema` hook (`withJsonSchema` in `define-module-plugin.ts`). Validation still runs through this package's zod. Do not pass a raw zod schema to `ctx.tool` yourself.
- Share a common field by exporting one schema fragment or description constant and spreading it into each `z.object` (see `SESSION_ARG_DESCRIPTION` in a module's `config.ts`).

Tool naming: `snake_case`, prefixed by the module (`example_create_item`). The keys of the module's tool map are the tool names, and hosts list the tools in the map's key order. The keys need no lint directive: no camelcase rule is configured.

Tool descriptions drive when the model calls the tool. Say what it does, when to use it and which tool to call first, and the defaults of optional arguments.

### Module factory and `defineModulePlugin`

A module is a factory `(env: IModuleEnv) => IModule | Promise<IModule>` returning `{ tools, dispose? }` (`_core/types/module.types.ts`). The factory must not throw on missing credentials or config: log the problem and let the affected tools fail at call time with an actionable error. Services take their dependencies through constructors; no singletons.

`server.ts` adapts the factory to OpenCode:

```typescript
import { defineModulePlugin } from '../_core/plugin/define-module-plugin.js'
import { createExampleModule } from './example.module.js'

export default defineModulePlugin({ id: 'cookbook.example', create: createExampleModule })
```

The `id` is `cookbook.<module>`. `defineModulePlugin` wraps `Plugin.define`: in `setup` it creates the module for `ctx.location.directory`, registers each tool through `ctx.tool.transform` (`editor.add({ name, description, input, options: { codemode: false }, execute })`), registers integrations through `ctx.integration.transform`, and returns a cleanup that disposes the tool registration, the integrations, and then calls `module.dispose`. A string result becomes `{ content }`; an attachment becomes a `file` content part with `uri`, `mime` and `name`.

### Claude Code bridge (`src/mcp/server.ts`)

The bridge imports the module factories directly and does not go through OpenCode: it calls each factory with `{ directory: process.cwd() }`, converts every tool's input with `z.toJSONSchema(definition.input, { io: 'input', unrepresentable: 'any' })`, validates calls with `definition.input.parse`, forwards `progress` as MCP progress notifications when the client sent a progress token, and turns a thrown error into an `isError` result (`<tool> failed: <message>`). It also redirects `console.log`, `info` and `debug` to stderr, because stdout carries the JSON-RPC stream.

Consequences for module code: no OpenCode type may leak into a tool or service, nothing may write to stdout, and any state a module needs from OpenCode (credentials) must be readable without an OpenCode host. Modules flagged `isInClaudeCode: false` in the `MODULES` map in `src/modules/registry.ts` are OpenCode-only.

### Hooks-only plugins

A plugin with no tools skips the module layer and calls `Plugin.define` directly. `src/modules/compaction/server.ts` registers a session hook and returns a cleanup that disposes it:

```typescript
export default Plugin.define({
  id: 'cookbook.compaction',
  setup: async (ctx) => {
    const registration = await ctx.session.hook('compaction', async (event) => {
      const session = await ctx.session.get({ sessionID: event.sessionID })
      // session.location.directory is the session's own directory, not the plugin's location
    })
    return () => registration.dispose()
  },
})
```

Every registration (`transform`, `hook`) returns a `Registration` whose `dispose` the plugin must call from its cleanup.

### Errors (`_core/types/errors.ts`)

All failures use `PluginError(message, code, cause?)`. Codes: `AUTH_MISSING`, `AUTH_EXPIRED`, `AUTH_INVALID`, `RATE_LIMITED`, `NOT_FOUND`, `FORBIDDEN`, `VALIDATION_ERROR`, `CONNECTION_ERROR`, `TIMEOUT`, `ABORTED`, `EXTERNAL_API_ERROR`, `INTERNAL_ERROR`. `isErrnoCode(error, 'ENOENT')` narrows a Node system error without `any`.

### Logging (`_core/services/logger.service.ts`)

`new Logger('Context')` with `log(message)`, `warn(message, trace?)` and `error(message, trace?)`, created once per file as a module-level `const logger`, never held in a field or passed as a parameter. It writes level-tagged lines to stderr only (`INFO  [Context] message`). stdout is never safe: `opencode run --format json` streams its events there and the MCP bridge speaks JSON-RPC over it. v2 has no `client.app.log` and no toast channel for plugins, so there is nothing else to route to. No raw `console.*` in module code.

### Utilities

All under `src/modules/_core/services/`:

- `MarkdownBuilder` (`markdown-builder.service.ts`): fluent LLM-readable output. `MarkdownBuilder.create().heading(...).field(...).bullet(...).table(headers, rows).codeBlock(...).build()`; also `text`, `blank`, `separator`, `italic`. Never build tables with string concatenation.
- `format.utils`: `formatBytes`, `sleep`, `clipChars(text, max)` (cuts whole characters, so an emoji never splits into a lone surrogate) and `fillTemplate(template, { name: 'value' })` for `{{name}}` placeholders.
- Prompt templates: `readFileSync(new URL('../prompts/x.txt', import.meta.url), 'utf-8')`, filled with `fillTemplate`. `scripts/copy-assets.js` copies `.txt` and `.lua` files from anywhere under `src/` to `dist/`; other non-TypeScript files are not copied.
- `readJsonConfig(path, schema)` (`config-loader.service.ts`): `null` for a missing file, the parsed `z.infer` of the schema otherwise, and a `VALIDATION_ERROR` naming the path when the JSON does not parse or the schema rejects it. A factory must not throw, so a config read at startup catches that error, logs it with `logger.warn` and leaves the feature unconfigured.
- `runSubprocess` (`subprocess.service.ts`): the shared child-process runner.
- `parseJsonLines` / `parseJsonObject` (`json-lines.utils.ts`): JSON-lines parsing that skips any line that is not a JSON object.
- `tempPath`, `hasContent`, `removeTempPath` (`temp-file.utils.ts`): unique paths under the OS temp directory's `opencode/`, and a delete that logs a failure instead of throwing.
- `openSqlite` / `resolveOpenCodeDbPath` (`sqlite.service.ts`): see Credentials.

## Service layering

Modules use three layers: an API service (HTTP or SDK calls, auth headers, error mapping), a formatting service (data to markdown), and an orchestration service that combines them. An orchestration service exists only where it branches, combines calls or holds state (`IssueService`, `MessageService`), and where one exists, tools call it, never the API service. When an operation is one API call whose result goes straight to one formatter, the tool makes both calls itself; a tool that sends a webhook first calls the payload builder in the module's API service. A service with no state and no dependency other than a logger is a file of exported functions; it stays a class only when it holds state or takes another dependency (`HttpSessionService`, `ExampleApiService`). Each API service maps its own error format to `PluginError` codes; those mappings are intentionally not shared. Do not add pass-through methods that forward to another service without logic.

Output conventions: empty results get a readable sentence (`No items found in <context>.`), and mutation tools confirm with `[PASS] <message>` followed by `field` lines.

GitHub deliberately has no API module: agents use the `gh` CLI (see `workflow-git-cli`). The `github` module is not such a wrapper: it has one tool, `github_ci_wait`, which replaces a CI polling loop with one long call.

## Access control

v2 has no runtime confirmation for plugin tools, so access is gated only by static configuration:

- **OpenCode**: per-agent `permissions` rules in `opencode.json`, each `{ "action": "<tool name or glob>", "resource": "*", "effect": "allow" | "deny" }`. This repo's agents start from `{ "action": "*", "resource": "*", "effect": "deny" }` and allow-list families by wildcard (`example_*`, `codebase_*`). Because tools are direct and unprefixed, those names match. A `deny` rule also hides the tool from the model.
- **Claude Code**: permission rules on the bridge's tools, which appear as `mcp__opencode__<tool name>`.

Do not build a confirmation step into a tool, and do not reintroduce a `context.ask` style helper. A destructive tool is made safe by being absent from the allow-list of agents that should not use it.

## Credentials and /connect integrations

OpenCode 2 stores `/connect` credentials in the `credential` table of its database (`opencode.db`). `auth.json` is read only by a one-time migration when a v1 database is upgraded, which copies a v1 entry's `metadata` into the credential's `metadata` rather than `configuration`; a fresh install imports nothing, and later edits to `auth.json` are never read. Both harnesses read them through `CredentialStoreService` (`_core/services/credential-store.service.ts`) at call time, because the Claude Code bridge has no OpenCode host to ask.

- `readKey(integrationID)` returns `{ type: 'key', key, configuration? }`.
- The active credential is the one OpenCode itself would pick: the activated row, then the newest.
- `IntegrationID` is a key of `INTEGRATION_NAMES` (`{ example: 'Example' }`, a placeholder: this repo ships no integration modules), whose value is the name `/connect` lists and the store's error messages use; a new integration adds its id and name there.
- Missing credentials throw `AUTH_MISSING` with a message that begins "STOP - do not look for the credential elsewhere" and tells the user to run `/connect` in OpenCode, or `opencode auth login <id>` in a terminal, the only route from Claude Code, which has no `/connect`. Build module-specific auth errors from the exported `connectHint(integrationID)`, as an integration module would: the wording stops the model from inventing workarounds.

`resolveOpenCodeDbPath` resolves the database path as OpenCode 2.0.21 does: `OPENCODE_DB` (default `opencode.db`) against OpenCode's data directory, `$XDG_DATA_HOME/opencode` (default `~/.local/share/opencode`), so an absolute value is kept, a relative one lands below the data directory rather than the process's working directory, and `:memory:` passes through. `openSqlite` imports `bun:sqlite` under Bun (OpenCode) and `node:sqlite` under Node (the bridge) lazily, because a top-level `node:sqlite` import fails to load under Bun and would take every tool in the plugin with it. Open the database read-only.

Registering the `/connect` entry is the `integration` option of `defineModulePlugin`: `{ id, method }`, where `id` is an `IntegrationID` and `method` is an `IntegrationKeyMethod` from `@opencode/plugin/promise/integration`. The adapter takes the listed name from `INTEGRATION_NAMES`. Two patterns exist:

- **Key method**: `integration: { id: 'example', method: { type: 'key', label } }` in the module's `server.ts`. `/connect` prompts for the secret itself; a key method has no placeholder, so put the hint in `label`.
- **Key plus form field**: add `form: [{ key: 'accountId', type: 'string', title, description, required: true }]` to the method. The answers land in `Credential.Key.configuration`, read back as `readKey(...).configuration`.
  A provider with a browser login and rotating refresh tokens gets no `/connect` entry: the credential store exposes one active credential per integration at a time, and an OpenCode `refresh` callback beside the module's own refresher would race and invalidate the rotated token. The module owns the login instead: a login tool opens the browser and receives the code on a registered loopback port, one token file per account under `$XDG_STATE_HOME/<module>/` (mode 0600) serves every session in both harnesses, and one auth service is the only refresher. It refreshes when the token is within 60 seconds of expiry, under a lock file so processes that refresh at once do not invalidate each other, and a process that waited for the lock reads the winner's token instead of refreshing again.
  A second product behind the same OAuth app does not need a login of its own: its module can reuse the first module's auth service for the same account, because one app and one token cover both; the new product's scopes go into the shared scope list and reach an account at its next login.

Credentials a module cannot get from `/connect` (a client secret, a database connection list) come from files or environment variables: `.opencode/config/*.json` through `readJsonConfig`, or a file under `~/.config/opencode/` with environment variables taking precedence.

## Hooks and other native domains

The setup `Context` exposes these domains: `agent`, `aisdk`, `command`, `event`, `integration`, `mcp`, `model`, `generate`, `permission`, `provider`, `reference`, `rpc`, `session`, `shell`, `skill`, `storage`, `tool`, `vcs`, `websearch`, `worktree`, plus `location`, `options`, `app` and `plugin`. Mutations go through `domain.transform(editor => ...)`; interception goes through `domain.hook(name, callback)`. Both return a `Registration` to dispose.

Hook names seen in the installed types:

- `ctx.session.hook`: `prompt`, `context`, `compaction`, `generate`, `title`, `model.request`, `http.request`, `http.response`, `retry`, and the `experimental.ws.*` frame hooks. Model hooks accept `{ providerID }` to limit them to one provider.
- `ctx.tool.hook`: `execute.before` (may rewrite `input`) and `execute.after`.
- `ctx.permission.hook`: `evaluate`.
- `ctx.event.subscribe`: runtime events.

This repo uses two hooks: `ctx.session.hook('compaction', ...)` (`src/modules/compaction/server.ts`) and `ctx.session.hook('context', ...)` (`src/modules/structured-output/server.ts`), which reshapes the tools of each model request. A module that needs a hook next to its tools wraps the `defineModulePlugin` result in its own `Plugin.define`, as `structured-output` does; a tool that needs a session's metadata reads it through the factory's optional `sessions` (`IModuleEnv`), which only OpenCode sets. A `deny` permission rule removes a tool before the `context` hook runs, so the hook only sees tools the agent allows. The `experimental.*` hooks can change between minor versions; verify them against the pinned version before relying on them.

## Testing

Specs call a tool through `invokeTool(definition, args, context?)` (`_core/testing/tool-context.ts`). It parses the arguments with the tool's own schema, as both hosts do, awaits `execute` and returns the text. The context defaults to `createTestToolContext()`, whose `progress` does nothing; `createTestToolContext({ directory })` sets the directory. A rejection test passes the promise to `assert.rejects`. From a hypothetical `example/services/http-session.service.spec.ts`:

```typescript
const output = await invokeTool(createLoginTool(sessions), {
  tokenFile,
  baseUrl: BASE_URL,
  session: 'qa',
})

const attempt = invokeTool(createLoginTool(new HttpSessionService()), {
  token: 'a',
  tokenFile: '/tmp/b',
})
await assert.rejects(attempt, /Pass exactly one of token or tokenFile/u)
```

Specs use `node:test` and `node:assert/strict`, live next to the code as `*.spec.ts`, and run from the build output: `pnpm test` builds and runs `node --test 'dist/**/*.spec.js'`. To run one module, build and pass that module's compiled specs to `node --test`, in one `check_run` call with the repository root as an absolute `cwd`: `check_run({ cwd: "<absolute repository root>", commands: ["pnpm build", "node --test 'dist/modules/<module>/**/*.spec.js'"], timeoutMinutes: 10 })`. Mock `fetch` and other boundaries; for credentials, seed a temporary SQLite file with the `credential` table and pass its path to `new CredentialStoreService(dbPath)` (see `_core/services/credential-store.service.spec.ts`).

## Live-loading a plugin

Unit specs cannot show that OpenCode accepts the plugin. To check a real load, run the built binary against an isolated sandbox: separate `XDG_CONFIG_HOME`, `XDG_DATA_HOME` and cache directories so the run touches none of your real config, a config whose `plugins` entry is a directory containing a `server.js` that re-exports the built module, a provider entry pointing at a mock OpenAI-compatible server that replays scripted tool calls, and `opencode run --format json` with the permission rules set to allow. Then assert on the tool results in the JSON events. A plugin that is dropped for a bad entry path, a tool dropped for a name collision, or a schema that lost its descriptions only shows up this way. Keep the sandbox in scratch space, not in the repo.

## Build and install

- `pnpm build` runs `tsc` and `scripts/copy-assets.js` (copies the `.txt` and `.lua` files from `src/` into `dist/`).
- `pnpm symlink:opencode` builds, then `scripts/link-opencode.sh` copies `src/skills/*/` and `src/commands/*.md` into `~/.config/opencode/`, copies `AGENTS.md`, and writes `opencode.json` with `plugins` set to every `dist/modules/*/` directory that has a `server.js`. It copies real files, not symlinks, so containers that bind-mount `~/.config/opencode/` see them. Before copying anything it exits unless `opencode.json` sets `tool_output.max_bytes` and `max_lines`, and refuses any skill that would not fit them whole (its size plus 2,048 bytes and 20 lines for the skill tool's wrapper), because OpenCode cuts a longer tool result; raise `tool_output` when a skill outgrows it. Re-run it after any change to skills, commands, `opencode.json` or a module.
- `pnpm symlink:claude-code` builds and registers `dist/mcp/server.js` as the `opencode` MCP server (`claude mcp add --scope user`). `pnpm symlink` does both.
- `pnpm typecheck` (`tsc --noEmit`), `pnpm lint` (oxlint), `pnpm format` (oxfmt). Run the build, the typecheck, the lint and `pnpm format:check` through `check_run`, as every gate is.

## Deliberately not adopted

- **Runtime permission prompts.** v2 gives plugin tools no way to ask, and the repo removed the prompts; static agent rules and Claude Code rules are the only gate. See Access control.
- **The `permission` domain hook (`evaluate`).** Not used; static rules are visible and enough. Adopt it only for a rule that cannot be expressed per tool name, and verify that it fires for plugin tools on the pinned version first.
- **`ctx.tool.hook` as a wrapper for every tool.** The two adapters are already the error boundary, and the hooks fire for built-in tools too. Use them only for a genuinely global concern.
- **Plugin-registered tools only.** Every tool goes through a module so it can take injected services, be unit-tested through `invokeTool` with mocks, and also run under the Claude Code bridge. This skill does not cover any standalone file-based tool mechanism in v2, and nothing in the repo uses one.
- **Namespaces and Code Mode for repo tools.** Direct, unprefixed tools so permission rules match names.
- **Registering an OAuth `refresh` with OpenCode** for a provider the module refreshes itself.
- **The in-process OpenCode client for general tool logic.** Tools are outward integrations and do not drive session state.

## Anti-patterns

- Writing v1 code: importing `@opencode-ai/plugin`, `tool()`, `tool.schema`, a returned `Hooks` object, an `auth` block with `loader`, `client.app.log`, `client.tui.showToast`, `context.ask`
- Implying house-library items (`BaseTool`, `defineTool`, `defineModulePlugin`, `MarkdownBuilder`, `PluginError`, `Logger`) are part of `@opencode/plugin`
- Registering a plugin entry as a file path instead of a directory with a `server.js`, or a module without `server.ts`
- Adding a module to OpenCode but not to the `MODULES` map in `src/modules/registry.ts` (or the reverse) without meaning to
- Passing a zod schema straight to `ctx.tool` instead of going through `defineModulePlugin`, which loses every `.describe()`
- A tool name that collides with a built-in tool or namespace (`browser_*`); OpenCode drops it silently
- Leaving Code Mode on, or adding a namespace, for repo tools
- Writing to stdout (`console.log`, `process.stdout`) anywhere in module code
- A factory that throws on missing credentials or config instead of logging and failing the tool at call time
- Reading credentials from `auth.json` or caching them at startup instead of through `CredentialStoreService` at call time
- Registering an OAuth `refresh` for a rotating-refresh-token provider
- Refreshing a rotating token without a lock across processes (the harnesses refresh from separate processes), or using the new access token before writing the rotated pair back
- Top-level `import 'node:sqlite'` (breaks under Bun)
- `process.cwd()` in a tool instead of `context.directory`
- Tools bypassing an orchestration service that branches, combines calls or holds state, or an orchestration method that only hands one API result to one formatter
- A tool written as a class, through `BaseTool` or `defineTool`, or with a try/catch that only prefixes the error
- Manual string-concatenated markdown tables instead of `MarkdownBuilder.table()`
- Duplicated helpers across modules instead of `_core` utilities (`formatBytes` per module)
- Auth error messages without the `/connect` instruction
- Referencing `core/` instead of `_core/`
- Linking to `sst/opencode` instead of `anomalyco/opencode`
- Using `any` (use `unknown` and narrow) and `function` declarations (use arrow functions)
