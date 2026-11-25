---
name: develop-debug
description: "A cross-stack debugging playbook. The techniques here are language- and platform-agnostic: they apply equally to a C++ optimization engine, a TypeScript/NestJS backend, a Python service, and a Terraform/Kubernetes deployment. The principle in each section is what generalizes; ..."
---
# Debugging Playbook

## Purpose and Scope

A cross-stack debugging playbook. The techniques here are language- and platform-agnostic: they apply equally to a C++ optimization engine, a TypeScript/NestJS backend, a Python service, and a Terraform/Kubernetes deployment. The principle in each section is what generalizes; the concrete commands, status codes, and incidents are illustrative examples of that principle, drawn from whatever stack happened to surface it.

Two reading notes:

- **Examples are interchangeable, principles are not.** When a section uses CP-SAT, CloudWatch, Docker, or `psql`, read past the specific tool to the underlying move (read a status before theorizing, diff two environments literally, trust a work-unit metric over wall time). Substitute your own stack's equivalent.
- **A few sections only apply to a sub-domain.** Bounded-engine status codes and perturbation-sensitive stages apply when a solver, planner, query optimizer, type checker, or scheduler sits in your pipeline. The "Concrete Patterns" appendix is mostly backend/cloud worked examples. Skip what your system does not contain.

Throughout, **bounded engine** is the umbrella term for any component that searches for an answer under a time/work budget rather than running to a proven optimum: constraint/SAT/SMT solvers, query planners, schedulers, packers, layout heuristics, and type-inference engines all behave this way. Stack-specific names (CP-SAT, the query planner) are examples of a bounded engine.

## General Approach

1. **Reproduce the failure deterministically before doing anything else.** If the failure is intermittent, the next sections (bisection, state-dependent failures) apply. If it is reproducible, the rest of this skill applies more directly.
2. **Get the high-level picture first.** Use whatever observability tooling is available (dashboards, metrics, log aggregations) before diving into individual log entries or code.
3. **Verify metrics before trusting them.** Aggregated averages (`avg_ms`, p95) can be inflated by a single outlier. Pull raw entries for individual data points.
4. **Distinguish pipeline latency from handler latency** (auth middleware, request guards vs. DB query, external call, cache miss) before looking at code.
5. **When a downstream service is involved, check that service's own logs.** The visible error is often just a propagated symptom.
6. **Get the full log entry, not just the status code or error message.** Structured logs usually include the exception type, message, and stack frame where the error was thrown, not where it was caught. The top frame in the stack trace identifies the throwing site.
7. **Cross-reference timestamps** with recent deployments, config changes, dependency updates, image rebuilds.

## Verify the End State, Not the Fix's Local Effect

A change that demonstrably does its narrow job is **not** the same as the system now succeeding. After a fix, confirm two separate things: the immediate effect (the value moved, the metric dropped, the entity relocated, the constraint is now satisfied) AND that re-running reaches the actual terminal outcome you wanted.

The most seductive failure mode is a fix that works locally and merely **moves the problem** to a different layer or a later stage. You see the green local signal, conclude you are done, and the system fails somewhere new - often in a way that looks unrelated, so the next person (or you, an hour later) re-debugs it from scratch. Each "worked locally, failed globally" costs a full cycle: a change that satisfies its immediate objective while leaving a downstream consumer blocked, or one that makes a stage's target reachable while over-constraining a different stage into failure.

> Example (multi-stage pipeline): a packing-objective change made two endpoints adjacent (its job) while the route between them stayed blocked; separately, an interface change made a terminal reachable (its job) while over-constraining a different stage into infeasibility. Both did their narrow job and both moved the failure downstream.

Rule: run to the real end state every time, even when the local signal is unambiguous. "The thing I changed now reads the value I intended" is a checkpoint, not a conclusion. Only "the pipeline/request/job produced the correct final output" is a conclusion.

A specific and seductive variant: **a fix that resolves a conflict by GROUPING the conflicting items often recreates the same conflict one level up, among the groups.** If the bug is "N items processed sequentially each block the next" and the fix is "process items in batches together," verify that the BATCHES do not then block each other the same way - because if they are still processed sequentially, you have only changed the granularity of the identical bug, not removed it. The same shape recurs across domains: lock granularity (per-row locks that contend become per-page locks that still contend), retry batching, transaction grouping, and shard/partition boundaries. After any "group them to avoid the interaction" fix, ask: do the groups still interact the same way? Run to the end state to find out, because the local signal (within-group conflict gone) will look like success.

> Example: a per-item sequential-walling bug (each routed item became an obstacle for the next) was fixed by batching items that share a target and solving each batch jointly. That fixed within-batch walling but left the batches themselves solved sequentially, so the batches walled each other and the original failure reappeared one level up - the granularity of the bug had changed, not the bug.

## Bisection Over Reasoning

When you have N plausible causes for a failure, **verify the cheapest one to rule out, not the most likely one**.

Every minute spent reasoning about plausibility ("this is probably an auth issue because the error mentions tokens") is a minute not spent eliminating a candidate. Reasoning is biased by recency, by the loudest part of the stack trace, by your familiarity with one subsystem. Verification is not.

Cheap eliminations are usually:

- Read a config or credential file directly and compare its contents to a known-good version.
- Diff two log outputs literally.
- Check a version number (`<binary> --version`) against an expected one.
- `docker inspect`, `ls -la`, `cat`, `git log -1 -- path/to/file`.
- A single SQL query against the actual table.

Expensive paths are usually:

- Restructuring code to "fix" a hypothesized class of bug.
- Restarting services or rebuilding images "to see if it changes anything."
- Reading source code to reason about what _should_ happen.

If a cheap check would falsify the hypothesis you are about to spend an hour on, do the cheap check first. **A hypothesis with no verification is a guess.**

This applies with most force to a diagnosis you have already grown confident in, not just the opening list of candidates. The cheap discriminating check is most valuable precisely when you feel sure, because that is when you are about to commit the next phase of work to it. Before designing a fix premised on "X causes Y," confirm X with one tool call - a confident-but-wrong diagnosis is more expensive than an admitted unknown, because it silently steers the entire next phase down the wrong path. Treat your own latest conclusion as a hypothesis to falsify, not a fact to build on.

