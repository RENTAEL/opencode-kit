---
name: safe-refactor
description: "Treat behavior preservation as a claim that requires a baseline and repeated evidence."
---
# Safe Refactor

Treat behavior preservation as a claim that requires a baseline and repeated evidence.

## Define Observable Behavior

Include public APIs and types, serialized and database representations, errors, logs and events, generated output, filesystem effects, performance budgets, deployment compatibility, and user-visible behavior that callers rely on.

## Refactor Loop

1. Inspect repository instructions, worktree status, callers, tests, and generated-code boundaries. Preserve unrelated work.
2. Establish a green focused baseline. If coverage is thin, add characterization tests that capture current behavior before changing structure.
3. Make one mechanical step: rename, extract, move, or deduplicate.
4. Update direct callers and search for dynamic references in configuration, reflection, templates, serialization, migrations, documentation, and build tooling.
5. Run the smallest relevant checks after each step and expand to the full affected suite at stable checkpoints.
6. Keep behavior fixes and compatibility migrations outside the refactor. Pause and reclassify the task when a behavior change becomes necessary.
7. Use logical working-tree checkpoints. Do not create branches or commits unless the user explicitly requests them.

## Completion Evidence

- Show that focused and relevant suites remain green against the baseline.
- Confirm snapshots, golden files, generated output, and public contracts did not change unless explicitly approved.
- Search for obsolete names and paths after moves or renames.
- Review the final diff for a clear structural improvement and no hidden behavior change.
