---
name: uninstall
description: "Uninstall airc. NOTE: not available in the rust-rewrite yet — no airc uninstall/teardown --all verb exists; removal is a manual sequence."
---
# airc uninstall

> ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â **Not available in rust-rewrite yet** (TODO: remove this skill or port the
> command). There is no `airc uninstall` verb (and no `airc teardown --all`) in the
> rust-rewrite. Removal is a manual sequence, not a single subcommand.

**Destructive ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm with the user before doing any of this.**

## Nearest real path (manual)

1. Stop the running daemon for each scope you've joined:
   ```bash
   airc stop
   ```
   (`airc stop` only stops the current scope's daemon ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â repeat per scope/home.)
2. Delete the install directory by hand (e.g. `~/.airc/src` or wherever the binary was
   installed) and any `airc` shim on `PATH`.
3. Remove airc-owned skill directories under `~/.claude/skills/` (and `~/.codex/skills/`) by hand.
4. Per-project `.airc/` state dirs (identity keys, peer records, message logs) survive
   unless you delete them manually ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â there is no `--purge` flag.

None of this is automated by `airc` in the rust-rewrite; surface that to the user
rather than running a dead command.

## When this comes up

- The user says "uninstall airc" / "remove airc". Walk the manual steps above; do not run `airc uninstall`.

## Reinstall

The standard one-liner re-installs cleanly:

```bash
curl -fsSL https://raw.githubusercontent.com/CambrianTech/airc/main/install.sh | bash
```

## Notes

- Do not invent `airc uninstall` / `airc teardown --all` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â neither exists in the rust-rewrite.
