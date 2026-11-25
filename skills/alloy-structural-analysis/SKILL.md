---
name: alloy-structural-analysis
description: "A formal model-checking layer over Allium specs. Where `allium check` validates that a spec parses and is self-consistent, and `weed` compares a spec against the code by pattern and judgment, this skill adds the one thing neither does: exhaustively searching a spec's actual st..."
---
# Alloy Structural Analysis

A formal model-checking layer over Allium specs. Where `allium check` validates that a spec parses and is self-consistent, and `weed` compares a spec against the code by pattern and judgment, this skill adds the one thing neither does: exhaustively searching a spec's actual state space with Alloy, Electrod, and nuXmv for a counterexample to a claimed property. An `UNSAT` result here is a much stronger claim than "the tests pass" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it means no state satisfying the negated property exists within the checked scope, not just that no one has found one yet.

This skill does one thing well and hands off the rest. It does not parse Allium syntax (`allium` already does), does not judge spec-vs-code divergence (`weed` already does), and does not search code (`ast-grep`/`serena` already do). Its job is the translation into Alloy and the model-checking run in between.

Work phases **A ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ F** in order. C and D can loop back into B for a narrowed re-check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see Phase F.

---

## Phase A ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Scope

Establish exactly which Allium spec(s) and which codebase area are in scope before doing anything else.

1. Identify the spec file(s) or obligation(s) under analysis. If the user named a PR, ticket, or divergence already surfaced by `weed`, scope to the obligation that divergence concerns ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not the whole spec.
2. Identify the codebase area Phase E will search, if a counterexample surfaces. Ask if ambiguous; do not assume the whole repo is in scope just because a spec file doesn't say otherwise.
3. If temporal/CTL/LTL behavior is not actually being claimed (the property is purely structural, no "eventually"/"always"/state-transition claim), say so ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a plain Alloy check without Electrod/nuXmv is faster and the loop should use it instead of paying for the temporal solver on every run.

**Done when:** the spec/obligation in scope and the codebase search area are both named.

---

## Phase B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Translate (Allium ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Alloy)

Produce or update the `.als` model for each obligation in scope. This is a translation step, not free composition ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Allium's semantics have known traps that silently produce a model that checks the wrong thing:

- **`use` imports do not bring in value types.** A spec that imports a module via `use` does not get that module's value types along with it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the Alloy model needs one of those types, declare or import it explicitly rather than assuming the `use` covered it. A model missing a value type doesn't error; it just quietly checks a weaker property than the spec states.
- **Unused refs and untyped trigger params are a silent-acceptance trap.** Allium accepts a trigger parameter with no declared type, and accepts a ref that's declared but never used, without complaint. Both are usually authoring mistakes in the source spec, not intentional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â carry them into the Alloy translation only if you've confirmed they're deliberate, otherwise flag them back rather than encoding the gap into the model.
- **Check command-name uniqueness across the spec set now, not at invocation time.** Phase C's harness silently collapses duplicate command names (see below) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â catching a name collision here, while still composing the model, is cheaper than debugging a missing result later.
- **Run `allium check` against every spec file in the checked set together, not one at a time** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â checking a single file in isolation emits spurious unresolved-path warnings for anything it depends on elsewhere and hides real cross-file findings. The output is concatenated JSON objects, one per file, **not a single JSON document** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a plain parse of the combined output fails partway through; use a streaming/multi-document decoder.

Full detail and rationale: `references/allium-to-alloy.md`.

**Done when:** a `.als` file exists (or is updated) for every in-scope obligation, and command names are confirmed unique across the whole set being checked.

---

## Phase C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Check (invoke the toolchain)

Run the model(s) through Alloy's real backend, not the bounded default:

```bash
alloy exec -s electrod.nuxmv -t json -f -o <output-dir> <file>.als
```

Use the CTL-only path (no `-s electrod.nuxmv`) only when Phase A confirmed there's no temporal claim to check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's cheaper and the temporal solver adds nothing to a non-temporal property.

**Batch every spec in scope into one invocation** (concatenated JSON) rather than one process per file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is both cheaper and the way the toolchain expects to be driven at scale.

The harness has traps that will silently produce a wrong or absent result if skipped. None are optional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full mechanics, exact JSON structure, and the SAT/UNSAT discriminator in `references/alloy-harness.md`, read it before a first invocation:

