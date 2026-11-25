# Agent Skills Specification Reference

Complete format specification and creation guidance from
[agentskills.io](https://agentskills.io). Load this when you need exact
field constraints, validation rules, script design guidance, or eval
workflows.

## Directory structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

## `SKILL.md` format

YAML frontmatter followed by Markdown body. The body has no format
restrictions — write whatever helps the agent perform the task. Recommended
body sections: step-by-step instructions, input/output examples, common edge
cases.

### Frontmatter fields

| Field           | Required | Constraints |
| --------------- | -------- | ----------- |
| `name`          | Yes      | Max 64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing hyphen. |
| `description`   | Yes      | Max 1024 chars. Non-empty. What the skill does and when to use it. |
| `license`       | No       | License name or reference to a bundled license file. |
| `compatibility` | No       | Max 500 chars. Environment requirements (product, system packages, network). |
| `metadata`      | No       | Arbitrary string→string map for extra metadata. |
| `allowed-tools` | No       | Space-separated pre-approved tools. (Experimental) |

Minimal example:

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Example with optional fields:

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

### `name` field

- 1–64 characters
- Unicode lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`) only
- Must not start or end with a hyphen
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name

Valid: `pdf-processing`, `data-analysis`, `code-review`
Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen),
`pdf--processing` (consecutive hyphens)

### `description` field

- 1–1024 characters
- Describe both what the skill does and when to use it
- Include specific keywords that help agents identify relevant tasks

Good: `Extracts text and tables from PDF files, fills PDF forms, and merges
multiple PDFs. Use when working with PDF documents or when the user mentions
PDFs, forms, or document extraction.`
Poor: `Helps with PDFs.`

### `license` field

Keep it short — a license name or the name of a bundled license file.
Example: `license: Proprietary. LICENSE.txt has complete terms`

### `compatibility` field

- 1–500 characters if provided
- Only include for specific environment requirements

Examples:

```yaml
compatibility: Designed for Claude Code (or similar products)
compatibility: Requires git, docker, jq, and access to the internet
compatibility: Requires Python 3.14+ and uv
```

Most skills do not need this field.

### `metadata` field

String→string map for properties not defined by the spec. Use reasonably
unique key names to avoid conflicts.

```yaml
metadata:
  author: example-org
  version: "1.0"
```

### `allowed-tools` field

Space-separated string of pre-approved tools. Experimental — support varies
between agent implementations.

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

## Progressive disclosure

Agents load skills progressively:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup
   for all skills.
2. **Instructions** (< 5000 tokens recommended): full `SKILL.md` body loaded
   on activation.
3. **Resources** (as needed): files in `scripts/`, `references/`, `assets/`
   loaded only when required.

Keep `SKILL.md` under 500 lines. Move detailed reference material to
separate files, and tell the agent *when* to load each one.

## Optional directories

### `scripts/`

Executable code agents can run. Scripts should be self-contained (or clearly
document dependencies), include helpful error messages, and handle edge
cases gracefully. Common languages: Python, Bash, JavaScript.

### `references/`

Documentation agents read when needed — `REFERENCE.md` (technical
reference), `FORMS.md` (form templates), or domain-specific files
(`finance.md`, `legal.md`). Keep individual files focused; smaller files
mean less context use.

### `assets/`

Static resources: templates, images, data files (lookup tables, schemas).

## File references

Use relative paths from the skill root. Keep references one level deep from
`SKILL.md` — avoid deeply nested reference chains.

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

## Validation

Two linters validate skills against the specification:

**skillscheck** (<https://github.com/swival/skillscheck>) — recommended.
Validates spec compliance (frontmatter, naming rules, directory-name
consistency, token budgets), quality (description length and "use when"
hints, user-centric phrasing, leaked secrets, broken links, orphaned files),
progressive disclosure (reference token budgets, nesting depth), and
agent-compatibility for Claude Code, Codex, Copilot, Cursor, Gemini CLI,
Roo Code, Swival, and Windsurf.

```bash
uvx skillscheck ./skills          # lint a skills directory
uvx skillscheck ./skills --strict # warnings count as errors (CI)
uvx skillscheck ./skills --format json
```

Exit codes: 0 = no errors, 1 = errors (or warnings with `--strict`).
Useful flags: `--fix` (safe mechanical fixes: lowercase names, collapse
consecutive hyphens, rename dirs to match `name`), `--agents`, `--check`.

**skills-ref** (<https://github.com/agentskills/agentskills/tree/main/skills-ref>) —
the official reference library. Checks that `SKILL.md` frontmatter is valid
and follows all naming conventions:

```bash
skills-ref validate ./my-skill
```

---

# Using scripts in skills

## One-off commands

When an existing package does what you need, reference it directly instead
of bundling a script. Pin versions for reproducibility and state
prerequisites in `SKILL.md` (or use the `compatibility` field).

- `uvx ruff@0.8.0 check .` — Python packages, requires uv
- `pipx run 'black==24.10.0' .` — Python packages, via OS package managers
- `npx eslint@9 --fix .` — npm packages, ships with Node.js
- `bunx eslint@9 --fix .` — Bun environments
- `deno run npm:create-vite@6 my-app` — Deno (permission flags required)
- `go run golang.org/x/tools/cmd/goimports@v0.28.0 .` — Go, built in

Move complex commands into bundled scripts — a tested script is more
reliable than a command that's hard to get right on the first try.

## Referencing scripts from `SKILL.md`

List available scripts so the agent knows they exist, then instruct the
agent to run them. Paths in code blocks are relative to the skill directory
root (the agent runs commands from there):

```markdown
## Available scripts

- **`scripts/validate.sh`** — Validates configuration files

## Workflow

1. Run the validation script:
   bash scripts/validate.sh "$INPUT_FILE"
```

## Self-contained scripts

Declare dependencies inline so the script runs with a single command:

- **Python (PEP 723)**: TOML block in `# ///` markers; run with
  `uv run scripts/extract.py`. Pin with PEP 508 specifiers
  (`"beautifulsoup4>=4.12,<5"`), constrain with `requires-python`.
- **Deno**: `npm:`/`jsr:` import specifiers; run with
  `deno run scripts/extract.ts`.
- **Bun**: version in the import path (`from "cheerio@1.0.0"`); run with
  `bun run scripts/extract.ts`. Auto-install disabled if a `node_modules`
  exists up the tree.
- **Ruby**: `bundler/inline` with a `gemfile do` block; pin versions
  explicitly.

## Designing scripts for agentic use

Agents read stdout/stderr to decide next steps. Design accordingly:

- **No interactive prompts** (hard requirement) — agents cannot answer TTY
  prompts. Accept all input via flags, env vars, or stdin. Fail with a clear
  usage message when required args are missing.
- **Document with `--help`** — brief description, flags, usage examples.
  This is the primary way an agent learns the interface. Keep it concise.
- **Helpful errors** — say what went wrong, what was expected, what to try:
  `Error: --format must be one of: json, csv, table. Received: "xml"`.
- **Structured output** — JSON/CSV/TSV over free-form text; composable with
  `jq`/`cut`/`awk`. Data to stdout, diagnostics to stderr.
- **Idempotency** — agents may retry. "Create if not exists" beats "create
  and fail on duplicate."
- **Reject ambiguous input** — clear errors over guessing; use enums/closed
  sets.
- **Dry-run support** — `--dry-run` for destructive or stateful operations.
- **Meaningful exit codes** — distinct codes per failure type, documented in
  `--help`.
- **Safe defaults** — destructive ops may need `--confirm`/`--force`.
- **Predictable output size** — harnesses truncate large output. Default to
  summaries; support `--offset` pagination or require `--output` for large
  results.

---

# Best practices for skill creators

## Start from real expertise

Don't generate skills from general training knowledge alone — the result is
vague ("handle errors appropriately"). Ground skills in real expertise:

- **Extract from a hands-on task**: complete a real task with an agent, then
  extract the reusable pattern. Capture steps that worked, corrections you
  made, input/output formats, and context the agent didn't know.
- **Synthesize from project artifacts**: internal docs, runbooks, style
  guides, API specs, code review comments, git history, real failure cases.

## Refine with real execution

Run the skill against real tasks and feed results (not just failures) back
into revision. Read execution traces, not just final outputs — wasted steps
usually mean instructions are too vague, inapplicable, or offer too many
options without a default.

## Spending context wisely

- **Add what the agent lacks, omit what it knows.** Ask of each piece:
  "Would the agent get this wrong without this instruction?" If no, cut it.
  If the agent handles the whole task well without the skill, the skill may
  not add value.
- **Design coherent units** — like scoping a function: encapsulate one
  coherent unit of work that composes with other skills.
- **Aim for moderate detail** — concise stepwise guidance with a working
  example outperforms exhaustive documentation.
- **Structure large skills with progressive disclosure** — core instructions
  in `SKILL.md`; detail in `references/` with explicit load triggers.

## Calibrating control

- **Match specificity to fragility** — freedom (with the *why*) where
  approaches vary; exact prescribed sequences where operations are fragile.
  Most skills mix both; calibrate each part independently.
- **Provide defaults, not menus** — one default, alternatives as brief
  escape hatches.
- **Favor procedures over declarations** — reusable methods over one-off
  answers.

## Patterns for effective instructions

- **Gotchas sections** — concrete, environment-specific facts that defy
  reasonable assumptions (soft-delete columns, mismatched ID names across
  services, misleading health endpoints). Keep in `SKILL.md`. When you
  correct an agent mistake, add it to gotchas.
- **Templates for output format** — concrete structures beat prose
  descriptions. Short ones inline; long ones in `assets/`.
- **Checklists for multi-step workflows** — explicit `- [ ]` steps when
  steps have dependencies or validation gates.
- **Validation loops** — do work → run validator → fix → repeat until pass.
  A reference document can serve as the validator.
- **Plan-validate-execute** — for batch/destructive operations: produce a
  structured plan, validate it against a source of truth with a script, then
  execute. Error messages should let the agent self-correct.
- **Bundle reusable scripts** — if the agent reinvents the same logic across
  runs, write a tested script once and bundle it in `scripts/`.

---

# Optimizing skill descriptions

Agents typically consult skills only for tasks needing knowledge beyond
their own — specialized APIs, domain workflows, uncommon formats. The
description carries the entire triggering burden.

Principles:

- **Imperative phrasing** — "Use this skill when...".
- **User intent over implementation.**
- **Err pushy** — include contexts where the user doesn't name the domain.
- **Keep concise** — a few sentences to a short paragraph; hard limit 1024
  chars.

## Trigger evals

Build ~20 eval queries in `eval_queries.json`
(`{"query": ..., "should_trigger": true|false}`): 8–10 should-trigger,
8–10 should-not. Vary phrasing (formal/casual/typos), explicitness (naming
the domain vs. describing the need), detail, and complexity. The best
should-trigger queries are ones where the connection isn't obvious. The best
negative queries are near-misses sharing keywords but needing something
different. Include realistic context: file paths, personal backstory,
specific values.

Run each query 3+ times (nondeterminism) and compute trigger rates.
Should-trigger passes above ~0.5; should-not-trigger passes below.

Split queries into train (~60%) and validation (~40%) sets to avoid
overfitting. Optimize against train only; select the best iteration by
validation pass rate. When revising: broaden scope for missed triggers, add
specificity/negative boundaries for false triggers, and avoid adding literal
keywords from failed queries (that's overfitting). ~5 iterations is usually
enough.

---

# Evaluating skill output quality

## Test cases

Store in `evals/evals.json` inside the skill directory. Each case: `id`,
`prompt` (realistic user message), `expected_output` (human-readable success
criteria), optional `files`. Start with 2–3 cases; vary phrasing and
formality; cover at least one edge case; use realistic context.

## Running evals

Run each case twice — **with the skill** and **without it** (baseline) — in
clean contexts (subagents or fresh sessions). Organize results in a
workspace: `iteration-N/eval-<name>/{with_skill,without_skill}/outputs/`.
Record `timing.json` (tokens, duration) per run. When improving an existing
skill, snapshot the old version and use it as the baseline.

## Assertions and grading

Add assertions after seeing first outputs. Good assertions are verifiable,
specific, countable ("The output file is valid JSON", "at least 3
recommendations"). Avoid vague ("output is good") or brittle (exact phrase)
checks. Grade each PASS/FAIL with concrete evidence quoted from the output —
no benefit of the doubt. Use scripts for mechanical checks, LLM judgment for
the rest. For comparing versions, blind comparison (judge doesn't know which
output came from which version) complements assertion grading.

## Aggregating and iterating

Compute `benchmark.json` per iteration: pass rate, time, tokens per
configuration, plus deltas. The delta tells you what the skill costs and
buys. Then:

- Drop assertions that always pass in both configurations (no signal).
- Fix assertions that always fail in both (broken test, wrong check).
- Study assertions that pass with skill but fail without (the skill's value).
- Tighten instructions when results are inconsistent across runs.
- Check time/token outliers by reading execution transcripts.

Review outputs with a human and record specific, actionable feedback per
test case. Iterate: give failed assertions + feedback + transcripts +
current `SKILL.md` to an LLM and ask for improvements. Generalize from
feedback (no narrow patches), keep the skill lean (removing instructions
often helps), explain the *why* in instructions, and bundle repeated work
into scripts. Repeat until satisfied or improvements plateau.
