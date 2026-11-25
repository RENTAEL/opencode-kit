---
name: tool-creator
description: "Use this skill when creating OpenCode TypeScript tools that extend the agent's capabilities. The skill interviews you about what the tool should do, generates valid boilerplate via `tool-scaffolder`, and validates the output."
---
# Tool Creator

Use this skill when creating OpenCode TypeScript tools that extend the agent's capabilities. The skill interviews you about what the tool should do, generates valid boilerplate via `tool-scaffolder`, and validates the output.

## When to Use

- Creating a new TypeScript tool for `~/.config/opencode/tools/` (global scope)
- Creating a project-specific tool in `.opencode/tools/` (project scope)
- Adding a missing tool type: file editing, validation, state management, search, etc.
- User says "create a tool for X" or "I need a tool that does Y"

## When Not to Use

- The task is better served by an existing tool (check `tools/` first)
- The user wants a skill, not a tool (use `/resource-hub create skill`)
- The user wants a slash command (use `opencode-command-creator`)
- The user wants an agent (use `opencode-agent-creator`)

## Workflow

### Step 1: Interview

Ask the user these questions, one at a time:

1. **Name** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â What should the tool be called? (kebab-case, e.g. `my-utility`, `project-info`, `db-migrate`)
2. **Description** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â What does this tool do? (1-2 sentences)
3. **Language** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â TypeScript (native OpenCode tools) or shell (bash)?
4. **Scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Global (available everywhere) or project (available only in this project)?
5. **Parameters** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Does the tool need input parameters?

If the user says yes to parameters, collect each parameter:
- **Name** (camelCase for TS; UPPER_SNAKE for bash convention)
- **Type** (string | number | boolean | array | object)
- **Required?** (true/false)
- **Description** (what the parameter does)
- **Valid values** (optional, for enums)

### Step 2: Generate

Call `tool-scaffolder` with the collected information:

```
tool-scaffolder {
  action: "generate",
  language: "typescript" | "bash",
  name: "<kebab-case-name>",
  description: "<description>",
  params: '[{"name":"...","type":"string","required":true,"description":"..."}]',
  scope: "global" | "project"
}
```

The tool returns `{ ok: true, language: "...", path: "...", params: N, size: N }`.

### Step 3: Validate

Call `tool-scaffolder` with the validate action:

```
tool-scaffolder {
  action: "validate",
  outputPath: "<path from generate step>"
}
```

Validation checks vary by language:

| Language   | Checks                                                                 |
| ---------- | ---------------------------------------------------------------------- |
| TypeScript | import, export default tool(), description, args, async execute        |
| Bash       | shebang (`#!/usr/bin/env bash`), `set -euo pipefail`                     |

If validation fails, fix the issues and re-validate.

### Step 4: Hand Off

Show the user:
- The generated file path
- Parameter count and file size
- A preview of the generated code (first 20 lines)
- Reminder: the handler stub needs custom logic ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â search for `TODO: implement tool logic`

## Tool File Structure

Generated tools follow this canonical pattern:

```typescript
import { tool } from "@opencode-ai/plugin"
import * as fs from "fs"
import * as path from "path"
import { homedir } from "os"

interface MyToolArgs {
  input: string
  verbose?: boolean
}

export default tool({
  description: "What this tool does",
  args: {
    input: tool.schema.string().describe("Input value"),
    verbose: tool.schema.boolean().optional().describe("Enable verbose output"),
  },
  async execute(args: MyToolArgs, context) {
    const projectRoot = context.directory || process.cwd()
    // TODO: implement tool logic
    return JSON.stringify({ ok: true })
  },
})
```

### Bash Output Structure

```
#!/usr/bin/env bash
set -euo pipefail

# <description>

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) INPUT="$2"; shift 2 ;;
    --verbose) VERBOSE=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# TODO: implement tool logic
printf '{"ok": true}\n'
```

## Scope Rules

| Scope   | TypeScript                       | Shell (bash)                                 | Available         |
| ------- | -------------------------------- | -------------------------------------------- | ----------------- |
| global  | `~/.config/opencode/tools/`       | `~/.config/opencode/skills/<name>/scripts/`  | All projects      |
| project | `<project>/.opencode/tools/`      | `<project>/.opencode/skills/<name>/scripts/` | This project only |

**Artifact placement rule:** TypeScript tools go into `tools/` (global) or `.opencode/tools/` (project). Bash scripts go into `skills/<name>/scripts/` (global) or `.opencode/skills/<name>/scripts/` (project). Never create standalone scripts at the project root. See `rules/file-operations.md`.

## Parameter Types

| Type      | TypeScript              | Bash                | Use Case          |
| --------- | ----------------------- | ------------------- | ----------------- |
| `string`    | `tool.schema.string()`    | positional/flag       | Text, paths, IDs    |
| `number`    | `tool.schema.number()`    | positional/flag       | Counts, limits      |
| `boolean`   | `tool.schema.boolean()`   | flag, no value        | Flags, toggles      |
| `array`     | `tool.schema.array()`     | `IFS`-split string    | Lists (of strings)  |
| `object`    | `tool.schema.object()`    | JSON string parse    | Complex nested data |

## Validation Checks

After generation, always validate. The `tool-scaffolder validate` action checks:

**TypeScript:**
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ Import from `@opencode-ai/plugin` present
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ `export default tool(` present
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ `description:` field defined
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ `args:` schema defined
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ `async execute` handler present

**Bash:**
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ `#!/usr/bin/env bash` shebang present
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ `set -euo pipefail` present

## Anti-Patterns

| BAD                                | GOOD                                        |
| ---------------------------------- | ------------------------------------------- |
| Creating a tool that duplicates an existing one | Check `tools/` first, then create     |
| Hand-rolling boilerplate           | Use `tool-scaffolder generate`                |
| Putting tools at project root      | Always in `.opencode/tools/` or `tools/`      |
| Skipping validation                | Always run `tool-scaffolder validate`         |
| Unclear parameter descriptions     | Each param gets a meaningful `.describe()`     |

## Related

- `tool-scaffolder` tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the generator this skill employs
- `opencode-command-creator` skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â for slash commands instead of tools
- `opencode-agent-creator` skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â for agents instead of tools
- `opencode-plugin-creator` skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â for plugins instead of tools
- `rules/artifact-placement.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â where generated files go
