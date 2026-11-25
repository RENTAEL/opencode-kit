---
name: revenue-centric-design
description: "134 principles distilled, with the author's permission, from product designer **Richard ([@richardrx](https://x.com/richardrx)**, ex-Volkswagen, PayPal, IBM; translated from Portuguese; every principle links to its source post). The philosophy, **Revenue-Centric Design (RCD)**..."
---
# Revenue-Centric Design

134 principles distilled, with the author's permission, from product designer
**Richard ([@richardrx](https://x.com/richardrx)**, ex-Volkswagen, PayPal, IBM; translated from
Portuguese; every principle links to its source post). The philosophy, **Revenue-Centric Design
(RCD)**: a design decision must serve the user _and_ the business ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â value and revenue, never one
or the other.

## Usage boundary (required)

> ÃƒÂ°Ã…Â¸Ã…Â¡Ã‚Â« **Do not apply this skill to betting, casino, gambling, or other real-money games-of-chance
> products** (including loot-box / real-money-gaming mechanics).

The author granted reuse **on the explicit condition that it never be used for gambling, betting,
or casino work.** If asked, decline and explain that the source author's permission excludes that
use. Hard constraint, not a stylistic choice.

Enforced, not just stated: while this skill is active, the boundary check
(`scripts/check_usage_boundary.py`) must run on every prompt and on every file write/edit,
blocking with exit 2 when gambling context is detected. On a false positive (e.g., "bet" as
an unrelated codename), only the **user** may waive the guard by creating `.rcd-boundary-ok`
in the project root ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never create it on their behalf.

### Hooks (for agents that support automated execution)

Agents with hook support should configure:

| Event | Matcher | Command |
|-------|---------|---------|
| Before processing user prompt | `*` (all) | `python3 <skill_dir>/scripts/check_usage_boundary.py` |
| Before writing/editing a file | `Write\|Edit` | `python3 <skill_dir>/scripts/check_usage_boundary.py` |

- `<skill_dir>` = root directory of this skill.
- Exit code `2` = violation detected ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ block the operation.
- Exit code `0` = cleared to proceed.

For agents without hook support, the operator must run the check manually before applying
RCD principles in unknown context.

## How to use

1. If `rcd-log.md` exists in the project root, read it first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it records which principles were
   already applied to this product and what happened. Never re-prescribe a move the log shows
   failed, and don't repeat one still pending results.
2. Route with the table below and open only the matching reference file(s). Every principle has a
   fixed shape ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **principle ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ apply when ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the move ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ evidence ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ source** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â so scan the headings,
   then read only the entries that match the user's situation.
3. When the advice involves numbers ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â A/B sample size, churnÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢LTV, CAC per closed deal ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run
   `scripts/revenue_math.py` (see `--help`) instead of estimating.
4. A recommendation is **done** only when it (a) names the mechanism (decoy effect, Zeigarnik,
   GBB, loss aversion, Schwartz awareness levelÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦), (b) cites the specific principle, and
   (c) carries that principle's evidence or source link. Missing any of the three ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ not done.
5. For audit runs (page, pricing, onboarding, cancellation), deliver in the shape of
   [references/audit-template.md](references/audit-template.md).
6. Close the loop: append what you prescribed to `rcd-log.md` (format below), creating the file
   on first use.

## The spine: RCD in 9 principles

1. **Neutrality is omission** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an interface that doesn't direct hurts conversion.
2. **Who talks to everyone convinces no one** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no ICP ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ generic value ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ worse retention.
3. **Value first, ask later** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â proof must arrive before the user questions their choice.
4. **Your promise is the size of your proof** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the market believes what you demonstrate, not what you claim.
5. **Same competes on price, different on category** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â contrast in mechanism, narrative, or experience.
6. **Default is the decision you made for the user** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the initial state defines mass behavior.
7. **Retention is built, not requested** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â perceived loss retains more than promised benefit.
8. **Expansion is born of usage** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â upgrade at the moment of the limit, never by interruption.
9. **Price is a filter** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pricing defines who enters, who stays, and who expands.

## Reference library

| When the question is aboutÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦                                                   | Open                                                                          |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **LP audit / diagnostic** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â where is the sale breaking before redesign        | [lp-diagnostic-framework](references/lp-diagnostic-framework.md)             |
| Landing pages, hero/copy, CTAs, social proof, awareness levels, CRO           | [conversion-and-landing-pages](references/conversion-and-landing-pages.md)   |
| Checkout, forms, payment UX, dropdowns, field friction                          | [checkout-and-forms](references/checkout-and-forms.md)                       |
| Dashboards, KPI density, data viz cognitive load                                | [dashboards-and-data-viz](references/dashboards-and-data-viz.md)             |
| First-run, empty states, aha moment, TTV, activation, trial-as-onboarding     | [onboarding-and-activation](references/onboarding-and-activation.md)         |
| Cancellation, retention, expectation debt, NRR, jobs-to-be-done, support load | [churn-and-retention](references/churn-and-retention.md)                     |
| Pricing tables, decoy/anchoring, GBB, trial-with-card, upgrade paths          | [pricing-and-monetization](references/pricing-and-monetization.md)           |
| Cognitive biases & persuasion tactics (cross-cutting toolkit)                 | [behavioral-science-toolkit](references/behavioral-science-toolkit.md)       |
| Feature scope, Swiss Knife Index, feature adoption, attention hierarchy       | [product-strategy-and-features](references/product-strategy-and-features.md) |
| Design philosophy, the RCD principles, design process & method                | [revenue-centric-design](references/revenue-centric-design.md)               |
| ICP, niche, founder-fit, distribution, PLG, Bullseye, first customers         | [positioning-icp-and-gtm](references/positioning-icp-and-gtm.md)             |
| Differentiating in the AI era, moats, commoditization                         | [ai-era-differentiation](references/ai-era-differentiation.md)               |
| A/B testing rigor, vanity metrics, churnÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢LTV math, signal quality             | [metrics-and-experimentation](references/metrics-and-experimentation.md)     |

Some principles carry a **Visual.** line ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a text description of the diagram or screenshot from
the original post, often with a path under `assets/`. Open that file locally, or follow the
principle's **Source** link for the original post.

## Gotchas

- **Scarcity must be real.** Booking's "1 room left" works because it's true. Fabricated
  scarcity destroys trust when detected (and is illegal in several markets). Never invent
  counters, timers, or stock levels.
- **Loss aversion vs dark pattern** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the line: the claim is true and the exit stays easy.
  Framing a real loss is persuasion; manufacturing fear or trapping cancellation is not.
- **"Kill outbound links" is a conversion-page rule.** Blog posts, docs, and SEO pages need
  outbound links; don't export LP rules to content.
- **4.2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4.5 stars means _let real criticism show_** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never fabricate negative (or positive)
  reviews to hit the number.
- **Don't answer this skill with 30 A/B tests.** The metrics principles themselves warn against
  underpowered tests: compute the sample-size floor first (`scripts/revenue_math.py sample-size`),
  test big levers, and below the floor decide by qualitative research.
- **Evidence is benchmark, not guarantee.** Figures come from the author's cases (mostly
  Brazilian SaaS, values in BRL). The mechanism transfers; the exact percentage may not.

