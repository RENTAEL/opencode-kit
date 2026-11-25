---
name: cloudpress-api
description: "Activate this skill when:"
---
<!-- NOTE: the `description` above is 1003 of the 1024-character limit. Do not
     append to it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a longer value silently breaks skill activation. Any
     addition must be balanced by a cut elsewhere in the same field. -->

<!-- API SNAPSHOT: the line below is the only place this file records which
     CloudPress release its contents were verified against. The skill's own
     release version is a publish date and does not encode it. Bump this in the
     same pass that bumps package.json, .claude-plugin/plugin.json, and
     CHANGELOG.md in the cloud-press/skills repo. -->

*Verified against CloudPress platform release **2026.08.01**.*

# When to Use This Skill

Activate this skill when:
- User asks how to call a specific CloudPress API endpoint
- User asks what parameters an endpoint accepts or what a response looks like
- User asks about authentication, API keys, OAuth, scopes, or the `X-Auth-Account` header
- User asks about permissions, roles, or what their token can do
- User is debugging a 400, 401, 402, 403, 404, 409, 422, 429, 502, or 503 from the API
- User asks about async operations, task polling, registrar processes, or completion callbacks
- User asks about **billing webhooks** (outbound site-subscription lifecycle webhooks configured on a billing plan) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what events fire, the payload shape, or why a domain/registrar event didn't produce one
- User asks about **cPanel hosting accounts** through the API ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ordering, resizing, domains, passwords, control-panel sessions
- User asks about **Mailspace mail hosting** through the API ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ordering or resizing a mailspace, or managing what is inside one: mailboxes, app passwords, mail rules, vacation responses, aliases, groups, mailing lists, masked emails, mail domains and their ownership verification, deleted-mail recovery, or delivery logs
- User asks about a WordPress site's **transactional email** through the API ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sender settings, send logs, mail metrics, or the sender-DNS check
- User asks how to set up, configure, or connect the CloudPress **MCP server** (e.g. in Claude Desktop/Cowork), what MCP tools exist, or why an MCP token is rejected
- User is building an integration with CloudPress

---

# CloudPress REST API

---

## Authentication

All `/api/*` requests authenticate via an HTTP Bearer token:

```bash
Authorization: Bearer <token>
```

There are **three credential types**, all presented as a Bearer token. The server resolves which kind it is (session/API key first, then OAuth).

| Credential | Identity | Admin-capable? | OAuth scopes apply? | Notes |
|---|---|---|---|---|
| **User API key** | A user (accesses accounts that user belongs to) | If the key's `is_admin` is set | No (bypasses scope checks) | Optional IP access list (`allowed_ips`). |
| **System API key** | An account (system-managed only) | If `is_admin` | No | `system_managed` keys only; IP must be on the system access list. The account is resolved from the key's `bearer` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `X-Auth-Account` is **not** required (and is ignored). |
| **OAuth 2.1 access token** | A user, bound to one `(account, brand)` | **Never** (OAuth tokens are never admin) | **Yes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fail-closed** | Issued by the OAuth 2.1 authorization server. See [OAuth 2.1](#oauth-21). |

**Account scoping ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `X-Auth-Account`:**

```bash
X-Auth-Account: <account_guid>
```

Scopes a user API key to a single account: index endpoints then return only that
account's resources, instead of resources across every account the token's user can
access.

The endpoints that **require** the header answer **`400`**
`{"errors":["Missing X-Auth-Account"],"code":"missing_account"}` when it is absent. That
set is exactly:

- every route under `/api/orders` (including `POST /api/orders/domain`),
  `/api/subscriptions`, `/api/carts`, `/api/users`, `/api/domain_contacts`,
  `/api/domain_registrations` (including its nested `hosts` and `processes`), and
  `/api/cpanel_accounts` (including its nested `password`, `purge`, `session` and
  `domains`)
- `POST /api/sso`
- `POST /api/dns_zones` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â zone **create** only; its body carries **no** `code` key,
  just `{"errors":["Missing X-Auth-Account"]}`
- `POST /api/mailspace` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mailspace **create** only; it answers `400` with
  `code: "account_required"` and a longer message. The two codes mean the same thing on
  different routes. The nested `/api/mailspace/:mailspace_id/ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` routes do **not** inherit
  this: sent without the header, they resolve the mailspace from the ones the token's user
  can reach, and an inaccessible guid is a **`404`** with an empty body ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â deliberately
  indistinguishable from one that does not exist.

Nothing else requires it. In particular the **webhook** endpoints do not:
`GET /api/webhooks/task` needs no account at all, and `POST /api/webhooks/task/:id` has
no header check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â called with no account context it fails inside the action and returns
a **`500`**, not a `400`.

OAuth tokens always carry an account, so the header is irrelevant for them.

**Authentication failures** return **`401`** with header `WWW-Authenticate: Token realm="Application"` and an empty body. Causes: no/invalid token, IP not on the access list, the resolved account is on trial, or the `X-Auth-Account` GUID doesn't match an account the token can access. **Trial accounts cannot use the API at all** (both session and OAuth auth reject them; a user-API-key call with no `X-Auth-Account` resolves no account and so isn't trial-blocked at auth time).

There are **three** `401` body shapes:

1. the empty body above ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â also what `DELETE /api/accounts/:id` returns when the caller
   is refusing to delete their only remaining account;
2. `{"error":"invalid_token","error_description":"..."}` for an audience-bound OAuth
   token (next paragraph);
