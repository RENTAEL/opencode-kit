---
name: smart-git-automation
description: "Use this when you want a faster, smarter git workflow that groups changes logically and reduces manual confirmation overhead."
---
## What I do
- Intelligently detect and group related changes
- Auto-generate descriptive branch names from changes
- Streamlined workflow: scan ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ branch ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ push ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ PR with fewer prompts

## When to use me
Use this when you want a faster, smarter git workflow that groups changes logically and reduces manual confirmation overhead.

## Workflow Steps

### 1. Smart Detection & Grouping
Run in parallel:
- `git status` - check what's changed
- `git diff --stat` - see file modification summary
- `git diff --name-only` - list changed files only
- `git diff --staged --stat` - see what's already staged

Analyze changes to group them logically:
- Files in the same module/directory ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ likely related
- Files that were modified together in recent edits ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ likely related
- New files that complement each other ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ likely related

Present grouped changes in a clear format, e.g.:
```
ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â Group 1: UI Components
  - src/components/Button.tsx (modified)
  - src/components/Button.test.tsx (modified)

ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â Group 2: API Layer
  - src/api/client.ts (new)
  - src/api/types.ts (modified)
```

### 2. Auto Branch Name Generation
Generate branch name from dominant change pattern:
- Use format: `<type>/<short-description>`
- Types: `feature`, `fix`, `refactor`, `docs`, `test`, `chore`
- Derive description from most significant changed file/feature
- Convert to kebab-case, max 50 chars
- Examples:
  - `feature/add-user-auth` (from auth-related files)
  - `fix/login-validation` (from validation changes)
  - `refactor/api-cleanup` (from API refactoring)

Show the proposed branch name and ask for one-word confirmation (or type alternative).

### 3. Streamlined Branch & Commit
- If not on main/master: check if current branch matches proposed name
  - If yes: stay on it
  - If no: ask to switch or create new
- Create branch: `git checkout -b <branch-name>`
- Stage changes: `git add <grouped-files>`
- Auto-generate commit message from changes:
  - First line: `<type>: <short description>` (max 72 chars)
  - Body: grouped file changes with brief descriptions
- Commit with generated message, show preview first
- Ask for one-word confirmation to proceed

### 4. Push & Optional PR
- After commit, ask: "Push to remote? (yes/no/abort)"
- If yes: `git push -u origin <branch-name>`
- Then ask: "Create PR? (yes/no)"
- If yes:
  - Check remote: `git remote -v`
  - If fork: use fork's remote (e.g., `mskadu/repo-name`)
  - Auto-generate PR description from commit messages
  - Use `gh pr create` with:
    - Title from branch name
    - Body: summary of changes + file breakdown + follow-up notes

## Key Rules
- Group related files automatically, but allow user to adjust
- Generate branch names from actual changes, don't ask user to name them
- Reduce confirmations: ask for one-word answers or single confirmation points
- Never commit secrets, credentials, or large binaries
- Check if GitHub repo exists before PR creation
- Skip PR step if user says "no" at any point
- If branch already exists with changes, offer to amend or add new commit
