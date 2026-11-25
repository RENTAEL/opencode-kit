---
name: workflow-aws-cli
description: "Agents reach AWS through the plain `aws` CLI (v2), authenticated by IAM Identity Center. No tool wraps an AWS API and no credentials are pasted. The `aws-session` plugin's four tools (`aws_session_start`, `aws_session_login`, `aws_session_end`, `aws_session_list`) give each ag..."
---
# AWS CLI Workflow

## Purpose

Agents reach AWS through the plain `aws` CLI (v2), authenticated by IAM Identity Center. No tool wraps an AWS API and no credentials are pasted. The `aws-session` plugin's four tools (`aws_session_start`, `aws_session_login`, `aws_session_end`, `aws_session_list`) give each agent session its own AWS config file containing only the profiles that session's work needs, so parallel agents can work against different environments without touching shared state, and nothing secret is ever written to disk by the agent.

How the pieces fit:

| Piece                                    | Where                                                        | Holds secrets    |
| ---------------------------------------- | ------------------------------------------------------------ | ---------------- |
| Project SSO configuration                | `<main checkout>/.opencode/config/aws-sso.json` (gitignored) | no               |
| Session config (one per agent session)   | `~/.local/state/aws-session/<session-id>/config`             | no               |
| SSO token (one per portal, shared)       | `~/.aws/sso/cache/`, written by `aws sso login`              | yes, AWS-managed |
| Role credentials (short-lived, per role) | `~/.aws/cli/cache/`, refreshed by the CLI from the SSO token | yes, AWS-managed |

One human-approved login fills the token cache for every session on the same portal until the token expires. Sessions themselves are plain config; a leftover session directory is clutter, not a leak.

## Core Rules

- **One session per agent per task, holding only the environments the work needs.** A deploy check on dev starts `dev` (plus `common` when it must read images). Start a session that includes `stg` or `prod` only when the task explicitly targets that environment.
- **Every AWS command names its profile with the `--profile` flag and the session file with `AWS_CONFIG_FILE`:** `AWS_CONFIG_FILE=<session config> aws --profile dev ...`. Verified on 2026-09-22 with AWS CLI 2.35: the `--profile` flag outranks exported `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, while `AWS_PROFILE` in the environment loses to them. Never export credentials, and never export `AWS_PROFILE` in a loop: a loop that exported one profile after another once left the wrong account active and produced a `ClusterNotFoundException` that looked exactly like an infrastructure failure.
- **The agent that starts a session ends it** with `aws_session_end` when its AWS work is done. A worker starts its own session; it never ends someone else's.
- **Non-interactive workers never run the login.** When `aws_session_start` returns `[BLOCKED]`, the worker stops its AWS work and reports `BLOCKED: SSO login needed` to its caller; the calling workflow decides whether steps that need no AWS access continue (the Ask Angel dev verification records the running-image check as pending and goes on; stage and production workflows stay blocked). Only an interactive session with the human present calls `aws_session_login`, because the human approves it in a browser and the tool waits for that approval.
- **Never print secret values.** SSM `SecureString` values, access keys and passwords go into shell variables in the same command that uses them, never to stdout. Never run `aws configure export-credentials`.
- **Keep output small.** Always shape responses with `--query` and `--output text|table`, bound listings with `--max-items`, and bound log reads by time and count. A raw `describe-*` JSON dump is thousands of lines of context for one field.
- **Writes are named by the task.** `put-parameter`, `stop-deployment`, `create-user`, `create-access-key` and every other mutating call runs only when the task or the human asked for that specific change.

## Project Configuration

`aws_session_start` reads `.opencode/config/aws-sso.json` from the main checkout of the current repository (the session's project directory, or the `project` argument). It resolves the main checkout through the repository's common git directory, so the same file serves every linked worktree, where the gitignored `.opencode/config/` does not exist.

```json
{
  "ssoStartUrl": "https://<portal>.awsapps.com/start",
  "ssoRegion": "<Identity Center home region>",
  "environments": {
    "common": {
      "accountId": "222222222222",
      "roleName": "AdministratorAccess",
      "region": "eu-central-1"
    },
    "dev": {
      "accountId": "111111111111",
      "roleName": "AdministratorAccess",
      "region": "eu-central-1"
    }
  }
}
```

Where each value comes from:

| Key           | Source                                                                                                                                                       |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ssoStartUrl` | the AWS access portal URL the human signs into; the portal's "Access keys" dialog shows it as "SSO start URL". It cannot be discovered from a member account |
| `ssoRegion`   | the region of the organization's Identity Center instance; the same dialog shows it as "SSO Region"                                                          |
| `accountId`   | the project's Terraform (`aws_<env>_account_id`), or the account in `aws sts get-caller-identity`                                                            |
| `roleName`    | the permission set name, which is the middle of the assumed-role ARN: `assumed-role/AWSReservedSSO_<roleName>_<hash>/<user>`                                 |
| `region`      | the region the environment's resources run in                                                                                                                |

