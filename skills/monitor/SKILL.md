---
name: monitor
description: "Auto-fire sub-skill, 5th member of the sub-skill-flags family (telegraph, backprop, socratic, steno, monitor). No hook ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the skills-only invariant bans runtime interception; monitor = LLM self-report, not a wrapper. Ships PUBLISHED to every consumer ÃƒÂ¢Ã¢â‚¬Â..."
---
# monitor ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skill-deviation capture ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skill-pack-repo issue

Auto-fire sub-skill, 5th member of the sub-skill-flags family (telegraph, backprop, socratic, steno, monitor). No hook ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the skills-only invariant bans runtime interception; monitor = LLM self-report, not a wrapper. Ships PUBLISHED to every consumer ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ every skill pack user is a data source.

Trigger lives in this frontmatter description only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â zero edits to existing skill bodies (byte-identical). Body LLM-facing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ telegraph.

## WHEN ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fires mid-skill-run when an sdd skill deviates:

- instruction ambiguous or self-contradictory
- recipe loop step impossible as written
- prescribed tool / flag fails
- user corrects the skill's behavior

Not: consumer-repo code bugs, env breakage unrelated to an sdd skill, operator typo. No deviation ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no fire.

## PROTOCOL ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ordered, stop on bail:

1. **CAPTURE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skill name + skill pack version + expected (quoted skill-body line) vs actual + minimal excerpt. Version ÃƒÂ¢Ã¢â‚¬Â Ã‚Â `git describe --tags --always` in the skill pack repo (fallback `unknown`). If running from a cloned skill pack, `cd` to its root for the version query; otherwise use `unknown`.
2. **REDACT** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â strip consumer-repo paths, code, identifiers, URLs; only the sdd skill-body text + deviation description survive. Mandatory pre-publish (monitor-protocol invariant) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â excerpts originate in third-party repos.
3. **ROUTE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cwd == skill pack repo? `git remote get-url origin` resolves to the skill pack's GitHub repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ dev repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ hand off to backprop (backprop-protocol invariant): Ãƒâ€šÃ‚Â§B row, no issue filed. Stop. Else consumer repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ continue.
4. **TARGET** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â issue repo ÃƒÂ¢Ã¢â‚¬Â Ã‚Â skill pack repo URL parsed to `owner/repo`. Determined from `git remote get-url origin` within the skill pack directory, or hardcoded as `kborovik/.dotfiles` as fallback (parametric-recipe invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the repo URL is sourced from git, not hardcoded in this body).
5. **DEDUP** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `gh issue list --repo <target> --search "<skill> <keywords>"`. Hit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ comment path. Miss ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new-issue path.
6. **GATE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â AskUserQuestion before any gh write (decision-gate invariant). Header `Skill deviation`, question body surfaces the resolved `--repo <target>` verbatim (operator confirms exact write destination before any publish); mutually-exclusive labels: `File issue` (miss), `Comment` (hit), `Skip`. No auto-file path exists.
7. **WRITE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â immediately pre-write assert resolved `--repo` == `<target>` (= skill pack repo URL, step 4); mismatch ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ abort, no gh write (monitor-protocol invariant). Then per gate selection:
   - miss + File issue ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `gh issue create --repo <target> --title "<skill>: <deviation summary>" --body <steno>` (github-facing-register ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ steno per steno skill).
   - hit + Comment ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `gh issue comment <n> --repo <target> --body <steno occurrence>` (occurrence count = signal; one issue per deviation class).
   - Skip ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ nothing written.

## DISPATCHED ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `mechanization-candidate` entry path

Second entry path, not auto-fire (mechanize-scan invariant). Engaged from a user-invocable recipe's MECHANIZE `## Next` item ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â consumer repo only. Carries the observed pattern + proposed script mode, not a deviation ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no CAPTURE, no WHEN trigger. Skips the dev-repo backprop hand-off: mechanize-scan routes a dev-repo candidate to invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Ãƒâ€šÃ‚Â§T row and a consumer repo one to the consumer invoking the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ extras row; only the consumer case reaches here, so no ROUTE step.

Ordered, stop on bail:

1. **REDACT** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â strip consumer-repo paths, code, identifiers, URLs; only the observed pattern + proposed script mode survive. Mandatory pre-publish (monitor-protocol invariant) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â candidate originates in a third-party repo.
2. **TARGET** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â issue repo ÃƒÂ¢Ã¢â‚¬Â Ã‚Â skill pack repo URL parsed to `owner/repo`. Same resolve as the auto-fire path ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â git remote owns the slug (parametric-recipe invariant), no hardcoded slug.
3. **DEDUP** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `gh issue list --repo <target> --search "<skill> mech candidate <keywords>"`. Hit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ comment path. Miss ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new-issue path. One issue per candidate class ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â recurrence comments, never duplicates.
4. **GATE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â AskUserQuestion before any gh write (decision-gate invariant). Header `Mech candidate`, question body surfaces the resolved `--repo <target>` verbatim (operator confirms exact write destination before any publish); mutually-exclusive labels: `File issue` (miss), `Comment` (hit), `Skip`. No auto-file path exists.
5. **WRITE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â immediately pre-write assert resolved `--repo` == `<target>` (= skill pack repo URL, TARGET step); mismatch ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ abort, no gh write (monitor-protocol invariant). Then per gate selection:
   - miss + File issue ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `gh issue create --repo <target> --title "<skill>: mech candidate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <pattern>" --body <steno>` (github-facing-register ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ steno per steno skill; body = observed pattern + proposed script mode).
   - hit + Comment ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `gh issue comment <n> --repo <target> --body <steno occurrence>` (occurrence count = signal; one issue per candidate class).
   - Skip ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ nothing written.

## REDACTION ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mandatory

Survives: sdd skill name + skill pack version, the quoted sdd skill-body line, deviation description.
Stripped: consumer file paths, code snippets, identifiers (names, secrets, consumer repo slug), URLs.
Excerpt originates in a third-party repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ strip first, publish second. Uncertain a token is safe ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ drop it.

## DEV-REPO ROUTING

cwd == skill pack repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ an out-of-repo issue is the wrong channel: backprop owns dev-repo capture (Ãƒâ€šÃ‚Â§B row), and a mirrored issue duplicates that record against the freshness contract. Hand off to backprop, file no issue.

## NON-GOALS

- no hook / runtime interception (skills-only invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no hooks).
- no auto-file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every gh write operator-gated; silent publish impossible (decision-gate invariant).
- no CI / scheduled filing, no telemetry, metrics, or dashboards.
- never edits SPEC.md or any skill body ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â existing skills stay byte-identical.