# Orders, Carts & Mailspace

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### Orders

**Base route:** `/api/orders` — **requires `X-Auth-Account`**. Index/show scope `billing:read`; **create/update/destroy are OAuth-blocked** (session/API-key only). Ordering now flows through the cart/billing system and charges the account's **default saved payment method off-session** — there is no Stripe checkout redirect.

#### GET /api/orders — list account orders
```json
{ "orders": [ { "id": "<uuid>", "status": "completed", "created_at": "...", "updated_at": "...", "location": "pdx", "account": { "id": "<guid>", "name": "Acme" } } ] }
```
`location` is the order's location `short_name`, or **`null`** for orders with no location (e.g. domain-registration orders) — both index and show now render `location: null` rather than erroring.

#### GET /api/orders/:id — view order
```json
{
  "order": { "id": "<uuid>", "status": "completed", "created_at": "...", "updated_at": "...", "location": "pdx" },
  "tasks": [ { "id": 123, "status": "OK" } ],
  "site": { "id": "<guid>", "name": "my-site", "domain": "my-site.example.com", "variant": "vanilla", "location": "pdx",
    "ssh_data": { "ipaddr": "192.0.2.10", "username": "user", "password": "...", "port": "22" } },
  "subscription": { "id": "<guid>", "status": "active", "bucket_type": "...", "bucket_year": 2026, "bucket_month": 6, "stripe_id": "..." },
  "domain": { "name": "example.com", "action": "register", "registration": null, "provisioning_status": "processing" },
  "payment": { "status": "succeeded", "method_type": "card", "hosted_invoice_url": "...", "amount_charged_cents": 1000, "credit_applied_cents": 0 },
  "account": { "id": "<guid>", "name": "Acme", "...": "full account object" },
  "user": { "id": "<guid>", "email": "jane@example.com", "...": "full user object" }
}
```

- `site` appears only when the order provisioned a site, and `subscription` only when
  the order has a backing subscription. Inside `site`, `ssh_data` is **`null`** when the
  site has no SFTP credentials — the key is always emitted, so branch on `null`, not on
  the key's absence.
- **`domain`** appears only on domain orders (`POST /api/orders/domain`) and is the block
  a domain-order integrator polls: `{ name, action, registration, provisioning_status }`.
  During the async window — before the registrar call succeeds — `registration` is
  **`null`** and `provisioning_status` carries the order's own status. Once the
  registration exists, `registration` is the full domain-registration object (the same
  shape `GET /api/domain_registrations/:id` returns) and `provisioning_status` is not
  emitted at all.
- `account` and `user` are the **full** objects here, not the short `{id, name}` /
  `{id, email}` pairs. `account` carries `id`, `name`, `reseller`, `is_trial`,
  `trial_start`, `trial_end`, `nameservers`, `created_at`, `updated_at`,
  `parent_account` and `reseller_billing_plan`; `user` carries `id`, `fname`, `lname`,
  `email`, `account_brand_id`, `locale`, `created_at`, `updated_at`. See
  [`endpoints-accounts.md`](endpoints-accounts.md). (The orders **index** above really
  does use the short `{id, name}` account shape — the two differ.)
- `amount_charged_cents` and `credit_applied_cents` are read from the order's invoice
  record and are **`null`** — not `0` — until that record exists, i.e. throughout the
  async window, and permanently for an order that never produced one.

**`payment.status` on this endpoint is its own five-value enum**, wider than the cart
envelope's three (below):

| `payment.status` | When |
|---|---|
| `pending` | the order has not reached a payment state yet |
| `processing` | the payment is in flight (e.g. SEPA / other bank debit) |
| `succeeded` | the order completed |
| `awaiting_authentication` | parked on a 3DS/SCA challenge — send the user to `hosted_invoice_url` |
| `failed` | order `failed` or `cancelled`, or parked awaiting a *new* payment method after a decline |

