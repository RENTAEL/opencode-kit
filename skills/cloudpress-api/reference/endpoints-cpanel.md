# cPanel Hosting

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

cPanel hosting accounts are a separate product from WordPress sites: a cPanel account
with its own control panel, domains and mailboxes, billed through the same order and
checkout flow as sites. All routes below **require `X-Auth-Account`**
(absent → **`400`** `{"errors":["Missing X-Auth-Account"],"code":"missing_account"}`).

**Availability gate.** cPanel hosting is limited to workspaces that are already
cPanel customers. Every endpoint here returns **`403`**
`{"errors":["cPanel hosting isn't available for this workspace."],"code":"cpanel_not_enabled"}`
for a workspace that is not, and **`503`** `{"errors":[...],"code":"cpanel_unavailable"}`
when the hosting platform cannot be reached (also used when a mirrored read fails,
and when a requested domain could not be verified against the servers).
`cpanel_not_enabled` is not retryable.

**`cpanel_unavailable` is not reliably retryable**, despite the `503`. The identical
code and body are returned both when the hosting platform is genuinely unreachable
(transient — a retry may succeed) **and** when cPanel is simply not configured on the
deployment at all (permanent — a retry never will). The two are indistinguishable from
the response, so bound your retries instead of looping indefinitely.

**OAuth reach.** `cpanel:read` reaches the two reads (`GET /api/cpanel_accounts`,
`GET /api/cpanel_accounts/:username`) and the domain **list**. There is **no
`cpanel:write` scope**: every write here is OAuth-blocked and needs a session or
API-key credential (**`403`** `{"error":"insufficient_scope","error_description":"endpoint not available via OAuth"}`).
A system account-bearer key (no user) is rejected on writes with **`401`** `user_required`.
That api_key/session requirement is deliberate — these endpoints move money or hand
over full control of the hosting account, and the API has no step-up auth, so a
first-class credential plus a role check stands in for the portal's re-authentication
prompt.

**Reads do not require a user.** The `user_required` rule is scoped to the writes
only, so a **system account-bearer key with no user attached can call both reads and
the domain list** — `GET /api/cpanel_accounts`, `GET /api/cpanel_accounts/:username`
and `GET .../domains`. The asymmetry is deliberate: making a cPanel account's domain
list stricter than the account record itself would serve no purpose. Unattended
inventory and reconciliation jobs can therefore run on a system key; only the writes
need a real user.

**Role gates** are evaluated on the account that **owns** the cPanel account, not on
`X-Auth-Account` — a user who manages billing in one workspace but is view-only in
another cannot mutate the other's hosting. Failure is **`403`**
`{"errors":["Not Authorized"],"code":"not_authorized"}`.

| Operation | Required on the owning account |
|---|---|
| Order, resize, change password, add/remove a domain | `billing` (manage billing) |
| Cancel, purge | Site-lifecycle role (members only — non-member staff excluded) |
| Create a control-panel session | `can_edit` |

**One exception — Order.** `POST /api/cpanel_accounts` has no cPanel account to own it
yet, so its `billing` check falls back to the workspace named by **`X-Auth-Account`**.
Every other operation in the table resolves the owning account from the existing
account first and only falls back when it cannot.

**Not-found is `404` for both unknown and unauthorized usernames** —
`{"errors":["cPanel account not found."],"code":"account_not_found"}` — deliberately,
so the endpoint cannot be used to probe which usernames exist elsewhere on the
platform.

**Trial workspaces** are refused with **`403`** `trial_account` on the account order and
resize, and on every nested write (password, purge, session, domain add/remove).
Cancelling an account (`DELETE /api/cpanel_accounts/:username`) is deliberately **not**
trial-gated — a trial workspace that somehow holds an account can still cancel it.

---

### cPanel Accounts

**Base route:** `/api/cpanel_accounts` — the `:username` segment is the cPanel
username, constrained to `[A-Za-z0-9_]+`. Reads scope `cpanel:read`; writes OAuth-blocked.

#### GET /api/cpanel_accounts — list accounts

Query params: `page`, `per_page` (default `50`, max `100`), and `q`.

