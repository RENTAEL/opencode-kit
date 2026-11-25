# Sites & Site Resources

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### Sites

**Base route:** `/api/sites` — scopes `sites:read` / `sites:write`.

A soft-deleted ("pending delete") site behaves differently on nearly every endpoint in
this file — read [Pending-delete lock](#pending-delete-lock) before using any of them.

#### GET /api/sites
Lists the sites for the authenticated account.

**Not paginated.** Unlike the other index endpoints there is no `page`/`per_page`
parameter and no pagination metadata — the full set comes back in one response.

**Not "active only" either.** The set is *active **plus** pending-delete* sites, so a
soft-deleted site awaiting purge is still listed. Filter on `pending_delete` if you
want only live sites.

Each item:
```json
{ "id": "<guid>", "name": "my-site", "created_at": "...", "updated_at": "...",
  "primary_domain": "my-site.example.com", "location": "pdx", "package": "Basic",
  "dunning_suspended": false, "pending_delete": false, "delete_scheduled_at": null,
  "account": { "id": "<guid>", "name": "Acme" } }
```

| Field | Notes |
|---|---|
| `pending_delete` | Always present. `true` while the site is soft-deleted and awaiting purge. |
| `delete_scheduled_at` | Always present. The frozen purge date; `null` for a live site. |
| `dunning_suspended` | The subscription status stays `active` for a dunning-suspended site, so this is the only signal in the list that per-site endpoints will return `402`. |

#### GET /api/sites/:id

This endpoint returns **one of two completely different bodies**. Read `pending_delete`
first and branch on it — a client that assumes the live shape will find most of its
fields missing (not null: *absent*) for a pending-delete site.

**Live site** (`pending_delete: false`):
```json
{
  "site": {
    "id": "<guid>", "name": "my-site", "primary_domain": "my-site.example.com",
    "location": "pdx", "package": "Basic", "pending_delete": false,
    "region": "pdx01", "php_version": "8.2",
    "domain_cname": "<cdn-hostname>",
    "sftp_base_path": "/home/sftpuser/apps/<service>/wordpress",
    "dunning_suspended": false,
    "account": { "id": "<guid>", "name": "Acme" },
    "domains": [ ... ],
    "subscription": { "id": "<guid>", "status": "active", "created_at": "...", "updated_at": "...",
      "price": { "amount_cents": 1000, "term": "monthly" }, "product": { "id": "basic", "name": "Basic" } },
    "ssh": { "ipaddr": "192.0.2.10", "username": "user", "password": "...", "port": 22 },
    "created_at": "...", "updated_at": "..."
  }
}
```

| Field | Notes |
|---|---|
| `php_version` | Key always present; the value is `null` when the running container's variant cannot be read. |
| `sftp_base_path` | `/home/sftpuser/apps/<service>/wordpress`, where `<service>` is the site's container-service name — or `null` when the service cannot be resolved. **Read it from the response; do not construct it.** |
| `ssh` | Key always present. When the site has no SFTP credentials the value is an **empty object `{}`** — not `null`, not absent. |
| `domain_cname` | The site's CDN hostname, assigned per site by the CDN. Use the returned value; there is no pattern to derive it from. |

**Pending-delete site** (`pending_delete: true`) — a reduced payload with a different key set:
```json
{
  "site": {
    "id": "<guid>", "name": "my-site", "primary_domain": "my-site.example.com",
    "created_at": "...", "updated_at": "...",
    "location": "pdx", "package": "Basic",
    "pending_delete": true, "status": "pending_delete",
    "delete_scheduled_at": "2026-09-01T00:00:00Z",
    "account": { "id": "<guid>", "name": "Acme" }
  }
}
```

`region`, `php_version`, `domain_cname`, `sftp_base_path`, `dunning_suspended`,
`domains`, `subscription` and `ssh` are **omitted entirely** in this branch — the site
is powered off, so those would either reach into a dead container or describe state
that no longer applies. `status` and `delete_scheduled_at` appear only here.

#### PATCH /api/sites/:id
Update name and/or change plan.
```json
{ "name": "new-site-name", "plan": "professional" }
```
- **Name-only** rename returns **`202`** (no body); a name validation failure returns **`422`** `{"errors":[...]}`.
- **Plan change** flows through the cart/billing system and returns the **same cart envelope** as orders (poll the cart) — it does **not** return a `task_id`. The envelope's `poll_url` is an **absolute URL**, not a path: request it as given rather than joining it onto the API base. Constraints/errors: `multi_site_resize_unsupported` (422, single-site accounts only), `subscription_not_proratable` (422), `no_price_for_plan` (422), `cart_pay_failed` (422), unknown/unavailable product — `unknown_product`/`product_unavailable` (400), `no_default_payment_method` (400), billing-settling guard (**422** `billing_settling`).
- Blocked by the pending-delete lock (**403** `pending_delete`).

#### POST /api/sites — no-op stub, returns `400`.

#### DELETE /api/sites/:id — soft-delete the site (async via job). Returns **`200`** with an empty body.

**Permission gate (stricter than every other write here).** The caller must hold the
**billing-management role** on the site's account — not merely site-edit permission.
Failing that, the request is refused with **`403`** `{"errors":["Not Authorized"]}`
before anything else runs.

Unlike the sibling permission checks, this one grants **no platform-staff bypass**: a
staff user who is not an actual member of the account holding that role is refused
exactly like any other caller.

Also blocked by the billing-settling guard (**422** `billing_settling`) and, for a site
already soft-deleted, by the pending-delete lock (**403** `pending_delete`).

---

### Pending-delete lock

A site can be **soft-deleted**: it stops running and is retained until a scheduled
purge. While it is in that state, **every nested resource under
`/api/sites/:site_id/...` documented in this file is locked — reads included, not just
writes**. That covers backups, backup exports, restores, restart, domains,
certificates, SSO and variants. Each returns:

**`403 Forbidden`**
```json
{ "errors": ["This site is pending deletion and is locked. Restore it to make changes."],
  "code": "pending_delete",
  "delete_scheduled_at": "2026-09-01T00:00:00Z" }
```

On the site resource itself the behaviour differs: `GET /api/sites` still lists the
site and `GET /api/sites/:id` still answers (with the reduced pending-delete payload
above), while `PATCH` and `DELETE /api/sites/:id` are locked like everything else.

A `403 pending_delete` is not an authorization problem and retrying will not clear it —
the site must be restored first. Check `pending_delete` on the site before calling any
nested endpoint.

---

### Sites / Backups

**Base route:** `/api/sites/:site_id/backups` — scopes `sites:read` / `sites:write`. (No feature flag.)

#### GET .../backups
Backups grouped by volume, as a JSON **object keyed by volume label**.
```json
{
  "wordpress": { "id": 1, "size": 10.5, "usage": 3.2, "archives": [ { "id": "abc123", "name": "Daily Backup", "created": "2024-01-15T10:00:00Z" } ] },
  "mysql": { "id": 2, "size": 5.0, "usage": 1.1, "archives": [ ... ] }
}
```
`size` = volume capacity (GB); `usage` = compressed/deduplicated backup size (GB).

Three distinct "nothing here" shapes — do not conflate them:

- **No volumes at all** → the response is `[]`, an empty **array**, not an empty object.
- **A volume with no backup configured** → that volume is **omitted entirely**; its label is not a key in the object. Absence of a key is not the same as an empty one.
- **A volume with a backup but no archives** → the key is present with an empty object `{}` (no `id`/`size`/`usage`/`archives`).

#### PATCH .../backups/:id — create backup
`:id` is the integer volume ID. Returns **`202`**. Unknown volume → `404` `{"errors":["Volume not found"]}`.
```json
{ "name": "Pre-migration snapshot" }
```

#### DELETE .../backups/:id — delete backup. Returns **`202`**. Unknown volume → `404` `{"errors":["Volume not found"]}`.
```json
{ "backup_id": "abc123" }
```

---

### Sites / Backup Exports

**Base route:** `/api/sites/:site_id/backups/:id/export` — download a backup archive as
a `.tar.gz`. The member segment is the **integer volume ID** (the route's member
parameter is `:id`, inherited from the backups resource — there is no `volume_id`
parameter), and `backup_id` is the archive ID; both come from the
[backups list](#sites--backups).

**Scope `sites:write` on BOTH the request and the status read**, and both also require
**edit** permission on the site. That is not a mistake: the status response hands back
a presigned URL that grants read of the entire site backup, so it is gated as a write
rather than a read — a `sites:read` token cannot retrieve it.

#### POST .../export — request an export. Returns **`202`**.

```json
{ "backup_id": "abc123" }
```

```json
{ "status": "preparing", "backup_id": "abc123" }
```

A `202` does **not** guarantee a *new* export started — if one is already in flight for
that volume the duplicate is dropped. The status endpoint reflects the real archive
state and is the only thing worth polling; there is no task id to follow.

#### GET .../export?backup_id=abc123 — export status

```json
{ "status": "ready", "url": "https://...", "expires_at": "2026-08-18T12:00:00Z", "size": 524288000 }
```

| Field | Type | Notes |
|-------|------|-------|
| `status` | String | `none`, `in_progress`, `ready`, `expired`, or `failed`. |
| `url` | String | **Only when `ready`.** Short-lived presigned HTTPS download URL. |
| `expires_at` | String (ISO 8601) | Only when `ready` — when that URL lapses. |
| `size` | Integer | Only when `ready` — export size in bytes. |
| `error` | String | Only when `failed` — human-readable reason. |

**`url` is a bearer secret** granting read of the whole backup. It appears only while
`ready`, only in this response body, and the response is sent `Cache-Control: no-store`.
Do not log it, cache it, or pass it on.

**Errors:** `422` `{"errors":["backup_id is required"]}` when `backup_id` is absent (on
either verb); `404` `{"errors":["Volume not found"]}` for an unknown volume;
`404` `{"errors":["Backup not found"]}` for an unknown archive on the status read.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/sites/$SITE_ID/backups/1/export?backup_id=abc123"
```

---

### Sites / Restores

**Base route:** `/api/sites/:site_id/restores` — scope `sites:write`.

#### PATCH .../restores/:id — restore a backup
`:id` is the volume ID; `backup_id` is the archive ID. Returns **`202`**.
Unknown volume → `404` `{"errors":["Volume not found"]}`.
```json
{ "backup_id": "abc123" }
```

---

### Sites / Restart

`POST /api/sites/:site_id/restart` — restart the WordPress container. No params. Returns **`202`**. Scope `sites:write`.

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  https://my.cloudpress.com/api/sites/$SITE_ID/restart
```

---

### Sites / Domains

**Base route:** `/api/sites/:site_id/domains` — scopes `sites:read` / `sites:write`. (No feature flag.)

#### GET .../domains — list site domains
#### POST .../domains — connect a domain. Returns **`202`**.

The domain becomes the site's **primary** when the site has none yet, otherwise it is
added as an **alias**. There is no parameter to choose — promote an existing alias with
`PATCH .../domains/:id` instead.

```json
{ "domain": "example.com", "provision_method": "cname" }
```
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `domain` | String | Yes | FQDN. Blank → **`400`** `{"errors":["Domain can't be blank."],"code":"domain_blank"}`. |
| `provision_method` | String | No | `cname` (default) or `dns` — any value other than the exact string `dns` is treated as `cname`. |
| `replace_records` | Boolean | No | See below — narrower than it looks. |

**`replace_records` only has an effect when the zone-conflict check actually runs**, and
that check runs in exactly one case: a `dns` connect that resolves onto a DNS zone
already hosted for this billing family. It is ignored for a `cname` connect, and
ignored for a `dns` connect where no family-hosted zone resolves (the manual
NS-delegation path). When the check does run and finds colliding records, the request
is rejected with `conflicts_found`; resend with `replace_records: true` to destroy
them and proceed.

**Success responses**

- CNAME: `{ "id": "<guid>", "cname": "<cname-target>" }` — the target is derived from the site's location/region. Point the record at the value this response returns.
- DNS (delegates the zone): `{ "id": "<guid>", "ns1": "<nameserver-1>", "ns2": "<nameserver-2>" }`

> **Nameservers are account-derived and are returned in this response — never hardcode
> them.** The pair resolves from the account's own nameservers, else the **highest** ancestor
> account's in the account chain, else a platform-wide default. They therefore differ
> between accounts and between resellers, and can change. Delegate the zone to exactly
> the two values `ns1`/`ns2` carry in the response you received. Delegating to a
> guessed or remembered hostname takes the domain dark.

**Error codes:**

| Code | Status | Meaning |
|---|---|---|
| `domain_blank` | `400` | No `domain` supplied. |
| `conflicts_found` | `422` | A `dns` connect hit existing records in the zone. The body carries a `conflicts` array describing them — retry with `replace_records: true` to replace them, or resolve them yourself first. |
| `hostname_in_use` | `422` | The hostname is already attached to a different site **anywhere in the billing family** — not just in the workspace you are calling with. The blocking site may therefore be one this token cannot see, including a pending-delete site still holding the hostname. |
| `invalid_domain` | `422` | Validation or ownership rejection. Also the answer for a `dns` request against a root that a **different** customer holds a registration for, which is refused so a zone name cannot be claimed out from under them. |

#### PATCH .../domains/:id — promote to primary. No params. **`202`**.
#### DELETE .../domains/:id — remove domain. **`202`**.

#### External-DNS Certificates (DNS-01)
Pre-provision a Bunny SSL cert for a hostname whose DNS is elsewhere. **Requires CDN active** (else `409 cdn_not_active`).

**Wildcard certificates are not supported by this flow and there is no `wildcard`
parameter or field anywhere in it.** Bunny validates the wildcard CNAME when the
hostname is registered, which cannot happen before DNS cutover — that would defeat the
entire point of pre-issuance. Request the exact hostname.

- `GET /api/sites/:site_id/domains/:id/certificate` — status (scope `sites:read`). The body has exactly these five keys:
  ```json
  { "provision_type": "dns01_external", "challenge": { ... },
    "requested_at": "...", "issued_at": null, "active": false }
  ```
  `provision_type` is one of `null` | `"http01"` | `"dns01_external"` | `"custom"`.
  `challenge` is the DNS-01 TXT record to add while issuance is pending, shape
  `{ "TxtRecordName": "_acme-challenge.host", "TxtRecordValue": "<token>", "ExpiresAt": "<iso8601>" }`,
  and is `null` otherwise. `requested_at` and `issued_at` are timestamps or `null`.
- `POST /api/sites/:site_id/domains/:id/request_certificate` — step 1. **Takes no parameters — the action reads no request body at all.** Returns the DNS-01 TXT challenge to add. (scope `sites:write` **and** site write/modify permission)
- `POST /api/sites/:site_id/domains/:id/complete_certificate` — step 2 (after the TXT record is live); Bunny validates and issues. (scope `sites:write` **and** site write/modify permission)
- `POST /api/sites/:site_id/domains/:id/refresh_certificate` — step 3, the recovery step. Re-reads the certificate status upstream: if a certificate is already active (for example one issued out-of-band through the standard flow) the domain is resolved; if issuance is still pending, completion is re-attempted. It never re-requests a new TXT challenge, so it is safe to call repeatedly while waiting. (scope `sites:write` **and** site write/modify permission)

All three write steps pass through the Bunny responder, so upstream failures surface as **`502`** and an unprovisioned CDN as **`409`** `cdn_not_active`.

---

### Sites / Mail (Transactional Email)

**Base route:** `/api/sites/:site_id/mail` — outbound transactional email for a
WordPress site (sender identity, DNS verification state, message log, send volume).
The route segment is `/mail`; the upstream provider (MailChannels) surfaces only in
error codes, never in a path.

| Method | Path | Scope | Site permission |
|---|---|---|---|
| `GET` | `/api/sites/:site_id/mail` | `sites:read` | read |
| `PATCH` \| `PUT` | `/api/sites/:site_id/mail/settings` | `sites:write` | edit |
| `DELETE` | `/api/sites/:site_id/mail/suspension` | `sites:write` | **edit** (not delete) |
| `POST` | `/api/sites/:site_id/mail/dns_check` | `sites:write` | edit |
| `GET` | `/api/sites/:site_id/mail/logs` | `sites:read` | read |
| `GET` | `/api/sites/:site_id/mail/metrics` | `sites:read` | read |

The overview read is the base route itself — `GET /api/sites/:site_id/mail`. There is
no `/overview` segment.

**These are the same two scopes that cover ordinary site management.** There is no
mail-specific scope: a token that already holds `sites:write` so it can rename a site
or change its plan can also rewrite that site's **sender identity** (the `From:` local
part and display name on every transactional message the site sends) and lift its
outbound-mail suspension. Grant `sites:write` with that in mind; a reporting client
needs only `sites:read`.

**Three subsystem-specific failures, on top of the usual site gates** (unknown site
**404** with no body, dunning **402** `service_suspended`, pending-delete **403**
`pending_delete` — see [Pending-delete lock](#pending-delete-lock) — and **403**
`{"errors":["Not Authorized"]}` when the caller lacks edit permission on a write):

| Code | Status | Meaning |
|---|---|---|
| `mailchannels_unavailable` | **503** | `{"errors":["Transactional email is not available."],"code":"mailchannels_unavailable"}`. The platform-level integration is not configured, so the whole subsystem is dark. The gate is platform-wide: all six endpoints answer this. |
| `mail_not_provisioned` | **422** | `{"errors":["This site has no transactional email account."],"code":"mail_not_provisioned"}`. The site never provisioned mail. |
| `mail_not_active` | **422** | `{"errors":["This site's transactional email account is not active."],"code":"mail_not_active"}`. Mail is provisioned but not yet active, so the sub-account credential the provider needs for reads does not exist yet. |

**A site with no mail account is a normal state, not a missing record — and reads and
writes answer it differently.** Do not treat it as a `404`:

- `GET .../mail` answers **`200`** with `{"mail": null}`.
- `PATCH .../mail/settings`, `DELETE .../mail/suspension` and `POST .../mail/dns_check`
  reject with **`422`** `mail_not_provisioned`.
- `GET .../mail/logs` and `GET .../mail/metrics` reject with **`422`**
  `mail_not_provisioned`, and then with **`422`** `mail_not_active` while `status` is
  anything other than `active`. These two are the only endpoints that require an
  active account.

Gate order matters when several apply. Unknown site (**404**) → dunning (**402**) →
pending-delete (**403**) → edit permission for `settings` and `dns_check` (**403**) →
`mailchannels_unavailable` (**503**) → `mail_not_provisioned` (**422**) →
`mail_not_active` (**422**) → per-endpoint validation. `DELETE .../mail/suspension` is
the one exception: its edit-permission check runs *after* the **503**, so on a platform
with no mail integration a read-only member sees `mailchannels_unavailable` rather than
`Not Authorized`.

#### GET .../mail — transactional email state

Returns `{"mail": {...}}`, or `{"mail": null}` for a site that never provisioned mail.
The `mail` key is always present. Every key inside `mail` is always present too — a
missing value is `null`, never an absent key.

```json
{
  "mail": {
    "status": "active",
    "configured": true,
    "notifications_active": true,
    "dns": {
      "verdict": "verified",
      "spf_verified": true, "dkim_verified": true, "lockdown_verified": true,
      "all_verified": true, "locally_checked": false,
      "checked_at": "2026-08-19T04:11:02Z"
    },
    "sender_identity": {
      "from_email": "noreply@example.com",
      "from_local_part": "noreply", "from_name": "my-site",
      "mail_from_local_part": null, "mail_from_name": null,
      "dkim_domain": "example.com"
    },
    "suspension": {
      "suspended": false, "abuse": false, "system": false,
      "reason": null, "suspended_at": null,
      "can_self_unsuspend": false, "remaining_self_unsuspends": 2
    },
    "created_at": "...", "updated_at": "..."
  }
}
```

| Field | Type | Notes |
|---|---|---|
| `status` | String | `pending`, `active` or `failed`. Only `active` satisfies the `mail_not_active` gate on logs and metrics. |
| `configured` | Boolean | Whether a mail configuration is currently in place on the site's WordPress engine. `false` means nothing is configured on the site itself, whatever `status` says. |
| `notifications_active` | Boolean | Whether this mail account is enrolled for lifecycle email notifications. Read-only — no endpoint here changes it. |
| `dns.verdict` | String | `unknown`, `verified` or `failed`. **`unknown` is a hold, not a failure** — it means no provider answer is on file, or the only answer on file is a locally predicted one. Do not surface it as broken. |
| `dns.spf_verified` `dns.dkim_verified` `dns.lockdown_verified` | Boolean | Per-record verdicts; `true` only when the provider reported that record as passing. |
| `dns.all_verified` | Boolean | All three of the above. |
| `dns.locally_checked` | Boolean | `true` when the verdict on file is a local prediction rather than a provider answer. This is the distinction `verdict: "unknown"` collapses. |
| `dns.checked_at` | String (ISO 8601) \| `null` | When the verdict on file was last stamped — **not** evidence a provider answered. Provisioning and a primary-domain promotion also stamp it, from a purely local prediction, and one path stamps it even when no verdict was resolved at all. **Do not read a non-null `checked_at` as "the provider has checked"** — use `dns.locally_checked` above, which is the field that actually separates the two. |
| `sender_identity.from_email` | String \| `null` | Effective `From:` address, composed as `from_local_part@dkim_domain`. **`null` until `dkim_domain` is set** — it is never composed from the site's primary domain, and the two differ while a DKIM key rotation is in flight. |
| `sender_identity.from_local_part` | String | Effective local part, defaults applied — `noreply` when no override is stored. Never `null`. |
| `sender_identity.from_name` | String | Effective display name, defaults applied: the stored override, else the site name, with control characters replaced by spaces, whitespace collapsed, and truncated to 255 bytes. Never `null`. |
| `sender_identity.mail_from_local_part` `sender_identity.mail_from_name` | String \| `null` | The **stored overrides only** — `null` when the default is in force. These are the two values `PATCH .../mail/settings` writes; the `from_*` pair above is what is actually used. |
| `sender_identity.dkim_domain` | String \| `null` | Domain whose DKIM key signs this site's mail. |
| `suspension.suspended` | Boolean | Outbound mail is currently held. |
| `suspension.abuse` / `suspension.system` | Boolean | Which kind of hold. `system` is a platform billing/lifecycle hold — `reason` is `Payment overdue` or `Site deleted`; `abuse` is anything else. Both are `false` when not suspended. |
| `suspension.reason` | String \| `null` | Human-readable hold reason. |
| `suspension.suspended_at` | String (ISO 8601) \| `null` | |
| `suspension.can_self_unsuspend` | Boolean | Whether `DELETE .../mail/suspension` would be accepted right now. **Check this before calling it** — see that endpoint for the four cases that make it `false`. |
| `suspension.remaining_self_unsuspends` | Integer | Self-lifts left in the current 30-day allowance window: `2` once the window has lapsed, otherwise `2` minus the number used, clamped to `0..2`. |
| `created_at` / `updated_at` | String (ISO 8601) | |

The response never carries the sub-account's API key, SMTP password or configuration
digest — there is no field for them.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  https://my.cloudpress.com/api/sites/$SITE_ID/mail
```

#### PATCH .../mail/settings — sender identity

`PATCH` or `PUT`. Writes the two sender-identity overrides. **Flat params — no wrapper
key.** Returns **`200`** with the same `{"mail": {...}}` object as `GET .../mail`.

```json
{ "mail_from_local_part": "hello", "mail_from_name": "Acme Support" }
```

| Param | Type | Required | Notes |
|---|---|---|---|
| `mail_from_local_part` | String \| `null` | No | The part before the `@`. Must match `\A[A-Za-z0-9]([A-Za-z0-9._%+-]*[A-Za-z0-9])?\z` (alphanumeric at both ends), contain no consecutive dots, and be at most **64 bytes**. Blank or `null` clears the override and restores the default `noreply`. |
| `mail_from_name` | String \| `null` | No | Display name. No control characters; at most **255 bytes** (bytes, not characters — a multi-byte name hits the cap sooner). Blank or `null` clears the override, so `from_name` falls back to the site name. |

Only these two keys are read; anything else in the body is ignored. Both are also
**used**, not merely permitted — each supplied key is written. Omitting a key leaves
that override unchanged, so this is a partial update: send `""` or `null` explicitly to
clear one.

**Saving is decoupled from pushing.** The values persist even when DNS is unverified,
and this action makes no upstream call — a background reconciliation pushes them.
So a `200` here means *stored*, not *live at the provider*: re-read `GET .../mail` and
watch `configured` / `sender_identity.from_email` to see the change take effect.

- **`422`** `{"errors":[...],"code":"invalid_sender_identity"}` — validation rejected the
  values. `errors` carries human-readable English messages.
- **`422`** `mail_not_provisioned`, **`403`** `Not Authorized` without edit permission.

```bash
curl -X PATCH -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{"mail_from_local_part":"hello","mail_from_name":"Acme Support"}' \
  https://my.cloudpress.com/api/sites/$SITE_ID/mail/settings
```

#### DELETE .../mail/suspension — lift an outbound-mail hold

**This endpoint lifts a suspension; it does not create one and deletes nothing else.**
The resource being deleted is the *suspension*. On success it clears the hold,
reactivates the sub-account with the provider, schedules a background reconciliation,
and returns **`200`** with the
same `{"mail": {...}}` object as `GET .../mail` (re-read from the refreshed record, so
`suspension.suspended` is already `false` in the response).

It requires **edit** permission, not delete permission — the same permission the
control panel requires to lift a hold. Scope is `sites:write`.

Refused with **`403`** `{"errors":["This suspension cannot be lifted from here."],"code":"unsuspend_not_allowed"}`
in four cases: the account is not suspended at all; the hold is a platform
billing/lifecycle hold (`suspension.system` is `true`); an abuse verdict is parked
awaiting an existing hold's release; or the self-lift allowance for the current 30-day
window is spent. Check `suspension.can_self_unsuspend` on `GET .../mail` first — it is
the authoritative signal, and the parked-verdict case is **not** visible in any other
response field, so a `false` there cannot always be explained from the rest of the
payload.

If the provider refuses the reactivation, the response is **`422`**
`{"errors":["Could not lift the suspension. Please try again later."],"code":"unsuspend_failed"}`
and the hold stands. Also **`422`** `mail_not_provisioned`.

#### POST .../mail/dns_check — queue a DNS re-check

Queues a re-check of the site's mail DNS records (SPF, DKIM, domain lockdown) instead
of waiting for the scheduled sweep. Takes no parameters. Returns **`202`**:

```json
{ "status": "queued" }
```

`status` is the literal string `queued` — it is not a task id and there is nothing to
poll on this endpoint. Read the verdict from `GET .../mail`: `dns.checked_at` advances
and `dns.verdict` / the three `*_verified` flags are rewritten when the check lands. If
the provider check itself fails, nothing is written, so `checked_at` may not advance at
all — treat an unchanged `checked_at` as "no answer yet", not as a failure.

**Rate limited to one accepted check per site per 5 minutes**, returning **`429`**
`{"errors":["A DNS check for this site ran within the last 5 minutes."],"code":"rate_limited"}`.
The window opens on the accepted request. The limiter is shared with the control
panel's own re-check button: a check triggered there blocks this endpoint for the rest
of the window and vice versa, so the API cannot be used to bypass it.

Also **`422`** `mail_not_provisioned`, **`403`** `Not Authorized` without edit
permission.

#### GET .../mail/logs — outbound message log

Searches the site's outbound message log at the provider. Requires an **active** mail
account (**`422`** `mail_not_active` otherwise). Scope `sites:read`.

| Param | Type | Required | Notes |
|---|---|---|---|
| `rcpt` | String | No | Recipient match. Blank/absent values are dropped from the query rather than sent as empty. |
| `sender` | String | No | Sender match. |
| `subject` | String | No | Subject match. |
| `start_date` | String | No | `YYYY-MM-DD`. Expanded to `<date>T00:00:00Z` before it is sent upstream. |
| `end_date` | String | No | `YYYY-MM-DD`. Expanded to `<date>T23:59:59Z`. |
| `delivered` | String | No | `Y` or `N` (case-insensitive). `N` is the failures-only view. **Any other value is silently ignored** — the filter is simply not applied, so a typo returns everything rather than an error. |
| `start_at` | Integer | No | Page cursor (offset), **clamped to `0..10000`**. |

The three text fields are separate named params — there is no `search_field`/`query`
pair on this endpoint. There is **no page-size parameter**: the page size is fixed
server-side, and paging advances via `start_at`.

**The date range is not validated locally.** Whatever you send is expanded and forwarded
to the provider as-is: an inverted range (`start_date` after `end_date`), or a value that
is not a date at all, is not rejected here. The observable outcome is therefore whatever
the provider does with it — either a normal `200` with `total: 0`, or, if the provider
refuses the query, **`502`** `{"errors":["Could not fetch logs from MailChannels."],"code":"log_search_failed"}`.
Validate ranges client-side.

```json
{
  "messages": [
    { "sender": "noreply@example.com", "rcpt": "customer@example.com",
      "subject": "Your receipt", "delivered": true,
      "rspcode": "<smtp-code>", "rspmsg": "...",
      "spam_disposition": null, "timestamp": "..." }
  ],
  "total": 412, "start_at": 0, "page_count": 50,
  "next_start_at": 50, "prev_start_at": null
}
```

| Field | Type | Notes |
|---|---|---|
| `messages` | `Array<Object>` | Each element carries exactly these eight keys, always present; a value the provider did not supply is `null`. |
| `messages[].sender` `messages[].rcpt` `messages[].subject` | String \| `null` | |
| `messages[].delivered` | Boolean \| String \| `null` | **The provider's value, passed through unchanged — it arrives as either a boolean or the strings `"true"`/`"false"`, and is `null` when absent.** Handle all three; do not assume a boolean. Note the asymmetry with the request: the *filter* is `Y`/`N`, the *field* is not. |
| `messages[].rspcode` | String \| `null` | SMTP response code. The leading digit is the classification used elsewhere in this API: `2` delivered, `4` or `5` failed, `5` permanently rejected. |
| `messages[].rspmsg` | String \| `null` | SMTP response text. |
| `messages[].spam_disposition` | String \| `null` | Provider-supplied, **unfiltered** — this surface does not suppress no-op values, so expect placeholder-ish values here as well as real dispositions. |
| `messages[].timestamp` | String \| `null` | |
| `total` | Integer | Matching messages upstream, before this endpoint's own filtering (below). |
| `start_at` | Integer | The **effective** (clamped) offset of this page. Compare it against what you sent: past `10000` it will differ, and further paging is not possible. |
| `page_count` | Integer | The **raw** page size upstream returned, before filtering. Paging advances by this, so it — not `messages.length` — is what a "showing X–Y of N" footer must count. |
| `next_start_at` | Integer \| `null` | Cursor for the next page; `null` on the last page. |
| `prev_start_at` | Integer \| `null` | Cursor for the previous page; `null` on the first. |

**`messages.length` can be smaller than `page_count`, and a page can even come back
empty while `next_start_at` is non-`null`.** Intermediate relay/queue-acceptance entries
and internal placeholder rows are dropped from `messages` after the page is counted.
Drive pagination from `next_start_at`, never from `messages.length`.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/sites/$SITE_ID/mail/logs?delivered=N&start_date=2026-08-01&end_date=2026-08-19"
```

#### GET .../mail/metrics — send volume, engagement and quota

Requires an **active** mail account (**`422`** `mail_not_active` otherwise). Scope
`sites:read`.

| Param | Type | Required | Notes |
|---|---|---|---|
| `days` | Integer | No | Lookback window, default `30`. Parsed **base 10** (`010` is ten days, not eight) with surrounding whitespace stripped. A **numeric** value out of range is clamped to `1..90`. A present-but-unparseable value (`days=abc`, `days=0x1e`) is **refused with `400`** and code `invalid_days` rather than coerced — it does not silently answer a one-day window. |

Read the effective window back from the response's `days`, which is the clamped value.

```json
{
  "days": 30,
  "volume": {
    "processed": { "2026-07-21": 12, "2026-07-22": 0 },
    "delivered": { "2026-07-21": 11, "2026-07-22": 0 },
    "dropped":   { "2026-07-21": 1,  "2026-07-22": 0 },
    "bounced":   { "2026-07-21": 1,  "2026-07-22": 0 }
  },
  "engagement": { "opens": { "2026-07-21": 4 }, "clicks": { "2026-07-21": 1 } },
  "usage": {
    "period_start": "...", "period_end": "...",
    "sent": 812, "limit": 2500,
    "usage_pct": 32, "cycle_pct": 60, "projected": 1353, "projected_pct": 54
  }
}
```

The `volume` block above is abridged: each of its four series carries **one key per
date in the window** — 30 keys at the default.

| Field | Type / unit | Notes |
|---|---|---|
| `days` | Integer (days) | Effective window after clamping to `1..90`. |
| `volume.processed` `volume.delivered` `volume.dropped` `volume.bounced` | Object: `YYYY-MM-DD` → Integer (delivery **attempts**) | All four keys always present. Each is **zero-filled for every date in the window**, so the key set is exactly `days` dates ending on the current date — a quiet day is `0`, not a missing key. An empty object `{}` appears only if the whole series could not be built. Series meanings below. |
| `engagement.opens` `engagement.clicks` | Object: `YYYY-MM-DD` → Integer | Both keys always present, `{}` when the provider returned nothing. **Not zero-filled** — unlike `volume`, only dates the provider actually reported appear, so a missing date means "not reported", and the two blocks do not share a key set. |
| `usage` | Object \| `null` | **`null`** when the provider returned no usage figure for the period. The key is always present. |
| `usage.period_start` `usage.period_end` | String (ISO 8601) | The current cycle, anchored on the date the site's mail account was provisioned and advancing in whole months — **not** the account's invoice period. |
| `usage.sent` | Integer (messages) | Provider-reported sends in the current period. |
| `usage.limit` | Integer (messages) | The site's configured send allowance for the period; `0` when none is set. Read it from the response — it is not derivable from the plan name. |
| `usage.usage_pct` | Integer (whole percent) | `sent` as a percentage of `limit`, rounded. `0` when `limit` is `0`. **Not capped — it can exceed 100.** |
| `usage.cycle_pct` | Integer (whole percent) | How far through the cycle the current time is, rounded, `0..100`. |
| `usage.projected` | Integer (messages) | End-of-cycle projection at the current daily rate, rounded. `0` for the first day of a cycle, before a full day has elapsed. |
| `usage.projected_pct` | Integer (whole percent) | `projected` as a percentage of `limit`, rounded and **capped at 100**. `0` when `limit` is `0`. Note the asymmetry with `usage_pct`, which is not capped. |

The four `volume` series:

- `processed` — every attempt counted for that date.
- `delivered` — the attempt's `delivered` flag was `true` (or the string `"true"`); when
  that flag is absent or unrecognised, an `rspcode` starting with `2` counts as delivered.
- `dropped` — the mirror image: `delivered` was `false`/`"false"`, or, absent that flag,
  the `rspcode` starts with `4` or `5`. `4xx` deferrals and `5xx` rejections alike.
- `bounced` — the subset of `dropped` whose `rspcode` starts with `5`. A failure carrying
  no response code at all raises `dropped` only, never `bounced`.

**`dropped` and `bounced` are nested, not additive.** `dropped` ⊇ `bounced`; adding them
double-counts every permanent rejection. `bounced` counts only `5xx` responses — a `4xx`
deferral raises `dropped` alone.

**Counts are per delivery attempt, not per message.** The log is not collapsed by
message, so a message deferred twice and then delivered contributes `2` to `dropped`
and `1` to `delivered`, and `processed` counts attempts too. Intermediate
relay/queue-acceptance entries are excluded.

**`volume` is derived from a bounded walk of the message log — at most 10 pages of 50
entries.** A site sending more than roughly 500 attempts inside the window will see
**truncated** volume counts; the series is not a complete aggregate for high-volume
sites. `engagement` comes from a separate provider metrics call and is not subject to
that cap, so the two blocks can disagree. `usage.sent` is the provider's own
period counter and is likewise independent of the walk — trust it over
`sum(volume.processed)` for quota questions.

Each call makes several upstream round trips (the log walk plus two provider reads) and
nothing is cached. **Poll it sparingly** — it is not a cheap endpoint.

**An upstream failure degrades silently instead of erroring.** This endpoint has no
equivalent of the log endpoint's `log_search_failed`: if the provider refuses or is
unreachable, the response is still **`200`** — the `volume` series come back
zero-filled, `engagement` comes back as `{}` objects, and `usage` comes back `null`. A
quiet site and an upstream outage are indistinguishable from this response alone; if
that matters, corroborate with `GET .../mail/logs`, which does surface a **`502`**.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/sites/$SITE_ID/mail/metrics?days=7"
```

---

### Sites / SSO

**Base route:** `/api/sites/:site_id/sso` — **OAuth-blocked** (session/API-key only).

#### GET .../sso — list WordPress users
```json
{ "users": [ { "ID": 1, "user_login": "admin", "display_name": "Admin",
  "user_email": "admin@example.com", "user_registered": "...", "roles": "administrator",
  "url": "https://example.com/wp-admin/?autologin=1&..." } ] }
```

#### POST .../sso — generate SSO URL
```json
{ "kind": "wordpress", "username": "admin" }
```
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `kind` | String | No | `wordpress` (default if omitted/unknown) or `database` |
| `username` | String | Yes for non-`database` | WP username; ignored for `database` |

Success → `200` `{ "url": "..." }`.

Two different failure statuses — they are not interchangeable:

- **`422`** `{"errors":["Missing username"]}` — request validation, raised before anything is attempted, when `kind` is anything other than `database` and `username` is blank or absent. Fix the request and retry.
- **`400`** `{"errors":[...]}` — the SSO generation itself failed downstream. The message comes from the underlying service; retrying the same request usually will not help.

**Authorization:** without `wp_login`, you can only generate URLs for WP users the token's user is linked to; with `wp_login`, any user in the index.

#### Top-level `POST /api/sso`
Reserved stub — always returns **`401`** (account-level SSO not implemented). Requires `X-Auth-Account`.

---

### Sites / Variants (PHP version)

**Base route:** `/api/sites/:site_id/variants` — scopes `sites:read` / `sites:write`.

- `GET .../variants` — `{ "php": [ { "id": 2, "label": "PHP 8.2", "is_default": true, "active": true } ] }`

  The `php` key is always present, but its value has three states: an array of variants, an **empty array** `[]` when the site's image exposes no variants, or **`null`** when the variant list could not be retrieved at all. Handle `null` — it is not the same as "no versions available".
- `PATCH .../variants/php` — change PHP version; body `{ "variant_id": 3 }`; returns **`202`** `{ "task_id": 456 }`. Non-`php` variant → `422`.
