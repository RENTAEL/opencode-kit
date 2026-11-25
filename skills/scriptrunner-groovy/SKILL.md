---
name: scriptrunner-groovy
description: "ScriptRunner Cloud uses the HAPI API (`com.adaptavist.hapi.cloud.jira.issues.Issues`) instead of Data Center's `ComponentAccessor`. Scripts are Groovy but with Cloud-specific patterns. Scripts referenced via `file:` in YAML get auto-imports; root-level scripts may need explici..."
---
# ScriptRunner Cloud Groovy Scripting

## Overview

ScriptRunner Cloud uses the HAPI API (`com.adaptavist.hapi.cloud.jira.issues.Issues`) instead of Data Center's `ComponentAccessor`. Scripts are Groovy but with Cloud-specific patterns. Scripts referenced via `file:` in YAML get auto-imports; root-level scripts may need explicit imports.

## Quick Reference

| API | Purpose | Features |
|-----|---------|----------|
| `Issues.getByKey(key)` | Fetch issue by key | All features |
| `Issues.create(projectKey, type) { ... }` | Create issue with closure DSL | Jobs |
| `issue.addComment(body)` | Add comment | Listeners, post functions |
| `issue.subtasks` | Access subtask list | Escalation services |
| `issue.getStatus().name` | Status name | Escalation services |
| `issue.created.toZonedDateTime()` | Date field conversion | Script fields |
| `Users.getLoggedInUser()` | Current user (`.accountId`) | Script Manager |
| `get(path)`/`post(path)` | REST client (fluent builder, auto-auth) | All features |
| `baseUrl` | Instance base URL (e.g. `https://mysite.atlassian.net`) | All features |
| `logger.warn/info/debug/error` | Built-in logging | All features |

## HAPI APIs

### Issues.getByKey

Use `Issues.getByKey(issue.key as String)` to get a full issue object. The `as String` cast is important because `issue.key` may be a GString.

```groovy
import com.adaptavist.hapi.cloud.jira.issues.Issues

def hapiIssue = Issues.getByKey(issue.key as String)
def creator = hapiIssue.getCreator()
hapiIssue.addComment("Hello from ScriptRunner")
```

### Issues.create

Creates issues with a closure DSL. Used in jobs where there's no pre-bound `issue`.

```groovy
def newIssue = Issues.create("PROJ", "Task") {
    setSummary("Monthly report")
    setDescription("Auto-generated report")
}
```

### Issue Properties (HAPI Object)

The raw `issue` binding only reliably exposes `issue.key`. For all other properties, fetch the HAPI object first:

```groovy
def hapiIssue = Issues.getByKey(issue.key as String)
```

| Property / Method | Returns |
|-------------------|---------|
| `hapiIssue.created` | DateTime ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â call `.toZonedDateTime()` |
| `hapiIssue.updated` | DateTime ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â call `.toZonedDateTime()` |
| `hapiIssue.subtasks` | Iterable of HAPI issue objects |
| `hapiIssue.getStatus()` | Status ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cast `as Map` to access `.name` |
| `hapiIssue.getCreator()` | User ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `.displayName`, `.accountId` |
| `hapiIssue.getAssignee()` | User or `null` |
| `hapiIssue.getSummary()` | `String` |

### Updating Issue Fields

Use the REST client for field updates on existing issues. `put()` is available alongside `get()` and `post()`:

```groovy
import groovy.json.JsonOutput

put("/rest/api/3/issue/${issue.key}")
    .header("Content-Type", "application/json")
    .body(JsonOutput.toJson([
        fields: [
            summary  : "Updated summary",
            assignee : [accountId: "557058:abc123"]  // null to unassign
        ]
    ]))
    .asString()
```

### JQL Search

Query multiple issues in a script (common in jobs and additional scripts):

```groovy
import groovy.json.JsonOutput
import com.adaptavist.hapi.cloud.jira.issues.Issues

def result = post("/rest/api/3/search")
    .header("Content-Type", "application/json")
    .body(JsonOutput.toJson([
        jql       : "project = PROJ AND status = 'In Progress'",
        maxResults: 50,
        fields    : ["summary", "assignee", "status"]
    ]))
    .asObject(Map)

result.body.issues.each { raw ->
    def hapiIssue = Issues.getByKey(raw.key as String)
    hapiIssue.addComment("Processed by scheduled job")
}
```

