---
name: finetuning-method-selection
description: Decide whether to fine-tune at all, and route to the right method (SFT, DPO/ORPO/KTO, GRPO/RLVR, continued pretraining) and base model. Use when starting any fine-tuning effort, when unsure whether RAG or prompting would suffice, or when choosing between preference-optimization and reinforcement methods.
---
# Fine-Tuning Method Selection

This is the router skill for the fine-tuning
lifecycle: it decides whether fine-tuning is the
right tool at all, and if so, which method and
which base-model size class. Every other skill
in this plugin assumes this routing already
happened ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â start here before opening
`lora-qlora-recipes`, `preference-optimization`,
or `grpo-rlvr-training`.

## When to Use This Skill

- Starting any fine-tuning effort, before a
  framework or base model has been chosen.
- Unsure whether RAG or prompt engineering would
  solve the problem more cheaply than training.
- Choosing between preference optimization (DPO
  family) and a reinforcement method (GRPO/RLVR)
  for the same underlying task.
- Sizing a candidate model/method combination
  before committing to a run.

## Quick Reference

| Situation | Route |
|---|---|
| Facts change often (prices, docs, news) | RAG, not fine-tuning |
| Desired behavior still being figured out | Prompt engineering |
| Stable domain knowledge, ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥500MB text | CPT then SFT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see Off-Ramps First |
| Have input/output demonstrations | SFT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `lora-qlora-recipes` |
| Have preference pairs or thumbs-up/down | DPO/ORPO/KTO ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `preference-optimization` |
| Have a verifiable pass/fail signal | GRPO+RLVR ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `grpo-rlvr-training` |
| No eval harness yet | Stop ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `eval-harness-first` |

## Off-Ramps First

Most requests that sound like "fine-tune this"
are served better and cheaper elsewhere. Check
these off-ramps before opening a training run:

- **Knowledge-bound and volatile** (the gap is
  facts that change ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â prices, docs, current
  events): route to RAG, not fine-tuning. A
  fine-tuned model bakes in a snapshot; volatile
  facts go stale immediately.
- **Behavior-bound and shifting** (the desired
  behavior is still being figured out, or
  changes per request): route to prompt
  engineering. Fine-tuning locks in a behavior;
  don't lock in one that hasn't stabilized yet.
- **Stable, dense domain knowledge**: this is
  where continued pretraining (CPT) enters, sized
  by how much domain text exists:

| Domain text volume | Route |
|---|---|
| <10MB | RAG only |
| 10MBÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“500MB | RAG + fine-tune |
| 500MBÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“10GB | CPT, then SFT |
| >10GB | CPT required |

CPT learning rate ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  **10% of the pretraining
LR**. CPT is guidance-only in this plugin ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
sizing and LR guidance live here, but this
plugin does not execute a CPT run.

## Method Router

Once the off-ramps are ruled out, this is the
full decision tree (verbatim from the research
this plugin is built on):

```
New FACTS?  volatile ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ RAG | stable+dense ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ CPT (LR ~10% of pretrain) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SFT
New BEHAVIOR? shifting ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ prompt-engineering | stable:
  demos ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SFT (LoRA/QLoRA, all-linear, ÃƒÅ½Ã‚Â±=2r)
  preference pairs ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ DPO (SimPO if length-bias, ORPO if memory-bound)
  unpaired ÃƒÂ°Ã…Â¸Ã¢â‚¬ËœÃ‚Â/ÃƒÂ°Ã…Â¸Ã¢â‚¬ËœÃ…Â½ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ KTO
  verifiable success ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ RLVR + GRPO (DAPO/GSPO/Dr.GRPO per failure mode)
Deploy: FP8 (Hopper+) | NVFP4 (Blackwell scale) | AWQ (older) | GGUF+imatrix (edge)
BEFORE ANY OF THIS: the eval harness must exist first.
```

Read the tree top-down: answer "new facts or new
behavior," then follow the branch that matches
the data shape in hand (demos, preference pairs,
thumbs up/down, or verifiable success/failure).
The data shape picks the method ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not the other
way around.

### Worked Routing Examples

