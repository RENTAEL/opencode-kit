# senior-prompt-engineer (Claude Code Skill)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A63D2)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)


A Claude Code Agent Skill that makes Claude behave like a **senior prompt
engineer**: before doing any real work, it silently rewrites your short/vague
request into a comprehensive spec, then executes against it - and it **learns
from mistakes** and edits its own memory when a result isn't what you wanted.

Built by analyzing multiple full-length prompt-engineering video courses and
cross-checking the techniques against current best practices (Anthropic, OpenAI,
promptingguide.ai, IBM, and prompt-framework references).

## What it does
- Turns generic prompts into senior-level specs (Role, Goal+success criteria, Context, Inputs, Method, Output format, Constraints).
- Asks focused clarifying questions when critical info is missing, or states explicit assumptions.
- Applies the right technique automatically: few-shot, chain-of-thought, tree-of-thought, decomposition/chaining, self-critique, anti-hallucination guardrails.
- Has domain playbooks for **apps, websites, UI/UX, presentations, code, research, data analysis**.
- **Self-corrects:** when you say a result was wrong / not expected / "try again", it diagnoses the prompting gap, fixes it, and appends a rule to `LEARNINGS.md` (and updates domain playbooks) so it won't repeat the mistake.

## Install

**Personal (all your projects):**
```
~/.claude/skills/senior-prompt-engineer/
```
**Project (this repo only):**
```
<your-project>/.claude/skills/senior-prompt-engineer/
```
Copy the whole `senior-prompt-engineer/` folder (with `SKILL.md`, `LEARNINGS.md`,
and `references/`) into one of those locations. Claude Code auto-discovers it and
loads it when a request matches its description. The folder name is the command:
`/senior-prompt-engineer`.

> Also compatible with other agents that support the open Agent Skills / `SKILL.md`
> format. `references/` files are read on demand (progressive disclosure).

## Files
```
senior-prompt-engineer/
├── SKILL.md              # Core workflow + self-learning loop (always loaded)
├── LEARNINGS.template.md # Committed seed for the memory file
├── LEARNINGS.md          # LOCAL, git-ignored memory (auto-created from seed; never committed)
├── README.md             # This file
├── LICENSE               # MIT
├── .gitignore            # Ignores LEARNINGS.md + OS junk
└── references/
    ├── techniques.md                    # Full technique library
    ├── frameworks.md                    # GRASP+Q, CRAFT, CO-STAR, TCREI, RTF...
    ├── domain-playbooks.md              # Per-domain spec checklists
    ├── anti-hallucination-and-quality.md# Grounding + pre-delivery QA
    └── examples.md                      # Before/after transformations
```

## How the self-learning works
1. On first run, if `LEARNINGS.md` is missing, Claude creates it from `LEARNINGS.template.md`.
2. Every run, Claude reads `LEARNINGS.md` and applies its rules.
3. When you flag a bad result, Claude diagnoses the root cause as a *prompting gap*, fixes the output, and appends a structured rule to `LEARNINGS.md`.
4. Domain-wide misses also update `references/domain-playbooks.md`.
Over time the skill gets measurably better at your specific needs.

### Privacy of learnings (important for maintainers)
`LEARNINGS.md` is **git-ignored**, so your personal, machine-specific learnings are
never committed or pushed to the public repo. Only the clean seed
(`LEARNINGS.template.md`) is tracked. This means:
- Each person who clones the repo starts from the same seed and grows **their own**
  local `LEARNINGS.md` on their machine.
- The file **does not develop universally** in the repo - your private corrections
  stay yours.

If you already committed `LEARNINGS.md` in an earlier push, stop tracking it once:
```
git rm --cached LEARNINGS.md
git commit -m "Stop tracking local LEARNINGS.md; keep only the seed template"
```

## License
MIT - see `LICENSE`. Copyright (c) 2026 arush mukundan.

## Tip
To force it explicitly, start a message with `/senior-prompt-engineer` or say
"upgrade this prompt first, then build it."