3. `{"errors":["This endpoint requires a user-scoped API key."],"code":"user_required"}`
   from the endpoints that need a user behind the credential (see [Scopes](#scopes)).

**Audience-bound OAuth tokens:** an OAuth access token minted with a `resource` (RFC 8707 audience, e.g. for `/mcp`) is rejected at `/api/*` with **`401`** `{"error":"invalid_token","error_description":"token audience is not valid for /api"}`. Only un-audienced (or `/api`-audienced) tokens work here.

**Rate limiting:** 600 requests / 10 minutes. Two details that are easy to get wrong:

- The budget is keyed on the **client IP**, not on the credential ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â several tokens
  behind one egress IP share one bucket.
- It is counted **per resource group**, not once across all of `/api` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sites, domains
  and DNS each get their own 600, so exhausting one leaves the others untouched.

Exceeding it returns **`429`** with an empty body.

The `/mcp` endpoint is the opposite on both counts: 6000 requests / 10 minutes, keyed on
the **OAuth access token** (falling back to the client IP when there is no token), so LLM
clients sharing egress IPs don't collide.

---

## OAuth 2.1

CloudPress runs a standard OAuth 2.1 authorization server. Use it for third-party apps acting on a user's behalf; use API keys for first-party/server integrations.

**Authorization server metadata** (per-brand, derived from request host):

```bash
GET /.well-known/oauth-authorization-server
```

```json
{
  "issuer": "https://<host>",
  "authorization_endpoint": "https://<host>/oauth/authorize",
  "token_endpoint": "https://<host>/oauth/token",
  "revocation_endpoint": "https://<host>/oauth/revoke",
  "introspection_endpoint": "https://<host>/oauth/introspect",
  "registration_endpoint": "https://<host>/oauth/registration",
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "token_endpoint_auth_methods_supported": ["none"],
  "scopes_supported": ["sites:read","sites:write","domains:read","domains:write","dns:read","dns:write","mailspace:read","mailspace:write","billing:read","cpanel:read"],
  "service_documentation": "https://<host>/docs/oauth"
}
```

- **Grant types:** `authorization_code` and `refresh_token` only. **PKCE is mandatory** (`S256` only). Refresh tokens rotate (previous token revoked on use).
- **No OpenID Connect** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â there is no `/.well-known/openid-configuration`, no userinfo endpoint, and no ID tokens. The only OIDC-adjacent surface CloudPress exposes is Dynamic Client Registration (below).
- **Dynamic Client Registration (DCR, RFC 7591):** `POST /oauth/registration`. This
  server only ever issues **public PKCE clients**, but it does **not reject** a
  registration that asks for a confidential `token_endpoint_auth_method` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the
  requested value is **coerced to `"none"`** and the registration succeeds as a public
  client, echoing `"none"` back with no `client_secret`. So a client that sends
  `client_secret_post` (as some connector implementations do regardless of the
  advertised metadata) registers successfully and then uses PKCE. Per-IP limit: 50
  registrations/hour ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **`429`**
  `{"error":"too_many_requests","error_description":"registration rate limit exceeded"}`.
- **Brand isolation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â OAuth tokens only:** an OAuth access token is bound to the brand
  (hostname) it was issued under and is rejected on any other brand's hostname. The
  authorize screen only lists the user's non-trial accounts on the current brand.
  **API keys and session tokens are not brand-checked** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they authenticate on any
  brand host.

### Scopes

There are **no default scopes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every resource scope is opt-in. The complete vocabulary:

| Scope | Grants |
|---|---|
| `sites:read` | Site read + nested site reads (show/index, backups list, cache status, CDN status, variants list, tasks, edge-rules list, Shield reads, logs, **all four metrics endpoints** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â resources, CDN, Shield, transactional mail ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and the transactional-email overview and send logs). Note `POST /api/sites/:id/metrics/cdn` is a **read** despite the POST verb: the body carries the query window, and the scope it requires is `sites:read`. |
| `sites:write` | Site + nested site writes (update/destroy, backups, backup exports, cache, restart, restore, edge rules, Shield writes, certificates, site-domain CRUD, variant change, transactional-email sender settings, **lifting** a transactional-email suspension ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the endpoint is a `DELETE` that clears a hold, it does not apply one ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and the sender-DNS re-check). **Not site creation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `POST /api/sites` is a no-op stub returning `400`; sites are created by ordering one via `POST /api/orders`. |
| `domains:read` | Domains list/show/query/available; domain-registration index/show/check/suggestions; contacts/hosts/processes reads |
| `domains:write` | Domain-registration mutations; domain-contact create/update/destroy/resend; host/process writes |
| `dns:read` | DNS zones index/show/dns_stats; DNS records index/show |
| `dns:write` | DNS zone & record create/update/destroy |
| `mailspace:read` | Mailspace list/show, **and every read inside a mailspace** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mailboxes (plus the address-availability check), mailbox app-password list, mailbox mail rules, vacation responses, aliases, groups, mailing lists, masked emails, mail domains with their DNS records and verification status, the purged-mailbox recovery list, archived (deleted) mail **including the raw-message download**, and delivery logs. This is not a metadata-only scope ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read the warning below before granting it. |
| `mailspace:write` | Mailspace purchase/resize/delete, **and every mutation inside a mailspace** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mailbox create/update/delete/restore and irreversible force-delete, app-password mint/update/revoke, mail-rule create/update/delete/toggle/move/adopt, vacation responses, aliases, groups, mailing lists, masked emails, mail-domain CRUD with DNS re-check and ownership verification, purged-mailbox restore, archived-mail restore/delete, and the immediate permanent purge of a soft-deleted mailspace. |
| `billing:read` | Orders index/show; subscriptions index/show; carts show |
| `cpanel:read` | cPanel account list/show; cPanel account domain **list** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reads only |

**`GET /api/about`** accepts any valid token regardless of scope.

**There is no `cpanel:write` scope and no `billing:write` scope.** Do **not** read that
as "OAuth cannot spend the account's money" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it can.

- **What the missing scopes really cover.** Direct order placement (`POST /api/orders`,
  `POST /api/orders/domain`, `POST /api/domain_registrations/:id/registrant_change`) and
  the cPanel writes (account order/resize/cancel, password, purge, control-panel
  session, domain add/remove) declare no scope at all, so they fail closed for **every**
  OAuth token. That much is true.
- **What is NOT covered ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read this before granting either scope.** Two scopes that do
  exist reach a purchase:
  - **`mailspace:write`** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `POST /api/mailspace` buys a new mailspace, and
    `PATCH /api/mailspace/:id` resizes one.
  - **`sites:write`** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `PATCH /api/sites/:id` with a `plan` parameter changes the
    site's plan (an up- or downgrade of the recurring subscription).

  Each of those builds a cart and charges the account's saved default payment method
  **off-session** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no interactive confirmation step, no separate billing scope, and the
  `202` comes back whether the charge succeeded or was declined.

**Consequence:** an OAuth token holding `mailspace:write` or `sites:write` can spend the
account's money and change its recurring bill. Treat those two as billing-capable when
deciding what to request or grant. Only the *order-placing* and *cPanel* endpoints listed
above are genuinely out of OAuth's reach.

**A second consequence ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â data access, not only money.** The two `mailspace` scopes are
often assumed to cover subscription metadata. They do not:

- **`mailspace:read` reaches mail itself.** It lists a mailspace's mailboxes, reads its
  delivery logs, and ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â where the mail platform's archive feature is available ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â lists a
  mailbox's deleted mail and **downloads a raw message**.
- **`mailspace:write` reaches irreversible destruction.** Mailbox force-delete erases the
  mail the ordinary restore path exists to bring back, and the mailspace purge destroys a
  soft-deleted mailspace immediately rather than at the end of its retention window.

There is no narrower mail scope to request instead, and no separate scope for either
capability. Grant `mailspace:read` only where reading a customer's mail is intended, and
`mailspace:write` only to a client that genuinely administers mail.

**Endpoints unavailable via OAuth** (no scope declared ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fail-closed): account CRUD & roles, API keys, users, `user_roles`, global `tasks`, SSO (site and top-level), webhooks, the domain-order endpoints (`POST /api/orders/domain`, `POST /api/domain_registrations/:id/registrant_change`), **every cPanel write** (account order/resize/cancel, password, purge, control-panel session, domain add/remove), and `POST`/`PATCH`/`DELETE` on `/api/orders`. These require a session or API-key credential.

Several of those blocked endpoints additionally reject a **system account-bearer** key
(an account with no user) with **`401`**
`{"errors":["This endpoint requires a user-scoped API key."],"code":"user_required"}`.
The endpoints that do this are: `POST /api/orders/domain`,
`POST /api/domain_registrations/:id/registrant_change`,
`POST /api/cpanel_accounts`, `PATCH`/`DELETE /api/cpanel_accounts/:username`, and the nested cPanel
`password`, `purge`, `session`, and domain `create`/`destroy` endpoints.

### Scope enforcement

Session and API-key credentials **bypass** scope checks entirely. For OAuth tokens:
- Missing the required scope ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **`403`**, header `WWW-Authenticate: Bearer error="insufficient_scope", scope="<required>"`, body `{"error":"insufficient_scope","error_description":"requires scope: <required>"}`.
- Endpoint declares no scope (OAuth-blocked) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **`403`** `{"error":"insufficient_scope","error_description":"endpoint not available via OAuth"}`.

Removing a user's role on an account revokes their OAuth tokens and sessions for that account.

---

## Base URL & Conventions

- **Host:** `https://my.cloudpress.com` is the default CloudPress host, and every example in this document uses it. White-label brands are served on their own hostname (e.g. `brand.example.com`) with **identical paths** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â substitute your brand's host throughout, including the `/mcp` and `/oauth/*` URLs.
  Brand-locking applies to **OAuth access tokens only** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one issued on a given brand's
  hostname is rejected on any other. API keys and session tokens are not brand-checked
  and authenticate on any brand host.
- All API routes are under `/api/`. All responses are JSON.
- Resource IDs are GUIDs (UUID format). The complete list of exceptions:
  - task IDs, volume IDs, DNS record-type codes and `domain_contact` IDs are **integers**;
  - a **cPanel account** is addressed by its cPanel **username**
    (`/api/cpanel_accounts/:username`);
  - a **cPanel domain** is addressed by the **domain name**
    (`/api/cpanel_accounts/:username/domains/:id`);
  - a **registrar host** is addressed by its **host name**
    (`/api/domain_registrations/:id/hosts/:host_name`);
  - a **cart** is addressed by an **opaque token**, not a GUID
    (`/api/carts/:token`).
- Timestamps are ISO 8601, UTC.
- Async operations return **`202 Accepted`**, but the *body* varies by endpoint ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see
  [Async Patterns](#async-patterns) for the enumerated shapes and what to poll.
- **Pagination:** exactly five index endpoints paginate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `GET /api/domains`,
  `GET /api/subscriptions`, `GET /api/dns_zones`, `GET /api/orders`, and
  `GET /api/cpanel_accounts`. They accept `page` and `per_page` (default `50`, max `100`;
  values outside `1..100` are clamped). **Every other index endpoint ignores `page` and
  `per_page` and returns the full set** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't build a pager against them.

---

## Error Responses

| Status | When it occurs | Body shape |
|--------|---------------|------------|
| `400` | Missing required header; invalid/no-op params; **order & site-resize validation errors** (unknown variant/location/term/product); `no_default_payment_method`; a non-numeric `days` on mail metrics (`invalid_days`); OAuth picker/DCR errors | `{"errors":["..."]}` often with a `"code"`; OAuth: `{"error":"...","error_description":"..."}` |
| `401` | Authentication failed (no/invalid token, IP blocked, trial account, account mismatch); admin-only endpoint with non-admin credential; `DELETE /api/accounts/:id` refusing to delete the caller's only remaining account; OAuth token bound to a non-`/api` audience; a domain-order or cPanel-write endpoint called with a system account-bearer key (`user_required`) | Empty + `WWW-Authenticate: Token realm="Application"`; `{"error":"invalid_token",...}` for the audience case; `{"errors":[...],"code":"user_required"}` for the account-bearer case |
| `402` | Service suspended for unpaid invoice (dunning); registrar fee gate (privacy/registrant change) | `{"errors":["..."],"code":"service_suspended","invoice":{...}}` or `{...,"code":"payment_required","price":{...},"portal_url":"..."}` |
| `403` | Insufficient role (`{"errors":["Not Authorized"]}`); OAuth scope failure; Shield not in plan / premium required; inside a mailspace ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no edit permission (`not_authorized`), staff/dunning hold (`mailspace_suspended`), or soft-deleted (`pending_delete`) | `{"errors":["Not Authorized"]}` or `{"error":"insufficient_scope"/"shield_not_in_plan"/"shield_premium_required"}` |
| `404` | Resource not found or not accessible to this token | Usually empty (`head`); some render `{"errors":[...]}` |
| `409` | Conflict ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Bunny resource not active (`cdn_not_active`, `shield_not_active`); registrar process already in flight (`registration_busy`); mailspace not yet in the mail platform (`not_provisioned`); a verification retry on a mailspace that is already set up (`already_provisioned`) | `{"error":"cdn_not_active"}` / `{"errors":[...],"code":"registration_busy",...}` |
| `422` | Validation failure or permission restriction (e.g. inherited role, reseller-only, resize constraints); billing still settling (`billing_settling`); payment could not be initiated for an order/plan-change/domain order (`cart_pay_failed`); a site's transactional email not provisioned (`mail_not_provisioned`) or not active (`mail_not_active`) | `{"errors":["..."]}`, often with a `"code"` |
| `429` | The global rate limit (600/10min) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **empty body**. Also two per-endpoint limiters that *do* carry a body, both one run per 5 minutes: `POST /api/mailspace/:id/domains/dns_check` (per domain) and `POST /api/sites/:id/mail/dns_check` (per site, shared with the control panel) | Global: empty. The two DNS checks: `{"errors":["..."],"code":"rate_limited"}` |
| `502` | Upstream failure ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Bunny (CDN/Shield), the domain registrar, or the transactional-email provider. **The three use different body shapes**, so don't parse them with one branch. | Bunny: `{"error":"<message>"}` (a bare `error` string, no `code`). Registrar: `{"errors":["..."],"code":"..."}` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `registrar_unavailable`, `authcode_unavailable` (EPP-code fetch) or `process_unavailable` (process resend/cancel). Transactional email: `{"errors":["..."],"code":"log_search_failed"}` on `GET /api/sites/:id/mail/logs`. |
| `503` | Feature disabled (`domain-registration` flag); no registrar configured for a TLD; mail hosting not configured (`stalwart_unavailable`, on **every** `/api/mailspace/:id/ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` endpoint, reads included); transactional email not configured (`mailchannels_unavailable`); **any mail-server read or write that could not be performed** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â as distinct from one the mail server refused ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â under a per-resource code, see the mailspace read-failure convention below | `{"errors":["..."],"code":"feature_disabled"/"registrar_unavailable"/"missing_api_key"/"stalwart_unavailable"/"mailchannels_unavailable"/"mailboxes_unavailable"/"domains_unavailable"/"aliases_unavailable"/"groups_unavailable"/"mailing_lists_unavailable"/"archived_items_unavailable"/"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` |

> **Note:** there is **no longer** a generic `domains`/`backups` "feature flag ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 503" model. DNS, domains, backups, and restores are no longer feature-flag gated. The only `FeatureFlag` 503 in the API is the `domain-registration` flag. CDN/Shield availability is signaled by **`409`** (`cdn_not_active`/`shield_not_active`), and Shield plan access by **`403`** (`shield_not_in_plan`/`shield_premium_required`).

**Common error messages:**

| Error body | Cause |
|-----------|-------|
| `{"errors":["Missing X-Auth-Account"],"code":"missing_account"}` | Header required but absent (400) |
| `{"errors":["Missing X-Auth-Account"]}` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **no `code` key** | Same condition on `POST /api/dns_zones` only. Zone create renders its own body and does not carry a `code`, so a client keying on `code == "missing_account"` will miss it (400). |
| `{"errors":["Account unable to create orders."],"code":"account_cannot_order"}` | Account state prevents orders (e.g. trial with 2+ sites) (400). Both the site-order and the domain-order path send this same message **and** this `code` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â branch on the code. |
| `{"errors":["Must have reseller permissions"]}` | Reseller-only endpoint (422) |
| `{"errors":["Unable to remove an inherited role."]}` | Deleting an inherited account role (422) |
| `{"errors":["..."],"code":"no_default_payment_method"}` | Order/resize with no saved payment method (400) |

---

## Authorization & Account Model

Many 401/403 errors come from token scope or role gaps.

### Account Types

| Type | How to identify | What it can do |
|------|----------------|----------------|
| Regular | Default | Manage own resources per role flags |
| Reseller | `reseller: true` on account | Create sub-accounts, create users, manage sub-account billing |
| Admin | `is_admin` on the **user/API key** (not the account) | A broad, but **not universal**, bypass: it satisfies the view / edit / create / destroy / billing-view / WP-login checks on any account, and it can create top-level accounts. It does **not** satisfy the site-lifecycle check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see the `is_admin` role-flag row below. **OAuth tokens are never admin.** |
| Trial | `is_trial: true` | **Blocked from the API entirely** (auth returns 401) |

**Brands:** resellers can white-label via an `AccountBrand` (hostname, name, logo, theme, SMTP, support contacts). Each account belongs to a brand; the brand is resolved from the request hostname and isolates OAuth tokens.

### Role Permission Flags

Every user has a role on each account they belong to. Flags on the role:

| Flag | What it controls in the API |
|------|-----------------------------|
| `is_admin` | Full access to account operations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â overrides the other flags on this table. **One deliberate exception:** the site-lifecycle gate (below) ignores platform-staff `is_admin` entirely and requires actual membership on the account. |
| `can_edit` | PATCH/update on accounts, sites, domains, zones, registrations |
| `can_create` | POST orders / create resources |
| `can_destroy` | The `DELETE` gate on: `/api/accounts/:id`, `/api/dns_zones/:id`, and the per-site sub-resources (backups, cache, site domains, edge rules, Shield rules and access lists). A non-admin user cannot delete their **only** remaining account even with this flag ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the refusal is **`401` with an empty body**, not a `403`. |
| *(site lifecycle)* | **`DELETE /api/sites/:id` is not gated on `can_destroy`.** It requires the **billing** role on the account: either `is_admin`, or `billing` **and** `can_edit` together (walked up to the billing account for children that inherit billing). Platform-staff `is_admin` on the *user* grants nothing here ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the caller must be a member of the account. `DELETE /api/cpanel_accounts/:username` uses the same gate. |
| `billing` | View billing/pricing data; with `can_edit`, manage billing |
| `wp_login` | Generate SSO URLs for **any** WP user ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â without it, SSO is limited to WP users the token's user is explicitly linked to |

A suspended user fails every permission check. List available roles: `GET /api/user_roles`.

### Role Inheritance

A user granted a role on a parent account automatically receives the same role on all child accounts (cascaded asynchronously). Inherited roles carry `inherited_from` in the response and cannot be removed at the child level ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â change the parent role to update all descendants (deleting an inherited role returns **`422`**).

### Permission Check Flow

1. Is the token valid, IP allowed, account not on trial, not rate-limited?
2. For OAuth tokens: does the token's scope cover this action? (Session/API keys skip this.)
3. Is `X-Auth-Account` required by this endpoint?
4. Does the token's user have the required role flag on the target account?
5. For reseller-only operations: is the account a reseller?
6. For per-site tool endpoints: is the site dunning-suspended? (ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 402)

### Reseller Capabilities

With a reseller account and `X-Auth-Account` set to it:
- `POST /api/accounts` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create sub-accounts
- `POST /api/users` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create managed users (returned with an auto-generated password and API token)

Sub-accounts inherit the reseller's billing plan.

### Dunning Suspension

When a site's invoice is unpaid, per-site **show/update/destroy and tool endpoints** return **`402`**:

```json
{
  "errors": ["This service is suspended because an invoice is unpaid."],
  "code": "service_suspended",
  "invoice": { "number": "INV-123", "hosted_url": "https://..." }
}
```

List endpoints are not blocked ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they surface `dunning_suspended: true` on the site instead.

---

## Async Patterns

### Tasks

Most provisioning operations are async and answer **`202 Accepted`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â but there is **no
single envelope**. Do not assume a task reference; several `202` bodies carry no task id
at all, and some carry nothing. The shapes actually in use:

| `202` body | Endpoints |
|---|---|
| **Empty** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no body | site rename (`PATCH /api/sites/:id` with only `name`); `POST /api/sites/:id/restart`; `PATCH /api/sites/:id/restores/:id`; `PATCH`/`DELETE /api/sites/:id/backups/:id`; `PATCH`/`DELETE /api/sites/:id/domains/:id`; `DELETE /api/dns_zones/:id`; `PATCH`/`DELETE /api/dns_zones/:zone_id/records/:id`; `POST /api/accounts/:id/roles` and `DELETE /api/accounts/:id/roles/:id`; `DELETE /api/accounts/:id`; `DELETE /api/api_keys/:id`; `DELETE /api/orders/:id` (order cancel) |
| `{"task_id": <int>}` | `PATCH /api/sites/:id/variants/:id` (PHP version change) |
| `{"task_id": <int>, "status": "PENDING", "cache_type": "<id>"}` | the cache layer ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `PATCH`/`DELETE /api/sites/:id/cache/:id` and `DELETE /api/sites/:id/cache/:id/purge` |
| **The cart envelope** (`{status:"accepted", cart:{ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦}, payment:{ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦}, orders:[ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦]}`) | `POST /api/orders` and `POST /api/orders/domain`; `PATCH /api/sites/:id` **with** `plan`; `POST`/`PATCH /api/cpanel_accounts`; `POST`/`PATCH /api/mailspace`; `POST /api/domain_registrations/:id/registrant_change` |
| `{"status":"preparing","backup_id":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` | `POST /api/sites/:id/backups/:id/export` |
| `{"status":"purging","username":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` | `POST /api/cpanel_accounts/:username/purge` |
| `{"status":"pending_deletion","username":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦","delete_scheduled_at":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` | `DELETE /api/cpanel_accounts/:username` |
| `{"status":"accepted","domain":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦","domain_type":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` | `POST /api/cpanel_accounts/:username/domains` |
| `{"id":"<guid>","ns1":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦","ns2":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` **or** `{"id":"<guid>","cname":"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"}` | `POST /api/sites/:id/domains` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which of the two you get depends on how that domain has to be pointed (nameservers vs CNAME) |
| **The resource's own body** | `PATCH /api/accounts/:id` (the account); a domain-registration or domain-contact mutation that opened a registrar process (its `show` body, carrying a `pending_process` block) |
| **The verification block** (`{"verification":{"domain":ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦,"state":ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦,ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦}}`) | `POST /api/mailspace/:id/domain_verification` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â provisioning is enqueued, not finished. Poll `GET` on the same path until `state` reads `"provisioned"`. |
| `{"status":"queued"}` | `POST /api/sites/:id/mail/dns_check` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no id to poll; re-read the transactional-email overview for the result. |
| `{"status":"accepted","task_id":<int>}` or `{"status":"accepted","noop":true}` | `POST /api/webhooks/cdn_cache` (infra-facing, not a customer endpoint) |

That table is the complete set ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no other `/api` endpoint answers `202`.

**Async operations include:** PHP version change, backup creation, restore, restart, domain add/remove, account-role removal, cache enable/disable/purge, account delete. (Site creation, site resize/plan-change, domain orders, cPanel account orders and resizes, and Mailspace purchases and resizes are also async but are polled via the **cart**, not a task ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see [Carts](reference/endpoints-orders.md#carts) below.)

**Polling task status:**

```bash
GET /api/tasks/:id
GET /api/sites/:site_id/tasks/:id
```

**Task statuses:**

| Status | Meaning |
|--------|---------|
| `PENDING` | Queued, not yet started |
| `RUNNING` | Currently executing |
| `OK` | Completed successfully |
| `FAILED` | Failed |
| `CANCELLED` | Cancelled |
| `PAUSED` | Paused |

**Completion callback** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â attach a `callback` to an order (`POST /api/orders`, `POST /api/orders/domain`, or `POST /api/cpanel_accounts`) and CloudPress POSTs to your URL when that order's task finishes, instead of you polling:

```json
{ "callback": { "url": "https://your-app.com/webhook", "authorization": "Bearer your-secret" } }
```

- **Permitted keys:** `url` (required) and `authorization` (optional, sent **verbatim** as the `Authorization` header). Any other key in the `callback` object is discarded. Only the three order-placing endpoints above consume a `callback`, so callbacks attach to **order** tasks only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it is ignored if sent anywhere else (a Mailspace purchase, for instance, does not accept one).
- **What CloudPress sends:** `POST` to your `url` with body `{ "timestamp": <epoch int>, "success": <bool>, "data": <task.data string> }` and headers `Authorization` (verbatim) + `Accept: application/json`. Same outbound delivery layer as billing webhooks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 30s timeout, any 2xx counts as
  success. **Retry backoff:** the wait is chosen from the age of the delivery's
  `timestamp` (5 / 10 / 15 minutes), which in practice means the first retry lands
  ~5 minutes after the failed attempt and every retry after that at 15-minute intervals.
  Retries stop once that `timestamp` is more than 4 hours old, so delivery is
  at-least-once ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â de-dup on `timestamp`, which stays fixed across all retries of one
  delivery.
- **When it fires:** only on a **terminal** task transition ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task reaching `OK`,
  `FAILED`, or `CANCELLED` (including when an infrastructure component reports the
  result in via `POST /api/webhooks/task/:id`, which sets `OK` or `FAILED`). Intermediate
  transitions such as `PENDING ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ RUNNING`, or a pause, queue **no** delivery. So expect
  one callback per order task, not a status stream.
- **Mechanism:** the `callback` is stashed on the cart and stamped onto the order task,
  and the delivery is queued at that terminal transition if the task carries one.
- **Utility endpoints** (distinct from your receiver ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â these are *inbound to CloudPress*): `GET /api/webhooks/task` returns `{ip_address}` for a reachability test; `POST /api/webhooks/task/:id` is how a task result is reported **into** CloudPress (used by infra; API-key credential, **OAuth-blocked**; idempotent via a `data`+`success` digest), and posting that result is what triggers the outbound callback. It expects an account context and, unlike the endpoints listed under [`X-Auth-Account`](#authentication), does not check for one ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sending it without one produces a `500`, not a `400`.

### Carts (order/billing async window)

Five endpoints return the same **cart envelope** (status `accepted`): `POST /api/orders`; site plan-change (`PATCH /api/sites/:id` with `plan`); cPanel account order/resize (`POST`/`PATCH /api/cpanel_accounts`); Mailspace purchase/resize (`POST`/`PATCH /api/mailspace`); and the paid registrant change (`POST /api/domain_registrations/:id/registrant_change`). Poll the cart for materialized orders. `orders` is empty during the async window on Stripe-billed plans, and a **declined off-session charge is still a `202`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never branch on the HTTP status. What to branch on depends on the operation: a **purchase** reports a declined or challenged charge as `payment.status: "awaiting_authentication"`, but a **resize** (site plan-change, cPanel resize, Mailspace resize) builds a proration cart and reports `processing` with a populated `payment.hosted_invoice_url` instead. On a resize, branch on that URL being non-null. See [Orders](reference/endpoints-orders.md#orders) and [Carts](reference/endpoints-orders.md#carts).

### Registrar processes

Domain-registration mutations may complete synchronously (200) or open a registrar **process** (202 with `pending_process`). Poll via the [processes](reference/endpoints-domains.md#domain-registration-processes) endpoints. A registration with an in-flight process is "busy" and rejects further mutations with **`409`** `registration_busy`.

---

## Feature & Plan Gating

- **`domain-registration` feature flag** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when off, all domain-registration and domain-contact endpoints return **`503`** `{"errors":[...],"code":"feature_disabled"}`.
- **Shield plan entitlement** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the site's product must include Shield, else **`403`**
  `{"error":"shield_not_in_plan"}`. The gate is declared on this enumerated set:
  `/api/sites/:id/shield` (show/create/update/destroy) plus the nested
  `shield/events`, `shield/bot_detection`, `shield/waf`, `shield/waf_custom_rules`,
  `shield/rate_limits` and `shield/access_lists` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **reads as well as writes**. Two of
  those actions additionally require a **premium** plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
  `PATCH /api/sites/:id/shield/bot_detection` and
  `POST /api/sites/:id/shield/waf_custom_rules` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â else **`403`**
  `{"error":"shield_premium_required"}`.
- **Bunny activation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â CDN/Shield endpoints return **`409`** `cdn_not_active` / `shield_not_active` when the underlying Bunny pull zone / shield zone hasn't been provisioned yet.
- **Registrar availability** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â registrar operations on a TLD with no configured registrar return **`503`** `registrar_unavailable`.
- **cPanel availability** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cPanel hosting is limited to workspaces that are already cPanel customers; every `/api/cpanel_accounts` route returns **`403`** `{"errors":[...],"code":"cpanel_not_enabled"}` for any other workspace. A **`503`** `cpanel_unavailable` means the hosting platform could not be reached and is retryable; `cpanel_not_enabled` is not.
- **Mail platform availability** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when mail hosting is not configured, **every**
  `/api/mailspace/:id/ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` endpoint returns **`503`**
  `{"errors":["The mail server is not configured."],"code":"stalwart_unavailable"}`.
  Reads included ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this gate runs before the mailspace is even looked up, so it is not a
  write-only refusal.
- **Mailspace state gates** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the endpoints nested under `/api/mailspace/:id` apply four
  further gates in this order, and a client should map each code to exactly one cause:
  **`403`** `not_authorized` (no edit permission on the mailspace's own workspace),
  **`403`** `mailspace_suspended` (staff block or dunning hold), **`403`** `pending_delete`
  (mailspace soft-deleted), **`409`** `not_provisioned` (mailspace not yet in the mail
  platform ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â complete domain verification first). Two of those four are decided on the
  **HTTP verb**, not the action name ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `not_authorized` and `pending_delete`: `GET` and
  `HEAD` always pass, so **reads stay available on a soft-deleted mailspace for its whole
  retention window**. `mailspace_suspended` is **not** verb-gated: a staff-blocked or
  dunning-held mailspace refuses **reads as well as writes**, even though its message reads
  "cannot be modified". Do not infer the verb rule from one code to the next.
  **Two deliberate exceptions:** the mailspace **purge** endpoint does not apply
  `pending_delete` (being soft-deleted is its precondition), and the **primary-domain
  verification** endpoint does not apply `not_provisioned` (it runs before provisioning is
  possible).
- **Mailspace read failures are `503` with a per-resource code, and an empty collection
  is never one of them.** Every index inside a mailspace reads the mail server live, and
  each answers its own code when that read could not be **performed** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
  `mailboxes_unavailable`, `domains_unavailable`, `aliases_unavailable`,
  `groups_unavailable`, `mailing_lists_unavailable`, `archived_items_unavailable`,
  `purged_mailboxes_unavailable`. The code names *which* read failed, which is the point:
  `GET .../groups` has two, and `group_members_unavailable` now means only that the member
  tally failed while the group list itself came back. **So an empty array in a `200` means
  the mail server was asked** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a `200` no longer hides a failed read, and a client may
  reconcile its own state against it. That buys honesty about the read, **not
  completeness**: every one of these lists is capped upstream (500 rows) and truncates
  silently, with no total and no flag, and `purged_mailboxes` has the worst of it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â its cap
  is applied server-wide *before* tenant filtering, so an empty `200` there is still not
  proof the mail is gone. Three further exceptions, none of which generalises: mailbox mail
  rules answer **`422`** `mail_rules_unavailable` rather than a 503; the app-password list,
  the masked-email list, the delivery logs and the by-id group and mailing-list lookups are
  still **tolerant** and degrade to an empty result or a `404`.
- **On a mailspace write, `503` answers one of two opposite questions ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check which.**
  The distinction is deliberate and it is per code, not per status: some `503`s mean
  *nothing was attempted*, others mean *something was attempted and the outcome is
  unknown*. `restore_unavailable` (purged-mailbox restore) and
  `archived_item_lookup_unavailable` mean nothing happened and the resource is untouched.
  `restore_unconfirmed` / `delete_unconfirmed` (archived mail) and `aliases_unavailable`
  on an alias write mean the request went out and its fate is unknown ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **re-read the
  resource before retrying**, and treat `delete_unconfirmed` with particular care, since
  that erase is irreversible. `delete_unavailable` on mailbox force-delete is a third
  thing again: the mailbox **is** gone from the mail server, and what could not be
  established is whether its mail is still recoverable. A **`422`** is the only answer
  that means the mail server replied and refused.
- **Same code, different body.** A mailspace `pending_delete` **`403`** carries only
  `errors` and `code` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **no `delete_scheduled_at`**, unlike the site lock below. And a
  cPanel account scheduled for deletion uses a *different* code entirely
  (`pending_deletion`). Three surfaces, two codes, three bodies ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't share one branch.
- **Transactional site email** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `/api/sites/:id/mail` adds three of its own: **`503`**
  `{"errors":["Transactional email is not available."],"code":"mailchannels_unavailable"}`
  when the platform integration is not configured, **`422`** `mail_not_provisioned` when
  the site has no transactional-email account, and **`422`** `mail_not_active` when it has
  one that has not finished provisioning. A site that never provisioned mail is a normal
  state, not an unknown record.
- **Pending-delete lock (sites)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `DELETE /api/sites/:id` is a *soft* delete: the site
  enters a pending-delete window before it is purged, and while it is there the site is
  **locked**. `PATCH` and `DELETE` on the site itself, and **every** nested site
  sub-resource ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reads included: backups, backup exports, restores, restart, domains and
  their certificates, cache, CDN and CDN caching, edge rules, Shield and all its
  sub-resources, logs, metrics, tasks, variants, SSO, transactional email ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â return **`403`**:

  ```json
  {
    "errors": ["This site is pending deletion and is locked. Restore it to make changes."],
    "code": "pending_delete",
    "delete_scheduled_at": "2026-09-01T00:00:00Z"
  }
  ```

  Exactly two endpoints are exempt. `GET /api/sites/:id` returns a **reduced** payload
  (`pending_delete: true`, `status: "pending_delete"`, `delete_scheduled_at`, plus name,
  primary domain, package, location and the account block ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and *not* the PHP version,
  domain list, SFTP details or subscription), and `GET /api/sites` still lists the site
  with `pending_delete: true`. A `403 pending_delete` on a plain read is therefore
  expected behavior, not a bug ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â restore the site to unlock it.
- **Pending-deletion lock (cPanel)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the same idea with a **different code**: a cPanel
  account scheduled for deletion answers **`403`**
  `{"errors":[...],"code":"pending_deletion","delete_scheduled_at":"..."}` on resize
  (`PATCH /api/cpanel_accounts/:username`), the password endpoint, and cPanel domain
  add/remove. Minting a control-panel session is deliberately **not** blocked.
- **Trial workspaces** cannot buy cPanel hosting: **`403`** `trial_account` on the account order and resize, and on the nested password, purge, session and domain writes. Cancelling an account is deliberately **not** trial-gated.

---

## Endpoint Reference

Per-endpoint documentation ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â routes, parameters, response shapes, status codes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
lives in the reference files below.

**Read the reference file for the relevant topic before answering an
endpoint-specific question or writing integration code.** Do not answer endpoint
questions from this router alone: it deliberately carries only the cross-cutting
concepts, and guessing a parameter name or response shape is worse than reading
the file.

| Topics | Reference file |
|---|---|
| GET /api/about, Accounts, Account Roles, API Keys, Subscriptions, Users, User Roles | [`reference/endpoints-accounts.md`](reference/endpoints-accounts.md) |
| Sites, Sites / Backups, Sites / Backup Exports, Sites / Restores, Sites / Restart, Sites / Domains, Sites / SSO, Sites / Variants (PHP version), Sites / Mail (transactional email) | [`reference/endpoints-sites.md`](reference/endpoints-sites.md) |
| Orders, Carts, Mailspace (mail hosting) | [`reference/endpoints-orders.md`](reference/endpoints-orders.md) |
| cPanel Hosting ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â accounts, password, purge, sessions, domains | [`reference/endpoints-cpanel.md`](reference/endpoints-cpanel.md) |
| Mailspace Mailboxes, Mailbox App Passwords, Mailbox Mail Rules, Vacation Responses, Purged Mailboxes, Archived Items (deleted mail) | [`reference/endpoints-mailboxes.md`](reference/endpoints-mailboxes.md) |
| Mailspace Aliases, Groups, Mailing Lists, Masked Emails, Delivery Logs | [`reference/endpoints-mail-routing.md`](reference/endpoints-mail-routing.md) |
| Mailspace Domains, Primary & Secondary Domain Verification, Mailspace Purge | [`reference/endpoints-mailspace.md`](reference/endpoints-mailspace.md) |
| Domains, Domain Registration | [`reference/endpoints-domains.md`](reference/endpoints-domains.md) |
| DNS Zones, DNS Zone Records | [`reference/endpoints-dns.md`](reference/endpoints-dns.md) |
| Sites / CDN, Sites / Cache, Sites / Edge Rules, Sites / Logs, Sites / Metrics / CDN | [`reference/endpoints-cdn.md`](reference/endpoints-cdn.md) |
| Sites / Shield (WAF, DDoS, bots), Sites / Metrics / Shield | [`reference/endpoints-shield.md`](reference/endpoints-shield.md) |
| Tasks, Sites / Metrics / Resources, Webhooks / Tasks | [`reference/endpoints-tasks.md`](reference/endpoints-tasks.md) |
| MCP Server (Model Context Protocol) | [`reference/mcp-server.md`](reference/mcp-server.md) |
| Billing Webhooks | [`reference/webhooks.md`](reference/webhooks.md) |