> Example: a confident mid-investigation conclusion ("my change grew the bounding box, which flipped the downstream layout") was about to drive an hour-long fix. One instrumented print showed the bounding box was byte-identical in both versions; the real cause was a different mechanism entirely. The cheap check fired exactly when confidence was highest.

## Pressure-Test a Diagnosis With an Adversary Before Spending On It

A second model (or a fresh session) that cannot see your tool results is a pure reasoning adversary - it reasons only from what you tell it, so it cannot inherit your confirmation bias or your attachment to the diagnosis you have been building. Use it at decision forks before committing expensive work: a fix design, a diagnosis you are about to build on, a constraint you are about to relax, a knob you are about to turn.

How to use it well:

- Frame the fork with the concrete options and your current lean, paste the VERIFIED facts (it cannot see them otherwise - it has no access to your logs, dumps, or source), and ask for the single strongest argument you are wrong. Tell it explicitly NOT to restate your framing, or it will burn the exchange agreeing with you.
- It is an adversary for REASONING, never a source of FACTS. It cannot run the build, read a status code, or see a dump. Re-verify every source/run/status claim it makes against the actual system - it can be confidently wrong (in one instance a partner endorsed a "forbid rotation" fix that a single tool call disproved).
- Its highest value is catching OVERCLAIMED SCOPE ("this change is safe everywhere" when it is safe only in some cases) and naming a failure mode you did not consider - not confirming what you already believe.

Representative catches (the kind of thing an adversary surfaces that you, attached to the diagnosis, will not): an optimization that was safe for the sequential case but UNSAFE for the simultaneous case; a knob believed to control feasibility that actually only controlled search speed; and a fixation on preserving "byte-identical output" when the invariant that actually mattered was the weaker "no validation regression."

- Reuse one persistent adversary session across the investigation so it accumulates context cheaply, rather than re-onboarding a fresh one each fork.

## Symptom Layer vs Cause Layer

Errors propagate up; causes live down. The visible error text typically describes the reaction at the layer where the failure surfaced, not the behavior at the layer that originated it.

Generic layer model. Every system is a stack of these whether it is a web backend, a CLI tool, a compute pipeline, or an infrastructure deployment - the labels differ but the propagation rule does not:

```
Layer 7  Entry point        (client / UI / CLI invocation / API request / job trigger)
Layer 6  Request handling    (controller / command parser / pipeline stage / IaC plan)
Layer 5  Domain logic        (business rules / algorithm / orchestration)
Layer 4  Data / dependency   (ORM / data access / client library / SDK / module loader)
Layer 3  External resource   (database / external API / message queue / cloud provider API)
Layer 2  Runtime             (language VM / interpreter / compiled binary / container image)
Layer 1  System              (filesystem / OS / network / container sandbox)
Layer 0  Hardware / infra    (host / cloud provider / scheduler)
```

When you get an error at layer N, the cause is usually 1-3 layers below it. The error at layer N describes how N reacted to a bad input from N-1, N-2, or N-3, not what N-2 actually did.

Examples of the gap (each from a different stack, all the same shape):

- **500 from an API handler** (L6) often means an unhandled exception from a service call (L5) caused by an ORM mapping error (L4) caused by a missing DB column (L3).
- **`UnknownError` from a runtime** (L2) often means provider initialization failed because of a malformed config file (L1) that was provisioned wrong.
- **A compiled tool crashing at startup** (L2) often means it loaded a config or plugin (L4) built against an incompatible SDK version (L3/L1 mismatch).
- **A Terraform apply failing on a resource** (L6) often means the provider API (L3) rejected state that a prior plan (L5) computed from drifted remote state (L0).
- **High p95 latency** observed at L6 often means connection pool exhaustion at L4 caused by a slow upstream API at L3.

When debugging, ask: "what layer is _this error message_ really describing?" then look one to three layers below it.

## State-Dependent Failures ("Worked Once, Fails Now")

If a system worked then stopped working without a code change, **something is being mutated between runs**. The investigation question is "what is recreated on every run vs what persists?"

Common sources of inter-run state mutation:

- **Credential stores** that get re-provisioned on every run (auth tokens, OAuth refresh, secrets injected by an orchestrator).
- **Caches** that are populated by the first successful run and invalidated by something later.
- **Ephemeral file mounts** that are rewritten by a provisioning step.
- **Database rows** that are upserted by a startup activity (registry tables, seed data).
- **Container volumes** that survive across container restarts while the binary in the container itself does not.
- **Background processes** that hold a lock or a port until they die.
- **Connection pools** that accumulate stale connections after a database failover.

Diagnostic procedure:

1. Find the boundary between "last known working run" and "first failing run."
2. List every artifact that was touched between those two runs: which files were rewritten, which DB rows were updated, which services were restarted, which credentials were refreshed.
3. For each, ask: "if this artifact's previous state was preserved, would the failure still occur?"
4. The artifact that would unblock the system if reverted is the one being mutated incorrectly.

**Critical insight:** intermittent success is not noise. The successful run had a state the failing runs do not. Find the delta. The "fluke" run is often the most informative one in the entire investigation.

## Comparison Diagnostics ("Works Here, Fails There")

When the same code works in environment A and fails in environment B, **the question is not "why does A work" but "what state does B have that A does not."** The first framing leads to plausibility reasoning. The second admits a finite checklist.

Things to literally diff between the two environments (in order from cheapest to most expensive):

1. **Versions** - of every binary, every dependency, every base image, every CLI tool involved. Pin matching versions; do not assume "1.2.3 in both places" means identical builds (distributions, forks, and bundled chunks differ).
2. **Configuration files** - byte-for-byte. Do not summarize; diff. A one-line difference invisible to "the files look similar" is the most common cause of "works here, fails there."
3. **Environment variables** - the actual set the process sees, not the documented set.
4. **Filesystem mounts** - what is mounted where, what is read-only, what is bind-mounted vs volume-mounted, what is overlaid on top of what.
5. **Network reachability** - DNS resolution, firewall rules, TLS validation paths.
6. **OS / kernel / arch** - especially when bundled binaries (Bun, Go, Rust) cross OS boundaries; the same version number can be a different build per platform.
7. **Persistent state** - DBs, named volumes, caches. Empty in B but populated in A is a different system, not the same system.

