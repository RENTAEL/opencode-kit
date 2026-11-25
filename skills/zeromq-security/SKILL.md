---
name: zeromq-security
description: "Secure ZeroMQ transports and application messages using current mechanisms without inheriting the Guide's historical SASL/PLAIN examples as modern advice."
---
# ZeroMQ Security

## Goal

Secure ZeroMQ transports and application messages using current mechanisms
without inheriting the Guide's historical SASL/PLAIN examples as modern advice.

## Workflow

1. Write the threat model: passive observer, active MITM, unauthorized client,
   compromised broker/server, stolen device key, replay, and metadata leakage.
2. Separate identities:
   - transport/routing identity;
   - authenticated principal;
   - application/user/device identity.
3. For untrusted TCP networks, prefer current CURVE transport encryption and
   authentication with ZAP authorization where supported.
4. Pin or otherwise authenticate server/public keys; fail closed on unexpected
   key changes.
5. Keep private keys out of source, config committed to Git, logs, diagnostics,
   screenshots, and message metadata.
6. Define rotation, revocation, enrollment, recovery, and stale-key behavior.
7. If intermediaries must not read payloads, add application-layer E2EE above
   ZeroMQ transport security; brokers then route opaque ciphertext.
8. Bind authorization to the authenticated principal, never a caller-controlled
   display name or ROUTER routing ID.
9. Test wrong keys, unknown/revoked principals, replay, tampering, restart,
   rotation races, and diagnostic redaction.

## Rules

- PLAIN-style password authentication is not confidentiality.
- Do not use obsolete digest choices from Guide examples for security.
- Encryption does not solve replay, authorization, or application idempotency.
- Authenticate protocol metadata needed to prevent substitution/downgrade.
- Treat security mechanism availability and option names as runtime-specific.
