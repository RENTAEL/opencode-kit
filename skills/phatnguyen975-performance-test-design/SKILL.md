---
name: phatnguyen975-performance-test-design
description: "This skill takes a system's requirements documentation and turns it into a complete set of implementer-ready **Performance Test Case Specifications** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one per Operational Profile the system needs tested ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â following the ISTQB Certified Tester ..."
---
# Performance Test Design Skill

## Overview

This skill takes a system's requirements documentation and turns it into a complete set of implementer-ready **Performance Test Case Specifications** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one per Operational Profile the system needs tested ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â following the ISTQB Certified Tester Performance Testing (CT-PT) syllabus process, extended with real-world workload-modeling practice beyond what the syllabus covers at a summary level.

The process has exactly **two phases**:

1. **Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Operational Profile Discovery:** Read the system's documentation once, and produce a reviewed, approved list of every Operational Profile the system needs performance-tested.
2. **Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Per-Profile Test Case Design:** For each approved profile, in order, run it through four dependent steps (profile analysis ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ load profile design ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ throughput/concurrency analysis ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ test case specification) to produce that profile's complete design, then pause for human review before moving to the next profile.

This skill is the **design layer** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it stops at the specification. It never writes JMeter/k6/Gatling/LoadRunner code, and it never picks a tool.

## When to Use

- Starting performance test design for a system (or a release/module of one) from its requirements documentation, before any scripting begins.
- Discovering and enumerating the full set of Operational Profiles a system needs tested ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not just designing one test case in isolation.
- Translating NFRs/SLAs into concrete, measurable, per-transaction test case specifications.
- Determining defensible virtual-user counts, throughput targets, and think-time values ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â with the calculation shown, not guessed.
- Defining what test data a performance test needs (volume, diversity, parameterization, correlation) before an implementer writes scripts.
- Re-validating or refining part of an existing design ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â any step in Phase 2 can be re-run on its own once its prerequisite step's output already exists for that profile.

## When NOT to Use

- **Writing or debugging actual test scripts/code** for any load-testing tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill stops at specification; scripting is a separate, subsequent activity done by the user.
- **Functional test case design** (equivalence partitioning, boundary value analysis, decision tables, state transitions) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â unrelated to performance test design.
- **Executing tests, monitoring live runs, or analyzing post-execution results/bottlenecks** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is a pre-execution design skill only.
- **Capacity planning or infrastructure sizing** as a standalone activity disconnected from a specific test case ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill uses capacity/throughput numbers as _input_ to test design, it does not do infrastructure procurement sizing.
- **Designing a single, ad-hoc test case with no intention of discovering the system's full profile set** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â still possible (skip straight to Phase 2 with a manually supplied profile), but the skill's primary value is the systematic Phase 1 discovery; if that's not wanted, a lighter-weight approach may suit better.

## Input

**Required for Phase 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â system documentation, in whatever form is available:

| Document                                                                                      | What Phase 1 extracts from it                                            |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Business Requirements (BRD)**                                                               | Business processes and their relative importance                         |
| **Functional Requirements (FRD) / User Stories**                                              | Functions/transactions the system supports                               |
| **Use Case Documents**                                                                        | User roles and their goals ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â maps directly to Operational Profile actors |
| **NFR / SLA Documents**                                                                       | Response time, throughput, error-rate, concurrency targets               |
| **System Architecture / Design Docs**                                                         | Protocols, tiers, integration points, sync/async boundaries              |
| **Production logs / APM / analytics data** (if the system, or a predecessor, is already live) | Real transaction frequencies and think-time distributions                |

If a document type is entirely unavailable, Phase 1 still proceeds using what exists, and states explicitly which profile details had to be estimated rather than sourced ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see Core Principle 1.

**Required for Phase 2** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the approved output of Phase 1 (`operational-profiles.md`), taken one profile at a time.

## Core Principles

