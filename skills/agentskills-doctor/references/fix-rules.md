# Fix Rules for Agent Skills Findings

Per-finding fix guidance, keyed by skillscheck check ID where one exists.
Load this when the user asks to fix validation findings.

Two fix tiers:

- **Safe tier** — mechanical, behavior-preserving. Auto-apply without
  per-item confirmation.
- **Judgment tier** — rewrites or removals that change meaning. Confirm
  with the user before applying (per finding or a blanket "fix all").

Prefer `uvx skillscheck --fix` for the findings it auto-fixes, then
hand-fix the rest using the rules below.

## Spec compliance (category 1)

### Naming — `[1a.name.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| Uppercase in `name` | Safe | Lowercase it (`PDF-Processing` → `pdf-processing`). |
| Leading/trailing hyphen | Safe | Strip it (`-pdf` → `pdf`). |
| Consecutive hyphens | Safe | Collapse to one (`pdf--processing` → `pdf-processing`). |
| `name` ≠ directory name | Safe | Rename the directory to match `name` (or change `name` to match the directory — prefer renaming the directory, since the name is the public identifier). |
| Missing/empty `name` | Judgment | Derive from the directory name; confirm with the user. |

### Frontmatter — `[1b.frontmatter.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| Missing `description` | Judgment | Draft one from the body (imperative, what + when); confirm. |
| Invalid YAML | Judgment | Fix the syntax error; preserve all fields and values. |
| Unknown frontmatter field | Judgment | Move it under `metadata:` if it's a custom property, or remove it if redundant. Confirm before removing. |
| `description` over 1024 chars | Safe | Trim to ≤ 1024 by cutting redundant clauses; keep what + when + trigger keywords. |
| `compatibility` over 500 chars | Safe | Trim to the essential environment requirements. |

### `allowed-tools` — `[1c.allowed-tools.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| Unknown tool (`[1c.allowed-tools.unknown-tool]`) | Judgment | Usually a false positive from space-separated subcommand wildcards (`Bash(git status *)` splits into fragments). Leave as-is if the syntax matches the host agent's convention; otherwise rewrite to recognized tool names. Explain to the user before changing. |

### Cross-skill duplicates — `[1d.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| Duplicate skill names | Judgment | Determine which skill is canonical with the user; rename or remove the other. |

## Quality (category 2)

### Description — `[2a.description.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| User-centric phrasing (`[2a.description.user-centric]`) | Safe | Convert to agent-directed form: "Use when the user asks/wants/mentions X" → "Use when <verb>ing X". E.g. "Use when the user asks to create a skill" → "Use when creating a skill". |
| Too short / missing "use when" hint | Judgment | Expand to state what the skill does AND when to use it, with trigger keywords. Confirm the rewrite. |
| Keyword-stuffing (`[2a.description.keyword-stuffing]`) | Judgment | Merge the comma-separated fragments into 1–2 sentences that explain what the skill does and when to activate it; keep the keywords as part of the prose. Confirm the rewrite. |

### Secrets and assets — `[2b.*]`, `[2c.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| Leaked secret (API key, token, private key, `.env`) | Judgment | Remove the secret immediately and replace with a placeholder; tell the user to rotate the credential. Never commit the real value. |
| Binary file in skill | Judgment | Confirm whether it's needed; remove or replace with a text/template equivalent. |
| Oversized asset | Judgment | Compress, split, or move to external storage; confirm. |

### Files and links — `[2d.*]`, `[2e.*]`

| Finding | Tier | Fix |
| --- | --- | --- |
| Extraneous root file (README, LICENSE, Makefile) | Judgment | Move license text into the `license` frontmatter field or a bundled file; remove build files. Confirm before deleting. |
| Orphaned file in `scripts/`/`references/`/`assets/` not referenced from `SKILL.md` | Judgment | Either reference it from `SKILL.md` with an explicit load trigger, or remove it. Confirm which. |
| Broken local markdown link | Safe | Fix the path to an existing file, or remove the link if the target is gone. |
| Broken fragment anchor | Safe | Fix the anchor to match an existing heading. |
| Unclosed code fence | Safe | Add the closing fence. |

## Progressive disclosure (category 3)

| Finding | Tier | Fix |
| --- | --- | --- |
| `SKILL.md` over 500 lines / token budget | Judgment | Move detail sections into `references/` and add explicit load triggers ("Read `references/x.md` when …"). Keep gotchas and the core workflow in `SKILL.md`. Confirm the split. |
| Reference file over token budget | Judgment | Split the reference into focused files; confirm. |
| Reference nesting too deep | Judgment | Flatten the reference tree; keep file references one level deep from `SKILL.md`. Confirm. |

## Agent compatibility (category 4)

| Finding | Tier | Fix |
| --- | --- | --- |
| Invalid agent config (`plugin.json`, `gemini-extension.json`, etc.) | Judgment | Fix the field to match the platform's schema; confirm. |
| Cross-agent field mismatch (name/version/description differ between config files) | Judgment | Align the fields to the canonical source (usually `SKILL.md` frontmatter); confirm. |
| Deprecated rules file (`.cursorrules`, `.roorules`, `.windsurfrules`) | Judgment | Migrate content into the platform's current convention; confirm. |

## After fixing

Re-run `uvx skillscheck <dir>` (and `skills-ref validate ./<name>` when
installed). Confirm every fixed finding is gone and no new findings were
introduced. Report the final result and the list of applied changes.