Concrete diff techniques:

- `diff <(env)` between host and container, sorted.
- `docker inspect <container> --format='{{range .Mounts}}{{.Source}} -> {{.Destination}} {{.Mode}}{{println ""}}{{end}}'` for mount comparison.
- `python3 -c "import json; print(sorted(json.load(open('file.json')).keys()))"` to compare config-key sets.
- `md5sum <binary>` on both sides to confirm whether two "same version" binaries are actually identical builds.

## Perturbation-Sensitive Stages ("My Unrelated Change Broke Something Downstream")

When a stage is a **bounded engine** (solver, query planner, scheduler, packer, layout heuristic, type-inference pass) that is **time-bounded rather than run to optimality** - it returns the best feasible answer at a budget, not the proven optimum - a small, legal, correct change upstream can flip its entire output. Not because your change is wrong, but because the bounded search lands on a different equal-validity result, and the new result happens to break a later stage.

This shares the surface symptom of state-dependent failures ("it worked, then a change broke it") but the root is different: nothing was mutated between runs; the stage is a deterministic function of its input that is **chaotically sensitive** to that input because it stops at a budget instead of an optimum.

Diagnostic procedure:

1. Identify whether the downstream stage proves optimality. Look for a status flag and whether it hit its time/work cap. A status of `FEASIBLE` (not `OPTIMAL`) together with elapsed time equal to the cap means it returned an arbitrary good-enough answer, not the best one.
2. Confirm your change is logically irrelevant to the failure by checking that the stage's actual inputs (the constraint set, the cost matrix, the input geometry) are unchanged - instrument them if no log exposes them (see Instrument When No Observation Point Exists). Identical inputs plus different output across two builds is search roulette, not a logic bug you introduced.
3. Once confirmed, stop trying to make your upstream change "not perturb" the stage - that is chasing noise, since any legal change can reshuffle a capped search. Fix the fragility at its source: make the stage stable (raise the cap toward optimality if reachable, or bias its objective so the answer you need wins) or make the next stage tolerate any valid output of it.

Critical framing: "make my change output-neutral" is the wrong goal when the engine is capped - even a one-element change can flip it. The defensible goals are "make the stage deterministic/optimal" or "make downstream robust to any valid output," not "tiptoe around the roulette."

> Example (CP-SAT packing stage): an upstream change that grew a packing objective flipped a capped packer's layout, which broke a later routing stage. The change was legal and the packer's inputs were byte-identical across both builds - the flip was search roulette, not a logic bug. Chasing "make my change packing-neutral" was the wrong goal; the fix was to stabilize the packer or make routing tolerant of any valid packing.

## Bounded-Engine Status Codes

When a stage is a bounded engine (constraint/SAT/SMT solver, query planner, type checker, scheduler), the **failure mode it reports dictates the fix**, and two fast failures can mean opposite things. Read the status before theorizing.

- **Proof of impossibility** (CP-SAT `INFEASIBLE`, an UNSAT core, a type-checker "no instance matches", a planner "no valid join order") - the engine proved no solution exists for that exact model. It returns fast precisely because it is a proof. More time, more workers, a bigger budget will NEVER help. The fix is upstream: relax a constraint, reorder, or change the inputs that made it impossible.
- **Budget exhaustion** (CP-SAT `UNKNOWN`/status 0, a solver timeout, "search limit reached") - the engine ran out of time/work units without finding or disproving a solution. This is a model-SIZE problem: shrink the model, tighten the search window, or raise the budget. It is NOT a proof of anything.

The trap: both can surface as a fast non-success, and treating one as the other wastes hours. An impossibility-proof returned in milliseconds is a proof, not a slow run - do not throw budget at it. A timeout is not an impossibility - do not start relaxing constraints that were never the problem. Find the status field first; it is usually a single integer or enum on the engine's response.

**A budget-exhaustion conclusion is only valid if the work-unit counter actually reached the cap - capture it.** "The solver returned UNKNOWN so the model is too big" is a guess unless you logged the deterministic-time/work value at the moment of failure and it is at (or near) the configured limit. A solve that returns UNKNOWN at a LOW work count was not budget-exhausted - it was paused, killed externally, or interrupted (see Distinguish a Real Performance Problem From a Measurement Artifact). Many engine wrappers log work-unit/time on SUCCESS only; if yours does, add the same fields to the FAILURE path before trusting any "too big" conclusion - otherwise a throttled or killed run is indistinguishable from a genuine budget wall, and you will "fix" a model size that was never the problem.

**Classify the knob before you turn it: feasibility-affecting or performance-affecting.** Before reaching for a parameter to fix an engine failure, decide whether it changes whether a solution EXISTS (a constraint, the geometry, the model inputs) or only how fast / which one the search FINDS (time/work budget, worker count, search-window shape, variable/constraint ordering, restart strategy). A performance knob cannot fix a feasibility wall (`INFEASIBLE`) - if a full-strength fallback exists (e.g. the search always tries the full window before giving up), then a knob that only reshapes the search provably cannot turn an infeasible case feasible, only change its speed. Conversely, relaxing a real constraint to "fix" a timeout relaxes something that was never the blocker. Match the knob's class to the failure's class.

> Example: a search-window knob was believed necessary for a stage to SUCCEED, when in fact it only governed how fast that stage searched - the stage was feasible either way. The knob was performance-affecting, not feasibility-affecting, so turning it could never have fixed a feasibility wall.

## Separate the Cost of FINDING an Answer From the Cost of PROVING It Optimal

When a bounded engine is slow but eventually succeeds, ask which of two very different costs you are paying, because they have opposite fixes and the wrong one wastes the whole investigation:

- **Finding a feasible answer** - the search for any valid solution that satisfies the constraints.
- **Proving it optimal** - closing the gap between the best solution found and the lower bound, to certify nothing better exists.

