# Domains & Domain Registration

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### Domains

**Base route:** `/api/domains` — scopes `domains:read`. (Manages WordPress site hostnames — distinct from [Domain Registration](#domain-registration).)

#### GET /api/domains
List domains. Returns `{ "domains": [ ... ] }`. **Paginated** — `page` and `per_page` (default `50`, max `100`).

#### GET /api/domains/:id
View one domain. Returns a **single object** (not an array):

```json
{
  "domain": {
    "id": "<guid>", "hostname": "example.com",
    "created_at": "...", "updated_at": "...",
    "site_id": "<guid>", "site_pending_delete": false,
    "account_id": "<guid>",
    "dns_zone": { ... }, "dns_zone_records": [ ... ]
  }
}
```

- `site_pending_delete` is emitted alongside `site_id`: `true` when the attached site is soft-deleted (pending purge), `null` when no site is attached.
- **`dns_zone` is explicitly `null`** when the domain has no zone — the key is always present, so test its value rather than its presence.

#### POST /api/domains/query
Search domains by **substring** anywhere in the hostname. Renders the same shape as `index` but is **not paginated** — every match comes back in one response.
```json
{ "q": "example" }
```

#### POST /api/domains/available
Check availability.
```json
{ "hostname": "example.com" }
```
- `200` + `{"status":"example.com is unavailable"}` — exists in the system
- `404` + `{"status":"example.com is available"}` — free
- `422` — invalid/missing hostname

---

### Domain Registration

> **Registrar feature** — registering, transferring, and managing TLD registrations (distinct from `/api/domains`, which manages site hostnames). **Gated by the `domain-registration` feature flag** — when off, every endpoint below returns **`503`** `{"errors":[...],"code":"feature_disabled"}`. Scopes `domains:read` / `domains:write`. All require an account context (`X-Auth-Account` / `400` if missing). Mutations require `can_edit` — **with one exception: `GET .../:id/epp_code`**, which carries the `domains:write` scope but is not on the can-edit list, so the permission check never runs on it. A view-only member of the account holding a `domains:write` token can retrieve the transfer authcode. Registrar operations may be async (202 + `pending_process`).

#### Domain Contacts

**Base route:** `/api/domain_contacts`. `:id` is the numeric contact ID. Contact object:
```json
{ "id": 42, "handle": "<registrar-assigned>", "first_name": "Jane", "last_name": "Doe",
  "organization": "Acme Inc", "street_address": "1 Main St", "post_code": "10001", "city": "New York",
  "state": "NY", "country": "US", "email": "jane@example.com", "phone": "+1.2125551234",
  "extra_properties": {}, "validations": [], "split_from_id": null, "created_at": "...", "updated_at": "..." }
```
`handle` is generated at create time and is read-only. Its shape is `<registrar customer handle>-<first name>-<last name>-<6 hex chars>` with non-alphanumerics stripped from the names, truncated to 40 characters — never a fixed prefix like `CONTACT-`, so don't parse or construct it.
- `GET /api/domain_contacts` — list (optional `q`). Scope `domains:read`.
- `GET /api/domain_contacts/:id` — view.
- `POST /api/domain_contacts` — create (registrar + local). **`201`**. Body: `tld_id` or `tld_name`, plus `domain_contact.{first_name,last_name,organization,street_address,post_code,city,state,country,email,phone,extra_properties}`. `country` is ISO-2; `phone` E.164 `+CC.NUMBER`. Unknown TLD → **`404`** `tld_not_found`.
  **Required:** `first_name`, `last_name`, `street_address`, `post_code`, `city`, `country`, `email`, `phone`. **Optional: `organization` and `state` — those two only**; everything else in that list is validated for presence and a missing one comes back as `422`. An individual TLD can require further fields (delivered through `extra_properties`) on top of these.
- `PATCH /api/domain_contacts/:id` — update; may split if some domains reject. `200` or `202` (`pending_process`). No resolvable TLD context → **`422`** `tld_not_found` — note the status differs from create, where the same code is a `404`.
- `DELETE /api/domain_contacts/:id` — only if unused; orphan contacts need `tld_id`/`tld_name` (else `422 tld_required_for_orphan`). `204`. In use → `422 contact_in_use`.
- `POST /api/domain_contacts/:id/resend_verification` — `{ "status": "queued" }`.

#### Domain Registrations

**Base route:** `/api/domain_registrations`. `:id` is the registration **guid**.

The canonical object includes `id, name, status, expires_at, auto_renew, locked, privacy_protect, dnssec_enabled, server_transfer_prohibited, local_contact_active, cancellation_deadline_at, within_cancellation_window, nameservers, tld{id,name,registrar}, owner_contact, admin_contact, tech_contact, billing_contact, pending_async, rtr_process_id, rtr_process_status, transfer_out_pending, push_transfer_pending, subscription_id, feature_flags{...}, fees{...}, created_at, updated_at`. `cancellation_deadline_at` (timestamp) and `within_cancellation_window` (Boolean) are the **only** way to predict a `422 cancellation_window_passed` before issuing a cancellation — read them from a fresh `show` rather than assuming.

**`409 registration_busy` does not cover every mutation.** While a registrar process is in flight the guard rejects exactly `PATCH :id`, `nameservers`, `lock`, `privacy`, `dnssec`, `holder`, `contacts`, `push_transfer`, `registrant_change` — **and all three `.../hosts` mutations** (`POST`, `PATCH`, `DELETE`), which is easy to miss because the hosts endpoints are documented separately below. It deliberately does **not** cover `force_sync`, `transfer_out` or `resend_contact_verification`; those stay callable mid-process. Body: `{"errors":[...],"code":"registration_busy","pending_process_id":<id>}`.

- `GET /api/domain_registrations` — list (optional `q`). Scope `domains:read`.
- `GET /api/domain_registrations/:id` — show (+ `dns_zone`, `linked_site`, `transfer_out` when applicable).
- `POST /api/domain_registrations/check` — availability for `{ "domain": "example.com" }`. Returns `domain`, `available`, `premium`, `owned_by_account`, `reason`, **`price`**, `transfer_price`.
  > **The registration price comes back as `price`, not `create_price`.** `create_price` is only the internal name; it is renamed on the way out. A client reading `create_price` gets `undefined` on every call. `transfer_price` keeps its name.

  Both price fields are `{"amount_cents": <integer>, "currency": "<ISO-4217, upper-case>"}`, or **`null`** when the caller's billing plan has no orderable price for that role. `available` is `true` only when the registrar reports the domain free **and** a registration `price` exists — a genuinely unregistered domain your plan cannot sell still reports `available: false`. Errors: `422` `missing_domain`/`invalid_domain`/`unknown_tld`; `502` `registrar_unavailable`. (To register/transfer, place an order via `POST /api/orders/domain`.)
- `POST /api/domain_registrations/suggestions` — alternates for `{ "domain": "..." }`. Errors: `422` `missing_domain`; `503` `missing_api_key`; `502` `registrar_unavailable`.
- `PATCH /api/domain_registrations/:id` — `{ "domain_registration": { "auto_renew": true } }`. Returns show + `scenario`.
- `PATCH .../:id/nameservers` — `{ "nameservers": [...] }`. Async-capable. Empty list → `422 nameservers_required`.
- `PATCH .../:id/lock` — `{ "locked": true }`. Async-capable. `422 lock_unsupported` if the TLD can't lock; `422 server_transfer_prohibited` if a server-transfer-prohibited lock is set.
- `PATCH .../:id/privacy` — `{ "privacy_protect": true }`. Async-capable. `422 privacy_unsupported` if the TLD has no WHOIS privacy. The fee gate fires **only when enabling** on a metered TLD → **`402 payment_required`** (with `price` whose `role` is `privacy`, plus `portal_url`); disabling is always free.
- `PATCH .../:id/dnssec` — `{ "mode": "enable"|"disable"|"add_keys", "key_data": [ { "flags", "algorithm", "publicKey" } ] }`. `422 invalid_mode` for an unknown mode; `422 dnssec_no_keys` when keys are required but absent.
- `PATCH .../:id/holder` — **in-place** registrant edit/change; `holder_contact.action_mode` = `edit_current`|`change`. The fee gate fires **only on `change`** on a metered TLD → `402 payment_required` (price `role` = `registrant_change`). `404 source_contact_not_found` if `source_domain_contact_id` resolves to nothing; `409 reverification_required` when validated fields change without `confirm_reverification: "1"`. For a **billable** registrant change placed as an order, use `POST .../:id/registrant_change` (below).
- `PATCH .../:id/contacts` — set the admin/tech/billing role contacts. Each role is independently optional; an omitted role is left unchanged. The holder/registrant is **not** settable here — use `/holder`. For each role you do send, `{role}_contact.source` picks the mode, and two of the three modes need a **companion top-level param**:

  | `{role}_contact.source` | Companion param | Notes |
  |---|---|---|
  | `same_as_owner` | — | Reuses the registration's owner contact. |
  | `existing` | `{role}_source_domain_contact_id` (Integer) | An existing contact of this account. Without it the mode resolves to nothing and the role is left unset. |
  | `new` | `{role}_new_contact: { ... }` | Same fields as a contact create. |

  Note the naming: the mode lives *inside* `{role}_contact`, but the companion params are siblings of it (`admin_source_domain_contact_id`, `admin_new_contact`, and likewise for `tech`/`billing`) — not nested under it. Returns `200` (or `202` with `pending_process`). Errors: **`422 owner_contact_missing`** when any role asks for `same_as_owner` on a registration that has no owner contact; `422` with `errors` on registry rejection.
- `GET .../:id/epp_code` — `{ "authcode": "..." }`. (GET, but requires `domains:write`.) **No `can_edit` check and no busy check** — unlike every other `domains:write` action here, this one is reachable by a view-only member and while a registrar process is in flight. `422 server_transfer_prohibited`; `422 authcode_unavailable` if the TLD hides authcodes; `502 authcode_unavailable` on registrar failure.
- `POST .../:id/force_sync` — re-sync from registrar; returns show + `changed[]`.
- `POST .../:id/transfer_out` — `{ "decision": "approve"|"reject" }`. `422 no_pending_transfer_out`; `422 invalid_decision`.
- `POST .../:id/registrant_change` — **billable** registrant change placed as an **order** (the paid counterpart to `PATCH .../holder` with `action_mode: change`). **OAuth-blocked**; requires a user credential with order-create permission (system key → `401 user_required`; user lacking order-create → `403 forbidden`). Body: `source_domain_contact_id` (Integer, an owned contact) **or** `new_contact` (object requiring `first_name, last_name, country, email, phone`; optional `organization, street_address, post_code, city, state, extra_properties`).

  "One or the other" is a convention, **not an enforced constraint**: sending *both* silently uses `source_domain_contact_id` and ignores `new_contact` entirely, and sending *neither* is not reported as "pick one" — it falls through to the new-contact path and returns `422 contact_invalid` listing all five required fields as missing. Send exactly one and check which branch the error came from.

  Returns **`202`** with the order/cart envelope. **Poll `cart.poll_url`, not the orders.** `cart.poll_url` is always present; `orders[]` can be **empty** at the 202 — on the Stripe payment path the order does not exist yet — so a client that only follows `orders[].poll_url` is left with nothing to poll. Errors: `403 trial_account`; `409 registration_busy`; `422` `source_contact_not_found` (note: **422** here, vs 404 on `/holder`) / `contact_invalid` (with `violations`) / `no_registrant_change_price` / `cart_pay_failed`.
- `POST .../:id/push_transfer` — `{ "recipient": "REG-IDS" }`. Async-capable.
- `POST .../:id/resend_contact_verification` — `{ "status": "queued" }`.

#### Domain Registration Hosts (glue records)

**Base route:** `/api/domain_registrations/:domain_registration_id/hosts`. Route param is `:host_name`. The three mutations here require `can_edit` and are **covered by the `409 registration_busy` guard** — a host change fails while any registrar process is in flight on the parent registration, exactly like the registration-level mutations.
- `GET .../hosts` — `{ "hosts": [ { "host_name", "addresses": [ { "address", "version" } ] } ] }`.
- `POST .../hosts` — `{ "host_name": "ns1.example.com", "addresses": [ { "address": "203.0.113.10" } ] }`. **`201`**.
- `PATCH .../hosts/:host_name` — replace addresses. `200`.
- `DELETE .../hosts/:host_name` — `204`.

#### Domain Registration Processes

**Base route:** `/api/domain_registrations/:domain_registration_id/processes` — poll these after a 202.
- `GET .../processes` — `{ "processes": [ ... ] }` (newest first).
- `GET .../processes/:id` — `{ "process": {...}, "log": [...] }`. `404` if the process doesn't belong to the registration.
- `POST .../processes/:id/resend` — resume a suspended process. `{ "status": "queued" }`.
- `DELETE .../processes/:id/cancel` — `{ "status": "cancelled" }`.
