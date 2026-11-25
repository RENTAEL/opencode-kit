# ARCHITECTURE VALIDATION CHECKLIST

Before giving the result, check each point:

**Layers and Dependencies:**
- [ ] All `UseCase.invoke()` return `Result<T>` (or `Flow<Result<T>>` for streams)
- [ ] UseCase exposes a single `suspend operator fun invoke()` entry point
- [ ] No import from another `feature/` directory; `core/` does not import `feature/`
- [ ] `domain/repository/` does not import anything from `data/` (no DataSource/DTO references)
- [ ] Repository is an interface in `domain/repository/` and `<FeatureName>RepositoryImpl` is in `data/repository/`
- [ ] Repository contract matches the existing DataSources: no `refresh()` without Remote, no `observe()` without Local
- [ ] Repository does not import another Repository
- [ ] DataSource does not import another DataSource
- [ ] DataSource does not import UseCase or ViewModel
- [ ] Dispatchers are injected; no `Dispatchers.*` outside DI modules
- [ ] No `!!` in production code

**DTO and mapping:**
- [ ] DTOs are marked `@Serializable`
- [ ] DTO → Domain mapping occurs in the Repository via the Mapper, not in the DataSource
- [ ] DTOs do not extend beyond `data/`

**Errors:**
- [ ] Has `<FeatureName>Error.kt` sealed class
- [ ] UseCase maps exceptions to `<FeatureName>Error`, does not pass raw Exception
- [ ] No explicit `throw` outside DataSources and Repositories; no `getOrThrow()`, no `runCatching` around suspend calls. Repositories propagate exceptions, UseCases map them to `<FeatureName>Error`
- [ ] `CancellationException` is rethrown before mapping other errors
- [ ] Streams return `Flow<Result<T>>`; `Result<Flow<T>>` is absent
- [ ] Domain errors contain no text and no `R`; ViewModel maps them to `UiText`

**Presentation:**
- [ ] ViewModel is the sole source of state and exposes `StateFlow`
- [ ] Artifacts are named `<FeatureName>UiState`, `<FeatureName>UiEvent`, `<FeatureName>UiEffect`
- [ ] `UiState` is `@Immutable`; collections are `ImmutableList`/`ImmutableSet`; no `MutableList`
- [ ] Presentation models live in `presentation/model/<Model>Ui.kt`; no domain logic there
- [ ] `ImmutableList` appears only in presentation; domain and data use `List`
- [ ] One-time events are handled via `Channel`, not `StateFlow`
- [ ] No navigation lambdas in the ViewModel constructor; navigation goes through `UiEffect`
- [ ] Screen uses `collectAsStateWithLifecycle()`; no `collectAsState()`
- [ ] `AppNavGraph` owns the `NavController`; `MainActivity` does not pass one
- [ ] View does not call UseCase/Repository directly
- [ ] UiEffects are handled in Screen via `LaunchedEffect`, not in View
- [ ] Every composable takes `modifier: Modifier = Modifier`
- [ ] No hardcoded user-visible strings (except inside `@Preview`); text goes through `stringResource`/`UiText`
- [ ] Previews are light + dark, contain no ViewModel/Koin
- [ ] Data formatting happens in the ViewModel, not in the View
- [ ] Colors/typography come from `MaterialTheme`; spacing from `Spacing.kt`

**Room:**
- [ ] Every `@ForeignKey` child column has an `@Index`
- [ ] `onConflict` is specified explicitly on every insert
- [ ] Multi-step writes use `@Transaction` or `withTransaction`
- [ ] `exportSchema = true`; schemas are committed
- [ ] Migrations are manual `Migration(from, to)` in separate files, added to `addMigrations`
- [ ] No `@AutoMigration`, no `fallbackToDestructiveMigration()` in release
- [ ] Every migration has a `MigrationTestHelper` test
- [ ] Paginated lists use Paging 3 (`PagingSource`/`RemoteMediator`, `cachedIn`)
- [ ] TypeConverters are explicit; enums stored as `String`; dates as epoch millis

**Files:**
- [ ] One class - one file
- [ ] No files > 1000 lines

**Tests:**
- [ ] Test for each UseCase
- [ ] ViewModel tests declare `MainDispatcherRule`
- [ ] Flow/StateFlow/UiEffect tests use Turbine when emissions or ordering are checked; `state.value` only for a final state after `advanceUntilIdle()`
- [ ] Non-trivial DAO SQL or migrations are covered with a Room in-memory test; mapping may use fake DataSources
- [ ] Each View has a Compose smoke test
- [ ] No `Thread.sleep`, `runBlocking`, `first()` on infinite flows
