---
name: project-config-composer
description: "Takes a stack fingerprint and resource recommendations and auto-generates a lean, production-quality `.opencode/` configuration for the target project."
---
# Project Config Composer

Takes a stack fingerprint and resource recommendations and auto-generates a lean, production-quality `.opencode/` configuration for the target project.

## When to Use

- During `/hub-setup provision` after `@stack-detector` + `stack-recommender` have run
- When regenerating an existing project's `.opencode/` from an updated fingerprint
- When setting up a greenfield project from a natural language description
- As a standalone call when the user already knows what they want

## Principles

1. **Reference, don't copy** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â project configs reference global resources; never duplicate them. The project `.opencode/` only contains project-specific overrides, new files, and references.
2. **Minimal by default** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â start with only what's needed. Add more as the project evolves.
3. **Merge-safe** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every generated file is safe to re-run (writes are idempotent, merges conventions rather than replacing them).
4. **Human-editable** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â output is clean, well-commented, and follows standard opencode conventions.
5. **Synthesize, never copy** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a hint pack (`templates/projects/*/manifest.json`) is a starting point. Generate config tailored to the actual codebase; do not copy pack directories.
6. **Hints are non-terminal** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the pack lacks the specific you need, research it (Context7 / SearXNG / gh_grep) rather than falling back to defaults.
7. **Write, don't ask** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â provisioning owns `.opencode/`; the command that invoked it is the consent. Do not add confirmation prompts.

## Input

Takes two inputs (either from previous pipeline steps or direct arguments):

### A. Stack Fingerprint (from @stack-detector)
```json
{
  "fingerprint": { ... },
  "projectType": "webapp",
  "detected": true
}
```

### B. Recommendations (from stack-recommender)
```json
{
  "recommends": {
    "hint_pack": "nextjs-webapp",
    "hints": [...],
    "research": [...],
    "preferences": [...],
    "skills": [...],
    "agents": [...],
    "rules": [...],
    "commands": [...],
    "notes": [...],
    "gaps": [...]
  }
}
```

## Generated Files

The composer creates the following structure under the project's `.opencode/`:

```
.opencode/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ opencode.jsonc              # Project-level config (valid keys only; references global resources)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ rules/                      # Synthesized from observed conventions + research
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ project-conventions.md  # Conventions actually observed in the codebase
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ project-testing.md      # Testing approach matching the codebase
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ {category}-{name}.md    # Fine-grained rules from templates/rules (if recommended)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...                     # One per recommended fine_rule
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ tools/                      # Synthesized tools (only on a genuine gap)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ {name}.ts               # TypeScript tools from templates/tools (if recommended)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...                     # One per recommended tool
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ skills/                     # Only project-specific skills the codebase needs
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...                     # Reference global skills; never duplicate them
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ agents/                     # Project-specific agent wrappers (if needed)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ... (only if gaps identified)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ instructions/               # AGENTS.md fragment for project-specific docs
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ README.md               # Brief note about what was generated
```

> **Local availability gate + synthesis.** Check `templates/projects/*/manifest.json` for a
> matching **hint pack** and record what was found (`{found: [...], none: bool}`). A hint pack is a
> starting point, not a payload: its `hints`, `research`, and `preferences` inform synthesis, but no
> `agents/`, `rules/`, `skills/`, or `tools/` directories are copied. If the pack lacks the specific
> you need, research it (Context7 / SearXNG / gh_grep) and cache under `.opencode/context/research/`.

### 1. opencode.jsonc

The main project config file. It:
- Sets `"$schema"` to the opencode config schema
- Includes project-specific instructions and rules
- Selects relevant global skills via filter tags
- Optionally overrides the default agent for this project

