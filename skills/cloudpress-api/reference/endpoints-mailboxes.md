# Mailspace Mailboxes & Mail Recovery

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

Everything here is nested under **`/api/mailspace/:mailspace_id/…`**, where
`:mailspace_id` is the mailspace **guid** (a UUID). `X-Auth-Account` is **not**
required on these routes — an account-scoped credential resolves the mailspaces on
that account, and a user/session/OAuth credential sent without the header resolves the
mailspaces its user can reach. The examples below send it anyway.

**Every endpoint in this file inherits the same six gates, evaluated in this order.**
They are not repeated per endpoint; only endpoint-specific codes are listed below each
one.

1. **503** `stalwart_unavailable` — the mail server is not configured.
2. **404**, **empty body** — the mailspace guid is unknown *or* not reachable by this
   credential. Deliberately indistinguishable.
3. **403** `not_authorized` — decided on the **HTTP verb**: `GET` and `HEAD` always
   pass; anything else needs edit permission on the mailspace's own workspace.
4. **403** `mailspace_suspended` — staff block or dunning hold
   (`"This mailspace is on hold and cannot be modified. Please contact support."`).
   **Not verb-gated, unlike #3 and #5: reads are refused too**, despite the message
   saying "cannot be modified".
5. **403** `pending_delete` — the mailspace is soft-deleted. Verb-gated like #3, so
   **reads stay available for the whole retention window**.
6. **409** `not_provisioned` — the mailspace is not in the mail server yet
   (`"This mailspace is not provisioned yet. Complete domain verification first."`).

Error envelope is `{"errors": ["…"], "code": "…"}`. Error messages are **always
English regardless of `Accept-Language`** — branch on `code`, never on the text.

**Scopes.** Reads take `mailspace:read`, mutations `mailspace:write`. The exact split
per controller:

| Endpoint group | `mailspace:read` | `mailspace:write` |
|---|---|---|
| Mailboxes | `index`, `show`, `check` | `create`, `update`, `destroy`, `restore`, `force_delete` |
| App passwords | `index` | `create`, `update`, `destroy` |
| Mail rules | `index` | `create`, `update`, `destroy`, `toggle`, `move`, `adopt` |
| Vacation responses | `index`, `show` | `update`, `destroy` |
| Purged mailboxes | `index` | `update` |
| Archived items | `index`, `show`, `download` | `restore`, `destroy` |

`download` is a **read** — it rides `mailspace:read` despite returning a file.

**No endpoint in this file paginates.** Every index returns the full set and ignores
`page` / `per_page`. Two of them are bounded by a mail-server query cap instead, noted
where they are.

**No step-up ("sudo") auth applies to any of these routes**, including the irreversible
ones. The portal re-challenges for a mailbox password change, an app-password mint, a
permanent mailbox delete and a permanent archived-mail erase; over the API those are
gated by `mailspace:write` plus the edit-permission check, and each writes an audit-log
line naming the acting credential.

---

### Mailboxes

**Base route:** `/api/mailspace/:mailspace_id/mailboxes`. The `:id` segment is the
mailbox **guid** (a UUID), never the address — an address is mutable and contains dots,
which the segment would not carry. Both `restore` and `force_delete` are member routes
on that guid.

`status` is one of `active`, `suspended`, `pending_deletion`.

#### GET /api/mailspace/:mailspace_id/mailboxes — list mailboxes

Query param `q`: case-insensitive substring match on the mailbox's **primary address**
only. It does not match display names, aliases, or the `pending` bucket.

**This is a live read against the mail server**, not a table scan — the mail server is
the system of record for which mailboxes exist, so each call costs a JMAP round trip and
**may create local rows as a side effect** (a mailbox that exists upstream but has
drifted out of the local table is backfilled here, with `status` defaulting to
`active`). Poll it sparingly.

```json
{
  "mailboxes": [
    { "id": "<guid>", "email": "sales@example.com", "display_name": "Sales",
      "status": "active", "quota_mb": 5120, "used_mb": 214,
      "aliases": ["info@example.com"], "stalwart_id": "acct-1a2b",
      "scheduled_deletion_at": null }
  ],
  "pending": [
    { "id": "<guid>", "email": "old@example.com", "status": "pending_deletion",
      "scheduled_deletion_at": "2026-08-27T09:12:44.000Z", "days_until_deletion": 7 }
  ]
}
```

Every key in both arrays is **always present**; nullable ones are emitted as explicit
`null`, never omitted.

| Field | Type | Notes |
|-------|------|-------|
| `id` | String (UUID) | The mailbox guid — the `:id` segment for every other endpoint here. |
| `email` | String | The principal's primary address. |
| `display_name` | String | `""` when the mail server reports none — a String, never `null`. |
| `status` | String | `active` or `suspended` in this array; a `pending_deletion` mailbox is moved to `pending` instead and never appears in both. |
| `quota_mb` | Integer | The per-mailbox cap. **`0` means "no per-mailbox cap"** — the mailbox is still bounded by the package's storage pool. Converted from the mail server's bytes by integer division. |
| `used_mb` | Integer | Converted from bytes and **rounded up**, so any non-zero usage reports at least `1`. |
| `aliases` | `Array<String>` | Every address on the principal after the primary one. |
| `stalwart_id` | String | The mail-server principal id. |
| `scheduled_deletion_at` | String (ISO 8601) / null | `null` for a live mailbox. |
| `pending[].days_until_deletion` | Integer / null | Whole days left, **floored at 0**; `null` when the row carries no date. |

`pending` is ordered by `scheduled_deletion_at` (soonest first) and is **not** filtered
by `q` — it is a short fixed to-do list, not a searchable index.

**An empty `mailboxes` array is authoritative.** The underlying principal read is
strict: a mailspace whose mailboxes could not be read answers **503**
`mailboxes_unavailable`, never **200** with an empty array. So `"mailboxes": []` means
the mail server was asked and holds none, and a client may reconcile its own state
against it.

`mailboxes_unavailable` covers **every** failure of that one read — unreachable, timed
out, a 5xx, or the platform's own mail-server credential refused — and only that read. A
bug anywhere else in the endpoint is a 500, not this code. Note that `pending` is **not**
returned alongside the 503: the response is the error envelope and nothing else, even
though `pending` comes from local state and is still knowable. Retry rather than treating
the mailspace as empty.

**Ceiling: the mail server is asked for at most 500 accounts.** A mailspace holding
more than that cannot reach the remainder, and `q` filters the already-capped set in
memory rather than narrowing the query.

