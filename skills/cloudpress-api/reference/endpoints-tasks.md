# Tasks & Resource Metrics

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### Tasks

#### Per-site: `/api/sites/:site_id/tasks`
- `GET .../tasks` — up to 100 most recent (bare array). Scope `sites:read`.
- `GET .../tasks/:filter/filter` — filter by `OK`, `PENDING`, `RUNNING`, `CANCELLED`, `PAUSED`, `FAILED`, `TODAY`. An **unrecognized value does not error** — it falls through to the same unfiltered 100-most-recent list, so a typo returns a plausible-looking wrong answer. Check the `status` values you get back.
- `GET .../tasks/:id` — one task. 404 → `{"errors":["Unknown task"],"code":"unknown_task"}`.
```json
{ "id": 123, "name": "site:create", "data": "...", "labels": {}, "status": "OK",
  "start_on": "...", "end_on": "...", "created_at": "...", "updated_at": "...",
  "performed_by": { "id": "<guid>", "name": "Jane Doe", "email": "jane@example.com" } }
```

`start_on` and `end_on` are **omitted entirely when null**, not sent as `null` — a task
that has not started has no `start_on` key at all. `created_at` / `updated_at` are always
present.

Like every per-site route, these reads also return **`402`**
`{"errors":[...],"code":"service_suspended"}` when the site is dunning-suspended and
**`403`** `{"errors":[...],"code":"pending_delete"}` when it is pending deletion.

**`labels` is redacted.** Any key beginning `callback_` — including the
`callback_url`/`callback_auth` pair an order callback is stamped with — is stripped
before serialization. Your own callback URL and its `Authorization` value are therefore
**never** readable back from a task; keep your own record of what you attached.

**`performed_by` is masked for non-customer actors.** Real users are reported in full;
internal identities are not:

| Actor | `performed_by` |
|---|---|
| A user in the workspace | `{ "id": "<guid>", "name": "Jane Doe", "email": "jane@example.com" }` |
| Platform automation | `{ "id": null, "name": "System", "email": null }` |
| CloudPress staff | `{ "id": null, "name": "Support", "email": null }` |

So a `null` `performed_by.id` is not missing data — it means the task was not performed
by anyone in the workspace. Do not key records on `performed_by.id`. Every task has an
associated user, so `performed_by` is **always present** — the masked forms above are the
only "no real user" case you will see. This masking is a property of the task
representation, so it applies identically to the MCP `list_site_tasks` tool.

#### Global: `/api/tasks`

**OAuth-blocked** (session/API-key only) — these routes declare no scope, and an
undeclared endpoint fail-closes for any OAuth token: **`403`**
`{"error":"insufficient_scope","error_description":"endpoint not available via OAuth"}`.

