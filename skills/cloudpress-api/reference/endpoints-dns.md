# DNS

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### DNS Zones

**Base route:** `/api/dns_zones` — scopes `dns:read` / `dns:write`.

Reads are **not account-scoped.** List returns the zones of *every* account the
credential's user belongs to, and show resolves a zone id from any of them —
`X-Auth-Account` does **not** narrow either one. (Only zone *create* consumes the
header; see below.)

#### GET /api/dns_zones — list

**Paginated** — accepts `page` and `per_page` (default 50, max 100). This is one of the
few index endpoints that genuinely paginates; the zone *records* list below does not.

Each element is the zone summary only: **no `records` and no `nameservers`** — those two
keys exist on show and nowhere else.

```json
{
  "dns_zones": [
    { "id": "<guid>", "name": "example.com",
      "dnssec": false, "dnssec_data": null,
      "account": { "id": "<guid>", "name": "Acme" },
      "created_at": "...", "updated_at": "..." }
  ]
}
```

#### GET /api/dns_zones/:id — view zone with records

```json
{
  "dns_zone": {
    "id": "<guid>", "name": "example.com",
    "dnssec": false, "dnssec_data": null,
    "account": { "id": "<guid>", "name": "Acme" },
    "records": [ ... ],
    "nameservers": ["<nameserver-1>", "<nameserver-2>"],
    "created_at": "...", "updated_at": "..."
  }
}
```

**Never hardcode nameserver hostnames.** `nameservers` is assigned by the upstream DNS
provider per zone and can be overridden per account, so the pair varies from zone to zone
and account to account — the values shown above are placeholders, and this skill
deliberately does not name any real one. Read the hostnames out of *this* response for
*this* zone and delegate to those; a delegation pointed at a guessed nameserver takes the
domain offline. The key is an **empty array** until the zone is provisioned upstream —
treat `[]` as "not ready yet", not as "no nameservers". A populated result is cached for ten minutes, so a
just-provisioned zone can report `[]` for a short window.

`dnssec_data` when enabled: `{ "Enabled", "DsRecord", "Digest", "DigestType", "Algorithm", "PublicKey", "KeyTag", "Flags", "DsConfigured" }`.

#### POST /api/dns_zones — create zone
**Requires `X-Auth-Account`** — the new zone is attached to the account that header names,
and there is no body field to override it. Missing header → **`400`**
`{"errors":["Missing X-Auth-Account"]}`. Also requires **edit access** on that account,
else **`403`** `{"errors":["Not Authorized"]}`. Only `name` is accepted:
```json
{ "dns_zone": { "name": "example.com" } }
```
Success is **`200`** with the full show body (records + nameservers), not `201`.
Validation failure → **`422`** `{"errors":[...]}`.

#### PATCH /api/dns_zones/:id — toggle DNSSEC
```json
{ "dns_zone": { "dnssec": true } }
```
Requires **edit access** on the zone's account, else **`403`**
`{"errors":["Not authorized to edit this zone."],"code":"forbidden"}`.
Success is **`200`** with the full show body; validation failure → **`422`** `{"errors":[...]}`.

#### DELETE /api/dns_zones/:id — delete zone. Returns **`202`**.
Requires **destroy access** on the zone's account, else **`403`**
`{"errors":["Not authorized to delete this zone."],"code":"forbidden"}`.

#### GET /api/dns_zones/:id/dns_stats — DNS query statistics
Optional `date_from` / `date_to` (ISO 8601; default last 14 days).
```json
{
  "total": 12345,
  "series": [ { "name": "Queries", "data": [[1704067200000, 42], ...] } ],
  "date_from": "...", "date_to": "..."
}
```
The series name is the literal `"Queries"` (capital Q), and the series array always has
exactly that one entry. `502` if the zone is unprovisioned or upstream fails.

---

### DNS Zone Records

**Base route:** `/api/dns_zones/:dns_zone_id/records` — scopes `dns:read` / `dns:write`.