For many engines (constraint/SAT/MILP solvers, schedulers, planners) the optimality PROOF dominates wall time: a valid answer appears quickly, then the engine spends most of its budget proving minimality. If your consumer only needs a VALID result - the validator checks correctness, not minimality; the layout must be legal, not shortest; the schedule must be conflict-free, not cost-minimal - then the proof is pure waste, and the fix is to tell the engine to stop at the first feasible solution (CP-SAT `stop_after_first_solution`, a MILP gap tolerance / `SolutionLimit`, "satisfy" vs "optimize" mode). This can turn minutes into seconds with no model change.

But confirm which cost you are paying before reaching for that switch, because stopping at first-feasible does NOTHING when FINDING any solution is itself the hard part. A large multi-commodity / disjoint-paths / bin-packing instance can fail to produce even a first feasible point within budget (status UNKNOWN at the cap) - there, the bottleneck is the search, not the proof, and the fix is to shrink the instance (decompose into smaller independent sub-problems, tighten the domain) so a feasible point is reachable at all. The discriminating observation: does the engine report a feasible incumbent early and then grind (proof-bound - stop early), or does it never report one (search-bound - decompose)? Read the incumbent/bound log, do not guess.

The two fixes COMBINE and that is usually the win: decompose so each sub-problem's find-feasible is cheap, AND stop each at first-feasible so no sub-problem pays for a proof nobody needs.

> Example: routing N nets jointly was slow; the instinct was "shrink the model." But the model size was a red herring - the solver found a valid routing fast and then spent all its budget proving it minimal, which the validator did not require. Switching to first-feasible collapsed a 96-second solve to 9 seconds with no model change. Separately, the single all-nets joint solve never found a first feasible point even with first-feasible enabled, because for that instance FINDING was the hard part; the fix there was to decompose into small per-target batches, each of which finds-and-stops in seconds. The combination - decompose plus first-feasible per batch - was what worked.

## A Smaller or More-Constrained Model Is Not Always Easier to Solve

The intuition "fewer variables / a tighter feasible region = faster solve" is often FALSE for a search-based engine, and acting on it can make the problem dramatically harder. A constraint that removes slack can remove exactly the maneuvering room the search relied on to find a feasible point quickly: the variable count drops, yet the instance becomes harder or infeasible because the easy solutions were in the space you just blocked.

This is the inverse of the previous section's trap - there, the goal was to shrink the model so a feasible point is reachable; here, the warning is that a particular WAY of shrinking it (adding hard constraints, walling off regions, tightening a domain too far) can backfire. Decomposition into independent sub-problems makes finding easier; over-constraining a single problem makes it harder. They are not the same move. Measure the actual find-feasible time and status after any "this should make it simpler" change rather than assuming the smaller model is the faster one.

> Example: blocking off large regions of a routing grid to "force structure and reduce variables" did cut the variable count, but a sub-problem that previously found a valid routing in seconds then ran for minutes without one - the solid regions had removed the open space the solver used to maneuver. Fewer variables, far harder instance.

## Escalating Fix Complexity Is a Signal the Premise Is Wrong

When each fix attempt is more elaborate than the last - a tweak, then a new mechanism, then a redesign of an upstream stage, then a redesign of two - treat the escalation itself as evidence that the underlying premise is wrong, not that the problem is merely hard. A correct diagnosis usually makes the fix SIMPLER as understanding sharpens; a wrong diagnosis makes each fix bigger because every patch is compensating for the unexamined false assumption beneath it.

When you notice the complexity ratchet, stop adding machinery and re-examine the assumption every attempt has shared. Often a stakeholder's offhand "this shouldn't be so hard" is the correct signal: the simple solution exists and is being blocked by a premise no one has questioned. Go back to the cheapest version of the problem and ask what would have to be true for the simple fix to work - frequently the elaborate machinery was solving a problem created by an earlier wrong turn, and removing that turn dissolves the need for all of it.

> Example: a routing slowness drove an escalating chain - tune a budget, then add domain bands, then block group footprints, then move interface slots, then carve reach-channels, each fix larger and spawning its own failures. The premise underneath all of them ("the open layout causes the slowness") was wrong; the open layout was helping. The actual fix was a one-line solver flag (stop at first feasible) plus reverting to small batches, and every piece of the elaborate machinery was discarded. The escalation was the tell.

## Regression Attribution Against a Reverted Baseline

Before claiming a failure is a regression you introduced - or that it is pre-existing and "not mine" - prove it in the same environment. Cross-environment diffing (see Comparison Diagnostics) answers "works here, fails there"; this answers "did MY change cause this."

Procedure:

1. **Save your uncommitted work before reverting.** `git stash` is recoverable. But `git checkout <baseline-ref> -- <files>` OVERWRITES the working tree destructively - if you use that form to swap in the baseline, you will lose any uncommitted change that is not stashed or committed first. Commit a checkpoint (even a throwaway `wip:` commit) or copy the files somewhere safe before reverting. This is a real, costly footgun: it can silently destroy an entire uncommitted implementation, forcing a reconstruction from memory.
2. Rebuild, and run the **single failing case** on the clean baseline.
3. If baseline is green and your change is red on the same case, the regression is yours. If baseline is also red, it is pre-existing and your change merely surfaced or moved it.
4. Capture a discriminating quantity in both runs, not just pass/fail, when the failure is about magnitude (a variable count, a grid size, a row count, a latency). "Baseline produced 36k variables for this route; my change produced 91k" is the attribution evidence and also points at the mechanism.

**Do not attribute a bundle of changes as a unit.** When several changes are committed together or made in one multi-file edit, isolate each against the symptom individually - revert one, keep the others, re-run - before concluding the bundle is the cause. A bundle can contain both the regressor AND an unrelated improvement; reverting it wholesale throws away the good change with the bad.

> Example: a two-change bundle regressed one fixture. Isolating the changes showed one was the regressor while the other was independently helping a different fixture, so a wholesale revert would have discarded a genuine improvement.

State the distinction explicitly in any report. A "regression" that is red on baseline too is not yours to fix under the current task, and conflating the two sends effort at the wrong target.

## Read the Actual Stack Trace Before Theorizing

For any non-trivial failure, the stack trace is usually more informative than the error message text. **Find the stack trace, even if the tool tries to hide it.**

Common ways tools hide stack traces:

