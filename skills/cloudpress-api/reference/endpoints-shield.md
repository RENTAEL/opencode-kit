# Shield (WAF, DDoS, Bots)

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### Sites / Shield (WAF, DDoS, bots)

**Base route:** `/api/sites/:site_id/shield` — scopes `sites:read` / `sites:write`. Writes need `can_edit`; deletes need `can_destroy`. All calls are synchronous.

**Plan gate.** Every endpoint under this base route — the shield zone itself plus `bot_detection`, `waf`, `waf_custom_rules`, `rate_limits`, `access_lists` and `events` — returns `403 {"error":"shield_not_in_plan"}` when the site's product doesn't include Shield. This describes the endpoints under this base route only; the `/api/sites/:site_id/metrics/shield` endpoints in the last section are outside it, and nothing here should be read as describing their plan behavior.

**Role is checked before plan.** The site-role filters run ahead of the plan gate, so a read-only collaborator on a site whose plan lacks Shield gets `403 {"errors":["Not Authorized"]}` and **never** sees `shield_not_in_plan`. The two 403s have different body shapes — an `errors` **array** for the role failure, an `error` **string** for the plan failure — so match on the shape, not just the status.

**`409 shield_not_active` / `502` upstream, with two exceptions.** Reads generally return `409 {"error":"shield_not_active"}` when the shield zone isn't provisioned and `502` on upstream failure. Two endpoints do **not** follow that rule, and both are called out in place below:

- `GET .../shield/waf` returns **`502`** — never a `409` — when the zone is missing or won't load (`{"error":"Not configured"}` when there is no pull zone).
- `GET .../shield/events` can never return `502`: upstream failure is reported as `409 shield_not_active`, indistinguishable from "no zone".

#### Shield zone
- `GET /api/sites/:site_id/shield` — config summary
  ```json
  { "active": true, "plan": "advanced",
    "waf": { "enabled": true, "execution_mode": 0, "disabled_rules": [], "log_only_rules": [], "learning_mode": false, "learning_mode_until": "..." },
    "ddos": { "sensitivity": 0, "execution_mode": null, "challenge_window": 3600 },
    "whitelabel_response_pages": false }
  ```
- `POST /api/sites/:site_id/shield` — activate (creates the zone). **`201`**.
  - No pull zone on the site → **`409 {"error":"shield_not_active"}`**. There is no `cdn_not_active` anywhere in the Shield path; a client branching on that literal never matches. The absence of a CDN pull zone surfaces here as `shield_not_active`, the same literal you get for "zone not provisioned".
  - Zone **already active** → **`502 {"error":"Shield Zone already exists"}`**, not a `409` and not a `2xx`. Activation is not idempotent: re-POSTing a live zone is an error, and a `502` here does not mean the upstream is unhealthy.
- `PATCH /api/sites/:site_id/shield` — update. Params (all optional): `plan_type` (0–3) or `premium` (bool), `learning_mode`, `waf_enabled`, `waf_execution_mode`, `waf_disabled_rules[]`, `waf_log_only_rules[]`, `ddos_sensitivity`, `ddos_execution_mode`, `ddos_challenge_window`, `whitelabel_response_pages`. The two rule lists are arrays of rule-**ID strings**, not integers.
- `DELETE /api/sites/:site_id/shield` — deactivate (soft: disables WAF + DDoS).

#### Bot detection
- `GET .../shield/bot_detection` — config
- `PATCH .../shield/bot_detection` — **premium-only** (`403 shield_premium_required`). Params: `execution_mode`, `request_integrity_sensitivity`, `ip_address_sensitivity`, `browser_fingerprint_sensitivity`, `browser_fingerprint_aggression`, `browser_fingerprint_complex_enabled`.

#### WAF
- `GET .../shield/waf` — WAF config. **Does not return `409`.** Every failure on this route lands on `502`: with no pull zone the body is `{"error":"Not configured"}`, and a genuine upstream failure returns the upstream error text under the same `error` key and the same status. So a `502` here cannot tell you which of the two happened — call `GET /api/sites/:site_id/shield` if you need to distinguish "not provisioned" from "upstream broken".
- `PATCH .../shield/waf` — params: `waf_enabled`, `waf_execution_mode` (0=Log, 1=Block), `waf_disabled_rules[]`, `waf_log_only_rules[]`. The two rule lists are arrays of rule-**ID strings** (not integers).
- `GET .../shield/waf/rules` — list managed WAF rules (bare array).

