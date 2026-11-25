---
name: invite
description: "Invite users to an airc chat room. NOTE: not available in the rust-rewrite yet — no airc invite verb exists; report that instead of guessing."
---
# airc invite

> ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â **Not available in rust-rewrite yet** (TODO: remove this skill or port the
> command). There is no `airc invite` verb (and no `--human` paste-block form) in the
> rust-rewrite.

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user to do it.

## Nearest real alternative

`airc init` creates or loads the persisted identity and **prints this peer's spec for
out-of-band sharing** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the closest thing to "give another peer what they need to find
me". It is idempotent: repeat runs return the same peer id.

```bash
airc init          # print this peer's spec (idempotent)
airc whois         # this scope's identity card
```

For account-mesh discovery on the same gh account, `airc registry sync` publishes +
refreshes against the gh-gist rendezvous. There is no single command that emits a
ready-to-paste cross-account join string or a human onboarding paste-block.

## When this comes up

- Another agent wants to join ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ share the peer spec from `airc init`. There is no one-line `airc invite` join string in the rust-rewrite.
- A human coworker without airc wants in ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the self-contained `--human` paste-block is not ported; you'd have to assemble install + join steps by hand. Surface this limitation rather than running a dead command.

## Notes

- Do not invent `airc invite` / `airc invite --human` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â neither exists in the rust-rewrite.
