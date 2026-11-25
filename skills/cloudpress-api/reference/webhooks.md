# Billing Webhooks

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

Outbound webhooks that CloudPress **sends to your billing system** when a **site's subscription**, a **domain registration**, or a **cPanel hosting account** lifecycle changes. They exist so an external biller (a plan with `payment_method: none` that invoices customers outside Stripe) can mirror provisioning, resizing, ownership moves, teardown, and domain registry events into its own books.

All three resource types share the same plan endpoint, envelope, and delivery behavior; they differ only in the payload block — `site`, `domain`, or `cpanel_account_link`.

> **Direction matters.** These are *outbound* (CloudPress → your endpoint). They are unrelated to the *inbound* Stripe webhooks (`invoice.paid`, `payment_intent.succeeded`, …) that CloudPress receives from Stripe, and to the *inbound* registrar (RTR) webhooks CloudPress receives from the domain registrar. Don't conflate the three.

### Configuration

Billing webhooks are configured **per billing plan** by an account/reseller admin in the CloudPress admin UI — **there is no public API endpoint to manage billing plans or their webhook settings**. Three fields on the plan control delivery:

| Field | Type | Notes |
|-------|------|-------|
| `webhook_enabled` | Boolean | Master on/off switch (default `false`). |
| `webhook_url` | String | The HTTPS endpoint that receives the POST. |
| `webhook_auth` | String | Sent **verbatim** as the `Authorization` request header value. Supply the full header value you want — e.g. `Bearer <secret>`, `Token <secret>`, or a raw token. Optional; omitted header if blank. |

Webhooks fire only when **both** `webhook_enabled` is true **and** `webhook_url` is present. Otherwise the event is silently dropped (no retry, no error).

### Events

The event name is delivered in the `action` field; the resource block (`site`, `domain`, or `cpanel_account_link`) identifies the kind. The same `action` string is reused across kinds — **all four** site actions (`created`, `resized`, `owner_change` and `deleted`) are also cPanel-account actions, so the two catalogs collide completely — so **route on the resource block, never on `action` alone**.

**Site-subscription events** (payload block `site`):

| `action` | When it fires |
|----------|---------------|
| `created` | A newly ordered site finished provisioning and its subscription became active. |
| `resized` | A site's plan/resources changed (resize / plan-change completed). |
| `owner_change` | A site was transferred to a different owning account. |
| `deleted` | A site was deleted. |

**Domain-registration events** (payload block `domain`). Billable events carry a populated `price`; lifecycle-only events send `price: null`:

| `action` | Billable | When it fires |
|----------|----------|---------------|
| `registered` | ✅ create | A new registration completed. |
| `transferred_in` | ✅ transfer | An inbound transfer completed. |
| `renewed` | ✅ renew | Registry expiry advanced — auto-renew, manual renew, or an **at-risk** recovery renew. **Not** the redemption restore path, which emits `restored` instead (see below). |
| `restored` | ✅ combined | Redemption recovery completed — `price` is the combined restore + renewal amount (single recovery invoice). |
| `registrant_change` | ✅ registrant_change | A registrant/owner-contact change completed. |
| `privacy_enabled` | ✅ privacy | WHOIS privacy turned on (may be `$0`/`null` on some TLDs). |
| `local_contact_added` | ✅ local_contact | A required local/registry contact was added. |
| `transferred_out` | — | Domain transferred away to another registrar. |
| `expired` | — | Domain passed expiry on the exact `OK` → `EXPIRED` transition — **and only when redemption is not being entered in the same sync** (see below). |
| `redemption` | — | Domain entered the redemption/recovery phase. |
| `purged` | — | A lapsed domain was purged at the registry. |
| `privacy_disabled` | — | WHOIS privacy turned off. |
| `local_contact_removed` | — | A local/registry contact was removed. |
| `auto_renew_enabled` | — | Auto-renew turned on (incl. an external/registry-portal change synced back, or re-enabled on recovery). |
| `auto_renew_disabled` | — | Auto-renew turned off (incl. an automatic dunning lock on non-payment). |

**Two suppression rules decide which of a pair of near-synonymous events you get.** Both exist so one real-world change produces one event, and both mean the "obvious" event is the one that does *not* arrive:

