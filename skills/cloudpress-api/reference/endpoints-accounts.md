# Accounts, Users & API Keys

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### GET /api/about

Returns the deployment's release version, the calling identity, the public locations, the product catalog, and the available PHP versions. Accepts **any** valid token (no scope required).

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" https://my.cloudpress.com/api/about
```

```json
{
  "version": "2026.08.01",
  "logged_in_as": "<user_guid>",
  "account_scoped": "<account_guid or null>",
  "locations": [ { "id": "pdx", "name": "Portland, OR" } ],
  "products": [ { "id": "basic", "name": "Basic", "description": "..." } ],
  "php": [ { "id": 1, "label": "<php variant label>", "is_default": true } ]
}
```

- `version` is the **deployment's release version** (`YYYY.MM.DD`), not an API version — it changes with every release, so don't branch on it.
- `locations` lists only locations that have a **public** region, so it is a subset of the locations that exist. `id` is the location's short name, `name` its display name.
- `products` is the **entire** product catalog, unfiltered. `id` is the product's **short name**, `name` its display name. Seeded short names are `lite`, `basic`, `pro`, `max` (WordPress), `cpanel_mini`, `cpanel_basic`, `cpanel_pro`, `cpanel_max` (cPanel) and `mail_5`, `mail_20`, `mail_50`, `mail_200`, `mail_500` (Mailspace); a deployment may define others.
- `php` comes from the platform's WordPress image catalog — `id` is that catalog's integer id and `label` its display label, so both are deployment data rather than fixed strings. `[]` when no versions are available.

The `pdx` / `basic` values above are this deployment's seeded catalog; read the real values from this endpoint rather than hardcoding them.

---

### Accounts

**Base route:** `/api/accounts` — **OAuth-blocked** (session/API-key only).

#### GET /api/accounts
List accounts the token's user can access. Returns `{ "accounts": [ ... ] }`, where each entry is the account object below **without** `account_roles` — only the single-account view adds that key.

#### GET /api/accounts/:id
View an account.

```json
{
  "account": {
    "id": "<guid>", "name": "Acme Corp",
    "reseller": false, "is_trial": false, "trial_start": null, "trial_end": null,
    "nameservers": [], "created_at": "...", "updated_at": "...",
    "parent_account": { "id": "<guid>", "name": "Parent" },
    "reseller_billing_plan": { "id": 1, "name": "default" },
    "account_roles": [ {
        "inherited_from": null,
        "created_at": "...", "updated_at": "...",
        "role": { "id": 1, "name": "account_admin", "label": "Account Admin",
          "is_admin": true, "can_edit": false, "can_create": false,
          "can_destroy": false, "billing": false, "wp_login": false },
        "user": { "id": "<guid>", "fname": "Jane", "lname": "Doe", "email": "jane@example.com",
          "account_brand_id": null, "locale": "en", "created_at": "...", "updated_at": "..." } } ]
  }
}
```

**`parent_account` and `reseller_billing_plan` are absent, not `null`.** When either does not apply the serializer stops emitting rather than writing `null`, and it stops for the rest of the account object:

| Account | `parent_account` | `reseller_billing_plan` |
|---------|------------------|-------------------------|
| Top-level (no parent) | **absent** | **absent** — dropped along with it, even when a plan is set |
| Sub-account, no reseller billing plan | present | **absent** |
| Sub-account with a reseller billing plan | present | present |

Test for key presence, not `=== null`. `account_roles` is emitted outside that object and is unaffected. `reseller_billing_plan.id` is a numeric plan id (not a guid).

#### POST /api/accounts
Create an account. Two modes:
- **Top-level** — no `X-Auth-Account`; requires admin user.
- **Sub-account** — `X-Auth-Account` = parent GUID; requires admin role on parent AND parent must be a reseller.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `account.name` | String | Yes | The only param accepted from non-admin callers. |

(Admin callers may additionally set `is_trial`, `trial_start`, `trial_end`, `reseller`, `reseller_bill_trial`, `billing_plan_id`, `parent_account_guid`. `term` is **not** an accepted create/update param.)

#### PATCH /api/accounts/:id
Update account name. Requires edit permission. Returns **`202`**.

#### DELETE /api/accounts/:id
Delete account. Requires destroy permission. Returns **`202`**. A non-staff user is additionally refused with **`401`** when this is their **only** account — that check lives inside the destroy permission, so it is not distinguishable from an ordinary permission failure.

---

### Account Roles

**Base route:** `/api/accounts/:account_id/roles` — requires admin on the account. **OAuth-blocked.**

`:user_id` is the **user's guid**: a role row is addressed by the user who holds it, not by the role row's own id. An unknown user, or a user with no role on this account, returns `404`.

- `GET /api/accounts/:account_id/roles` — list roles. Returns `{ "account_roles": [ <account role>, ... ] }`.
- `GET /api/accounts/:account_id/roles/:user_id` — view one user's role. Returns `{ "account_role": <account role> }`:
  ```json
  {
    "account_role": {
      "inherited_from": null,
      "created_at": "...", "updated_at": "...",
      "role": { "id": 1, "name": "account_admin", "label": "Account Admin",
        "is_admin": true, "can_edit": false, "can_create": false,
        "can_destroy": false, "billing": false, "wp_login": false },
      "user": { "id": "<user_guid>", "fname": "Jane", "lname": "Doe", "email": "jane@example.com",
        "account_brand_id": null, "locale": "en", "created_at": "...", "updated_at": "..." }
    }
  }
  ```
  `inherited_from` is the **guid of the account the role is inherited from**, or `null` when the role is held directly on this account. Each element of the list has exactly this shape, and `PATCH` returns it too.
- `POST /api/accounts/:account_id/roles` — invite a user by email. Returns **`202`**.
  ```json
  { "email": "user@example.com", "user_role_id": 2 }
  ```
  The invitee **does not have to be an existing user**: on a lookup miss an unverified user record is created for that address. Either way the call then creates an invitation and emails it — **no role row exists until the invitee accepts**, so the invited address does **not** appear in `GET .../roles` in the meantime, and `202` means "invitation sent", not "user added". Failures come back as `422 { "errors": ["..."] }` — for example `"Missing role"` when `user_role_id` matches no role, `"Missing user information"` when `email` is blank.
- `PATCH /api/accounts/:account_id/roles/:user_id` — change role. Returns **`200`** with the account-role object above; validation failure → `422 { "errors": [...] }`.
  ```json
  { "account_role": { "user_role_id": 3 } }
  ```
- `DELETE /api/accounts/:account_id/roles/:user_id` — remove user. **`202`**. Inherited role → **`422`** `"Unable to remove an inherited role."`

Use `GET /api/user_roles` for valid `user_role_id` values.

---

### API Keys

**Base route:** `/api/api_keys` — for the authenticated user. **OAuth-blocked.**

- `GET /api/api_keys` — list (no token value)
- `GET /api/api_keys/:id` — view (no token value)
- `POST /api/api_keys` — create; **token returned only on creation**
  ```json
  { "api_key": { "name": "My Integration" } }
  ```
- `PATCH /api/api_keys/:id` — rename
- `DELETE /api/api_keys/:id` — delete. Returns **`202`**.

Keys created here are always non-admin and non-system (`is_admin` / `system_managed` are forced `false`).

---

### Subscriptions

**Base route:** `/api/subscriptions` — **requires `X-Auth-Account`**; scope `billing:read`.
```json
{
  "subscription": { "id": "<guid>", "status": "active", "created_at": "...", "updated_at": "...",
    "price": { "amount_cents": 1000, "term": "monthly" },
    "run_rate": { "cents": 3000, "currency_iso": "USD" },
    "sites": [ { "id": "<guid>", "name": "my-site", "created_at": "...", "updated_at": "...",
      "primary_domain": "my-site.example.com", "location": "pdx", "package": "Basic",
      "dunning_suspended": false, "pending_delete": false, "delete_scheduled_at": null } ],
    "product": { "id": "basic", "name": "Basic" } }
}
```

- **`run_rate` is an object, not an integer.** It serializes as `{"cents": <integer>, "currency_iso": "<ISO-4217>"}` and is the subscription's whole rate (per-unit price times provisioned units) — `0` cents while the subscription is inactive, while the account is in trial, or when no price is set. The neighbouring `price.amount_cents` *is* a plain integer; the two fields are shaped differently, so don't read them the same way.
- `price` is always present as an object, but both `amount_cents` and `term` are `null` when the subscription has no price.
- **`package` and `product.id` are different vocabularies.** `package` is the site's product **display name** (`"Basic"`, `"Pro"`) and is `null` when the site has no subscription or product. `product.id` is the product's **short name** (`"basic"`). Never compare or substitute one for the other; short names are what other endpoints accept as identifiers.
- `pending_delete` / `delete_scheduled_at` — a soft-deleted ("pending delete") site stays in this list; `delete_scheduled_at` is the frozen purge date and is `null` for a live site.
- `location` is the location's short name. `primary_domain` is the site's attached hostname when it has one, otherwise the platform-assigned default hostname (deployment-specific — the value above is a placeholder).

---

### Users

**Base route:** `/api/users` — **requires `X-Auth-Account`** + admin on the account; the account must be a **reseller** (`422 "Must have reseller permissions"` on create/update/delete otherwise). **OAuth-blocked.**

- `GET /api/users` — list; `GET /api/users/:id` — view (fields include `account_brand_id`, `locale`).
- `POST /api/users` — create a sub-user. Rejected with `422` when the **calling user** is a CloudPress staff administrator — the guard is on who is calling, not on which account is targeted.
  ```json
  { "user": { "fname": "Jane", "lname": "Doe", "email": "jane@example.com",
    "company_name": "Acme", "locale": "en", "billing_term": "monthly" } }
  ```
  | Param | Type | Required | Notes |
  |-------|------|----------|-------|
  | `user.fname` / `user.lname` / `user.email` | String | Yes | |
  | `user.company_name` | String | No | |
  | `user.locale` | String | No | `en` or `nl` |
  | `user.billing_term` | String | No | `monthly` or `annual` |

  Response:
  ```json
  { "user": { "id": "<guid>", "fname": "Jane", "lname": "Doe", "email": "jane@example.com",
    "created_at": "...", "updated_at": "...", "password": "auto-generated", "account_id": "<guid>", "api_token": "<token>" } }
  ```
  `password` and `api_token` are returned **only on creation** — store them immediately.
- `PATCH /api/users/:id` / `DELETE /api/users/:id` — never permitted, but `401` from the action itself is only the **last** of several outcomes. In order: no `X-Auth-Account` → **`400`** `{"errors":["Missing X-Auth-Account"],"code":"missing_account"}`; caller is not an admin on the account → **`401`**; unknown user id → **`404`**; account is not a reseller → **`422`** `"Must have reseller permissions"`; only a request that passes all of those reaches the action and gets **`401`**.

---

### User Roles

`GET /api/user_roles` — list role definitions (use the IDs when inviting users). **OAuth-blocked**: this endpoint declares no scope, so an OAuth token gets `403 {"error":"insufficient_scope","error_description":"endpoint not available via OAuth"}`. Session or API-key credentials only.

```json
{ "user_roles": [
  { "id": 1, "name": "account_admin", "label": "Account Admin",
    "is_admin": true, "can_edit": false, "can_create": false, "can_destroy": false, "billing": false, "wp_login": false },
  { "id": 2, "name": "site_admin", "label": "Site Admin",
    "is_admin": false, "can_edit": true, "can_create": true, "can_destroy": true, "billing": true, "wp_login": false }
] }
```

The seeded roles and their flags:

| `name` | `label` | `is_admin` | `can_edit` | `can_create` | `can_destroy` | `billing` | `wp_login` |
|--------|---------|-----------|-----------|-------------|--------------|----------|-----------|
| `account_admin` | Account Admin | `true` | `false` | `false` | `false` | `false` | `false` |
| `site_admin` | Site Admin | `false` | `true` | `true` | `true` | `true` | `false` |
| `site_manager` | Site Manager | `false` | `true` | `false` | `false` | `false` | `false` |
| `site_viewer` | Site Viewer | `false` | `false` | `false` | `false` | `false` | `false` |
| `billing_manager` | Billing Manager | `false` | `false` | `false` | `false` | `true` | `false` |

`is_admin` is a superset, not a peer of the other flags: every permission check passes for an `is_admin` role regardless of the `false`s next to it — which is why `account_admin` needs none of them. **No seeded role sets `wp_login: true`.** A deployment can seed different roles and the `id`s are database ids rather than stable constants, so read this endpoint instead of hardcoding either.