- Default log level is `INFO` or `WARN`. The stack lives at `ERROR` or `DEBUG`.
- The default error renderer prints a generic message (`UnknownError`, `Internal Server Error`) and stashes the stack in a structured log field (`responseBody.stack`, `error.cause`, `effect.failures`).
- Bundled or transpiled binaries (Bun standalone, webpack output, native compilations) emit stack frames like `chunk-48ktgwjs.js:667:56894`. The file/line numbers drift per build and are not directly useful, but the **symbol names** in the trace (`SessionPrompt.getModel`, `Provider.init`) are stable across builds and map to source semantics.

Procedure for getting at the real trace:

1. Look for a verbose / debug / log-level flag on the tool itself (`--verbose`, `--log-level DEBUG`, `--print-logs`).
2. Look for a debug command or subcommand the tool exposes for its own troubleshooting (`<tool> debug ...`).
3. Look for environment variables (`<TOOL>_LOG_LEVEL`, `DEBUG=*`, `RUST_BACKTRACE=full`).
4. If the failure happens behind a wrapper (CI runner, container exec, orchestrator), run the underlying command directly with verbose flags. The wrapper often swallows useful output.
5. Once you have the trace, extract **symbol names**, not line numbers. Search the codebase or distribution for those symbols.

Heuristic: if the error message is a single line and ends with `ref:err_xxxxxx` or `id:xxx-xxx-xxx`, there is almost always a richer error somewhere - the ref is opaque on purpose because the tool wants the human to go find the structured log entry.

## Instrument When No Observation Point Exists

"Observe what does happen rather than read what should happen" assumes a log, trace, or dump already exposes the value you need. Often it does not - the value you must know is an intermediate computed inside a function with no output. Do not fall back to reading the code and arguing about what the value "must be." Add a temporary observation point, capture it, and revert it:

1. Add a temporary print/log of the exact value at the exact site (`spdlog::warn("[SCRATCH] bounds={} {} {} {}", ...)`, a `console.error`, a `print()`), built with an obvious marker like `SCRATCH` so it is easy to find and remove.
2. Build, then run **only far enough** to hit the line - kill the run once the value is captured. For an expensive pipeline, instrument an early stage so you do not pay for the whole run.
3. Revert the probe immediately. A compiled binary or a long-lived process keeps its loaded image after you delete the source line, so you can remove the instrumentation right away and keep the working tree clean while the captured output remains valid.

This settles "does this value actually change / what is it really" in one run, where pure reading would leave it an unverified assumption. It is the observation tool for values the system does not already surface. (This is also the cheap discriminating check for a confident mid-investigation diagnosis - see Bisection Over Reasoning.)

## Distinguish a Real Performance Problem From a Measurement Artifact

Before investing in a performance investigation, confirm the slowness is real and not an artifact of an uncontrolled measurement environment. Wall-clock time is only trustworthy when nothing outside the code under test is distorting it. Three things silently inflate wall time with no code being slow: the host sleeping/suspending mid-run (a laptop idle-sleeping between your polls), CPU contention from your own overlapping background runs, and thermal throttling.

