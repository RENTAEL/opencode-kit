# Mailspace Addresses, Groups & Delivery

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

Every endpoint here is nested under `/api/mailspace/:mailspace_id/…`, where
`:mailspace_id` is the mailspace guid (a UUID), and all of them run the same six
gates in this order before the action does anything:

1. **`503`** `stalwart_unavailable` — mail server not configured.
2. **`404`** with an **empty body** — the guid is unknown *or* not reachable by this
   credential. The two are deliberately indistinguishable.
3. **`403`** `not_authorized` — decided on the HTTP verb: `GET`/`HEAD` always pass,
   anything else needs edit permission on the mailspace's own workspace.
4. **`403`** `mailspace_suspended` — staff block or dunning hold. **Not verb-gated:
   reads are refused too.**
5. **`403`** `pending_delete` — soft-deleted mailspace; verb-gated like #3, so reads
   stay available for the whole retention window.
6. **`409`** `not_provisioned` — the mailspace is not in the mail server yet
   ("This mailspace is not provisioned yet. Complete domain verification first.").

Per-endpoint sections below list only the codes that are **specific to that
endpoint**; assume the six above everywhere. The envelope is
`{"errors": ["…"], "code": "…"}`, and **error messages are always English
regardless of `Accept-Language`** — branch on `code`, never on the message text.

**OAuth scopes.** Reads take `mailspace:read`, mutations take `mailspace:write`, and
every action in this file declares one, so all of them are reachable with an OAuth
token. The exact split:

| Resource | `mailspace:read` | `mailspace:write` |
|---|---|---|
| Aliases | `index` | `create`, `destroy` |
| Groups | `index`, `show` | `create`, `update`, `destroy` |
| Mailing lists | `index`, `show` | `create`, `update`, `destroy` |
| Masked emails | `index` | `create`, `destroy` |
| Delivery logs | `show` | — (no mutating action exists) |

**`X-Auth-Account` is not required here.** Sent, it narrows the mailspace lookup to
that workspace's mailspaces; omitted on a user/session/OAuth credential, the lookup
spans every mailspace that credential's user can reach.

**Nothing in this file paginates.** The four index endpoints —
`GET .../aliases`, `GET .../groups`, `GET .../mailing_lists`,
`GET .../masked_emails` — return the full set in one array, with no `page`,
no `per_page`, and no pagination metadata of any kind in the body. `GET .../logs`
is a single fixed-size read (see that section). The upstream caps that *do* bound
these lists are documented per endpoint; they are ceilings, not pages, and there is
no way to reach past them.

The `/api` rate limit (600 requests per 10 minutes) applies to all of it.

---

### Aliases

**Base route:** `/api/mailspace/:mailspace_id/aliases`.

An alias is **keyed by its address, not by an id** — upstream it is not a standalone
object at all but an entry in the alias field of a mailbox, group or mailing-list
principal, so there is nothing else to key on. The route segment is constrained to
"anything except `/`", which is what lets a dotted, `@`-bearing address through.

#### GET /api/mailspace/:mailspace_id/aliases — list every alias

Scope `mailspace:read`. Joins mailboxes, groups and mailing lists into one flat list,
sorted ascending by alias address.

Query params: `q` — optional, case-insensitive substring, matched against the alias
address **and** the target's primary address. Leading/trailing whitespace is stripped
and a blank value is ignored.

```json
{
  "aliases": [
    { "address": "sales@example.com", "target_email": "team@example.com",
      "target_name": "Sales team", "target_type": "group",
      "target_id": "<stalwart-id>" }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `address` | String | The alias, lowercased. |
| `target_email` | String | The **primary** address it delivers to, as the mail server stores it (not lowercased). Each row is built from its owning principal's primary, so this is never itself an alias. |
| `target_name` | String / null | The target's description, falling back to its name (the address local part). `null` only when both are blank. |
| `target_type` | String | `mailbox`, `group`, or `list`. |
| `target_id` | String | The target's mail-server principal id — an opaque string. |

**`target_id` is addressable for two of the three target types only.** For
`target_type` `group` or `list` it is exactly the `:stalwart_id` segment those
endpoints take. For `mailbox` it is **not** usable: mailbox endpoints are keyed by
the CloudPress-side guid, not by the mail-server principal id, so a `target_id` from
a `mailbox` row will not resolve there.

**An empty list is authoritative.** The three principal reads behind it — mailboxes,
groups, mailing lists — are strict and share one fate: if any of them cannot be read the
endpoint answers **`503`** `aliases_unavailable`, never a **`200`** with the rows it did
manage to collect. So `[]` here means the mail server was asked and this mailspace has no
aliases.

`aliases_unavailable` covers **every** failure of those reads, including the platform's
own mail-server credential being refused — on a read there is no useful difference
between "no answer" and "an answer about our request rather than your aliases".

**Ceiling.** Each principal read is capped at 500 upstream rows. Mailboxes and groups
come out of the **same** capped query and are separated afterwards by type, so the 500
is shared between them: a mailspace with 500+ mailboxes can return no group aliases at
all. Mailing lists have their own 500. **The cap is the one way this list is still
quietly short** — truncation is silent, unlike a failed read.

**Codes:** **`503`** `aliases_unavailable`.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" -H "X-Auth-Account: $ACCOUNT_ID" \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/aliases?q=sales"
```

