# OpenCode Kit

A portable, repeatable install for the OpenCode skills and plugins accumulated
in a global config directory. Everything lives in one repo; `install.ps1` is the
one file you run.

Public repo: https://github.com/RENTAEL/opencode-kit

## Contents

| Path | What it is |
|------|-----------|
| `install.ps1` | The installer. Copies payloads, merges two config keys, backs up first. |
| `skills/` | 2,277 skill directories (the full `~/.config/opencode/skills` snapshot). |
| `plugins/` | Local plugin entry points: `index.ts`, `index.js`, `ecc-hooks.ts`, `lib/`. |
| `config/opencode.kit.json` | The only config keys the kit owns: `plugins` and `skills`. |
| `package.json` | npm dependencies referenced by the config (`@opencode-ai/plugin`, `oh-my-openagent`). |
| `.gitignore` | Keeps `node_modules/`, backups, and OS junk files out of the repo. |

Repo size is about 218 MB across 13,016 tracked files. The largest single file
is ~13 MB, below GitHub's 100 MB hard limit.

### About the local plugins

- `index.ts` — minimal V2 entry point (`{ id, setup }`), effectively a stub.
- `index.js` — registers tool hooks that auto-approve read-only tools
  (`read`, `glob`, `grep`, `search`, `list`) and known formatter/test commands.
  Everything else still goes through normal permission flow.
- `ecc-hooks.ts` — the ECC V2 hook plugin, with its runtime under `lib/`.

## What is deliberately NOT in this repo

- **Your `opencode.jsonc` providers, MCP servers, agents, permissions, and
  instructions.** The source config contained live Obsidian and Context7 API
  keys and absolute machine paths, so none of it was copied. You set those up
  yourself on a new machine.
- **API keys, tokens, credentials, or customer data.** None are shipped.
- **`node_modules/`** — installed on demand by the installer.

The installer never overwrites your whole config. It only adds missing entries
to the `plugins` and `skills` arrays and leaves every other key untouched.

## Install

```powershell
# Global install (default): ~\.config\opencode
.\install.ps1

# Project-local install: <current directory>\.opencode
.\install.ps1 -Target Project

# Preview only — prints what would happen, changes nothing
.\install.ps1 -WhatIf

# Custom destination and/or config file
.\install.ps1 -TargetDir 'C:\work\my-opencode' -ConfigFile 'C:\work\my-opencode\opencode.jsonc'

# Skip npm plugin installation
.\install.ps1 -SkipNpm
```

`-Target` and `-TargetDir` are mutually exclusive in practice: `-TargetDir`
wins when supplied. `-Confirm` is also available (standard PowerShell
`ShouldProcess` behaviour).

### What a run does, in order

1. Checks that `skills/` and `plugins/` exist beside the script.
2. Copies `skills/` to `<target>\skills` and `plugins/` to `<target>\plugins`
   using `robocopy /E`. Existing extra files in the destination are **left
   alone** — the copy never deletes.
3. Picks the config file: an explicit `-ConfigFile`, else `<target>\opencode.jsonc`,
   else `<target>\opencode.json`, else creates a new `opencode.jsonc`.
4. Writes a timestamped backup: `opencode.jsonc.bak-install-YYYYMMDD-HHMMSS`.
5. Merges the kit's `plugins` and `skills` entries into the config, deduplicated,
   preserving order and all other keys. Valid JSONC comments are stripped
   safely (URLs inside strings are untouched), and the result is written as
   plain JSON with no BOM.
6. Unless `-SkipNpm`: copies `package.json` only if the target has none, then
   runs `npm install --no-audit --no-fund --omit=dev` in the target directory.
   A failed npm install warns but does not fail the whole install.

### Idempotency and rollback

Re-running is safe: arrays are deduplicated, so you do not get repeated entries,
and `robocopy` only copies newer/changed files. Each run still makes a new
config backup, so backups accumulate.

To roll back a config change:

```powershell
$bak = Get-ChildItem '~\.config\opencode' -Filter 'opencode.jsonc.bak-install-*' |
       Sort-Object LastWriteTime -Descending | Select-Object -First 1
Copy-Item $bak.FullName '~\.config\opencode\opencode.jsonc' -Force
```

Removing the installed skills/plugins is a manual choice — the installer does
not delete files from a target, precisely so it cannot destroy your own work.

## Verify the install

```powershell
$dir = "$HOME\.config\opencode"
(Get-ChildItem "$dir\skills" -Directory).Count          # expect 2277
(Get-ChildItem "$dir\plugins" -Recurse -File).Count     # expect 6
$cfg = Get-Content "$dir\opencode.jsonc" -Raw | ConvertFrom-Json
$cfg.plugins                                          # includes ./plugins, oh-my-openagent@latest
$cfg.skills                                           # includes ./skills
```

Then start OpenCode normally and confirm the skills/plugins are visible.

## Requirements

- Windows with PowerShell 5.1+ or PowerShell 7 (the installer uses `robocopy`).
- `npm` on PATH unless `-SkipNpm` is used.

### Linux / macOS

The payload folders are portable; only the installer is Windows-specific.
Manual equivalent:

```bash
cp -R skills  ~/.config/opencode/skills
cp -R plugins ~/.config/opencode/plugins
# then merge the two arrays from config/opencode.kit.json into your opencode.jsonc
```

A `install.sh` is not included yet.

## Updating

```powershell
cd path\to\opencode-kit
git pull
.\install.ps1
```

Note that upstream removals are not propagated: because the copy only adds and
updates, a skill deleted from the repo will remain in your target directory
until you remove it yourself.

## Provenance and licensing

The skills were collected from several sources (ECC, AI-Agent-skills, and
individual skill repos); 43 embedded `.git` directories were stripped before
publishing to reduce size and avoid carrying upstream histories. Licensing and
reuse terms of the individual skills were **not audited** before this repo was
made public. Check a skill's own `LICENSE` or `SKILL.md` before redistributing
it elsewhere.
