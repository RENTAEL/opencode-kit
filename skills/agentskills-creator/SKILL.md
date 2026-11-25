---
name: agentskills-creator
description: "Create a new Agent Skill: a folder containing a `SKILL.md` file (metadata + instructions), optionally with `scripts/`, `references/`, and `assets/` directories. Agents load skills through progressive disclosure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `name` and `description` at startup, the full `..."
---
# Agent Skills Creator

Create a new Agent Skill: a folder containing a `SKILL.md` file (metadata +
instructions), optionally with `scripts/`, `references/`, and `assets/`
directories. Agents load skills through progressive disclosure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `name` and
`description` at startup, the full `SKILL.md` body on activation, bundled
files on demand ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â so keep the main file lean and push detail into referenced
files.

## Workflow

- [ ] Step 1: Gather inputs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skill **name** and **purpose**.
- [ ] Step 2: Validate the name (rules below).
- [ ] Step 3: Determine the target directory.
- [ ] Step 4: Draft the `description` and confirm it with the user.
- [ ] Step 5: Scaffold the directory and `SKILL.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â propose author
      metadata from existing skills and confirm with the user (they may
      provide their own name), version `"1.0.0"`.
- [ ] Step 6: Write the body content.
- [ ] Step 7: Verify ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â lint with skillscheck and validate with skills-ref
      when available, then run the manual checklist.

### Step 1: Gather inputs

You need two inputs before creating anything:

1. **Name** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the skill's identifier and directory name.
2. **Purpose** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what task or workflow the skill teaches, and when it
   should trigger.

If either is missing, **ask the user** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent a purpose. You may
propose a name derived from the purpose, but confirm it before proceeding.

### Step 2: Validate the name

The `name` field must follow these rules (from the specification):

- 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“64 characters
- Lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`) only
- Must not start or end with a hyphen
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name

Valid: `pdf-processing`, `data-analysis`, `code-review`
Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen),
`pdf--processing` (consecutive hyphens)

If the user's proposed name is invalid, say why and suggest a fixed version.

### Step 3: Determine the target directory

If the user has not said where to create the skill, ask. Common locations:

- **This plugin**: `skills/<name>/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ships with the git-plugin.
- **Global**: `~/.agents/skills/<name>/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â available across projects.

The directory name must equal the `name` field.

### Step 4: Draft the description

The `description` carries the entire burden of triggering ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â agents match
user requests against it alone. Rules (1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1024 characters):

- **Imperative phrasing** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Use when..." not "This skill does...".
- **What + when** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â describe what the skill does AND when to use it.
- **User intent, not mechanics** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â match what the user asks for, not the
  skill's internals.
- **Err pushy** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â list contexts where it applies, including cases where the
  user doesn't name the domain directly.
- **Add a negative boundary** when a nearby capability exists ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â state what
  the skill does NOT cover.

Poor: `Helps with PDFs.`
Good: `Extracts text and tables from PDF files, fills PDF forms, and merges
multiple PDFs. Use when working with PDF documents or when the user mentions
PDFs, forms, or document extraction.`

Show the drafted description to the user for confirmation before writing.

### Step 5: Scaffold

Create the directory and `SKILL.md`. Add `scripts/`, `references/`, or
`assets/` only when the purpose calls for them ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not create empty
directories:

- `scripts/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â executable code the agent runs (must be non-interactive,
  accept input via flags/args/stdin, document usage with `--help`, print
  structured output to stdout and diagnostics to stderr, pin versions).
- `references/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â documentation loaded on demand (keep files focused).
- `assets/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â templates, images, data files.

Write frontmatter with `name` and `description` (required). Add
`allowed-tools` when the skill needs pre-approved tools, and
`compatibility` only for real environment requirements.

**Metadata** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â resolve the author before writing:

1. Search the target project for existing skills (e.g. `skills/*/SKILL.md`,
   `~/.agents/skills/*/SKILL.md`) and read their `metadata.author`.
2. **Always ask the user to confirm the author** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â even when one is found.
   If an existing skill provides an author, propose it as the default and
   offer the user the option to provide their own name instead. If no
   author is found, ask the user to provide one. Never invent an author.
3. Always set `metadata.version` to `"1.0.0"` for a new skill.

### Step 6: Write the body

The body is loaded in full on activation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every token competes for the
agent's attention. Guidelines:

- **Add what the agent lacks, omit what it knows.** Focus on project
  conventions, domain procedures, non-obvious edge cases. Don't explain
  what a PDF is or how HTTP works. Ask of each line: "Would the agent get
  this wrong without it?" If no, cut it.
- **Procedures over declarations** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â teach how to approach a class of
  problems, not the answer to one instance.
- **Defaults, not menus** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pick one default tool/approach; mention
  alternatives briefly as escape hatches.
- **Match specificity to fragility** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â give freedom where approaches vary
  (explain the *why*); be prescriptive where a sequence must be followed
  exactly.
- **Gotchas section** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â concrete, environment-specific corrections to
  mistakes the agent would otherwise make. Keep these in `SKILL.md`, not in
  a reference file.
- **Checklists** for multi-step workflows with dependencies; **validation
  loops** (do work ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run validator ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ repeat) for fragile output;
  **templates** for required output formats.
- **Keep `SKILL.md` under 500 lines.** Move detail to `references/` and
  tell the agent exactly when to load each file ("Read
  `references/api-errors.md` if the API returns a non-200 status" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not
  "see references/ for details").

Reference bundled files with relative paths from the skill root, one level
deep (e.g. `references/REFERENCE.md`, `scripts/extract.py`).

### Step 7: Verify

**Validate with skillscheck if available.** skillscheck
(<https://github.com/swival/skillscheck>) validates the skill against the
agentskills.io specification plus quality, progressive-disclosure, and
agent-compatibility checks:

```bash
uvx skillscheck <path-to-skills-dir>
```

- If `uvx` is installed, run it pointed at the directory containing the new
  skill (e.g. `uvx skillscheck skills` when creating `skills/<name>/`).
  Otherwise, if a `skillscheck` binary is on `PATH`, run that instead.
- Exit code 0 means no errors. Fix every reported error and re-run until
  clean; address warnings where they apply to the new skill, and fix
  user-centric description phrasing (`[2a.description.user-centric]`) by
  using agent-directed "Use when <verb>ing..." form.
- If neither `uvx` nor `skillscheck` is available, note that the lint was
  skipped and fall back to the manual checklist below.

**Validate with skills-ref if available.** As a second automated check, run
the official reference linter when it is installed:

```bash
skills-ref validate ./<name>
```

It verifies that the frontmatter is valid and follows all naming
conventions. If `skills-ref` is not available, skip it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the manual
checklist below covers the same rules.

**Manual checklist** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â after writing, re-read the created `SKILL.md` and
check (run regardless when skillscheck is unavailable, or to confirm what
skillscheck already covers):

- [ ] `name` matches the directory name and follows all naming rules
- [ ] `description` is present, ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1024 characters, states what + when
- [ ] Frontmatter is valid YAML with only spec-defined fields
- [ ] Body is under 500 lines; detail lives in `references/` with explicit
      load triggers
- [ ] Referenced file paths are relative and exist
- [ ] `metadata.author` was confirmed by the user (found author proposed as
      default, own name accepted) and `metadata.version` is `"1.0.0"`

Report the created paths and the skillscheck result to the user.

## Reference

For the complete field-by-field specification, script design rules, and
eval-driven iteration guidance, read
[references/specification.md](references/specification.md). Load it when you
need exact frontmatter constraints, validation details, or when the user
asks about testing/evaluating skills.
