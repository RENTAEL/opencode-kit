---
name: tdd-loop
description: "Use a failing behavior test as the executable specification."
---
# TDD Loop

Use a failing behavior test as the executable specification.

## Preserve Scope and State

- Inspect existing tests, commands, conventions, and worktree state before editing.
- Preserve unrelated changes. Do not create branches, stage, commit, sync remotes, or push unless the user explicitly requests that git workflow.
- If no test framework exists, prefer an existing dependency-free mechanism. Ask before adding a new framework or dependency.

## Red-Green-Refactor

1. **Red:** Write the smallest test that demonstrates one missing behavior. For a diagnosed bug, preserve the reproduction as a regression test.
2. **Observe:** Run the test and confirm it fails for the intended assertion, not setup, import, fixture, or environment noise. If it passes, determine whether the behavior already exists or the test is ineffective.
3. **Green:** Implement the minimum production change that satisfies the behavior.
4. **Expand:** Run the focused test, adjacent tests, and the relevant suite. Add contract or integration coverage when behavior crosses a process, network, database, filesystem, or public API boundary.
5. **Refactor:** Improve structure while all tests remain green. Use logical working-tree checkpoints; commit only when separately authorized.
6. Repeat for the next independently verifiable behavior.

## Protect Test Integrity

- Do not weaken, delete, skip, or broadly mock an assertion to manufacture green.
- Mock expensive collaborators, not the unit or behavior under test.
- Prefer observable outcomes over implementation-call assertions.
- Add characterization tests before changing poorly understood legacy behavior.
- Control time, randomness, concurrency, and external services where possible. For inherently stochastic AI behavior, use repeated evaluations through `evaluate-ai-changes` rather than pretending one unit test proves quality.
- Treat a painful test as design feedback, not permission to skip coverage.