A missing file, a missing key, or an unknown environment name fails loudly with the path and the missing keys. The SSO session is named after the portal's host (`https://acme.awsapps.com/start` becomes `acme`), so projects on the same portal share one cached token and one login.

## Session Lifecycle

### Start

```
aws_session_start(environments: ["dev", "common"])
```

Pass `project` with a path inside the repository when the session's working directory is not that repository. The result:

```
[PASS] AWS session started; every profile verified

Session: my-backend-mono-20260922T192606Z-1597
Profiles: dev, common
Config file: /Users/<you>/.local/state/aws-session/my-backend-mono-20260922T192606Z-1597/config
Use: AWS_CONFIG_FILE=/Users/<you>/.local/state/aws-session/my-backend-mono-20260922T192606Z-1597/config aws --profile <profile> ...

| Profile | Identity |
| dev     | arn:aws:sts::111111111111:assumed-role/AWSReservedSSO_AdministratorAccess_0123456789abcdef/<user> |
| common  | arn:aws:sts::222222222222:assumed-role/AWSReservedSSO_AdministratorAccess_fedcba9876543210/<user> |
```

Each identity is a live `sts get-caller-identity`, so a `[PASS]` proves every profile works before any real call is made. Copy the `Config file` path; shell state does not persist between tool calls, so every command carries the `AWS_CONFIG_FILE=...` prefix.

| Result      | Meaning                                                                                             | Action                                                                                                              |
| ----------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `[PASS]`    | session created, every profile verified                                                             | use it                                                                                                              |
| `[BLOCKED]` | session created, a profile failed in a way a login can fix (missing, expired or stale token)        | interactive session with the human: `aws_session_login`; worker: stop the AWS work and report BLOCKED to the caller |
| `[FAIL]`    | session created, a profile failed in a way a login cannot fix (no access, bad profile, no endpoint) | read the failing identity line; the configuration or the role assignment is wrong                                   |
| tool error  | nothing created: missing or invalid `aws-sso.json`, unknown environment, not a repository           | read the message; it names the file and the missing keys or the unknown environment                                 |

A `[FAIL]` line such as `ForbiddenException ... GetRoleCredentials: No access` means the permission set is not assigned in that account or `roleName` is wrong; a login would not fix it. Report it.

### Login

```
aws_session_login(sessionId: "<session id>")
```

Runs `aws sso login` for the session's portal. The CLI opens the browser and the tool waits (up to ten minutes, the lifetime of the device authorization) until the human approves, then re-verifies every profile. One approval serves every session on that portal until the token expires, so parallel workers do not each need a login.

### End and list

```
aws_session_end(sessionId: "<session id>")
aws_session_list()
```

`aws_session_end` deletes the session directory. `aws_session_list` shows every session with its creation time, profiles and project; sessions left behind by dead agents appear there and can be ended by the human or the orchestrator that owns the run.

## Parallel Agents

Each agent that needs AWS starts its own session with its own environments; two workers on dev and stg never share a config file and never race on an exported variable. An orchestrator briefing a worker that needs AWS writes the environment list into the brief ("start an AWS session with `dev` only") and does not hand over its own session. The token cache is shared by design: identity is per human, environment is per session.