#### Custom WAF rules
- `GET .../shield/waf_custom_rules` — list
- `POST .../shield/waf_custom_rules` — **premium-only**. **`201`**. Params: `rule_name`, `rule_description`, and `rule_configuration[action_type]` (1=Block,2=Log,3=Challenge,4=Allow,5=Bypass), `[variable_type]`, `[variable_subselector]`, `[operator_type]`, `[severity_type]` (0=NOTICE,1=WARNING,2=CRITICAL), `[value]`.
- `PATCH .../shield/waf_custom_rules/:id` — update (not premium-gated).

  > **Partial updates are unsafe on this route — it silently resets the rule's whole configuration.** `rule_name` and `rule_description` are sent only when present, but the `rule_configuration` object is rebuilt and transmitted **unconditionally**, from whatever the request supplied. A `PATCH` sending only `rule_name` therefore also writes `actionType: 0`, `operatorType: 0`, `severityType: 0`, `value: ""` and empty arrays for the variable types, transformations and chained conditions — wiping the rule's matching logic. `0` isn't even a valid action type (the enum starts at `1`). **Always read the rule first and re-send its complete `rule_configuration` with every PATCH.** This differs from the rate-limits PATCH, which drops unsupplied keys instead of zeroing them.
- `DELETE .../shield/waf_custom_rules/:id` — **`204`** (destroy role).

#### Rate limits
- `GET .../shield/rate_limits` — list
- `POST .../shield/rate_limits` — **`201`**. Params: `rule_name`, `rule_description`, `rule_configuration` (open hash, forwarded to Bunny).
- `PATCH .../shield/rate_limits/:id` — update
- `DELETE .../shield/rate_limits/:id` — **`204`** (destroy role).

**Name validation — rate limits only.** On **`POST .../shield/rate_limits` and `PATCH .../shield/rate_limits/:id`, and nowhere else**, `rule_name` and `rule_description` are checked before the upstream call: they may contain **only ASCII letters, numbers, and spaces** (hyphens, underscores, dots, and non-ASCII are rejected). A bad value returns **`422`** `{"error":"Rule name can only contain letters, numbers, and spaces."}` (or `"Rule description ..."`). These two writes are the only Bunny-Shield writes that map an invalid input to a `422` instead of a `502`.

> The check does **not** apply to the identically-named `rule_name` / `rule_description` params on `waf_custom_rules` two sections above, nor to the `name` on `access_lists`. Send a hyphenated or non-ASCII name to those routes and it is forwarded upstream as-is, coming back as an opaque **`502`**. Apply the same character restriction client-side for every named Shield object; only rate limits will tell you cleanly.

#### Access lists
- `GET .../shield/access_lists` — list custom lists
- `GET .../shield/access_lists/enums` — enum values
- `GET .../shield/access_lists/:id` — view
- `POST .../shield/access_lists` — **`201`**. Params: `name`, `description`, `type` (Integer), `content` (newline-delimited), `checksum`.
- `PATCH .../shield/access_lists/:id` — update. **Accepts five params but sends only three.** `name`, `content` and `checksum` are forwarded upstream; **`description` and `type` are silently dropped** — permitted by the endpoint, accepted with a success response, and never written. There is no error and no warning. Neither field can be changed after creation through this route.
- `DELETE .../shield/access_lists/:id` — **`204`** (destroy role).

#### Events
- `GET .../shield/events` — event log. Query: `date` (`MM-DD-YYYY`, default today), `continue` (continuation token). Returns `{ "logs", "hasMoreData", "continuationToken", "startToken" }`.

  **This route never returns `502`.** It doesn't use the shared upstream-error responder: an upstream fetch that fails is mapped to `409 {"error":"shield_not_active"}`, exactly the same response as "this site has no shield zone". A `409` here is ambiguous — don't read it as proof the zone is missing, and don't treat it as permanent without re-checking `GET /api/sites/:site_id/shield`.

---

### Sites / Metrics / Shield

`GET /api/sites/:site_id/metrics/shield` and `.../metrics/shield/overview` — Shield stats for the past 28 days. Scope `sites:read`. Returns `409 shield_not_active` when there is no zone **or** the stats payload comes back empty.

**Both endpoints are served from a server-side cache with a 1-hour TTL**, shared between them and keyed per shield zone. Both read the same cached payload, so a configuration change is not reflected in either until the entry expires — these numbers can be up to an hour stale. Don't poll them to confirm a write landed; read the config endpoints instead.

- `metrics/shield`: `{ "ddos": [...], "bots": [...], "waf": [...] }` — each series `{ "name", "data": [ { "x": "2026-05-01", "y": 0 } ] }`.
- `metrics/shield/overview`: bare array `[ { "name": "DDoS Attacks", "data": [...] }, { "name": "WAF Triggers", "data": [...] } ]`.
