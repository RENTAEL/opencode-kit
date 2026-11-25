# MCP Server (Model Context Protocol)

> Reference file for the **cloudpress-api** skill. Authentication, OAuth scopes, error responses, the authorization model, and async patterns are in [`../SKILL.md`](../SKILL.md).

---

CloudPress runs a **stateless, OAuth-only, JSON-RPC 2.0** MCP server at **`POST /mcp`** (one per brand host). It exposes a curated subset of the REST API as MCP **tools** (reads broadly, plus a narrow set of safe writes). It is a *remote* HTTP server — there is no SSE stream and no session id.

### Connecting an MCP client (end-user setup)

> **NOTE — surface this to anyone setting up CloudPress in an MCP client.**
>
> Modern MCP clients connect to CloudPress directly over **remote Streamable HTTP** — no local bridge or config file. The quick-start parameters are:
>
> - **Transport:** Streamable HTTP (remote)
> - **URL:** `https://my.cloudpress.com/mcp`
> - **Headers / credentials:** none up front — auth happens *after* setup via the OAuth browser flow.
>
> There is nothing to paste into a config file and no token to pre-provision. After the server is added, the client prompts the user to sign in to CloudPress and authorize; the access token is obtained and cached automatically.
>
> **Host:** replace `my.cloudpress.com` with the user's CloudPress brand hostname. White-label brands each have their own host (e.g. `brand.example.com`) — the `/mcp` URL must match the brand you authorize against, because tokens are brand-locked (see audience binding below).
>
> **Claude (desktop) — custom connector.** **Customize → Connectors → Add custom connector**, enter a **Name** (e.g. `CloudPress`) and the **Remote MCP server URL** `https://my.cloudpress.com/mcp`, then **Add**. More detail: <https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp>. Claude then prompts to authenticate with the CloudPress account to finish.
>
> **OpenAI Codex (desktop).** **Settings → MCP Servers → Add Server**, enter the URL `https://my.cloudpress.com/mcp` (no fields beyond the URL), save. Codex then prompts to authenticate with the CloudPress account to finish.
>
> **Advanced — stdio bridge (older clients only).** A client that only speaks **stdio** and can't reach a remote HTTP endpoint can use the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) bridge, which runs locally over stdio and proxies to CloudPress's `/mcp`, handling the OAuth login. Add CloudPress under the client's `mcpServers` object (e.g. `claude_desktop_config.json`):
>
> ```json
> "cloudpress": {
>   "command": "npx",
>   "args": ["-y", "mcp-remote", "https://my.cloudpress.com/mcp"]
> }
> ```
>
> If `npx` is not on the client's PATH (common — GUI apps don't inherit your shell PATH) and **`mise`** is available, use it to provide `npx`:
>
> ```json
> "cloudpress": {
>   "command": "mise",
>   "args": ["x", "--", "npx", "-y", "mcp-remote", "https://my.cloudpress.com/mcp"]
> }
> ```
>
> Then **fully restart** the client; first use opens a browser to authorize.

### Transport

- `POST /mcp` → JSON-RPC. `GET`/`PUT`/`PATCH`/`DELETE /mcp` → **`405`** `{"jsonrpc":"2.0","id":null,"error":{"code":-32600,"message":"Only POST JSON-RPC is supported at /mcp"}}`.
- Request body is a single JSON-RPC object (**batch arrays are rejected** with `-32600`). Malformed JSON → `-32700` Parse error.
- Notifications (a request with **no `id`**, e.g. `notifications/initialized`) get **`202`** with an empty body.
- **CORS** is enabled for `/mcp` (origins `*`, methods GET/POST/OPTIONS, exposes `WWW-Authenticate`/`Retry-After`) — unlike `/api`, which is not browser-accessible. A browser `Origin`, if present, must match the request host (DNS-rebinding guard) or **`403`** `Origin not allowed`; non-browser clients send no `Origin` (allowed).
- **`MCP-Protocol-Version`** header, if sent, must be one of `2025-06-18`, `2025-03-26`, `2024-11-05`, else **`400`**. Blank is allowed.
- **Rate limit:** 6000 requests / 10 min, keyed per OAuth token (10× the `/api` limit).

### Authentication — OAuth only, audience-bound