#### POST /api/orders — create a site
```json
{
  "site": { "name": "my-wordpress-site", "variant": "vanilla", "location": "pdx", "plan": "basic", "term": "monthly" },
  "callback": { "url": "https://your-app.com/webhook", "authorization": "Bearer your-secret" }
}
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `site.name` | String | Yes | |
| `site.variant` | String | Yes | `vanilla` or `extendify` |
| `site.location` | String | Yes | Location `short_name` (e.g. `pdx`) — the `id` field from `/api/about` |
| `site.plan` | String | Yes | Product `short_name` (e.g. `basic`) — the `id` field from `/api/about` |
| `site.term` | String | Yes | `monthly` or `annual` |
| `callback.url` | String | No | Webhook for async completion |
| `callback.authorization` | String | No | `Authorization` value sent to the callback |

> `site.return_url` is still accepted but unused (no Stripe redirect flow).

**Response — always `202 Accepted` (cart envelope):**
```json
{
  "status": "accepted",
  "cart":    { "token": "<cart_token>", "status": "...", "rollup_status": "...",
               "poll_url": "https://my.cloudpress.com/api/carts/<cart_token>" },
  "payment": { "status": "processing", "method_type": "card", "hosted_invoice_url": null },
  "orders":  [ { "id": "<uuid>", "status": "pending",
                 "poll_url": "https://my.cloudpress.com/api/orders/<id>" } ]
}
```

> **`poll_url` is an absolute URL, not a path** — on `cart` and on every entry of
> `orders` alike. Request it as-is; do not join it onto a base URL. (This is the
> canonical statement for the cart envelope wherever it appears — mailspace create and
> resize return the same envelope.)

Poll `cart.poll_url` (or each order's `poll_url`) until orders materialize. Payment is
charged off-session.

**The envelope's `payment.status` carries only three values**, and `failed` is not one
of them:

| `payment.status` | Meaning |
|---|---|
| `processing` | the charge is in flight — the ordinary async case |
| `awaiting_authentication` | parked for admin recovery: a 3DS/SCA challenge **or** a recoverable decline. `payment.hosted_invoice_url` is populated; send the user there. **Purchases only** — see below. |
| `succeeded` | the cart finalized synchronously |

A client that polls `cart.poll_url` waiting for `payment.status: "failed"` waits
forever — `failed` appears only on `GET /api/orders/:id`, whose enum is the wider
five-value one above. On a non-Stripe (externally billed) plan the envelope stays at
`processing` even after provisioning completes; the terminal signal there is
`orders[].status`.

> **`awaiting_authentication` never appears on a resize.** The signal is stamped only on
> the fresh-charge path a *purchase* takes; a resize is billed as a proration against the
> existing subscription, and a proration cart is excluded from that path. So a declined
> or challenged **resize** is still a `202`, but its envelope reports
> **`payment.status: "processing"`** with `payment.hosted_invoice_url` **populated**.
>
> | Operation | Declined/3DS shows as |
> |---|---|
> | `POST /api/orders`, cPanel order, Mailspace purchase, registrant change | `awaiting_authentication` |
> | `PATCH /api/sites/:id` (`plan`), cPanel resize, Mailspace resize | `processing` + non-null `hosted_invoice_url` |
>
> **On any resize, branch on a non-null `hosted_invoice_url`, not on `payment.status`.**

**Pre-flight / validation errors — all `400`, each with a `code`:**

| Code | Meaning |
|---|---|
| `account_cannot_order` | the account may not place orders (`"Account unable to create orders."`) |
| `unknown_variant` | `site.variant` is neither `vanilla` nor `extendify` |
| `unknown_location` | no public location has that `short_name` |
| `unknown_term` | `site.term` is neither `monthly` nor `annual` |
| `unknown_product` | no plan with that `short_name` is available to the account |
| `over_capacity` | that variant has no inventory at that location — retry later |
| `no_price_for_plan` | the plan has no price for the requested term |
| `no_default_payment_method` | the billing account is not chargeable off-session (needs a Stripe customer, a saved default payment method, and a complete billing contact). The body also carries a `remediation` string. |
| `item_add_failed` | validation passed but the cart refused the item |

After pre-flight passes, a payment that cannot be initiated returns **`422`**
`{...,"code":"cart_pay_failed"}`.

**Order states** — the full set is `pending`, `awaiting_payment`, `processing`,
`completed`, `failed`, `cancelled`. Typical flow: `pending` → `processing` →
`completed` / `failed`; `awaiting_payment` is the parked state for a 3DS challenge or a
decline.

#### POST /api/orders/domain — register or transfer a domain
Places a **paid** domain order (register or transfer a TLD registration) through the same cart/billing flow as site orders. Distinct from `POST /api/orders` (which creates sites). **OAuth-blocked** — requires a **user-scoped** credential (a system account-bearer key → `401 user_required`). Requires `X-Auth-Account` and the `domain-registration` feature flag (off → `503 feature_disabled`); trial accounts → `403 trial_account`.

```json
{
  "domain": {
    "name": "example.com",
    "action": "register",
    "authcode": "<epp-code>",
    "contact": { "first_name": "Jane", "last_name": "Doe", "country": "US", "email": "jane@example.com", "phone": "+1.2125551234", "organization": "...", "street_address": "...", "post_code": "...", "city": "...", "state": "...", "extra_properties": {} },
    "contact_source": { "registration_id": 4217 },
    "role_contacts": { "admin": { "source": "same_as_owner" }, "billing": { "source": "existing", "source_registration_id": 4217 }, "tech": { "source": "new", "first_name": "...", "...": "..." } }
  },
  "callback": { "url": "https://your-app.com/webhook", "authorization": "Bearer your-secret" }
}
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `domain.name` | String | Yes | FQDN; normalized & validated. |
| `domain.action` | String | No | `register` (default) or `transfer`. |
| `domain.authcode` | String | Cond. | Required for `transfer` when the TLD demands it. |
| `domain.contact` | Object | Cond. | Inline registrant — required unless `contact_source` is given. ISO-2 `country`, E.164 `phone`. |
| `domain.contact_source` | Object | Cond. | `{ "registration_id": <integer> }` — reuse an owned registration's contacts instead of `contact`. **Integer, not the GUID — read the warning below.** |
| `domain.role_contacts` | Object | No | `admin`/`billing`/`tech`; each `{ source: "same_as_owner"\|"existing"\|"new", source_registration_id?, ...contact fields }`. `source_registration_id` is the same integer identifier as `contact_source.registration_id`. |
| `callback` | Object | No | Same webhook shape as site orders. |

