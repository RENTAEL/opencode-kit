# Changelog

All notable changes to the skill rules. Format: Keep a Changelog.

## [1.1.0] — 2026-11-02

### Added

- `presentation/model/<Model>Ui.kt` for pre-formatted presentation data.
- `UiText.asString(context)` for non-composable contexts.
- `viewModelOf(::ViewModel)` as an allowed Koin definition.
- Rules for smoke-test findings: no `!!`, navigation ownership, test scope.

### Changed

- `AppNavGraph` now owns the `NavController`; `MainActivity` only hosts the graph.
- Turbine is required for emissions/ordering/effects; `state.value` is allowed for a final state.
- Room in-memory tests are required only for non-trivial SQL and migrations.

## [1.0.0] — 2026-11-02

### Added

- Repository sync contract with four DataSource combinations (`rules-core.md` 2.4).
- Dispatcher injection through Koin qualifiers (`rules-core.md` 9.5).
- Error contract: `Result<T>` / `Flow<Result<T>>`, `CancellationException` rethrow, no
  `getOrThrow`/`runCatching`.
- `UiText` and string-resource rules (English base, `values-ru` translation).
- Compose stability rules: `@Immutable` `UiState`, immutable collections, `modifier` contract,
  previews, accessibility.
- Room rules: indices, foreign keys, transactions, Paging 3, manual migrations, converters.
- Test infrastructure: `MainDispatcherRule`, Turbine, Room in-memory, Compose smoke tests.
- `references/versions.md` baseline and the dependency policy.
- "Never do this" table in `rules-core.md`.

### Changed

- Rules split into `rules-core`, `rules-data`, `rules-presentation`, `rules-navigation` and
  `rules-quality`.
- One layer list (in `SKILL.md`) and one generation order (`rules-core.md` 3.1).
- Dependency versions are no longer hardcoded in the rules; they come from the project catalog
  or a verified baseline.

### Fixed

- Layer contradictions: domain no longer depends on data; Repository is an interface with an
  implementation in `data/`.
- UseCase contract unified on `suspend operator fun invoke()`.
- Navigation always goes through `Channel<UiEffect>`; no navigation lambdas in ViewModels.
- Presentation artifacts named `<FeatureName>UiState` / `UiEvent` / `UiEffect`.
- Broken links and anchors in the reference files.
- Non-compiling examples (records, error message, table name, SQL query).
- README typos and the skill frontmatter name.
