---
name: DavidWanm-stable_operation_skill
description: "When rules conflict, apply in this order:"
---
# Stable Operation Skill

## Terms (defined once, used everywhere)

- **ÃƒÂ¥Ã‚Â­Ã‹Å“ÃƒÂ©Ã¢â‚¬Â¡Ã‚ÂÃƒÂ¤Ã‚Â»Ã‚Â£ÃƒÂ§Ã‚Â Ã‚Â (existing code)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â any file, function, export, endpoint, or config that exists before you start this task. One word, one meaning: anything you did not create in this task is existing code.
- **ÃƒÂ¤Ã‚Â»Ã‚Â»ÃƒÂ¥Ã…Â Ã‚Â¡ÃƒÂ¨Ã…â€™Ã†â€™ÃƒÂ¥Ã¢â‚¬ÂºÃ‚Â´ (task scope)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the minimal set of files you must touch to complete the user's request. Define it explicitly before editing: "I will touch: X, Y. I will not touch: Z."
- **ÃƒÂ¥Ã‚Â­Ã‹Å“ÃƒÂ©Ã¢â‚¬Â¡Ã‚ÂÃƒÂ¤Ã‚Â¿Ã‚ÂÃƒÂ¦Ã…Â Ã‚Â¤ (existing-code protection)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the set of rules below that stop existing code from breaking.

## Priority (resolves all conflicts)

When rules conflict, apply in this order:

1. **User's explicit instruction** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always wins. If the user says "rewrite this function", you rewrite it. This overrides every rule below.
2. **Task scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â files inside the declared task scope may be edited freely.
3. **Existing-code protection** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rules for anything outside task scope.

A user instruction that names a file or function and states what to do is "explicit". An instruction that only names a goal ("make it better") is NOT explicit and does not grant permission to change existing code.

## Core Principle

Existing code must remain working. Never sacrifice a verified feature to add a new one.

## Rules

### 1. Add before you change

- Prefer new files over editing existing ones.
- Add new functions/classes instead of rewriting existing ones.
- Append new logic at the END of existing functions, never in the middle.
- New parameters must have defaults that preserve existing behavior.
- If a task that needs one file has you editing five, stop and reconsider ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â you have left your task scope.

### 2. Never delete or repurpose existing code (outside task scope)

- Do not delete or comment out existing code unless explicitly asked.
- Do not rename existing exports, functions, types, endpoints, or files.
- Do not change existing signatures without backward-compatible defaults.
- Do not give an existing function a new meaning; add a new function.

### 3. Preserve behavior, not just syntax

Same inputs must produce the same outputs:

- Existing tests keep passing.
- API responses, CLI output, error messages, edge cases stay the same.
- File paths, imports, config keys remain valid.
- Timing, ordering, side effects you do not understand must not change.

### 4. Gate behavior changes per user intent

If a new feature changes behavior that existing code depends on, wrap it in a feature flag. The flag's default is decided by the USER'S intent, not a fixed rule:

- User wants the new behavior now ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ default ON, but keep the old path reachable via the flag.
- User wants backward compatibility ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ default OFF.
- State the flag default out loud before you implement it.

### 5. Existing-code modification protocol

This replaces any "ask first" wording. If the task requires changing existing code outside task scope:

1. STOP.
2. State exactly which code will change and why.
3. Describe the risk and the user's alternatives.
4. Wait for an explicit "yes / go ahead". A nod is not consent; require a clear instruction.

### 6. Verify before you claim done

Prerequisites: this protocol assumes a git repository. If there is NO git, skip to "no-git fallback" at the end.

1. **Before you edit:** make a baseline. Commit any current work or record `git status` output. You cannot diff against a state you never captured.
2. After editing, run `git diff` and read your own diff line by line. Every changed line must be inside task scope.
3. Revert any change outside task scope.
4. Run the test command. If the project has no test command, or you do not know it, SAY SO and ask the user ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not skip silently.
5. Confirm no file was deleted that existed at baseline.
6. If you cannot run tests, state that explicitly. Never claim tests pass without running them.

### 7. Rollback

1. If you broke existing behavior, decide first: is the break in an uncommitted edit, or in a commit?
   - **Uncommitted:** restore from baseline with `git checkout -- <file>` (this discards your new work too ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-do the new feature after restoring).
   - **Committed:** `git revert <commit>` to undo in a new commit, preserving history.
2. Tell the user what broke and what you did.
3. Do not "fix" a break by rewriting more existing code.

## Decision tree (apply in order)

```
Is the user explicitly ordering the change?
  ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ YES ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ do it. Done.
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ NO  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Is the change inside task scope?
            ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ YES ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ do it, following Rules 1-3.
            ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ NO  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ It touches existing code outside scope.
                      ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Follow Rule 5: STOP, state plan, ask, wait for yes.
```

## Scope of protection

Protects ALL existing artifacts, not just source code:

- configuration files
- database migrations
- data files and fixtures
- documentation
- CI/CD configs
- build scripts

## Examples

### Good ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â additive

```python
# existing.py
def render_dashboard(options):
    # ... existing logic unchanged ...

    # appended at the end only:
    if options and options.enable_new_widget:
        _render_new_widget()
```

### Bad ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â destructive

```python
# FORBIDDEN: rewrote the existing function body, old behavior gone
def render_dashboard(options):
    # brand new logic
```

### Good ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â correct priority: explicit instruction wins

> User: "rewrite render_dashboard to use the new data source."
> Model: rewrites render_dashboard as instructed. Other files untouched.

### Good ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ask first (existing code outside scope)

> User: "add a download button to the dashboard."
> Model: "render_dashboard is existing code. I'll add the button by appending a new renderer ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â file gains ~10 lines, existing logic untouched. OK to proceed?"
> (waits for explicit approval before editing)

### Bad ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â silent deletion

```javascript
// FORBIDDEN: commenting out a shipped function
// export function legacyTotals() { ... }
```

## Final checklist

- [ ] Task scope declared before editing.
- [ ] Baseline captured before editing (commit or `git status`).
- [ ] Every diff line is inside task scope.
- [ ] No file was deleted.
- [ ] No export/function/type/endpoint removed or renamed (outside scope).
- [ ] Tests pass ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or I stated clearly I could not run them.
- [ ] Existing-code modification was approved by the user first.

## No-git fallback

If the project is not a git repository: before editing, save copies of every file you will modify to a temp location. After editing, diff your version against the saved copy and verify only intended lines changed. Delete the temp copies only after the user confirms.
