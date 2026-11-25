---
name: lh-data-pipelines
description: "Before writing a pipeline, profile the source: what each field actually means (not what its name suggests), its ranges, its nulls, its duplicates, its encoding, how it's generated and how often it lies. Most pipeline bugs are misunderstandings of the source dressed up as code ..."
---
## Critical Patterns

### 1. Understand the data before you move it

Before writing a pipeline, profile the source: what each field actually means
(not what its name suggests), its ranges, its nulls, its duplicates, its
encoding, how it's generated and how often it lies. Most pipeline bugs are
misunderstandings of the source dressed up as code bugs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the "amount" column
that's sometimes cents and sometimes dollars, the timestamp in three timezones,
the "unique" id that isn't. Curiosity here is cheaper than debugging downstream.

### 2. Validate at the boundary ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â data contracts, not hope

Every pipeline stage that ingests data checks it against an explicit contract:
expected schema, types, ranges, nullability, referential integrity. Bad data is
caught and quarantined at the door, not discovered three tables downstream as a
wrong dashboard number. This is [lh-fullstack-boundaries](../../../senior-dev/skills/lh-fullstack-boundaries/SKILL.md)
applied to data: the source is untrusted until validated, and a silent bad row
is worse than a loud rejected one because it poisons everything computed from it.

### 3. Idempotent and reprocessable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run it twice, same result

Pipelines fail and get re-run; a stage that double-counts on re-run or corrupts
on partial failure is a data-integrity time bomb. Design each stage to be
idempotent (re-running produces the same state, not duplicates) and able to
reprocess a date range without manual surgery. When a bug ships in the
transform logic, you WILL need to reprocess history ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â build for that day from
the start.

### 4. Prefer ELT and keep the raw layer immutable

Land raw source data untouched first (immutable, append-only), then transform
into cleaned/modeled layers on top. Two payoffs: when transform logic has a bug
(it will), you reprocess from raw instead of re-fetching from a source that may
have changed; and the raw layer is your audit trail of what actually arrived.
Transforming-on-ingest and discarding the original throws away your only ground
truth.

Immutable is not forever, and personal data is where that bites. Minimize at
landing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a field you don't land can't leak and needs no deletion; give the
raw layer a retention period with a date, not "keep everything"; and design
the deletion path before the first byte arrives, because an erasure request
applies to raw and to every layer and cache built from it. Append-only
storage needs a way to make one subject's data unreadable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a partition per
subject that can be dropped, or per-subject encryption keys you can destroy ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
or it can't honour one.

### 5. Model storage for how it's read, name it for humans

Choose storage by access pattern: OLTP database for transactional app reads
(that model belongs to [dba/lh-data-modeling](../../../dba/skills/lh-data-modeling/SKILL.md)
ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â you read from it, you don't reshape it), columnar warehouse for
analytics/aggregation, object storage for big/raw/blobs.
Don't run analytics queries against the production OLTP database ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â you'll hurt
the app and the query. Model the analytical layer for the questions asked
(star-ish schemas, sensible grain) and name tables/columns so an analyst
understands them without a decoder ring ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â undocumented cryptic schemas are where
data trust goes to die.

### 6. Observe data like you observe services

Data pipelines fail silently in a way services don't: they keep running and
produce wrong numbers. Add data-specific monitoring ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â freshness (did today's
data arrive?), volume (row count in expected range, not suddenly half?),
distribution (did a key metric's shape shift?), and null/duplicate rates.
This is [lh-observability](../../../devops/skills/lh-observability/SKILL.md) for
data: the alert you want is "the numbers look wrong" BEFORE a stakeholder sees
the wrong number in a report.

## Resources

- Sibling skills: [lh-ml-modeling](../lh-ml-modeling/SKILL.md) (the consumer of clean
  data ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â garbage in, garbage out starts here), [lh-llm-integration](../lh-llm-integration/SKILL.md)
  (retrieval data needs the same rigor)
- Boundary/observability discipline: [senior-dev/lh-fullstack-boundaries](../../../senior-dev/skills/lh-fullstack-boundaries/SKILL.md),
  [devops/lh-observability](../../../devops/skills/lh-observability/SKILL.md)