`q` matches (case-insensitively, as a substring) the **username**, the **server**
hostname, the account's **main domain**, and its **alias / add-on** domains.
**Subdomains are not searched** — rows the hosting server types as `main` or `sub` are
excluded from the domain-match branch, so searching for `shop.example.com` will not
find it as a subdomain.

The response carries **no pagination metadata at all** — no total, no page count, no
next-page link, just the `cpanel_accounts` array.

**Do not page until the array comes back empty.** Because `provisioning` rows are
appended to every page (see below), a page past the end of the real results still
returns those rows rather than an empty array — a naive "loop until empty" never
terminates while any account is provisioning. Stop when a page returns no rows you
have not already seen, and see the caps below for why reaching the end still does not
mean you saw everything.

```json
{
  "cpanel_accounts": [
    {
      "username": "acme123",
      "primary_domain": "example.com",
      "package": { "code": "M", "key": "basic", "label": "Basic" },
      "disk": { "used_mb": 2048, "quota_mb": 10240 },
      "server": "web12.example.net",
      "mailbox_count": 4,
      "addon_domain_count": 1,
      "state": "active",
      "delete_scheduled_at": null,
      "subscription": { "id": "<guid>", "status": "active", "term": "monthly" },
      "account": { "id": "<guid>", "name": "Acme" }
    }
  ]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `username` | String | The cPanel username — the `:username` path segment for every other endpoint here. |
| `primary_domain` | String / null | The account's main domain. |
| `package` | Object | `{ code, key, label }` — the **live** package on the hosting server. `code` is the raw server-side code — `S`/`M`/`L`/`XL` for catalog packages, but whatever the server reports otherwise — and `key` the catalog key (`mini`/`basic`/`pro`/`max`). **All three sub-fields are nullable** — see below. |
| `local_package` | String | **Present only** while the package CloudPress last provisioned disagrees with the live mirror, **in either direction** (see below). Absent otherwise; do not treat its absence as an error, and do not use it as a resize-completion signal (poll the order for that). |
| `disk` | Object | `{ used_mb, quota_mb }`. |
| `server` | String / null | Normalized hostname of the server holding the account. |
| `mailbox_count` | Integer | Falls back to `0` when the mirror cannot be read. |
| `addon_domain_count` | Integer | |
| `state` | String | `active`, `provisioning`, `dunning_suspended`, `admin_suspended`, or `pending_deletion`. `pending_deletion` wins over both suspension states — it is terminal and changes which operations are possible. |
| `delete_scheduled_at` | String (ISO 8601) / null | The frozen purge date once cancelled; `null` while live. |
| `subscription` | Object / null | `{ id, status, term }`. Emitted as an explicit **`null`** when the account has none — present-but-null, not omitted. |
| `account` | Object | `{ id, name }` — the owning account. **Omitted entirely** when there is no local link, or the link has no account — **absent, not `null`**. See below. |

**`account` can be missing, and that is a supported state.** It is emitted only when a
local link exists *and* that link has an account. A workspace authorized by cPanel
customer id alone holds accounts with no local link at all, and those rows carry no
`account` key. Note the deliberate contrast with `subscription` in the same row, which
*is* emitted as an explicit `null`: the two absences are encoded differently, so
`resp.account.id` raises rather than yielding `null`. Test for the key's presence
before reading through it.

**All three `package` sub-fields are nullable.** `key` is **`null` for any package code
outside the four-entry catalog** — the code path handles that explicitly as a real
legacy case (accounts on packages predating the catalog), so treat a null `key` as
normal data, not an error, and key your own logic on `code` when you need to round-trip
an unknown package. `label` falls back to the raw code and is `null` only when that is
empty too; `code` is `null` when the mirror reports no package at all.

**`local_package` is emitted on *any* disagreement**, not only the mirror-lag case. It
appears whenever the package CloudPress last provisioned differs from the live mirror
in either direction — including an out-of-band package change made on the hosting
server that the mirror has *already* caught up with, where the stale value is
CloudPress's own. It is also never emitted on `provisioning` rows, which have no live
mirror value to disagree with.

- A just-ordered account appears with `state: "provisioning"` and the
  mirror-sourced fields (`disk`, `server`) null and the counters `0`, so a client
  that just POSTed can find its account before the hosting mirror syncs.
- **Those `provisioning` rows are appended to *every* page.** They come from a
  separate query that is not paginated, not filtered by `q`, and not subject to the
  500-row caps below, and they are concatenated onto the end of each page's array. A
  client paging through the list receives **the same provisioning rows repeated on
  every page** — de-duplicate on `username` rather than accumulating pages blindly.
  They are also why "at most 500 rows in total" is not literally true.
- Mail-only accounts are **not** listed — they are not cPanel hosting accounts and
  the other endpoints here `404` on them.
- **Ceiling: several independent 500-row caps sit under this endpoint**, so a
  workspace with more accounts than that cannot reach the remainder however it pages.
  **Narrowing with `q` does not help** — `q` filters the already-capped set in memory,
  after the cap has been applied, so it can only ever return a subset of the same 500
  and never reaches what the cap left out. If you may be near the ceiling, treat this
  endpoint as incomplete rather than authoritative.
  - The **username allow-list** that seeds the read is capped **with no ordering** —
    a `DISTINCT … LIMIT 500` with no `ORDER BY`. *Which* 500 usernames it yields is
    therefore undefined and need not be stable between calls.
  - The **hosting-mirror fetches** keyed on those usernames are each capped at 500
    too, but those **are** ordered by username. The unordered layer is the allow-list,
    not the mirror.

**Codes:** `400` `missing_account`, `403` `cpanel_not_enabled`, `503` `cpanel_unavailable`.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/cpanel_accounts?q=example.com"
```

