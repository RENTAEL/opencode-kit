---
name: parallel
description: "parallel"
---
# Code Forge ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Parallel

## ÃƒÂ¢Ã…Â¡Ã‚Â¡ Execution Entry Point

@../shared/execution-entrypoint.md

**For this skill:** start at **the first executable step**. If you catch yourself about to say "falling back to manual handling", STOP and go to the indicated step.

---

Dispatch independent sub-agents to solve multiple unrelated problems concurrently.

## When to Use

- 3+ test files failing with different root causes
- Multiple independent subsystems broken simultaneously
- Several unrelated bugs reported at once
- Any situation with 2+ problems that share no state

## When NOT to Use

- Failures are related (fix one, others may resolve)
- Problems share state or dependencies
- Need full system state to diagnose (single-threaded investigation needed)
- Only 1 problem exists

**For task execution within a feature:** Use `/code-forge:impl` which has built-in parallel task support.

## Core Principle

**One agent per independent problem domain. Let them work concurrently.**

## Workflow

### Step 1: Identify Problems

List all problems. For each, note:
- What is failing (test file, error message, component)
- Which files/modules are involved
- Whether it shares state with other problems

### Step 2: Assess Independence

Build a dependency matrix:

```
Problem A ÃƒÂ¢Ã¢â‚¬Â Ã‚ÂÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Problem B: independent? (yes/no, why)
Problem A ÃƒÂ¢Ã¢â‚¬Â Ã‚ÂÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Problem C: independent? (yes/no, why)
Problem B ÃƒÂ¢Ã¢â‚¬Â Ã‚ÂÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Problem C: independent? (yes/no, why)
```

Group dependent problems together. Each independent group gets its own agent.

### Step 3: Dispatch Agents

For each independent problem group, launch a `Agent(subagent_type="general-purpose")`:

**Agent prompt structure:**
```
You are investigating and fixing: {problem description}

## Scope
- Files involved: {list}
- Error messages: {paste}
- Expected behavior: {description}

## Constraints
- Only modify files in your scope
- Use code-forge:tdd methodology (write failing test first)
- Use code-forge:debug methodology (root cause before fix)

## Output Required
- Root cause (1-2 sentences)
- Files changed (list)
- Test results (pass/fail counts)
- Summary of fix (1-2 sentences)
```

**CRITICAL:** Launch all agents in a single message using multiple `Agent` tool calls. This enables true parallel execution.

### Step 4: Review and Integrate

After all agents complete:

1. **Check for conflicts** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â did any agents modify the same file?
   - No conflicts: proceed
   - Conflicts: resolve manually, prefer the more targeted change
2. **Run full test suite** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify all fixes work together
3. **Report results:**

```
Parallel dispatch complete: {N} agents, {M} problems resolved

Agent 1: {problem} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {root cause} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {status}
Agent 2: {problem} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {root cause} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {status}
Agent 3: {problem} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {root cause} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {status}

Full test suite: {pass}/{total} passing
```

## Example

```
3 test files failing: auth.test.ts, payment.test.ts, email.test.ts

Independence check:
  auth ÃƒÂ¢Ã¢â‚¬Â Ã‚ÂÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ payment: independent (different modules, no shared state)
  auth ÃƒÂ¢Ã¢â‚¬Â Ã‚ÂÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ email:   independent (different modules)
  payment ÃƒÂ¢Ã¢â‚¬Â Ã‚ÂÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ email: independent

Dispatch 3 agents in a single message:
  Agent 1: "Fix auth.test.ts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â files: src/auth/, error: missing token validation"
  Agent 2: "Fix payment.test.ts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â files: src/payment/, error: decimal precision"
  Agent 3: "Fix email.test.ts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â files: src/email/, error: template not found"

Results: 3/3 resolved, full suite 128/128 passing
```

## Common Mistakes

- Dispatching agents for related problems (they'll step on each other's changes)
- Not providing enough context in agent prompts (agent wastes time re-discovering)
- Launching agents sequentially instead of in a single parallel message
- Skipping the full test suite after integration
- Dispatching too many agents (>5) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â diminishing returns, harder to integrate