### Group Management

**Do not use `Groups.getByName(groupName).add(accountId)`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â deprecated HAPI method, throws as of August 2025.

**Do not use `post("/rest/api/3/group/user")`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â org-level groups (created in `admin.atlassian.com`) are above Jira's OAuth scope. `GET /rest/api/3/group` works (200), but `POST /rest/api/3/group/user` returns 403 with no body even when the ADD_ON has `ADMINISTER=true`.

Use the **Atlassian Admin v1 REST API** instead, called via `HttpURLConnection` (the built-in `get()`/`post()` client only auto-auths Jira REST, not `api.atlassian.com`).

**Prerequisites:**
- Two ScriptRunner Script Variables: `ATLASSIAN_ORG_ID` (org UUID from `admin.atlassian.com` URL) and `ATLASSIAN_API_KEY`.
- The API key must be **unscoped** (created in `admin.atlassian.com ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Settings ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ API keys` with no scope selection). Scoped keys return `ADMIN-401-2 INSUFFICIENT_SCOPE`. Atlassian's [scopes documentation](https://developer.atlassian.com/cloud/admin/scopes/) states: *"If the endpoint you want to use is not listed on the above table, you need to use an API key without scopes."* No `write:groups` scope exists for this endpoint.

```groovy
import groovy.json.JsonOutput
import groovy.json.JsonSlurper

def orgId  = ATLASSIAN_ORG_ID  as String
def apiKey = ATLASSIAN_API_KEY as String

// Resolve group name ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ UUID via Jira REST (read is allowed for ADD_ON)
def groupId = get("/rest/api/3/group?groupname=${groupName}").asObject(Map).body?.groupId

// Write membership via Atlassian Admin v1
def url  = new URL("https://api.atlassian.com/admin/v1/orgs/${orgId}/directory/groups/${groupId}/memberships")
def conn = url.openConnection() as HttpURLConnection
conn.requestMethod = "POST"
conn.setRequestProperty("Authorization", "Bearer ${apiKey}")
conn.setRequestProperty("Content-Type", "application/json")
conn.setRequestProperty("Accept", "application/json")
conn.doOutput = true
conn.outputStream << JsonOutput.toJson([account_id: accountId])  // snake_case, not accountId

def status = conn.responseCode
if (status >= 400) {
    def errBody = conn.errorStream ? new JsonSlurper().parse(conn.errorStream) : "(no error stream)"
    logger.warn("Failed to add ${accountId} to group ${groupId}: HTTP ${status} | ${errBody}")
}
// status < 400 = added (Admin v1 returns success for an already-a-member add ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no 409, no special-casing needed)
```

#### Listing group members (read) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use Jira REST, not the Admin API

There is **no Admin API to list members**: `GET /admin/v1/orgs/{orgId}/directory/groups/{groupId}/memberships` returns **405** (the endpoint is POST-only). List via Jira REST `GET /rest/api/3/group/member` instead. Watch for these traps:

- **Query by `groupId`**, not `groupname` (resolve the id first via `GET /rest/api/3/group`).
- **Pass `includeInactiveUsers=true`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the default `false` silently omits deactivated, suspended, and invited members, so your count comes up short.
- **Filter `accountType == "atlassian"`** for real human users. The endpoint also returns `app`-type accounts (Marketplace apps, integrations, automation/service accounts) that the admin **Members** tab hides ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â these inflate the count well beyond what the UI shows.
- **Don't trust the `active` field** from this endpoint ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it can report `true` for suspended/deactivated users. Use `includeInactiveUsers` + `accountType` instead.
- **Paginate by page size**, not the `isLast` flag: `isLast = body.isLast ?: true` hits the Groovy Elvis bug (`false ?: true` evaluates to `true`) and stops a page early. Stop when a page returns fewer than `maxResults`.