#### GET /api/cpanel_accounts/:username — view one account

The same object as the list, under a `cpanel_account` key.

**Codes:** `400` `missing_account`, `403` `cpanel_not_enabled`, `404` `account_not_found`, `503` `cpanel_unavailable`.

This read is deliberately **not** blocked while the account is suspended or pending
deletion — a client can always still see why an account is locked.

#### POST /api/cpanel_accounts — order an account. Returns **`202`**.

Payment-first: this charges the billing account's saved default payment method
off-session and provisions asynchronously. **OAuth-blocked.**

```json
{ "package": "basic", "term": "monthly", "domain": "example.com",
  "callback": { "url": "https://your-app.com/webhook", "authorization": "Bearer your-secret" } }
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `package` | String | Yes | Catalog key (`mini`/`basic`/`pro`/`max`) or server code (`S`/`M`/`L`/`XL`). |
| `term` | String | No | `monthly` or `annual`; defaults to the workspace's billing term. |
| `domain` | String | No | A domain the workspace **already owns** and that is actually registered, used as the account's main domain. Omit and the platform generates a placeholder domain. Registering a new domain in the same cart is not supported here — call `POST /api/orders/domain` first. |
| `callback` | Object | No | Same contract as `POST /api/orders` (`url`, `authorization`). |

**Response — `202 Accepted`**, the same cart envelope as
[`POST /api/orders`](endpoints-orders.md#orders):

```json
{ "status": "accepted",
  "cart":    { "token": "<cart_token>", "status": "...", "rollup_status": "...",
               "poll_url": "https://my.cloudpress.com/api/carts/<token>" },
  "payment": { "status": "...", "method_type": "card", "hosted_invoice_url": "..." },
  "orders":  [ { "id": "<uuid>", "status": "pending",
                 "poll_url": "https://my.cloudpress.com/api/orders/<id>" } ] }
```

Both `poll_url` values are **absolute URLs**, not paths — don't prepend your base URL
to them.

`orders` is **empty** during the async window on Stripe-billed plans (the order is
minted once the charge settles) — poll `cart.poll_url`. Branch on the envelope, not on
the HTTP status. Note the two cPanel operations differ: the **order** (`POST`) is a fresh
charge, so a decline or 3DS challenge surfaces as `payment.status:
"awaiting_authentication"`; the **resize** (`PATCH`) is a proration and surfaces the same
situation as `processing` with a populated `payment.hosted_invoice_url`. See
[Carts](endpoints-orders.md#carts).

**Codes:** `400` `missing_account` / `unknown_package` / `invalid_term` /
`product_unavailable` / `no_default_payment_method`; `401` `user_required`; `403`
`cpanel_not_enabled` / `trial_account` / `not_authorized`; `422` `no_price_for_plan` /
`domain_not_owned` / `domain_not_registered` / `domain_in_use` / `cart_add_failed` /
`cart_pay_failed`; `503` `cpanel_unavailable`.

`domain_not_owned` means the name is not in this workspace; `domain_not_registered`
means it is not registered anywhere; `domain_in_use` means it is already live on
another hosting account.

The `400` `no_default_payment_method` body carries a third key, **`remediation`**,
alongside the usual `errors` and `code` — a human-readable string naming the fix
(adding a default payment method to the billing account). Surface it rather than
writing your own copy:

```json
{ "errors": ["No default payment method configured for the billing account."],
  "code": "no_default_payment_method",
  "remediation": "Add a default payment method to the billing account before creating orders via the API." }
