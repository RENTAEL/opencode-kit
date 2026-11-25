---
name: lisheng-SenLee-project-anchor
description: "Use this skill to provide lightweight project governance that preserves project intent across long-running AI-assisted development without turning documentation into bureaucracy."
---
# Project Anchor

Use this skill to provide lightweight project governance that preserves project intent across long-running AI-assisted development without turning documentation into bureaucracy.

## Core model

Keep these concerns separate:

- `AGENTS.md`: small, persistent repo guidance and routing.
- Product boundaries: what the system does and intentionally does not do.
- Specs: observable behavior the system currently promises.
- Architecture: how the current system is structured and behaves internally.
- Invariants: rules that must remain true across implementations.
- ADRs: why important architecture decisions were made.
- Active changes: proposed future state for significant changes.
- `tasks.md` execution state: short-lived navigation for the current implementation task; it points back to authoritative change/current-truth docs rather than duplicating them.
- Tests/CI: executable enforcement of critical behavior and invariants.
- Git: code history.

Never use one giant append-only memory file.

## Before acting

1. Inspect the repository before creating governance files.
2. Read existing `AGENTS.md`, README, docs, tests, build config, CI, and relevant source.
3. Preserve valid existing documentation. Prefer incremental migration.
4. Do not invent product facts. Mark uncertain content `TBD` or an open question.
5. Use `references/document-roles.md` when document ownership is unclear.
6. Use `references/change-classification.md` to choose lightweight vs significant-change flow.

## Change classification

For trivial changes, avoid governance ceremony:

`understand -> edit -> test -> done`

For significant changes, use:

`proposal -> spec -> design -> tasks -> implementation -> verification -> reconciliation -> current truth -> archive`

Create only the artifacts that add decision value.

## Initialization / upgrade workflow

When asked to initialize or improve governance:

1. Audit what already exists.
2. Explain what can be reused and what is missing.
3. Create the smallest useful structure.
4. Keep `AGENTS.md` concise and route deeper knowledge through `docs/index.md`.
5. Initialize only facts supported by code, tests, existing docs, or explicit user requirements.
6. Use the helper script for deterministic scaffolding when useful:
   - `python scripts/governance.py init --root <repo> --profile generic|agent|python|java`
7. Review generated placeholders and replace only what can be verified.

The script never overwrites existing files.

## Starting a significant change

1. Read current truth first.
2. Create a change workspace:
   - `python scripts/governance.py new-change <change-name> --root <repo>`
3. Fill:
   - `proposal.md`: why, goal, scope, non-goals, constraints, done condition.
   - `spec.md`: requirements, scenarios, edge cases, acceptance criteria.
   - `design.md`: implementation approach, modules, data/state/concurrency, alternatives, trade-offs.
   - `tasks.md`: executable plan, compact execution state, progress/diagnoses, verification evidence, open questions.
4. Link to existing invariants/specs/ADRs rather than copying them.
5. Initialize `tasks.md` execution state from the authoritative proposal/spec/design using references, not duplicated requirement text.
6. Keep current truth unchanged until the change is delivered.

## Execution control during significant work

Use lightweight execution control only when the work is long-running, multi-step, failure-prone, interrupted/resumed, or otherwise at risk of drifting.

Maintain a compact `Execution State` in `tasks.md`:

- `Goal`: point to the authoritative goal.
- `Core anchors`: link the constraints/specs/invariants/ADRs that must stay true.
- `Active slice`: the one coherent implementation slice currently in focus.
- `Next`: the next concrete action within or immediately after that slice.
- `Deferred` (optional): known work that matters later but should not compete for current attention.

Refresh it at meaningful seams, not every tool call or model iteration. Typical seams include:

- completing a major implementation slice;
- discovering a fact that changes the plan;
- a failed verification that requires a different approach;
- expanding scope across modules or boundaries;
- resuming after interruption or context reset;
- preparing to declare the change complete.

At a seam, check only what is needed:

1. Is the goal still the original goal?
2. Are core anchors still respected?
3. What materially changed or became verified?
4. Is the active slice still the right focus, and is `Next` still the right next action?

Keep only one coherent active slice in working focus. Put useful but non-urgent side work in `Deferred` instead of switching context mid-slice. Do not use hard numeric limits; split work only when multiple concerns are competing for attention.

If repeated work fails, carry the diagnosis forward before retrying. Record only failures that change the next decision, and include what failed, why it failed, what must not be repeated, and the next approach. Do not materially repeat a failed approach unless new evidence or a changed hypothesis justifies it.

Do not record private chain-of-thought, full transcripts, or routine tool-by-tool history. Read `references/execution-control.md` when a task needs this control layer.

## Verification evidence

For significant changes, do not treat a command name or a green test suite as sufficient evidence by itself.

Record compact evidence in `tasks.md` when it matters:

- `Verifier`: test/command/review used.
- `Covers`: requirement, invariant, failure mode, lifecycle/concurrency case, or other behavior actually checked.
- `Result`: pass/fail and any decision-relevant note.

Prefer a small number of high-signal evidence entries over an exhaustive log.

## Completion gate

A significant change is not complete merely because implementation is finished or tests are green. Before declaring completion, confirm that:

- required scope and acceptance criteria are accounted for;
- important behavior/invariants have decision-relevant verification coverage;
- no unresolved blocker or open question still affects correctness or intended scope;
- final reconciliation has been completed.

Keep this as a gate, not a new document or ceremony.

## ADR rule

Create an ADR only for consequential, durable architecture choices where a future maintainer could reasonably ask, ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œWhy did we choose this instead of the simpler alternative?ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â

Use:
`python scripts/governance.py new-adr "<title>" --root <repo>`

Do not create ADRs for ordinary implementation details, renames, small bug fixes, or routine refactors.

## Reconciliation before completion

For significant changes, compare:

- intent / goal
- active change spec
- implementation
- tests and verification coverage
- product boundaries
- invariants
- current architecture
- ADR status

Resolve mismatches before declaring completion. Read `references/reconciliation.md`.

Only after verification:
1. Update current specs/architecture/invariants as needed.
2. Add/supersede ADRs if a durable architecture decision changed.
3. Archive the active change.
4. Do not require future sessions to read archived changes by default.

## Safety against documentation bloat

- One fact -> one authoritative source.
- Execution state points to authoritative facts; it does not become another source of truth.
- Current-truth docs describe the current system, not a timeline.
- Progress notes record only decision-relevant changes, diagnoses, or blockers.
- Verification evidence records coverage, not raw command logs.
- Git records ordinary code history.
- Archive is historical context, not default prompt context.
- Prefer links over duplication.
- Prefer stable code anchors over line numbers.
- If no semantic contract changed, documentation usually does not need changing.

## Validation

Use:
`python scripts/governance.py validate --root <repo>`

Treat validation as structural hygiene, not proof that the docs are semantically correct.

## Supporting references

Read only when needed:

- `references/document-roles.md`
- `references/change-classification.md`
- `references/execution-control.md`
- `references/reconciliation.md`
- `references/language-profiles.md`

Templates live under `assets/templates/`.
