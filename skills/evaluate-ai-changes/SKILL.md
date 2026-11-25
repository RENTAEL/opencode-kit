---
name: evaluate-ai-changes
description: "Treat model behavior as a versioned, probabilistic product surface rather than a single passing example."
---
# Evaluate AI Changes

Treat model behavior as a versioned, probabilistic product surface rather than a single passing example.

## Establish Authority and Objectives

1. Define user-visible quality, safety, latency, reliability, and cost objectives before changing prompts, models, retrieval, tools, or policies.
2. Identify material risks, affected users, decision owners, and the offline-versus-production boundary. Use `plan-first` when rollout, contracts, or data choices require human decisions.
3. Confirm dataset provenance, consent, minimization, redaction, retention, residency, and provider data policy. Do not send private or production data to a model or tool without explicit authorization.

## Build the Evaluation

1. Freeze a representative, versioned dataset covering normal, edge, adversarial, multilingual, refusal, and previously failed cases. Keep holdout cases separate from prompt development.
2. Capture the current prompt, model, parameters, retrieval configuration, tool schemas, and routing logic as the baseline.
3. Test task quality plus relevant failure modes: hallucination, unsupported claims, prompt injection, data leakage, unsafe compliance, over-refusal, structured-output validity, tool selection and arguments, retrieval relevance, citation support, and fallback behavior.
4. Use deterministic unit and contract tests for adapters, parsers, schemas, permissions, and tool execution through `tdd-loop`. Do not use model scores as a substitute for code tests.
5. Run repeated trials or fixed seeds where supported. Report distributions, confidence intervals or variance, regressions by slice, and every failed case instead of selecting the best sample.
6. Compare token use, end-to-end latency, rate and context limits, provider availability, and monetary cost against the baseline.

## Decide and Roll Out

1. Define acceptance thresholds before viewing final results. Separate offline evaluation success from production readiness.
2. Version prompts, datasets, model settings, and graders. Record enough trace data to reproduce a result without retaining unnecessary sensitive content.
3. Use canaries or shadow traffic when authorized, with monitoring, fallback, rollback, and kill criteria. Never exercise live users, send external messages, or incur material cost without explicit authority.
4. Report the decision, evidence, regressions, uncertain slices, production coverage gaps, and rollback path. Use `verify-done` for the final implementation evidence gate.