The decisive signal: when the operation reports a WORK-UNIT metric (a solver's deterministic time, instructions retired, rows scanned, bytes processed, GC-adjusted CPU time) AND that metric diverges wildly from wall time, the wall measurement is corrupted, not the code.

Rules:

- Prefer a deterministic/work-unit metric over wall time for any timing judgment. If the operation exposes one (a solver's deterministic time, a query's rows/buffers, an instruction count, CPU-seconds), use it - it is reproducible across machines and immune to host pauses. Wall time is the fallback, not the default.
- Pin the environment for any run whose timing you will trust: prevent sleep (`caffeinate -i` on macOS, `systemd-inhibit --what=idle:sleep` on Linux, an active power plan on Windows), run ONE thing at a time (do not benchmark while other heavy runs contend for the same cores), and sanity-check that the process's CPU-time (`ps`, `/usr/bin/time`, a profiler) is in the same ballpark as elapsed wall time.
- A low work-unit count at a high wall time means the run was paused/contended/killed, not that the code is slow. Re-run pinned before concluding anything about performance - a performance investigation built on a corrupted measurement is pure waste.

> Example: hours were burned chasing "46-minute" and "695-second" solves that, read by their deterministic-time counter, had done seconds of actual work - the laptop was asleep between polls (`ps` showed ~4 min CPU over ~33 min wall; one solve logged `time=302.95s det=3.56`). Every performance conclusion drawn from wall time in that state was wrong, and the "too slow" diagnosis that drove a delicate optimization was never real.

## Debugging Under Expensive Feedback Loops

The default playbook assumes fast feedback - you can re-run freely, restart a service, retry a request in seconds. When a single run is expensive (a long solve, a large build, a pipeline that takes tens of minutes to over an hour, a slow integration suite), the strategy inverts: speculative re-runs are forbidden, so the cost of a wrong hypothesis is enormous. Adapt:

- **Front-load every cheap discriminating check before you spend a run.** Read the dumps, instrument the inputs, compute the arithmetic by hand, pressure-test the design - exhaust the seconds-cost checks before paying the hour-cost run. One wasted long run can cost more than a day of cheap checks.
- **Fail fast on the earliest signal.** A long pipeline writes intermediate artifacts; check the earliest one that would falsify your fix instead of waiting for the final result. (Example: an early-stage dump confirmed in 90 seconds that a fix took effect, versus ~60 minutes to reach the stage that consumes it; a separate run was killed the instant an early stage proved the design wrong, rather than letting it run to the end.)
- **Detach and poll; never block on the run.** Launch long runs in the background (`nohup ... > out.log 2>&1 &`) and poll the log in separate short commands. A foreground run dies when the command times out or the host sleeps; a detached one survives both (it pauses on sleep, not dies). Note `timeout`/`gtimeout` is not present on macOS by default - wrapping a launch in it silently fails to start the process.
- **Clear stale artifacts before each run** so a prior run's outputs are not misread as the current run's. Hash or strip volatile prefixes (timestamps) before comparing two runs' outputs for equality.

## Tools to Know

Cross-stack debugging toolkit. These are example commands per category; substitute your stack's equivalent (the category is what generalizes, not the specific binary). Reach for these before writing code.

| Need                                     | Example tools                                                   |
| ---------------------------------------- | --------------------------------------------------------------- |
| Compare two text files                   | `diff`, `comm`, `git diff --no-index`                           |
| Inspect a JSON/YAML config               | `jq`, `yq`, `python3 -c 'import json; ...'`                     |
| Compare two binaries                     | `md5sum`, `shasum`, `file`, `strings`                           |
| Inspect a container's mounts and env     | `docker inspect`, `docker exec ... env`, `kubectl describe`     |
| Inspect a running process                | `lsof -p <pid>`, `ps aux` piped to `grep`, `pgrep -af`          |
| Inspect what is listening on a port      | `lsof -nP -iTCP:<port> -sTCP:LISTEN`, `ss -tlnp`                |
| Trace system calls                       | `strace` (Linux), `dtruss` (macOS), `ltrace`                    |
| Profile CPU / find a hot path            | `perf`, `py-spy`, `pprof`, a language profiler                  |
| Inspect HTTP requests/responses          | `curl -v`, `mitmproxy`, `tcpdump`                               |
| Inspect SQLite DBs                       | `sqlite3 <path> ".tables"`, `.schema <table>`                   |
| Inspect Postgres                         | `psql`, `EXPLAIN (ANALYZE, BUFFERS)`                            |
| Decode an opaque token                   | `jwt.io` for JWTs; `base64 -d` for everything else              |
| Search a bundled binary for symbol names | `strings <binary>` piped to `grep -i <symbol>`, `nm`, `objdump` |
| Inspect a native core dump / backtrace   | `gdb`, `lldb`, `bt full`                                        |
| Inspect infra/cloud state                | `terraform plan`, `terraform state show`, provider CLIs         |
| Watch a log file as it grows             | `tail -F`, `less +F`, `kubectl logs -f`                         |

## Concrete Patterns

The following are concrete pattern instantiations of the universal techniques above. Treat them as worked examples; the technique is what generalizes.

### Misleading Metrics - Aggregated Averages

**Pattern:** Dashboard shows high avg response time (e.g. 1,000-15,000ms) for an endpoint that should be trivial based on its code path.

**Root cause candidates:**

- **Database cold start** - serverless / auto-pausing databases (Aurora Serverless, PlanetScale, etc.) take seconds to wake after idle periods. The first request after a pause absorbs the full cold-start cost, which gets averaged with subsequent fast requests.
- **Single outlier** - one request with an unusual condition (cache miss, lock contention, third-party timeout) skews the average for a large batch of fast requests.
- **Client polling** - a client hammering the same endpoint repeatedly drives up request count, which amplifies the weight of any outliers in the average.

**How to distinguish inflated average from real slowness:**

1. Pull individual raw log entries for the slow endpoint - filter by URL in application logs.
2. Read `responseTime` from each individual entry, not the aggregated avg.
3. If individual values are consistently fast (< 50ms) and only one or two are high, the average is an artifact. Real slowness shows as consistently elevated times across many requests.
4. Check request timestamps - if the first request after a quiet period is slow and all subsequent ones are fast, it is a cold-start issue, not a code bug.

**Observed instance:** `GET /v1/profiles/:id` showed avg_ms 1,150 in CloudWatch dashboard. Individual application log entries showed `responseTime: 9, 9, 12, 13, 11ms`. Aurora Serverless v2 was configured with a 5-minute auto-pause; the dashboard average was inflated by the single post-pause wake-up request.

### Dependency Missing From the Deployed Artifact (Load-Time Failure)

**Principle:** A dependency that exists in source but is absent from the _packaged_ artifact fails at load time, before any of your code runs. This is the general shape behind "works locally, 100% failure when deployed": the build that assembles the deployment artifact (a Docker image, a zip bundle, a static binary, a wheel) did not include something the entry point imports at startup. It is stack-agnostic - Node `Cannot find module`, Python `ModuleNotFoundError` at import, a JVM `NoClassDefFoundError`, a dynamically linked binary failing on a missing `.so`.

**Key characteristics (true regardless of stack):**

- Failure is 100%, not intermittent - every invocation fails identically.
- It happens during initialization (module/import resolution), not inside request/handler logic, so it fires before your first log line.
- Everything sharing the same entry point or packaging step is affected, not just the one place the dependency was added.

**Root cause class:** Any packaging step that _manually enumerates_ what to include (hand-written `COPY` lines, an explicit bundle allowlist, a curated `files` array) will silently omit anything added after that list was last maintained.

**Worked example (AWS Lambda + monorepo Docker image):** A Lambda showed a near-100% error rate with:

```
ImportModuleError: Error: Cannot find module '<package-name>'
Require stack:
- /var/task/apps/lambda-<name>/dist/main.js
```

The entry point (`instrument.ts`) imported the module as its first statement, before any handler code. The package existed in source but the Lambda Dockerfile enumerated `COPY` lines per workspace package and never listed the newly added one. Fix - add the missing package's compiled output to the production stage, then audit every other Lambda sharing the entry-point pattern for the same omission:

```dockerfile
COPY --from=builder /app/packages/<name>/dist ${LAMBDA_TASK_ROOT}/packages/<name>/dist
COPY --from=builder /app/packages/<name>/package.json ${LAMBDA_TASK_ROOT}/packages/<name>/
```

Concretely: adding `@workspace/telemetry` to all Lambda entry points without updating the Dockerfiles caused `lambda-subscriptions` to fail 65/67 invocations (97%) and `lambda-routine-builder` to fail 1/1, surfacing as a `POST /v1/routines/generate` 500 in the API.

### Container Runtime Failures (Worker Exits Clean, No Output)

**Pattern:** An agent / worker / job runs inside a container and exits cleanly (exit code 0) within seconds, but produces no expected output. No error message, no obvious failure.

**Root cause candidates** (in cheapest-to-verify order):

- **Credential or config file in the container is the wrong shape** (missing fields, extra fields that the runtime rejects, expired tokens) - the runtime fails during startup and short-circuits.
- **Bind-mount is read-only** when the runtime expects to write (OAuth refresh, session DB, cache file). Symptom: runtime exits silently because its first write fails.
- **Version mismatch** between a bundled runtime in the container and the configuration it loads (plugin built against SDK vN, runtime is vN-3).
- **Missing or stale entry** in a persisted DB / cache that the runtime reads at startup and panics on.

**Diagnostic:**

1. `docker exec <container> <binary> <subcommand> --print-logs --log-level ERROR` (or the runtime's equivalent verbose mode) to surface the trace that the wrapper swallowed.
2. `docker inspect <container> --format='{{range .Mounts}}{{.Destination}} {{.Mode}}{{println ""}}{{end}}'` to confirm which paths are read-only.
3. Compare every config/credential file inside the container to the working host equivalent, byte-for-byte.
4. Verify versions of every bundled binary inside the container against the working environment.

### State-Dependent: Credentials Re-Provisioned Per Run

**Pattern:** A worker or job runs successfully once, then starts failing reproducibly even though no code changed. Hand-editing the failing container's state unblocks it, but the next run fails again.

**Root cause:** A provisioning activity (CI step, init container, orchestrator activity, entrypoint script) rewrites the state on every run start. Your hand-edit is clobbered the next time the activity fires.

**Diagnostic:**

1. After the activity runs and the state is clobbered, diff the resulting state against your hand-edited version.
2. Find the code that does the writing (`grep -r 'write\|cp\|provision' ...`).
3. Fix at the source, not in the resulting file. Hand-editing is only useful as a hypothesis test.

### Investigating Slow Endpoints

1. Rule out aggregated average inflation first (see Misleading Metrics).
2. Check whether the endpoint has a cache layer and whether the cache was cold or recently invalidated.
3. Run `EXPLAIN (ANALYZE, BUFFERS)` on the suspected query against a representative dataset. Look for sequential scans on large tables.
4. Verify indexes exist for all `WHERE`, `JOIN`, and `ORDER BY` columns in the query.
5. Look for N+1 patterns - ORM calls inside loops, or eagerly loaded relations on list endpoints.
6. Check whether the slowness correlates with request spikes - connection pool exhaustion under load looks like slow queries but is actually queueing time.

### Database Investigation

- Query a shared deployed database (dev, staging, production) only when the human asked for an investigation of that environment or approved the query; read-only does not lift this. Local and per-test databases need no approval.
- Send a lightweight query (`SELECT 1`) first if the database may be auto-paused - avoids a timeout on the first real query.
- Inspect the schema for existing indexes before concluding one is missing.
- Run `EXPLAIN (ANALYZE, BUFFERS)` to get actual execution plans against real data - estimated plans from local empty databases are not representative.
- When row counts look normal but queries are slow, check for bloat, stale statistics, or missing vacuums on heavily updated tables.

### Filtering Structured Logs

**Principle:** When logs are structured (JSON or key-value), filter on fields, not on substring grep. Field filters survive log-format changes and let you slice by status code, latency threshold, endpoint, or level precisely. Every aggregation backend has its own dialect (CloudWatch Logs Insights, GCP Logging, Loki/LogQL, Elasticsearch/Kibana, Datadog, `jq` over a local file) - the queries below are CloudWatch examples; translate the field paths to your own logger's shape.

```
# All 5xx responses
{ $.res.statusCode >= 500 }

# Specific endpoint
{ $.req.url = "/v1/example" }

# Slow requests above a threshold
{ $.responseTime > 2000 }

# Module load failures (substring is acceptable for a known error class)
ImportModuleError

# Error-level entries
{ $.level = "ERROR" }
```

The same five slices in `jq` against a JSON-lines file: `jq 'select(.res.statusCode >= 500)'`, `select(.req.url == "/v1/example")`, `select(.responseTime > 2000)`, `select(.level == "ERROR")`.

## Anti-Patterns

- **Committing to a hypothesis without first verifying the cheapest evidence.** "It is probably X" is a starting point, not a conclusion. Falsify cheaply before investing.
- **Declaring victory on a fix's local effect.** "The value I changed now reads what I intended" is a checkpoint, not a conclusion. A fix that does its narrow job can simply move the failure elsewhere; run to the real end state.
- **Fixing a per-item conflict by grouping items, without checking the groups still conflict.** Batching/grouping the conflicting units to remove their interaction often just recreates the identical interaction one level up among the groups (per-item sequential walling becomes per-batch sequential walling). Verify the groups do not interact the same way.
- **Trusting wall-clock time from an uncontrolled environment.** Host sleep, CPU contention from your own overlapping runs, and thermal throttling inflate wall time with no code being slow. If a work-unit metric (deterministic time, rows scanned, instructions) diverges wildly from wall time, the measurement is corrupted - re-run pinned (`caffeinate -i`, one run at a time) before any performance conclusion.
- **Concluding "model too big" from a solver UNKNOWN without capturing the work-unit count at failure.** UNKNOWN at a low deterministic-time/work value is a paused/killed/interrupted run, not a budget wall. Log the work metric on the failure path; only UNKNOWN at (or near) the cap proves budget exhaustion.
- **Building a fix on a confident mid-investigation diagnosis without falsifying it.** Your own latest conclusion is still a hypothesis; the cheap discriminating check matters most exactly when you feel sure, because that is when you are about to spend the effort.
- **Reading code to guess an internal value instead of instrumenting it.** When no log exposes the value, add a temporary print, capture it in one run, and revert the probe - do not argue from what the value "must be."
- **Assuming your change is logically at fault when a capped bounded engine (solver, planner, scheduler) is downstream.** A time-bounded stage reshuffles its whole output under any legal perturbation; confirm its inputs are unchanged before blaming your change, and do not chase "make my change not perturb it."
- **Confusing a proof-of-impossibility with a budget timeout.** A solver `INFEASIBLE`/UNSAT returns fast because it proved no solution - more time never helps; relax upstream. A timeout means the model is too big - shrink or raise the budget. Opposite fixes.
- **Turning a performance knob at a feasibility wall (or relaxing a constraint at a timeout).** A search-shape/budget knob cannot make an `INFEASIBLE` case feasible when a full-strength fallback already exists; relaxing a real constraint does nothing for a timeout. Classify the knob before turning it.
- **Shrinking the model when the cost is the optimality proof, not the search.** If the engine finds a valid answer fast then grinds proving it minimal - and the consumer only needs a valid answer - the fix is to stop at first-feasible, not to shrink anything. Read the incumbent/bound log to tell a proof-bound solve (stop early) from a search-bound one (decompose).
- **Assuming fewer variables / a tighter region is always faster.** Over-constraining a single search problem can remove the slack the search needed and make finding a feasible point harder or impossible, even as the variable count drops. Decomposing into independent sub-problems makes finding easier; walling off regions of one problem does not. Measure find-feasible time after the change instead of assuming.
- **Ignoring the complexity ratchet.** When each successive fix is more elaborate than the last and spawns its own failures, the shared premise is probably wrong. Stop adding machinery, return to the cheapest version of the problem, and question the assumption every attempt inherited - the simple fix is often being blocked by an earlier wrong turn.
- **Reverting a bundle of changes as a unit for attribution.** A bundle can hold both the regressor and an unrelated improvement; isolate each change individually before concluding, or a wholesale revert discards the good with the bad.
- **Reverting with `git checkout <ref> -- <files>` over uncommitted work.** That form is destructive and unrecoverable; stash, checkpoint-commit, or copy the files first.
- **Building on a confident diagnosis without an adversarial check at the fork.** A second model that cannot see your tool results catches overclaimed scope and unconsidered failure modes that you, attached to the diagnosis, will not - use it before spending the expensive next phase, but re-verify any fact it asserts.
- **Claiming a regression without checking the baseline.** Revert your change, rebuild, run the one failing case on clean baseline. Only green-on-baseline-red-with-change is yours; a failure red on baseline too is pre-existing.
- **Burning an expensive run on an unverified hypothesis.** When a run costs tens of minutes, exhaust every cheap check first and fail-fast on the earliest falsifying artifact instead of waiting for the final result.
- **Treating intermittent success as noise.** A run that worked is the most informative data point in the investigation. Find its state delta against the failing runs.
- **Following a generic error message literally.** "UnknownError," "Internal Server Error," "Something went wrong" describe how the wrapper reacted, not the cause. Find the real trace.
- **Reasoning about why A works instead of finding the state delta against B.** The first leads to plausibility theorizing; the second leads to a finite checklist.
- **Rebuilding, restarting, or redeploying before confirming the change made the failing path different.** Without a hypothesis-driven diff, restarts are just noise.
- **Summarizing two configurations as "basically the same" instead of running a literal diff.** Most "works here, fails there" bugs are a one-line config difference invisible to a summary.
- **Trusting line numbers in stack traces from bundled / minified / transpiled binaries.** They drift per build. Use symbol names, not file:line.
- **Stopping at the layer where the error surfaced.** The cause is usually 1-3 layers below.
- **Reading source code to predict what should happen instead of running the system to observe what does happen.** Reading is cheap but unreliable for runtime behavior; observation is authoritative.
- **Adding fallbacks, retries, or defensive code while the root cause is still unknown.** This converts a loud failure into a silent corruption.

## Rules

- Reproduce deterministically first. If you cannot, the failure is state-dependent until proven otherwise.
- Verify the cheapest hypothesis first, not the most plausible one - and apply that to your own confident mid-investigation conclusions, not just the opening candidates.
- Verify the end state, not a fix's local effect. A change doing its narrow job is a checkpoint, not a conclusion - and a fix that resolves a per-item conflict by grouping items must be checked for the same conflict reappearing among the groups.
- Trust a work-unit metric (deterministic time, rows, instructions) over wall time; pin the environment (`caffeinate -i`, one run at a time) before any timing judgment, and treat a work-unit/wall-time divergence as a corrupted measurement, not a slow code path. A solver UNKNOWN proves a budget wall only if the work-unit count actually reached the cap.
- When no log exposes the value you need, instrument it, capture it in one run, and revert the probe.
- Read the solver/planner status before theorizing: impossibility-proof (`INFEASIBLE`/UNSAT) demands relaxing upstream; budget timeout demands a smaller model or bigger budget. Opposite fixes.
- Classify a knob as feasibility-affecting or performance-affecting before turning it; a search-shape/budget knob cannot fix a feasibility wall, and relaxing a constraint cannot fix a timeout.
- Separate the cost of finding a feasible answer from the cost of proving it optimal: if the consumer needs only a valid result and the engine grinds proving minimality, stop at first-feasible (no model change); if it never finds a first feasible point, decompose so the search becomes reachable. Read the incumbent/bound log to tell which; the two fixes combine.
- Do not assume a smaller or more-constrained model is easier; over-constraining one search problem can remove the slack the search needs, while decomposing into independent sub-problems genuinely helps. Measure find-feasible time and status after the change.
- Treat escalating fix complexity as a signal the shared premise is wrong: when each fix is bigger than the last, stop adding machinery and re-question the assumption every attempt inherited rather than building further on it.
- When a downstream stage is a capped (feasible-not-optimal) solver, a legal upstream change can reshuffle its whole output; fix the stage's stability or the next stage's tolerance, not your change's "neutrality."
- At a decision fork before expensive work, pressure-test the diagnosis with an adversary that cannot see your tool results; re-verify any fact it asserts, and use it to catch overclaimed scope rather than to confirm your lean.
- Attribute regressions against a reverted baseline in the same environment before claiming the failure is (or is not) yours - saving uncommitted work first (stash/checkpoint; never destructive `checkout -- <files>` over live edits), and isolating bundled changes individually rather than reverting them as a unit.
- Under expensive feedback loops, front-load cheap checks, fail-fast on the earliest falsifying artifact, and detach-and-poll long runs.
- Map the symptom layer to a candidate cause layer (1-3 layers below) before opening source.
- For "works here, fails there," diff the environments literally before reasoning.
- For "worked once, fails now," find what is being mutated between runs - unless a downstream stage is a capped bounded engine, where nothing was mutated and the output is just perturbation-sensitive.
- Find the real stack trace before theorizing. Generic error messages are wrappers.
- Use symbol names from stack traces, not file:line numbers in bundled binaries.
- Cross-reference timestamps with deployments, image rebuilds, config changes.
- Fix at the source that writes the bad state, not in the resulting artifact.
- Do not restart or rebuild without a hypothesis that predicts a different observable outcome.
