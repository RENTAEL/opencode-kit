---
name: hubs-reference
description: "Use this built-in reference when you need detailed OAS catalog information that does not need to live in every `AGENTS.md` session."
---
# OAS Reference

Use this built-in reference when you need detailed OAS catalog information that does not need to live in every `AGENTS.md` session.

## Agent Catalog

Prefix: `OpenCode Hubs:`. See `agents/*.md` for full prompts.

- `explore` (haiku) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fast codebase search and mapping
- `analyst` (opus) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â requirements clarity and hidden constraints
- `planner` (opus) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sequencing and execution plans
- `architect` (opus) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â system design, boundaries, and long-horizon tradeoffs
- `debugger` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â root-cause analysis and failure diagnosis
- `executor` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â implementation and refactoring
- `verifier` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â completion evidence and validation
- `tracer` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â trace gathering and evidence capture
- `security-reviewer` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â trust boundaries and vulnerabilities
- `code-reviewer` (opus) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â comprehensive code review
- `test-engineer` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â testing strategy and regression coverage
- `designer` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â UX and interaction design
- `writer` (haiku) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â documentation and concise content work
- `qa-tester` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â runtime/manual validation
- `scientist` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â data analysis and statistical reasoning
- `document-specialist` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SDK/API/framework documentation lookup
- `git-master` (sonnet) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â commit strategy and history hygiene
- `code-simplifier` (opus) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â behavior-preserving simplification
- `critic` (opus) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â plan/design challenge and review

## Model Routing

- `haiku` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â quick lookups, lightweight inspection, narrow docs work
- `sonnet` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â standard implementation, debugging, and review
- `opus` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â architecture, deep analysis, consensus planning, and high-risk review

## Tools Reference

### External AI / orchestration
- `/team N:executor "task"`
- `opencode team N:codex|gemini "..."`
- `opencode ask <opencode|codex|gemini>`
- `/ccg`

### OAS state
- `state_read`, `state_write`, `state_clear`, `state_list_active`, `state_get_status`

### Team runtime
- `TeamCreate`, `TeamDelete`, `SendMessage`, `TaskCreate`, `TaskList`, `TaskGet`, `TaskUpdate`

### Notepad
- `notepad_read`, `notepad_write_priority`, `notepad_write_working`, `notepad_write_manual`

### Project memory
- `project_memory_read`, `project_memory_write`, `project_memory_add_note`, `project_memory_add_directive`

### Code intelligence
- LSP: `lsp_hover`, `lsp_goto_definition`, `lsp_find_references`, `lsp_diagnostics`, and related helpers
- AST: `ast_grep_search`, `ast_grep_replace`
- Utility: `python_repl`

## Skills Registry

Invoke built-in workflows via `/<name>`.

### Workflow skills
- `autopilot` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full autonomous execution from idea to working code
- `ralph` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â persistence loop until completion with verification
- `ultrawork` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â high-throughput parallel execution
- `visual-verdict` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â structured visual QA verdicts
- `team` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â coordinated team orchestration
- `ccg` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Codex + Gemini + OpenCode synthesis lane
- `ultraqa` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â QA cycle: test, verify, fix, repeat
- `omc-plan` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â planning workflow and `/plan`-safe alias
- `ralplan` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â consensus planning workflow
- `sciomc` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â science/research workflow
- `external-context` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â external docs/research workflow
- `deepinit` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hierarchical AGENTS.md generation
- `deep-interview` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Socratic ambiguity-gated requirements workflow
- `ai-slop-cleaner` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â regression-safe cleanup workflow

### Utility skills
- `ask`, `cancel`, `note`, `learner`, `hubs-setup`, `mcp-setup`, `hud`, `hubs-doctor`, `trace`, `release`, `project-session-manager`, `skill`, `writer-memory`, `configure-notifications`

### Keyword triggers kept compact in AGENTS.md
- `"autopilot"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢autopilot`
- `"ralph"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ralph`
- `"ulw"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ultrawork`
- `"ccg"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ccg`
- `"ralplan"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ralplan`
- `"deep interview"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢deep-interview`
- `"deslop" / "anti-slop"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ai-slop-cleaner`
- `"deep-analyze"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢analysis mode`
- `"tdd"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢TDD mode`
- `"deepsearch"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢codebase search`
- `"ultrathink"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢deep reasoning`
- `"cancel"ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢cancel`
- Team orchestration is explicit via `/team`.

## Team Pipeline

Stages: `team-plan` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `team-prd` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `team-exec` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `team-verify` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `team-fix` (loop).

- Use `team-fix` for bounded remediation loops.
- `team ralph` links the team pipeline with Ralph-style sequential verification.
- Prefer team mode when independent parallel lanes justify the coordination overhead.

## Commit Protocol

Use git trailers to preserve decision context in every commit message.

### Format
- Intent line first: why the change was made
- Optional body with context and rationale
- Structured trailers when applicable

### Common trailers
- `Constraint:` active constraint shaping the decision
- `Rejected:` alternative considered | reason for rejection
- `Directive:` forward-looking warning or instruction
- `Confidence:` `high` | `medium` | `low`
- `Scope-risk:` `narrow` | `moderate` | `broad`
- `Not-tested:` known verification gap

### Example
```text
feat(docs): reduce always-loaded OAS instruction footprint

Move reference-only orchestration content into a native OpenCode skill so
session-start guidance stays small while detailed OAS reference remains available.

Constraint: Preserve AGENTS.md marker-based installation flow
Rejected: Sync all built-in skills in legacy install | broader behavior change than issue requires
Confidence: high
Scope-risk: narrow
Not-tested: End-to-end plugin marketplace install in a fresh OpenCode profile
```
