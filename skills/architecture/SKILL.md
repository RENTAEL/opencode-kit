---
name: architecture
description: "Create or evaluate an architecture decision record (ADR). Use when choosing between technologies (e.g., Kafka vs SQS), documenting a design decision with trade-offs and consequences, reviewing a system design proposal, or designing a new component from requirements and constraints."
allowed-tools: Read, Glob, Grep
argument-hint: <decision or system to design>
---
# /supergraph:architecture

Three phases: explore ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ HTML report ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ grilling loop.

Announce: "ÃƒÂ°Ã…Â¸Ã‚ÂÃ¢â‚¬ÂºÃƒÂ¯Ã‚Â¸Ã‚Â /supergraph:architecture ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mapping codebase structure..."

## Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Explore

**1a. Read CONTEXT.md:**
```bash
cat CONTEXT.md 2>/dev/null || echo "No CONTEXT.md"
```

**1b. Codebase Memory overview (optional):**
Use `CBM_PROJECT` with `get_architecture` aspects `overview`, `layers`,
`boundaries`, `clusters`, and `hotspots`. After `get_graph_schema`, run shared
contract recipes `hubs`, `bridges`, `cross-boundary`, and `test-gaps`.
If codebase-memory-mcp is unavailable, label graph evidence `unavailable`, use
Serena/filesystem evidence, and generate Mermaid diagrams from imports.

**1c. Serena structure (optional):**
```
mcp__serena__get_symbols_overview()
```

**1d. Read 3-5 hub node files** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â understand actual structure, naming, patterns.

## Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Generate HTML Report
Write self-contained `docs/supergraph/architecture-review-<YYYY-MM-DD>.html` with Tailwind+Mermaid header, architecture `graph TD`, per-candidate card (Problem/Proposal/Before/After Mermaid/Impact/Trade-offs with badge Strong/Worth exploring/Speculative), plus tables for Test Gaps and Unexpected Coupling.

Open: `open docs/supergraph/architecture-review-<date>.html || xdg-open ... || echo "Report saved: ..."`

## Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Grilling Loop

For each Strong candidate, ask one focused question:

> "Candidate N proposes [X]. Is this consistent with [constraint from CONTEXT.md / known business rule]?"

Incorporate answers to refine the candidate cards. Mark dismissed candidates as `Rejected ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [reason]`.

After grilling, present final prioritized list:
```
Strong candidates (ready for /supergraph:plan):
  1. [Name] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [one-line rationale]

Worth exploring (needs spike first):
  2. [Name] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [open question to resolve]

Speculative (park for later):
  3. [Name] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [what would need to be true]
```

## Report

```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ /supergraph:architecture complete
- Report: docs/supergraph/architecture-review-<date>.html
- Communities: N | Hub nodes: N | Bridge nodes: N
- Candidates: N Strong, N Worth exploring, N Speculative
- Next: /supergraph:plan (for Strong candidates) or /supergraph:prototype (for uncertain ones)
```

## Rules

- Always open the HTML file automatically
- Mermaid diagrams must reflect actual graph data, not invented structure
- Speculative candidates must be labeled ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never present guesses as strong recommendations
- Update CONTEXT.md if review revealed undocumented architectural invariants:
  ```bash
  printf '\n## <invariant>\n[description]\n' >> CONTEXT.md
  ```
- If graph was empty or unavailable, note "Diagram generated from filesystem structure" in the HTML report header
