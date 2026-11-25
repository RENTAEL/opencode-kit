---
name: condense
description: "Operator-triggered six-prong sweep. Scope: SPEC.md + `SPEC.archive.md` + `.opencode/check-extras.md`. Not auto-fire ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the check skill emits advisory when token estimate > 20k; operator invokes next turn. Single atomic commit (all firing prongs or none); rollba..."
---
# condense ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SPEC.md condenser

Operator-triggered six-prong sweep. Scope: SPEC.md + `SPEC.archive.md` + `.opencode/check-extras.md`. Not auto-fire ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the check skill emits advisory when token estimate > 20k; operator invokes next turn. Single atomic commit (all firing prongs or none); rollback `git revert`. Writes serialize main-thread; per-prong scan reads delegable to sub-agents.

## LOAD

1. Read `SPEC.md`. Missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "no spec, nothing to condense." Stop.
2. Read `skills/spec/SPEC-FORMAT.md` (deployed to `~/.opencode/skills/spec/SPEC-FORMAT.md`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â row schema + section catalog.
3. Baseline tokens = bytes / `check-mechanical.py` `TOKEN_RATIO` (single source; not hardcode divisor). Record.

## PROPOSE

Six prongs, execution order 1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 6. Per prong: scan SPEC.md for trigger match; emit firing-set + skip-set w/ 1-line rationale each.

Script modes below run `python3 ~/.opencode/scripts/check-mechanical.py <mode>`.

### Prong 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V fold-first sweep

Fold pattern-mirrored sibling Ãƒâ€šÃ‚Â§V rows into target row inline. Seed script-computed: `check-mechanical.py emit-fold-seeds` emits `cluster_members|co_citers` table ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â connected components of live Ãƒâ€šÃ‚Â§V rows sharing a citer (Ãƒâ€šÃ‚Â§T `cites` or Ãƒâ€šÃ‚Â§B `fix` naming ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 2 live Ãƒâ€šÃ‚Â§V rows). Seed advisory not auto-apply: co-citation is candidacy signal not proof; operator confirms each fold @ CONFIRM (LLM judges topic coherence). Augment seed w/ topic-keyword overlap (shared scope tokens / procedure refs / verb pattern) where co-citation thin. Fires first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fold reshapes later prongs (prong 6 inherits folded shape).

### Prong 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SUPERSEDED Ãƒâ€šÃ‚Â§T inline marker

Candidates script-computed: `check-mechanical.py emit-superseded` emits `tid|superseded_v|original_cites` table ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â closed Ãƒâ€šÃ‚Â§T (status `x`) whose Ãƒâ€šÃ‚Â§V cite resolves into no live Ãƒâ€šÃ‚Â§V row (only archived Ãƒâ€šÃ‚Â§V.retired block or nowhere) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SUPERSEDED candidate. Live-only resolution ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â distinct from cite-DAG audit live+archive scope. Consume table; not by-hand per-cite resolution. Operator confirms each (content-amend-away not cite-detectable). Replace task body wholesale: `T<n>|x|SUPERSEDED ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V.<m> amend|<original cites>`. Preserves row id; closes cite-DAG-miss audit noise.

### Prong 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§T/Ãƒâ€šÃ‚Â§B window-vs-archive split

Trigger: closed Ãƒâ€šÃ‚Â§T rows > 50. Older closed rows ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `SPEC.archive.md` (repo-root sibling, committed, id ascending). Ãƒâ€šÃ‚Â§T/Ãƒâ€šÃ‚Â§B gain per-section marker `## archived: Ãƒâ€šÃ‚Â§<S>.<a>..Ãƒâ€šÃ‚Â§<S>.<b> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SPEC.archive.md (<n> rows)`. Archive carries verbatim row text. The check skill cite-DAG sweep eager-probes archive; archived rows stable so memo HOLD-SINCE-CLEAN across runs.

### Prong 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â history-residue prune

Prune history residue across live Ãƒâ€šÃ‚Â§V/Ãƒâ€šÃ‚Â§T/Ãƒâ€šÃ‚Â§B row bodies ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SPEC.md is clean current design; history lives in commit log + archive. Pattern set single-sourced by freshness-contract invariant (shared w/ check skill audit + spec skill write-time prune):

- amendment-counter `(ÃƒÂ¢Ã‹â€ Ã¢â‚¬Â )` markers ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ drop.
- `retired YYYY-MM-DD` clause inlined in live row ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ drop (wholesale-retired row is reorganize archival job).
- supersession-narration ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ drop: `pre-amend ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`, `prior ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ retired/dropped/superseded`, recurrence-class lineage, surfaced-by prose. Commit msg + `Ãƒâ€šÃ‚Â§B.cause`/`Ãƒâ€šÃ‚Â§T.cites` cite-DAG preserve narrative.
- standalone `Closes Ãƒâ€šÃ‚Â§B.<x>` sentence ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `(closes Ãƒâ€šÃ‚Â§B.<x>)` suffix on prior clause.

**Ãƒâ€šÃ‚Â§T body-trim** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â owned here because the build skill flips status cell only, so Ãƒâ€šÃ‚Â§T body not reachable by spec skill write-time prune: oversized `task` cell carrying step-by-step transcript ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ one-line goal; surplus ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commit-msg body. Mirrors Ãƒâ€šÃ‚Â§B `cause` one-line trim.

Pre-filters (match exempt): backtick-wrapped tokens (pattern-definition rows not self-flag); cite-modifier `Ãƒâ€šÃ‚Â§V.<n>(ÃƒÂ¢Ã‹â€ Ã¢â‚¬Â )`; wholesale-retired `V<n>: retired YYYY-MM-DD` rows pending reorganize. Verbatim-preservation holds: code, paths, URLs, identifiers, error strings, regex.

### Prong 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V prose ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ telegraph rewrite

Rewrite embedded English connectives per telegraph skill. Targets: `Why:`, `For example`, `In other words`, explanatory `because` / `due to` clauses. Verbatim-preservation holds: code, paths, URLs, identifiers, numbers, versions, error strings, SQL, regex, JSON, YAML, quoted strings.

### Prong 6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V audit-recipe extraction

Heavy set script-computed: `check-mechanical.py emit-v-weights` emits `v_row|bytes|tokens|cum_pct|heavy` table, heaviest first; heavy = top rows whose cumulative weight first reaches ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 50% of Ãƒâ€šÃ‚Â§V-section total (tie-break descending weight then ascending id ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run-stable). Not by inspection. Heavy rows: extract audit-recipe content ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.opencode/check-extras.md` (REPO-LOCAL extension); SPEC.md row keeps 1-line ref. Check skill loader already path-probes `.opencode/check-extras.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no check-skill amend.

## CONFIRM

Always fires post-PROPOSE. Single bulk AskUserQuestion covers full sweep ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â mid-flow re-prompt not allowed:

- **question**: `Condense SPEC.md: prongs {<firing-set>} firing, {<skip-set>} skipped. Baseline ~<n>k tokens, est. ~<m>k post-sweep. Apply?`
- **header**: `Condense gate`
- **options** (4, mutually exclusive, label is action description):
  - `apply all firing prongs` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ EXECUTE full firing set.
  - `force-skip prong 3` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ EXECUTE minus prong 3 (archive split deferred; prong 3 load-bearing so explicit override).
  - `subset` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ user supplies N in {1..6} via Other-typed input; EXECUTE prong N only.
  - `cancel` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no mutation; PROPOSE report retained as final output.

## EXECUTE

Single atomic commit:

1. Apply firing prongs in order (1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 6 minus skips).
2. Prong 3 fired ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `git add SPEC.archive.md`.
3. Prong 6 fired ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `git add .opencode/check-extras.md`.
4. Prong 1 fired ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ cite-DAG sweep same commit; touch REPO-LOCAL citers renumbered by fold.
5. Stage remaining artifacts + `SPEC.md` (`git add`), then path-scoped commit `git commit -m <subject> -- <staged artifacts> SPEC.md` (write-ownership invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â commit scopes to staged owned set, pre-staged files never leak; `-m` flags ! precede `--`); auto-commit msg `condense SPEC.md: prongs {<firing-set>} (~<n>k ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ~<m>k tokens)`; no user prompt.

EXECUTE ends @ commit. Rollback `git revert <condense-sha>`. Drift cascade ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Next-block item #1; operator dispatches next turn.

## MECHANIZE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â script-candidate scan

Recipe end ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ before the `## Next` block, scan this run for a mechanization candidate. Candidate = any of:

- ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit exactly one `## Next` item naming the observed pattern + proposed script mode; none ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no item. Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants). Route by cwd:

- dev repo (this skill pack) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new Ãƒâ€šÃ‚Â§T row
- consumer repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.opencode/check-extras` row

## OUTPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Next" block

Heading `## Next`; 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `invoke the <skill-name> skill [args]`). Optional `## Hint` (ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 3 lines) precedes when item selection needs hidden state. State-mutator ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ post-EXECUTE prefer invoking the check skill (confirm cite-DAG + format-layer + token-budget clean).

Example after EXECUTE (firing-set {1,2,3,4,5}; commit auto-fired):

```
## Next

1. invoke the check skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cascade scan over condensed SPEC.md
2. invoke the build skill --next ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â start the next pending Ãƒâ€šÃ‚Â§T row
3. git revert <condense-sha> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rollback if condensation breaks downstream
```

Variants: CONFIRM cancel (no commit) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ swap item 1 for: invoke the condense skill (re-run to apply after spec review), drop item 3. CONFIRM subset ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Next-block unchanged.

## NON-GOALS

- not auto-fire ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the check skill emits advisory; operator invokes the condense skill next turn.
- not partial commit ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every firing prong applies or none.
- not retune thresholds (20k-token advisory, > 50 closed-Ãƒâ€šÃ‚Â§T archive trigger) in this skill body ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â canonical values live in the token-budget-condense invariant row (SPEC.md) w/ mechanical mirrors in `check-mechanical.py` constants; retune via invoking the spec skill AMEND + sync the script constant same commit.