1. **Traceability over invention.** Every number in any output (transaction mix %, VU count, TPS, think time, NFR threshold) must trace to a cited source or be explicitly labeled `[ASSUMPTION]` with the reasoning shown. Never present an assumed number as if it were measured.
2. **Discover the whole system before designing any one profile.** Phase 1 must complete and be approved before Phase 2 begins ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â designing a profile's test case before the full profile list is confirmed risks scope drift (missed profiles, wrongly merged profiles) that's expensive to unwind later.
3. **One Operational Profile per design cycle in Phase 2.** Never design test cases for multiple profiles in a single pass ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each gets its own complete run through all four steps and its own human review before the next one starts.
4. **Tool-agnostic by construction.** Nothing in any output should assume a specific load-testing tool's syntax, feature set, or terminology.
5. **Specification, not implementation.** Step 4 of Phase 2 describes _what_ a script must do ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it never contains actual tool syntax or code.
6. **Step outputs are inspectable, the final spec is lean.** Each step's output is deliberately explicit about its reasoning so a reviewer can localize a wrong assumption to the exact step that introduced it. The final Test Case Specification (Step 4's last artifact) is a **separate, condensed document** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it must not simply concatenate the earlier steps' content.
7. **Use the technique that fits the transaction, not a default technique applied uniformly.** Every technique in this skill has explicit "When to Use" / "When NOT to Use" guidance ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read it before applying the technique, and state in the output which techniques were applied to which transactions and why.

## Design Process

```
 INPUT: System documentation (BRD, FRD, use cases, NFR/SLA, architecture, logs)
                             ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
                             ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
 ÃƒÂ¢Ã¢â‚¬ÂÃ…â€™ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‚Â
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ PHASE 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Operational Profile Discovery                            ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ phases/phase-1-operational-profile-discovery/README.md          ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  Read every available system document once. Identify user roles,   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  business flows, and NFR-relevant constraints. Partition the       ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  system into a numbered, prioritized list of Operational Profiles. ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  OUTPUT: operational-profiles.md                                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‚Â¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‹Å“
                             ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
                   ÃƒÂ¢Ã‚Â¬Ã‚Â¡ AI GATE (Phase 1 output-quality-checklist.md)
                             ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
                   ÃƒÂ¢Ã‚Â¬Ã‚Â¡ HUMAN REVIEW GATE 1
                     "Is this profile list correct and complete?"
                     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Needs changes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ revise operational-profiles.md, ask again
                     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Approved ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ proceed to Phase 2, Profile #1
                             ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
 ÃƒÂ¢Ã¢â‚¬ÂÃ…â€™ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‚Â
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ PHASE 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Per-Profile Test Case Design                             ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ phases/phase-2-per-profile-test-design/README.md                ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  Repeat the 4 steps below for each approved profile, IN ORDER,     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  one profile fully completed and human-approved before the next    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  profile begins:                                                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   STEP 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Profile Analysis (ISTQB CT-PT 4.2.1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4.2.3)              ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ step-1-profile-analysis/README.md                            ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     OUTPUT: p1-profile-analysis.md                                 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                    ÃƒÂ¢Ã‚Â¬Ã‚Â¡ AI Gate (step-1 output-quality-checklist.md)  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   STEP 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Load Profile Design (ISTQB CT-PT 4.2.4)                 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ step-2-load-profile-design/README.md                         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     OUTPUT: p2-load-profile.md                                     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                    ÃƒÂ¢Ã‚Â¬Ã‚Â¡ AI Gate (step-2 output-quality-checklist.md)  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   STEP 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Throughput & Concurrency Analysis (ISTQB CT-PT 4.2.5)   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ step-3-throughput-concurrency/README.md                      ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     OUTPUT: p3-workload-numbers.md                                 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                    ÃƒÂ¢Ã‚Â¬Ã‚Â¡ AI Gate (step-3 output-quality-checklist.md)  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   STEP 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Test Case Specification (ISTQB CT-PT 4.2.6ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4.2.7,       ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡            specification scope only, no scripting)                 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ step-4-test-case-specification/README.md                     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡     OUTPUT: p4-test-data-specification.md (intermediate, verbose)  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡           + test-case-spec.md (final, condensed)                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                    ÃƒÂ¢Ã‚Â¬Ã‚Â¡ AI Gate (step-4 output-quality-checklist.md)  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                                                                    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
 ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‚Â¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‹Å“
                             ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
                   ÃƒÂ¢Ã‚Â¬Ã‚Â¡ HUMAN REVIEW GATE 2 (after every profile)
                     "Is this profile's design correct and complete?"
                     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Needs changes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fix the specific step that's wrong, re-run only the steps downstream of the fix, ask again
                     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Approved ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ more profiles remain in the list?
                                     ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Yes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ back to Phase 2, next profile
                                     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ No  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ DONE
```

### AI Gates vs. Human Review Gates

These are two different checks, both required, never skipped:

- **AI Gate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â You (AI Agent) self-review the step's output against that step's `output-quality-checklist.md` before presenting it. Catches content defects (missing citation, unhandled edge case, wrong formula application) before the human ever sees them.
- **Human Review Gate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â The person using this skill explicitly approves or requests changes. Never assume approval; always ask and wait.

