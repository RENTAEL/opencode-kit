# Example: Significant change

This example shows the governance shape for a fictional change: making a job runner idempotent across retries.

It is intentionally small. The point is to demonstrate the relationships between artifacts, not to model a complete production system.

```text
proposal.md   -> goal, scope, non-goals, constraints
spec.md       -> observable requirements and acceptance criteria
design.md     -> implementation approach and trade-offs
tasks.md      -> compact execution navigation + evidence
```

Notice that `tasks.md` links back to the authoritative goal and requirements instead of copying them in full.
