---
name: agentskills-doctor
description: "Validate an existing Agent Skill against the agentskills.io specification and best practices, report every finding with its check ID, and ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when the user asks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix the findings and re-verify. Read-only by default: never modify a skill unless ..."
---
# Agent Skills Doctor

Validate an existing Agent Skill against the agentskills.io specification
and best practices, report every finding with its check ID, and ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when the
user asks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix the findings and re-verify. Read-only by default: never
modify a skill unless the user explicitly asks for fixes.

## Workflow

- [ ] Step 1: Gather input ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the path to the skill to validate.
- [ ] Step 2: Detect ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run skillscheck and skills-ref when available, then
      the manual checklist.
- [ ] Step 3: Report ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â present findings grouped by severity with suggested
      fixes.
- [ ] Step 4: Fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only when the user asks; auto-apply safe fixes, confirm
      judgment fixes.
- [ ] Step 5: Re-verify ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-run the linters and confirm findings are gone.

### Step 1: Gather input

You need one input: the **path to a skill directory** (or a `SKILL.md`
file). If the user has not provided one, ask. Do not guess which skill to
validate when several exist.

### Step 2: Detect

Run every check that is available, collecting findings with their check IDs:

1. **skillscheck** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â primary linter. If `uvx` is installed, run
   `uvx skillscheck <skills-parent-dir>` (e.g. `uvx skillscheck skills` for
   `skills/<name>/`); otherwise run a `skillscheck` binary on `PATH`. Use
   `--format json` when you need to parse output programmatically. Exit code
   0 = no errors, 1 = errors. If neither is available, note the skip.
2. **skills-ref** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â second automated check. If installed, run
   `skills-ref validate ./<name>` to verify frontmatter validity and naming
   conventions. Skip silently when not installed.
3. **Manual checklist** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-read the target `SKILL.md` and check what the
   linters do not cover:
   - [ ] `name` matches the directory name and follows all naming rules
   - [ ] `description` is present, ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1024 characters, states what + when,
         and uses agent-directed phrasing ("Use when <verb>ing...", not
         "when the user asks/wants/mentions")
   - [ ] Frontmatter is valid YAML with only spec-defined fields
   - [ ] Body is under 500 lines; detail lives in `references/` with
         explicit load triggers
   - [ ] Referenced file paths are relative and exist

For exact field constraints, naming rules, and token budgets, read
[references/specification.md](references/specification.md).

### Step 3: Report

Present findings grouped by severity ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â errors, then warnings, then info.
For each finding give:

- The check ID (e.g. `[2a.description.user-centric]`) when one exists
- The file and line
- What the rule is
- A concrete suggested fix

End the report by telling the user you can fix the findings on request.
Do not fix anything yet.

### Step 4: Fix

Only when the user explicitly asks ("fix it", "fix all", "fix the
description finding"). Read [references/fix-rules.md](references/fix-rules.md)
for per-finding fix guidance, then apply fixes in two tiers:

- **Safe tier ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â auto-apply without per-item confirmation.** Mechanical
  fixes: lowercase a `name`, collapse consecutive hyphens, rename a
  directory to match `name`, convert user-centric description phrasing to
  agent-directed form, trim an over-length `description`. Prefer
  `uvx skillscheck --fix` for what it covers, then hand-fix the rest.
- **Judgment tier ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm before changing.** Rewrites and removals:
  rewriting a description, deleting orphaned files, moving content out of
  an over-long body into `references/`, changing metadata. Present the
  proposed change and get a "yes" per finding or a blanket "fix all".

Never touch files outside the target skill directory.

### Step 5: Re-verify

After fixing, re-run skillscheck (and skills-ref when available) on the
skill. Confirm every fixed finding is gone and no new findings appeared.
Report the final lint result and the list of applied changes to the user.

## Reference

- [references/specification.md](references/specification.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full
  agentskills.io field-by-field specification, script design rules, and
  eval guidance. Load when you need exact constraints.
- [references/fix-rules.md](references/fix-rules.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-finding fix
  guidance keyed by skillscheck check ID. Load when the user asks to fix
  findings.