## Using Other Tools With a Session

Terraform and AWS SDK scripts read the same files. They take the profile from `AWS_PROFILE`, which exported credential variables outrank, so confirm none are set in that command:

```bash
env | grep -E '^AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)=' && echo "unset these first"
AWS_CONFIG_FILE=<session config> AWS_PROFILE=dev terraform plan
AWS_CONFIG_FILE=<session config> AWS_PROFILE=dev node scripts/some-sdk-script.js
```

Both Terraform's AWS provider and the AWS SDK for JavaScript v3 resolve `sso_session` profiles from the shared token cache. `language-terraform` owns how to plan (read-only), preview imports and apply against a live environment.

## Recipes

Every recipe below assumes `CF` is the session's `Config file` path, written out in the command, because no variable survives between tool calls:

```bash
CF=/Users/<you>/.local/state/aws-session/<session-id>/config
```

### ECS: rollout state and the running image

```bash
AWS_CONFIG_FILE=$CF aws --profile dev ecs describe-services --cluster <cluster> --services <service> \
  --query 'services[0].deployments[].{status:status,rollout:rolloutState,taskDef:taskDefinition,running:runningCount,desired:desiredCount,updated:updatedAt}' \
  --output table

TASK=$(AWS_CONFIG_FILE=$CF aws --profile dev ecs list-tasks --cluster <cluster> --service-name <service> \
  --desired-status RUNNING --query 'taskArns[0]' --output text)
AWS_CONFIG_FILE=$CF aws --profile dev ecs describe-tasks --cluster <cluster> --tasks "$TASK" \
  --query 'tasks[0].containers[].{name:name,image:image,status:lastStatus}' --output table
```

The image tag is the deployed commit or release; compare it with the merge commit SHA or the release tag. For stopped tasks, list with `--desired-status STOPPED` and read `tasks[].{reason:stoppedReason,containers:containers[].reason}`.

### ECS: the running task definition's environment

The proof that a configuration flag is live, not merely deployed:

```bash
TD=$(AWS_CONFIG_FILE=$CF aws --profile dev ecs describe-services --cluster <cluster> --services <service> \
  --query 'services[0].taskDefinition' --output text)
AWS_CONFIG_FILE=$CF aws --profile dev ecs describe-task-definition --task-definition "$TD" \
  --query 'taskDefinition.containerDefinitions[0].environment[?name==`<FLAG_NAME>`].value' --output text
```

### CloudWatch logs

```bash
AWS_CONFIG_FILE=$CF aws --profile dev logs describe-log-groups --log-group-name-prefix <prefix> \
  --query 'logGroups[].logGroupName' --output text

AWS_CONFIG_FILE=$CF aws --profile dev logs tail <log-group> --since 1h --filter-pattern ERROR --format short | tail -n 80

AWS_CONFIG_FILE=$CF aws --profile dev logs filter-log-events --log-group-name <log-group> --filter-pattern '"<exact text>"' \
  --start-time $(( ($(date +%s) - 3600) * 1000 )) --max-items 50 --query 'events[].message' --output text
```

Never pass `--follow` to `logs tail`; it never returns.

### CloudWatch Logs Insights

A query runs asynchronously: `start-query` returns an id, and `get-query-results` returns partial or empty results until its `status` is `Complete`. Poll the status; a fixed `sleep` either wastes time or reads an unfinished query as "no rows". Times are epoch seconds (not milliseconds, unlike `filter-log-events`), and `--log-group-names` takes several groups:

```bash
Q=$(AWS_CONFIG_FILE=$CF aws --profile dev logs start-query --log-group-names <group> [<group> ...] \
  --start-time $(( $(date +%s) - 3600 )) --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /<text>/ | sort @timestamp desc | limit 20' \
  --query queryId --output text)
until [ "$(AWS_CONFIG_FILE=$CF aws --profile dev logs get-query-results --query-id "$Q" --query status --output text)" = "Complete" ]; do sleep 2; done
AWS_CONFIG_FILE=$CF aws --profile dev logs get-query-results --query-id "$Q" --output json \
  | jq -c '.results[] | map(select(.field != "@ptr") | {(.field): .value}) | add'
```

