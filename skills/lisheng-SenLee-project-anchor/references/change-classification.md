# Change classification

Use the lightest process that protects the project.

## Trivial / lightweight change

Usually no change workspace is needed when scope is local and obvious, observable contracts do not change, there are no cross-module lifecycle implications, and verification is straightforward.

Examples: typo, logging improvement, narrow bug with already-defined expected behavior, rename, behavior-preserving refactor.

Flow:

`understand -> edit -> test -> done`

## Significant change

Use an active change when one or more apply:

- new user/system capability
- observable behavior or contract changes
- multiple modules must coordinate
- state machine or lifecycle changes
- session/memory/tool/background-job semantics change
- API or data model changes
- migration required
- security or permission boundary changes
- concurrency or consistency model changes
- architecture-affecting refactor
- high regression cost
- meaningful edge cases

Flow:

`proposal -> spec -> design -> tasks -> implementation -> verification -> reconciliation -> current truth -> archive`

If the significant change is long-running, multi-step, failure-prone, interrupted/resumed, or otherwise at meaningful risk of drift, use the lightweight execution-control rules in `references/execution-control.md`, including one coherent active slice and optional deferred side work. Do not add them to routine short changes merely because a change workspace exists.

## ADR threshold

An ADR is justified when the choice is durable, architecture-relevant, non-obvious, has meaningful alternatives/trade-offs, and future maintainers benefit from knowing why.

Do not use ADR as a generic change log.