> **ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â CRITICAL: Only valid schema keys allowed.** The OpenCode config schema (`https://opencode.ai/config.json`) sets `additionalProperties: false`. Generated files MUST contain ONLY the following valid top-level keys: `$schema`, `shell`, `logLevel`, `server`, `command`, `skills`, `references`, `watcher`, `snapshot`, `plugin`, `share`, `autoupdate`, `disabled_providers`, `enabled_providers`, `model`, `small_model`, `default_agent`, `username`, `agent`, `provider`, `mcp`, `formatter`, `lsp`, `instructions`, `permission`, `tools`, `attachment`, `enterprise`, `tool_output`, `compaction`, `experimental`. Keys like `extends`, `agents` (plural), `project`, `rules`, `state`, `context`, `cache` are NOT valid and will cause validation errors.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "AGENTS.md",
    "./rules/project-conventions.md",
    "./rules/project-testing.md"
  ],
  "permission": {
    "edit": "allow",
    "bash": "allow"
  }
}
```

> **`resource_tags` is NOT a valid top-level config key ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never emit it.** Resource selection
> happens through `instructions`, `agent`, and `skills`; tag filtering belongs in hint-pack
> metadata, not the generated project config.

### 2. Project Conventions Rule

Auto-generated from the detected stack:

```markdown
---
name: project-conventions
description: Auto-generated conventions for [framework] project
---

# Project Conventions

## Tech Stack
- **Language:** TypeScript (strict mode)
- **Framework:** Next.js 15 (App Router)
- **CSS:** Tailwind CSS v4
- **Database:** PostgreSQL via Prisma
- **Testing:** Vitest (unit) + Playwright (e2e)

## Code Conventions
- Use `async/await` over raw promises
- Preher server components by default; client components only when needed
- Route handlers in `app/api/` directory
- Prisma schema follows singular table naming: `user`, `post`, `comment`
- All API routes must be validated with Zod schemas

## Naming
- Components: PascalCase
- Hooks: camelCase with `use` prefix
- Utilities: camelCase
- Types/Interfaces: PascalCase with `Type`/`Interface` suffix where disambiguation helps

## Imports
- Absolute imports using `@/` alias
- Group: external ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ internal ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ types
```

### 3. Tools (from templates/tools)

When the recommendations include `tools[]`, the composer generates TypeScript tool files from the local template catalog at `~/.config/opencode/templates/tools/`:

```bash
TOOL_TEMPLATES_DIR="$HOME/.config/opencode/templates/tools"
PROJECT_TOOLS_DIR="$PROJECT_DIR/.opencode/tools"
```

For each recommended tool, the composer:
1. Reads the template file from `$TOOL_TEMPLATES_DIR/{category}/{name}.ts`
2. Replaces `{{PLACEHOLDERS}}` with values from the stack fingerprint (e.g., `{{PROJECT_NAME}}`, `{{LANGUAGE}}`, `{{FRAMEWORK}}`)
3. Writes the result to `$PROJECT_TOOLS_DIR/{name}.ts`
4. Registers the tool in `opencode.jsonc` under the `tools` array

**Template placeholders:**

| Placeholder | Source | Example |
|-------------|--------|---------|
| `{{PROJECT_NAME}}` | Fingerprint or directory name | `my-app` |
| `{{LANGUAGE}}` | `fingerprint.language.primary` | `typescript` |
| `{{FRAMEWORK}}` | `fingerprint.framework.name` | `nextjs` |
| `{{TEST_FRAMEWORK}}` | `fingerprint.testing.frameworks[0].name` | `vitest` |
| `{{PACKAGE_MANAGER}}` | `fingerprint.packageManager.name` | `pnpm` |
| `{{BUILD_TOOL}}` | `fingerprint.buildTool.name` | `tsc` |
| `{{ORM}}` | `fingerprint.database.orm` | `prisma` |
| `{{DATABASE}}` | `fingerprint.database.database` | `postgresql` |

**Example output** (from `templates/tools/typescript/type-check.ts`):

```typescript
// Auto-generated from tool-template: typescript/type-check.ts
// Project: my-app (TypeScript, Next.js)

import { execSync } from 'child_process'

export default {
  name: 'type-check',
  description: 'Run TypeScript type checking for my-app',
  handler: () => {
    execSync('npx tsc --noEmit', { stdio: 'inherit' })
  }
}
```

### 4. Fine-Grained Rules (from templates/rules)

When the recommendations include `fine_rules[]`, the composer generates granular rule files from the local template catalog at `~/.config/opencode/templates/rules/`:

```bash
RULE_TEMPLATES_DIR="$HOME/.config/opencode/templates/rules"
PROJECT_RULES_DIR="$PROJECT_DIR/.opencode/rules"
```

For each recommended fine_rule, the composer:
1. Reads the template file from `$RULE_TEMPLATES_DIR/{category}/{name}.md`
2. Replaces `{{PLACEHOLDERS}}` with values from the stack fingerprint
3. Writes the result to `$PROJECT_RULES_DIR/{category}-{name}.md`
4. Adds the rule to `opencode.jsonc` under `instructions`

**Example output** (from `templates/rules/framework/nextjs.md`):

```markdown
---
name: nextjs-conventions
description: Auto-generated Next.js framework conventions for my-app
tags: [nextjs, react, conventions, framework]
---

