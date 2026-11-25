# stable-operation-skill

<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README.en.md">English</a>
</p>

An opencode skill that stops the AI from wrecking your existing code when it adds new features.

## The problem

Classic AI coding fail: you ask for "CSV export support", and it refactors the whole service layer. The export works, but the existing order query endpoint returns 500, and the changes are scattered across eight files under a commit message that just says `feat: add CSV export`.

This skill doesn't aim to make the model write smarter code. It has one job: **keep the old stuff working**. It doesn't change what the model can do, only how it behaves when editing.

## How it works

Three concepts, one decision:

- **Existing code** — anything that existed before the task: files, functions, endpoints, configs. If you didn't create it in this task, it's existing code.
- **Task scope** — the minimal set of files needed to complete the request. The model must state this before editing: "I'll touch X and Y, not Z."
- **Priority** — conflicts resolve as `explicit user instruction > task scope > existing-code protection`.

Before any edit, the model walks a decision tree:

```
Did the user explicitly order the change?
 ├─ yes → do it
 └─ no  → is the change inside task scope?
           ├─ yes → do it (additive only, preserve behavior)
           └─ no  → touches existing code → stop, explain, wait for approval
```

## Core rules

1. **Additive first** — new features go in new files, or appended at the end of existing functions. Don't rewrite what's there. New parameters must have defaults that keep the old behavior.
2. **Existing code is off-limits** — no deletion, no renaming, no signature changes, unless the user calls it out specifically.
3. **Behavior is conserved** — same input, same output. Tests, API responses, CLI output, edge cases all stay the same.
4. **Gate behavior changes** — wrap behavior changes in a feature flag; the default is decided by user intent, and stated out loud before implementing.
5. **Baseline first** — commit or record `git status` before editing. You can't verify a diff against a state you never captured.
6. **Verify before claiming done** — run tests, review the diff line by line, confirm no files were deleted. If you can't run tests, say so. Don't fake it.

## Install

Put the repo in opencode's skills directory:

```
.opencode/skills/stable-operation-skill/
```

Or point `opencode.json` at your skills path:

```json
{
  "skills": {
    "paths": [".opencode/skills"]
  }
}
```

Restart opencode; it loads on demand.

## When to use it

- **Good for** — iterating on a codebase that already has working code, adding features, fixing bugs.
- **Not for** — greenfield projects (nothing to protect); large authorized refactors (consider disabling it); anything requiring hard guarantees that code won't be touched (that needs git hooks or CI — a prompt can't enforce that).

## Limitations

- It's a prompt constraint, not a sandbox. The model can ignore it. Effectiveness depends on the model's instruction-following.
- Verification and rollback rely on git; in non-git repos it degrades to manually copying files before editing and diffing after.
- It protects existing code only; code the model adds is outside its scope.

## Troubleshooting

**Model still touched the wrong code?**
- Verify the skill actually loaded (there should be a log entry).
- Check your prompt for fuzzy authorization words like "clean this up" — the model reads those as permission.
- Switch to a model with better instruction-following.

**Model asking too many questions?**
- Expected. It would rather ask than break something. Say "this is fine to change" and it moves on.

**Want to lock a file down hard?**
- The skill can't do that. Use a git hook or make the file read-only.

## License

MIT.