- Each result row is a list of `{field, value}` pairs; the `jq` line flattens a row into one object and drops the `@ptr` pointer.
- Field names with dots or dashes need backticks inside the query string: `` `attributes.http.route` ``. Keep the query in single quotes so the shell leaves the backticks alone; when the query has to interpolate a shell variable, switch to double quotes and escape each backtick as `` \` ``.
- A `@ptr` value opens the whole record: `logs get-log-record --log-record-pointer "<@ptr>" --query 'logRecord."@message"' --output text`. It shows every attribute a record really carries, which is the fastest way to find the field a query or a dashboard widget should filter on.
- A dashboard's log widget is an ordinary Logs Insights query. To check a widget that shows nothing, read the query from `cloudwatch get-dashboard --dashboard-name <name> --query DashboardBody --output text` and run it with this recipe: no rows means no data or a wrong filter, and an error means the query itself is broken.

### Traces: from an error response to its spans (X-Ray Transaction Search)

With Transaction Search on, every span is a JSON record in the `aws/spans` log group (created by X-Ray, 30-day retention), so a trace is read with the Logs Insights recipe above. The fields that matter:

| Field                                                                       | Holds                                                                                                  |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `traceId`, `spanId`, `parentSpanId`                                         | the W3C ids; the root span has no `parentSpanId`                                                       |
| `kind`                                                                      | `SERVER`, `CLIENT`, `PRODUCER`, `CONSUMER`, `INTERNAL`                                                 |
| `name`                                                                      | the span name; an HTTP server span is often just `<METHOD> /<prefix>` and says little                  |
| `` `resource.attributes.service.name` ``                                    | the service that emitted the span                                                                      |
| `` `attributes.aws.local.operation` ``                                      | the Application Signals operation, `<METHOD> <route template>`; the best filter for one endpoint       |
| `` `attributes.http.route` ``, `` `attributes.http.response.status_code` `` | the matched route and the response status                                                              |
| `` `attributes.db.system.name` ``, `` `attributes.db.statement` ``          | the database client spans (Postgres is `postgresql`) and their SQL; connection spans have no statement |
| `status.code`                                                               | `ERROR`, `OK` or `UNSET`                                                                               |
| `startTimeUnixNano`, `durationNano`                                         | ordering and duration; `durationNano / 1000000` is milliseconds                                        |

The path from a failed request to its cause:

1. Take the request id from the error response body or the load balancer's `X-Amzn-Trace-Id` header. On AWS load balancers it has the X-Ray shape `Root=1-<8 hex>-<24 hex>`, which is not the span `traceId` (32 hex).
2. Find the application's log lines for it with `logs filter-log-events --filter-pattern '"Root=1-..."'` on the service's log group. A structured logger wired to OpenTelemetry writes the OTel `traceId` and `spanId` on the same line, next to the stack trace.
3. Read the trace, in order:

   ```bash
   --log-group-names aws/spans --query-string 'filter traceId = "<32 hex>"
     | fields startTimeUnixNano, `resource.attributes.service.name` as svc, kind, name, `attributes.aws.local.operation` as op,
       durationNano / 1000000 as ms, status.code as status, `attributes.db.statement` as sql
     | sort startTimeUnixNano asc | limit 100'
   ```

Useful span-wide queries over a recent window:

```
stats count(*) as spans by `resource.attributes.service.name`, kind | sort spans desc
stats count_distinct(`resource.attributes.service.name`) as services, count(*) as spans by traceId | filter services > 1 | sort spans desc | limit 5
filter `attributes.aws.local.operation` = "<METHOD> <route>" | fields traceId | limit 1
filter `attributes.db.system.name` = "postgresql" and ispresent(`attributes.db.statement`) | stats count(*) as calls, pct(durationNano, 95) / 1000000 as p95_ms by `attributes.db.statement` | sort p95_ms desc | limit 10
```

The second query finds traces that crossed services (an HTTP call to another service, or a queue message that carried the trace context to a worker); an asynchronous consumer's spans appear under the producer's `traceId` only when the consumer extracts the context from the message attributes.

Application Signals aggregates the same spans into per-operation metrics in the `ApplicationSignals` namespace (`Latency`, `Fault` for 5xx, `Error` for 4xx; dimensions `Service`, `Operation`, `Environment`), and `application-signals list-service-operations --key-attributes Type=Service,Name=<service>,Environment=<env> --start-time <epoch> --end-time <epoch>` lists the operations it has seen.

### CloudWatch metrics

A health snapshot is a handful of `get-metric-statistics` calls. macOS `date` takes `-v-1H` for "one hour ago":

```bash
START=$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ); END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
AWS_CONFIG_FILE=$CF aws --profile dev cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name CPUUtilization \
  --dimensions Name=ClusterName,Value=<cluster> Name=ServiceName,Value=<service> \
  --start-time "$START" --end-time "$END" --period 300 --statistics Average Maximum \
  --query 'sort_by(Datapoints,&Timestamp)[].[Timestamp,Average,Maximum]' --output text
