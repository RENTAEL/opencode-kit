---
name: config-sync
description: "Enforce that `opencode.jsonc` stays compliant with the latest OpenCode configuration schema."
---
# Config Sync

Enforce that `opencode.jsonc` stays compliant with the latest OpenCode configuration schema.

## Why This Exists

OpenCode's config schema evolves. Keys get deprecated (`mode` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `agent`, `autoshare` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `share`), new keys are added (`tool_output`, `compaction`, `experimental.policies`), and invalid keys that don't exist in the schema can silently cause config load failures.

This skill fetches the latest schema from `https://opencode.ai/config.json`, compares it against the current config, and reports any compliance issues.

## When to Use

- After OpenCode updates
- When config load errors occur
- Before major config changes
- As part of `/verify-hub audit`

## Workflow

### 1. Fetch Current Schema
Fetches `https://opencode.ai/config.json` via web fetch and extracts valid top-level keys, deprecated keys, and new additions.

### 2. Compare Against Local Config
Reads `opencode.jsonc`, parses all top-level keys, and checks:
- Each key exists in schema ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ valid
- Each key is not `@deprecated` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ warn if still used
- No unknown/invalid keys present ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flag as error

### 3. Report & Fix
- Reports all issues grouped by severity (error, warning, info)
- Can auto-fix: remove deprecated keys, add recommended missing keys
- Saves schema to `.opencode/context/research/opencode-config-schema.md` for offline reference

## Script

`scripts/check-schema-compliance.ts` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Standalone compliance checker

```
node scripts/check-schema-compliance.ts         # Check only
node scripts/check-schema-compliance.ts --fix    # Auto-fix issues
node scripts/check-schema-compliance.ts --save   # Save schema to context
```

## Cached Schema

The last-fetched schema is stored at:
`.opencode/context/research/opencode-config-schema.md`

This serves as the durable reference and diff baseline.