Mailboxes already hard-deleted whose mail the server is still holding are **deliberately
not** in this response — see [Purged Mailboxes](#purged-mailboxes). That bucket's own read
is skipped entirely here rather than computed and discarded, so a failure to read it can
never decide this endpoint's status.

**Codes:** **503** `mailboxes_unavailable`.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/mailspace/<guid>/mailboxes?q=sales"
```

#### GET /api/mailspace/:mailspace_id/mailboxes/check — is an address free?

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `username` | String | Yes | The local part. Blank → **400** `invalid_address`. |
| `domain` | String | No | Defaults to the mailspace's primary domain. |

```json
{ "available": true, "used_by": null }
```

| Field | Type | Notes |
|-------|------|-------|
| `available` | Boolean / null | `null` means **could not verify**. |
| `used_by` | String / null | `"mailbox"`, `"group"`, or `"mailing list"` — `null` when the address is free or when `available` is `null`. |

The mail server's address namespace is flat across mailboxes, groups and mailing lists
and **includes their aliases**, so this cannot be answered locally: an address held only
as a mailing-list alias reads as free in local state and then fails the create. The
local table is consulted only as a fallback, so a mailbox row that has drifted out of
the mail server still reads as taken.

**Advisory only.** `available: null` is neither taken nor free — any failure reading the
mail server collapses to it, and there is no error code. **Never branch on
`!available`**, and treat a `true` as a hint, not a reservation: the create is the
authority.

**Codes:** **400** `invalid_address`.

#### GET /api/mailspace/:mailspace_id/mailboxes/:id — show one mailbox

Several JMAP round trips per call.

```json
{
  "mailbox": {
    "id": "<guid>", "email": "sales@example.com", "display_name": "Sales",
    "status": "active", "quota_mb": 5120, "used_mb": 214,
    "aliases": ["info@example.com"], "stalwart_id": "acct-1a2b",
    "scheduled_deletion_at": null,
    "allowed_ips": ["203.0.113.4", "198.51.100.0/24"],
    "groups": ["team@example.com"],
    "lists": ["announce@example.com"],
    "two_factor": { "enabled": false },
    "app_passwords": [
      { "id": "cred-9", "description": "Thunderbird", "allowed_ips": [],
        "created_at": "2026-06-01T10:00:00.000Z" }
    ],
    "created_at": "2026-05-02T08:31:00.000Z",
    "updated_at": "2026-08-14T11:02:19.000Z"
  }
}
```

The list fields above, plus:

| Field | Type | Notes |
|-------|------|-------|
| `allowed_ips` | `Array<String>` | Sign-in IP restriction on the mailbox's **own** password credential. `[]` = any address. App passwords carry their own separate lists. |
| `groups` | `Array<String>` | Group addresses this mailbox belongs to. |
| `lists` | `Array<String>` | Mailing-list addresses it is subscribed to. |
| `two_factor.enabled` | Boolean | **Flag only.** The shared secret and the `otpauth://` URL are never emitted, and enrolment is not available over this API. |
| `app_passwords` | `Array<Object>` | The same objects as the app-passwords index — **never including `secret`**. |
| `created_at` / `updated_at` | String (ISO 8601) | Of the local mailbox record. |

**Three quiet degradations, all answering 200.** Each mail-server read behind this
payload is tolerant, so a read that fails contributes a default rather than an error:

- `display_name` → `""`, `quota_mb` → `0`, `used_mb` → `0`, `allowed_ips` → `[]` when the
  principal read fails. **`stalwart_id` does not degrade** — it is taken from the local
  record first and only falls back to the mail server's value, so a failed read leaves it
  intact. A `null` `stalwart_id` means the local record was never stamped, **not** that
  this payload is degraded; do not use it as a retry sentinel.
- `aliases`, `groups`, `lists`, `app_passwords` → `[]` when their own reads fail.
- `two_factor.enabled` → `false` when that read fails.

`quota_mb: 0` is the collision that matters: it is also the legitimate encoding for "no
per-mailbox cap", so a failed read and an uncapped mailbox are indistinguishable here.
`id`, `email` and `status` come from local state and are always real.

**Codes:** **404** `unknown_mailbox` (unknown guid, or a guid belonging to another
workspace — the same answer, so this cannot probe what exists elsewhere).

#### POST /api/mailspace/:mailspace_id/mailboxes — create a mailbox. Returns **201**.

```json
{ "username": "sales", "domain": "example.com", "password": "…",
  "display_name": "Sales", "quota_mb": 5120,
  "aliases": ["info@example.com"], "groups": ["team@example.com"], "lists": [] }
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `username` | String | Yes | Local part. Blank → **400** `username_blank`. |
| `domain` | String | No | Defaults to the mailspace's primary domain. |
| `password` | String | Yes | Blank → **400** `password_blank`. No confirmation field. |
| `display_name` | String | No | Defaults to `""`. |
| `quota_mb` | Integer | No | Defaults to `0` = no per-mailbox cap. May not exceed the package's whole storage pool. |
| `aliases` | `Array<String>` | No | Blank entries are dropped. |
| `groups` | `Array<String>` | No | Group addresses **in this mailspace**. |
| `lists` | `Array<String>` | No | Mailing-list addresses **in this mailspace**. |

TOTP enrolment is not accepted here — there is no secret parameter.

Response is the `mailbox` object of `#show`'s **summary** fields plus `created_at` /
`updated_at`; it does **not** carry `allowed_ips`, `groups`, `lists`, `two_factor` or
`app_passwords`. `GET` the mailbox for those.

**Codes:** **400** `username_blank` / `password_blank`; **422** `create_failed`.

`create_failed` covers an enumerated set, distinguishable only by the `errors` text:
the package's mailbox limit is already reached; `quota_mb` exceeds the package's whole
storage pool; the address is already used by a mailbox, group or mailing list in this
mailspace; a submitted group or list address is not one of this mailspace's own; the
group/list check could not be performed against the mail server; or the mail server
refused the create.

A partial failure after the principal exists still leaves a usable mailbox: the local
record is written immediately after the principal is created, before aliases, groups and
lists are applied, so a failure in that tail leaves a real, editable mailbox rather than
an invisible orphan. Re-`PATCH` the fields that did not land.

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{"username":"sales","password":"…","quota_mb":5120}' \
  "https://my.cloudpress.com/api/mailspace/<guid>/mailboxes"
```

#### PATCH /api/mailspace/:mailspace_id/mailboxes/:id — update a mailbox

A true partial update: an **omitted** key is left untouched. What an *empty* value does
differs per field, and two of them are traps:

| Param | Type | Empty value means |
|-------|------|-------------------|
| `display_name` | String | `""` clears the display name. |
| `quota_mb` | Integer | `""` is **ignored, not cleared** — the current cap stays. Send `0` to mean "no per-mailbox cap". |
| `status` | String | `"active"` or `"suspended"`. `""` is **not** "leave alone" — it fails validation and answers **422** `update_failed`. Omit the key instead. |
| `password` | String | Blank or omitted keeps the current password. |
| `aliases` | `Array<String>` | `[]` removes every alias. |
| `groups` | `Array<String>` | `[]` removes every group membership. |
| `lists` | `Array<String>` | `[]` unsubscribes from every list. |
| `allowed_ips` | `Array<String>` or String | `[]` / `""` clears the sign-in IP restriction. |

`status: "pending_deletion"` is **refused** (**422** `update_failed`) **only when the
mailbox is not already pending deletion** — scheduling a deletion goes through `DELETE`,
which suspends the mailbox upstream and starts the retention clock together. Re-sending
the value against an already-scheduled mailbox is **accepted** (**200**) and changes
nothing, so echoing a mailbox's own `status` back on `PATCH` is safe. Any other
unrecognized status is refused with **422** `update_failed`.

**`status: "active"` on a `pending_deletion` mailbox is a second restore path.** It
reactivates the mailbox upstream and clears `scheduled_deletion_at`, and it is subject
to the same package mailbox-limit re-check as `POST .../restore` — so it can answer
**422** `update_failed` on a mailspace that has since been downgraded.

**`allowed_ips` is parsed before anything is written.** It accepts an array or a single
comma / whitespace / semicolon separated string. At most **20** entries. Every entry
must be an IP address or CIDR range; a rejected list is a **400** that names the
offending entry and **writes nothing**. Entries are normalized and de-duplicated, and a
masked range is stored in masked form — `10.0.0.5/8` is stored and returned as
`10.0.0.0/8`, so the value you read back may differ from the one you sent. The
validation exists because a wrong entry locks the mailbox out of webmail and every
device while the mail server tells the refused client nothing about why (JMAP answers a
bare 403, IMAP drops the connection), so a typo presents as an unexplained outage.

Response is the same shape as `POST`. Note it does **not** echo `allowed_ips` — `GET`
the mailbox to read back what was stored.

**Codes:** **400** `invalid_allowed_ips`; **404** `unknown_mailbox`; **422**
`update_failed`.

`update_failed` covers: an unrecognized `status`; `quota_mb` above the package pool; a
foreign group or list address; a group/list check that could not be performed; the
mailbox-limit re-check on an un-delete; or the mail server refusing the write.

#### DELETE /api/mailspace/:mailspace_id/mailboxes/:id — schedule deletion

**Soft delete.** The mailbox is suspended upstream immediately (mail stops flowing) and
erased after a **7-day** retention window; until then `POST .../restore` brings it back
with its mail intact.

**Idempotent.** Repeating it on a mailbox that is already scheduled reports success and
**does not push `scheduled_deletion_at` further out** — a retry after a timeout cannot
extend the window indefinitely.

```json
{ "mailbox": { "id": "<guid>", "email": "old@example.com", "status": "pending_deletion",
               "scheduled_deletion_at": "2026-08-27T09:12:44.000Z",
               "days_until_deletion": 7 } }
```

**Codes:** **404** `unknown_mailbox`; **422** `delete_failed`.

#### POST /api/mailspace/:mailspace_id/mailboxes/:id/restore — undo a scheduled deletion

Reactivates the mailbox upstream and clears the deletion date. Idempotent on an
already-active mailbox. Response is the same shape as `DELETE`, with `status: "active"`
and both date fields `null`.

Refused with **422** `restore_failed` when the package's mailbox limit no longer has
room — the limit counts only live mailboxes, so a downgrade performed while mailboxes
were parked in the grace window blocks the restore. Resize up first.

**Codes:** **404** `unknown_mailbox`; **422** `restore_failed`.

#### DELETE /api/mailspace/:mailspace_id/mailboxes/:id/force_delete — permanent

**Irreversible.** This expedites the mail server's erase instead of leaving the mailbox
recoverable for the rest of the retention window, so it is also the route to freeing
storage and mailbox count before a downgrade — a soft-deleted mailbox still counts
against the package's mailbox limit; a force-deleted one does not.

**Precondition: the mailbox must already be `pending_deletion`.** Call `DELETE` on it
first. A live mailbox is refused with **409** `not_pending_deletion`, so no single call
can erase a working mailbox.

Every call writes an audit-log line naming the mailbox and the acting credential,
**after** the erase succeeds.

```json
{ "status": "deleted", "email": "old@example.com" }
```

**Codes:** **404** `unknown_mailbox`; **409** `not_pending_deletion`; **422**
`delete_failed`; **503** `delete_unavailable`.

The two failures are **not** the same and the difference is the retry decision:

| Code | Status | What is known |
|---|---|---|
| `delete_failed` | **422** | The erase did not complete — a refusal, or a failure part-way. Not necessarily terminal; a plain mail-server outage also lands here, because the remote destroy is the first thing that raises. |
| `delete_unavailable` | **503** | The destroy **did** go through, but whether the mail is still recoverable could not be confirmed. The mailbox stays `pending_deletion` and a background sweep retries. Do not read this as "nothing happened". |

Unless the erase is expedited this way, the mail server keeps the account's mail for its
own retention window after the mailbox record is gone — that bucket is
[Purged Mailboxes](#purged-mailboxes).

---

### Mailbox App Passwords

**Base route:** `/api/mailspace/:mailspace_id/mailboxes/:mailbox_id/app_passwords`.
Note the nested segment is `:mailbox_id` (the mailbox guid); `:id` on this resource is
the **app password's own credential id**, a String from the mail server, not a guid.

An app password is a standalone IMAP/SMTP/JMAP credential that keeps working after the
mailbox's own password is changed. There is no local record — every action talks to the
mail server.

**A mailbox that is `pending_deletion` is not addressable here**: all four actions
resolve the mailbox with pending-deletion rows excluded, so they answer **404**
`unknown_mailbox`. Restore the mailbox first. (The mailbox endpoints themselves
deliberately do not exclude those rows — `restore` and `force_delete` are only legal on
one.)

#### GET .../app_passwords — list a mailbox's app passwords

```json
{ "app_passwords": [
    { "id": "cred-9", "description": "Thunderbird", "allowed_ips": [],
      "created_at": "2026-06-01T10:00:00.000Z" } ] }
```

| Field | Type | Notes |
|-------|------|-------|
| `id` | String | The credential id — the `:id` segment on `PATCH` and `DELETE`. |
| `description` | String / null | Whatever the mail server holds. |
| `allowed_ips` | `Array<String>` | `[]` = any address may authenticate with this credential. |
| `created_at` | String (ISO 8601) / null | `null` when the mail server recorded none. **The only history an app password has** — there is no last-used timestamp anywhere. |

Ordered oldest-created first. **Never carries `secret`.**

**An empty array can also mean the read failed.** This read is tolerant: a mail-server
failure answers **200** with `[]` rather than an error code.

**Codes:** **404** `unknown_mailbox`.

#### POST .../app_passwords — mint an app password. Returns **201**.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `description` | String | Yes | Blank → **400** `description_blank`. It is the only way to tell two credentials apart when revoking. |

```json
{ "app_password": { "id": "cred-9", "description": "Thunderbird",
                    "allowed_ips": [], "created_at": null,
                    "secret": "…" } }
```

**`secret` is returned exactly once, here.** The mail server keeps no readable copy, so
neither the index nor the mailbox payload can return it — a client that loses this
response can only revoke the credential and mint another. Store it on receipt; treat it
as a credential and do not log it.

`created_at` in **this** response is always `null` — the create response is assembled
locally and does not read the stored timestamp back. `GET` the list to see it.

The new credential is **unrestricted**; `PATCH` it to pin it to a set of addresses.
Every mint writes an audit-log line naming the mailbox and the acting credential.

**Codes:** **400** `description_blank`; **404** `unknown_mailbox`; **422**
`app_password_create_failed` (the mail server refused, or the mailbox has no principal
there).

#### PATCH .../app_passwords/:id — restrict one credential by IP

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `allowed_ips` | `Array<String>` or String | **Yes** | Addresses and CIDR ranges allowed to authenticate with **this** credential. `[]`, `""`, `null` or `allowed_ips[]=` all clear the restriction. |

**The key is required**, unlike the sibling mailbox `PATCH` where an omitted field is
left untouched. It is this endpoint's only writable field, and clearing is a real write
(an empty set means *unrestricted* upstream), so an absent key would be indistinguishable
from an intent to clear. An absent key is **400** `allowed_ips_missing` and writes
nothing; every way of *expressing* "clear" still works.

Same parsing rules and same 20-entry cap as the mailbox `PATCH`, and the same
parse-before-write guarantee: a rejected list is a **400** naming the offending entry
with nothing written.

This is **per credential** — it never touches the mailbox's own sign-in password, so it
cannot lock anyone out of webmail.

```json
{ "app_password": { "id": "cred-9", "allowed_ips": ["10.0.0.0/8"] } }
```

Only those two fields come back — not `description`, not `created_at`. The
`allowed_ips` value is the **normalized list that was written**, echoed from the
submitted input rather than read back from the credential, so it may differ from what
you sent (a masked range is stored masked).

**Codes:** **400** `allowed_ips_missing` / `invalid_allowed_ips`; **404**
`unknown_mailbox`; **422** `app_password_update_failed`. A credential id the mail server
does not accept surfaces as that **422** — there is no distinct 404 for one.

#### DELETE .../app_passwords/:id — revoke

The credential stops authenticating immediately. The mailbox's own password and every
other app password are untouched.

```json
{ "status": "revoked", "id": "cred-9" }
```

`id` is echoed from the request path, not read back from the mail server.

**Codes:** **404** `unknown_mailbox`; **422** `app_password_delete_failed`.

---

### Mailbox Mail Rules

**Base route:** `/api/mailspace/:mailspace_id/mailboxes/:mailbox_id/mail_rules`, with
the rule segment spelled **`:rule_id`** (`.../mail_rules/:rule_id`). `toggle` and
`move` are member routes on it; `adopt` is a collection route.

**A rule is not an addressable object — the script is.** A mailbox has exactly one
active filter script, and every rule (plus the out-of-office reply that
[Vacation Responses](#vacation-responses) writes) is a block inside it. There is no
"update rule 3" call on the mail server, so **every mutation is a whole-script
read-modify-write**. Three consequences:

1. **Every mutating response returns the entire rule list**, not just the rule you
   touched. Use it — a client that holds a stale list and writes from it deletes what
   it forgot.
2. Writes on one mailbox are serialized server-side across the whole
   read-modify-write, so two concurrent writers cannot silently drop each other's
   rules.
3. **Rule order is evaluation order** (top to bottom), and `stop_processing` really
   does skip everything below. `move` changes behavior, not presentation.

**`unmanaged: true` means the mailbox's active script was not written by CloudPress's
rule builder** — hand-edited, or written by another mail client. Its rules are still listed as far as
they could be parsed, but **every write answers 409 `script_unmanaged`** until
`POST .../adopt` is called. Check the flag from the index rather than discovering it on
the 409. The check also runs again inside the write, so a script that becomes unmanaged
between your read and your write is caught too.

**A mailbox that is `pending_deletion` is not addressable here** — **404**
`unknown_mailbox`. Restore it first.

**Rule object**

```json
{ "id": "8f14…", "name": "Invoices", "display_name": "Invoices",
  "enabled": true, "match_type": "all", "stop_processing": false, "editable": true,
  "conditions": [ { "field": "subject", "comparator": "contains",
                    "values": ["invoice", "receipt"], "header_name": null } ],
  "actions": [ { "type": "move", "value": "Invoices" } ] }
```

| Field | Type | Notes |
|-------|------|-------|
| `id` | String (UUID) | The rule's own id from the script metadata — the `:rule_id` segment. Rules have no local record. |
| `name` | String | Always a String; `""` for a rule written elsewhere with no name. |
| `display_name` | String | `name`, or the literal `"Untitled rule"` when it is blank. |
| `enabled` | Boolean | A disabled rule keeps its place and settings but emits nothing. |
| `match_type` | String | `all` (every condition must match) or `any` (one is enough). |
| `stop_processing` | Boolean | Skip the rules below this one when it matches. Distinct from the `stop` action. |
| `editable` | Boolean | `false` when the rule uses filtering this API does not write. Such a rule can still be toggled, moved or deleted; `PATCH` refuses it with **409** `rule_not_editable`. |
| `conditions[].field` | String | See the vocabulary below. |
| `conditions[].comparator` | String | Valid set depends on `field`. |
| `conditions[].values` | `Array<String>` | Several values in **one** condition are OR'd together, whatever `match_type` says. |
| `conditions[].header_name` | String / null | **Always present.** `null` when the stored condition carries no header name. It is **not** gated on `field` — a `header_name` sent alongside any valid field is retained and echoed back non-null. |
| `actions[].type` | String | See below. |
| `actions[].value` | String / null | **Always present**, `null` for an action that takes no value. |

**Condition vocabulary.** Fields accepted on a write: `from`, `to`, `cc`, `subject`,
`header`, `body`, `size`, `attachment`. Anything else is **400** `invalid_rule`. Only
`from`, `to`, `cc`, `subject` and `body` are **writable** — a rule using `header`, `size`
or `attachment` round-trips and can be toggled, moved or deleted. **Two different codes
refuse a write, and which one you get depends on where the non-editable field is.**
Submitting one on create, or on an update of an otherwise editable rule, is **422**
`unsupported_rule`. Updating a rule that is *already stored* with a non-editable field is
**409** `rule_not_editable` — that check runs first, so the **422** is never reached on
that path.

| Field | Comparators |
|---|---|
| `from`, `to`, `cc`, `subject`, `header` | `contains`, `not_contains`, `is`, `not_is`, `starts_with`, `ends_with`, `matches` |
| `body` | `contains`, `is` |
| `size` | `greater_than`, `less_than` |
| `attachment` | `has_any`, `has_type` |

A comparator outside its field's set is **422** `invalid_rule`.

**Action vocabulary.** Accepted on a write: `move`, `copy`, `forward`, `mark_read`,
`star`, `add_label`, `discard`, `reject`, `keep`, `stop`. Anything else is **400**
`invalid_rule`. Only `move`, `forward`, `mark_read`, `star` and `discard` are
**writable**; `copy`, `add_label`, `reject`, `keep` and `stop` are read-only in the same
way the three read-only fields are. Of the writable ones, `move` needs a folder name and
`forward` needs a value that parses as an email address; `mark_read`, `star` and
`discard` take none.

#### GET .../mail_rules — list rules in evaluation order

```json
{ "mailbox": { "id": "<guid>", "email": "sales@example.com" },
  "mail_rules": [ { "id": "8f14…", "…": "…" } ],
  "unmanaged": false }
```

Costs one script fetch plus a blob download on the mail server.

**Codes:** **404** `unknown_mailbox`; **422** `mail_rules_unavailable` (the script could
not be read — note the **422**, not a 503).

#### POST .../mail_rules — create a rule. Returns **201**.

Appended to the **end** of the list, so it evaluates after every existing rule.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | String | Yes | Blank → **422** `invalid_rule`. Max 200 characters. |
| `enabled` | Boolean | No | Default `true`. |
| `match_type` | String | No | `all` (default) or `any`. **An unrecognized value is silently coerced to `all`**, not rejected. |
| `stop_processing` | Boolean | No | Default `false`. |
| `conditions` | `Array<Object>` | Yes in practice | `{field, comparator, values, header_name}`; `values` may be sent as a single `value` String instead. An empty list → **422** `invalid_rule`. |
| `actions` | `Array<Object>` | Yes in practice | `{type, value}`. An empty list → **422** `invalid_rule`. |

Keys other than these six are dropped, in `conditions` and `actions` elements too.
Each condition on a writable field needs at least one non-blank value, or the rule
compiles into a filter that matches nothing — refused with **422** `invalid_rule` rather
than saved.

```json
{ "mail_rule": { "id": "8f14…", "…": "…" },
  "mail_rules": [ "…the whole new list…" ],
  "unmanaged": false }
```

**Codes:** **400** `invalid_rule` (unknown condition field or action type); **404**
`unknown_mailbox`; **409** `script_unmanaged`; **422** `invalid_rule` /
`unsupported_rule` / `mail_rules_unavailable` / `save_failed`.

The two spellings of `invalid_rule` are deliberate: **400** means the request used a
word that is not in the vocabulary at all, **422** means the vocabulary was right and
the rule is not usable.

#### PATCH .../mail_rules/:rule_id — edit a rule in place

Keeps the rule's id and its position in the evaluation order. Any field you omit keeps
its stored value — but sending `conditions` or `actions` **replaces that whole array**;
there is no per-element merge, because the elements have no ids.

A rule whose stored form is not `editable` is refused with **409** `rule_not_editable`;
rewriting it would silently turn it into a different rule. Toggle, move and delete
still work on it.

Response and codes as `POST` (status **200**), plus **404** `unknown_rule` and **409**
`rule_not_editable`.

#### DELETE .../mail_rules/:rule_id — delete a rule

```json
{ "deleted_rule_id": "8f14…", "mail_rules": [ "…the remaining list…" ],
  "unmanaged": false }
```

Works on a rule that is not `editable`.

**Codes:** **404** `unknown_mailbox` / `unknown_rule`; **409** `script_unmanaged`;
**422** `mail_rules_unavailable` / `save_failed`.

#### PATCH .../mail_rules/:rule_id/toggle — enable or disable a rule

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `enabled` | Boolean | No | **Omitting it flips the current value**, which is not idempotent — a retry after a timeout flips it back. Automated callers should always send it explicitly. |

Works on a rule that is not `editable` — turning a rule off does not touch what it
matches. Response is the `PATCH` shape.

**Codes:** **404** `unknown_mailbox` / `unknown_rule`; **409** `script_unmanaged`;
**422** `mail_rules_unavailable` / `save_failed`.

#### PATCH .../mail_rules/:rule_id/move — reorder one place

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `direction` | String | Yes | `up` or `down`. Anything else → **400** `invalid_direction`. |

Moves the rule exactly one position. Moving the first rule up, or the last one down, is
**422** `invalid_move` rather than a silent no-op. Response is the `PATCH` shape — read
`mail_rules` for the new order.

**Codes:** **400** `invalid_direction`; **404** `unknown_mailbox` / `unknown_rule`;
**409** `script_unmanaged`; **422** `invalid_move` / `mail_rules_unavailable` /
`save_failed`.

#### POST .../mail_rules/adopt — take over a foreign script

**Destructive, and the only endpoint here that ever overwrites an unmanaged script.**
It replaces the customer's own script with the rules that could be parsed out of it —
anything this API cannot represent is **gone afterwards**. Call the index first and show
a human what is about to be replaced. On an already-managed script it is a harmless
no-op rewrite.

Takes no body parameters.

```json
{ "adopted": true, "mail_rules": [ "…" ], "unmanaged": false }
```

**Codes:** **404** `unknown_mailbox`; **422** `mail_rules_unavailable` / `save_failed`.
There is no `script_unmanaged` here — an unmanaged script is the precondition, not a
refusal.

---

### Vacation Responses

**Base route:** `/api/mailspace/:mailspace_id/vacation_responses`, keyed by
**`:mailbox_id`** — the **mailbox guid**, not an id of its own. One reply per mailbox.

The reply lives in the **same script as the mailbox's filter rules**, so everything the
mail-rules section says about whole-script writes and `unmanaged` applies unchanged:
a script written outside CloudPress's rule builder is never overwritten implicitly
(**409** `script_unmanaged`), and `POST .../mailboxes/:mailbox_id/mail_rules/adopt` is the
explicit opt-in — **there is no separate adopt here**, because there is one script.

**There is no `POST` route.** `PATCH` is an upsert.

A mailbox that is `pending_deletion` is not addressable by `show`, `update` or
`destroy` (**404** `unknown_mailbox`), and is omitted from the index.

#### GET .../vacation_responses — out-of-office state for every mailbox

**Served from local cached state — this endpoint never touches the mail server.**
Reading the live reply costs a script fetch plus a blob download *per mailbox*, which is
not a list operation. It is therefore **stale** for any mailbox whose script was last
changed elsewhere.

Ordered by `email`. Mailboxes pending deletion are omitted.

```json
{ "vacation_responses": [
    { "mailbox_id": "<guid>", "email": "sales@example.com", "synced": true,
      "configured": true, "enabled": false,
      "from_date": "2026-09-01", "to_date": "2026-09-14" } ] }
```

| Field | Type | Notes |
|-------|------|-------|
| `mailbox_id` | String (UUID) | The mailbox guid — the segment for the other three actions. |
| `email` | String | |
| `synced` | Boolean | `false` when this mailbox has no cached summary yet (its script has not been read or written since the feature shipped). |
| `configured` | Boolean | A reply exists. |
| `enabled` | Boolean | It actually goes out. Separate from `configured` because a reply can be written, dated and switched off. |
| `from_date` / `to_date` | String (`YYYY-MM-DD`) / null | `null` means the reply is not limited in that direction. |

**On a `synced: false` row, `configured` and `enabled` are `false`, not `null`** — only
the two dates are `null`. Do not read those `false` values as "no reply"; they mean
"unknown". `GET` that mailbox's own reply for live state.

This response carries **no `unmanaged` key** — only the three per-mailbox actions do.

**Codes:** none beyond the inherited gates. Note that `not_authorized` cannot occur on
this or any other `GET` here.

#### GET .../vacation_responses/:mailbox_id — one reply, read live

```json
{ "vacation_response": {
    "mailbox_id": "<guid>", "email": "sales@example.com",
    "configured": true, "enabled": true,
    "subject": "Out of office", "text_body": "Back on the 15th.", "html_body": null,
    "from_date": "2026-09-01", "to_date": "2026-09-14" },
  "unmanaged": false }
```

`configured: false` with `subject`, `text_body`, `html_body`, `from_date` and `to_date`
all `null` means the mailbox has no reply at all. All keys are always present.

**Codes:** **404** `unknown_mailbox`; **422** `mail_rules_unavailable` (the script could
not be read).

#### PATCH .../vacation_responses/:mailbox_id — create or replace (upsert)

Every field is optional; an **omitted** field keeps its stored value, and an **empty
string clears** it.

| Param | Type | Notes |
|-------|------|-------|
| `enabled` | Boolean | Whether the reply actually goes out. Defaults to `true` for a mailbox that has no reply yet, and to the stored value otherwise. |
| `subject` | String | |
| `text_body` | String | |
| `html_body` | String | Clients that render HTML prefer this over `text_body`, so send `""` to stop sending an HTML version. |
| `from_date` | String | `YYYY-MM-DD`. The reply only answers inside the window. |
| `to_date` | String | Same. |

**Dates are validated strictly as ISO 8601.** A full ISO 8601 datetime is accepted and
trimmed to its date — the window is whole days. Anything else, prose included, is
**400** `invalid_date` and nothing is written; it is not guessed at. `""` clears the
bound.

**An enabled reply needs something to say.** Enabling one with no subject and no body of
either kind is **422** `vacation_body_required` rather than saved as a reply that answers
no one. Use `DELETE` to remove one.

Because the mail server compiles the reply as a single block, an omitted field is
re-supplied from what is stored before the write — which is what makes
`{"enabled": false}` switch a reply off instead of erasing its text.

Response is the `show` shape, status **200**.

**Codes:** **400** `invalid_date`; **404** `unknown_mailbox`; **409**
`script_unmanaged`; **422** `vacation_body_required` / `mail_rules_unavailable` /
`save_failed`.

```bash
curl -X PATCH -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{"enabled":true,"subject":"Out of office","text_body":"Back on the 15th.","from_date":"2026-09-01","to_date":"2026-09-14"}' \
  "https://my.cloudpress.com/api/mailspace/<guid>/vacation_responses/<guid>"
```

#### DELETE .../vacation_responses/:mailbox_id — remove the reply

The reply drops out of the mailbox's script and its **filter rules are left exactly as
they were**. Idempotent — removing a reply the mailbox does not have is a **200**.

Response is the `show` shape with the reply cleared: `configured: false`, `enabled:
false`, and `subject` / `text_body` / `html_body` / `from_date` / `to_date` all `null`.

**Codes:** **404** `unknown_mailbox`; **409** `script_unmanaged`; **422**
`mail_rules_unavailable` / `save_failed`.

---

### Purged Mailboxes

**Base route:** `/api/mailspace/:mailspace_id/purged_mailboxes`, keyed by **`:guid`**
(`.../purged_mailboxes/:guid`) — the guid of the *snapshot*, not of the deleted mailbox
record, which no longer exists. Only `index` and `update` are routed.

Deleting a mailbox on the mail server does not erase anything: it drops the account and
**schedules** the erase for after the server's retention window. Until that fires, the
account can be put back with its original id and every message intact. These endpoints
are that window.

This bucket is **deliberately absent from the mailbox index** — listing it in two places
would invite a client to reconcile one against the other.

#### GET .../purged_mailboxes — what can still be restored

Ordered by `recoverable_until`, **soonest to expire first**.

```json
{ "purged_mailboxes": [
    { "id": "<guid>", "email": "old@example.com", "display_name": "Old Sales",
      "purged_at": "2026-08-01T12:00:00.000Z",
      "recoverable_until": "2026-08-31T12:00:00.000Z",
      "days_remaining": 11 } ] }
```

| Field | Type | Notes |
|-------|------|-------|
| `id` | String (UUID) | The snapshot guid — the `:guid` segment for the restore. |
| `email` | String | The address that comes back. |
| `display_name` | String / null | |
| `purged_at` | String (ISO 8601) | When the mailbox was hard-deleted. |
| `recoverable_until` | String (ISO 8601) | **The mail server's own scheduled-erase time, mirrored at delete time** — never a locally computed window. The retention setting is server-wide and staff can change it. |
| `days_remaining` | Integer | Whole days left, floored at 0. |

**A snapshot the mail server no longer holds is omitted.** The local list is intersected
with the mail server's actual pending erases on every call, because the retention window
is a server-wide setting an admin can shorten and an expedited erase takes effect at
once — either leaves a snapshot whose `recoverable_until` is still in the future while
the mail is already gone. A restore this endpoint cannot honour is never offered.

**That cross-check is strict, and this is the one index in this file that does not
degrade to an empty 200.** When the mail server cannot be asked, it answers **503**
`purged_mailboxes_unavailable`, not `[]`. A degraded read cannot hide inside an empty
array here.

**But an empty list is still not proof, and this is the one caveat to take seriously on
this endpoint.** The underlying cross-check reads the mail server's pending-erase tasks
with a **server-wide cap of 500 rows, applied before this mailspace's tasks are selected
out of the result** — there is no total count and no truncation flag, so nothing in the
response says the cap was hit. On a server holding more than 500 pending account erases,
a recoverable mailbox's task can fall outside the window and its snapshot is silently
omitted from an otherwise healthy **200**. So: treat a listed snapshot as real, and treat
an empty list as "nothing found", **not** as "the mail is gone". Do not drop your own last
record of a mailbox on the strength of it.

Costs two JMAP round trips when there are snapshots to resolve — the erase tasks, then
the domain lookup that names them — and none at all when there is nothing to check.

**Codes:** **503** `purged_mailboxes_unavailable`.

#### PATCH .../purged_mailboxes/:guid — restore a purged mailbox

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `password` | String | **Yes** | A recovered account comes back with **no credentials at all**, so this sets the mailbox's new password. Blank → **400** `password_blank`. |

This is the only parameter. Because the call hands the caller a working mailbox at an
address that receives mail, every success writes an audit-log line naming the address
and the acting credential.

```json
{ "mailbox": { "id": "<guid>", "email": "old@example.com", "status": "active",
               "scheduled_deletion_at": null, "days_until_deletion": null } }
```

The response is the same shape the mailbox `DELETE` and `restore` return, so a restore
reports like any other mailbox state change. The `id` is the **new** mailbox guid, not
the snapshot guid you addressed.

**The snapshot is consumed on success** — a second `PATCH` of the same guid is **404**
`unknown_purged_mailbox`.

What comes back and what does not: quota, display name, aliases and group/list
memberships are replayed from the snapshot. A quota that no longer fits the package is
**clamped** to the package's pool rather than refused. A group or list that has since
been deleted is **skipped**, and the restore still succeeds.

**A `200` is not proof the mailbox came back whole.** The alias replay is a tolerant
full-replace: an alias whose domain no longer resolves is **silently dropped** and the
write still reports success. Group and list membership degrade the same way. Read the
mailbox back with `GET .../mailboxes/:id` and compare against what you expected before
telling anyone the recovery is complete — mail to a dropped alias simply bounces, with
nothing in this response to hint at it.

**Gate order matters.** The expiry check runs before the password check, so an expired
snapshot sent with no password answers **409** `not_recoverable`, not **400**.

**Codes:**

| Code | Status | Meaning |
|---|---|---|
| `password_blank` | **400** | No password supplied. |
| `unknown_purged_mailbox` | **404** | No such snapshot in **this** mailspace. |
| `not_recoverable` | **409** | **Terminal — the mail is gone, do not retry.** Two paths reach it: the retention window had already closed, or the pre-flight read of the mail server's pending-erase list **succeeded** and reported the server is no longer holding this account. On the second path the snapshot is consumed on the way out, so a retry answers **404** `unknown_purged_mailbox`. |
| `restore_failed` | **422** | The mail server **answered** and the restore did not happen. Covers: the address has been taken by a new mailbox since; the package's mailbox limit no longer has room; the server refused; or the attempt failed part-way. |
| `restore_unavailable` | **503** | The pre-flight read of the mail server's pending-erase list **could not be performed**, so nothing was attempted. The snapshot is untouched. This is the one failure here that can be stated to have changed nothing. |

**`restore_failed` is retryable.** The restore is idempotent — it skips straight to
reattaching when the account already exists — so a retry is the right move on anything
that looks transient. The one case that is *not* retryable is broken out into **409**
`not_recoverable` rather than sharing this code, precisely so a client does not have to
guess: when the pre-flight read succeeds and reports the mail server is **no longer
holding** the account, the snapshot is deleted and the answer is the 409.

**The three failure statuses answer three different questions**, and this endpoint is the
clearest place on the mail surface to learn the pattern: **409** means nothing can be done
(the mail is gone), **422** means the server refused and a retry may work, **503** means
the check could not be made and nothing was attempted at all.

**Second exception, and it never clears: account recovery is an Enterprise capability
upstream.** On a deployment without it the mail server refuses every attempt, and that
refusal surfaces as this same **422** `restore_failed`. Bound your retries — an
indefinite loop on this code will never succeed there. If a restore fails identically
several times with the snapshot still listed in the index, stop and escalate rather than
continuing to poll.

```bash
curl -X PATCH -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  -H "Content-Type: application/json" -d '{"password":"…"}' \
  "https://my.cloudpress.com/api/mailspace/<guid>/purged_mailboxes/<guid>"
```

---

### Archived Items (Deleted Mail)

**Base route:** `/api/mailspace/:mailspace_id/archived_items`, keyed by
**`:stalwart_id`** (`.../archived_items/:stalwart_id`) — the mail server's opaque JMAP
item id, not a guid. `restore` and `download` are member routes on it.

An item lands here when a user deletes a message; the mail server keeps it until
`archived_until` and then purges it for good.

**Requires the mail server's Enterprise tier.** There is no capability field and no
distinct error code: on a build without it, `index` answers **200** with an empty
`archived_items` array and every by-id action answers **404** `unknown_archived_item`.
"Not licensed" and "nothing archived" are deliberately indistinguishable.

That holds even though every read here is strict, and the reason is worth carrying: the
mail server answers a request for a licensed-only object with a **per-method error** —
which is an *answer*. So the licence gate degrades to the empty list and the generic 404,
while a mail server that gave **no** answer at all (unreachable, timed out, a 5xx) is a
**503** instead. Unreachable is therefore distinguishable from an empty archive.
Unlicensed is not.

**Cross-tenant safety is enforced here, and it is why the 404 is generic.** Item ids are
global handles on the mail server — the transport does not scope them — so every by-id
action re-resolves the id and checks the item's owning account against **this
mailspace's own mailboxes**, failing closed. An id belonging to another workspace is
**404** `unknown_archived_item`, the same answer an id that never existed gets, and the
same answer an id that vanished between two reads gets. It is never confirmed as
foreign.

Archived mail belonging to a mailbox that is `pending_deletion` **is** included —
those mailboxes still exist upstream and their deleted mail is still restorable.

**Item object**

```json
{ "id": "ai-42", "type": "Email", "status": "archived",
  "subject": "Invoice 4471", "from": "billing@example.com", "size": 18422,
  "received_at": "2026-08-10T07:14:00Z", "archived_at": "2026-08-12T09:00:00Z",
  "archived_until": "2026-09-11T09:00:00Z",
  "mailbox_email": "sales@example.com", "mailbox_id": "<guid>" }
```

| Field | Type | Notes |
|-------|------|-------|
| `id` | String | The opaque item id — the `:stalwart_id` segment. |
| `type` | String / null | `"Email"` in practice. Emitted so a client can tell if that ever changes. |
| `status` | String | `archived` or `requestRestore`. Defaulted to `archived` server-side, because the mail server omits the field while it holds its default — never treat it as absent. |
| `subject` | String / null | |
| `from` | String / null | |
| `size` | Integer / null | Bytes. |
| `received_at` | String (ISO 8601) / null | |
| `archived_at` | String (ISO 8601) / null | |
| `archived_until` | String (ISO 8601) / null | The permanent-deletion deadline. **Server-wide retention, not per item — it cannot be extended or shortened through this API.** |
| `mailbox_email` | String / null | The mailbox the message was deleted from. |
| `mailbox_id` | String (UUID) / null | That mailbox's guid. |

The message body, the item's blob handle and its owning account id are **not** emitted.
The message itself comes back from `download`.

#### GET .../archived_items — list restorable deleted mail

**Newest-archived first**, ordered server-side (the mail server rejects sorting on that
field, so it is done after the fetch; an unparseable timestamp sorts last).

Queried per mailbox and filtered to this mailspace's own mailboxes, so it cannot surface
another tenant's archive. One JMAP round trip per 8 mailboxes.

**Two ways this list is quietly incomplete.** Both matter if you reconcile against it:

- **Capped at 500 items per mailbox.** Beyond that the list is truncated with **nothing
  in the response** to say so.
- **An unlicensed mail server also answers `[]`**, so `archived_items: []` with a **200**
  does not distinguish "nothing archived" from "Enterprise not licensed". It does **not**
  hide "the mail server could not be asked" — that is the **503**
  `archived_items_unavailable`, and it is the only meaning of an empty list this endpoint
  rules out.

```json
{ "archived_items": [ { "id": "ai-42", "…": "…" } ] }
```

**Codes:** **503** `archived_items_unavailable`.

#### GET .../archived_items/:stalwart_id — one archived item

```json
{ "archived_item": { "id": "ai-42", "…": "…" } }
```

The same fields as the index. **The message body is not here** — use `download`.

**Codes:** **404** `unknown_archived_item`; **503** `archived_item_lookup_unavailable`
(the ownership lookup could not be performed, so the item is neither confirmed nor
denied — retriable, and it must not be read as the item being gone).

#### POST .../archived_items/:stalwart_id/restore — queue a restore

**Asynchronous with no completion signal.** The mail server has no synchronous restore:
the trigger sets the item's status and the server processes it in its own time
(sub-second in practice). The response therefore reports **`status: "restore_queued"`,
never "restored"**, and returns **200** rather than a 202.

```json
{ "status": "restore_queued",
  "archived_item": { "id": "ai-42", "status": "archived", "…": "…" } }
```

**Read the top-level `status`, not the nested one.** The `archived_item` block is the
copy captured *before* the trigger was sent, so on a **first** restore its `status` still
reads `archived` even though the request was accepted. It reads `requestRestore` only on
a second restore of the same item. A client that confirms off the nested field will
conclude a successful restore was refused.

**What to poll:** the item's own `status` reads back as `requestRestore` until the
server picks it up. When it completes, the message reappears in the mailbox **under a
new id** and leaves `GET .../archived_items` entirely — so the poll signal is the
item's disappearance from that list, and there is no id to follow it by. Watch the
list, not the item.

**Codes:**

| Code | Status | Meaning |
|---|---|---|
| `unknown_archived_item` | **404** | No such item, not yours, or it was gone by the time the restore resolved the id again — a client retrying its own timed-out restore is the realistic case. |
| `restore_failed` | **422** | The mail server **answered** and refused. Nothing was queued. |
| `archived_item_lookup_unavailable` | **503** | The ownership lookup could not be performed, so **nothing was sent**. The item is untouched. |
| `restore_unconfirmed` | **503** | **Indeterminate.** The status patch went out and its fate is unknown, so the restore may already be queued. |

**Two 503s that promise opposite things, and the distinction is the point.**
`archived_item_lookup_unavailable` means nothing was attempted; `restore_unconfirmed`
means something was attempted and the outcome is unknown. On the second, re-read the item
(or the index) before retrying rather than assuming the restore failed — and note this is
also the opposite promise from `restore_unavailable` on the purged-mailbox path, which
means nothing happened. Do not generalise across the two surfaces from the word
"unavailable".

#### DELETE .../archived_items/:stalwart_id — erase permanently

**Irreversible.** The archived message goes with it and there is no second archive
behind this one. The erase is audit-logged with the acting credential **after** it
succeeds.

```json
{ "deleted": true, "id": "ai-42", "subject": "Invoice 4471" }
```

`subject` is read from the item before the erase and is `null` when it carried none.

**Codes:**

| Code | Status | Meaning |
|---|---|---|
| `unknown_archived_item` | **404** | No such item, or not yours. |
| `delete_failed` | **422** | The mail server **answered** and refused. Nothing was erased. |
| `archived_item_lookup_unavailable` | **503** | The ownership lookup could not be performed, so **nothing was sent**. The item is untouched. |
| `delete_unconfirmed` | **503** | **Indeterminate**, and this erase is irreversible: the item may already be gone. |

**On `delete_unconfirmed`, re-read the item before doing anything else.** It is the one
place on this surface where an unknown outcome is unrecoverable, so treating it as "the
delete failed" is the worst of the three available guesses. `GET` the item: a **404**
means it went through.

#### GET .../archived_items/:stalwart_id/download — the original message

**This endpoint does not return JSON on success.** It responds **200** with the raw
RFC822 bytes of the original message:

- `Content-Type: message/rfc822`
- `Content-Disposition: attachment`, filename `<name>.eml`

The body is the message itself, byte-identical to what was delivered — not base64, not
wrapped in an envelope. The download is proxied through the API rather than handed over
as a mail-server URL.

The filename stem is derived from the subject and sanitised: characters outside word
characters, spaces, hyphens and dots collapse to underscores, runs of underscores are
squeezed, a leading dot is dropped, and the stem is capped at **80** characters. A blank
subject — or one that sanitises away entirely — falls back to the item id. **It never
varies with `Accept-Language`**, unlike the equivalent download in the web portal.

Failures **are** JSON, in the usual envelope:

| Code | Status | Meaning |
|---|---|---|
| `unknown_archived_item` | **404** | No such item in this workspace. |
| `download_unavailable` | **404** *or* **503** | The message could not be delivered. **The status is the difference, and this is the one code on the mail surface where you must read it:** **404** means the mail server answered that the blob is gone — terminal, stop. **503** means the read failed for any other reason (unreachable, or the platform's own credential refused) — the message may still be there, so retry. One code, because it is one fact about one resource; the status carries what to do next. |
| `archived_item_lookup_unavailable` | **503** | The ownership lookup could not be performed. |

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  -o message.eml \
  "https://my.cloudpress.com/api/mailspace/<guid>/archived_items/ai-42/download"
```