- `GET /api/tasks` — tasks from the last 3 days (scoped to account if `X-Auth-Account` set,
  otherwise the credential's user across all their accounts). The window is a comparison
  on `start_on`, so a task whose `start_on` is null **never appears here at all**,
  regardless of age — use the per-site route if you need those.
- `GET /api/tasks/:id`:
```json
{ "task": { "id": 123, "name": "site:create", "title": "Create Site", "status": "OK", "data": "...",
  "start_on": "...", "end_on": "...", "user": { "id": "<guid>", "email": "jane@example.com" },
  "accounts": [ { "id": "<guid>", "name": "Acme" } ], "sites": [ { "id": "<guid>", "name": "my-site" } ],
  "orders": [ { "id": "<uuid>", "status": "completed" } ] } }
```

---

### Sites / Metrics / Resources

**Base route:** `/api/sites/:site_id/metrics/resources` — scope `sites:read`.
Both routes are per-site, so both also carry the **`402`** `service_suspended` and
**`403`** `pending_delete` responses described above.

#### GET .../metrics/resources — realtime snapshot

**Keys are image names, not service names.** The only normalized one is WordPress: an
image of `wordpress` (in any case) is reported as the literal `"WordPress"`, capital W.
Every other key is the image string exactly as the platform reports it, so do not
hardcode key names — iterate the object and skip `total_storage`.

```json
{ "total_storage": 15.5,
  "WordPress": { "cpu": 12.5, "storage": 8.3, "memory": 256.0 },
  "<image-name>": { "cpu": 3.2, "storage": 2.1, "memory": 128.0 } }
```
CPU = % of plan allocation; storage in GB; memory in MB. A redis container is omitted
unless the site's plan includes redis.

**This endpoint has no error status.** It returns **`{}` with HTTP `200`** when the site
has no compute project behind it, when the upstream metrics call fails, and on any
unexpected error. An empty object is therefore ambiguous — "no data" and "metrics are
broken" look identical. Do not treat `200` as proof the numbers are current.

#### POST .../metrics/resources — historical

**Requires edit permission on the site's account**, despite being a read — it is a `POST`,
and every per-site `POST` carries the same write gate regardless of whether it changes
anything. A caller with read-only access gets **`403`** `{"errors":["Not Authorized"]}`.
The `sites:read` scope is necessary but not sufficient.

```json
{ "kind": ["cpu", "memory"], "period_start": 1704067200, "period_end": 1704153600, "step": "5m" }
```
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `kind` | Array | Yes | `cpu`, `cpu_throttled`, `memory`, `memory_throttled`, `storage`. Empty → `422` `{"errors":["Invalid kind."]}`; unknown value → `422` `{"errors":["Invalid kind: ..."]}` |
| `period_start` | Integer | Yes | Unix timestamp; must be within the last 1 month |
| `period_end` | Integer | Yes | Unix timestamp; must also be within the last 1 month and `> period_start` |
| `step` | String | No | Default `1m` |

Error bodies use the `{"errors":[...]}` array shape: `422` for invalid `kind` or out-of-range period bounds; `502` `{"errors":["Error connecting to metric service"]}` / `{"errors":["Fatal error"]}` on upstream failure; a catch-all `400` `{"errors":["Fatal Error"]}` on unexpected errors.

The upstream payload is passed through **verbatim**, and its shape is two levels deep —
each time-series metric is an **object keyed by container name**, whose values are the
`[timestamp, value]` arrays. It is *not* a bare array:

```json
{ "<service-name>": { "id": 1, "name": "wordpress", "image": "wordpress",
  "resources": {
    "cpu":     { "<container-name>": [[1704067200, 12.5]] },
    "memory":  { "<container-name>": [[1704067200, 256.0]] },
    "storage": 8.3 } } }
```
A service can have several containers, so plan for more than one key under `cpu` /
`memory` / `cpu_throttled` / `memory_throttled`. `storage` is the exception — always a
single current value, and `period_*` / `step` do not affect it.

Two consequences of the pass-through: unlike the realtime snapshot, **nothing is filtered
here** — containers you cannot interact with, redis on a plan without redis, and data
points predating the site's own creation all appear as the platform reported them.

---

### Webhooks / Tasks

**Base route:** `/api/webhooks/task` — async callback endpoint for task completion. This
is *inbound to CloudPress* (infrastructure reporting a result), not your receiver.
**OAuth-blocked.**

- `GET /api/webhooks/task` — connectivity test; returns `{ "ip_address": "<request ip>" }`. No account header needed.
- `POST /api/webhooks/task/:id` — update a task with a result. **Needs `X-Auth-Account`**, and
  its absence is **not** handled: the task lookup goes through the account named by the
  header, so omitting it fails with a **`500`**, not a clean `400`. Send the header.
  ```json
  { "data": "Task output or result payload", "success": true }
  ```
  | Param | Type | Required | Notes |
  |-------|------|----------|-------|
  | `data` | Any | No | Appended to the task's data |
  | `success` | Boolean | No (but always send it) | `true` → `OK`; anything else, **including omitting it**, → `FAILED` |

  `success` is **not validated**. An omitted `success` is cast as falsy and silently marks
  the task **`FAILED`**, still returning `200` — there is no error to tell you the flag
  never arrived.

  Otherwise returns `200` (idempotent — duplicate callbacks are de-duplicated by digest),
  regardless of whether the task ID exists.