```groovy
def groupId = get("/rest/api/3/group")
    .queryString("groupname", groupName)
    .asObject(Map).body?.groupId

def members    = []
def startAt    = 0
def maxResults = 50

while (true) {
    def resp = get("/rest/api/3/group/member")
        .queryString("groupId", groupId)            // by id, not name
        .queryString("includeInactiveUsers", true)  // include deactivated/suspended/invited
        .queryString("startAt", startAt)
        .queryString("maxResults", maxResults)
        .asObject(Map)
    if (resp.status >= 400) {
        logger.warn("Failed to list members at startAt=${startAt}: HTTP ${resp.status}")
        break
    }
    def values = (resp.body.values ?: []) as List
    values.each { m ->
        if (m.accountId && m.accountType == "atlassian") {   // humans only; skip app accounts
            members << [accountId: m.accountId as String, displayName: m.displayName as String]
        }
    }
    if (values.size() < maxResults) break   // reliable last-page signal (not isLast)
    startAt += maxResults
}
```

#### Removing a member (write)

Same Admin v1 endpoint family as adding, but `DELETE` with the account id in the path. A 2xx response means removed. Add `Thread.sleep(100)` between calls when removing in bulk to avoid rate limits.

```groovy
def conn = new URL("https://api.atlassian.com/admin/v1/orgs/${orgId}/directory/groups/${groupId}/memberships/${accountId}").openConnection() as HttpURLConnection
conn.requestMethod = "DELETE"
conn.setRequestProperty("Authorization", "Bearer ${apiKey}")
conn.setRequestProperty("Accept", "application/json")
try {
    def status = conn.responseCode
    if (status < 200 || status >= 300) {
        def errBody = conn.errorStream ? new JsonSlurper().parse(conn.errorStream) : "(no error stream)"
        logger.warn("Failed to remove ${accountId} from group ${groupId}: HTTP ${status} | ${errBody}")
    }
} finally {
    conn.disconnect()
}
```

#### A group can grant multiple products ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check before bulk-removing

A single group's membership may grant access to **several products at once** (admin ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the group ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **Apps** tab lists each granted product and its plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. a paid product alongside one or more Free ones). Removing members from the group revokes **every** product it grants, not just the one you have in mind. To revoke a **single** product for everyone, remove that product's grant from the group's Apps tab instead of removing members.

### Comments

Simple strings work for plain text. Use ADF for formatted comments.

```groovy
// Plain text
issue.addComment("This is a plain text comment")

// ADF (Atlassian Document Format) for rich text
import groovy.json.JsonOutput
def adf = [
    version: 1,
    type: "doc",
    content: [
        [type: "paragraph", content: [
            [type: "text", text: "This is ", marks: [[type: "strong"]]],
            [type: "text", text: "bold text"]
        ]]
    ]
]
post("/rest/api/3/issue/$issue.key/comment")
    .header("Content-Type", "application/json")
    .body(JsonOutput.toJson(adf))
    .asJson()
```

## REST Client

The built-in `get()` and `post()` methods handle Jira authentication automatically. No API tokens needed.

```groovy
// GET request
def response = get("/rest/api/3/issue/${issue.key}")
    .asObject(Map)
def status = response.body.fields.status.name

// GET with query parameters ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use .queryString(), not string interpolation
// .queryString(name, value) URL-encodes the value automatically
def group = get("/rest/api/3/group")
    .queryString("groupname", groupName)
    .asObject(Map)

// POST with JSON body
def result = post("/rest/api/3/search")
    .header("Content-Type", "application/json")
    .body(JsonOutput.toJson(jql: "project = PROJ", maxResults: 5))
    .asJson()

// Response methods:
// .asJson()      -> returns { status, body } (parsed JSON)
// .asString()    -> returns { status, statusText }
// .asObject(Map) -> returns { body } as Map
```

## Implicit Bindings

| Feature | `issue` bound? | Other bindings |
|---------|---------------|----------------|
| Listener | Yes | event context |
| Script Field | Yes | return value = last expression |
| Job | **No** | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â |
| Escalation Service | Yes (per JQL match) | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â |
| Workflow Post Function | Yes | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â |
| Condition/Validator | Yes | return boolean |
| Additional Script | No | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â |

`baseUrl` and `logger` are available in all feature types.

## executionUser

Controls which user context the script runs under:

| Value | Runs as | Use when |
|-------|---------|----------|
| `ADD_ON` | ScriptRunner service account (elevated) | Automated tasks needing admin-level access |
| `INITIATING_USER` | The user who triggered the event | Operations that should respect user permissions or preserve audit trails |