**Response — always `202 Accepted`**, identical cart envelope to `POST /api/orders` (poll `cart.poll_url` / order `poll_url`).

> **`contact_source.registration_id` is the domain registration's integer primary key —
> *not* the `id` the API hands you.** The lookup runs against the account's domain
> registrations by their integer `id`, while `GET /api/domain_registrations` and
> `GET /api/domain_registrations/:id` both key on, and return as `id`, a **separate
> `guid` column**. So the identifier a caller reads back from the domain-registration
> API is exactly the value that will *not* work here: passing it gets you `400`
> `invalid_contact_source`, which reads like "you don't own that registration" rather
> than "wrong identifier". The same applies to `role_contacts.*.source_registration_id`.
> The API exposes no lookup that returns the integer key, so this parameter is usable
> only when you already hold it out of band.

**Errors:** `400` `invalid_action` / `invalid_domain` / `unsupported_tld` / `pricing_unavailable` / `authcode_required` / `incomplete_contact` / `invalid_contact` / `invalid_contact_source` / `no_default_payment_method` / `account_cannot_order` (`"Account unable to create orders."`); `422` `domain_unavailable` (register only) / `domain_availability_unknown` (register only) / `domain_add_failed` / `domain_contact_invalid` / `domain_contact_needs_augmentation` / `cart_pay_failed`; `503` `feature_disabled`; `403` `trial_account`; `401` `user_required`.

The two contact rejections carry extra keys alongside `errors` and `code`:

| Code | Status | Extra key |
|---|---|---|
| `domain_contact_invalid` | `422` | `violations` — what the registry rejected about the registrant contact |
| `domain_contact_needs_augmentation` | `422` | `needs_augmentation` — the additional fields this TLD requires; resubmit with them filled in |

Both are raised after the inline contact is validated, and any contacts created during
the attempt are torn down, so a retry starts clean.

> **`domain_unavailable` vs `domain_availability_unknown`** — both are `422` on a
> register, and the difference is a claim about the name versus no claim at all.
> `domain_unavailable` means the registry said the name is not registerable.
> `domain_availability_unknown` means the availability check itself failed, so
> CloudPress cannot say either way — **retry it**, and do not tell the customer the
> name is taken or offer alternatives.

#### PATCH /api/orders/:id — no-op stub, returns `400`.
#### DELETE /api/orders/:id — cancel order. Returns **`202`**.

---

### Carts

