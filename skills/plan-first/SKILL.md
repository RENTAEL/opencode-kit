---
name: plan-first
description: "Convert uncertainty into explicit decisions before implementation."
---
# Plan First

Convert uncertainty into explicit decisions before implementation.

## Select the Mode

- **Plan only:** When the user asks only for a plan, create only the requested plan artifact or response, then stop. Do not write tests or implementation code.
- **Plan and execute:** When implementation is requested and the task is clear and reversible, state the plan and proceed phase by phase.
- **Decision required:** When ambiguity changes behavior, security, data, cost, or external effects, present the options and obtain direction before crossing that boundary.

## Plan Format

Keep the plan concise and include:

- goal and user-visible outcome;
- non-goals and scope boundaries;
- known facts, assumptions, and decisions still requiring input;
- approach and expected files or systems;
- ordered steps with an observable check for each phase;
- compatibility, security, data, and coordination risks;
- rollout, monitoring, rollback, and recovery where relevant;
- final verification, including unavailable environments or credentials.

## Execution Rules

1. Base the plan on repository evidence, not guessed files or APIs.
2. Prefer risk, reversibility, uncertainty, and coordination cost over file count as planning signals.
3. Update the plan when evidence invalidates an assumption. Explain material pivots instead of silently improvising.
4. Keep at most one phase active and reconcile every item as completed, blocked, or cancelled before handoff.
5. Treat non-goals as constraints. Do not expand the task because an adjacent improvement looks useful.