Every **write** (create/update/destroy) requires **edit access** on the zone's account,
else **`403`** `{"errors":["Not authorized to edit records on this zone."],"code":"forbidden"}`.

- `GET .../records` — list, as `{"dns_records":[ ... ]}`
- `GET .../records/:id` — view, as `{"dns_record":{ ... }}`

```json
{
  "dns_record": {
    "id": "<guid>", "record_type": 0, "ttl": 300, "value": "192.0.2.1",
    "name": "@", "priority": null, "weight": null, "port": null,
    "flags": null, "record_tag": null, "comment": "Main A record",
    "site": null, "created_at": "...", "updated_at": "..."
  }
}
```

#### Record type codes

`record_type` is an **integer code**, not a string — there is no `"A"` / `"CNAME"` form
anywhere in the API. Note that `1` is **AAAA**, not A: pairing `record_type: 1` with an
IPv4 address fails validation with `"Value is not a valid ipv6 address"`.

| Code | Type | Code | Type |
|---|---|---|---|
| `0` | **A** (the column default) | `8` | **SRV** |
| `1` | **AAAA** | `9` | **CAA** |
| `2` | **CNAME** | `10` | PTR |
| `3` | **TXT** | `11` | Script |
| `4` | **MX** | `12` | **NS** |
| `5` | Redirect | `13` | **SVCB** |
| `6` | Flatten | `14` | **HTTPS** |
| `7` | Site (pull zone) | `15` | TLSA |

The codes in **bold** — `0, 1, 2, 3, 4, 8, 9, 12, 13, 14` — are the ones the control
panel offers when creating a record. The rest are platform-managed: `7` and `11` are
locked against user edits, and `15` is written by automation. The model validates
`record_type` only as an integer `0`–`15`, so the API will attempt the others; it will
not necessarily accept them, since the record is also pushed to the upstream DNS
provider and a rejection there surfaces as a **`422`**.

#### POST .../records — create

The body must be **wrapped in `dns_record`**, exactly as zones are wrapped in `dns_zone`.
An unwrapped body is rejected before the action runs, with a **`400`** — the same is true
of PATCH.

```json
{ "dns_record": { "record_type": 0, "name": "www", "value": "192.0.2.1", "ttl": 3600 } }
```

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `record_type` | Integer | No | Code from the table above. **Omitting it silently creates an A record** (`0`) rather than erroring — always send it. Must be `0`–`15`. |
| `ttl` | Integer | No | Defaults to `14400`. Must be `> 29` and `< 604800`. |
| `value` | String | **Yes** | Record value/target. Required for every type except `7`, which is not user-creatable — treat it as always required. |
| `name` | String | No | Subdomain or `@` |
| `priority` | Integer | **Conditional** | **Required for `4` (MX) and `8` (SRV)**; `0`–`65535`. Omitting it on those types → `422`. |
| `weight` | Integer | **Conditional** | **Required for `8` (SRV)**; `0`–`100`. |
| `port` | Integer | **Conditional** | **Required for `8` (SRV)**; `0`–`65535`. |
| `flags` | Integer | **Conditional** | **Required for `9` (CAA)**; integer `>= 0`. An **integer**, not a string. |
| `record_tag` | String | **Conditional** | **Required for `9` (CAA)**. |
| `comment` | String | No | |

A conditionally-required field is only validated on its own types — sending `priority` on
a TXT record is ignored, omitting it on an MX record is a **`422`**.

Create returns **`200`** with the `dns_record` body (renders `show`, not `201`).

#### PATCH .../records/:id — update
Same `{"dns_record": {...}}` wrapper. Permits `ttl, value, priority, weight, port, flags,
record_tag, comment` (not `name` or `record_type`). Returns **`202`** with no body; the
conditional-requirement rules above still apply, so blanking `value` on any type but `7`
is a **`422`**.

#### DELETE .../records/:id — delete. Returns **`202`** with no body.