#### POST /api/mailspace/:mailspace_id/aliases — point an alias at a principal

Scope `mailspace:write`. Returns **`201`**.

```json
{ "address": "sales", "domain": "example.com", "target_email": "team@example.com" }
```

| Param | Type | Required | Notes |
|---|---|---|---|
| `address` | String | Yes | The alias address. A bare local part (no `@`) is qualified with `domain`, or with the mailspace's own primary domain when `domain` is absent. An address that already carries an `@` is passed through untouched. |
| `domain` | String | No | Used **only** when `address` has no `@`. Ignored otherwise. |
| `target_email` | String | Yes | The **primary** address of a mailbox, group or mailing list in this mailspace. An alias cannot point at another alias, so only primaries resolve. |

Three things are validated, and all three collapse into one code:

- the alias's domain must be one of this mailspace's own domains;
- the address must be unused across the **whole** mailspace address namespace —
  mailbox primaries, group addresses, mailing-list addresses, and existing aliases of
  any of those three;
- `target_email` must resolve to a principal in this mailspace.

**Response — `201`.** Note this is **not** the index row shape: it echoes the pair
that was established and nothing else, both values lowercased.

```json
{ "alias": { "address": "sales@example.com", "target_email": "team@example.com" } }
```

**Codes:** **`400`** `address_blank`, **`400`** `target_blank`, **`422`**
`invalid_alias`, **`503`** `aliases_unavailable`.

**`invalid_alias` means the mail server answered and one of the three checks genuinely
failed.** All three are live reads, and a read that could not be made answers **`503`**
`aliases_unavailable` instead — so this code never stands in for "we could not ask". That
matters most on the first check: an unreachable mail server used to make the domain gate
report *"`example.com` isn't one of this mailspace's domains. Add the domain first"*, a
confident and actionable-looking claim about the customer's own configuration that the
platform was in no position to make.

**`errors[0]` is curated text, not upstream text.** On a refusal of the write itself the
message is a fixed sentence rather than the mail server's own string, so there is nothing
in it to parse. Branch on `code`; display `errors[0]` if you like.

**`503` `aliases_unavailable` on this endpoint is indeterminate**, because it covers the
write leg as well as the three pre-flight reads: the alias may have been created. The
write is a read-modify-write of the target's whole alias set, so repeating it is safe —
but re-read `GET .../aliases` rather than reporting failure to a human.

The write is a read-modify-write of the target's full alias set, so the target keeps
its existing aliases.

#### DELETE /api/mailspace/:mailspace_id/aliases/:address — remove one alias

Scope `mailspace:write`. Returns **`200`**.

`:address` is the alias itself, **sent literally in the path**. Dots and `@` are legal
in the segment and need no escaping, and there is no trailing-format split to worry
about — the whole remainder of the segment is taken as the address. An alias address
cannot contain `/`, so it is always exactly one path component.

```bash
curl -X DELETE -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/aliases/sales@example.com"
```

```json
{ "deleted": true, "address": "sales@example.com", "target_email": "team@example.com" }
```

`address` is lowercased; `target_email` is the owning principal's primary address.
The owning principal and its other aliases are left alone — only this one entry goes.

**Codes:** **`404`** `unknown_alias`, **`422`** `alias_remove_failed`, **`503`**
`aliases_unavailable`.

**`404` `unknown_alias` is authoritative.** The owner is located through a strict
tenant-scoped read *before* the write is attempted, so it means the mail server was asked
and nothing in this mailspace carries that address. A lookup that could not be performed
answers **`503`** `aliases_unavailable` instead, and no write is attempted on either path
— a `404` is a terminal answer to a question, and it must not be given for a question
that was never asked.

**`503` here is indeterminate on the write leg**, the same as on `POST`: it also covers a
removal whose outcome is unknown. Removing an alias that is already gone is a no-op, so a
retry is safe.

The owner lookup is deliberately done first so that an address which is not an alias
*in this mailspace* answers `404` rather than a service-level `422` — the three failure
shapes stay distinct: `404` nothing holds it, `422` the server refused the write, `503`
we could not ask.

`errors[0]` on the `422` is curated text, not the mail server's own string — as on `POST`.

---

### Groups

**Base route:** `/api/mailspace/:mailspace_id/groups`, keyed by `:stalwart_id`.

**A group has no CloudPress-side record.** There is no guid — the only handle is the
mail server's own principal id, which is what `id` in every response body carries.
Get it from `GET .../groups`, from a create response, or from an alias row's
`target_id`.

**Tenant ownership is checked on every by-id action.** `show`, `update` and `destroy`
resolve the id and confirm the principal belongs to this mailspace before touching it;
anything else answers **`404`** `unknown_group` — the identical answer an id that does
not exist gets, so the endpoint cannot be used to probe ids elsewhere on the mail
server. That check fails closed: a read failure on the lookup is also a `404`.

