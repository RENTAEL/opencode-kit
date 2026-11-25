---
name: list
description: "List rooms or invites in airc. NOTE: not available in the rust-rewrite yet — no airc list/ls verb exists; report that instead of guessing."
---
# /list ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what's on the substrate

> ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â **Not available in rust-rewrite yet** (TODO: remove this skill or port the
> command). There is no `airc list` / `airc ls` verb that enumerates rooms or invites
> on your gh account. There is currently **no direct "list all rooms" command.**

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user.

## Nearest real alternatives

| You want | Real command |
|---|---|
| The current room (name + wire + channel) | `airc room` |
| Switch to / derive a room by name | `airc room <name>` |
| Enrolled peers in this scope | `airc peers` |
| Account-mesh discovery (same-account cross-machine) | `airc registry sync` |

```bash
airc room              # print the current room
airc peers             # list enrolled peers
airc registry sync     # one publish+refresh against the gh-gist rendezvous; prints who was enrolled
```

`airc registry sync` is the closest thing to "what's reachable on my account" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it
runs the account-registry publish+refresh and prints what was published and who was
enrolled. It is not a room catalog.

## When this comes up

- Before `/join` you wanted to see what's alive. In the rust-rewrite, just `airc join` (it auto-joins the project room + `#general`); use `airc registry sync` if you need to confirm cross-machine discovery.
- To confirm the room you're in, use `airc room`.

## Notes

- A full room/invite catalog command is not ported. Do not invent flags on `airc room` / `airc registry` to fake one ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â surface the limitation to the user instead.
