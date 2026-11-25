---
name: opencode-config-workflow
description: "Workflow methodology for working on global (`~/.config/opencode/`) and per-project (`.opencode/`) OpenCode configurations with minimal API requests while ensuring schema compliance."
---
# OpenCode Config Workflow

Workflow methodology for working on global (`~/.config/opencode/`) and per-project (`.opencode/`)
OpenCode configurations with minimal API requests while ensuring schema compliance.

## When to Use

- Modifying `opencode.jsonc` (any scope) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use this skill to decide the most API-efficient approach
- Creating new agents, skills, commands, rules, or plugins ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pick global vs project placement
- Validating config after changes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run the free shell-based validation pipeline
- Deciding "should this go in global or project config?" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use the decision framework
- Debugging broken config ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use escape hatches first, targeted fix second
- Migrating config after OpenCode updates ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use config-sync + batch edits
- Any config task where you want to minimize LLM turns ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use the efficiency patterns

## Do NOT Use When

- You need to know the exact schema shape of an `opencode.jsonc` field ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `customize-opencode` skill or fetch `https://opencode.ai/config.json`
- You need the full config surface reference ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `opencode-configure` skill
- You need to create a specific entity type (agent, skill, command) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use the dedicated creator skill (`opencode-agent-creator`, `skill-creator`, `opencode-command-creator`)

---

## 5 Types of Config Work

Every config task falls into one of these types. Each has a distinct optimal workflow.

### Type A: Create New Config Entities

**Examples:** New agent, skill, command, rule, tool, plugin, MCP server, provider model

**Optimal Workflow (2-3 turns):**
1. **Turn 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Load creator skill (if complex) or proceed directly (if format is memorized)
2. **Turn 2** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Write entity file + update `opencode.jsonc` references (batch in parallel)
3. **Turn 3** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Validate (shell, free) + report

**API Cost:** 2-3 turns
**Key Savings:** Creator skills embed schema rules ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no extra lookups needed.

### Type B: Modify Existing Config

**Examples:** Change model/provider, edit agent prompt, update permissions, add instruction path

**Optimal Workflow (1-2 turns):**
1. **Turn 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Read affected files (parallel) + apply edits via `json-edit`/`Edit`
2. **Turn 2** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Validate (shell, free) + report

**API Cost:** 1-2 turns
**Key Savings:** Read and edit in same turn. Use `json-edit` for JSONC (0 LLM turns per edit).

### Type C: Validate Config (Free ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 0 LLM Turns)

**Examples:** JSONC syntax check, schema compliance, reference integrity, frontmatter validation

**Free validation commands:**
```bash
# JSONC syntax check
node -e '
const fs = require("fs");
let c = fs.readFileSync("opencode.jsonc", "utf-8");
c = c.replace(/\/\/.*$/gm, "").replace(/\/\*[\s\S]*?\*\//g, "");
JSON.parse(c);
console.log("OK");
'

# Plugin path existence
for p in $(node -e '
const fs = require("fs");
let c = fs.readFileSync("opencode.jsonc", "utf-8");
c = c.replace(/\/\/.*$/gm, "").replace(/\/\*[\s\S]*?\*\//g, "");
const cfg = JSON.parse(c);
(cfg.plugin || []).forEach(p => console.log(p));
'); do
  [ -f "$p" ] && echo "ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ $p" || echo "ÃƒÂ¢Ã…â€œÃ¢â‚¬â€ $p NOT FOUND"
done

# Agent frontmatter check
for f in agents/*.md; do
  head -1 "$f" | grep -q "^---" && echo "ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ $f" || echo "ÃƒÂ¢Ã…â€œÃ¢â‚¬â€ $f missing frontmatter"
done
```

**API Cost:** 0 turns ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all shell commands, no LLM calls.

### Type D: Debug Broken Config

**Examples:** opencode won't start, plugin not loading, MCP not connecting, skill not found

**Optimal Workflow (1-3 turns):**
1. **Turn 0** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Use escape hatches first (free, no LLM):
   - `OPENCODE_DISABLE_PROJECT_CONFIG=1` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip broken project config, start from globals
   - `OPENCODE_CONFIG_CONTENT='{"$schema":"https://opencode.ai/config.json"}'` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â inject inline JSON
   - `OPENCODE_DISABLE_DEFAULT_PLUGINS=1` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip default plugins
   - `OPENCODE_PURE=1` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip external plugins entirely
2. **Turn 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Identify root cause (read error messages, check referenced files)
3. **Turn 2** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Fix and validate
4. **Turn 3** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Report

**API Cost:** 1-3 turns
**Key Savings:** Always try escape hatches before debugging ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they cost 0 LLM turns and often bypass the broken config entirely, letting you see the error from outside the broken session.

