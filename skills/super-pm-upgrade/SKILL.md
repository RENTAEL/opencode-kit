---
name: super-pm-upgrade
description: "Upgrade helper for super-PM skills: resolves the package root via scripts/package-root.sh, verifies the super-PM SKILL.md exists, and (when needed) updates super-PM skill files via git."
---

# Super-PM Upgrade

Helper for upgrading super-PM skills.

## Resolve package root

```bash
PACK_ROOT="$(bash "<skill-dir>/scripts/package-root.sh")" || exit 2
printf 'super-pm package: %s\n' "$PACK_ROOT"
```

## Verify skill file

```bash
test -f "$PACK_ROOT/SKILL.md" && echo "SKILL.md present" || echo "SKILL.md missing"
```

## Upgrade steps

1. Resolve the package root.
2. Verify the target `SKILL.md` exists.
3. If upgrading from git: `git -C "$PACK_ROOT" pull` (or fetch/checkout the target revision).
4. Report the result with the resolved path and revision.

## Guardrails

- Never upgrade outside the resolved package root.
- Never modify git history.
