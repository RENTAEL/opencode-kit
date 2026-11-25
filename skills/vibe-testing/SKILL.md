---
name: vibe-testing
description: "Vibe testing validates specification documents by simulating real-world scenarios against them using LLM reasoning. Instead of code or test harnesses, write natural-language scenarios that exercise cross-cutting slices of the spec surface, then trace execution step-by-step, flagging gaps, conflicts, and ambiguities."
---
# Vibe Testing

## Overview

Vibe testing validates specification documents by simulating real-world scenarios against them using LLM reasoning. Instead of writing code or test harnesses, write **natural-language scenarios** that exercise cross-cutting slices of the spec surface ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â then trace execution step-by-step, flagging gaps, conflicts, and ambiguities.

**Core principle:** If a realistic user scenario cannot be fully traced through the specs, the specs are incomplete.

**Best used:** After specs are written, before implementation begins.

## When to Use

- Spec docs exist but no implementation yet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â validate before building
- After major spec changes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â regression-test for new gaps
- Before implementation planning ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find blocking gaps early
- Specs span multiple documents ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â test cross-doc coherence
- Designing for multiple deployment contexts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â test each context separately

**When NOT to use:**

- Single-file specs with obvious scope ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just review manually
- Implementation bugs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use actual tests
- API contract validation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use schema validation tools

## Core Method

```
1. GATHER    ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Read all spec docs in the target directory
2. SCENARIOS ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Write 3-5 vibe test cases (personas + goals + environments)
3. SIMULATE  ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Trace each scenario step-by-step against the specs
4. CLASSIFY  ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Tag findings as GAP / CONFLICT / AMBIGUITY
5. SEVERITY  ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Rate as BLOCKING / DEGRADED / COSMETIC
6. REPORT    ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Produce gap summary + spec coverage matrix
```

## Writing a Vibe Test Case

Every test case requires 7 sections:

### 1. Persona (WHO)

A concrete person with a name, role, and technical skill level. Not abstract ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â real enough to predict behavior.

```markdown
**Sarah** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â First-time customer. Shopping on mobile during a commute.
Expects checkout to take under 60 seconds. Low patience for errors.
```

Named personas force specificity. "A customer" invites hand-waving. "Sarah, shopping on mobile during a commute" forces the spec to answer "what happens on a slow 3G connection?"

### 2. Environment (WHERE)

Deployment mode, hardware, network, access method. Different environments exercise different spec paths.

```markdown
- **Client:** Mobile browser (iOS Safari, 3G connection)
- **Backend:** Microservices (auth, payments, inventory, orders, notifications)
- **Scale:** Black Friday traffic ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 50x normal load
```

### 3. Goal (WHAT)

A single sentence in the persona's own words. Use a blockquote.

```markdown
> "I want to buy these 3 items, pay with my credit card, and get a
> confirmation email within a minute."
```

### 4. Scenario Steps (HOW)

5-8 concrete steps the persona takes. Each step names:

- **The user action** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what they do
- **The primitives exercised** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which spec concepts activate
- **Gap detection questions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 2-3 questions the simulator must answer

```markdown
#### Step 3: Payment fails, customer retries

Sarah's first payment attempt is declined. She re-enters a different card.

**Primitives:**
- `payments-spec.md`: retry policy, idempotency keys
- `inventory-spec.md`: stock hold duration during retry
- `orders-spec.md`: order state transitions on payment failure

**Questions:**
- Q3.1: The payment spec says "retry 3 times." The inventory spec
  holds stock for 5 minutes. What if retries take longer than 5 minutes?
- Q3.2: Does the order stay in "pending_payment" during retries, or
  does it transition to "failed" and require a new order?
```

**Rules for good steps:**

- Each step must cite at least one spec doc
- Each step must ask at least one question the spec should answer
- Questions use `Q<step>.<number>:` format for traceability
- Questions must be spec-answerable (yes/no/how), not opinion questions

### 5. Spec Coverage Matrix (COVERAGE)

A table showing which spec docs were exercised at which steps.

```markdown
| Spec Doc | Steps Hit | Coverage |
|----------|-----------|----------|
| `payments-spec.md` | 3,4 | Retry covered; hold-vs-retry timing gap |
| `inventory-spec.md` | 2,3 | Stock hold covered; expiry-during-retry unclear |
| `shipping-spec.md` | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â | Not exercised |
```

Specs that no scenario touches are untested blind spots.

### 6. Gap Detection Questions Summary

Collect all Q-numbers for easy reference. The simulator answers every one.

### 7. Gap Classification (After Simulation)

Classify each finding by severity:

