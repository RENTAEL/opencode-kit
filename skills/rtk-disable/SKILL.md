---
name: rtk-disable
description: "RTK (output injection) can block visibility of command output in certain environments. When you need to see the raw output of a command for analysis, prefix it with `RTK_DISABLED=1`."
---
# RTK Disable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Single Command

RTK (output injection) can block visibility of command output in certain
environments. When you need to see the raw output of a command for analysis,
prefix it with `RTK_DISABLED=1`.

## When to use

Use `RTK_DISABLED=1` **only** on the specific command whose output you need to
read. Do not apply it globally or to every command ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only the one that is
blocking you.

## How to apply

Prefix the command with the environment variable:

```bash
RTK_DISABLED=1 <your-command>
```

**Examples:**

```bash
# Build verification
RTK_DISABLED=1 go build ./...

# Test output you need to analyze
RTK_DISABLED=1 go test -count=1 -race ./internal/generator/

# Make targets
RTK_DISABLED=1 make test-unit

# Any other command whose output you need
RTK_DISABLED=1 npm run build
RTK_DISABLED=1 cargo test
```

## Scope

- Apply to **one command at a time** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the one whose output is needed.
- Do not wrap entire scripts or multi-command chains unless every command's
  output is needed.
- After capturing the output, continue normally without `RTK_DISABLED=1`.

## Why this works

`RTK_DISABLED=1` signals the RTK layer to pass the command's stdout/stderr
through unmodified, making the output visible to the agent for analysis.