### Where "Workload Modeling" and "Operational Profiling" Fit

These are umbrella terms used in the industry, not standalone techniques in this skill:

- **"Operational Profiling"** = Phase 1 as a whole (discovering and defining the profile list) plus Step 1 of Phase 2 (analyzing one profile in depth). If asked to "do operational profiling," this covers both.
- **"Workload Modeling"** = Step 2 (load shape) + Step 3 (throughput/concurrency numbers) of Phase 2 combined. Step 2 decides the _shape_; Step 3 decides the _numbers_ that fill it.

## Design Rules

- Never invent a metric threshold, transaction frequency, or user count. If a source doesn't provide it, label it `[ASSUMPTION - needs confirmation]` with the reasoning used to derive it.z
- Never begin Phase 2 for any profile before Phase 1's list has passed Human Review Gate 1.
- Never let Step 4 introduce a new business requirement, transaction, or NFR that wasn't already surfaced in Step 1 or Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Step 4 specifies data and structure for decisions already made, it does not reopen them.
- Never merge two Operational Profiles into one Phase 2 cycle, even if they share transactions ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â design them separately and cross-reference the overlap.
- Never carry a failed AI Gate forward. Fix the defect in the step that produced it before continuing.
- Always keep the final Test Case Specification free of the full reasoning trails that live in the step outputs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â link back to them by file reference instead of repeating them.
- Always select the specific technique(s) that fit each transaction's actual behavior (see each step's technique files for selection criteria) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never apply one technique uniformly across all transactions without checking whether a different technique fits better for a particular one.

## Anti-Patterns

Phase- and step-specific anti-patterns live in each phase/step's own `anti-patterns.md`. Cross-cutting anti-patterns for the overall process:

- **Skipping Phase 1 and jumping straight into designing one profile** because "we already know what to test." This risks missing profiles entirely or scoping the one profile too broadly/narrowly.
- **Treating the four Phase 2 steps as optional checkboxes rather than a dependency chain.** Step 3's Little's Law calculation needs Step 2's duration and target throughput; Step 4's data spec needs Step 1's transaction list. Doing them out of order produces numbers that don't reconcile.
- **Producing one giant document covering all profiles at once**, defeating the purpose of per-profile review.
- **Copy-pasting all step content into the final Test Case Specification** "to be safe" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â explicitly disallowed (Core Principle 6).
- **Applying the same technique to every transaction by default** instead of checking each technique's "when to use" criteria per transaction.

## Best Practices

Phase- and step-specific best practices live in each phase/step's own `best-practices.md`. Cross-cutting best practices:

