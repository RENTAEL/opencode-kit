# Active Changes

Each significant change may use:

```text
<change-name>/
├── proposal.md
├── spec.md
├── design.md
└── tasks.md
```

Do not create this structure for trivial changes.

Current truth remains authoritative until the change is delivered and reconciled.

For long-running or failure-prone significant work, `tasks.md` may also carry a compact execution state (`Goal`, `Core Anchors`, `Active Slice`, `Next`, optional `Deferred`). It is navigation, not a second source of truth.
