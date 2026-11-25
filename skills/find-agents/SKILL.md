---
name: find-agents
description: "Find the right agent for a task by searching across **agent registries** and **GitHub** simultaneously."
---
# Find Agents

Find the right agent for a task by searching across **agent registries** and **GitHub** simultaneously.

## When to Use

- Setting up a project (`/hub-setup setup` or `/hub-setup refresh`)
- The user asks "find an agent for X" or "is there an agent that does X"
- You need to extend agent capabilities with specialized subagents
- You're about to build a new agent from scratch that a published one might already cover

## Multi-Source Search Strategy

| Registry | Search Method | Signal | Blind Spot |
|----------|--------------|--------|------------|
| **skills.sh** | `GET /api/search?q=` (filter agent category) | lifetime installs | smaller corpus |
| **GitHub topics** | `gh search repos --topic ai-agent --topic agent-framework --topic autonomous-agent` | repo stars, description | repo-level, not agent-level |
| **skills.sh API** | Fetch and rank by installs | cross-registry validation | newer registries have less data |

## How to Choose

**Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Read before you judge.** Never recommend from metadata alone. Get the actual agent definition.

**Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Weigh signals in this order:**
1. **Fit** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Does the agent's described behavior match the real need?
2. **Quality signals** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Installs/stars, maintenance recency, documentation quality
3. **Scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Is it focused or a grab-bag?
4. **Safety** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Check what tools/permissions it requests

**Step 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Deliver a verdict, not a menu:**
- One **primary recommendation** with why
- 1-2 **alternatives** framed by need
- If nothing fits, offer to scaffold a custom agent

## Installation

For skills.sh agents (project scope ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â installs to .opencode/ in the current project):
```bash
npx skills add <owner>/<repo> --skill <agent-name>
```

For GitHub agents, direct the user to the repo for setup instructions.

## Post-Install: Agent Integration (CRITICAL)

After installing an agent-related skill package, integrate it into the existing agent ecosystem:

1. **Update /resource-hub create agent spec** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â If the package provides agent definition patterns (like `opencode-agent-creator` or `custom-agent-definitions`), add it as a relatedSkill to `/resource-hub create agent` so the agent-creation workflow loads it automatically.

2. **Update agent-creator skill** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â If the package enhances agent creation, update the `opencode-agent-creator` skill's "Best Practices" or "References" section to mention the new package.

3. **Update /hub-setup provision spec** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â If the package relates to provisioning (agent wrappers, config generation), add it as a relatedSkill to `/hub-setup provision`.

4. **Update stack-recommender** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Add the package to the relevant mapping table (e.g. Agent/Tool Development section).

5. **Create or update agent definitions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â For packages that define complete agent workflows, create a corresponding subagent in `agents/` that loads the skill and exposes it via `@mention`.

## Integration with /init-project

This skill is used by `/hub-setup setup` and `/hub-setup refresh` to:
1. Search for agents relevant to the detected project stack and needs
2. Present findings for user selection
3. Install selected agent packages
4. **Post-install integration** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â wire packages into hub specs, skill references, and agent definitions

## Security & Privacy

- Issues read-only HTTP GETs to public APIs
- Requires no API keys or tokens
- Never auto-installs anything ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always user-confirmed
- Check agent permissions before installation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â agents run with configured permissions
