# Rules — quality and dependencies

This is one part of the rule set. Section numbers are local to this file; cross-file
references name the file. The file map is in
`../SKILL.md`. Read `rules-core.md` first, then the file for the layer you generate.

===============================================================================

## 1. TESTING

### 1.1 UseCase testing

UseCase tests are the most important. Mock the Repository:

```kotlin
// app/src/test/java/<basePackage>/feature/auth/domain/usecase/LoginUseCaseTest.kt
class LoginUseCaseTest {
    private val authRepository = mockk<AuthRepository>()
    private val useCase = LoginUseCase(authRepository)

    @Test
    fun `invoke returns success when login succeeds`() = runTest {
        // Given
        val token = AuthToken("access", "refresh", /* expiresAt */)
        coEvery { authRepository.login(any(), any()) } returns token

        // When
        val result = useCase(LoginParams("user@test.com", "password"))

        // Then
        assertTrue(result.isSuccess)
        assertEquals(token, result.getOrNull())
    }

    @Test
    fun `invoke returns InvalidCredentials on 401`() = runTest {
        // Given
        coEvery { authRepository.login(any(), any()) } throws
            ClientRequestException(mockk { every { status } returns HttpStatusCode.Unauthorized }, "")

        // When
        val result = useCase(LoginParams("user@test.com", "wrong"))

        // Then
        assertTrue(result.isFailure)
        assertIs<AuthError.InvalidCredentials>(result.exceptionOrNull())
    }
}
```

### 1.2 ViewModel testing

`viewModelScope` uses `Dispatchers.Main`, so every ViewModel test declares `MainDispatcherRule`:

```kotlin
// app/src/test/java/<basePackage>/core/testing/MainDispatcherRule.kt
class MainDispatcherRule(
    val dispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(dispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}
```

```kotlin
// app/src/test/java/<basePackage>/feature/auth/presentation/AuthViewModelTest.kt
class AuthViewModelTest {
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val loginUseCase = mockk<LoginUseCase>()
    private val viewModel = AuthViewModel(loginUseCase)

    @Test
    fun `onEvent EmailChanged updates state`() = runTest {
        viewModel.onEvent(AuthUiEvent.EmailChanged("test@test.com"))
        assertEquals("test@test.com", viewModel.state.value.email)
    }

    @Test
    fun `login success sends NavigateToMain effect`() = runTest {
        coEvery { loginUseCase(any()) } returns Result.success(mockk())

        viewModel.effects.test {
            viewModel.onEvent(AuthUiEvent.Login)
            assertEquals(AuthUiEffect.NavigateToMain, awaitItem())
            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

For repeated emissions prefer a fake repository over mocks:

```kotlin
class FakeHistoryRepository : HistoryRepository {
    private val records = MutableStateFlow<List<Record>>(emptyList())

    override fun observeRecords(): Flow<List<Record>> = records
    override suspend fun refresh() = Unit

    fun emit(items: List<Record>) {
        records.value = items
    }
}
```

### 1.3 Repository and Room testing

Mapping logic is tested on the JVM with fake DataSources. A Room in-memory test is required only
when the DAO contains non-trivial SQL (joins, projections, ordering that matters) or when a
migration exists. Simple CRUD covered by a fake repository test does not need a database.

DAO and migration tests run as instrumented tests with an in-memory database:

```kotlin
// app/src/androidTest/java/<basePackage>/core/database/RecordDaoTest.kt
@RunWith(AndroidJUnit4::class)
class RecordDaoTest {
    private lateinit var db: AppDatabase

    @Before
    fun setUp() {
        db = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java,
        ).build()
    }

    @After
    fun tearDown() = db.close()

    @Test
    fun `observeByUser emits inserted records`() = runTest {
        db.recordDao().upsert(
            listOf(
                RecordEntity(
                    id = "r1",
                    userId = "u1",
                    externalId = "ext-1",
                    createdAt = 0L,
                ),
            ),
        )

        val records = db.recordDao().observeByUser("u1").first()

        assertEquals(1, records.size)
    }
}
```

### 1.4 Compose UI testing

Test the stateless `View`, not `Screen`:

```kotlin
// app/src/androidTest/java/<basePackage>/feature/auth/presentation/AuthViewTest.kt
class AuthViewTest {
    @get:Rule
    val compose = createComposeRule()