- State the data source inline next to every number ("35% ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â derived from 90-day access log analysis" vs. "35% ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â assumption, no log data available").
- When production data is unavailable, still produce a number, but make the assumption and its justification impossible to miss.
- Re-run only the steps downstream of a fix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if a Step 2 fix changes the load shape, re-check whether Step 3 (which depends on Step 2's duration/throughput) still holds.
- Keep step output files small and single-purpose so a reviewer scanning a profile's folder can tell exactly where in the pipeline something went wrong just from the filename.
- Before applying any technique, re-read its "When to Use / When NOT to Use" section for the specific transaction at hand ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the right technique varies by transaction, not just by phase.

## Quality Checklist (Process Conformance)

Different from each step's `output-quality-checklist.md` (which checks the _test design content_). This one checks that **the process itself was followed**. Run once per completed profile, right before Human Review Gate 2:

- [ ] Phase 1 was completed and passed Human Review Gate 1 before any Phase 2 work began.
- [ ] Exactly one Operational Profile was in scope for this Phase 2 cycle ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no scope creep to a second profile.
- [ ] All four Phase 2 steps were executed in order; none were skipped.
- [ ] Every AI Gate (Phase 1, and Steps 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4) was actually checked against its checklist file, not assumed to pass.
- [ ] Every number in every output is either sourced or explicitly marked `[ASSUMPTION]`.
- [ ] The final Test Case Specification is a condensed, standalone document ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not a concatenation of the step outputs.
- [ ] All output files were named and placed according to the Invoke Syntax section below.
- [ ] For each technique applied, its "when to use" criteria were actually checked against the transaction it was applied to ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not applied by default.
- [ ] The human has not yet been asked to approve this profile ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this checklist itself is the last step before that ask.

## Common Rationalizations

- _"We already know our system, we can skip Phase 1's document analysis."_ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Skipping it risks missing a profile or misjudging its priority ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 1 exists precisely to make that judgment traceable and reviewable rather than assumed.
- _"The NFR doc doesn't have exact numbers, I'll use industry-typical values instead of asking."_ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Mark it `[ASSUMPTION]` and flag it; don't silently substitute a plausible-looking number.
- _"This profile is simple, I can skip straight to the workload numbers."_ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Every profile still needs Step 1's transaction mix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â simple profiles are exactly where an unexamined assumption slips through easiest.
- _"I already wrote most of this in the step outputs, I'll copy it into the final spec to save time."_ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Violates Core Principle 6. The final spec must be authored fresh, condensed to what an implementer needs.
- _"The human will catch anything wrong at the review gate, so I don't need to run the AI Gates carefully."_ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ AI Gates exist precisely to catch defects before burdening the human with a review pass.
- _"Two profiles are almost identical, I'll design one and duplicate it."_ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Even similar profiles can diverge in transaction mix or NFR ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run each through the full process.

## Red Flags ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Stop and Reconsider

- About to write a VU count, TPS figure, or think-time value with no citation and no `[ASSUMPTION]` tag.
- About to start Phase 2 for a profile before Phase 1's list has been human-approved.
- About to design test cases for a profile with no clear NFR/SLA, without flagging the gap.
- About to include tool-specific syntax (a JMeter element, a k6 script snippet, a Gatling DSL call) anywhere in an output.
- About to skip an AI Gate "because the output looks fine."
- About to merge multiple Operational Profiles' outputs into a single specification file.
- About to apply a technique to every transaction without checking whether it's actually the right one for each.

## Output Templates

Located inside each phase/step's own folder (not centralized) so the template lives next to the guidance that explains how to fill it in:

- `phases/phase-1-operational-profile-discovery/output-template.md`
- `phases/phase-2-per-profile-test-design/step-1-profile-analysis/output-template.md`
- `phases/phase-2-per-profile-test-design/step-2-load-profile-design/output-template.md`
- `phases/phase-2-per-profile-test-design/step-3-throughput-concurrency/output-template.md`
- `phases/phase-2-per-profile-test-design/step-4-test-case-specification/output-template-data-spec.md`
- `phases/phase-2-per-profile-test-design/step-4-test-case-specification/output-template-test-case-spec.md`

## Invoke Syntax

**Default mode ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print to conversation:**

```
/performance-test-design
```

Runs Phase 1 first (prints `operational-profiles.md`, pauses for Human Review Gate 1), then Phase 2 for each approved profile in order (prints each step's output, pausing at each AI Gate as described, then at Human Review Gate 2 after each profile completes).

**File mode ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â write to disk:**

```
/performance-test-design --file=docs/perf-test-profiles/
```

The path given after `--file=` is a **directory**, not a single file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â because this skill's output spans Phase 1's profile list plus a per-profile subfolder for each profile in Phase 2. Layout:

```
docs/perf-test-profiles/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ operational-profiles.md                    ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Phase 1 output
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ PROF-01-{short-name}/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ p1-profile-analysis.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ p2-load-profile.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ p3-workload-numbers.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ p4-test-data-specification.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ test-case-spec.md                       ÃƒÂ¢Ã¢â‚¬Â Ã‚Â final, condensed
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ PROF-02-{short-name}/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ [same 5 files]
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...
```

The `{short-name}` slug is derived from the profile's name in `operational-profiles.md` (lowercase, hyphenated, short enough to scan in a directory listing). This keeps every profile's full design ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all four step outputs plus the final spec ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â together in one place, and keeps the final spec's filename identical and predictable across every profile.

In file mode, still print a short progress summary to the conversation after each phase/step (not the full content) so the human can follow along without opening files, and still pause at every AI Gate and Human Review Gate exactly as in default mode.

## Reference Files

- `phases/phase-1-operational-profile-discovery/README.md`
- `phases/phase-2-per-profile-test-design/README.md`
- `phases/phase-2-per-profile-test-design/step-1-profile-analysis/README.md`
- `phases/phase-2-per-profile-test-design/step-2-load-profile-design/README.md`
- `phases/phase-2-per-profile-test-design/step-3-throughput-concurrency/README.md`
- `phases/phase-2-per-profile-test-design/step-4-test-case-specification/README.md`
- `examples/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a complete, worked example: system documentation ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Phase 1 discovery ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 4 fully designed Operational Profiles, generated by actually applying this skill after it was built
