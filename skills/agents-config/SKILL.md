---
name: agents-config
description: "This skill documents the `agents-config` repository layout."
---
# agents-config repository guide

This skill documents the `agents-config` repository layout.

## Directory roles

- `.agents/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cross-client, [Agent Skills](https://agentskills.io/) compatible directory. Use it for skills, agents, commands, or rules that should be visible to any client following the `.agents/` convention.
- `.claude/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Claude Code native configuration.
- `.opencode/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â opencode native configuration.

Both `.claude/` and `.opencode/` read the root `AGENTS.md` for shared conventions.

## Adding a component

| Component     | opencode path                    | Claude Code path               | Agent Skills path                |
| ------------- | -------------------------------- | ------------------------------ | -------------------------------- |
| Subagent      | `.opencode/agent/<n>.md`         | `.claude/agents/<n>.md`        | `.agents/agents/<n>.md`          |
| Skill         | `.opencode/skill/<n>/SKILL.md`   | `.claude/skills/<n>/SKILL.md`  | `.agents/skills/<n>/SKILL.md`    |
| Slash command | `.opencode/command/<n>.md`       | `.claude/commands/<n>.md`      | `.agents/commands/<n>.md`        |
| Always-on rule| add to `opencode.json` instructions| add to `.claude/rules/`        | add to `.agents/rules/`          |

## Restart after config changes

`opencode.json`, agent files, skills, plugins, and commands are loaded once at startup. Restart opencode after editing them.