    @Test
    fun `error is displayed`() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val error = UiText.Resource(R.string.error_network)

        compose.setContent {
            AuthView(state = AuthUiState(error = error), onEvent = {})
        }

        compose.onNodeWithText(context.getString(R.string.error_network)).assertIsDisplayed()
    }
}
```

### 1.5 Testing rules

- UseCase tests are required.
- ViewModel tests are required for complex logic.
- Repository tests are optional (required when mapping is non-trivial).
- DataSource tests are not required (covered via Repository).
- Use `kotlinx-coroutines-test` (`runTest`, `TestScope`, `TestDispatcher`).
- Use `MainDispatcherRule` in every ViewModel test.
- Use Turbine (`test { }`, `awaitItem()`, `expectNoEvents()`) when a test checks emissions, ordering or a `UiEffect`. `state.value` is allowed for a single final state after `advanceUntilIdle()`.
- Use `mockk` for UseCase contracts and a fake repository with `MutableStateFlow` for ViewModel flows.
- Use a Room in-memory test for non-trivial DAO SQL or migrations; mapping may be covered by a JVM test with fake DataSources.
- Use a Compose smoke test for each `View`.
- PROHIBITED in tests: `Thread.sleep`, `runBlocking`, `first()`/`toList()` on infinite flows.
- Test file: `app/src/test/java/<basePackage>/feature/<featureName>/.../<Class>Test.kt`.
- UI test file: `app/src/androidTest/java/<basePackage>/feature/<featureName>/.../<View>Test.kt`.
- Test name: backtick string describing the scenario.

===============================================================================

## 2. DEPENDENCIES VERSIONS

Set up dependency versions ONLY via `gradle/libs.versions.toml`.

**Where versions come from (in order):**

1. An existing project: read its `gradle/libs.versions.toml` and reuse the versions. Do not bump
   dependencies as part of a feature task.
2. A new project: verify the current versions on developer.android.com and Maven Central before
   writing the catalog. [versions.md](versions.md) is a baseline with a verification date — it is
   a reference, not a source of truth.

Template of `gradle/libs.versions.toml` (values are intentionally placeholders):

```toml
[versions]
kotlin = "<verified>"
agp = "<verified>"
koin = "<verified>"
room = "<verified>"
coroutines = "<verified>"
lifecycle = "<verified>"
paging = "<verified>"
immutableCollections = "<verified>"
turbine = "<verified>"

[libraries]
koin-android = { group = "io.insert-koin", name = "koin-android", version.ref = "koin" }
koin-androidx-compose = { group = "io.insert-koin", name = "koin-androidx-compose", version.ref = "koin" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-paging = { group = "androidx.room", name = "room-paging", version.ref = "room" }
room-testing = { group = "androidx.room", name = "room-testing", version.ref = "room" }
lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycle" }
paging-runtime = { group = "androidx.paging", name = "paging-runtime", version.ref = "paging" }
paging-compose = { group = "androidx.paging", name = "paging-compose", version.ref = "paging" }
kotlinx-collections-immutable = { group = "org.jetbrains.kotlinx", name = "kotlinx-collections-immutable", version.ref = "immutableCollections" }
turbine = { group = "app.cash.turbine", name = "turbine", version.ref = "turbine" }
```

Required by the rules:
- `lifecycle-runtime-compose` — `collectAsStateWithLifecycle`.
- `kotlinx-collections-immutable` — immutable `UiState` collections.
- `paging-runtime` + `paging-compose` + `room-paging` — Paging 3.
- `room-testing` + `turbine` — test-only (`testImplementation`).
- `androidx.compose.ui:ui-test-junit4` and `ui-test-manifest` — Compose UI tests.

Never hardcode a version in `build.gradle.kts`, and never copy a version from this skill without
checking it first.

There are only aliases inside `build.gradle.kts`.

```kotlin
// ✅ Correct
implementation(libs.koin.android)
// ❌ Incorrect
implementation("io.insert-koin:koin-android:4.2.0")
```

===============================================================================

Follow these rules at all times. You're building a production-ready Android feature slice.