`/mcp` accepts **only OAuth access tokens** (session and API-key credentials are refused). On top of the normal OAuth checks (brand isolation, account present, **trial accounts blocked**, live role re-check), the token must be **audience-bound to this MCP resource** (RFC 8707): its `resource` must equal the `/mcp` URL of the brand host it was authorized against — **`https://my.cloudpress.com/mcp`** on the default brand.

- A token minted for `/api` (no `resource`) or for another brand's `/mcp` → **`401`**, body `{"jsonrpc":"2.0","id":null,"error":{"code":-32600,"message":"invalid_token: token audience is not valid for this MCP resource"}}`, header `WWW-Authenticate: Bearer resource_metadata="https://my.cloudpress.com/.well-known/oauth-protected-resource/mcp"` (the brand host you called).
- Conversely, an `/mcp`-audience token is rejected at `/api` with `401 invalid_token` (see [Authentication](../SKILL.md#authentication)).
- The audience is fixed at **authorize** time and inherited immutably across refresh.

### Protected-resource metadata (RFC 9728)

```bash
GET /.well-known/oauth-protected-resource        # root form
GET /.well-known/oauth-protected-resource/mcp     # canonical (advertised in the 401 challenge)
```
```json
{
  "resource": "https://<host>/mcp",
  "authorization_servers": ["https://<host>"],
  "scopes_supported": ["sites:read","sites:write","domains:read","domains:write","dns:read","dns:write","mailspace:read","mailspace:write","billing:read","cpanel:read"],
  "bearer_methods_supported": ["header"]
}
```
`scopes_supported` is rendered from the server's **whole** scope vocabulary — all ten
scopes — not from the subset the MCP tools happen to use. Do not read it as a list of
what `/mcp` exposes: `mailspace:*` and `cpanel:read` are advertised here but back no
MCP tool (see "Not exposed as tools"), and `billing:write` is absent because no such
scope exists at all.

The client follows `authorization_servers` to `GET /.well-known/oauth-authorization-server` (see [OAuth 2.1](../SKILL.md#oauth-21)) to discover the authorize/token endpoints, then runs the standard PKCE flow.

### JSON-RPC methods

| Method | Result |
|---|---|
| `initialize` | `{ "protocolVersion": "2025-06-18", "capabilities": { "tools": { "listChanged": false } }, "serverInfo": { "name": "cloudpress-mcp", "version": "1" } }` (echoes a supported requested version) |
| `ping` | `{}` |
| `tools/list` | `{ "tools": [ … ] }` — **filtered to the tools the token's scopes allow** |
| `tools/call` | executes a tool (see result shape below) |
| `notifications/*` | acknowledged, no response (202) |
| anything else | `-32601` Method not found |

**JSON-RPC error codes:** `-32700` parse error, `-32600` invalid request / batch / origin / version / auth, `-32601` method not found, `-32602` invalid params (`Unknown tool`, `insufficient_scope` with `data.required_scope`, missing `request_id`), `-32603` internal error.

### Scopes & tool visibility

Each tool declares a required scope from the same vocabulary as the REST API. `tools/list` shows only tools the token's scopes cover. Calling a tool the token lacks scope for returns a **JSON-RPC error in a `200`** (not an HTTP 403):
```json
{ "jsonrpc":"2.0","id":1,"error":{"code":-32602,"message":"insufficient_scope","data":{"required_scope":"sites:write"}} }
```

### Idempotency (mutation tools)

Every **write** tool requires an `arguments.request_id` (an idempotency key) — omitting it → `-32602` `"request_id is required for this tool"`. Keyed per (token, tool, `request_id`) with a fingerprint of the other arguments:
- Replay of a **completed** call → returns the original stored result (no re-execution).
- Same `request_id` still **in flight** → success result `{"structuredContent":{"status":"processing"},"isError":false,...}`.
- Same `request_id` with **different arguments** → `isError:true` "already used with different arguments. Use a new request_id."

Keys are retained ~24h (daily cleanup). Each write tool's behavior is advertised in its `tools/list` `annotations` (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`).

**`idempotentHint:false` is the default, not a declaration.** A tool is reported as
non-idempotent unless it *opts in* to idempotency, so the absence of the hint carries
no meaning — what tools actually declare is `idempotent: true`. **Eight** of the 27
write tools end up non-idempotent, either by declaring `false` outright or by never
declaring anything:

| Non-idempotent write tool | How |
|---|---|
| `create_edge_rule`, `create_waf_custom_rule`, `create_rate_limit`, `create_access_list`, `activate_shield` | declare `idempotent: false` |
| `create_dns_zone`, `create_dns_record`, `restart_site` | declare nothing — they inherit the `false` default |

Two of these are easy to miss: **`create_dns_record` and `restart_site` are also
non-idempotent**, and `restart_site` is not a create at all. Avoid blind retries on
any of the eight; to change an existing record use the corresponding `update_*` tool
(by id/Guid). Note that the idempotency machinery above still dedupes a replay of the
*same* `request_id` on these tools — the hint describes what happens when you retry
with a **new** one.

### Tool result shape

A successful `tools/call` returns both a text block and structured data — the same payload in both:
```json
{ "content": [ { "type": "text", "text": "<JSON string>" } ], "structuredContent": { … }, "isError": false }
```

**Do not assume a tool's payload matches its REST counterpart.** Only **20 of the 66**
tools render the shared `/api` templates; the other 46 build their own Hash, and those
diverge from REST in shape. Four patterns cover the whole surface:

| Pattern | Tools | Shape |
|---|---|---|
| **REST templates** | 20 read/create tools, mostly the sites / DNS / domains / orders / subscriptions reads (`list_sites`, `get_site`, `list_dns_zones`, `get_order`, …) | byte-identical to the REST response |
| **Write acknowledgement** | most mutation tools — the deletes, `rename_site`, `restart_site`, `purge_cdn_cache`, `toggle_edge_rule`, `deactivate_shield`, `update_dns_record`, `update_rate_limit`, `update_waf_custom_rule`, `update_curated_access_list`, `create_access_list` | `{"status": "accepted", "<identity>": "…"}` — see below |
| **Named-key wrapper** | `list_site_tasks`, `list_edge_rules`, `list_waf_custom_rules`, `list_waf_managed_rules`, `list_rate_limits`, `list_access_lists`, `list_curated_access_lists`, `search_domains` | a single-key object wrapping the array, **where the REST endpoint returns a bare array** |
| **Upstream passthrough** | the live observability reads (`get_cdn_metrics`, `get_cdn_status`, `get_cdn_caching`, `get_cache_status`, `get_cdn_logs`(`_summary`), `get_origin_logs`, `get_resource_metrics`, `get_dns_metrics`, `get_shield_status`, `get_waf_config`, `get_shield_events`, `get_shield_metrics`) | the upstream vendor/service payload, forwarded largely as-is |

Where a write tool returns that acknowledgement, it carries an **identity key alongside
`status`** — `site_id`, `guid`, `record_id`, `rule_id`, `list_id`, `dns_zone_id` or
`configuration_id`, depending on the tool. That key is what you need to address the
record you just created or changed, and for a create it is the only place the new id is
handed to you.

**Several Shield and edge write tools are shape-conditional at runtime**, so do not
hard-code either branch: `activate_shield`, `create_edge_rule`, `create_waf_custom_rule`,
`create_rate_limit`, `update_shield`, `update_bot_detection` and `update_access_list`
return the **upstream object verbatim** when the upstream supplied one, and fall back to
the `{"status": "accepted", …}` envelope when it did not. Branch on whether `status` is
present rather than assuming. Two further exceptions: `update_cdn_caching` returns the
**refreshed caching config** (no `status` key at all), and `create_dns_zone` /
`create_dns_record` render the **REST templates** like the reads.

**Business failures are not JSON-RPC errors** — they come back as a normal result with `"isError": true` and a text message. Secret redaction is applied to both emits: `get_site` includes `site.ssh` **only** if the token also holds `sites:write`; `get_order` always strips `site.ssh_data`.

### Tool catalog

**66 tools**, all account-scoped (operate on the authorized account). Reads are broad; writes cover DNS CRUD, site rename/restart, CDN caching + purge, edge rules, and the full Shield surface (activate/deactivate, WAF settings & managed/custom rules, rate limits, access lists, bot detection). `*` = required argument. Mutations (✎) require `request_id`. Registrar writes, order/site/cart writes, backups, SSO, and the account/user/API-key surface remain REST-only (see the end of this section).

**Sites** (`sites:read` / `sites:write`)
| Tool | Scope | Args | Notes |
|---|---|---|---|
| `list_sites` | `sites:read` | — | active **and pending-delete** sites — a site scheduled for deletion is still listed. Filter on the site's own state if you only want live ones |
| `get_site` | `sites:read` | `id*` | same scope as `list_sites` — resolves a pending-delete site too (it returns a minimal payload, powered off). SSH creds only if token also has `sites:write` |
| `rename_site` ✎ | `sites:write` | `id*`, `name*`, `request_id*` | name-only (no plan change); returns `{status:"accepted"}` |
| `restart_site` ✎ | `sites:write` | `id*`, `request_id*` | async container restart |
| `list_site_tasks` | `sites:read` | `id*`, `page`, `per_page` | a site's task/activity history, newest first. **Full history, paginated** (50/page, max 100) — unlike `GET /api/sites/:id/tasks`, which returns at most the 100 most recent in one bare array, so counts and totals differ between the two. **The shape differs too**: this tool returns `{"tasks": [ … ]}`, an object wrapping the array, where the REST endpoint returns the bare array — so the tasks are one level deeper than a REST-shaped parser expects. Same `labels` redaction and `performed_by` masking as REST |

**DNS** (`dns:read` / `dns:write`)
| Tool | Scope | Args |
|---|---|---|
| `list_dns_zones` | `dns:read` | `page`, `per_page` |
| `get_dns_zone` | `dns:read` | `id*` |
| `create_dns_zone` ✎ | `dns:write` | `name*`, `request_id*` |
| `delete_dns_zone` ✎ | `dns:write` | `id*`, `request_id*` |
| `get_dns_metrics` | `dns:read` | `id*`, `date_from`, `date_to` |
| `list_dns_records` | `dns:read` | `dns_zone_id*`, `page`, `per_page` |
| `get_dns_record` | `dns:read` | `dns_zone_id*`, `id*` |
| `create_dns_record` ✎ | `dns:write` | `dns_zone_id*`, `record_type*` (int code), `value*`, `request_id*`, + `ttl/name/priority/weight/port/flags/record_tag/comment` |
| `update_dns_record` ✎ | `dns:write` | `dns_zone_id*`, `id*`, `request_id*`, + `ttl/value/priority/weight/port/flags/record_tag/comment` |
| `delete_dns_record` ✎ | `dns:write` | `dns_zone_id*`, `id*`, `request_id*` |

**Domains & registration** (`domains:read`)
| Tool | Args | Notes |
|---|---|---|
| `list_domains` | `page`, `per_page` | site hostnames |
| `get_domain` | `id*` | |
| `list_domain_registrations` | `q` | registrar registrations |
| `get_domain_registration` | `id*` | |
| `list_domain_contacts` | `q` | |
| `get_domain_contact` | `id*` | **integer** ID, not a GUID |
| `check_domain_availability` | `domain*` | availability + pricing |
| `search_domains` | `base_name*` | multi-TLD search |
| `suggest_domains` | `domain*` | registrar suggestions |

All registrar **writes** (register/transfer, contact CRUD, hosts) are intentionally **not** exposed — use the REST API for those.

**CDN / Cache / Logs / Metrics** (site-scoped). Reads `sites:read`; writes `sites:write`. CDN reads/writes need a provisioned pull zone (else `cdn_not_active`).
| Tool | Scope | Args | Notes |
|---|---|---|---|
| `get_cdn_status` | `sites:read` | `id*` | pull-zone status overview |
| `get_cdn_caching` | `sites:read` | `id*` | caching settings (smart cache, expirations, vary toggles, stale-while-*) |
| `get_cache_status` | `sites:read` | `id*` | cache-layer status (redis/nginx/bunny) |
| `get_cdn_metrics` | `sites:read` | `id*`, `period`/`period_start`, `step` | read despite REST POST. **Given neither `period` nor `period_start` it defaults to the 24h preset**, where the REST endpoint `422`s — a deliberate divergence, so a bare call returns data instead of an error. Pass a window explicitly if you need a specific one |
| `get_cdn_logs` | `sites:read` | `id*`, + CDN log filters (`from/to/period/status/cache_status/country/url_contains/limit/offset/order`) | window ≤ 3 days |
| `get_cdn_logs_summary` | `sites:read` | same filters | aggregated |
| `get_origin_logs` | `sites:read` | `id*`, `date` (MM-DD-YYYY) | |
| `get_resource_metrics` | `sites:read` | `id*`, `kind[]`, `period_start`, `period_end`, `step` | no range → snapshot; range → series |
| `update_cdn_caching` ✎ | `sites:write` | `id*`, `request_id*`, + any caching fields | **merge** — sends only the keys you pass; returns the refreshed config |
| `purge_cdn_cache` ✎ | `sites:write` | `id*`, `request_id*` | purges the entire pull-zone cache |

**Edge rules** (`sites:read` / `sites:write`, site-scoped, CDN active). System (`CPRESS -`) rules are hidden and cannot be created, relabeled into, updated, deleted, or toggled.
| Tool | Scope | Args | Notes |
|---|---|---|---|
| `list_edge_rules` | `sites:read` | `id*` | returns each rule's Bunny `Guid` + readable labels |
| `create_edge_rule` ✎ | `sites:write` | `id*`, `request_id*`, `ActionType*`, + `ActionParameter1/2/3`, `TriggerMatchingType`, `Triggers`, `ExtraActions`, `Description`, `Enabled`, `OrderIndex` | **non-idempotent** (creates a fresh rule). Bunny PascalCase shape |
| `update_edge_rule` ✎ | `sites:write` | `id*`, `guid*`, `request_id*`, + any of the create fields | **merge** (read-modify-write; send only what changes) — an MCP-only convenience; the REST/web update is a full replace |
| `delete_edge_rule` ✎ | `sites:write` + destroy role | `id*`, `guid*`, `request_id*` | |
| `toggle_edge_rule` ✎ | `sites:write` | `id*`, `guid*`, `enabled*`, `request_id*` | enable/disable |

**Shield** (site-scoped). Reads `sites:read`; writes `sites:write`. Most tools here are plan-gated (`shield_not_in_plan`) — the gate is per-tool, so check the row rather than assuming it applies uniformly. Reads/writes need a provisioned shield zone (`shield_not_active`).
| Tool | Scope | Args | Notes |
|---|---|---|---|
| `get_shield_status` | `sites:read` | `id*` | config summary (no engine-config) |
| `get_waf_config` | `sites:read` | `id*` | full WAF config incl. engine-config (paranoia levels + protocol allow-lists) |
| `list_waf_managed_rules` | `sites:read` | `id*` | managed-rule catalogue (rule ids for `update_shield`) |
| `list_waf_custom_rules` | `sites:read` | `id*` | custom rules + their ids |
| `list_rate_limits` | `sites:read` | `id*` | rate-limit rules + their ids |
| `list_access_lists` | `sites:read` | `id*` | custom allow/block lists + their ids |
| `list_curated_access_lists` | `sites:read` | `id*` | curated Bunny threat lists (no REST equivalent) |
| `get_shield_events` | `sites:read` | `id*`, `date`, `continue` | event log |
| `get_shield_metrics` | `sites:read` | `id*`, `view` (`individual`/`overview`) | Shield stats series |
| `activate_shield` ✎ | `sites:write` | `id*`, `request_id*` | **non-idempotent**; **`shield_not_active`** if there is no pull zone (not `cdn_not_active` — the Shield path never emits that literal) |
| `deactivate_shield` ✎ | `sites:write` + destroy role | `id*`, `request_id*` | soft (disables WAF + DDoS) |
| `update_shield` ✎ | `sites:write` | `id*`, `request_id*`, + WAF / sensitivity (paranoia) / protocol / DDoS / `plan_type` / `learning_mode` / `whitelabel_response_pages` fields | **merge** (all fields optional). `waf_realtime_threat_intelligence_enabled` is premium-only (silently dropped otherwise) |
| `update_bot_detection` ✎ | `sites:write` | `id*`, `request_id*`, + `execution_mode` / sensitivity / fingerprint fields | **premium-only** (`shield_not_premium`); merge |
| `create_waf_custom_rule` ✎ | `sites:write` | `id*`, `request_id*`, `rule_name*`, `action_type*`, `variable_type*`, `operator_type*`, `severity_type*`, `value*`, + `variable_subselector`, `rule_description` | **premium-only**, **non-idempotent** |
| `update_waf_custom_rule` ✎ | `sites:write` | `id*`, `rule_id*`, `request_id*`, `rule_name*`, `action_type*`, `variable_type*`, `operator_type*`, `severity_type*`, `value*`, + `variable_subselector`, `rule_description` | **full replace** — the schema **requires** the whole rule field set, not just the ids. Sending only `id`/`rule_id`/`request_id` is rejected by schema validation before the call runs; read the current rule with `list_waf_custom_rules` and resubmit every field. Not premium-gated |
| `delete_waf_custom_rule` ✎ | `sites:write` + destroy role | `id*`, `rule_id*`, `request_id*` | not premium-gated |
| `create_rate_limit` ✎ | `sites:write` | `id*`, `request_id*`, `rule_name*`, `action_type*`, `match_variable*`, `operator_type*`, `severity_type*`, `value*`, `request_count*`, `timeframe*`, + `block_time`, `counter_key_type`, `rule_description` | **non-idempotent**. `rule_name`/`rule_description`: letters, numbers, spaces only |
| `update_rate_limit` ✎ | `sites:write` | `id*`, `rule_id*`, `request_id*`, `rule_name*`, `action_type*`, `match_variable*`, `operator_type*`, `severity_type*`, `value*`, `request_count*`, `timeframe*`, + `block_time`, `counter_key_type`, `rule_description` | **full replace** — the schema **requires** the whole rule field set, not just the ids. A partial call is rejected by schema validation before it runs; read the current rule with `list_rate_limits` and resubmit every field |
| `delete_rate_limit` ✎ | `sites:write` + destroy role | `id*`, `rule_id*`, `request_id*` | |
| `create_access_list` ✎ | `sites:write` | `id*`, `request_id*`, `name*`, `type*`, `content*`, + `description`, `checksum`, `action` (`allow`/`block`) | **non-idempotent**; also sets the list action (warn-and-continue). **Partial success is reported, not raised**: the list is created and the response still says `"status": "accepted"`, but carries `"action_set": false` plus a `configure_warning` string when the action could not be applied. Check `action_set` whenever you pass `action` — otherwise a list silently exists with the wrong action |
| `update_access_list` ✎ | `sites:write` | `id*`, `list_id*`, `request_id*`, + `name`, `content`, `checksum`, `action` | content full-replace |
| `delete_access_list` ✎ | `sites:write` + destroy role | `id*`, `list_id*`, `request_id*` | |
| `update_curated_access_list` ✎ | `sites:write` | `id*`, `configuration_id*`, `request_id*`, + `is_enabled`, `action` (int) | curated list enable/action (no REST equivalent; sellable plans only) |

**Orders / Subscriptions** (`billing:read`, read-only)
| Tool | Args |
|---|---|
| `list_orders` | `page`, `per_page` |
| `get_order` | `id*` (always strips SSH) |
| `list_subscriptions` | `page`, `per_page` |
| `get_subscription` | `id*` |

**Not exposed as tools** (use the REST API, with a session/API-key credential where OAuth-blocked): site create/delete/resize, backups & restores (incl. exports), SSO, users/roles/accounts/API-keys, carts & order/domain-order writes, registrar/contact/host writes, site-domain & certificate writes, the global `/api/tasks` endpoints and task webhooks (only the per-site task history is a tool — see `list_site_tasks`), the whole cPanel-hosting and Mailspace surface, and all billing **writes** (there is no `billing:write` scope).

Also REST-only, and easy to assume otherwise because a neighbouring read *is* a tool:

- **Site cache writes** — updating, clearing and purging the site's own cache layers. `get_cache_status` reads them, but nothing writes them; `purge_cdn_cache` is the CDN pull-zone purge, a different thing on a different layer.
- **Site variants** — listing and changing a site's variant (PHP version and the like). Neither the read nor the write is a tool.
- **Domain-registration processes** — listing, showing, resending and cancelling registrar processes, even though the rest of the domain read surface is exposed.
- **`GET /api/about`** — the token/workspace introspection endpoint.
- **The CDN-cache webhook** endpoint (distinct from the task webhooks named above).
