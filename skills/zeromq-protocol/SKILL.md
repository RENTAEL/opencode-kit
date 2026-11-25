---
name: zeromq-protocol
description: "Turn a ZeroMQ topology into a small, explicit, evolvable wire contract with bounded flow control and testable peer state."
---
# ZeroMQ Protocol

## Goal

Turn a ZeroMQ topology into a small, explicit, evolvable wire contract with
bounded flow control and testable peer state.

## Workflow

1. Write the protocol before hiding it inside code.
2. State goals, roles, transport assumptions, version/maturity, security, and
   exact failure semantics.
3. Define message grammar and frame/field types; use normative MUST/SHOULD/MAY
   intentionally.
4. Keep implementation internals out of the wire model.
5. Split low-volume control from high-volume data when their needs differ:
   - control: descriptive, extensible, synchronous errors are normal;
   - data: compact, async, stable, exceptional errors are fatal/drop/recover.
6. Model non-trivial peer conversations as finite state machines.
7. Add protocol signatures/version fields where endpoints can receive stale or
   unrelated traffic.
8. For bulk transfer, use receiver-issued byte/message credits instead of
   unbounded sender queues.
9. Cross-test independent client/server implementations and malformed inputs.
10. Version contracts compatibly; never repurpose old names with new meaning.

## Rules

- Code is an implementation, not the only specification.
- Multipart framing is atomic but not a substitute for semantic versioning.
- Measure before choosing a custom binary codec.
- Make parsers bounded and reject impossible sizes/states before allocation.
- Recovery state should travel with the client/request when that avoids
  fragile server-held sessions.