- **Redemption recovery emits `restored`, not `renewed`.** The restore-then-renew path deliberately suppresses the renew hook, so the expiry advance it performs fires nothing; the single `restored` event covers it (and its `price` is the combined restore + renewal amount). Only the **at-risk** recovery renew — where the domain never entered redemption — leaves the hook armed and fires `renewed`. A biller that reconciles renewals on `renewed` alone will miss every redemption recovery.
- **Entering redemption emits `redemption`, not `expired`.** A single registry sync that moves a domain straight from `OK` to `[EXPIRED, PENDING_DELETE]` emits **`redemption` only** — the `expired` hook is gated off whenever redemption is being entered in that same sync, so one transition yields one event rather than two. Do not treat `expired` as a prerequisite for `redemption`; a domain can reach redemption having never fired `expired`.

Status/expiry domain events (`registered`, `transferred_in`, `renewed`, `expired`) are claimed single-winner — the registration records the last lifecycle event it emitted and a given logical event can only be claimed once — so concurrent registry syncs emit each of them exactly once. `auto_renew_enabled`/`auto_renew_disabled` are at-least-once (a rare duplicate is accepted) and also send the workspace's billing owner an email. All domain hooks are fully rescued — a webhook failure never rolls back or aborts the domain operation.

### cPanel account events

Payload block `cpanel_account_link`. Four events, none of which carries a `price`
block — the amount lives on the subscription:

| `action` | When it fires |
|----------|---------------|
| `created` | A newly ordered cPanel account finished provisioning. |
| `resized` | The account's package changed (the resize was applied on the hosting server). Fires once per applied change; a re-entry that changed nothing does not emit. |
| `owner_change` | The account was transferred to a different owning account. |
| `deleted` | The account was cancelled. |

