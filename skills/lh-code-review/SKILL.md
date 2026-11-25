---
name: lh-code-review
description: "_Verified against Xcode 26 / iOS 26 / macOS 26 (September 2026). Apple moves these facts yearly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the year has changed, re-check a claim before teaching it._"
---
_Verified against Xcode 26 / iOS 26 / macOS 26 (September 2026). Apple moves
these facts yearly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the year has changed, re-check a claim before teaching it._

## Critical Patterns

### 1. Review in three passes, report by severity

Pass 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **correctness & safety** (ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´): retain cycles, force unwraps, data
races, main-thread violations, leaked resources. Pass 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **design** (ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡):
logic in views, missing abstractions, state ownership, testability. Pass 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
**style** (ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¢): naming, idiom, formatting. Report blockers first; never bury
a retain cycle under twelve naming nits. Every finding carries its failure
case ("this closure captures self strongly; when X outlives Y, the whole
graph leaks") ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and when the code is genuinely good, say WHAT is good with
the same precision.

### 2. The Swift-specific ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ checklist

- **Retain cycles**: `self` captured strongly in escaping closures stored by
  `self` (handlers, subscriptions, timers); delegates declared strong. A
  bare `Task { }` retains `self` only until it finishes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that is not a
  cycle; the leak needs BOTH `self` storing the task AND the task never
  completing (an endless `for await`). `[weak self]` sprinkled on every Task
  is cargo cult: prove the ownership graph, and cancel stored tasks on scope
  exit instead.
- **Force unwraps** (`!`, `try!`, `as!`): each one is a crash with a date TBD.
  Acceptable only with a written invariant ("IBOutlet after viewDidLoad") ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
  otherwise `guard let` with a real fallback path.
- **Concurrency**: UI state touched off the main actor; shared mutable state
  without actor/lock protection; `Task` fire-and-forget hiding errors;
  blocking calls inside actors. In Swift 6 language mode, isolation and
  Sendable violations are compile errors; blocking inside an actor and
  fire-and-forget Tasks are NOT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the compiler is an ally for the first two
  only. And under Xcode 26's MainActor default with caller-actor async, the
  new ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ runs the other way: heavy work silently on main because nobody
  marked it `@concurrent` (see [lh-state-architecture #6](../lh-state-architecture/SKILL.md)).
- **Error swallowing**: `try?` discarding errors the user needs to see;
  empty catch blocks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an error that vanishes silently becomes QA's
  [lh-flow-hunting](../../../qa/skills/lh-flow-hunting/SKILL.md) finding later.

### 3. The SwiftUI ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ checklist

- **Logic in the view**: formatting, filtering, network calls inline in
  `body` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ belongs in the ViewModel/model; `body` is a pure function of
  state, and every recomputation runs it.
- **State ownership**: `@State` for view-local only; one source of truth per
  piece of state ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â two views each "owning" a copy is the bug factory;
  `@Binding` down, not state duplicated down.
- **Observation hygiene**: with `@Observable`, a view re-evaluates only when
  a property its `body` READ changes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â so "re-renders on unrelated changes"
  is the `ObservableObject`/`@Published` smell (any published change
  invalidates every observer), and `ObservableObject` in new code is the
  finding. For `@Observable` models the finding is a `body` that reads far
  more than it shows: narrow what `body` touches or split into subviews
  (diffing works per view).
- **SwiftData**: `ModelContext` or `@Model` objects crossing actors ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ (not
  Sendable); `@Query` inside a ViewModel ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ (view-only, main-actor);
  relationships without delete rules ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡; a schema change in a shipped app
  without a `VersionedSchema` + migration plan ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that is a crash on
  upgrade, not on first install.
- **Untested-by-omission** ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡: a ViewModel behind a protocol-fronted service
  with no Swift Testing target is testability that never cashed in; and a
  `@MainActor` ViewModel's tests are `@MainActor`/awaited or they don't
  compile in Swift 6.
- **The missing states**: view renders happy path only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â where are loading,
  empty, error? (The screen-state enum from
  [lh-state-architecture](../lh-state-architecture/SKILL.md), and the ux-ui
  [five states (`lh-ux-flows`)](../../../ux-ui/skills/lh-ux-flows/SKILL.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â same table.)

### 4. Platform-honesty: iOS code isn't Mac code automatically

When the target includes macOS: check window/scene assumptions (Mac has many
windows, resizable), keyboard/menu/right-click support, `NavigationSplitView`
over stack navigation for wide layouts, sandbox entitlements for file access.
Flag "iOS-shaped" code shipped to Mac as ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it runs, and it feels like a
port, which Mac users smell instantly.

### 5. Review as teaching: pattern over instance

The user's growth beats the diff. When the same mistake appears three times,
teach the PATTERN once (with the underlying rule: "closures that outlive the
call need an ownership decision") instead of flagging three instances ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â then
have them find the third occurrence themselves. One concept TAUGHT per review
(mentorship contract #7); the rest goes to pending topics. That limits the
teaching, never the report: every blocker is named in this review, whatever
the count ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a crash moved to pending topics is a crash shipped.

## Resources

- Sibling skills: [lh-state-architecture](../lh-state-architecture/SKILL.md) (where
  the design findings point), [lh-debugging](../lh-debugging/SKILL.md) (when a
  finding needs a repro)
- Generic review altitude and severity honesty:
  [senior-dev/lh-pairing](../../../senior-dev/skills/lh-pairing/SKILL.md),
  [architect/lh-design-review](../../../architect/skills/lh-design-review/SKILL.md)
