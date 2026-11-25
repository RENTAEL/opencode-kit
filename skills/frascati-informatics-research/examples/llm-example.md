# Example: LLM

## Weak starting idea

“Fine-tuning an LLM for education.”

## Diagnosis

Insufficient evidence to judge. The target task, failure mode, adaptation method, baselines, and evaluation protocol are unspecified. Fine-tuning alone is not a novelty claim.

## Researchable direction

Investigate whether a defined retrieval-and-verification policy improves factual correctness and pedagogical usefulness of Indonesian tutoring responses under curriculum-specific questions, compared with prompt-only, standard RAG, and fine-tuned baselines.

## Design constraints

- Pre-register or document the rubric, reference-answer source, evaluator protocol, and leakage controls.
- Measure factuality, citation support, pedagogical quality, refusal/uncertainty behaviour, latency, and cost.
- Blind human evaluation where feasible; report inter-rater reliability.
- Ablate retrieval, verification, and policy components.
- Report failures and safety limitations rather than only aggregate scores.

## Claim discipline

Call this a possible applied-research direction only after a literature-backed gap and qualifying uncertainty are established. The framework/LLM product remains an artifact unless the study yields transferable knowledge.