A group may contain **any address that resolves to a principal in this mailspace** —
the pre-write guard rejects a member only when the address does not resolve at all, and
it does **not** filter by kind. In practice that means mailboxes, but another group's
address resolves too and is written rather than refused, so `members` can hand you back
an address that is not a mailbox. For an address outside this mailspace, use a mailing
list.

#### GET /api/mailspace/:mailspace_id/groups — list groups

Scope `mailspace:read`.

Query params: `q` — optional, case-insensitive substring, matched against the group's
**primary address** and its **`description`**. Aliases are not searched.

```json
{
  "groups": [
    { "id": "<stalwart-id>", "name": "sales", "email": "sales@example.com",
      "aliases": ["sales-team@example.com"], "description": "Sales team",
      "member_count": 4 }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | String | Mail-server principal id — an opaque string, and the `:stalwart_id` segment. |
| `name` | String | The address local part as the mail server stores it. Not editable through this API. |
| `email` | String | Primary address. |
| `aliases` | `Array<String>` | Additional addresses; `[]` when there are none. |
| `description` | String / null | The display name the mail server shows. |
| `member_count` | Integer | Never `null` — a group with no members is `0`. |

**The index carries no `members` key.** Only the count. Use the show endpoint for the
address list.

**Codes: two distinct `503`s, and which one you get says which read failed.** Both are
retryable, and both exist so the endpoint never reports a confident lie.

| Code | Meaning |
|---|---|
| `groups_unavailable` | The **group list** could not be read, so nothing about this mailspace's groups is known. This is what a full mail-server outage answers. Never an empty `groups` array instead. |
| `group_members_unavailable` | The groups came back but the member **tally** did not — a partial failure, and the only case left for this code here. The endpoint refuses to report `member_count: 0` for every group when it could not ask. |

Each guard covers its own read alone: a failure anywhere else in the action is a genuine
`500`.

**Ceiling.** The group list and the member tally are two separate capped reads, each
bounded at 500 upstream rows, and both draw from the same account/group population.
A mailspace with more than 500 accounts and groups combined can therefore see groups
missing from the list *and* `member_count` under-reported on the groups it does see.

#### GET /api/mailspace/:mailspace_id/groups/:stalwart_id — one group with members

Scope `mailspace:read`.

```json
{
  "group": { "id": "<stalwart-id>", "name": "sales", "email": "sales@example.com",
             "aliases": ["sales-team@example.com"], "description": "Sales team",
             "members": ["bob@example.com", "ann@example.com"], "member_count": 2 }
}
```

The index fields plus:

| Field | Type | Notes |
|---|---|---|
| `members` | `Array<String>` | Addresses that resolve in this mailspace — normally mailboxes, but not guaranteed to be (see above). |
| `member_count` | Integer | Here this is `members.length`. On the index it comes from a separate tenant-wide tally, so the two are computed differently and can disagree when the index's cap bites. |

**Codes:** **`404`** `unknown_group`, **`503`** `group_members_unavailable`.

**The `404` is the one read failure on this surface that is still reported as "not
found".** Unlike the index, the by-id principal lookup that resolves `:stalwart_id` is
tolerant: a mail server that cannot be read yields nothing and this endpoint answers
`404` `unknown_group`, indistinguishable from a group that does not exist or belongs to
another mailspace. Do not read a single `404` here as proof the group is gone — the index
is the authoritative check.

The member read **on this endpoint** is strict: `[]` in a `200` body means "we asked,
and the group is empty". It never stands in for a failed read, because this endpoint
invites a read-modify-write and a bogus `[]` PATCHed back would evict every member for
real. **`PATCH` is strict too — but `POST` is not.** See the create endpoint below.

#### POST /api/mailspace/:mailspace_id/groups — create a group

Scope `mailspace:write`. Returns **`201`** with the same body shape as show — but
**not with show's strictness.** The create's member read-back is **tolerant**: if the
mail server blips after the group has already been created, the response is still a
**`201`**, with a real non-null `id` and `members: []` / `member_count: 0` for a group
that genuinely has members. **Do not reconcile off the `201` body, and never `PATCH` it
straight back** — an explicit `members: []` is honoured and would evict every member for
real. Re-read with `GET .../groups/:stalwart_id`, which answers **`503`** rather than
lying, and treat that as the authoritative membership.

```json
{ "name": "Sales team", "email": "sales", "domain": "example.com",
  "description": "Inbound sales", "aliases": ["sales-team@example.com"],
  "members": ["bob@example.com"] }