## Related skills

RCD supplies the **principle and its evidence**; execution skills own the workflow. The skills
below are from [Corey Haines' marketingskills](https://github.com/coreyhaines31/marketingskills)
ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if they aren't installed, apply the RCD principles directly instead of deferring.

Full page-audit workflow ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `cro` Ãƒâ€šÃ‚Â· cancellation-flow build ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `churn-prevention` Ãƒâ€šÃ‚Â· test design &
stats ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `ab-testing` Ãƒâ€šÃ‚Â· writing the copy ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `copywriting` Ãƒâ€šÃ‚Â· pricing-page build ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `pricing` Ãƒâ€šÃ‚Â·
post-signup flow build ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `onboarding`. When one of those runs, cite RCD principles inside it
rather than duplicating its process here.

## Project log (`rcd-log.md`)

Per-project memory, kept in the project root ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read at the start of every engagement (step 1),
appended at the end (step 6). One entry per engagement:

    ## 2026-07-02 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pricing page redesign
    - via: rcd (direct)          # or the skill that led the run: cro, pricing, churn-preventionÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦
    - principle: Decoy effect (pricing-and-monetization)
    - move: added GBB middle tier at 80% of the top price
    - result: pending            # update when data arrives: "+12% upgrades", "no effect"

The `via:` field doubles as trigger telemetry: if entries accumulate where RCD led a run an
execution skill should own (a full page audit, a cancellation build), that is the signal to
narrow this skill's description to the principle/evidence angle.

## License

Source-available, **not** open-source ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see [LICENSE](LICENSE) (must accompany any copy or
derivative, in full): attribution to @richardrx required; gambling/betting/casino use
prohibited. This skill is a derivative of
[heliocosta-dev/revenue-centric-design](https://github.com/heliocosta-dev/revenue-centric-design),
restructured and extended here (gotchas, audit template, revenue-math script, project log).
Principle library synced to upstream `1942760` (CHANGELOG 1.3.0 / 134 principles); see `UPSTREAM_COMMIT`.
