# CDN, Cache, Edge Rules & Logs

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

### Sites / CDN

`GET /api/sites/:site_id/cdn` — Bunny pull-zone status/config. Scope `sites:read`. `409 cdn_not_active` if there is no pull zone **or** the zone exists but its configuration could not be loaded (upstream failure) — a `409` here does **not** prove the CDN is off.

```json
{
  "active": true, "cdn_type": "premium", "optimizer_enabled": true,
  "origin_url": "https://origin.example.com", "origin_type": 0,
  "enable_logging": true, "origin_shield_enabled": false, "auto_ssl": true,
  "cache_control_max_age_override": 3600, "smart_cache": true, "cache_enabled": true,
  "hostnames": [ { "value": "www.example.com", "force_ssl": true, "has_certificate": true, "is_system_hostname": false } ]
}
```

`"active"` is a hardcoded `true` in this payload, never `false` — reaching a `200` at all is what tells you the zone loaded. Don't branch on it; branch on the `409` instead.

#### Caching settings

**Base route:** `/api/sites/:site_id/cdn/caching` — the pull-zone caching configuration (smart cache, expirations, vary toggles, stale-while-*). **Distinct from** the async `/api/sites/:site_id/cache` layer management (redis/nginx/bunny) below. All require **CDN active** (`409 cdn_not_active`). Sync; upstream failures → `502`.

- `GET .../cdn/caching` — settings. Scope `sites:read`.
  ```json
  { "smart_cache": true, "cache_expiration": 3600, "browser_cache_expiration": 0,
    "query_string_ordering": true, "cache_error_responses": false,
    "vary_avif": false, "vary_webp": true, "vary_mobile": false, "vary_hostname": false,
    "vary_country_code": false, "vary_country_state_code": false, "vary_cookie": false,
    "cookie_vary_parameters": [], "query_string_vary_parameters": [],
    "disable_cookies": false, "cache_slice": false,
    "stale_while_offline": true, "stale_while_updating": true }
  ```
- `PATCH .../cdn/caching` — update. Scope `sites:write`. **Partial** — only the keys you send are written (the update is forwarded upstream as a sparse write; unsent keys keep their current value). Returns the refreshed settings (same shape as GET). Permitted fields: the scalar/boolean keys above plus the two arrays `cookie_vary_parameters[]` and `query_string_vary_parameters[]`. `cache_expiration` is seconds (`-1` = respect origin, `0` = cache nothing).
- `POST .../cdn/caching/purge` — purge the entire pull-zone cache. Scope `sites:write` (+ modify role). Sync.

---

### Sites / Cache

**Base route:** `/api/sites/:site_id/cache`. The `:type` segment is the cache layer: `redis`, `nginx`, `bunny`, or `all`. The `:type` filter on `PATCH`/`DELETE`/purge returns **two different 422s**:

- unknown type → `{"error":"unknown_cache_type","allowed":["redis","nginx","bunny","all"]}`
- a **valid** type whose layer the site's plan doesn't include → `{"error":"cache_type_unavailable","cache_type":"redis"}` (e.g. a plan tier with no Redis)

Branch on `error`, not on the status: both are `422`.

- `GET .../cache` — status. Scope `sites:read`. → `{ "bunny": true, "nginx": true, "redis": false }`
- `PATCH .../cache/:type` — enable layer. Scope `sites:write`. **Async `202`.**
- `DELETE .../cache/:type` — disable layer. Scope `sites:write` + destroy role. **Async `202`.**
- `DELETE .../cache/:type/purge` — purge layer. Scope `sites:write`. **Async `202`.**

Async responses: `{ "task_id": 12345, "status": "PENDING", "cache_type": "nginx" }`. Poll the task.

---

### Sites / Edge Rules

**Base route:** `/api/sites/:site_id/edge_rules` — scopes `sites:read` / `sites:write`. All actions require **CDN active** (`409 cdn_not_active`). `:id` is the rule **Guid**. Sync; responses pass through Bunny.

- `GET .../edge_rules` — list
- `POST .../edge_rules` — create. **`201`**. Body wrapped in `edge_rule`:

| Param | Type | Notes |
|-------|------|-------|
| `Guid` | String | Omit to create |
| `ActionType` | Integer | 0–34 (e.g. 0=ForceSSL, 1=Redirect, 2=OriginUrl, 4=BlockRequest, 5=SetResponseHeader, 23=DisableWAF, 28=DisableShield) |
| `ActionParameter1/2/3` | String | |
| `TriggerMatchingType` | Integer | How the rule's `Triggers` combine: `0`=MatchAny, `1`=MatchAll, `2`=MatchNone |
| `Description` | String | |
| `Enabled` | Boolean | |
| `OrderIndex` | Integer | |
| `Triggers` | Array<Object> | Each: `{ Type (0=Url,1=RequestHeader,2=ResponseHeader,3=UrlExtension,4=CountryCode,5=RemoteIP,6=UrlQueryString,7=RandomChance,8=StatusCode,9=RequestMethod,10=CookieValue,11=CountryStateCode,12=OriginRetryAttemptCount,13=OriginConnectionError), PatternMatchingType (0=MatchAny,1=MatchAll,2=MatchNone), Parameter1, PatternMatches:[String] }`. The **`Triggers` array holds at most 5 conditions per rule**, and **`PatternMatches` holds up to 5 values** per condition (both Bunny maxima; the per-rule condition cap is validated first). A trigger's `PatternMatchingType` sets how its values combine. |
| `ExtraActions` | Array<Object> | `{ ActionType, ActionParameter1/2/3 }` — additional actions applied with the primary action |