```

| Param | Type | Required | Notes |
|---|---|---|---|
| `name` | String | Yes | **Not the address, and not the response's `name`.** See below. |
| `email` | String | Yes | The group's address. A bare local part is qualified with `domain`, else with the mailspace's primary domain. |
| `domain` | String | No | Used only when `email` has no `@`. |
| `description` | String | No | |
| `aliases` | `Array<String>` | No | Blank entries are discarded before the write. |
| `members` | `Array<String>` | No | Mailboxes in this mailspace only. Blank entries discarded. |

**`name` is the description fallback, not the display name field and not the
address.** The stored display name is `description` if present, otherwise `name`. The
address local part comes from `email`. So `POST {name: "Sales team", email: "sales@…"}`
comes back as `"name": "sales"` with `"description": "Sales team"` — the value you sent
as `name` reappears under `description`, and the `name` you get back is derived from
the address. Send `description` explicitly if you care which is which.

**A member that is not a mailbox here fails the whole create.** It is not silently
dropped — the write is refused before it is attempted, because the mail server would
otherwise accept the create and discard the unresolvable member without saying so.

**Codes:** **`400`** `email_blank`, **`400`** `name_blank`, **`422`**
`group_create_failed`. That one code covers four distinct situations: a domain that is
not in this mailspace; an address already in use anywhere in the mailspace namespace;
a submitted member that is not a mailbox here; and a mail-server read failure during
the pre-write member check ("We couldn't verify the selected members just now"). The
message distinguishes them; the code does not.

**The `201` body is a read-back and can be degenerate.** The upstream create returns no
id, so the new group is read back from the principal list to supply one. If that
read-back misses, the response is **still `201`** but carries `"id": null`,
`"aliases": []`, `"members": []` and `"member_count": 0` — even though the aliases and
members were written. Do not treat that body as state; if `id` is `null`, re-read
`GET .../groups` for the real row.

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Sales team","email":"sales@example.com","members":["bob@example.com"]}' \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/groups"
```

#### PATCH /api/mailspace/:mailspace_id/groups/:stalwart_id — update a group

Scope `mailspace:write`. Returns **`200`** with the same body as show. `PUT` routes to
the same action.

**This is a merge keyed on key presence, and omitting the member list is safe.**

| Param | Type | Required | Notes |
|---|---|---|---|
| `description` | String | No | Omitted → unchanged. Explicit `""` → **cleared**. This is the display name. |
| `aliases` | `Array<String>` | No | Omitted → the current alias set is re-sent unchanged. Explicit `[]` → all aliases cleared. |
| `members` | `Array<String>` | No | Omitted → **membership is not touched at all**: it is not read and not written. Explicit `[]` → the group is emptied. A supplied list **replaces** the membership. |
| `name` | String | No | Accepted and **ignored** — the address local part is immutable. |

There is no `email` parameter: a group's address cannot change.

**A member list is not required on update.** An omitted `members` key is passed through
as "not supplied" and the membership diff is skipped entirely — no read, no write.
Sending the *current* list back is not necessary and is worse than omitting it: reading
the list to re-send it is exactly the pattern that used to evict every member when the
read blipped.

**Blank entries are stripped before the presence test is acted on.** `{"members": [""]}`
becomes an explicit empty list and **empties the group**; `{"aliases": [""]}` clears
every alias. Send no key at all to mean "leave it alone".

Two post-write behaviours to plan for:

- **A `description`-only PATCH can still answer `503`.** The action performs a strict
  post-write member read to build the response body, and if *that* read fails you get
  **`503`** `group_members_unavailable` — with the update **already applied**. This
  status does not mean the write was rejected. Re-read the group rather than retrying
  the PATCH.
- **A failed principal read-back still answers `200`.** The response is then assembled
  from the pre-write principal with the values just written applied (`description`,
  `aliases`, and the address list derived from them) — not from nulls. The write
  succeeded, so reporting failure would be wrong.

**The update is not atomic.** The description/alias patch is applied first, then the
membership diff as per-address changes. A failure partway through surfaces as **`422`**
`group_update_failed` after the earlier part has already landed — re-read the group
instead of assuming nothing changed.

**Codes:** **`404`** `unknown_group`, **`422`** `group_update_failed` (service
rejection, e.g. a submitted member that is not a mailbox here), **`503`**
`group_members_unavailable`.

#### DELETE /api/mailspace/:mailspace_id/groups/:stalwart_id — delete a group

Scope `mailspace:write`. Returns **`200`**.

```json
{ "deleted": true, "id": "<stalwart-id>", "email": "sales@example.com" }
```

The member mailboxes are untouched — only the group principal goes.

**Codes:** **`404`** `unknown_group`, **`422`** `group_delete_failed`.

---

### Mailing Lists

**Base route:** `/api/mailspace/:mailspace_id/mailing_lists`, keyed by
`:stalwart_id`.

Like a group, **a mailing list has no CloudPress-side record** — the mail server's
principal id is the only handle, and the same fail-closed tenant-ownership check runs
on `show`, `update` and `destroy`, answering **`404`** `unknown_mailing_list` for
anything outside this mailspace.

**The difference from a group:** a list's recipients are a plain address map upstream,
so a list **may carry addresses this mailspace does not host**. There is no membership
validation, and no `group_members_unavailable` analogue — recipients arrive with the
principal in the same read.

#### GET /api/mailspace/:mailspace_id/mailing_lists — list mailing lists

Scope `mailspace:read`.

Query params: `q` — optional, case-insensitive substring, matched against the list's
**primary address** and its **`description`**. Same two fields as the groups index, and
the same predicate.