```

| Signal               | Namespace    | Metric                                                                | Dimensions                   |
| -------------------- | ------------ | --------------------------------------------------------------------- | ---------------------------- |
| service CPU / memory | `AWS/ECS`    | `CPUUtilization`, `MemoryUtilization`                                 | `ClusterName`, `ServiceName` |
| database load        | `AWS/RDS`    | `CPUUtilization`, `DatabaseConnections`, `ServerlessDatabaseCapacity` | `DBClusterIdentifier`        |
| database latency     | `AWS/RDS`    | `ReadLatency`, `WriteLatency`, `CommitLatency`                        | `DBClusterIdentifier`        |
| Lambda health        | `AWS/Lambda` | `Errors`, `Invocations`, `Duration`, `Throttles`                      | `FunctionName`               |

### SSM parameters

```bash
AWS_CONFIG_FILE=$CF aws --profile dev ssm get-parameters-by-path --path /<app>/ --recursive \
  --query 'Parameters[].Name' --output text

AWS_CONFIG_FILE=$CF aws --profile dev ssm get-parameter --name /<app>/<plain-name> --query Parameter.Value --output text
```

A `SecureString` is read into a variable and used in the same command, never echoed:

```bash
PGPASSWORD=$(AWS_CONFIG_FILE=$CF aws --profile dev ssm get-parameter --name /<app>/rds/api/password \
  --with-decryption --query Parameter.Value --output text) <command that consumes PGPASSWORD>
```

Writing (only when the task names the parameter and the value's source):

```bash
AWS_CONFIG_FILE=$CF aws --profile dev ssm put-parameter --name /<app>/<name> --type SecureString --value "$VALUE" --overwrite
```

### CodeDeploy

```bash
AWS_CONFIG_FILE=$CF aws --profile dev deploy list-applications --output text
AWS_CONFIG_FILE=$CF aws --profile dev deploy list-deployment-groups --application-name <app> --output text
AWS_CONFIG_FILE=$CF aws --profile dev deploy list-deployments --application-name <app> --deployment-group-name <group> \
  --include-only-statuses InProgress Failed --max-items 3 --query 'deployments' --output text
AWS_CONFIG_FILE=$CF aws --profile dev deploy get-deployment --deployment-id <id> \
  --query 'deploymentInfo.{status:status,created:createTime,completed:completeTime,error:errorInformation}' --output json
```

Stopping a stuck deployment is a write and rolls back:

```bash
AWS_CONFIG_FILE=$CF aws --profile dev deploy stop-deployment --deployment-id <id> --auto-rollback-enabled
```

### ECR images

Images usually live in a shared `common` account, not in the environment account:

```bash
AWS_CONFIG_FILE=$CF aws --profile common ecr describe-images --repository-name <repo> --image-ids imageTag=<tag> \
  --query 'imageDetails[0].{tags:imageTags,pushed:imagePushedAt}' --output json
