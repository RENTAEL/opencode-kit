# S2 Informatics Research Framework

## Status of this document

This is an **S2 Informatics interpretation and AI heuristic**, not a Frascati thesis requirement. It operationalises Frascati's R&D-identification concepts for thesis advising.

## Core distinction

| Implementation-centered | Research-centered |
|---|---|
| Problem -> requirements -> design -> development -> testing -> deployment | Problem -> evidenced gap -> research question -> hypothesis/proposition -> method -> experimental design -> baselines -> evaluation -> analysis -> knowledge contribution |
| Success: system functions | Success: evidence answers a non-trivial question and changes what is known |

Neither column is morally superior. The distinction identifies whether the proposed endpoint matches a Master's research contribution.

## S1-to-S2 transformation pattern

| Starting formulation | Upgrade question |
|---|---|
| Build an app using model M for domain D. | Under what conditions does mechanism X improve outcome Y over baselines, and why/when does it fail? |
| Deploy a model at the edge. | What compression, adaptation, or scheduling mechanism best manages the measured accuracy-latency-energy trade-off under stated constraints? |
| Make an AI framework. | Does the specified framework mechanism improve reproducibility, adaptation, reliability, or efficiency versus defined alternatives? |
| Fine-tune an LLM. | Which adaptation or retrieval mechanism changes robustness, factuality, cost, or safety under domain shift, relative to baselines? |

## Evidence ladder for a proposal

1. Problem is consequential and bounded.
2. State of the art is documented.
3. A limitation is evidenced, not merely asserted.
4. The limitation becomes a researchable gap.
5. A proposed mechanism or explanatory proposition addresses the gap.
6. Comparison/baselines could falsify the claim.
7. Results are analysed, including limits and failures.
8. The resulting knowledge can be reproduced or used beyond a single deployment.

## Minimum experimental specification

- Unit of analysis and dataset/data source.
- Inclusion/exclusion and split strategy; leakage control when relevant.
- Baselines selected for scientific relevance, not convenience alone.
- Independent variables and controlled variables.
- Dependent metrics aligned with the question.
- Scenarios including stress/domain-shift/resource conditions where relevant.
- Ablation or component analysis if claiming a multi-component mechanism.
- Repetitions, uncertainty intervals, or suitable statistical comparison when stochastic variation materially affects the claim.
- Reproduction package: code/version/configuration/seed/data-access protocol where ethically and legally feasible.
- Failure-mode and limitation analysis.

## Research ethics and data governance

This is an **S2 Informatics interpretation and AI heuristic**, not a Frascati classification rule.

- Identify data provenance, license/terms, and permitted use for datasets, models, APIs, and benchmarks.
- Identify personal, sensitive, biometric, educational, health, proprietary, or copyrighted data. Require consent, anonymisation, access controls, and ethics/IRB review when applicable.
- For human evaluation, define the evaluator population, consent/compensation, rubric, privacy protection, and reliability plan.
- Identify foreseeable safety, fairness, misuse, environmental, and domain-specific harms. State mitigation, scope boundary, or unresolved limitation.
- Disclose AI assistance in annotation, synthetic-data creation, evaluation, or writing when required by institutional, venue, or data-source rules.

## Honest status labels

| Status | Meaning |
|---|---|
| Strong research potential | A credible gap, uncertainty, method, and evaluation path are already specified. |
| Moderate research potential | A plausible research direction exists, but critical gap/method/evidence details are incomplete. |
| Weak research potential | The question or contribution is vague; substantial reframing is needed. |
| Primarily implementation-oriented | The endpoint is a deployed artifact, integration, or routine engineering activity without an established knowledge claim. |
| Insufficient evidence to judge | Required details or literature evidence are absent. |

Do not rank topics as “best” without evidence and user-specific constraints.