1. **The process exit code is always 0, except for an actual `.als` syntax error.** SAT, UNSAT, a solver crash, a missing file, and an unmatched command name all return 0. The real success criterion is: `receipt.json` exists **and** every expected command name is present as a key in it.
2. **`receipt.json`'s `values` field is unsound off-scope, and the defect is solver-dependent** (corrupts under `sat4j`/`glucose`/`minisat.prover`; correct under `minisat`/`sat4j.light`). Use `exactly N Sig` scopes, or parse `-t xml` instead of trusting `values` from JSON. `skolems` (the counterexample witness) is never affected ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â trust it first.
3. **Duplicate command names silently collapse, last-write-wins** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `receipt.json`'s `commands` field is a dict keyed by name, so a second command with the same name overwrites the first's result even though the console shows both ran. This should already be caught in Phase B; re-verify against the actual invoked set before trusting an unexpectedly-short result list.
4. **Self-diagnose rather than assume the solver ran.** Whenever a result looks suspiciously clean ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â instant `UNSAT`, no meaningful search time ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm the solvers actually executed:
   ```bash
   alloy -D debug exec -s electrod.nuxmv -t json -f -o <output-dir> <file>.als 2>&1 | grep -i "kodkod.solvers.api.NativeCode"
   ```
   A hit naming both `electrod` and `nuXmv` binaries confirms a real check happened. No hit means the result is not evidence of anything, and a temporal model's `UNSAT` without this check might mean "proved" or might mean "the bounded search couldn't even construct a trace" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â those are not the same thing and must not be reported as if they were.

**Done when:** every in-scope model has been checked, its verdict parsed from `receipt.json`/stdout (never from exit code), and a suspiciously clean result has been debug-verified.

---

## Phase D ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Interpret the verdict

- **`UNSAT`** (no counterexample to the negated property exists) means the property holds *within the checked scope*. State the scope bound explicitly whenever reporting this ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an `UNSAT` at an insufficient scope is not a proof, and reporting it as one overclaims what was actually checked.
- **`SAT` with a witness** means a genuine counterexample was found. This is the fork into Phase E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't stop at "SAT", carry the witness forward, since it's the concrete trace that will make the code-side location in Phase E precise instead of a guess. **Read the rendered counterexample itself, not just the verdict** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a witness can be technically SAT for reasons that don't point at anything actionable, e.g. an underspecified relation the solver filled in arbitrarily to satisfy the model rather than because the property is genuinely violated. `references/alloy-harness.md` covers how to phrase assertions so a real counterexample names the specific violating atom instead of just proving existence.
- **Ambiguous or error output** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â report exactly what was parsed and stop. Never guess a verdict from partial output; an unparseable result is itself the finding.

**Done when:** every checked model has a stated verdict (UNSAT-with-scope, SAT-with-witness, or ambiguous-and-reported), never an assumed one.

---

## Phase E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Locate in code (only on a genuine counterexample)

This phase locates, it does not judge. Whether the counterexample means the *code* is wrong or the *spec* is wrong is a divergence-judgment question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that's `weed`'s job, not this skill's. Report which side moved; never assume it's the code just because that's the more common case.

Hand off the search itself rather than reasoning about code structure inline:

- **Structural pattern location** (does this code shape exist, where) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `ast-grep`.
- **Semantic/symbol-level location** (call graphs, references, especially Scala) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `serena`.
- **The comparison itself** (is this actually a spec-vs-code divergence, and which side is authoritative) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the **`weed`** skill directly with the witness as context, rather than re-deriving its judgment here.

**Done when:** the witness has either been located in code via ast-grep/serena and handed to `weed` for judgment, or explicitly reported as not-yet-located with a stated reason (e.g., scope didn't include a codebase search).

---

## Phase F ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Loop or report

If Phase E's handoff comes back with a fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â to the spec or to the code ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and the user wants to confirm the fix actually closes the gap, loop back to Phase B for just the changed obligation, not a full re-run of everything in scope. This is the point of framing this as a loop rather than a one-shot check: a fix is not confirmed until the same model that found the counterexample now returns `UNSAT` against it.

Otherwise, report:

- Every spec/obligation checked, its scope bound, and its verdict ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â including a stated non-finding for everything that came back clean. A verdict that isn't stated reads as "not checked," not as "fine."
- Any genuine counterexample: its witness, and where Phase E located it (or that it wasn't located, and why).
- Whether a suspiciously-clean result was debug-verified (Phase C gotcha 4). Never claim a check happened without saying so.

**Done when:** the user has a verdict for everything named in Phase A's scope, with no silently-skipped obligations.

---

## Anti-patterns

- Gating success/failure on `alloy exec`'s process exit code ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's 0 for everything except an actual syntax error
- Trusting `receipt.json`'s `values` field off-scope without knowing whether the solver in use is one of the ones that corrupts it
- Running one Alloy process per spec file instead of batching the checked set
- Checking one Allium spec file in isolation instead of the whole dependent set together
- Parsing multi-file `allium check` output as a single JSON document instead of concatenated objects
- Reporting an `UNSAT` as a proof without stating the scope bound it was checked at
- Treating an instant, suspiciously-clean result as a verdict without debug-log verification
- Trusting a SAT witness at face value without checking whether it names a real violation or an arbitrarily-filled underspecified relation
- Re-implementing spec-vs-code divergence judgment here instead of handing off to `weed`
- Reasoning about code structure from memory instead of using `ast-grep`/`serena`
- Assuming a `use` import brought in a value type the Alloy model needs
- Silently encoding an untyped trigger parameter or unused ref into the model instead of flagging it
- Skipping the Witness-rule check when a modeled property depends on reaching or leaving a status value
