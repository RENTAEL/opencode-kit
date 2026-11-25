# Example: CNN Plant-Disease App

## Input

“Building a plant-disease diagnosis app using a CNN.”

## Diagnosis

The current claim is **primarily implementation-oriented**. A CNN application and functioning diagnosis UI do not establish a software advance, a research gap, or uncertainty. This is not a claim that software or CNN work cannot be R&D.

**Frascati basis:** Using software for a new application/purpose alone is not an advance; known-tool websites/software are listed exclusions. Chapter 2, §§2.70-2.72, pp. 67-68.

## Research transformation

**Illustrative direction only, not an established gap or method:** Performance may degrade when a classifier trained on controlled leaf images is used on field images with different lighting, occlusion, background, and device characteristics.

**Evidence still needed:** A literature review and preliminary benchmark must establish that this domain-shift limitation applies to the chosen crop/datasets and is not already adequately addressed.

**Candidate research question:** To what extent does controlled-to-field domain shift degrade plant-disease classification, and can a specified continual/domain-adaptation mechanism reduce degradation against supervised fine-tuning, source-only, and existing adaptation baselines?

**Candidate hypothesis:** If the proposed mechanism selectively adapts features using [defined signal], then field-domain macro-F1 will improve over named baselines without unacceptable forgetting on the source domain.

**Experimental design:**

- Data: controlled and field image datasets, class-balanced splits, no plant/image leakage.
- Baselines: source-only CNN, ordinary fine-tuning, and relevant published adaptation baseline.
- Variables: adaptation mechanism, shift severity, labelled target-data budget.
- Metrics: macro-F1, per-class recall, calibration, source-domain retention, compute cost.
- Analysis: component ablation, repeated seeds/confidence intervals, error categories by lighting/occlusion/background.
- Reproducibility: fixed splits/seeds/configurations and data-access instructions.

**Expected knowledge contribution:** Evidence about the failure boundary of controlled-image training under field shift, and evidence for or against the specified mechanism. The app is a practical artifact, not the primary claimed contribution.