```

### IAM user onboarding

All writes; run them only in the account the task names:

```bash
AWS_CONFIG_FILE=$CF aws --profile <env> iam list-users --query 'Users[].UserName' --output text
AWS_CONFIG_FILE=$CF aws --profile <env> iam list-groups --query 'Groups[].GroupName' --output text
AWS_CONFIG_FILE=$CF aws --profile <env> iam create-user --user-name <first-last> --query 'User.Arn' --output text
AWS_CONFIG_FILE=$CF aws --profile <env> iam add-user-to-group --user-name <first-last> --group-name <group>
AWS_CONFIG_FILE=$CF aws --profile <env> iam create-login-profile --user-name <first-last> --password "$TEMP_PASSWORD" --password-reset-required
```

`iam create-access-key` returns the secret once. The command that asked for the key says where it goes; the secret never lands in a repository file or in the agent's reply beyond that destination.

## Failure Modes

| Symptom                                                                                                                                                          | Cause                                                                                                 | Fix                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `Error loading SSO Token: Token for <portal> does not exist`, `Token has expired and refresh failed`, `The SSO session associated with this profile has expired` | no login yet, or the token expired                                                                    | interactive: `aws_session_login`; worker: report BLOCKED                                                      |
| `ClusterNotFoundException`, `ServiceNotFoundException`, `RepositoryNotFoundException`, `ParameterNotFound`                                                       | usually the wrong account: runtime resources sit in environment accounts, images in `common`          | `aws sts get-caller-identity --profile <p>` through the session and compare the account before suspecting AWS |
| `InvalidClientTokenId` or `ExpiredToken` on a command that used the session                                                                                      | exported credential variables outranked the profile (the command used `AWS_PROFILE`, not `--profile`) | switch to `--profile`, or unset the exported variables                                                        |
| `ForbiddenException ... GetRoleCredentials: No access`                                                                                                           | the permission set is not assigned in that account, or `roleName` is wrong                            | fix `aws-sso.json`; report if the assignment itself is missing                                                |
| `AccessDenied` on a specific action                                                                                                                              | the permission set lacks that action                                                                  | report it; do not look for another role                                                                       |
| a command never returns                                                                                                                                          | a pager or `--follow`                                                                                 | session profiles set an empty `cli_pager`; outside a session prefix `AWS_PAGER=""`; drop `--follow`           |
| `aws_session_start` returns `[BLOCKED]` whose identity line is only a quoted hex string, such as `aws: [ERROR]: 'd7d60cfd79ff...'`                               | a stale entry in the SSO token cache: the CLI prints the cache key instead of an error message        | a login fixes it: interactive `aws_session_login`; worker: report BLOCKED                                     |
| a Logs Insights query returns no rows right after `start-query`                                                                                                  | the results were read before the query's `status` was `Complete`                                      | poll the status, as in the Logs Insights recipe                                                               |

## Anti-Patterns

- Pasting access keys or session tokens into a config file for the agent to read
- One long-lived shared profile that every agent switches with `export AWS_PROFILE=...`
- `AWS_PROFILE=<env>` on a CLI call instead of `--profile <env>` (exported keys silently win)
- Starting a session with `prod` "just in case"
- A worker calling `aws_session_login` in a non-interactive run and hanging on the browser flow
- Echoing a `SecureString`, an access key, or `aws configure export-credentials` output
- Unshaped `describe-*` or log output dumped into the context
- Reading a not-found error as an outage before checking which account the profile resolved to
- Ending another agent's session, or leaving your own behind

## Rules

- AWS access is the `aws` CLI plus a session from `aws_session_start`; no tool wraps an AWS API, no pasted credentials
- One session per agent per task, only the environments the work needs; `stg`/`prod` only when the task targets them
- Every call: `AWS_CONFIG_FILE=<session config> aws --profile <env> ...`
- `[BLOCKED]` from `aws_session_start` means login: the human approves `aws_session_login` in an interactive session; workers stop the AWS work and report BLOCKED, and the calling workflow decides what else continues
- End your own session when the AWS work is done; never end another agent's
- Secrets go into variables consumed in the same command, never to stdout
- Shape every response with `--query`, bound listings and log reads
- Mutating calls run only when the task names the change
- A not-found error is checked against the resolved account before anything else