**Route:** `GET /api/carts/:token` — **requires `X-Auth-Account`**; scope `billing:read`. Poll cart state during the async window after `POST /api/orders` or a site plan change. Response mirrors the order-create envelope (`status`, `cart`, `payment`, `orders`) — including the three-value `payment.status` and the absolute `poll_url`s described there. Scoped to your own account; unknown token → `404`.

---

### Mailspace

**Base route:** `/api/mailspace` — mail hosting for a domain. Scopes
`mailspace:read` (list/show) / `mailspace:write` (create/resize/delete). Create and
resize flow through the same cart + off-session charge as orders and return the same
`202` envelope; delete is synchronous.

Requires the mail platform to be configured — otherwise every write returns **`503`**
`{"errors":["The mail server is not configured."],"code":"stalwart_unavailable"}`.

**Account scoping.** Only `POST` requires an account context: without
`X-Auth-Account` (or an account-scoped credential) it returns **`400`**
`{"errors":[...],"code":"account_required"}`. List/show/resize/delete fall back to the
mailspaces the token's user can reach across their workspaces. **Create, resize and
delete** require **edit access** on the account being billed — for a create that is the
account you sent in `X-Auth-Account`, otherwise it is the mailspace's own account. Fail
it and you get **`403`** `{"errors":["Not Authorized"]}` — note this one carries no
`code`. List and show are not role-gated beyond that scoping.
An unknown id is an empty **`404`**.

**Holds.** Resize and delete are refused while the mailspace is on a staff or dunning
hold: **`403`** `{"errors":["This mailspace is on hold and cannot be modified. Please contact support."],"code":"mailspace_suspended"}`.
A hold is not a permission failure — edit access does not override it.

#### GET /api/mailspace — list

```json
{ "mailspaces": [ { "id": "<guid>", "domain": "example.com", "account_name": "Acme",
  "package": "mail_5", "package_name": "Mailspace 5GB", "status": "active",
  "storage_gb": 5, "max_mailboxes": 20, "used_mb": 1024, "mailbox_count": 2,
  "provisioned": true, "verified": true, "needs_domain_verification": false,
  "pending_deletion": false, "delete_scheduled_at": null,
  "created_at": "...", "updated_at": "...",
  "account": { "id": "<guid>", "name": "Acme" } } ] }
```

Active **and** pending-deletion mailspaces are listed; purged ones are gone.

**Package keys.** The seeded mail catalog is `mail_5`, `mail_20`, `mail_50`, `mail_200`
and `mail_500` — the five tiers, sized 5/20/50/200/500 GB with 20/50/100/100/100
mailboxes. Any other value on create or resize is rejected with `400 unknown_product`.
Mail is sold **annual-only**, one flat price per tier.

| Field | Type | Notes |
|-------|------|-------|
| `id` | String (GUID) | The `:id` segment on the other routes. |
| `domain` | String | The mailspace's primary mail domain. |
| `package` / `package_name` | String | Plan key and its display name. |
| `status` | String | Provisioning/lifecycle status: `pending`, `active`, `suspended` or `inactive`. |
| `storage_gb` / `max_mailboxes` | Integer | The plan's included limits. |
| `used_mb` / `mailbox_count` | Integer | Current usage. `used_mb` is a cached figure, refreshed when a resize is evaluated. |
| `provisioned` | Boolean | `false` until the mail tenant exists. |
| `verified` | Boolean | Domain ownership proven. |
| `needs_domain_verification` | Boolean | `true` while a DNS TXT record is still outstanding — the record itself is in the **show** payload's `verification` block. |
| `pending_deletion` | Boolean | Soft-deleted; locked to restore/purge. |
| `delete_scheduled_at` | String (ISO 8601) / null | The frozen purge date; `null` while live. |

#### GET /api/mailspace/:id — show

The list fields plus:

```json
{ "mailspace": { "...": "...", "synced_at": null, "webmail_url": "https://webmail.example.com",
  "verification": { "txt_prefix": "_mailspace-verify", "txt_host": "_mailspace-verify.example.com", "txt_value": "<token>" },
  "subscription": { "id": "<guid>", "status": "active", "created_at": "...", "updated_at": "...",
    "price": { "amount_cents": 3000, "term": "annual" } },
  "account": { "id": "<guid>", "name": "Acme" } } }
```

