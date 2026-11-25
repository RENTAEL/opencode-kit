# Mailspace Tenancy & Domains

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

Every route in this file is nested under `/api/mailspace/:mailspace_id/…`, where
`:mailspace_id` is the mailspace GUID. The mailspace's own lifecycle — list, show,
purchase, resize, soft-delete — is **not** here; it is
[`endpoints-orders.md#mailspace`](endpoints-orders.md#mailspace). This file covers the
domains inside a mailspace, the two ownership-verification flows, and the hard-delete.

`X-Auth-Account` is **not required** on these routes: the GUID is resolved against the
mailspaces the credential can reach (its account's, or — for a user/session/OAuth
credential sent without the header — every mailspace across the user's workspaces).
Sending it is harmless.

**Scopes.** Reads take `mailspace:read`, mutations take `mailspace:write`. Per action:

| Scope | Actions |
|---|---|
| `mailspace:read` | domains index, domains show, `GET .../domains/dns`, `GET .../domains/:domain_name/verification`, `GET .../domain_verification` |
| `mailspace:write` | domains create/update/destroy, `POST .../domains/dns_check`, `POST`+`DELETE .../domains/:domain_name/verification`, `POST`+`DELETE .../domain_verification`, `POST .../purge` |

None of these endpoints is OAuth-blocked — there is no `401 user_required` on this
chain. A credential with no user attached still passes every read; the writes fail
gate 3 below with `not_authorized`, because there is no user whose edit permission
could be checked.

## The inherited gate chain

Every endpoint in this file runs the same six gates, in this order, before its own
logic. Per-endpoint sections below name only the codes that are **specific to that
endpoint** — assume all six apply unless the section says otherwise.

| # | Status | `code` | Cause |
|---|---|---|---|
| 1 | **503** | `stalwart_unavailable` | The mail server is not configured. |
| 2 | **404** | *(empty body)* | The mailspace GUID is unknown **or** not reachable by this credential — deliberately indistinguishable, so the endpoint cannot be used to probe which GUIDs exist. |
| 3 | **403** | `not_authorized` | Decided on the HTTP verb: `GET` and `HEAD` always pass; every other method needs edit permission on the mailspace's **own** workspace (not the one in `X-Auth-Account`). |
| 4 | **403** | `mailspace_suspended` | Staff block or dunning hold — `{"errors":["This mailspace is on hold and cannot be modified. Please contact support."],"code":"mailspace_suspended"}`. Edit permission does not override it. **Not verb-gated, unlike gates 3 and 5: reads are refused too**, despite the message saying "cannot be modified". |
| 5 | **403** | `pending_delete` | Soft-deleted mailspace — `{"errors":["This mailspace is scheduled for deletion and cannot be modified. Restore it first."],"code":"pending_delete"}`. Verb-gated like gate 3, so **reads stay available for the whole retention window**. |
| 6 | **409** | `not_provisioned` | The mailspace is not in the mail server yet — `{"errors":["This mailspace is not provisioned yet. Complete domain verification first."],"code":"not_provisioned"}`. |

**Gate 4 does not fire on a soft-deleted mailspace.** It short-circuits when the
mailspace is pending deletion, leaving gate 5 to answer. A soft-deleted mailspace that
is *also* on a staff hold therefore returns `pending_delete`, never
`mailspace_suspended`.

### Two endpoints in this file break the chain

- **[Mailspace Purge](#mailspace-purge) does not apply gate 5.** Being soft-deleted is
  the *precondition* for a purge, not a refusal. Every other write in this file is
  refused for the whole retention window; this one is the single write that stays
  reachable. Gate 6 still applies (see that section for the dead end it creates).
- **[Primary Domain Verification](#primary-domain-verification) does not apply gate
  6.** It runs before the mailspace exists on the mail server — it is the step that
  *makes* provisioning possible, so `not_provisioned` would refuse the only endpoint
  that can clear it. All five other gates apply, and it substitutes its own **409**
  `already_provisioned` for the opposite condition.

Nothing else in this file skips a gate.

**Error envelope** is `{"errors": ["…"], "code": "…"}`. Messages are **always English
regardless of `Accept-Language`** — the locale switch that localizes the control panel
does not reach these responses. Branch on `code`.

**No endpoint in this file paginates.** The domains index returns every domain and every
pending domain in one response, with no page/limit parameters and no pagination
metadata. The optional `q` filter is the only way to narrow it.

**No endpoint in this file returns a task id or registers a callback.** The one
asynchronous response is `POST .../domain_verification` (**202**); everything else is
synchronous.

---

### Mailspace Domains

**Base route:** `/api/mailspace/:mailspace_id/domains`. A mailspace has exactly one
**primary** domain (its identity, created with the mailspace) plus any number of
**secondary** domains, which are in one of two states: *served* (live on the mail
server) or *pending verification* (a local row holding a TXT challenge, accepting no
mail).

**Encoding the name in the path.** The `:name` segment accepts any characters except
`/`, so a dotted FQDN goes through literally — `GET .../domains/example.com`. No
percent-encoding is needed or expected. The value is then normalized: lowercased, a
leading `http://`/`https://` stripped, a leading `www.` stripped, anything from the
first `/` onward dropped, and a trailing dot chomped. Two consequences:

- `EXAMPLE.COM`, `https://example.com` and `example.com.` all address `example.com`.
- A domain whose real name begins `www.` is **not addressable on this path** — the
  prefix is stripped before lookup.

**`dns` and `dns_check` are collection paths, matched ahead of `:name`.** They hang off
the collection, not off a single domain: `.../domains/dns` and `.../domains/dns_check`,
with the domain passed as an optional `domain` **query parameter**. There is no
`.../domains/:name/dns`.

**The `domain` query parameter is normalized differently from the `:name` path
segment.** `?domain=` is only trimmed and lowercased, then matched exactly against the
mailspace's own domains — no protocol, `www.` or path stripping. `?domain=WWW.example.com`
is a **404** `unknown_domain` where `.../domains/www.example.com` would have resolved.
Send the bare, exact FQDN.

Any `?domain=` value the mailspace does not own is **404**
`{"errors":["That domain is not on this mailspace."],"code":"unknown_domain"}` — it does
**not** fall back to the primary domain. A typo returns 404 rather than the primary's
records under the wrong name.

#### GET /api/mailspace/:mailspace_id/domains — list domains

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `q` | String | No | Case-insensitive substring match on the domain name. Filters both arrays. |

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/domains"
```

```json
{
  "primary_domain": "example.com",
  "domains": [
    { "name": "example.com", "description": null, "state": "primary",
      "verified": true, "dns_state": "managed" },
    { "name": "second.example", "description": "Trading name",
      "state": "served", "verified": true, "dns_state": "setup_needed" }
  ],
  "pending_domains": [
    { "name": "third.example", "description": null, "state": "pending_verification",
      "verified": false,
      "verification": { "txt_host": "_mailspace-verify.third.example",
                        "txt_value": "<token>", "txt_type": "TXT" },
      "last_checked_at": null,
      "created_at": "2026-08-01T09:12:44.000Z", "updated_at": "2026-08-01T09:12:44.000Z" }
  ]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `primary_domain` | String | The mailspace's own domain, from local state. Always present. |
| `domains` | `Array<Object>` | Read **live** from the mail server: the primary plus every verified secondary. Uses the served-domain shape below. |
| `pending_domains` | `Array<Object>` | Local rows awaiting a TXT proof, ordered by name. A different shape — see below. |

**`domains` and `pending_domains` are not the same object.** They share `name`,
`description`, `state` and `verified` and nothing else. A served domain carries
`dns_state` and no `verification`; a pending one carries `verification`,
`last_checked_at`, `created_at`, `updated_at` and no `dns_state`. Key off `state`.

**Served-domain shape** (`domains[]`, and the `domain` object on show/create/update):

| Field | Type | Notes |
|-------|------|-------|
| `name` | String | |
| `description` | String / null | Free text from the mail server. Explicit **`null`** when unset. |
| `state` | String | `primary` for the mailspace's own domain, `served` for a verified secondary. Those are the only two values this shape emits. |
| `verified` | Boolean | Always `true` here — a domain only reaches this shape by being live on the mail server. |
| `dns_state` | String | `managed`, `setup_needed` or `manual`. See below. |

`dns_state` values, in the order they are decided:

| Value | Meaning |
|---|---|
| `managed` | CloudPress hosts this domain's DNS zone and writes the mail records itself. Nothing for the customer to publish. |
| `setup_needed` | External DNS, and the last probe found required records missing. |
| `manual` | External DNS, with nothing known to be outstanding. Note this is also the value **before any probe has ever run** — it is not proof the records are live. |

**Pending-domain shape** (`pending_domains[]`, and the `domain` object on show/create
when the domain is parked):

| Field | Type | Notes |
|-------|------|-------|
| `name` | String | |
| `description` | String / null | Explicit **`null`** when unset. |
| `state` | String | Always the literal `pending_verification`. |
| `verified` | Boolean | Can be **`true` on a pending row** — ownership proven but the mail-server create has not succeeded yet. See [Secondary Domain Verification](#secondary-domain-verification). |
| `verification.txt_host` | String | `_mailspace-verify.` + the domain name. |
| `verification.txt_value` | String | The challenge token: 32 lowercase hex characters. |
| `verification.txt_type` | String | Always the literal `TXT`. |
| `last_checked_at` | String (ISO 8601) / null | Last verification attempt; **`null`** until one runs. |
| `created_at` / `updated_at` | String (ISO 8601) | |

**A mail-server read failure is a `503` `domains_unavailable`, not an empty `domains`
array.** The live read is strict, so `domains` is authoritative: a client may reconcile
its own state against it. The empty-array version of this failure was particularly hard to
spot, because `primary_domain` comes from local state and stayed populated — an outage
looked exactly like a mailspace serving nothing.

`domains_unavailable` covers that one read and only it; a failure in the `q` filter, the
`dns_state` lookup or the response template is a `500`. Note the whole response is the
error envelope, so `pending_domains` and `primary_domain` are not returned alongside it
even though both are local and still knowable.

Endpoint-specific codes: **503** `domains_unavailable`.

#### GET /api/mailspace/:mailspace_id/domains/:name — show one domain

Resolves a served domain **or** a pending one. The response is a single `domain` key
holding whichever shape applies:

```json
{ "domain": { "name": "second.example", "description": "Trading name",
              "state": "served", "verified": true, "dns_state": "manual" } }
```

Endpoint-specific codes: **404** `unknown_domain`.

**A `503` `stalwart_unavailable` here can mean two different things.** Besides gate 1
(mail server not configured), the same code and status are returned when the
mail-server lookup for this name fails *and* no pending row by that name exists.
The local table is consulted first, so a pending domain keeps resolving through a
mail-server blip — which is what lets a client poll a verification in progress
regardless of mail-server health.

#### POST /api/mailspace/:mailspace_id/domains — add a secondary domain

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | String | Yes | FQDN. Normalized as described above, then validated: 1–253 characters, lowercase alphanumeric labels with internal hyphens, and a 2–63 letter TLD. |
| `description` | String | No | Free text. Omitted or empty leaves it unset. |

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  -H "X-Auth-Account: $ACCOUNT_ID" -H "Content-Type: application/json" \
  -d '{"name":"third.example","description":"Trading name"}' \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/domains"
```

Returns **`201`** with the same `{"domain": …}` envelope as show — but **which shape you
get depends on ownership**, and that is the branch to program against:

- **The workspace's billing family is the registrar of record for the domain with
  CloudPress** (and the registration has not been released) → ownership is already
  proven, the domain is created on the mail server immediately, and you get the
  **served** shape with `state: "served"`. Nothing to publish, no verification step. The
  check is made against the name's **registrable root**, so a subdomain of a domain the
  workspace registered with CloudPress also counts as proven.
- **Anything else, including a domain whose DNS zone CloudPress hosts** → the domain is
  parked and you get the **pending** shape with `state: "pending_verification"` and the
  `verification` block. Hosting the zone is deliberately *not* accepted as proof of
  ownership. Publish the TXT record, then `POST` the verification endpoint.

Endpoint-specific codes:

| Status | `code` | Cause |
|---|---|---|
| **400** | `invalid_domain` | `{"errors":["Please provide a valid domain name."],"code":"invalid_domain"}` — missing or malformed `name`. |
| **409** | `domain_exists` | Already live on this mailspace. |
| **409** | `domain_pending_verification` | Already parked awaiting a TXT proof on this mailspace. |
| **422** | `domain_create_failed` | The create was refused. Also covers a name already live on **another** tenant of the mail server, which the per-mailspace checks above cannot see. |

After a successful create, a domain whose DNS CloudPress hosts has its mail records
written into that zone in the background; a domain on external DNS is flagged
`setup_needed` immediately so `GET .../domains/dns` shows the checklist from the first
request.

#### PATCH /api/mailspace/:mailspace_id/domains/:name — update the description

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `description` | String | No | **Three-way, and the three cases are distinct on the wire.** Omit the key → the description is left exactly as it is, and nothing about the field is sent to the mail server. Send `""` → the description is **cleared**, and reads back as `null` rather than `""` (the mail server rejects an empty string for the field, so a null is sent). Send a value → set to that value. |

Only a **served** domain can be patched. Returns **`200`** with the served-domain shape.
The name cannot be changed here; there is no rename.

**The `200` body is not always read back from the mail server**, and it is still
trustworthy when it is not. The post-write read can fail even though the write succeeded,
so the response falls back to what is known to be true: the description you just sent, or
the pre-write description when you omitted the key. Every other field in the served shape
is derived rather than read back — `state` from the name, `verified` from having reached
this shape at all, `dns_state` from the zone lookup — so nothing here degrades to a
placeholder.

Endpoint-specific codes: **404** `unknown_domain`; **409** `domain_pending_verification`
(the domain is parked — there is nothing on the mail server to patch); **422**
`domain_update_failed`, which also covers a domain that has since left this mailspace
(`"… is no longer on this mailspace — refresh the page."`). The two-meaning **503**
described under show applies here too.

#### DELETE /api/mailspace/:mailspace_id/domains/:name — remove a secondary domain

Returns **`200`** with an empty body. Removing a domain also removes the mail records
CloudPress wrote for it in a hosted zone, so the zone stops advertising a mail host that
no longer accepts mail for that name.

Endpoint-specific codes:

| Status | `code` | Cause |
|---|---|---|
| **404** | `unknown_domain` | |
| **409** | `primary_domain` | `{"errors":["The primary domain can't be deleted."],"code":"primary_domain"}` — the primary is the mailspace's identity and goes away only with the mailspace. |
| **409** | `domain_pending_verification` | The domain is parked. Cancel it with `DELETE .../domains/:domain_name/verification` instead. |
| **422** | `domain_delete_failed` | Includes the "still in use" refusal: the message names the counts blocking it, across mailboxes, groups and mailing lists — e.g. `"Can't delete third.example — it still has 2 mailboxes and 1 group. Delete those first, then remove the domain."` Delete those objects first. |

The two-meaning **503** described under show applies here too.

#### GET /api/mailspace/:mailspace_id/domains/dns — required mail DNS records

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `domain` | String | No | Query parameter. Defaults to the mailspace's primary domain. Must be a domain this mailspace owns (served, primary, or pending) — otherwise **404** `unknown_domain`. |

**Two response shapes, selected by `managed`.** `managed` is `true` only when CloudPress
hosts the domain's DNS zone *and* that zone is live enough to be written to; a hosted
zone that cannot be written to reads as `false`, so the customer still gets an
actionable checklist rather than "managed, nothing to do".

`managed: true` — reference only, no per-record status:

```json
{
  "domain": "example.com",
  "managed": true,
  "checked_at": null,
  "all_detected": null,
  "records": [
    { "type": "MX", "name": "example.com", "value": "mail.example.com",
      "priority": 10, "purpose": "Mail delivery",
      "optional": false, "placeholder": false }
  ]
}
```

`managed: false` — external DNS, every row annotated with the last probe's result:

```json
{
  "domain": "second.example",
  "managed": false,
  "checked_at": "2026-08-19T14:02:11Z",
  "detected": 7,
  "total": 8,
  "all_detected": false,
  "records": [
    { "type": "MX", "name": "second.example", "value": "mail.second.example",
      "priority": 10, "purpose": "Mail delivery",
      "optional": false, "placeholder": false,
      "status": "ok", "found": null },
    { "type": "CNAME", "name": "webmail.second.example",
      "value": "<shared autoconfig host, from the response>",
      "priority": null, "purpose": "Webmail",
      "optional": false, "placeholder": false,
      "status": "mismatch", "found": "webmail.someone-else.example" }
  ],
  "caa": { "status": "ok" }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `domain` | String | The domain the rows are for — the `domain` you sent, or the primary. |
| `managed` | Boolean | Selects the shape. |
| `checked_at` | String (ISO 8601) / null | Explicit **`null`** on `managed: true`. On `managed: false`, **`null`** until a probe has run. |
| `detected` / `total` | Integer | **Absent** on `managed: true` — the keys are not emitted at all, so reading them yields undefined, not `null`. Present on `managed: false`. Both count **required rows only**; optional rows are excluded from the ratio. |
| `all_detected` | Boolean / null | Explicit **`null`** on `managed: true`. On `managed: false`, `true` only when `total` is non-zero and every required row is `ok`. |
| `records` | `Array<Object>` | See the row fields below. |
| `caa` | Object | **Absent** on `managed: true`. On `managed: false` it is `{ "status": … }` and nothing else. |

Record row fields:

| Field | Type | Notes |
|-------|------|-------|
| `type` | String | `MX`, `A`, `AAAA`, `TXT` or `CNAME`. |
| `name` | String | The fully-qualified owner name to create the record at. |
| `value` | String | The value to publish. |
| `priority` | Integer / null | `10` on the MX row; explicit **`null`** on every other type. |
| `purpose` | String | Human label for the row, e.g. `Mail delivery`, `SPF – authorised senders`, `DKIM – message signing`, `Webmail`, `Outlook autodiscover`. Display text — do not key logic on it. |
| `optional` | Boolean | `true` on the IPv6 `AAAA` row only. Optional rows are shown with their own status but never gate `all_detected`: a domain reachable over IPv4 is working mail. |
| `placeholder` | Boolean | `true` when the DKIM `value` is an instructional stand-in rather than a real signing key (the mail server's zone could not be read, or the mailspace is not provisioned). **Never publish a row with `placeholder: true`** — re-request until it is `false`. |
| `status` | String | `managed: false` only — `ok`, `mismatch`, `missing`, or `unchecked` (no probe has covered this row yet). |
| `found` | String / null | `managed: false` only. The live value that was seen instead. Non-null on `mismatch`; **`null`** on `ok`, `missing` and `unchecked`. |

**`caa.status`** is advisory and gates nothing — it is deliberately outside `records`
and outside `detected`/`total`, because a domain with no CAA record at all is correctly
permissive and needs nothing added. Values: `ok`, `mismatch` (a CAA policy that excludes
the certificate authority CloudPress's mail certificates come from — the actionable
one; the mail certificate cannot issue), `unknown` (indeterminate, including a CAA
lookup that could not be completed over a signed zone), `unchecked` (no verdict
available). The certificate authority is resolved from live configuration on each
request, so no CA name is fixed in this contract.

**The row set** is the same on both shapes, and is the same set the probe checks — one
MX at the domain, an `A` and an optional `AAAA` at the mail host, a `TXT` SPF record at
the domain, a `TXT` DMARC record at `_dmarc.`+the domain, one `TXT` DKIM row per signing
key (or a single placeholder DKIM row), and three `CNAME` rows for webmail, email-client
autoconfiguration and Outlook autodiscover. The DKIM row count therefore varies with how
many keys the mail server holds.

**Publish `value` verbatim; do not hardcode any of these values.** The DKIM, SPF and
DMARC values are read live from the mail server on every request — the DKIM key rotates,
and the SPF row is the domain's *existing* SPF record with CloudPress's outbound relay
`include:` merged into it, so it differs per domain and changes when the customer edits
their own SPF. The remaining values are shared-infrastructure hostnames and addresses
returned in the response. A client that caches or reconstructs them will eventually
publish a stale record and take the domain's mail down.

Serving this endpoint performs no DNS lookups on `managed: false` — the statuses come
from the stored result of the last probe. Use `dns_check` to refresh them.

#### POST /api/mailspace/:mailspace_id/domains/dns_check — probe DNS now

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `domain` | String | No | Query parameter, same rules as `dns`. Defaults to the primary. |

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/domains/dns_check?domain=second.example"
```

**Synchronous.** The lookups run inline and the **`200`** carries the fresh result —
there is no `202`, no task, and nothing to poll. Same body as `GET .../domains/dns`.
A successful probe also updates the domain's `dns_state` (`manual` once every required
row is `ok`, `setup_needed` otherwise), so a following domains index reflects it.

**A managed domain short-circuits with `records: []`.** This is the one place the two
endpoints differ: `GET .../domains/dns` returns the full reference list for a managed
domain, while `dns_check` returns `{"domain":…,"managed":true,"checked_at":null,"all_detected":null,"records":[]}`
and runs no lookups. Fetch the record list from `GET .../domains/dns`, not from here.

**Rate limit: one probe per mailspace per domain per 5 minutes.** Exceeding it is
**429** `{"errors":["DNS for <domain> was checked recently. Try again in a few minutes."],"code":"rate_limited"}`.
Two things worth relying on: the window is keyed per **domain**, so checking one domain
never blocks another on the same mailspace; and the managed short-circuit is evaluated
*before* the limiter, so it never consumes the window. A probe that fails releases the
window immediately, so a retry after a resolver blip is not locked out.

Endpoint-specific codes: **404** `unknown_domain`; **429** `rate_limited`; **422**
`dns_check_failed` (the probe itself could not complete).

---

### Secondary Domain Verification

**Base route:** `/api/mailspace/:mailspace_id/domains/:domain_name/verification` — a
**singular** resource, verb-dispatched on one path. Note the segment is spelled
`:domain_name` here, not `:name`. Dotted FQDNs pass through it literally and are
normalized the same way as the `:name` segment on the domains routes.

| Verb | Meaning |
|---|---|
| `GET` | The TXT record to publish and the current state. Scope `mailspace:read`. |
| `POST` | Check the record now and, on success, create the domain on the mail server. Scope `mailspace:write`. |
| `DELETE` | Abandon the domain; drop the pending row. Scope `mailspace:write`. |

All three resolve a **pending** row only. A name that is not parked on this mailspace —
including one that is already served — is **404**
`{"errors":["No domain is awaiting verification under that name on this mailspace."],"code":"unknown_domain"}`.
All six gates apply to all three verbs, so a soft-deleted mailspace still serves the
`GET` and refuses the `POST`/`DELETE` with `pending_delete`.

#### GET .../domains/:domain_name/verification — challenge and state

```json
{
  "verification": {
    "domain": "third.example",
    "state": "awaiting_verification",
    "verified": false,
    "txt_type": "TXT",
    "txt_host": "_mailspace-verify.third.example",
    "txt_value": "<token>",
    "verified_at": null,
    "last_checked_at": "2026-08-19T14:02:11.000Z",
    "create_attempts": 0,
    "create_attempts_exhausted": false
  }
}
```

Every key above is always present.

| Field | Type | Notes |
|-------|------|-------|
| `domain` | String | |
| `state` | String | `awaiting_verification` or `verified`. Those are the only two values. |
| `verified` | Boolean | Same fact as `state`. |
| `txt_type` | String | Always the literal `TXT`. |
| `txt_host` | String | `_mailspace-verify.` + the domain name. |
| `txt_value` | String | The token to publish: 32 lowercase hex characters. Compared against each TXT string at `txt_host` and against their concatenation, so a value your DNS provider splits still matches. |
| `verified_at` | String (ISO 8601) / null | **`null`** until ownership is proven. |
| `last_checked_at` | String (ISO 8601) / null | Last attempt, whether it succeeded or not. **`null`** before the first. |
| `create_attempts` | Integer | Failed attempts by the unattended sweep to create this already-verified domain on the mail server. |
| `create_attempts_exhausted` | Boolean | `true` once `create_attempts` reaches 10 and the unattended sweep has given up. |

**`state: "verified"` on this endpoint means the row is stuck, not finished.** A
successful verification destroys the pending row, so a row that is still here *and*
verified proved ownership but could not be created on the mail server. `POST` here to
retry — it resets `create_attempts` to 0, which also re-arms the unattended sweep after
it has given up.

#### POST .../domains/:domain_name/verification — verify and create

Returns **`200`** on success. Synchronous — the DNS lookup and the mail-server create
both happen inline. The pending row is destroyed and the domain moves to
`.../domains/:name` from this point on:

```json
{ "domain": { "name": "third.example", "state": "served", "verified": true } }
```

Those three keys are the whole body — this is **not** the served-domain shape from the
domains routes: there is no `description` and no `dns_state`. Re-read
`GET .../domains/:name` for those.

Endpoint-specific codes — the two failure modes are deliberately distinct:

| Status | `code` | Cause and what to do |
|---|---|---|
| **404** | `unknown_domain` | Nothing parked under that name. |
| **422** | `verification_failed` | The TXT record was not visible. The message distinguishes "not found yet — DNS changes can take a few minutes to propagate" from "we couldn't complete the DNS lookup" and from "no verification token has been issued for this domain". Retry after DNS propagates. |
| **422** | `domain_create_failed` | Ownership **was** proven and stands — the mail-server create was refused. The pending row survives with `verified: true`; retry the same call. |

**This endpoint re-reads the TXT record on every call, including for a row that is
already verified — it does not skip ahead to the create.** That differs from the
primary-domain flow, which does skip a proven lookup. So **leave the TXT record published
until the domain is actually serving**: if you tear it down after seeing `verified: true`
and then retry a `domain_create_failed`, every retry answers **422** `verification_failed`
instead, and there is no path off that state, because the attempt counter is only reset
*after* the lookup succeeds. Re-publishing the record is the only way back.

It is idempotent against a race with the unattended sweep: a domain the sweep already
created is reported as success and the pending row is cleaned up.

#### DELETE .../domains/:domain_name/verification — abandon the domain

Returns **`200`** with an empty body. Purely local and non-destructive to mail: nothing
exists on the mail server at this point. Re-adding the domain later mints a new token,
so the TXT record you published becomes useless — replace it rather than reusing it.

Endpoint-specific codes: **404** `unknown_domain`.

---

### Primary Domain Verification

**Base route:** `/api/mailspace/:mailspace_id/domain_verification` — a **singular**
resource, verb-dispatched on one path, for the mailspace's **own** domain. This is the
pre-provisioning step a purchase lands in when the workspace was not already the
registrar of record for the domain it bought mail on.

**This is the one place in this file where gate 6 (`not_provisioned`) does not apply**
— it is the endpoint that gate sends an unprovisioned mailspace to. Gates 1–5 all
apply. The inverse condition has its own answer: on an already-provisioned mailspace
every verb returns **409**
`{"errors":["This mailspace is already set up — its domain needs no verification."],"code":"already_provisioned"}`.

| Verb | Meaning |
|---|---|
| `GET` | Setup state, and the TXT record while one is outstanding. Scope `mailspace:read`. |
| `POST` | Check the record and drive provisioning. Scope `mailspace:write`. Returns **`202`**. |
| `DELETE` | Cancel the purchase outright. Scope `mailspace:write`. **Irreversible and financial.** |

#### GET .../domain_verification — setup state

```json
{
  "verification": {
    "domain": "example.com",
    "state": "awaiting_verification",
    "verified": false,
    "provisioned": false,
    "verified_at": null,
    "txt_type": "TXT",
    "txt_host": "_mailspace-verify.example.com",
    "txt_value": "<token>",
    "last_checked_at": null,
    "provision_error": null,
    "provision_attempts": 0
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `domain` | String | The mailspace's primary domain. |
| `state` | String | One of exactly four values — see the table below. |
| `verified` | Boolean | Domain ownership proven. |
| `provisioned` | Boolean | The mail-server tenant exists. |
| `verified_at` | String (ISO 8601) / null | **`null`** until ownership is proven. |
| `txt_type` / `txt_host` / `txt_value` | String | **Absent as a group**, not `null`, unless `state` is `awaiting_verification`. The three keys are emitted together exactly when a challenge is outstanding, so `state == "awaiting_verification"` is the reliable test — check it before reading through them. `txt_host` is `_mailspace-verify.` + the domain; `txt_value` is 32 lowercase hex characters. |
| `last_checked_at` | String (ISO 8601) / null | **`null`** before the first attempt. |
| `provision_error` | String / null | The last setup failure's message. **`null`** when there is none — and cleared back to `null` by a `POST`, which is why it cannot be used to tell "never failed" from "retried after a failure". |
| `provision_attempts` | Integer | Failed setup attempts. Reset to `0` by a `POST`. The unattended sweep stops retrying at 10, and a `POST` re-arms it. |

| `state` | Meaning | Next step |
|---|---|---|
| `awaiting_verification` | The TXT record has not been seen. | Publish `txt_host`/`txt_value`, then `POST` here. |
| `provisioning` | Verified; the mail-server tenant is being built. | Poll. |
| `provision_failed` | Verified, but setup errored. `provision_error` carries the message. | `POST` here to retry. |
| `provisioned` | Done — the rest of the mailspace endpoints are live. | Nothing. Further calls to this resource return `409` `already_provisioned`. |

#### POST .../domain_verification — verify and provision

Returns **`202`** with the `GET` body, reflecting state *after* the reset:
`state: "provisioning"`, `provision_error: null`, `provision_attempts: 0`.

**The `202` means provisioning is enqueued, not finished.** Poll `GET` on this same path
until `state` reads `provisioned` (or `provision_failed`); `GET /api/mailspace/:id` and
its `provisioned` flag work equally well. No task id is returned and no callback is
registered.

Two behaviours in one call, decided by whether ownership is already proven:

- **Not yet verified** → the TXT record is looked up inline. Failure is **422**
  `verification_failed` and nothing is enqueued.
- **Already verified** (typically `state: "provision_failed"`) → **no DNS check is
  performed**; setup is simply re-driven. This is the retry call.

Endpoint-specific codes: **409** `already_provisioned`; **422** `verification_failed`;
**422** `provisioning_failed`.

#### DELETE .../domain_verification — cancel the purchase

Returns **`200`** with an empty body. **Irreversible:** the mailspace record is
destroyed, and there is no undo and no soft-delete window — re-buying is a fresh purchase.

**The money half is conditional.** Only when the originating order was actually charged
is the full prepaid first term credited back as a balance credit note and the dormant
subscription seat released. An uncharged order — a zero-total one, say — is simply
dropped: no credit note, and no seat to release. Do not block a reconciliation waiting
for a credit that was never owed. If the credit itself fails, the mailspace is
deliberately **left in place** rather than deleted, and the call answers **422**
`cancel_failed` — so the customer never loses both the mailspace and the money.

This is available only before provisioning. Once `state` is `provisioned`, cancel through
[`DELETE /api/mailspace/:id`](endpoints-orders.md#mailspace) instead, which is a
soft-delete with a retention window.

**A cancel whose credit could not be issued is refused rather than completed** — **422**
`cancel_failed` with `"We couldn't process your credit just now. Please try again in a
moment."` The mailspace stays pending so the customer never loses both the mailspace and
the money. Retry.

Endpoint-specific codes: **409** `already_provisioned`; **422** `cancel_failed`.

The API applies no step-up ("sudo") re-authentication to this call — a bearer token
re-authenticates on every request. Every cancel is written to the audit log with the
acting credential instead.

---

### Mailspace Purge

**Base route:** `POST /api/mailspace/:mailspace_id/purge` — a singular resource with
only a create. Scope `mailspace:write`; there is no read on this path.

**This is an immediate, permanent, irreversible hard-delete.** It destroys the
mail-server tenant — every domain, every mailbox, and all stored mail — destroys the
local mailspace record and its dependents, and removes the mail records CloudPress wrote
into the customer's hosted DNS zone. Nothing is recoverable afterwards and there is no
grace period. It is infrastructure only: billing was already cancelled when the
mailspace was soft-deleted, so no refund or credit is issued here.

**Required state: the mailspace must already be soft-deleted.** This is the endpoint
where [gate 5 (`pending_delete`)](#the-inherited-gate-chain) does not apply — being
pending deletion is the precondition, not a refusal, which makes this the only write in
this file that stays reachable during the retention window. Soft-delete first with
[`DELETE /api/mailspace/:id`](endpoints-orders.md#mailspace); purge only skips the wait.

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/purge"
```

**Synchronous: `200`, not `202`.** The teardown completes before the response and there
is nothing to poll — the mailspace GUID answers **404** from here on. The body is the
only record of what was removed, because the row it would have been serialized from is
gone:

```json
{ "purged": true, "domain": "example.com" }
```

| Field | Type | Notes |
|-------|------|-------|
| `purged` | Boolean | Always `true` in a `200` — a purge that removed nothing is a `409`, never a `200` with `false`. |
| `domain` | String | The primary domain of the mailspace that was destroyed, captured before the teardown. |

Endpoint-specific codes:

| Status | `code` | Cause |
|---|---|---|
| **409** | `not_pending_deletion` | `{"errors":["This mailspace is not scheduled for deletion. Delete it first, then purge."],"code":"not_pending_deletion"}`. Two causes, same answer: the mailspace is live, or a restore committed underneath the purge. In both cases **nothing was purged and the mailspace is still there** — it is safe to treat this as a no-op. |
| **422** | `purge_failed` | The teardown could not complete. The mailspace still exists. |

Two gate interactions specific to this endpoint:

- **Gate 4 (`mailspace_suspended`) is still reachable, but only on the way to a
  `409`.** It short-circuits for a pending-deletion mailspace, so a purge that is
  otherwise valid never hits it; a *live* mailspace on a staff or dunning hold answers
  `403` `mailspace_suspended` here rather than `409` `not_pending_deletion`. Either way
  nothing is purged.
- **Gate 6 (`not_provisioned`) still applies**, and it creates a dead end: a mailspace
  that was soft-deleted while still unprovisioned answers **409** `not_provisioned` on
  this path, and `DELETE .../domain_verification` answers **403** `pending_delete`. Such
  a mailspace cannot be purged or cancelled through the API — it has to wait out the
  retention window or be handled by support.

The API applies no step-up ("sudo") re-authentication to this call — a bearer token
re-authenticates on every request. Every purge is written to the audit log with the
acting credential instead.
