# OpenCode Kit

Portable payload of OpenCode skills and plugins, plus a single installer.

## What's inside

| Path | Contents |
|------|----------|
| `install.ps1` | The one file you run. Copies payloads and merges config. |
| `skills/` | 2,277 skills from the global OpenCode config. |
| `plugins/` | Local plugin entry points (`index.ts`, `index.js`, `ecc-hooks.ts`, `lib/`). |
| `config/opencode.kit.json` | The only config keys the kit owns: `plugins`, `skills`. |
| `package.json` | npm dependencies for the npm-declared plugin. |

No API keys, tokens, or absolute machine paths are stored in this repo. The
original `opencode.jsonc` had live Obsidian and Context7 keys and was
deliberately **not** copied; the installer merges only the two keys above into
whatever config already exists. Provider and MCP setup stays your responsibility
on a new machine.

## Install

```powershell
# Global install (default): ~\.config\opencode
.\install.ps1

# Project-local install: <cwd>\.opencode
.\install.ps1 -Target Project

# Preview without changing anything
.\install.ps1 -WhatIf

# Custom destination / config
.\install.ps1 -TargetDir 'C:\some\dir' -ConfigFile 'C:\some\dir\opencode.jsonc'

# Skip npm plugin installation
.\install.ps1 -SkipNpm
```

The installer is idempotent: re-running copies changed files and leaves extra
files in place. Before editing a config file it writes a timestamped
`.bak-install-<timestamp>` copy.

## Requirements

- Windows PowerShell 5.1+ (uses `robocopy`) or PowerShell 7 on Windows.
- `npm` on PATH unless `-SkipNpm` is used.

For Linux/macOS, the payload folders are portable; only the installer needs a
bash equivalent (`cp -R` plus the same config merge).