```json
{
  "mailing_lists": [
    { "id": "<stalwart-id>", "name": "announce", "email": "announce@example.com",
      "aliases": ["news@example.com"], "description": "Announcements",
      "members": ["bob@example.com", "outsider@elsewhere.example"],
      "member_count": 2 }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | String | Mail-server principal id — an opaque string, and the `:stalwart_id` segment. |
| `name` | String | The address local part as the mail server stores it. Not editable. |
| `email` | String | Primary address. |
| `aliases` | `Array<String>` | `[]` when there are none. |
| `description` | String / null | The display name. |
| `members` | `Array<String>` | Recipient addresses. May include addresses outside this mailspace. |
| `member_count` | Integer | `members.length`. |

**Unlike the groups index, this index carries the full `members` list** — there is no
separate show call needed to see recipients.

**Ceiling.** One capped read, bounded at 500 lists. Truncation at the cap is silent — it
is the one way this list is still quietly short.

**Codes:** **`503`** `mailing_lists_unavailable` — the list read could not be performed.
The read is strict, so an empty `mailing_lists` array in a `200` is authoritative and
never stands in for a failed read.

#### GET /api/mailspace/:mailspace_id/mailing_lists/:stalwart_id — one mailing list

Scope `mailspace:read`. Returns `{"mailing_list": { … }}` with **exactly the index row
fields** — there is no extra field on show, unlike groups.

**Codes:** **`404`** `unknown_mailing_list`. As on the groups show endpoint, the by-id
principal lookup behind it is **tolerant**, so this `404` also covers "the mail server
could not be read" — it is the exception to this file's otherwise strict reads, and the
index is the authoritative check.

#### POST /api/mailspace/:mailspace_id/mailing_lists — create a mailing list

Scope `mailspace:write`. Returns **`201`** with the same body as show.

| Param | Type | Required | Notes |
|---|---|---|---|
| `name` | String | Yes | The description fallback, not the address and not the response's `name` — the same behaviour as `POST .../groups`, described under **Groups** above. |
| `email` | String | Yes | The list's address. A bare local part is qualified with `domain`, else the mailspace's primary domain. |
| `domain` | String | No | Used only when `email` has no `@`. |
| `description` | String | No | |
| `aliases` | `Array<String>` | No | Blank entries discarded. |
| `members` | `Array<String>` | No | Recipients. **Outside addresses are allowed** and are not validated. Blank entries discarded. |

**Codes:** **`400`** `email_blank`, **`400`** `name_blank`, **`422`**
`mailing_list_create_failed` (an address whose domain is not in this mailspace, or one
already in use in the mailspace namespace).

**The `201` body is a read-back and can be degenerate**, for the same reason as groups.
If it misses you still get **`201`** with `"id": null` and `"aliases": []`, but here
`members` and `member_count` do reflect the recipients you submitted. An `id` of `null`
means re-read the index to get the real handle.

#### PATCH /api/mailspace/:mailspace_id/mailing_lists/:stalwart_id — update a list

Scope `mailspace:write`. Returns **`200`** with the same body as show. `PUT` routes to
the same action.

Merge semantics are identical to a group's:

| Param | Type | Required | Notes |
|---|---|---|---|
| `description` | String | No | Omitted → unchanged. Explicit `""` → **cleared**. |
| `aliases` | `Array<String>` | No | Omitted → current set re-sent. Explicit `[]` → cleared. |
| `members` | `Array<String>` | No | Omitted → **recipients are not touched and not even read**. Explicit `[]` → emptied. A supplied list **replaces** the recipients. |
| `name` | String | No | Accepted and **ignored**. |

**A recipient list is not required on update.** Omit `members` and the recipient sync
is skipped entirely. As with groups, blank-only arrays collapse to explicit empties:
`{"members": [""]}` empties the list.

**Unlike a group PATCH, this one performs no strict post-write member read**, so it
never answers `group_members_unavailable`. If the read-back cannot be performed you
still get **`200`**, assembled from the pre-write principal with the written
`description` and `aliases` applied; when `members` was omitted the response repeats
the pre-write recipients rather than `[]`.

**The update is not atomic, and the recipient half is per-address.** Recipients cannot
be bulk-replaced upstream, so a supplied `members` is applied as individual
subscribe/unsubscribe calls after the description and alias patch has already landed.
A failure partway through answers **`422`** `mailing_list_update_failed` with part of
the change applied — re-read the list.

**Codes:** **`404`** `unknown_mailing_list`, **`422`** `mailing_list_update_failed`.

#### DELETE /api/mailspace/:mailspace_id/mailing_lists/:stalwart_id — delete a list

Scope `mailspace:write`. Returns **`200`**.

```json
{ "deleted": true, "id": "<stalwart-id>", "email": "announce@example.com" }
```

The recipients' own mailboxes are untouched — only the list principal goes.

**Codes:** **`404`** `unknown_mailing_list`, **`422`** `mailing_list_delete_failed`.

---

### Masked Emails

**Base route:** `/api/mailspace/:mailspace_id/masked_emails`, keyed by `:guid` — the
**CloudPress-side record's UUID**, not the mail-server id. Only three routes exist:
`index`, `create`, `destroy`. There is **no show and no update**.

**What the Enterprise gate looks like from the client side.** Masked addresses are a
mail-server Enterprise object. There is no capability field in any response body, no
capability probe, and no dedicated error code. What you observe on a build that does
not license them:

- `GET .../masked_emails` → **`200`** with `{"masked_emails": []}`.
- `POST .../masked_emails` → **`422`** `masked_email_create_failed`, with the mail
  server's own rejection text in `errors[0]`.

So on the read, "not licensed" and "none created" are **indistinguishable** — an empty
array proves neither. If a client must know, attempt a create and read the code.

#### GET /api/mailspace/:mailspace_id/masked_emails — list masked addresses

Scope `mailspace:read`. **No query parameters** — no `q`, no filters.

Rows are the live mail-server objects joined to this mailspace's CloudPress records by
mail-server id. Exactly two kinds of row are dropped: a live address with no matching
CloudPress record (it is not this mailspace's), and a CloudPress record whose
mail-server object is gone.

```json
{
  "masked_emails": [
    { "id": "<guid>",
      "stalwart_id": "<stalwart-id>",
      "email": "a1b2c3@example.com",
      "description": "newsletter",
      "enabled": true,
      "for_domain": "news.example",
      "url": "https://news.example",
      "created_by": "signup-form",
      "created_at": "2026-08-01T09:00:00Z",
      "expires_at": null }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | String (UUID) | The CloudPress record guid — the `:guid` path segment. |
| `stalwart_id` | String | The mail server's own id, for correlation only. Not addressable through this API. |
| `email` | String | The masked address. **Assigned by the mail server**, never chosen by the client. |
| `description` | String / null | |
| `enabled` | Boolean | Never `null`. Anything other than an explicit upstream `false` renders `true`. |
| `for_domain` | String / null | The site the address was minted for. |
| `url` | String / null | |
| `created_by` | String / null | Free-text provenance note. |
| `created_at` | String (ISO 8601) / null | Server-set. |
| `expires_at` | String (ISO 8601) / null | Server-set, read-only upstream, usually `null`. |

Every key above is **always present**; a missing value is `null`, never an absent key.

**Ceiling, and it is not per-mailspace.** The upstream query is **server-wide** — it
filters by mail account, not by mailspace — and is capped at 2000 rows *before* this
mailspace's rows are selected out of it. On a mail server holding more masked addresses
than that, rows belonging to this mailspace can be missing from the response, and
nothing in the payload signals the truncation.

**Codes:** the inherited gates only.

#### POST /api/mailspace/:mailspace_id/masked_emails — mint a masked address

Scope `mailspace:write`. Returns **`201`** with one row under `masked_email`.

```json
{ "target_mailbox_email": "bob@example.com", "description": "newsletter",
  "for_domain": "news.example", "url": "https://news.example", "created_by": "signup-form" }
```

| Param | Type | Required | Notes |
|---|---|---|---|
| `target_mailbox_email` | String | Yes | A mailbox in **this** mailspace that the address forwards to. Resolved through this mailspace's own domains, so an address outside it is rejected. |
| `description` | String | No | |
| `enabled` | Boolean | No | Defaults to `true` when the key is **absent**. When present the value is cast, so `false`, `"false"`, `"0"` and `0` all read as `false`. |
| `for_domain` | String | No | The site the address is used on. |
| `url` | String | No | |
| `created_by` | String | No | |

You cannot pick the address — the mail server assigns it and the response carries it.

**Codes:** **`400`** `target_mailbox_email_blank`, **`422`**
`masked_email_create_failed` — the latter covering three situations: no such mailbox in
this mailspace, the mail server refusing the write, and the mail server not licensing
masked addresses at all.

**The `201` body is a read-back.** It re-reads the live list so the response can carry
the server-set fields. If that read-back misses, the response is still **`201`** but
assembled from what was submitted, which means **`created_at` and `expires_at` come
back `null`** even though the address exists and works. A `null` `created_at` is not a
failure signal.

```bash
curl -X POST -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_mailbox_email":"bob@example.com","description":"newsletter"}' \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/masked_emails"
```

#### DELETE /api/mailspace/:mailspace_id/masked_emails/:guid — delete an address

Scope `mailspace:write`. Returns **`200`**. Removes the mail-server object and the
CloudPress record. Mail already delivered through the address is untouched — only the
forwarding stops.

```json
{ "deleted": true, "id": "<guid>", "email": "a1b2c3@example.com" }
```

**Codes:** **`404`** `unknown_masked_email` (no such record in this mailspace — a guid
belonging to another workspace gets the identical answer, so the endpoint cannot
confirm that another workspace's guid exists), **`422`**
`masked_email_delete_failed`.

**This is not idempotent-`200`.** The lookup is on the CloudPress record, which the
successful delete removes, so repeating the call after a timeout that actually
succeeded answers **`404`** `unknown_masked_email` — treat that as "already gone", not
as an error.

---

### Delivery Logs

`GET /api/mailspace/:mailspace_id/logs` — scope `mailspace:read`. One route, one
action, **`200`**. There is no collection route, no id segment, and no mutating
action on this resource.

**It accepts no query parameters at all.** The action reads none: there is no time
range, no cursor or offset, no `q`, no direction filter, and no `limit`. Each dataset
is capped at the **100 most recent** entries by the upstream reader, and that cap is
not adjustable from the request.

Read-only and entirely live — no CloudPress table backs any of it.

#### Four separate keys, and the separation is the contract

| Key | Type | Upstream source | Availability |
|---|---|---|---|
| `incoming` | `Array<Object>` (trace shape) | delivery traces | **Stalwart Enterprise only** (`x:Trace`) |
| `outgoing` | `Array<Object>` (trace shape) | delivery traces | **Stalwart Enterprise only** (`x:Trace`) |
| `queue` | `Array<Object>` (message shape) | the outbound queue (`x:QueuedMessage`) | every build |
| `issues` | `Array<Object>` (message shape) | union: permanent failures from traces + still-retrying entries from the queue | partially degraded without the trace source |

The datasets are **not merged**, deliberately, because their availability differs and
merging would destroy the one signal a client has. On a build without the trace source
the trace reader degrades to empty, so:

- `incoming` and `outgoing` are `[]` **while `queue` still carries data** → tracing is
  not available on this deployment.
- all four empty → no mail activity (or an unreachable mail server — see below).

Merged into one list those two states would be indistinguishable, and "Enterprise not
licensed" would read as "no mail problems".

**`issues` degrades by half, not entirely.** Its permanent-failure entries
(`source: "trace"` — terminal bounces) come from the trace source and vanish without
it; its still-retrying entries (`source: "queue"`) come from the queue and survive.
The `source` field on each row tells you which half you are looking at.

**Internal mail is listed twice, on purpose.** A message from one mailbox in this
mailspace to another drains through the local queue and so classifies as incoming, but
it is genuinely both directions — so **the same row appears under both `incoming` and
`outgoing`**, carrying `internal: true`. Do not sum the two arrays to count messages,
and de-duplicate on `id` if you merge them — but see the `id` caveat in the field table
below before keying on it.

**Degradation is silent.** An unreachable or erroring mail server yields empty arrays
and a **`200`**, not a `5xx` — the readers swallow and log. Empty is not proof of a
quiet mailspace.

**Cost.** One request issues several upstream round trips: traces and the queue are
each queried once per domain in the mailspace, because neither upstream object carries
a tenant stamp. The `/api` rate limit of 600 requests per 10 minutes applies — poll
this on a human timescale, not in a loop.

**Codes:** the inherited gates only.

```bash
curl -H "Authorization: Bearer $CLOUDPRESS_TOKEN" \
  "https://my.cloudpress.com/api/mailspace/$MAILSPACE_ID/logs"
```

#### Trace shape — `incoming` and `outgoing`

```json
{
  "incoming": [
    { "id": "<trace-id>", "timestamp": "2026-08-01T09:00:00Z",
      "from": "sender@elsewhere.example", "to": "bob@example.com",
      "subject": "Quarterly report", "size": 4096,
      "direction": "incoming", "internal": false, "status": "delivered",
      "events": [ { "name": "delivery.dsn-success", "timestamp": "2026-08-01T09:00:01Z",
                    "key_values": [ { "key": "hostname", "value": "mx.example.com" } ] } ] }
  ],
  "outgoing": [], "queue": [], "issues": []
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | String \| `null` | The upstream trace id — an opaque string, passed through unguarded. **It can be `null`**: a trace that arrives without an id renders as `null` here. Guard for that before using it as a merge key, or several unrelated traces collapse into one bucket. (The `id` on `queue` and `issues` rows *is* guaranteed non-null — that guarantee does not extend to these two arrays.) |
| `timestamp` | String | |
| `from` | String | Envelope sender. |
| `to` | String | Recipients as one comma-joined string, **scrubbed** — see below. |
| `subject` | String | |
| `size` | Integer | |
| `direction` | String | `incoming` or `outgoing`. Derived from the queue the delivery attempt drained from; when no queue name is present, a message-ingest event means incoming and anything else outgoing. |
| `internal` | Boolean | Never `null`. `true` only for mailbox-to-mailbox mail inside this mailspace. A bounce notice delivered locally is *not* internal — a null return path carries no sender domain. |
| `status` | String | `delivered`, `bounced`, `failed`, `retrying`, or `sending`. Derived from `events`; a trace with no events reads `sending`. |
| `events` | `Array<Object>` | The SMTP log. |

**`to` is scrubbed, and so are recipient-bearing event values.** One upstream SMTP
transaction addressed to two mailspaces produces one shared trace, so co-recipients
that are not yours are removed: when the sender is **not** on one of this mailspace's
domains, only recipients on this mailspace's own domains survive. On mail this
mailspace sent, every recipient is shown, external ones included.

`status` is classified from the event names by substring, in this order — the names
themselves are the mail server's and vary by version, so match on these:

1. a name containing `perm-fail` or `message-rejected` → `bounced` if a name containing
   `dsn-queued` is also present, otherwise `failed`
2. else a name containing `temp-fail` → `retrying`
3. else a name containing `dsn-success`, starting with `message-ingest`, or containing
   `completed` → `delivered`
4. else → `sending`

#### Event shape — the `events` array on traces and on trace-derived issues

| Field | Type | Notes |
|---|---|---|
| `name` | String | The mail server's dot-namespaced event name, e.g. `delivery.dsn-success`. |
| `timestamp` | String | |
| `key_values` | `Array<Object>` | `[{ "key": …, "value": … }]`. A **list, not an object** — the same key can legitimately repeat within one event, and an object would silently drop all but the last. |

**`key_values` is filtered, not a faithful copy of the upstream event.** Internal
mail-server identifiers are stripped: `spanId`, `queueId`, `accountId`, `documentId`,
`mailboxId`, `blobId`, `changeId`, `messageId`, `total`. Recipient-bearing keys — `to`,
`rcptTo`, `rcpt`, `recipients`, `cc`, `bcc` — are scrubbed by the same rule as the
trace's `to`, and a key whose value scrubs down to nothing is **dropped from the list
entirely**. Multi-valued upstream values are flattened to a scalar, joined with `", "`
when there is more than one.

#### Message shape — `queue` and `issues`

Both arrays render through the same shape, so a queue entry and a delivery issue are
structurally identical and are told apart by `source`.

```json
{
  "queue": [
    { "id": "<queue-id>", "source": "queue", "created_at": "2026-08-01T09:00:00Z",
      "return_path": "bob@example.com", "subject": "Quarterly report", "size": 2048,
      "flags": [],
      "recipients": [
        { "address": "someone@elsewhere.example", "status": "TemporaryFailure",
          "retry_due": "2026-08-01T09:30:00Z", "retry_count": 2,
          "error": { "type": "connectionError", "response_code": 451,
                     "response_enhanced": "4.4.1",
                     "response_hostname": "mx.elsewhere.example",
                     "message": "Try again later" } }
      ],
      "events": [] }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | String | **Never `null` on either array.** A `queue` row carries the mail server's own queue id. A trace-derived `issues` row carries a synthetic `trace-`-prefixed id that is **stable across polls**, so keying or de-duplicating by `id` is safe. The prefix guarantees a trace id can never collide with a queue id. |
| `source` | String | `queue` or `trace`. |
| `created_at` | String | |
| `return_path` | String | **May be an empty string** — that is a null return path (`<>`), i.e. the message *is* a bounce notification. |
| `subject` | String | |
| `size` | Integer | |
| `flags` | `Array<String>` | `[]` when there are none. A trace-derived bounce carries `["dsnSent"]`. |
| `recipients` | `Array<Object>` | Scrubbed the same way as a trace's `to`. On an `issues` row derived from a trace, only the **failing** recipients appear. |
| `events` | `Array<Object>` | The SMTP log. **`[]` on every `queue` row**, and on `issues` rows whose `source` is `queue`; populated only on `issues` rows whose `source` is `trace`. |

**`source` is the discriminator for two things at once:** whether the row can still
change (a `queue` row is still being retried; a `trace` row is terminal — its bounce
notice has been sent and it has been flushed from the queue), and whether the row
carries an `events` log at all.

**There is no message-level `status` field on this shape** — derive it from
`recipients` and `flags`:

1. any recipient `PermanentFailure` → `bounced` if `flags` contains `dsnSent`,
   otherwise `failed`
2. else any recipient `TemporaryFailure` → `retrying`
3. else every recipient `Completed` → `delivered`
4. else → `sending`

Recipient object:

| Field | Type | Notes |
|---|---|---|
| `address` | String | |
| `status` | String / null | `Completed`, `TemporaryFailure`, or `PermanentFailure`. `null` for a recipient the mail server has not attempted yet. |
| `retry_due` | String / null | |
| `retry_count` | Integer / null | |
| `error` | Object / **`null`** | **Explicit `null`, never an absent key**, when the recipient has no error or an empty error object. Test for `null`, not for key presence. |

Error object — when `error` is non-null, **all five keys below are always emitted**, so
a missing upstream value is `null` rather than an absent key:

| Field | Type | Notes |
|---|---|---|
| `type` | String / null | The mail server's own error-type identifier, passed through unchanged and not validated here. Identifiers the platform recognizes elsewhere: `dnsError`, `connectionError`, `networkError`, `mailboxFull`, `messageRejected`, `unexpectedResponse`, `invalidRecipient`; the field is not constrained to that set, so an unrecognized value can reach you. **`null` on every trace-derived `issues` row** — that path builds the error out of the SMTP log and never sets a type. |
| `response_code` | Integer / null | SMTP status code. |
| `response_enhanced` | String / null | Enhanced status code. |
| `response_hostname` | String / null | The server that answered. |
| `message` | String / null | The SMTP response text, falling back to the error message. |

On a trace-derived `issues` row every one of those five can be `null` at once, when the
SMTP log carried no failure detail — the row is still a genuine permanent failure, and
its `events` array is where the detail lives.
