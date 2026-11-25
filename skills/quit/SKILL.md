---
name: quit
description: "Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user."
---
# /quit ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Leave the current airc room

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user.

In the rust-rewrite there is no `airc quit` verb. Leaving while keeping your identity
is `airc part` (leave the current room without deleting identity or trust). If you
also want this scope's daemon stopped, follow with `airc stop`.

## Execute

```bash
airc part        # leave the current room, keep identity + trust
airc stop        # (optional) also stop this scope's daemon
```

`airc part` with no room leaves the current default channel. Your identity, keys,
peers, and event history are preserved on disk. `airc stop` then shuts the local
daemon down gracefully (still no state wipe).

## When to use

- You want to step out of the current room cleanly without losing your airc identity.
- You're done in this scope for now and want the daemon stopped too (`airc part` then `airc stop`).

## Differences from related commands

- `/part` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â leave the current room, keep identity + trust. This `/quit` is the same primary action plus an optional `airc stop`.
- `airc stop` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â stops this scope's daemon; preserves all on-disk state. Does NOT leave the room on its own.

> ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â The pre-rewrite `/quit` cleared saved pairing so the next join went "fresh", and
> `/teardown --flush` wiped identity entirely. Neither has a CLI verb in the
> rust-rewrite ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `airc part` leaves the room, `airc stop` stops the daemon, and there
> is **no state-wipe subcommand**. A from-scratch identity is a manual reset of the
> scope's `$AIRC_HOME` directory.