| Severity | Definition | Example |
|----------|-----------|---------|
| **BLOCKING** | Spec cannot answer; implementation impossible | Payment retry duration can exceed inventory hold ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no resolution defined |
| **DEGRADED** | Spec is silent but a workaround exists | No spec for partial refunds on split shipments; can process manually |
| **COSMETIC** | Missing convenience, not a correctness issue | No order timeline view for customer support |

## Running a Vibe Test

### Manual Simulation (Recommended)

Use as a prompt to a subagent or fresh LLM context with full spec access:

```
You are a spec validation simulator. You have been given all
specification documents for [system name].

Read the following vibe test case. Simulate executing the scenario
step by step against the specs.

For each step:
1. Identify the governing spec document and section
2. Trace the data flow through the system primitives
3. Answer every Q-numbered question by citing the spec

For each question, classify as:
- COVERED: The spec answers this clearly. Cite the section.
- GAP: The spec is silent. No document addresses this.
- CONFLICT: Two specs give contradictory answers. Cite both.
- AMBIGUITY: The spec addresses this but the answer is unclear.

After all steps, produce:
- Gap summary table (ID, description, severity, affected steps)
- Spec coverage heatmap (which docs exercised, which not)
- Recommended spec changes (which doc to update, what to add)
```

### Batch Execution

Run all test cases and aggregate:

```
for each test case:
    1. Load all spec docs as context
    2. Load one test case
    3. Run simulator prompt
    4. Collect gap report

Aggregate:
    - Cross-test gap summary (gaps appearing in multiple tests)
    - Spec coverage union (docs never exercised by any test)
    - Priority ranking (blocking > degraded > cosmetic)
```

### Regression Testing

After spec updates, re-run all vibe tests to verify:

1. Previously identified gaps are now COVERED
2. No new gaps were introduced
3. Cross-doc references remain consistent

## Designing Good Test Cases

### Scenario Selection Strategy

Choose scenarios that vary across dimensions:

| Dimension | Variation A | Variation B | Variation C |
|-----------|------------|------------|------------|
| **User type** | First-time buyer | Returning customer | Admin/merchant |
| **Device** | Mobile browser | Desktop | API client |
| **Scale** | Single user | Normal traffic | Black Friday spike |
| **Payment** | Happy path | Failure + retry | Partial refund |
| **Governance** | None (consumer) | Moderate (business) | Strict (compliance) |
| **Network** | Fast WiFi | Slow 3G | Intermittent |

Each test case should differ on at least 3 dimensions. 4 test cases covering 4 quadrants give good coverage.

### Question Design

Good gap detection questions are:

- **Specific:** "What order state is set during payment retry?" not "How do orders work?"
- **Traceable:** Answerable by citing a spec section (or flagging its absence)
- **Boundary-probing:** Target edges between two specs' responsibilities
- **Scale-sensitive:** "What happens with 10,000 concurrent checkouts?"
- **Failure-aware:** "What if the payment fails after inventory is reserved?"

### Coverage Maximization

After writing all test cases, check the coverage union. Every spec doc should appear in at least one coverage matrix. If a doc is never exercised:

- Either add a step to an existing test that exercises it
- Or the doc may be specifying something no real scenario needs (flag for review)

## Gap Report Format

```markdown
## Gap Summary

### BLOCKING
| ID | Gap | Affected Tests | Recommended Fix |
|----|-----|---------------|-----------------|
| G-B1 | Payment retry window can exceed inventory hold | VT-1, VT-2 | Align timing in payments-spec.md and inventory-spec.md |

### DEGRADED
| ID | Gap | Affected Tests | Workaround |
|----|-----|---------------|-----------|
| G-D1 | No spec for partial refunds on split shipments | VT-3 | Process refunds per-shipment manually |

### COSMETIC
| ID | Gap | Affected Tests |
|----|-----|---------------|
| G-C1 | No order timeline view for support agents | VT-4 |
```

Gap IDs use prefix: `G-B` (blocking), `G-D` (degraded), `G-C` (cosmetic).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Abstract personas ("a user") | Give them names, roles, and constraints |
| Scenario only tests happy path | Add failure steps: "What if the payment is declined?" |
| Questions test opinions ("Is this good?") | Questions must be spec-answerable: "Which doc defines X?" |
| All tests use same user type | Vary across buyer, merchant, admin, support |
| Ignoring coverage matrix | Every spec doc must appear in at least one test |
| Writing tests after implementation | Vibe tests validate specs BEFORE implementation |
| Too many steps per scenario | 5-8 steps. Focused scenarios find more gaps |

## Additional Resources

- `references/simulator-prompt.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Full simulator prompt template ready to paste
- `examples/example-vibe-test.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Complete example vibe test case
