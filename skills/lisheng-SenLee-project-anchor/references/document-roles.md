# Document roles

| Artifact | Question it answers | Lifecycle |
|---|---|---|
| `AGENTS.md` | What should the coding agent consistently do in this repo? | Small, persistent |
| Product boundaries | What is in/out of scope? | Current truth |
| Specs | What observable behavior is promised? | Current truth |
| Architecture | How is the current system structured/implemented? | Current truth |
| Invariants | What must never be broken? | Current truth / normative |
| ADR | Why was an important architecture choice made? | Historical/explanatory |
| Active change | What are we proposing to change now? | Working change context |
| `tasks.md` execution state | What is the active implementation slice, next action, and any useful deferred side work? | Short-lived execution navigation |
| Tests/CI | Which critical contracts are executable? | Enforcement |
| Git history | What code changed over time? | History |

## Normative vs descriptive vs historical

**Normative:** product boundaries, accepted/current specs, invariants.

**Descriptive:** architecture.

**Historical/explanatory:** ADRs, archived changes, Git history.

**Short-lived operational:** `tasks.md` execution state. It points to normative/descriptive sources and must not silently replace them.

An old ADR does not override newer current truth. If a decision changes, create a new ADR that supersedes the old one.

## Current truth rule

Current-truth docs state what is true now.

Bad: “Timeout was 12h, then 24h, and now configurable.”

Good: “Session timeout is configurable.”

Use Git, ADRs, and archived changes for history.
