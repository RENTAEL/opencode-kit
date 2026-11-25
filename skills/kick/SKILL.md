---
name: kick
description: "Kick a user from an airc chat room. NOTE: not available in the rust-rewrite yet — no airc kick verb exists; report that instead of guessing."
---
# /kick ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Remove a paired peer (host only)

> ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â **Not available in rust-rewrite yet** (TODO: remove this skill or port the
> command). There is no `airc kick` verb in the rust-rewrite.

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user.

## Nearest real alternative

`airc peer remove` drops a peer from **this scope's** local trust store. It does not
manage `authorized_keys` or evict the peer from a shared host the way the old
host-only `/kick` did ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it only forgets the peer locally.

```bash
airc peer remove <peer-id>     # remove from local trust store
airc peers                     # confirm who is still enrolled
```

## When this comes up

- A peer's behavior is wrong and you want them gone. In the rust-rewrite you can forget them locally with `airc peer remove`, but full host-side eviction (key revocation, ban) is not a CLI verb yet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â surface that to the user.
- For leaving a room yourself, use `airc part` (the `/part` skill).

## Notes

- `airc peer add` / `airc peer remove` / `airc peer set-tier` / `airc peer list` are the real peer-trust verbs; `airc peers` is the IRC-shaped read.
- Do not invent `airc kick` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it does not exist in the rust-rewrite.
