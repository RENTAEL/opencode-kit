---
name: lh-threat-modeling
description: "The first deliverable is the attack surface map, not a bug. List every way data or control ENTERS the system: public endpoints, authenticated endpoints, forms, file uploads, webhooks, message queues, URL params, headers, cookies, env, third-party callbacks, admin panels, CLI, ..."
---
## When to Use

- Beginning a security review of a system or feature (do this BEFORE `lh-code-audit`)
- Designing something new that handles auth, money, or sensitive data
- "Where are we exposed?" / "What's our attack surface?"

## Critical Patterns

### 1. Enumerate the doors before checking any locks

The first deliverable is the attack surface map, not a bug. List every way data
or control ENTERS the system: public endpoints, authenticated endpoints, forms,
file uploads, webhooks, message queues, URL params, headers, cookies, env,
third-party callbacks, admin panels, CLI, and every dependency (their code runs
as yours). An LLM in the system is a door too, and a strange one: anything the
model reads (a document, a web page, a ticket, another user's message) is
input from whoever wrote it, and anything the model can call (tools, queries,
shell) is a sink that input can now aim at. The vulnerability you miss is
almost always on a door that wasn't on anyone's diagram ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the forgotten legacy
endpoint, the internal API assumed private, the debug route left in.

### 2. Draw the trust boundaries ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â value lives at the crossings

A trust boundary is any line where data or control passes between zones of
different privilege: internetÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Âserver, serverÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Âdatabase, serviceÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Âservice,
user-spaceÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Âadmin, your-codeÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Âdependency. Mark them all. Every boundary is where
a check must exist and where its absence is a vulnerability. Most real breaches
are one missing check at one boundary everyone assumed the OTHER side was
guarding ("the frontend validates it" / "the gateway authenticates it").

### 3. Model the adversary explicitly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â who, and what do they want

Vague "hackers" produce vague reviews. Name the threat actors and their goals
for THIS system:

| Actor | Wants | Typically reaches for |
|-------|-------|----------------------|
| Unauthenticated outsider | Any foothold, data, defacement | Public endpoints, injection, default creds, exposed configs |
| Authenticated user | OTHER users' data, privilege escalation | IDOR/authz gaps, mass assignment, tenant isolation holes |
| Malicious insider / stolen token | Reach beyond their role | Over-broad permissions, missing audit, secret sprawl |
| Supply chain | Run code inside your trust | Compromised deps, typosquats, poisoned build |
| Content author (prompt injection) | Make YOUR model act for them | Instructions hidden in data the LLM reads; tool calls the model can make; secrets in its context |

The most under-tested actor in most apps is the authenticated user attacking
OTHER authenticated users ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â because "they're logged in" gets mistaken for
"they're trusted".

### 4. Follow the sensitive data, end to end

Pick the crown jewels (credentials, tokens, PII, payment data, the business's
core records) and trace each one's full lifecycle: where it enters, every hop
it travels, where it rests, where it's logged, who can read it, when it's
deleted. Vulnerabilities cluster where sensitive data goes somewhere nobody
intended ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â into logs, into error messages, into a cache, into an analytics
payload, into a URL that ends up in browser history.

### 5. STRIDE as a checklist, not a religion

Walk each boundary/component against the six question-classes so you don't
tunnel on injection and miss the rest: **S**poofing (can identity be faked?),
**T**ampering (can data/code be altered?), **R**epudiation (can actions be
denied / is there an audit trail?), **I**nformation disclosure (what leaks?),
**D**enial of service (what's cheap to exhaust?), **E**levation of privilege
(can they become more than they are?). One pass per boundary catches the
categories a code-first review skips.

### 6. Output: a prioritized map that aims the audit

The threat model's job is to point the [lh-code-audit](../lh-code-audit/SKILL.md) at
the highest-risk surfaces first (impact ÃƒÆ’Ã¢â‚¬â€ exposure ÃƒÆ’Ã¢â‚¬â€ likely-weakness). Deliver:
the door list, the boundaries, the actor/goal pairs, and the ranked "look here
first" list. A threat model that doesn't change where you spend the next hour
was a documentation exercise, not analysis.

## Resources

- Sibling skills: [lh-code-audit](../lh-code-audit/SKILL.md) (verifies the model's
  suspicions against real code), [lh-remediation](../lh-remediation/SKILL.md)
- Adversarial re-reading of the dev's boundary map:
  [senior-dev/lh-fullstack-boundaries](../../../senior-dev/skills/lh-fullstack-boundaries/SKILL.md);
  functional-path cousin: [qa/lh-flow-hunting](../../../qa/skills/lh-flow-hunting/SKILL.md)