- *"Users want the assistant to follow our
  support macros exactly."* Behavior is stable
  and demonstrable from transcripts ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ demos ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢
  **SFT**.
- *"We have pairs of good/bad responses from
  reviewer thumbs-up/down, unpaired."* ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ unpaired
  signal ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **KTO**, not DPO (DPO needs paired
  preferences).
- *"The model can already solve some of these
  math problems and we can grade correctness
  automatically."* ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verifiable success signal ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢
  **GRPO+RLVR**, and only after confirming the
  model succeeds at least sometimes (see Key
  Routing Facts below).
- *"We want the model to know this week's
  pricing page."* ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ volatile facts ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **RAG**, no
  training run at all.

## Key Routing Facts

- **Loss-function choice is low-leverage.** A
  240-H100-run study found method choice worth
  ~1 percentage point versus ~50 points for model
  scale, and zero of 20 DPO variants beat vanilla
  DPO. Don't spend a routing decision agonizing
  over DPO-variant selection ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â spend it on
  getting the data shape and scale right.
- **DPO is for taste, GRPO+RLVR is for
  reasoning.** Preference pairs that encode a
  subjective judgment (tone, style, "which answer
  is better") route to DPO. Tasks with a
  verifiable pass/fail signal (math, code, tool
  calls) route to GRPO+RLVR instead.
- **RL is not the fix for a model that never
  succeeds.** GRPO and other RL methods sharpen
  an existing capability ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they don't teach one
  from zero. If the model doesn't yet understand
  the task or output format, run SFT first; only
  bring in RL once the model succeeds at least
  sometimes.

### Common Routing Mistakes

- Reaching for fine-tuning to fix facts that
  change weekly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that's a RAG problem, and
  fine-tuning will just go stale faster than the
  source data does.
- Picking a DPO variant before checking whether
  the actual bottleneck is data quality or model
  scale ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â variant choice is the ~1pp lever, not
  the ~50pp one.
- Starting an RL run on a model that fails every
  rollout ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â route to SFT first so RL has
  something to sharpen.
- Treating CPT as the default for "the model
  doesn't know our domain" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check the data
  volume thresholds first; under 500MB, RAG or
  RAG+fine-tune iterates faster than a CPT run.

## Model Selection

Base-model choice is size-class first, family
second, and it goes stale fast ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â so it lives in
exactly one place: `references/model-catalog.md`.
That file is the only place in this plugin (and
in the DGX Spark ops plugin) that names a base
model family. Neither this skill nor
`references/memory-math.md` names one; both
describe models by size class only (for example,
"8B-class LoRA," not a model name).

The catalog is dated on purpose ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â model rankings
turn over quarterly. It carries a "last verified"
date and a refresh checklist. Before trusting a
row, check that date; if stale, work the refresh
checklist in the catalog before recommending a
model from it.

**Precedence when the catalog and a method skill
disagree:** the catalog's per-row Notes column
states hardware/size-class *feasibility*, not a
method recommendation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `lora-qlora-recipes`'s
LoRA vs QLoRA vs Full FT table (routed by task
shape) governs the actual method choice.

## Memory Feasibility

Before committing to a method, size it: total
memory ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  **params ÃƒÆ’Ã¢â‚¬â€ dtype bytes + optimizer
state + gradients + activations**. Work each
term for the chosen dtype and method (full
fine-tune, LoRA, or QLoRA) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â worked worksheets
and size-class examples live in
`references/memory-math.md`.

On DGX Spark specifically, unified-memory
behavior breaks the naive estimate (transient
load peaks, `nvidia-smi` underreporting, thermal
throttling on long runs). Once the
`dgx-spark-ops` plugin is installed, defer
Spark-specific feasibility calls to its
`spark-memory-thermal-ops` skill rather than
re-deriving them here.

## Related Skills

Once this skill has picked a method, hand off to
the skill that executes it:

- `lora-qlora-recipes` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SFT via LoRA/QLoRA
- `preference-optimization` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â DPO, ORPO, KTO
- `grpo-rlvr-training` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â GRPO with verifiable
  rewards

No method is selected before the eval harness
exists ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `eval-harness-first`.