### Type E: Migrate/Upgrade Config

**Examples:** Schema version upgrade, deprecated key replacement, structural reorganization

**Optimal Workflow (2-3 turns):**
1. **Turn 0** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Run `config-sync` script to detect drift (free)
2. **Turn 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Fetch schema + compare current config
3. **Turn 2** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Batch ALL migration edits (parallel, one turn)
4. **Turn 3** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Validate + report

**API Cost:** 2-3 turns
**Key Savings:** Batch ALL migration changes in one turn ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never one-at-a-time.

---

## Tool Selection Matrix

| Tool | Best For | Why Efficient |
|------|----------|---------------|
| `json-edit` | `opencode.jsonc` field changes (set, merge, arrayAppend, delete) | 0 LLM turns per edit |
| `Write` | Creating new agent/skill/command/rule `.md` files | 1 turn per file (single write) |
| `Edit` | Modifying existing `.md` files (surgical changes) | 0 LLM turns per edit |
| `conf-edit` | `.env` key-value changes | 0 LLM turns |
| `yaml-edit` | YAML frontmatter in agent/command files | 0 LLM turns |
| `multi-edit` | Batch find-and-replace across multiple files | 0 LLM turns |
| Shell validation | JSONC check, file existence, frontmatter check | 0 LLM turns (free) |
| `validate-delegation` | Check delegation target integrity | 0 LLM turns |

**Golden Rule:** For JSONC edits, always prefer `json-edit` over reading + rewriting the entire file. A `json-edit` call costs 1 tool invocation (no LLM overhead). Rewriting a 120-line file costs all those tokens in context.

---

## Skill/Agent Selection Matrix

| Surface | Optimal Choice | Skip When |
|---------|---------------|-----------|
| `opencode.jsonc` field changes | `customize-opencode` skill or fetch schema URL | Edit is trivial (just `json-edit` directly) |
| Agent creation | `opencode-agent-creator` skill | Format is memorized (simple case) |
| Skill creation | `skill-creator` skill | Format is memorized |
| Command creation | `opencode-command-creator` skill | Format is memorized |
| Plugin creation | `opencode-plugin-creator` skill | Format is memorized |
| Multi-surface orchestration | `config-orchestrator` subagent | Only 1-2 files to change |
| Project `.opencode/` init | `provision` skill | `.opencode/` already exists |
| Schema compliance | `config-sync` script | Schema is up to date |
| Config workflow methodology | **This skill** (`opencode-config-workflow`) | Task is just a simple key-value change |

**Efficiency Principle ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Load Once, Apply Many:**
If you need multiple config changes in one session:
1. Load the relevant skill ONCE
2. Apply ALL changes while the skill context is active
3. Do NOT unload/reload between changes

---

## Global vs Per-Project Decision Framework

### The "Would Another Project Use This?" Heuristic

| Question | Answer ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Action |
|----------|----------------|
| Would another project use this tool/plugin/rule? | ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **Global** `~/.config/opencode/` |
| Is this specific to this project's domain? | ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **Project** `.opencode/` |
| Not sure? | ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Start project-specific, promote to global at #2 reuse |

### What Must Go Where

| Entity Type | Global? | Project? | Because |
|-------------|---------|----------|---------|
| **Tools** (`.ts` files) | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Always | ÃƒÂ¢Ã‚ÂÃ…â€™ Never | Project `.opencode/tools/` is NOT auto-discovered by OpenCode |
| **Plugins** (hook plugins) | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Always | ÃƒÂ¢Ã‚ÂÃ…â€™ Never | Project `.opencode/plugins/` is NOT auto-discovered |
| **Core rules** (shell, security, karpathy) | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Always | ÃƒÂ¢Ã‚ÂÃ…â€™ Never | Shared conventions across all projects |
| **Reusable agents** | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | ÃƒÂ¢Ã‚ÂÃ…â€™ | Put shared agents in global |
| **Project-specific agents** | ÃƒÂ¢Ã‚ÂÃ…â€™ | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | `.opencode/agents/*.md` |
| **Reusable skills** | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | ÃƒÂ¢Ã‚ÂÃ…â€™ | Put shared skills in global |
| **Project-specific skills** | ÃƒÂ¢Ã‚ÂÃ…â€™ | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | `.opencode/skills/*/SKILL.md` |
| **Project rules** | ÃƒÂ¢Ã‚ÂÃ…â€™ | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | `.opencode/rules/*.md` |
| **Config overrides** | ÃƒÂ¢Ã‚ÂÃ…â€™ | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | `.opencode/opencode.json` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only set DIFFERENCES from global |
| **Context (durable knowledge)** | ÃƒÂ¢Ã‚ÂÃ…â€™ | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | `.opencode/context/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â committed to git |
| **State (session data)** | ÃƒÂ¢Ã‚ÂÃ…â€™ | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ | `.opencode/state/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â gitignored |