Most scripts use `ADD_ON`. Configured in `extensions.yaml`, not in the script itself.

## Feature Patterns

### Listener
```groovy
import com.adaptavist.hapi.cloud.jira.issues.Issues
def eventIssue = Issues.getByKey(issue.key as String)
def creator = eventIssue.getCreator()
eventIssue.addComment("Issue created by ${creator.displayName}")
```

### Script Field
```groovy
import com.adaptavist.hapi.cloud.jira.issues.Issues
import java.time.temporal.ChronoUnit
def hapiIssue = Issues.getByKey(issue.key as String)
def created = hapiIssue.created.toZonedDateTime()
def updated = hapiIssue.updated.toZonedDateTime()
ChronoUnit.DAYS.between(created, updated).toString()
// last expression is the return value
```

Return type must match `scriptedFieldType` in `extensions.yaml`:

| `scriptedFieldType` | Expected return |
|---------------------|----------------|
| `TEXT_FIELD` | `String` |
| `NUMBER_FIELD` | `Number` (Integer or Double) |
| `DATE_FIELD` | `String` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `"yyyy-MM-dd"` |
| `DATETIME_FIELD` | `String` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ISO 8601 |
| `RICH_TEXT_FIELD` | ADF `Map` structure |

### Job (no `issue` binding)
```groovy
import com.adaptavist.hapi.cloud.jira.issues.Issues
def newIssue = Issues.create("PROJ", "Task") {
    setSummary("Scheduled report")
    setDescription("Generated at ${new Date()}")
}
```

### Escalation Service
The `jql` field in `extensions.yaml` selects which issues to process ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the script runs once per match with `issue` bound to each result. Configured under the `jobs` key with an added `jql` property.

```groovy
import com.adaptavist.hapi.cloud.jira.issues.Issues
def currentIssue = Issues.getByKey(issue.key as String)
if (currentIssue.subtasks.any { it.getStatus().name != "Done" }) {
    currentIssue.addComment("Not all subtasks are complete")
}
```

### Workflow Post Function
```groovy
import com.adaptavist.hapi.cloud.jira.issues.Issues
Issues.getByKey(issue.key.toString()).addComment("Transitioned to ${issue.status.name}")
```

### Workflow Condition
Conditions use Jira expressions (JavaScript-like syntax), not Groovy:
```javascript
(issue.assignee != null)
```

### Workflow Validator
```javascript
(issue.comments.filter(comment => comment.body.plainText.toLowerCase().includes('banned')).length <= 0)
```

Error message shown to user is configured in YAML (`errorMessage` field).

### Additional Script
Uploaded to the Script Manager, run on demand. No implicit `issue` binding. Access Jira APIs through the REST client or HAPI.

```groovy
def myself = Users.getLoggedInUser()
def result = post("/rest/api/3/project/PROJ/role/10002")
    .header("Content-Type", "application/json")
    .body([user: [myself.accountId]])
    .asObject(Map)
result.body
```

## ADF (Atlassian Document Format)

Required for formatted rich text in Cloud. Structure:

```groovy
def adf = [
    version: 1,
    type: "doc",
    content: [
        [type: "paragraph", content: [
            [type: "text", text: "Hello", marks: [[type: "strong"]]]
        ]],
        [type: "orderedList", content: [
            [type: "listItem", content: [
                [type: "paragraph", content: [
                    [type: "text", text: "First item"]
                ]]
            ]]
        ]]
    ]
]
post("/rest/api/3/issue/$key/comment")
    .header("Content-Type", "application/json")
    .body(JsonOutput.toJson(adf))
    .asJson()
```

## Cloud vs Data Center

| Concept | Cloud | Data Center |
|---------|-------|-------------|
| Issue API | `Issues.getByKey(key)` via HAPI | `ComponentAccessor.issueManager.getIssueObjectByKey(key)` |
| Issue creation | `Issues.create() { setSummary(...) }` | `IssueFactory`, `IssueService` |
| Comments | `issue.addComment(body)` | `CommentManager.create(issue, user, body, ...)` |
| REST calls | Built-in `get()`/`post()` auto-auth | HTTP client or `RestApiFactory` |
| Users | `Users.getLoggedInUser()` (`.accountId`) | `ComponentAccessor.jiraAuthenticationContext.loggedInUser` |
| Logging | `logger.warn(...)` | `log.warn(...)` or `LoggerFactory` |
| Behaviours | TypeScript | Groovy with `FormField` |
| Rich text | ADF (JSON) | Wiki markup or ADF |
| User ID | `accountId` (e.g. `557058:...`) | `username` or `key` |