# Next.js Conventions

## App Router
- Use `app/` directory for routes (App Router detected)
- Server Components by default; add `'use client'` only when needed
- Route handlers in `app/api/` directory
- Layouts in `app/layout.tsx`, nested layouts in route groups
```

### 4b. Universal Rules: Session Artifact Promotion + Writing Style

Every generated project **must** include two global rules, regardless of stack:

**1. `session-artifact-promotion.md`**

1. Copy `~/.config/opencode/rules/session-artifact-promotion.md` to `.opencode/rules/session-artifact-promotion.md`.
2. Add `"./rules/session-artifact-promotion.md"` to `instructions` in the project `opencode.jsonc`.

Makes session-created tools land in the project's durable `.opencode/` tree instead of being
reinvented next session.

**2. `writing-style.md`**

1. Copy `~/.config/opencode/rules/writing-style.md` to `.opencode/rules/writing-style.md`.
2. Add `"./rules/writing-style.md"` to `instructions` in the project `opencode.jsonc`.

Governs the prose the agent authors in this project ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â say it don't announce it, plain words over
inflated ones, end when the content ends. Keeps the agent's written output from reading as
machine-made.

Both are universal, not stack-specific ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always include them, never gate them behind a
recommendation.

### 5. Agent Wrappers (only when gap is flagged)

If a gap in global resources is detected, the composer generates a minimal project-specific wrapper agent. For example, if no global rule exists for Prisma conventions:

```markdown
---
description: Project-specific Prisma schema review and database migration guidance
mode: subagent
---
<Agent_Prompt>
  <Role>
    You are a database and Prisma specialist for this project.
  </Role>
  <Conventions>
    - Table names are singular: User, Post, Comment
    - All models have `id`, `createdAt`, `updatedAt`
    - Use `@default(autoincrement())` for primary keys
    - Relations use cascade delete by default
  </Conventions>
