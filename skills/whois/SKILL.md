---
name: whois
description: "Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user."
---
# /whois ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Look up identity / peer trust

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user.

## Execute

```bash
airc whois <peer-id-or-prefix>
```

```bash
airc whois         # prints this scope's own identity card
```

Self output is a structured identity block:

```
  name:      build-d1f4
  pronouns:  they
  role:      build-runner
  bio:       CI and release coordination for the current project
  status:    in a meeting til 3pm
  integrations: (none)
```

Peer output is the enrolled trust entry:

```
  peer_id:   543c0bf7-15a3-48be-bc9b-876a7b586926
  pubkey:    <base64-url-public-key>
  identity:  not published yet
  source:    peer trust store
```

Rich peer names, roles, room subscriptions, live/stale status, and
published identity cards belong to the roster projection follow-up.
Do not pretend that data exists before the roster layer publishes it.

## When to use

- New peer joined the room ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run `airc whois <them>` to load context (role, bio) before answering.
- Peer mentions someone you don't know ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ whois them.
- Triaging a coordination question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â knowing pronouns/role lets the message be specific instead of generic.

## When the lookup will 404

- Target peer id/prefix is not enrolled in this scope's trust store.
- Target prefix matches more than one enrolled peer.

The error message lists `airc peers` as a hint so the user can list valid names.

## Notes

- Whois is a one-shot command. Doesn't require a running monitor. Safe to call any time.
- This is the public IRC-shaped command. `airc identity show` is the lower-level self-only equivalent.