## Debugging

- **Logs:** `logger.warn("message")` output appears in the ScriptRunner script log viewer (Admin ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ScriptRunner ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Logs). Use `warn` or `error` during development; `debug` is filtered by default.
- **Compilation errors:** Shown in Gradle output when deploying. The script will not run until compilation errors are resolved.
- **Runtime errors:** Surface per feature ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â script fields show an error state on the issue; listener errors are logged but don't block the event; workflow post function errors may fail the transition.

## Deployment

Managed by the ScriptRunner Dev & Deployment Tool (Gradle). Supports both bulk and individual script deployment. See your project's `AGENTS.md` for the full command reference.

## Common Mistakes

- **Using `ComponentAccessor`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â doesn't exist in Cloud. Use HAPI.
- **Forgetting `as String`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `issue.key` may be GString. Use `issue.key as String` or `issue.key.toString()`.
- **Raw wiki markup** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Cloud requires ADF for rich text. Use `JsonOutput.toJson()` to serialize.
- **Assuming `issue` in jobs** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â plain jobs have no `issue` binding. Query or create explicitly.
- **REST v2 vs v3 for rich text** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â When posting comments or descriptions via REST directly (not via `addComment()`), use `/rest/api/3/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it expects ADF. For other endpoints (versions, projects, roles), `/rest/api/2/` is fine.
- **Missing `package`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â scripts in subdirectories must declare `package` matching the directory path.
- **Rate limits** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â scripts that loop over many issues and call the REST client repeatedly can hit Atlassian API rate limits. Add `Thread.sleep(200)` between iterations when processing large result sets.
- **`Groups.getByName().add(accountId)`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â deprecated HAPI method, throws since August 2025.
- **`post("/rest/api/3/group/user?groupname=...")`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â returns 403 for the ScriptRunner ADD_ON when targeting org-level groups (which is most groups in modern Cloud). Use the Atlassian Admin v1 API with an unscoped key ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see the "Group Management" section.
- **Scoped admin API key for `/admin/v1/orgs/ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦/memberships`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â returns `ADMIN-401-2 INSUFFICIENT_SCOPE`. The endpoint requires an unscoped (classic) key created with no scope selection; no `write:groups` scope exists for it.
- **`/admin/v2/orgs/{orgId}/directories/{directoryId}/groups/...`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â looks like a newer version but requires scopes that don't exist and returns `ADMIN-UAM-403-1`. Use v1 (no `directoryId` in path).
- **`{"accountId": "..."}` body for the Admin API** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â wrong; the Atlassian Admin REST API uses snake_case `account_id`. (camelCase `accountId` is correct for Jira REST only.)
- **String interpolation for query parameters** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `get("/rest/api/3/group?groupname=${groupName}")` will break if `groupName` contains spaces or special characters. Use `.queryString("groupname", groupName)` instead ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it URL-encodes the value automatically and is the documented pattern.
- **`GET /admin/v1/orgs/.../memberships`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â returns 405; the endpoint is POST-only. There is no Admin API to list members ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use Jira REST `GET /rest/api/3/group/member`.
- **Omitting `includeInactiveUsers=true` when listing members** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â silently drops deactivated/suspended/invited members, so the count comes up short of the admin UI.
- **Not filtering `accountType` when listing members** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `app`-type accounts (Marketplace apps, integrations, service accounts) are returned alongside humans and inflate the count beyond the admin Members tab. Filter `accountType == "atlassian"` for human users.
- **`isLast = body.isLast ?: true` for pagination** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Groovy's Elvis treats `false ?: true` as `true`, so the loop ends a page early. Stop when a page returns fewer than `maxResults` instead.
- **Trusting the `active` field from `group/member`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â unreliable; it can report `true` for suspended/deactivated users. Use `includeInactiveUsers` + `accountType`.
- **Bulk-removing group members to revoke one product** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a group can grant multiple products at once; removing members revokes all of them. Check the group's Apps tab first; to drop a single product, remove its grant from the group instead.
