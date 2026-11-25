---
name: natuleadan-skills
description: "Stub skill: the platform definition is still being written. These references hold the shape of each area, not final behavior."
---
# Natuleadan Skills

> Stub - the platform definition is still being written. These references hold
> the shape of each area, not final behavior.

One skill that groups the open-source programs of the platform. Each program
gets a reference here instead of a new top-level skill, so the surface stays
stable as programs appear.

## Map

| Need | Reference |
|---|---|
| Calls, categories, scheduling, human confirmation | `references/platform.md` |
| Service definition, entries, auth, events, docs | `references/services.md` |
| Provisioning, clusters, datastores, backups, firewall | `references/operations.md` |
| Relational storage, vectors, indexes, distribution | `references/data.md` |

## Status

- Every reference is a stub: one short description plus one flow diagram.
- Nothing here is a commitment; each area expands when the platform definition
  settles.
- `scripts/main.ts` prints this map; run it with `pnpm skill natuleadan-skills`.

## References

- `references/platform.md` - agents, robots, toolsets and calls
- `references/services.md` - declarative services and their contracts
- `references/operations.md` - hosts, clusters, datastores and recovery
- `references/data.md` - SQL storage with native vector search
