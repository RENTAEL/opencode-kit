---
name: skill-name
description: "One-paragraph overview: what this skill achieves and the core approach (e.g. \"the bundled script collects X as JSON; the agent writes the narrative\")."
---
# Skill Name

One-paragraph overview: what this skill achieves and the core approach
(e.g. "the bundled script collects X as JSON; the agent writes the narrative").

## How to run (script-backed skills)

`SCRIPT` = this skill's `scripts/Your-Script.ps1`. Document the exact invocation,
a table of the parameters that matter, and 2-3 copy-paste examples.

## Output contract

What the script prints (JSON shape, exit codes), and what goes to a file vs stdout.

## What you (the agent) do with the result

1. Numbered, imperative steps.
2. Lead with what matters; don't recite everything.
3. Fail loud: name every coverage gap, skipped section, or unverified assumption.

## Gotchas

REQUIRED (validator-enforced; may live here or in REFERENCE.md). The *real*,
mechanism-level pitfalls of this domain ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the traps that produce confident-but-wrong
conclusions. For each: **the trap ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ why it happens ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the correct check/fix.** Cover
measurement traps (a tool/command that reports a misleading value), errors that point
at the wrong cause, environment foot-guns, and known misattributions. Keep it honest and
specific ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a few verifiable gotchas beat a padded list. Add to it when a real run uncovers
a new pitfall. **Committed gotchas must be generic ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no company-specific data.**

**Environment-specific gotchas (local).** At the start of a run, read `gotchas.local.md`
in this skill's folder if it exists ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it holds traps learned in *this* environment (real
server/DB names, local quirks). When you discover a new environment-specific pitfall,
**append it there**, not to this file. `gotchas.local.md` is gitignored and is preserved
across skill updates, so the skill gets more useful every time it's used here.

## Verification

REQUIRED (validator-enforced; may live here or in REFERENCE.md). Document two things:
1. **Before changes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â how to verify correctness/preconditions first: a baseline, a repro,
   a health-check, or (for read-only skills) how to confirm ground truth and coverage before
   recommending anything. Never propose a change without a before-check.
2. **Output** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â how to verify the result afterward: re-run the check, confirm the expected
   effect landed, and **fail loud** if it can't be confirmed. Never report "done" unverified.

## Errors

Known failure modes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ what to tell the user.

<!--
Checklist before opening a PR (see CONTRIBUTING.md):
- [ ] Has a "## Gotchas" section (here or in REFERENCE.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â validator-enforced
- [ ] Has a "## Verification" section (before-change check + output check) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â validator-enforced
- [ ] Tells the agent to read/append gotchas.local.md for env-specific learnings
- [ ] Lives in a category folder: skills/<category>/<name>/ ; new category -> add it to .claude-plugin/plugin.json
- [ ] Skill's own folder name == frontmatter name (lowercase, hyphens), globally unique
- [ ] description ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1024 chars, includes when-to-use triggers
- [ ] metadata.version set; bump it on EVERY behavior change
- [ ] SKILL.md < 500 lines; details go in REFERENCE.md (linked one level deep)
- [ ] Scripts have tests next to them (*.Tests.ps1 / test_*.py)
- [ ] skill.install.json if the skill needs runtimes/credentials
- [ ] evals/<skill-name>.json with 3+ scenarios
- [ ] No company-specific data (AGENTS.md contract) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â placeholders only
- [ ] `npm run validate` passes
-->
