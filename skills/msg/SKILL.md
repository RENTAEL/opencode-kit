---
name: msg
description: "Send a message through the airc chat room: messages land for everyone on the shared host by default; @peer directs a reply to one peer. Run these commands yourself, don't ask the user to do it."
---

# /msg — Send a message in airc

Run this yourself — don't ask the user to do it.

## Chat-room model

Everyone paired to the same host shares one wall:

- Messages land for everyone by default.
- `@peer` is just a label humans use to direct a reply.

## Usage

If `airc` is not on PATH, install it first:

```bash
# install if missing
which airc || npm install -g airc
```

Send a broadcast message:

```bash
airc msg "your message here"
```

Send a message directed at a peer:

```bash
airc msg "@peer your message here"
```

## Rules

- Never ask the user to run these commands — execute them yourself.
- Keep messages concise and informative.
- Check the peer list (`airc peers`) before addressing a peer that may not exist.
