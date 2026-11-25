---
name: hive-methodology
description: "/swarm-hub hive` asks before executing (passing `--plan` skips it):"
---
# Agent Hive Methodology

## Gatekeeping Question

`/swarm-hub hive` asks before executing (passing `--plan` skips it):

> **Question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which plan to execute?** Select an approved plan (`.opencode/state/ideation/*.md`), or type a topic (run `/swarm-hub hive-plan` first), or type a path.

Resolved answer maps to `--plan=<file>`.

> **Stop vibing. Start hiving.** Plan first. Execute with trust. Context persists.

Inspired by [hung319/agent-hive](https://github.com/hung319/agent-hive)'s PHILOSOPHY.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a multi-agent orchestration framework grounded in bee colony efficiency.

## The 7 Core Principles

### P1: Context Persists
Calibration survives between sessions. Store grounded, project-specific knowledge that shapes agent behavior.

**Store:**
- "We use Zustand, not Redux"
- "Auth is in /lib/auth, don't create new auth code"
- "We tried X, it was overkill for our scale"

**Don't store:** General knowledge the agent already has.

### P2: Plan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Approve ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Execute
Two phases with a clear approval gate between them.

| Phase | Mode | Human Role |
|-------|------|------------|
| **Planning** | Dialogue | Shape, question, refine |
| **Execution** | Trust | Agent runs, human monitors |

Planning is collaborative. Execution is autonomous. The approval gate is where trust is earned.

### P3: Human Shapes, Agent Builds
- **Human owns:** The shape (what), the why (problem), the taste (what feels right)
- **Agent owns:** The details (how), the how (patterns/libraries), the execution (just do it)

Destination known. Path explored.

### P4: Good Enough Wins
Capture what's good enough FOR THIS CONTEXT. Reject over-engineering.

Valuable context examples:
- "We tried X, it was overkill for our 3-person team"
- "Don't suggest Z, we explicitly rejected it"

### P5: Batched Parallelism
Parallel tasks grouped into sequential batches. Context flows between batches.

```
Batch 1 (parallel):     Batch 2 (parallel):
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Task A              ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Task D (uses A+B+C)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Task B              ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Task E (uses A+B+C)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Task C
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
   Glue task synthesizes results
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
   Context flows to Batch 2
```

### P6: Tests Define Done
Best-effort worker verification + orchestrator batch testing.

- **Workers:** Write code, do best-effort checks (ast-grep, lint). ~80% confidence is enough to ship.
- **Orchestrator:** After batch merge, run full build + test suite. Diagnose failures, fix or re-dispatch.

### P7: Iron Laws + Hard Gates
Enforce with tools and instructions, not soft suggestions.

**Iron Laws:**
- Never plan without asking questions first
- Never complete without attempting verification
- Never assume when uncertain ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ASK
- Always one question at a time (discovery)
- Always best-effort verification before commit
- Always stop and ask when blocked

## Bee Colony Agent Roles

| Agent | Role | Description |
|-------|------|-------------|
| **Architect Bee** | Planner | Interviews, discovers requirements, writes plan.md. NEVER executes. |
| **Swarm Bee** | Orchestrator | Coordinates execution, delegates to workers, merges results. |
| **Forager Bee** | Executor | Executes tasks in isolated contexts. Does the actual coding. |
| **Scout Bee** | Researcher | Researches codebase and external docs in parallel. |
| **Hygienic Bee** | Reviewer | Reviews plan quality. Returns OKAY/REJECT verdict. |

## Workflow

### Ideation Phase (Architect Bee)

1. **Active Discovery**: Ask clarifying questions. Challenge assumptions. Don't accept vague requirements.
2. **Gather Context**: Research codebase, existing patterns, external docs. Produce royal jelly (context).
3. **Design the Comb**: Break into tasks with dependencies. Task types: greenfield, testing, modification, bugfix, refactoring.
4. **Write plan.md**: Each task has: objective, context, approach, files affected, acceptance criteria.
5. **Approval Gate**: Present to human. Wait for explicit approval before any execution.

### Orchestration Phase (Swarm Bee)

1. **Load Plan**: Read the approved plan.md.
2. **Execute Batches**: Group independent tasks into parallel batches. Sequential batches share context flow.
3. **Monitor Workers**: Forager Bees execute each task. If blocked, worker reports: status, reason, options, recommendation.
4. **Blocked Worker Protocol**: Pause ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask human via structured question ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ resume with decision context. NEVER guess.
5. **Merge Batches**: After each batch, merge completed work. Run full tests.
6. **Synthesize**: Glue tasks merge findings between batches. Context flows forward.

## Usage Examples

### Planning with Hive
```
/swarm-hub hive-plan add user authentication
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Architect Bee interviews you
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Gathers context (existing auth code, patterns)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Produces plan.md with task breakdown
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ You approve ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ready for /swarm-hub hive
```

### Execution with Hive
```
/swarm-hub hive user authentication
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Swarm Bee loads approved plan
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Batch 1: AuthService + Token refresh (parallel)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Batch 2: API routes + Tests (after Batch 1)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Each Forager in isolated worktree
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Blocked? Worker reports, you decide
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Final merge + tests ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ done
```

### Combined Flow
```
/hive add dark mode support
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /swarm-hub hive-plan plan (interviews, produces plan.md)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /swarm-hub hive execute (batched parallel execution)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Context persists for next session
```

## Integration with Hubs

| Hub | Subcommand | Hive Phase |
|-----|-----------|------------|
| `/swarm-hub hive-plan` | Plan | Architect Bee ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â interview ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ context ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plan.md ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ approval gate |
| `/swarm-hub hive` | Execute | Swarm Bee ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â batched parallelism ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ blocked protocol ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ batch test ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ merge |

## When to Use

- **Multi-file features** that need coordinated parallel work
- **Complex tasks** where planning prevents wasted effort
- **Team projects** where context must survive sessions
- **Any task** where you want assurance before execution begins

## When Not to Use

- **Single-file fixes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just use direct execution
- **Urgent hotfixes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â planning overhead isn't worth it
- **Exploratory/toy projects** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â vibe coding is fine