```

#### PATCH /api/cpanel_accounts/:username — resize. Returns **`202`**.

Changes the package and re-prorates billing. **OAuth-blocked.** The billing **term is
never changed by a resize** — the new package is priced on the live subscription's
current term.

```json
{ "package": "pro" }
```

`package` (required) is the only parameter — there is no `term`, `domain` or
`callback` here, so this endpoint never returns `invalid_term`, `domain_not_owned` or
`domain_in_use`. Response is the same cart envelope as `POST`.

**Codes:** as `POST` for `400` `missing_account` / `unknown_package` /
`product_unavailable` / `no_default_payment_method`, `401` `user_required`, `403`
`cpanel_not_enabled` / `trial_account` / `not_authorized`, `422` `no_price_for_plan` /
`cart_add_failed` / `cart_pay_failed`, `503` `cpanel_unavailable`. Plus:

| Code | Status | Meaning |
|---|---|---|
| `service_suspended` | `402` | Suspended for an unpaid invoice. |
| `account_suspended` | `403` | Suspended by staff — contact support. Reported ahead of `service_suspended` when both hold, because the customer cannot clear it themselves. |
| `pending_deletion` | `403` | The account is pending deletion; recover it first. Body carries `delete_scheduled_at`. |
| `account_not_found` | `404` | |
| `resize_in_flight` | `409` | An earlier package change is still applying. Wait for it — a retry during the async charge window is refused rather than charged twice. |
| `same_package` | `422` | Already on that package. Matched against **both** the live server package and the last one CloudPress provisioned, so a retry inside the mirror-lag window cannot double-charge. |
| `usage_exceeds_package` | `422` | **Downgrades only.** The target package is smaller than current disk / mailbox / add-on-domain usage. Upgrades are never usage-checked. |
| `no_billing_subscription` | `422` | Stripe-billed plan with no Stripe-linked subscription (a migrated account never billed through CloudPress). |
| `subscription_not_proratable` | `422` | The cart could not be staged as a proration; refused rather than charged as a new purchase. |

#### DELETE /api/cpanel_accounts/:username — cancel. Returns **`202`**.

Soft-delete: stamps the retention window, cancels billing (stopping renewals and
crediting the unused first term), and suspends the account on the hosting server. It
stays recoverable from the control panel until `delete_scheduled_at`.
**OAuth-blocked**; needs the site-lifecycle role.

```json
{ "status": "pending_deletion", "username": "acme123", "delete_scheduled_at": "2026-08-25T00:00:00.000Z" }
```

**Codes:** `400` `missing_account`, `401` `user_required`, `403` `cpanel_not_enabled` /
`not_authorized`, `404`
`account_not_found`, `422` `account_already_purged` (the account's local record is
already gone from a completed purge) / `account_delete_failed`, `503`
`cpanel_unavailable`.

**This call is idempotent.** Repeating it on an account that is already pending
deletion short-circuits and answers with the same `202` body — including the original
`delete_scheduled_at`, which is *not* re-stamped or extended. A retry after a timeout
is safe and will not shorten or lengthen the retention window.

To release the account sooner, see **Purge** below — that is the only path to
immediate destruction, and it requires the account to already be pending deletion, so
one mistaken call can never destroy a live account.

---

### cPanel Accounts / Password

`PATCH /api/cpanel_accounts/:cpanel_account_username/password` — set the account's
own control-panel password. **OAuth-blocked**; needs `billing`. Returns **`200`**.

Note the nested path segment is `:cpanel_account_username`, not `:username`.

```json
{ "password": "<new-password>" }
```

There is no `password_confirmation` — that is a form affordance, not an API contract.
The hosting server enforces its own strength policy.

**Synchronous** — the old password stops working at once. Whether cPanel also tears
down sessions already open under the old password is cPanel's behavior and is **not
guaranteed here**: if you are rotating because a session leaked, do not assume this
call closed it.

```json
{ "status": "changed", "username": "acme123" }
```

**Codes:** `400` `missing_account`, `401` `user_required`, `403` `cpanel_not_enabled` /
`trial_account` / `not_authorized` / `pending_deletion`, `404` `account_not_found`,
`422` `password_blank` / `password_change_failed` (rejected by the server, typically
strength policy), `503` `cpanel_unavailable`.

`pending_deletion` is permanent until a human restores the account — an unattended
rotation job should alert on it, not retry.

---

### cPanel Accounts / Purge

`POST /api/cpanel_accounts/:cpanel_account_username/purge` — **permanent and
irreversible.** Releases the account and its data now rather than at
`delete_scheduled_at`. **OAuth-blocked**; needs the site-lifecycle role. Returns
**`202`**.

The account **must already be pending deletion** — cancel it first with
`DELETE /api/cpanel_accounts/:username`. There is no combined path.

Asynchronous: the removal runs in the background, but the account disappears from
`GET /api/cpanel_accounts` immediately, so its absence from that list is the poll
signal.

```json
{ "status": "purging", "username": "acme123" }
```

**Codes:** `400` `missing_account`, `401` `user_required`, `403` `cpanel_not_enabled` /
`trial_account` / `not_authorized`, `404` `account_not_found`, `422`
`account_not_pending_deletion`, `503` `cpanel_unavailable`.

---

### cPanel Accounts / Session

`POST /api/cpanel_accounts/:cpanel_account_username/session` — mint a one-time login
URL for the account's cPanel interface. **OAuth-blocked**; needs `can_edit`. Returns
**`200`**.

```json
{ "url": "https://cpanel.example.net/..." }
```

**The full URL is generated by the hosting server, not by CloudPress** — its port,
path and query are whatever that server returns, and this API does not impose or
guarantee any particular shape for them. Treat the value as **opaque**: follow it
as-is and never parse, rebuild or pattern-match it.

The URL is single-use and short-lived — **treat it as a credential; do not log or
cache it.** Like `POST /api/sites/:id/sso` this returns the URL and never redirects.

Only the **host** of the returned URL is validated, against the server CloudPress just
contacted (exact, case-insensitive — no suffix or wildcard matching). A URL on any
other host is rejected with **`422`** `sso_url_rejected` and never returned. The port
and path are not validated, which is another reason not to depend on them.

**Codes:** `400` `missing_account`, `401` `user_required`, `403` `cpanel_not_enabled` /
`trial_account` / `not_authorized`, `404` `account_not_found`, `422`
`sso_url_rejected`, `503` `cpanel_unavailable` (server unreachable or authentication
to it failed — retryable).

Unlike the password and domain endpoints this is **deliberately allowed while the
account is pending deletion**: opening a control panel on one is how a customer
retrieves their files before the retention window closes.

---

### cPanel Accounts / Domains

**Base route:** `/api/cpanel_accounts/:cpanel_account_username/domains` — aliases
(parked), subdomains and add-on domains. The list is `cpanel:read`; create and delete
are **OAuth-blocked** and need `billing`.

#### GET .../domains — list the account's domains

Read live from the hosting server (falling back to the mirror), so a domain added
through this API is visible as soon as the server has finished building it.

```json
{
  "domains": [
    { "name": "example.com", "type": "main", "domain_type": null },
    { "name": "shop.example.com", "type": "sub", "domain_type": "subdomain" }
  ],
  "usage": {
    "addon":     { "count": 1, "limit": 3,    "unlimited": false, "at_limit": false },
    "alias":     { "count": 0, "limit": null, "unlimited": true,  "at_limit": false },
    "subdomain": { "count": 1, "limit": null, "unlimited": false, "at_limit": false }
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `domains[].name` | String | |
| `domains[].type` | String / null | The **raw** type cPanel reports (`main`, `addon`, `sub`, `parked`, `alias`, …) — server-dependent. |
| `domains[].domain_type` | String / null | The normalized vocabulary this API speaks: `parked`, `subdomain`, `addon`, or `null`. Derived server-side by mapping the raw `type`. It is `null` **both** for the main domain (which cannot be removed) **and for any raw `type` the mapping does not recognize** — the vocabulary is server-dependent, so an unfamiliar value normalizes to `null` rather than erroring. A `null` here therefore means "not removable through this API", not "this is the main domain"; use `type` to tell the two apart. |
| `usage.<kind>.count` | Integer | Per-kind counter for `addon` / `alias` / `subdomain`. |
| `usage.<kind>.limit` | Integer / null | `null` when unlimited **or unknown** — the two are not distinguished by this field. |
| `usage.<kind>.unlimited` | Boolean | `true` only when the server actually said "unlimited". |
| `usage.<kind>.at_limit` | Boolean | `true` only against a real numeric cap, so an unknown limit never reads as blocked. |

**Codes:** `400` `missing_account`, `403` `cpanel_not_enabled`, `404`
`account_not_found`, `503` `cpanel_unavailable`.

#### POST .../domains — add a domain. Returns **`202`**.

```json
{ "domain_type": "addon", "domain": "second-example.com", "dir": "public_html/second" }
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `domain_type` | String | Yes | `parked`, `subdomain`, or `addon`. |
| `domain` | String | For `parked` and `addon` | The full hostname. It must already be registered **and** owned by this workspace. |
| `label` | String | For `subdomain` | A single DNS label, no dots. |
| `rootdomain` | String | For `subdomain` | The parent, which must be one of this account's own domains. |
| `dir` | String | No | Document root (subdomain/addon). |

An alias's share target is **not** a parameter — it is always resolved server-side to
the account's primary domain.

```json
{ "status": "accepted", "domain": "second-example.com", "domain_type": "addon" }
```

**`202`, not `201`, and it matters:** the server returns success from the create
before the vhost/zone rebuild finishes, so the domain can be missing from
`GET .../domains` for a short while afterwards. Poll that list for the domain rather
than treating this response as proof it is live.

**Codes:** `400` `missing_account`; `401` `user_required`; `403` `cpanel_not_enabled` /
`trial_account` / `not_authorized` / `pending_deletion`; `404` `account_not_found`;
`422` `invalid_domain_type` / `domain_blank` / `invalid_hostname` / `label_blank` /
`invalid_label` / `rootdomain_blank` / `invalid_parent_domain` / `domain_not_eligible` /
`addon_domain_limit_reached` / `alias_domain_limit_reached` / `domain_create_failed`;
`503` `cpanel_unavailable`.

`domain_not_eligible` is deliberately generic — distinguishing the reasons would let a
client probe how any domain is known on the platform.

#### DELETE .../domains/:id — remove a domain. Returns **`200`**.

`:id` is the domain **name** (dots and all). The domain must be one of *this*
account's own domains; anything else answers `404` `domain_not_found`, the same
generic answer an unknown name gets, so this cannot be used to probe what lives
elsewhere on the platform.

The kind of removal is derived server-side from the domain's own listed row — there is
**no `domain_type` parameter** and a supplied one is ignored. The main domain cannot
be removed (`invalid_domain_type`); cancel the account instead.

Optional param `rootdomain` is a hint for a subdomain's parent, honored only when it
is genuinely one of this account's own parents; otherwise the server-side derivation
wins.

Removing a **subdomain** also strips its records from the parent DNS zone; alias and
add-on removals deliberately leave the zone in place for reuse.

```json
{ "status": "removed", "domain": "second-example.com", "domain_type": "addon" }
```

**Codes:** `400` `missing_account`; `401` `user_required`; `403` `cpanel_not_enabled` /
`trial_account` / `not_authorized` / `pending_deletion`; `404` `account_not_found` /
`domain_not_found`; `422` `invalid_domain_type` / `domain_remove_failed`; `503`
`cpanel_unavailable`.

---

### Billing webhooks

cPanel account lifecycle emits its own outbound billing webhook — a third payload
block alongside `site` and `domain`. See
[Billing Webhooks → cPanel account events](webhooks.md#cpanel-account-events).
