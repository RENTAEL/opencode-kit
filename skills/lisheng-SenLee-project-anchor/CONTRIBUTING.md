# Contributing

Contributions are welcome when they make Project Anchor clearer, safer, or easier to use without turning it into a heavyweight workflow framework.

## Contribution principles

Prefer changes that:

- preserve the distinction between current truth, historical rationale, and short-lived execution state;
- reduce drift, ambiguity, duplicated facts, uncontrolled retries, or premature completion;
- keep trivial changes lightweight;
- use deterministic scripts only where deterministic behavior is genuinely useful;
- keep `SKILL.md` focused and move optional detail into `references/`;
- avoid collecting chain-of-thought, full transcripts, or per-tool-call execution history.

Be cautious with changes that introduce:

- mandatory ceremony for small edits;
- fixed numeric working-set limits without strong evidence;
- a database, daemon, runtime controller, or background service;
- another long-lived source of project truth;
- generic project-management features better handled by existing tools.

## Before opening a pull request

1. Explain the concrete failure mode or usability problem being solved.
2. Show why the change belongs in this skill rather than in an external project-management/runtime layer.
3. Run a CLI smoke test:

```bash
python scripts/governance.py init --root <temp-repo> --profile generic
python scripts/governance.py new-change example-change --root <temp-repo>
python scripts/governance.py new-adr "Example decision" --root <temp-repo>
python scripts/governance.py validate --root <temp-repo>
```

4. If trigger behavior changes, add or update a case in `evals/prompts.csv`.
5. Keep examples and documentation consistent with the actual skill behavior.

## Scope test

A useful final question for every contribution is:

> Does this make the agent more reliably aligned with project intent, or does it merely add process?

If it only adds process, it probably does not belong here.