</Agent_Prompt>
```

## Workflow

### Step 0: Parse Flags

Check for `--minimal` flag: when present, generate only `opencode.jsonc` (valid keys only) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip rules, tools, agents, and instructions. Produces a ~10-line config instead of a full scaffold. Use for quick project setup where per-project rules aren't needed yet.

### Step 0b: Local Availability + Research

1. Enumerate `templates/projects/*/manifest.json` and record `{found: [...], none: bool}`.
2. If a pack matches, treat it as a starting point. If the specific you need is absent, research:
   Context7 (framework/convention docs), SearXNG (stack best practices), gh_grep (real configs).
3. Cache findings under `.opencode/context/research/` (the existing research cache).
4. Synthesize from the codebase + hints + research. Never copy pack directories.

### Step 1: Prepare Output Directory

```bash
PROJECT_DIR="."  # or specified path
mkdir -p "$PROJECT_DIR/.opencode/rules"
mkdir -p "$PROJECT_DIR/.opencode/tools"
mkdir -p "$PROJECT_DIR/.opencode/skills"
mkdir -p "$PROJECT_DIR/.opencode/agents"
mkdir -p "$PROJECT_DIR/.opencode/instructions"
```

> **Do not copy hint-pack directories.** If a hint pack matched, use its `hints`, `research`, and
> `preferences` to drive synthesis. If it lacks the specific you need, research it (Context7 /
> SearXNG / gh_grep) and cache under `.opencode/context/research/`. Global skills and tools are
> referenced, never duplicated into the project.

### Step 2: Generate opencode.jsonc

- Generate a standalone config with the valid keys listed above
- Do NOT include `extends` or `resource_tags` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â neither is a valid config key
- Do NOT include `agents` (plural), `project`, `rules`, `state`, `context`, or `cache` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â these are NOT valid config keys
- Writes are merge-safe and idempotent. Provisioning owns `.opencode/`; the invoking command is the consent ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do NOT add confirmation prompts. Merge conventions rather than clobbering.

### Step 2a: Validate opencode.jsonc against schema

After writing the config file, validate it against the actual OpenCode schema:

```bash
# Validate opencode.jsonc (JSONC-aware: comments + trailing commas) against schema keys
bash ~/.config/opencode/skills/project-config-composer/scripts/validate-config-keys.sh .opencode/opencode.jsonc

# If validation fails, fix the config and re-validate before proceeding
```

### Step 3: Generate Convention Rules

For each detected technology, generate a brief conventions rule file:
- Language conventions (TypeScript strict mode, Python type hints, Rust clippy rules)
- Framework conventions (App Router patterns, Django MTV structure, Rails convention over configuration)
- Testing conventions (mocking strategy, test file placement, naming)
- Database conventions (migration workflow, naming, indexing strategy)
- CSS conventions (Tailwind class ordering, component styling approach)

### Step 3a: Generate Tools (from templates/tools)

If the recommendations include `tools[]`:

1. For each recommended tool, check if a matching template exists at `~/.config/opencode/templates/tools/{category}/{name}.ts`
2. Read the template, replace `{{PLACEHOLDERS}}` with fingerprint values
3. Write the result to `$PROJECT_DIR/.opencode/tools/{name}.ts`
4. Add a `tools` entry to `opencode.jsonc` referencing the generated file

If a tool template doesn't exist locally, suggest running `/resource-hub find tools` to search registries.

### Step 3b: Generate Fine-Grained Rules (from templates/rules)

If the recommendations include `fine_rules[]`:

1. For each recommended fine_rule, check if a matching template exists at `~/.config/opencode/templates/rules/{category}/{name}.md`
2. Read the template, replace `{{PLACEHOLDERS}}` with fingerprint values
3. Write the result to `$PROJECT_DIR/.opencode/rules/{category}-{name}.md`
4. Add the rule to `opencode.jsonc` under `instructions`

If a rule template doesn't exist locally, suggest running `/resource-hub find rules` to search registries.

### Step 4: Generate Agent Wrappers (if gaps)

For each identified gap, create a minimal agent that fills the missing capability.

### Step 5: Report Results

```markdown
## Generated .opencode/ Configuration

### Files Created
- `.opencode/opencode.jsonc` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Project config (valid keys only)
- `.opencode/rules/project-conventions.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Stack-specific conventions
- `.opencode/rules/project-testing.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Testing guidelines
- `.opencode/tools/{n}.ts` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â N project-specific TypeScript tools (from templates/tools)
- `.opencode/rules/{category}-{name}.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â M fine-grained convention rules (from templates/rules)
- `.opencode/skills/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Project-specific skills only (global skills referenced, not copied)
- `.opencode/tools/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Synthesized tools (only on a genuine gap)

### Recommendations Applied
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Skills/agents/rules referenced (global resources, never duplicated)
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ 2 agents available for subdelegation
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Hint pack: nextjs-webapp (starting point; config synthesized from the codebase)
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ N tools generated from templates/tools
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ M fine-grained rules generated from templates/rules

### Gaps Identified
- ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â No global skill for Next.js App Router ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ created project agent wrapper
- ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â No global rule for Prisma conventions ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ added to project rules
- ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â No tool template for {missing_tool} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ suggest `/resource-hub find tools`
- ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â No rule template for {missing_rule} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ suggest `/resource-hub find rules`

### Next Steps
1. Review generated files and customize as needed
2. Run `/git-hub commit` to commit initial config
3. Start using OpenCode with stack-aware defaults
```

## Integration

### Via init-project provision flow

```
@stack-detector ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ stack-recommender ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ project-config-composer ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ .opencode/ output
```

### Via direct invocation

```bash
/hub-setup provision
# Automatically: detect ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ recommend ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ compose
```

### Via natural language

User says "Set up a Next.js project with Prisma" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `@stack-detector` produces
a synthetic fingerprint ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `stack-recommender` maps resources ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `project-config-composer`
generates the config ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all in one pipeline.

## Safety

- Writes are merge-safe and idempotent ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â merge conventions, never clobber unrelated content.
- Provisioning is authorized by the command that invoked it; do not add confirmation prompts.
- Generated rules are *suggestions* ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they should guide, not enforce.
- Always output a `.opencode/instructions/README.md` that explains what was generated and how to customize.
