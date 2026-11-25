---
name: morphir
description: "Translates pure business/decision logic into [Morphir](https://morphir.finos.org/) IR by hand-authoring an equivalent Elm model, then verifies the translation is behaviorally faithful using a hand-traced decision table ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not by trusting `morphir-elm gen`/`test..."
---
# Morphir

Translates pure business/decision logic into [Morphir](https://morphir.finos.org/) IR by hand-authoring an equivalent Elm model, then verifies the translation is behaviorally faithful using a hand-traced decision table ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not by trusting `morphir-elm gen`/`test`/`develop` round-trips, which are not reliable correctness signals for this purpose (see Phase 3).

This is a narrower, complementary technique to exhaustive state-space model-checking (e.g. an Alloy-based toolchain, if one is part of the project's workflow): it doesn't search a state space for a counterexample to a claimed property, it checks that a hand-authored model produces the same output as the source code on a curated set of concrete fixtures. That's a weaker guarantee in the abstract (untested inputs are unverified) but a much cheaper and more approachable one to produce and review by hand, and it's the right tool when the actual goal is "does this Elm model faithfully represent this Scala/Java function," not "does this system ever reach a bad state."

Work phases **A ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ D** in order.

---

## Phase A ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Scope: pure logic only

Before modeling anything, confirm the candidate function is actually pure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no I/O, no database access, no network calls, no mutable shared state. Morphir's IR and Elm's own language design both assume purity; effectful code doesn't benefit from being forced into this shape.

1. Identify candidate functions: decision/rule logic, eligibility checks, value comparison, tree/policy evaluation, matching, and similar branch-heavy logic with no external dependency in the signature or body are the strongest candidates.
2. For each candidate, confirm purity by reading the function body directly, or by using structural search (`ast-grep`) or symbol/call-graph tools (`serena`) to rule out effect types (e.g. `IO`/`Task`/`Future`/`ZIO`/DAO calls) anywhere in the call path the function actually exercises. A function only *called from* effectful code still qualifies if the function itself is pure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't over-exclude based on caller context.
3. Scope to one Morphir project per codebase area (one `morphir.json`, multiple `exposedModules`) rather than one project per function ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the incremental cost of adding a module to an existing project is much lower than standing up a new one each time.

**Done when:** the candidate function is confirmed pure, and it's clear which existing (or new) Morphir project it belongs to.

---

## Phase B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Author (Scala/Java ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Elm)

Translate the source function into an Elm module 1:1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â same branching structure, same short-circuit order. Order matters for behavioral fidelity: if the source short-circuits a guard before evaluating a later condition, the Elm model must preserve that exact evaluation order, not just the same eventual output on totally-evaluated inputs.

Full mechanics ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â project shape, CLI subcommands, and every verified toolchain trap ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â in `references/morphir-elm-cli.md`. Read it before a first `morphir-elm` invocation; skimming it after hitting an error costs more time than reading it up front.

Key points to keep in mind while authoring:

- `morphir-elm` bundles its own Elm frontend ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no separate `elm` binary is required or expected on PATH.
- `morphir.json`'s `exposedModules` entries are relative to the project's `name` field, not fully-qualified paths ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see the reference for the exact shape.
- `morphir-elm gen`'s Scala/TypeScript/etc. output is not meant to be diffed against hand-written source for a correctness check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the compiled output routes through Morphir SDK wrappers and always diverges textually from idiomatic hand-written code, even when behaviorally identical. Don't design a verification step around comparing generated code to the original; that's what Phase C's decision table is for instead.

**Done when:** an Elm module exists compiling into the project's IR (`morphir-elm make` exits 0) for every candidate function scoped in Phase A.

---

## Phase C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Verify (decision table)

This is the actual correctness gate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not `morphir-elm make`'s exit code (which only confirms the Elm parses, not that it's behaviorally correct), and not `gen`'s output (see Phase B).

Build a decision table: a set of concrete input fixtures, each hand-traced through **both** the Elm model and the cited source `file:line`, side by side. Any divergence is a finding to report explicitly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never silently adjust the Elm to match the source without flagging it, since the source could be the buggy side, not the model. Full format, fixture-selection guidance (happy path, every branch/guard, short-circuit cases, boundary/empty cases), and a worked example in `references/decision-table-methodology.md`. A starter template is at `references/templates/decision-table-template.md`, and a starter Elm module skeleton (with the project-shape and type-variable-casing reminders inline) is at `references/templates/starter-module.elm`.

**Done when:** every fixture in the table has traced outcomes recorded for both the model and the source, and every divergence is either resolved (with the resolution direction stated) or explicitly filed as an open finding ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never silently dropped.

---

## Phase D ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Report

State plainly, for everything modeled in this pass:

- Which functions were modeled, and where the Elm lives.
- The decision table's fixture count and pass/divergence outcome for each.
- Any divergence found, which side (model or source) is suspected wrong, and why ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is a judgment call to report, not to silently resolve. If the project has a dedicated spec-vs-code drift tool as part of its workflow, hand divergences needing that judgment off to it rather than re-deriving the call here.
- Anything explicitly left out of scope (effectful code, functions not yet swept) so a future pass doesn't have to re-derive what's already been ruled out.

**Done when:** the user has a clear picture of what's modeled, what's verified clean, and what's still open ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nothing silently skipped.

---

## Running `morphir-elm develop`

`morphir-elm develop` serves a web UI for browsing a project's IR, but it's a long-running foreground process with no built-in shutdown mode ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â launching it detached silently orphans it, leaving it bound to its port. Use the `morphir-develop` executable (assumed available on PATH ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not bundled with this skill) instead of invoking `morphir-elm develop` directly: it wraps the server with guaranteed cleanup (SIGINT/SIGTERM/normal-exit all kill the server and confirm the port is free) and warns if the project's `morphir-ir.json` looks older than its `.elm` sources. Run `morphir-develop --help` for usage; its one known limitation is that `kill -9` on the wrapper itself can't run its cleanup trap, requiring a manual `lsof -i :<port> -sTCP:LISTEN` + `kill` to recover.

---

## Anti-patterns

- Modeling effectful code (I/O, DB, network) in Morphir/Elm ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Morphir's guarantees are about pure functions only.
- Treating `morphir-elm make`'s exit code as a correctness signal ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it only confirms the Elm parses into IR, not that the IR is behaviorally correct.
- Diffing `morphir-elm gen`'s generated output against hand-written source code as a correctness check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the output always diverges textually even when correct.
- Silently "fixing" the Elm model to match the source on a decision-table divergence without flagging it as a finding ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the source may be the buggy side.
- Losing short-circuit/evaluation order during translation because the eventual output happened to match on the fixtures tried so far.
- Standing up a new Morphir project per function instead of adding modules to an existing project for the same codebase area.
- Launching `morphir-elm develop` detached without the cleanup wrapper, orphaning it on the port.
