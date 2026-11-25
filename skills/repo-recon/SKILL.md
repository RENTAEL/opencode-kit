---
name: repo-recon
description: "Map before changing. Keep recon proportional to the task and read-only unless the user explicitly requests a persistent artifact."
---
# Repo Recon

Map before changing. Keep recon proportional to the task and read-only unless the user explicitly requests a persistent artifact.

## Establish the Boundary

1. Read repository instructions and resolve their scope and precedence.
2. Inspect `git status` or the equivalent before interpreting files. Preserve unrelated and pre-existing work.
3. Keep notes in the agent's ephemeral context. Create `NOTES.md` or another repository file only when the user requests it.

## Map the Relevant System

1. **Read the map.** Inspect the root layout, manifests, lockfiles, build and CI configuration, entry points, generated-code boundaries, and domain docs.
2. **Learn commands safely.** Find install, build, test, lint, and typecheck commands. Inspect cost, side effects, required services, credentials, and likely runtime before executing them. Run the smallest useful baseline and record checks that are unavailable.
3. **Trace one representative flow.** Follow a task-adjacent input through validation, state changes, outputs, error handling, trust boundaries, and observability. Include workers, queues, caches, or persistence when relevant.
4. **Extract conventions.** Note naming, module boundaries, shared helpers, test placement, error patterns, dependency rules, and newer versus legacy patterns.
5. **Report the map.** Summarize relevant paths, exact commands, current baseline, important dependencies, risks, and open questions.

## Standing Rules

- Search before assuming that a file, symbol, command, or configuration exists.
- Read a file before editing it and prefer an established sibling implementation.
- Do not edit generated output when its source or generator is the real boundary.
- Scale the pass to uncertainty and risk, not repository size. Stop when enough evidence exists to perform the requested task safely.
