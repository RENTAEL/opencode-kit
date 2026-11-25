---
name: workflow-retrospective
description: "Review a work session and propose tooling improvements. The agent reflects on what went wrong, what workarounds it had to invent, what the user had to clarify, and what tooling changes would prevent those issues in the future. The goal is a self-healing process - the tooling i..."
---
# Retrospective Workflow

## Purpose

Review a work session and propose tooling improvements. The agent reflects on what went wrong, what workarounds it had to invent, what the user had to clarify, and what tooling changes would prevent those issues in the future. The goal is a self-healing process - the tooling improves over time through use.

Load it inside the session where the work happened, or in a fresh session started from a handoff. In the second case the conversation is not in context, and Step 1 works from durable data instead: the handoff's own account, the task directory (a workflow run's `workflows/<runId>/` files and journal, or the ledger and decision log of an arc kept in markdown, plus reports and review rounds), the run registry `~/.local/share/opencode/oc-async-runs.json` and its run logs, the Claude transcripts under `~/.claude/projects/`, and the host power log (`pmset -g log`). Test the handoff's account against that data; where they disagree the data wins, and the corrections are listed first. When the research is fanned out to agents, give each its own scratch subdirectory and its own output file: in one retrospective two agents shared a scratch directory and one overwrote the other's helper script.

The tooling lives in `<cookbook checkout>`: skills (`src/skills/`), commands (`src/commands/`), tools (`src/modules/`), and configuration (`AGENTS.md`, `opencode.json`, which also defines the agents). Project-local commands live in each project's `.claude/commands/` and are not in this repository.

### How tooling reaches the runtimes

Sources are copied, not linked. `pnpm run symlink` builds and runs both installers: `scripts/link-opencode.sh` (skills, commands, `AGENTS.md` and `opencode.json` into `~/.config/opencode/`) and `scripts/link-claude-code.sh` (skills, commands, `AGENTS.md` as `~/.claude/CLAUDE.md`, and the tools' MCP server registration). `pnpm run symlink:opencode` and `pnpm run symlink:claude-code` run one each. Edits to the installed copies are lost on the next run; edit the sources here.

## Constraints

- Do not make changes without user approval - this workflow produces a proposal, not automatic edits.
- Load relevant skills proactively to understand how the tooling is structured (especially `write-skill` and `develop-opencode-plugins`). Use `codebase_*` tools for broad investigation and read selectively to keep the context window healthy.

## Evolving Artifacts

Some commands and skills are explicitly designed to improve through use. During every retrospective, check these files for updates:

| File                                  | What to look for                                                                                                                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/commands/adversarial-consult.md` | New patterns from adversarial sessions - prompt structures that worked well, model-specific quirks discovered, consultation patterns that failed or succeeded, updates to the "Lessons from Practice" section |

If the session used `/adversarial-consult`, review the adversarial exchanges and extract:

- Prompt phrasings that got high-quality responses (add to Lessons from Practice)
- Prompt phrasings that got generic/unhelpful responses (note as anti-patterns)
- Model-specific behaviors worth documenting (e.g., "Gemini consistently over-abstracts on data structure questions")
- New consultation patterns that emerged organically (add as new Pattern types)
- Whether the adversary model selection rationale still holds or needs updating

## Step 1 - Reflect on the Session

Review the conversation history, or in a handoff retrospective the durable data listed under Purpose, and identify:

### Tooling friction

- **Skills/commands that were missing or incomplete** - Did you need information that wasn't in any loaded skill? Was a command workflow missing a step?
- **Skills/commands that were wrong or misleading** - Did a skill describe a pattern that didn't match reality? Did a command lead you down the wrong path?
- **Tool bugs or limitations** - Did any MCP tool behave unexpectedly? Did you have to work around a tool limitation?
- **Workarounds you had to invent** - Did you do something manually that should have been documented or automated?

### User clarifications

- **Questions the user had to answer that the tooling should have known** - Did the user correct an assumption? Did they clarify a convention that should be in a skill?
- **Decisions the user made that should become defaults** - Did the user pick an option that should be the standard going forward?
- **Corrections the user applied** - Did the user override your approach? What should change so next time the approach is correct from the start?

### What went well

- **Tooling that worked smoothly** - Which skills/commands/tools performed well? (Briefly acknowledge, don't over-elaborate.)

## Step 2 - Investigate the Tooling

Before proposing changes, read the relevant source files in the tooling repository to understand the current state. Don't propose changes based on assumptions - verify what actually exists.

Use `codebase_project_structure` on `<cookbook checkout>` to orient yourself.

For each issue identified in Step 1:

1. Read the relevant skill/command/agent/prompt file to understand what it currently says.
2. Check if the issue is already partially addressed somewhere else (maybe a different skill covers it).
3. Determine the minimal change that would fix the issue.

This investigation step is critical - many proposed changes turn out to be unnecessary once you read the current tooling. Answer your own questions before asking the user.

## Step 3 - Propose Changes

Present a numbered list of proposed changes to the user. For each item:

```
N. [FILE] path/to/file.md
   [ISSUE] What went wrong or what was missing (1 sentence)
   [CHANGE] What to add/modify/remove (concrete description)
   [REASON] Why this prevents the issue next time (1 sentence)
```

Group by category:

1. **Skill updates** - missing rules, wrong patterns, incomplete conventions
2. **Command updates** - missing steps, wrong workflow, missing clarifications
3. **Agent updates** - missing capabilities, wrong tool access
4. **New skills/commands** - entirely new tooling that should exist
5. **Tool/module issues** - bugs or limitations in MCP tools (these may require code changes, not just markdown)

Order by impact - most impactful improvements first.

If there are no meaningful issues to report, say so. Do not manufacture improvements to justify the retrospective.

## Step 4 - Await Approval

Present the full list and ask the user which items to implement. The user may:

- Approve all
- Approve specific items by number
- Reject items with reasoning (which itself is a learning - note it)
- Modify items before approval

Do not implement any changes until the user confirms.

## Step 5 - Implement Approved Changes

For each approved item:

1. Read the target file.
2. Make the change.
3. Mark the item as done.

Follow the `write-skill` skill conventions when modifying skills. Follow existing patterns when modifying commands.

Commit changes with a descriptive message:

```bash
git add <files>
git commit -m "fix: retrospective - <concise summary of changes>"
```

## Step 6 - Report

Summarize what was changed:

- Number of items proposed vs approved vs implemented
- Files modified
- Key improvements made
- Items rejected (with user's reasoning, for future reference)
