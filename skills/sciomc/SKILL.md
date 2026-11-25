---
name: sciomc
description: "Orchestrate parallel scientist agents for comprehensive research workflows with optional AUTO mode for fully autonomous execution."
---
# Research Skill

Orchestrate parallel scientist agents for comprehensive research workflows with optional AUTO mode for fully autonomous execution.

## Usage

```
/sciomc <goal>                    # Standard research with user checkpoints
/sciomc AUTO: <goal>              # Fully autonomous until complete
/sciomc status                    # Check current research session status
/sciomc resume                    # Resume interrupted research session
/sciomc list                      # List all research sessions
/sciomc report <session-id>       # Generate report for session
```

## Research Protocol

### Stage Decomposition

Decompose research goals into 3-7 independent stages. Each stage has: **Focus**, **Hypothesis** (optional), **Scope**, **Tier** (LOW|MEDIUM|HIGH).

### Parallel Scientist Invocation

Fire independent stages in parallel via Task tool. Always pass `model` parameter explicitly:

| Task Complexity | Agent | Model | Use For |
|-----------------|-------|-------|---------|
| Data gathering | `scientist` (model=haiku) | haiku | File enumeration, pattern counting, simple lookups |
| Standard analysis | `scientist` | sonnet | Code analysis, pattern detection, documentation review |
| Complex reasoning | `scientist` | opus | Architecture analysis, cross-cutting concerns, hypothesis validation |

```
@scientist(model="haiku", prompt="[RESEARCH_STAGE:1] Investigate...")
@scientist(model="sonnet", prompt="[RESEARCH_STAGE:2] Analyze...")
@scientist(model="opus", prompt="[RESEARCH_STAGE:3] Deep analysis of...")
```

### Verification Loop

After parallel execution, cross-validate findings:

```
@scientist(model="sonnet", prompt="[RESEARCH_VERIFICATION] Cross-validate these findings for consistency. Check: 1) Contradictions between stages 2) Missing connections 3) Gaps in coverage 4) Evidence quality. Output: [VERIFIED] or [CONFLICTS:<list>]")
```

## AUTO Mode

Runs complete research workflow autonomously with loop control. Max 10 iterations. Continues until `[PROMISE:RESEARCH_COMPLETE]` emitted or max iterations reached. Cancel via `/cancel`.

### Promise Tags

- `[PROMISE:RESEARCH_COMPLETE]` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â All stages done, verified, report generated
- `[PROMISE:RESEARCH_BLOCKED]` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Cannot proceed (missing data, access issues)

### Loop Control

```
[RESEARCH + AUTO - ITERATION {{ITERATION}}/{{MAX}}]
Current state: {{STATE}} | Completed: {{COMPLETED_STAGES}} | Pending: {{PENDING_STAGES}}
```

## Parallel Execution Patterns

**Independent stages** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fire simultaneously:
```
@scientist(model="haiku", prompt="[STAGE:1] Analyze src/api/...")
@scientist(model="haiku", prompt="[STAGE:2] Analyze src/utils/...")
```

**Hypothesis battery** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â test multiple hypotheses in parallel:
```
@scientist(model="sonnet", prompt="[HYPOTHESIS:A] Test if caching improves...")
@scientist(model="sonnet", prompt="[HYPOTHESIS:B] Test if batching reduces...")
```

**Cross-validation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sequential after all parallel stages complete:
```
@scientist(model="opus", prompt="[CROSS_VALIDATION] Validate consistency across all findings...")
```

**Concurrency limit:** Max 20 concurrent scientists. Batch if more.

## Session Management

```
.opencode/state/research/{session-id}/
  state.json              # Session state and progress
  stages/                 # Stage findings
  findings/raw/           # Raw findings from scientists
  findings/verified/      # Post-verification findings
  report.md               # Final synthesized report
```

State file: `{ id, goal, status, mode, iteration, maxIterations, stages: [{ id, name, tier, status, findingsFile }], verification: { status, conflicts }, createdAt, updatedAt }`

## Tag Extraction

Scientists use structured tags. Extract with regex:

```
[FINDING:<id>] <title> ... [/FINDING]
[EVIDENCE:<finding-id>] File: <path>, Lines: <range> [/EVIDENCE]
[CONFIDENCE:HIGH|MEDIUM|LOW] <reasoning>
[STAGE_COMPLETE:<id>]
[VERIFIED|CONFLICTS:<list>]
```

**Quality threshold:** Each [FINDING] needs ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥1 [EVIDENCE], a [CONFIDENCE], absolute file paths, and must be reproducible.

## Report Generation

Template: Executive Summary ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Methodology (stages table) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Key Findings (with evidence) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Cross-Validation Results ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Limitations ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Recommendations ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Appendix (raw data links, state.json).

Figures embedded via `[FIGURE:path] Caption [/FIGURE]` markers. Types: architecture diagrams, flow charts, dependency graphs, timelines, comparison tables.

## Configuration

```json
{ "hubs": { "research": { "maxIterations": 10, "maxConcurrentScientists": 5, "defaultTier": "MEDIUM", "autoVerify": true, "generateFigures": true, "evidenceContextLines": 5 } } }
```

## Troubleshooting

- **Stuck in verification loop?** Check for conflicting findings between stages; re-run specific stages with different approach.
- **Low-quality findings?** Check tier assignment; ensure prompts include clear scope and expected output format.
- **AUTO mode exhausted iterations?** Review state to see where stuck; consider breaking into smaller sessions.
- **Missing figures?** Verify figures/ directory exists and [FIGURE:] paths are relative to session directory.
