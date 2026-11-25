# AGENTS.md

## Project

{{PROJECT_NAME}}

Project type: `{{PROFILE}}`

Describe the project's purpose using verified facts only. Use `TBD` where intent is not yet established.

## Read Before Significant Work

1. `docs/index.md`
2. Relevant product boundaries and current specs
3. Relevant architecture docs
4. Relevant invariants
5. Relevant accepted ADRs
6. The active change, if one exists

Do not read all archived changes by default.

## Change Policy

### Lightweight changes

`understand -> edit -> test -> done`

### Significant changes

For observable behavior, cross-module, lifecycle/state, API/data, security/permission, concurrency, migration, or architecture-affecting changes:

`proposal -> spec -> design -> tasks -> implementation -> verification -> reconciliation -> update current truth -> archive`

Use `docs/changes/active/<change-name>/`.

For long-running or failure-prone significant work, keep the active change's `tasks.md` execution state current at meaningful seams. Keep one coherent active slice in focus; defer unrelated later work instead of context-switching. Do not checkpoint every tool call or duplicate requirements into it.

## Documentation Ownership

- Product boundaries: what is in/out of scope.
- Specs: observable behavior currently promised.
- Architecture: how the current system works internally.
- Invariants: rules that must remain true.
- ADRs: why durable architecture decisions were made.
- Active changes: proposed future state and working plan.
- `tasks.md` execution state: short-lived navigation during implementation, never a second source of truth.
- Git: ordinary code history.

Do not use long-lived docs as append-only change logs.

## Documentation Update Rules

- Behavior-preserving implementation refactor: usually no long-lived doc change.
- Observable behavior change: update current spec after delivery.
- Current internal design change: update architecture after delivery.
- Product scope/boundary change: update product boundaries.
- New/changed non-negotiable rule: update invariants and tests where practical.
- Durable architecture choice: add or supersede an ADR.
- Significant in-progress work: maintain the active change docs.

## Verification

Do not declare a significant change complete only because tests pass.

For important checks, record what the verifier actually covers, then reconcile intent, spec, implementation, tests, boundaries, invariants, architecture, and ADR status.

A significant change is complete only when required scope/acceptance criteria are accounted for, important verification coverage exists, correctness-affecting blockers are resolved, and final reconciliation is complete.

## Conflict Handling

If code, tests, and current-truth docs disagree, investigate whether code is wrong, docs are stale, or a migration/change is incomplete. Do not silently propagate the mismatch.
