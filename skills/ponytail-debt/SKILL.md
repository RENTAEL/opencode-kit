---
name: ponytail-debt
description: "Find and track technical-debt signals using the Ponytail framework (external import by Dietrich Gebert, MIT): prioritize cleanup like a lazy senior dev."
---
# Ponytail Debt

> External import of **Ponytail** by Dietrich Gebert and contributors, adapted from upstream v4.9.0 under MIT.

## Goal

Collect deliberate `ponytail:` simplification markers into a debt ledger so deferred upgrade paths stay visible.

## Input

A repository with text-search access. Git blame is optional when ownership is requested.

## Output

Group markers by file:

`<file>:<line>, <simplification>. ceiling: <limit>. upgrade: <trigger/path>.`

End with `<N> markers, <M> with no trigger.` If none exist: `No ponytail: debt. Clean ledger.`

## Workflow

Search source files for comment markers containing `ponytail:` while skipping VCS metadata, dependencies, and build output. Support the comment syntax used by the repository, not only `#` or `//`.

The convention is:

`ponytail: <known ceiling>, <upgrade trigger/path>`

Flag a marker with `no-trigger` when it does not name when or how to revisit the shortcut.

## Rules

- Read and report only by default.
- Persist a ledger such as `PONYTAIL-DEBT.md` only when the user asks.
- Do not invent owners or upgrade triggers. Use repository evidence.