### Config Merge Behavior

Project `.opencode/opencode.json` is deep-merged into global `~/.config/opencode/opencode.jsonc`.
Project takes precedence for overlapping keys. **Only set keys that differ from global.**

### Anti-Patterns

| Anti-Pattern | Problem | Correct |
|-------------|---------|---------|
| Duplicating global agents in project | Wastes writes + extra config entries | Just reference global agents by name |
| Overriding everything in project config | Unnecessary merges, harder to validate | Only override what differs |
| Inlining agent defs in `opencode.json` | Longer file = more tokens | Use file-based definitions (`.opencode/agents/`) |
| Creating project-specific tools | Not auto-discovered | Use global tools or skill scripts instead |

---

## Schema Compliance Strategy

### Truth Hierarchy (in order of authority)

1. **`https://opencode.ai/config.json`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Source of truth (authoritative JSON Schema)
2. `customize-opencode` skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Summary (may be slightly outdated)
3. `opencode-configure` skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Summary (may be slightly outdated)
4. LLM training data ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **Last resort** (most likely outdated)

**If unsure about a field shape, fetch the schema URL.** One `webfetch` call saves 3+ edit-retry cycles.

### Validation Pipeline (0 LLM Turns)

```
Step 1: JSONC parses    node -e "JSON.parse(fs.readFileSync('opencode.jsonc','utf-8')...)"
Step 2: References exist for p in plugin paths; do [ -f "$p" ]
Step 3: Frontmatter ok  head -1 agents/*.md | grep "^---"
Step 4: Schema ok       config-sync script
```

### Validate-Before-Writing Rule

**Always validate JSONC before writing to disk, not after.**
- `json-edit` operations are validated by the tool itself (no write happens on parse failure)
- For Write/Edit operations, run the shell validation immediately after
- A validation failure caught before the user sees it costs 0 trust. One caught after costs trust.

---

## Config Task Reference: API Cost Per Scenario

| Scenario | Turns | Steps |
|----------|-------|-------|
| Simple key change (e.g., change default model) | **2** | Read + `json-edit` + validate (shell, free) + report |
| Add new provider/model | **2** | Read + `json-edit` merge + validate + report |
| New agent definition | **3** | Load creator skill (or proceed if format known) + Write file + validate + report |
| New skill | **3** | Load `skill-creator` + Write SKILL.md + validate + report |
| New MCP server | **2** | Read + `json-edit` merge + validate + report |
| New command | **2** | Write command.md + verify instructions path + report |
| New rule | **2** | Write rule.md + verify `opencode.jsonc` instructions path + report |
| Multi-surface change | **3** | Load skill once + batch all writes + validate + report |
| Schema migration | **2** | `config-sync` (free) + batch edits + validate + report |
| Fix broken config | **2** | Escape hatch (free) + targeted fix + validate + report |
| Full project `.opencode/` init | **3** | `provision` skill + context dirs + `.gitignore` + validate |

### Maximum Efficiency Checklist

Before any config operation, verify:
- [ ] Can this be done in **2 turns or less**?
- [ ] Am I using `json-edit`/`Edit` instead of LLM-powered file rewriting?
- [ ] Are all **edits batched** in one turn?
- [ ] Is the relevant skill already loaded (avoiding reload)?
- [ ] Is this going in the **right place** (global vs project)?
- [ ] Will the config **parse on first attempt** (validate before writing)?

---

## Worked Example: Changing the Default Model

**Goal:** Change `model` from `opencode/deepseek-v4-flash-free` to `ollama/deepseek-v4-flash:0731-cloud`

**Type:** B (Modify) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Simple key change

**Cost:** 2 turns (optimal)

```
Turn 1:
  1. json-edit { file: "opencode.jsonc", action: "set", path: "$.model",
       value: "ollama/deepseek-v4-flash:0731-cloud" }

Turn 2:
  1. Validate: node -e 'JSON.parse(fs.readFileSync(...)...)'
  2. Report: "Changed model from X to Y. Restart opencode to apply."
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `opencode-configure` | Full config surface reference (all 8 surfaces, includes `opencode-config`) |
| `customize-opencode` | Schema shapes and field-level details for `opencode.json` |
| `config-sync` | Schema compliance checking and drift detection |
| `opencode-agent-creator` | Deep guide for creating agent definitions |
| `skill-creator` | Deep guide for creating skills |
| `opencode-command-creator` | Deep guide for creating commands |
| `opencode-plugin-creator` | Deep guide for creating plugins |
| `config-orchestrator` agent | Subagent for multi-surface config orchestration |
| `provision` | Auto-generate project `.opencode/` from stack fingerprint |
