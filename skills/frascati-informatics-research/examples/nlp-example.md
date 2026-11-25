# Example: NLP

## Weak starting idea

“Building a sentiment-analysis chatbot for Indonesian text.”

## Researchable direction

Study whether a defined discourse/context representation improves robustness of Indonesian sentiment classification for code-mixed, negated, and implicit-opinion text compared with token-only and contextual-language-model baselines.

## Candidate questions

1. Which error categories dominate existing baseline failures on the defined corpus?
2. Does the proposed representation improve macro-F1 and calibration on those categories without harming ordinary cases?

## Design

- Dataset: documented annotation guideline, train/validation/test split, code-mixing and negation subsets.
- Baselines: majority, established Indonesian transformer, and a relevant published method.
- Variables: representation components and training regime.
- Metrics: macro-F1, calibration, category-level performance; paired/repeated comparison where appropriate.
- Analysis: ablation and qualitative error taxonomy.

## Contribution boundary

Training a known model and serving it as a chatbot is practical work. The potential research contribution is evidence about a stated linguistic mechanism and its boundary conditions.