- `verification` is present **only** while `needs_domain_verification` is `true` — add
  a TXT record at `txt_host` with the value `txt_value` to prove ownership. `txt_prefix`
  is the label the host is built from. A domain the workspace already owns skips
  verification entirely and never gets this block.
- `webmail_url` is `https://webmail.` + the mailspace's mail domain.
- `subscription` is omitted when there is none. `price.term` is `annual` for every
  catalog tier; `amount_cents` is that tier's flat annual price.
- Served from local state — this endpoint does **not** make a live call to the mail
  platform.
- **`synced_at` is not a freshness indicator for `used_mb` / `mailbox_count`.** It is
  stamped only when the mailspace is opened in the control panel, so for a mailspace
  managed purely through the API it stays **`null`** indefinitely while `used_mb` and
  `mailbox_count` do keep updating (a resize refreshes them). The timestamp that
  actually tracks those figures is not exposed in this payload, so there is no field
  here you can use to age them.

#### POST /api/mailspace — purchase. Returns **`202`**.

```json
{ "domain": "example.com", "package": "mail_5" }
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `domain` | String | Yes | FQDN. Must be a domain that actually **exists** (registered with CloudPress or elsewhere). |
| `package` | String | No | One of the catalog keys (`mail_5` … `mail_500`). Omitted, you get the **smallest** tier — `mail_5` in the standard catalog. |

Response is the same cart envelope as [`POST /api/orders`](#orders) — poll
`cart.poll_url`. The mailspace record itself is minted only once payment settles; for
a domain the workspace does not already own it lands awaiting verification, and
`GET /api/mailspace/:id` then carries the `verification` block.

**On a purchase, a declined off-session charge is still a `202`** — the envelope reports
`payment.status: "awaiting_authentication"` with a `payment.hosted_invoice_url` to pay
through. Branch on `payment.status`, not on the HTTP status alone. (A *resize* behaves
differently — see `PATCH` below.)

**Codes:** `400` `account_required` / `invalid_domain` / `unknown_product` /
`no_default_payment_method` (body also carries a `remediation` string); `422`
`domain_not_registered` / `mailspace_exists` / `cart_item_rejected` /
`cart_pay_failed`; `503` `stalwart_unavailable`.

`mailspace_exists` also fires for a **soft-deleted** mailspace on that domain: the mail
domain stays claimed for the whole retention window, so restore the existing one
instead of buying a second.

#### PATCH /api/mailspace/:id — resize the package. Returns **`202`**.

```json
{ "package": "mail_50" }
```

`package` (required) is the only parameter, and must be one of the catalog keys
(`mail_5` … `mail_500`). Same cart envelope as `POST` — but **not** the same
declined-charge behavior:

> **A declined resize does not report `awaiting_authentication`.** This is not a Mailspace
> quirk — it applies to every resize, because every resize builds a proration cart. See
> the rule and the per-operation table under [Carts](#carts). Branch on a non-null
> `payment.hosted_invoice_url`.

**Codes:** `400` `unknown_product` / `no_default_payment_method`; `403`
`mailspace_suspended`; `422` `pending_delete` / `package_unchanged` /
`not_provisioned` / `resize_unavailable` / `downgrade_blocked` / `cart_item_rejected` /
`cart_pay_failed`; `503` `stalwart_unavailable`.

| Code | Meaning |
|---|---|
| `pending_delete` | Scheduled for deletion; cannot be resized. |
| `package_unchanged` | Already on that plan. |
| `not_provisioned` | The mail tenant does not exist yet. |
| `resize_unavailable` | Stripe-billed plan with no Stripe-linked subscription to prorate against. Externally-billed plans are not gated by this. |
| `downgrade_blocked` | The target plan is smaller than current mailbox count or stored mail. Usage is refreshed before the check, so this reflects live consumption. |

#### DELETE /api/mailspace/:id — soft-delete. Returns **`200`** (empty body).

Opens the retention window. Idempotent — deleting an already-pending-deletion mailspace
succeeds without changing anything. **Restore** is a control-panel operation with no API
route. **Purge** — an immediate, permanent hard-delete that ends the retention window
early — *is* an API endpoint: see
[Mailspace Purge](endpoints-mailspace.md#mailspace-purge).

**Codes:** `403` `mailspace_suspended`; `422` `delete_failed`; `503`
`stalwart_unavailable`.
