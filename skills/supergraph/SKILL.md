---
name: supergraph
description: "Graph evidence uses `codebase-memory-mcp` scoped by `CBM_PROJECT`. Orientation loads `get_architecture` aspects `overview`, `layers`, `boundaries`, `clusters`, and `hotspots`, plus validated `hubs`, `bridges`, and `test-gaps` recipes. If optional graph evidence is unavailable,..."
---
# supergraph

Graph evidence uses `codebase-memory-mcp` scoped by `CBM_PROJECT`. Orientation
loads `get_architecture` aspects `overview`, `layers`, `boundaries`, `clusters`,
and `hotspots`, plus validated `hubs`, `bridges`, and `test-gaps` recipes. If
optional graph evidence is unavailable, label it unavailable and use Serena or
filesystem evidence.

Dispatch to the right skill. 1% rule: if it *might* apply, invoke it.

## Priority

1. User CLAUDE.md / AGENTS.md (highest)
2. This skill set
3. Default system behavior

## Dispatch Table

| User intent | Skill to invoke |
|-------------|----------------|
| "start", "begin", unclear scope | `/supergraph:analyze` |
| "plan", "lÃƒÆ’Ã‚Âªn kÃƒÂ¡Ã‚ÂºÃ‚Â¿ hoÃƒÂ¡Ã‚ÂºÃ‚Â¡ch", explicit plan request | `/supergraph:plan` |
| "implement", "build", "execute" (plan saved) | `/supergraph:execute` |
| "fix bug", "debug", "why failing" | `/supergraph:fix` |
| "test", "TDD", "add tests" | `/supergraph:tdd` |
| "refactor", "clean up", "reorganize" | `/supergraph:plan` (then execute) |
| integration/e2e tests, after unit green | `/supergraph:integration` |
| "video demo", "demo video", "walkthrough", "quay video demo" | `/supergraph:video-demo` |
| "done?", "verify", before commit/PR | `/supergraph:verify` |
| "review", "merge", "PR", before merge | `/supergraph:review` |
| Need project context | `/supergraph:scan` |

## Adaptive Gate

- **< 20 lines, ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤2 files, no hub/bridge, complexity <10** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use `/supergraph:tdd` directly
- **ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤5 files, clear requirement, no cross-boundary** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/supergraph:plan` with lightweight tasks
- **>5 files, ambiguous, hub/bridge, cross-boundary** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/supergraph:analyze` first, then plan

## User Instructions

"Add X" or "Fix Y" is the WHAT. Skills determine HOW. Never skip a skill because the task "feels simple."

## Red Flags (STOP if you catch yourself):

- "I'll just do it quickly" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ pick a skill, follow it
- "I already know what to do" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skills evolve, load current one
- "This is too simple for a skill" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ simple becomes complex fast

## Integration

All skills depend on `/supergraph:scan` being loaded first in the session.

## Subagent Guard

When dispatching subagents (executor, code-reviewer, plan-writer, plan-reviewer, qa-tester, security-auditor, diagnostician):
- Subagents get self-contained prompts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never session history
- Subagents do NOT trigger skills independently ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is the orchestrator's job
- Subagents report results back; orchestrator decides next step (fix, verify, review)
