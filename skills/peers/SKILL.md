---
name: peers
description: "Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user."
---
# airc peers

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user.

## Execute

```bash
airc peers
```

Prints one line per paired peer. Current Rust output is the verification
truth: `<peer-id> <public-key>`.
Rich names, runtime kind, project scope, last-seen status, and live/stale
readiness belong to the roster projection follow-up.

## When to use

- Before sending ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm the peer name you want is actually paired.
- When coordinating work, confirm the peer identity you expect is enrolled.
- Debugging "who am I actually talking to?"

## Notes

- This is the IRC-shaped public command. `airc peer list` is the lower-level structured equivalent.
- Peer trust rows are loaded from the ORM-backed trust store each call.
- Cleanup belongs to typed drain/roster workflows, not ad hoc `--prune` behavior.