- `PATCH .../edge_rules/:id` — update (Guid from URL). **`200`**. **Full replace**: omitted fields are cleared (send the complete rule). The MCP `update_edge_rule` tool differs — it merges.
- `DELETE .../edge_rules/:id` — delete. Scope `sites:write` + destroy role. **`204`**.
- `PATCH .../edge_rules/:id/enabled` — toggle. Body `{ "enabled": false }`. **`200`**.

System-managed rules (Description prefixed `CPRESS -`) are **filtered out of the `GET` list**, so they never appear in a listing. That filter is the *only* protection these REST endpoints apply: **nothing blocks writing them.** A `PATCH` or `DELETE` carrying a system rule's Guid — obtained from anywhere other than this list — goes straight through to Bunny and takes effect. The system-rule write guard exists only on the MCP edge-rule tools, not here. Treat "absent from the list" as the sole signal, and never write a Guid you didn't read from that list.

---

### Sites / Logs

**Base route:** `/api/sites/:site_id/logs` — scope `sites:read`. Require **CDN active** (`409 cdn_not_active`).

- `GET .../logs/cdn` — CDN access logs. Query: `from`, `to` (ISO 8601); or `period` (`1h`,`6h`,`24h`,`72h`, used only if `from`/`to` blank); filters `status`, `cache_status`, `country`, `url_contains`; `limit` (**default 100**, clamped to 1–1000), `offset`, `order` (`asc`/`desc`). Errors: `422 invalid_period`, `422 invalid_range`, `422 range_exceeds_3_days`, `502 log_fetch_failed` (or another upstream message).
- `GET .../logs/cdn/summary` — aggregated summary (same query params). **Two divergences from the index route, both easy to trip over:** `limit` defaults to **1000**, not 100; and `invalid_range` / `range_exceeds_3_days` come back as **`502`** here, where the index route returns them as `422`. Only `invalid_period` is still a `422`. Upstream failure is `502 log_fetch_failed`.
- `GET .../logs/origin` — origin server logs. Query: `date`, which must be **`MM-DD-YYYY`** (e.g. `10-21-2025`; defaults to today in UTC). The format is **not validated** — any other shape builds a URL the upstream doesn't recognize and silently returns `502 origin_log_fetch_failed`, which is also what a genuine upstream failure returns. Each entry's `log` field is a JSON string, parsed into an added `parsed_log` key.

---

### Sites / Metrics / CDN

`POST /api/sites/:site_id/metrics/cdn` — CDN traffic/performance metrics. Scope `sites:read`, **plus site edit permission**.

This is a read operation behind a `POST` (the body carries the query), and the scope is correctly `sites:read` — but because it is routed as a `POST`, it also passes the same site-level **edit-permission** check every other write on a site passes, and that check is not waived here. A read-only collaborator holding `sites:read` gets **`403`** `{"errors":["Not Authorized"]}`. Read scope alone is not enough to call this endpoint.

```json
{ "period_start": 1704067200, "step": "hourly" }
```
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `period_start` | Integer | Yes* | Unix timestamp (>3 months old → 422) |
| `step` | String | No | Only `hourly` is special-cased (hourly buckets); any other value (incl. `monthly`) is treated as non-hourly |
| `period` | String | No | Preset `12h`/`24h`/`7d`/`30d`; `period_start` takes precedence |

\* Either `period_start` or a valid `period`. Errors use the `{"errors":[...]}` array shape (not a `"code"`): `409` `{"errors":["CDN Not active"]}` when CDN not active; `422` `{"errors":["Invalid period_start"]}`/`{"errors":["Invalid period"]}` for bad/missing period; `502` `{"errors":["Error loading metrics"]}` upstream.

**Response fields** include the scalars `TotalBandwidthUsed`, `TotalOriginTraffic`, `TotalRequestsServed` and **`CacheHitRate`** — a percentage on a 0–100 scale (so `93` means 93%, not 0.93), passed through from upstream unrounded.

> The key is **`CacheHitRate`**. There is no `CacheHitRatio` field; code branching on that name silently reads `nil`.

Timestamp-keyed chart objects (`{ "2025-11-20T00:00:00Z": 0, … }`): `OriginResponseTimeChart`, `BandwidthUsedChart`, `BandwidthCachedChart`, `CacheHitRateChart`, `RequestsServedChart`, `PullRequestsPulledChart`, `OriginTrafficChart`, `Error3xxChart`, `Error4xxChart`, `Error5xxChart`. Plus `GeoTrafficDistribution`, keyed by datacenter location (`{ "EU: Stockholm, SE": 2313 }`).

Bandwidth and traffic figures are in **bytes**, exactly as returned upstream.

> **This endpoint renders the upstream statistics payload verbatim** (only
> `UserBalanceHistoryChart` is stripped), so it carries **fields beyond those listed**
> — the request also enables origin-response-time and origin-shield-bandwidth series.
> The names above are the ones this platform reads itself and the only ones it can
> guarantee; read any others from a live response.
>
> Do not port figures from the control panel: the panel converts bandwidth to KB
> (flooring sub-1000-byte buckets to `0`), rounds and clamps `CacheHitRate`, and adds a
> reshaped `Geo` array. **None of that applies here** — those transforms live in a
> separate code path that this endpoint does not call.
