# Example: Edge AI

## Weak starting idea

“Deploying a classification model to a Raspberry Pi.”

## Diagnosis

Primarily implementation-oriented as stated. Deployment may be an engineering deliverable, but it does not itself establish an advance or uncertainty.

## Researchable direction

Investigate whether a defined adaptive inference policy can maintain a target accuracy/calibration level under energy, thermal, and latency constraints better than fixed quantisation, fixed early exit, and dynamic-baseline policies.

## Experimental design

- Hardware: named board/sensor/runtime; document clocks, power measurement, and thermal protocol.
- Workloads: representative data streams and resource-stress scenarios.
- Baselines: full precision/fixed quantisation/fixed early exit/relevant adaptive method.
- Outcomes: accuracy, macro-F1, calibration, latency distribution, energy per inference, thermal behaviour.
- Analysis: policy-component ablation; repeat measurements and report variance.
- Transferability: package runtime versions/configuration and clearly delimit hardware scope.

## Contribution

The potential contribution is evidence about an explicit adaptation mechanism and accuracy-resource boundary, not merely a deployed model.