Like the domain hooks, cPanel hooks are fully contained: a webhook failure never
rolls back or aborts the operation it reports on, so a missed delivery is possible
where the underlying change succeeded. Reconcile from
[`GET /api/cpanel_accounts`](endpoints-cpanel.md#cpanel-accounts) rather than treating
these as the only record.

**The containment guarantee is per resource type — it does not cover site events.**
Domain and cPanel-account emitters wrap their work so a failure there is logged and
swallowed. The **site** emitter has no such wrapper: nothing catches a failure raised
while it queues a site event. Do not generalize the domain/cPanel guarantee to sites —
if you need certainty about a site's state, reconcile against
[`GET /api/sites`](endpoints-sites.md#sites) rather than assuming the webhook path was
harmless either way.

### Delivery semantics

- **Method/body:** HTTP `POST` with a JSON body to `webhook_url`.
- **Headers:** `Authorization: <webhook_auth>` (verbatim, omitted if blank) and `Accept: application/json`.
- **Timeout:** 30 seconds per attempt.
- **Success:** any HTTP `2xx`. Anything else (or a connection failure/timeout) is treated as a failed delivery.
- **Retries:** failed deliveries are retried with backoff. The wait before the next attempt is chosen from the **age of the event** (measured from when it was emitted), not from how many attempts have already failed: under 2 minutes old → wait **5 min**; under 5 minutes old → wait **10 min**; otherwise → wait **15 min**. In practice the first failure is always the youngest case, so **the observed sequence is one retry after ≈5 minutes, then every 15 minutes** — the 10-minute branch is reachable only if the first attempt itself lands late. Make your receiver idempotent (an event may be delivered more than once).
- **Giving up:** retries stop once the event is **4 hours old**, measured from the **emit timestamp** — not from the first delivery attempt. An event that was slow to reach its first attempt gets correspondingly less retry time, so the total number of attempts is not fixed.
- **Asynchronous:** delivery happens out of band on a background queue. It is **not** part of the originating API call's response; the API returns/queues its task or cart as usual and the webhook arrives separately once the work completes.

### Payload

The POST body is a JSON object with two top-level keys: `action` (the event name) and a resource block — `site` for site events, `domain` for domain events, `cpanel_account_link` for cPanel-account events. Route on which key is present; the `domain` and `cpanel_account_link` blocks additionally carry an `object` field (`"domain_registration"` / `"cpanel_account_link"`).

**Site payload** — `site` is the full site representation (same shape as `GET /api/sites/:id`):

```json
{
  "action": "created",
  "site": {
    "id": "83426e2f-58f4-4e7e-99bc-b76b07a31574",
    "name": "adminsacc-dbe11dadb7eb9f9e",
    "primary_domain": "youthful-buck49235.example.com",
    "created_at": "2024-09-25T22:29:21.612Z",
    "updated_at": "2024-09-25T22:33:13.589Z",
    "location": "pdx",
    "region": "pdx01",
    "bunny_id": "1234567",
    "bunny_cname": "youthful-buck49235.b-cdn.net",
    "package": "Pro",
    "php_version": "8.3",
    "domain_cname": "youthful-buck49235.b-cdn.net",
    "sftp_base_path": "/home/sftpuser/apps/adminsacc-dbe11dadb7eb9f9e/wordpress",
    "dunning_suspended": false,
    "account": {
      "id": "16512906-c2b0-4c98-ac20-b1389838aa06",
      "name": "acme2"
    },
    "subscription": {
      "id": "6d8bf084-ed11-4378-8531-ef584da08439",
      "status": "active",
      "created_at": "2024-09-25T22:33:13.581Z",
      "updated_at": "2024-09-25T22:33:14.333Z",
      "price": {
        "amount_cents": 5000,
        "term": "monthly"
      },
      "product": {
        "id": "pro",
        "name": "Pro"
      }
    }
  }
}
```

**`site` fields:**

| Field | Type | Notes |
|-------|------|-------|
| `id` | String (UUID) | Site GUID. |
| `name` | String | Internal site name. |
| `primary_domain` | String | Current primary domain. |
| `created_at` / `updated_at` | String (ISO 8601) | Timestamps. |
| `location` | String | Location short name (e.g. `pdx`). |
| `region` | String | Region short name (e.g. `pdx01`). |
| `bunny_id` | String | Bunny pull-zone ID. |
| `bunny_cname` | String | Bunny CDN CNAME. |
| `package` | String | Product **display** name (e.g. `Pro`), not the short name. The short name (`pro`) is what order and resize requests take — never round-trip this value back into a request. |
| `php_version` | String | Active PHP version. |
| `domain_cname` | String | CDN CNAME target (same as `bunny_cname`). |
| `sftp_base_path` | String / null | SFTP base path, of the form `/home/sftpuser/apps/<container-service-name>/wordpress`. **`null`** when the site's container service cannot be resolved (e.g. a site not yet or no longer provisioned) — don't assume a string. |
| `dunning_suspended` | Boolean | `true` if the site is locked behind an unpaid invoice (subscription `status` can still read `active` while suspended). |
| `account` | Object | `{ id, name }` — the **owning** account, unless overridden below. |
| `subscription` | Object | `{ id, status, created_at, updated_at, price: { amount_cents, term }, product: { id, name } }`. Note the site `price` has **no** `currency` field (the domain `price` does). |

**Domain payload** — `domain` is the registration representation with a `price` block appended:

```json
{
  "action": "registered",
  "domain": {
    "id": "b2c3d4e5-6789-4abc-9def-0123456789ab",
    "object": "domain_registration",
    "name": "example.com",
    "status": "OK",
    "expires_at": "2026-09-25T00:00:00.000Z",
    "auto_renew": true,
    "privacy_protect": false,
    "tld": "com",
    "recovery_phase": null,
    "account": { "id": "16512906-c2b0-4c98-ac20-b1389838aa06", "name": "acme2" },
    "price": { "amount_cents": 1200, "currency": "usd", "term": "yearly" }
  }
}
```

**`domain` fields:**

| Field | Type | Notes |
|-------|------|-------|
| `id` | String (UUID) | Domain registration GUID. |
| `object` | String | Always `domain_registration` (use to distinguish from a `site` payload). |
| `name` | String | The domain name. |
| `status` | String | Registry status (e.g. `OK`, `EXPIRED`, `PENDING_TRANSFER`). |
| `expires_at` | String (ISO 8601) | Current registry expiry. |
| `auto_renew` | Boolean | Whether auto-renew is enabled. |
| `privacy_protect` | Boolean | Whether WHOIS privacy is active. |
| `tld` | String | The TLD (e.g. `com`). |
| `recovery_phase` | String / null | Redemption/recovery phase, or `null` when not in recovery. |
| `account` | Object | `{ id, name }` — the **owning** account, unless overridden below. |
| `price` | Object / null | `{ amount_cents, currency, term }` for billable events, else `null`. `currency` is the plan currency (ISO, lowercase); for `restored`, `term` is the renewal term. |

**cPanel-account payload** — `cpanel_account_link` is a deliberate **subset** of the
site field set: it carries the account's identity, its domain, its owner and its
subscription, and none of the site payload's CDN/infrastructure fields.

```json
{
  "action": "created",
  "cpanel_account_link": {
    "object": "cpanel_account_link",
    "id": "12",
    "guid": "acme123",
    "cpanel_username": "acme123",
    "primary_domain": "example.com",
    "account": { "id": "16512906-c2b0-4c98-ac20-b1389838aa06", "name": "acme2" },
    "subscription": {
      "id": "6d8bf084-ed11-4378-8531-ef584da08439",
      "status": "active",
      "price":   { "amount_cents": 5000, "term": "monthly" },
      "product": { "id": "cpanel_basic", "name": "Basic" }
    }
  }
}
```

**`cpanel_account_link` fields:**

| Field | Type | Notes |
|-------|------|-------|
| `object` | String | Always `cpanel_account_link` (use to distinguish from a `site` or `domain` payload). |
| `id` | String | An opaque internal handle, **not** a route key and not a GUID. Unlike the site payload — where `id` *is* the GUID — this block carries both `id` and `guid`; key your records on `guid` or `cpanel_username`. |
| `guid` | String | Equals the cPanel username. |
| `cpanel_username` | String | The `:username` segment on every `/api/cpanel_accounts` route. |
| `primary_domain` | String / null | The account's main domain. |
| `account` | Object | `{ id, name }` — the **owning** account, unless overridden by the sub-account rule below. |
| `subscription` | Object | **Omitted entirely** when the account has no subscription (a migrated account never billed through CloudPress) — absent, not `null`. When present: `{ id, status, price: { amount_cents, term }, product: { id, name } }`. Like the site `price`, it has **no** `currency` field. |

There is no `price` block on this payload — a cPanel event never carries a
per-event amount.

**Sub-account billing.** When the owning account is a **sub-account** of a different billing account, the payload identifies both: `account` is set to the **billing (parent) account** and an extra `sub_account` block (inside the resource block) names the actual owner. Applies to all three payload types.

```json
{
  "action": "resized",
  "site": {
    "id": "…",
    "account":     { "id": "<billing-account-guid>", "name": "Parent Co" },
    "sub_account": { "id": "<owner-account-guid>",   "name": "Child Team" },
    "subscription": { "…": "…" }
  }
}
```

### What does NOT trigger a billing webhook

Billing webhooks cover **site-subscription, domain-registration and cPanel-account lifecycle** events. The following do **not** emit a billing webhook — even when paid:

- **Backups, restores, cache, Shield, and other per-site task operations.** Track these via task polling or a per-request completion callback.
- **Order/invoice mechanics** (charges, refunds, payment status). Billing webhooks describe *service lifecycle*, not invoice state; for order-level detail use [Orders](endpoints-orders.md#orders) and the registrar [processes](endpoints-domains.md#domain-registration-processes).

### Billing webhooks vs. completion callbacks

These are two distinct mechanisms — don't confuse them:

| | Billing webhook | Completion callback |
|---|---|---|
| Configured on | The **billing plan** (admin UI) | **Per request**, in the `callback` object on `POST /api/orders`, `POST /api/orders/domain` or `POST /api/cpanel_accounts` (or seeded into a task) |
| Scope | All site, domain and cPanel-account lifecycle events under that plan | The single task/order it was attached to |
| Fires for | Site events (`created`, `resized`, …), domain events (`registered`, `renewed`, …) and cPanel-account events (`created`, `resized`, …) | Completion of that specific async task |
| Body | `{ "action", "site" }`, `{ "action", "domain" }` or `{ "action", "cpanel_account_link" }` | `{ "timestamp", "success", "data" }` (the task's result) |

See [Async Patterns → Completion callback](../SKILL.md#async-patterns) for the per-request callback contract.
