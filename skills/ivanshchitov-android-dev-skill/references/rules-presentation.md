# Rules — presentation layer

This is one part of the rule set. Section numbers are local to this file; cross-file
references name the file. The file map is in
`../SKILL.md`. Read `rules-core.md` first, then the file for the layer you generate.

===============================================================================

## 1. ViewModel RULES

### 1.1 ViewModel structure

State is immutable and holds ready-to-render data:

```kotlin
@Immutable
data class HistoryUiState(
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val records: ImmutableList<Record> = persistentListOf(),
    val error: UiText? = null,
)
```

```kotlin
class HistoryViewModel(
    private val observeHistoryUseCase: ObserveHistoryUseCase,
    private val refreshHistoryUseCase: RefreshHistoryUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow(HistoryUiState())
    val state: StateFlow<HistoryUiState> = _state.asStateFlow()

    // One-time events — via Channel, not StateFlow
    private val _effects = Channel<HistoryUiEffect>(Channel.BUFFERED)
    val effects: Flow<HistoryUiEffect> = _effects.receiveAsFlow()

    init {
        observeHistory()
    }

    fun onEvent(event: HistoryUiEvent) {
        when (event) {
            HistoryUiEvent.Refresh -> refresh()
            is HistoryUiEvent.RecordClicked -> navigateToEdit(event.id)
        }
    }

    private fun observeHistory() {
        viewModelScope.launch {
            observeHistoryUseCase().collect { result ->
                result
                    .onSuccess { records ->
                        _state.update {
                            it.copy(
                                isLoading = false,
                                records = records.toPersistentList(),
                                error = null,
                            )
                        }
                    }
                    .onFailure { error ->
                        _state.update { it.copy(isLoading = false, error = error.toUiText()) }
                    }
            }
        }
    }

    private fun refresh() {
        viewModelScope.launch {
            _state.update { it.copy(isRefreshing = true, error = null) }
            refreshHistoryUseCase()
                .onFailure { error -> _state.update { it.copy(error = error.toUiText()) } }
            _state.update { it.copy(isRefreshing = false) }
        }
    }

    private fun navigateToEdit(recordId: Long) {
        _effects.trySend(HistoryUiEffect.NavigateToEdit(recordId))
    }
}
```

### 1.2 ViewModel rules

- ViewModel should only have access to business logic through UseCases.
- PROHIBITED: Repositories, DataSources and DAO dependencies

### 1.3 Coroutines rules

- ViewModel uses only `viewModelScope`. Custom `CoroutineScope` in a ViewModel is PROHIBITED.
- UseCases and Repositories never create a scope: they are `suspend` functions running in the caller's scope.
- `Dispatchers.*` must not be referenced in ViewModel, UseCase or Repository. Dispatchers are injected through qualifiers (see `rules-core.md` 9.5).
- Dispatchers are needed only for blocking or CPU-bound work (files, crypto, heavy mapping). Room and Retrofit `suspend` calls are already main-safe — do not wrap them.
- Parallel work inside one call: `coroutineScope { }` + `async`; `supervisorScope { }` only when partial failure is acceptable and every child handles its own error.
- A long-lived scope is allowed only in `App`/DI and is injected where needed.
- `viewModelScope` is cancelled automatically when the ViewModel is cleared.

### 1.4 UiEffect rules

For events that cannot be repeated on resubscribe (navigation, toast, snackbar), use `Channel`, NOT `StateFlow`:

```kotlin
// mvi/AuthUiEffect.kt
sealed class AuthUiEffect {
    data object NavigateToMain : AuthUiEffect()
    data class ShowToast(val message: UiText) : AuthUiEffect()
}
```

```kotlin
// Inside ViewModel:
private val _effects = Channel<AuthUiEffect>(Channel.BUFFERED)
val effects: Flow<AuthUiEffect> = _effects.receiveAsFlow()
```

```kotlin
// Inside Screen (observe side effects):
LaunchedEffect(viewModel) {
    viewModel.effects.collect { effect ->
        when (effect) {
            is AuthUiEffect.NavigateToMain -> { /* navigation */ }
            is AuthUiEffect.ShowToast -> { /* show toast */ }
        }
    }
}
```

UiEffect is only created if there are truly one-time events. Don't create them just for the sake of it.

### 1.5 Strict rules

- ViewModel — the only source of state
- All public functions return `Unit`
- All functions that return values are private
- View has no business logic, mutable state or `remember` for logic (Compose rules in section 14)

===============================================================================

## 2. UI RULES (COMPOSE)

### 2.1 Screen is a thin adapter

```kotlin
@Composable
fun AuthScreen(
    viewModel: AuthViewModel = koinViewModel(),
    onNavigateToMain: () -> Unit,
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(viewModel) {
        viewModel.effects.collect { effect ->
            when (effect) {
                is AuthUiEffect.ShowToast -> { /* show toast */ }
                AuthUiEffect.NavigateToMain -> onNavigateToMain()
            }
        }
    }

    AuthView(state = state, onEvent = viewModel::onEvent)
}
```

- Screen is the only place that knows the ViewModel, Koin and navigation callbacks.
- State is collected with `collectAsStateWithLifecycle()`; plain `collectAsState()` is PROHIBITED.
- Cold Flows never reach the UI: the ViewModel exposes `StateFlow`.
- `UiEffect` is collected in `LaunchedEffect`; effects are never replayed.
- No business logic in Screen.

### 2.2 View is layout only

- Accepts `state`, `onEvent` and `modifier`.
- Contains `@Preview`s.
- No ViewModel, no Koin, no side effects.
- No business logic, no `remember` for logic.
- All user-visible text goes through `stringResource`/`UiText`; literals are allowed only inside `@Preview` functions and their sample-data helpers.
- Colors and typography come from `MaterialTheme`; spacing comes from `core/ui/theme/Spacing.kt` (multiples of 4/8/16/24).

### 2.3 Compose API and stability rules

- `UiState` is `@Immutable`; collections are `ImmutableList`/`ImmutableSet`/`ImmutableMap` from `kotlinx.collections.immutable`, default `persistentListOf()`.
- `MutableList` and mutable collections in `UiState` are PROHIBITED. Never mutate state in place; create a new instance.
- `ImmutableList` exists only in the presentation layer. Domain and data use `List`; the ViewModel converts with `.toPersistentList()`.
- Every reusable composable (`View` and shared components) takes `modifier: Modifier = Modifier` as a single modifier applied to its root layout. Required parameters first, then `modifier`, then optional parameters. `Screen` may omit it because it only wires state and effects.
- A reusable component does not force `fillMaxSize()` or outer padding; the caller decides.
- Formatting (dates, numbers, currency) happens in the ViewModel; the View only renders ready values. Presentation models with pre-formatted data live in `presentation/model/<Model>Ui.kt` and contain no domain logic. `stringResource` is the only allowed resolution in the View.
- `remember` is used only for expensive objects (formatters, `LazyListState`) and `rememberSaveable` for ephemeral UI state. Derived state uses `derivedStateOf`.
- No suspend calls, database writes or analytics in the composable body. `LaunchedEffect` keys reflect real dependencies; `DisposableEffect` cleans up listeners.
- `@Composable` functions returning `Unit` are PascalCase; value-returning functions (`rememberXxx`) are camelCase.
- A composable file over 300 lines is a signal to split it.

### 2.4 Previews

- `@Preview` lives in the `View` file, never in `Screen`.
- No ViewModel, no Koin, no navigation inside a preview.
- At least two previews: light and dark theme.
- Preview data comes from a sample factory (`sampleAuthUiState()`), not from literals duplicated in every preview.

### 2.5 Lists

- `LazyColumn`/`LazyRow` items always set `key`.
- Set `contentType` when a list mixes item types.
- `LazyListState` is created with `rememberLazyListState()`.

### 2.6 Accessibility

- Icons without text have `contentDescription` from resources.
- Clickable targets are at least 48dp.
- Custom `semantics { }` only when standard roles are insufficient.

### 2.7 UiText and string resources

```kotlin
// core/ui/UiText.kt
sealed interface UiText {
    data class Resource(@StringRes val resId: Int, val args: List<Any> = emptyList()) : UiText
    data class Dynamic(val value: String) : UiText
}

@Composable
fun UiText.asString(): String = when (this) {
    is UiText.Resource -> stringResource(resId, *args.toTypedArray())
    is UiText.Dynamic -> value
}

// for non-composable contexts: Toast, notifications, Snackbar via host
fun UiText.asString(context: Context): String = when (this) {
    is UiText.Resource -> context.getString(resId, *args.toTypedArray())
    is UiText.Dynamic -> value
}
```

- Every user-visible string comes from resources through `stringResource`/`UiText`. Literals are allowed only inside `@Preview` functions and their sample-data helpers.
- `UiText` lives in `core/ui/`, never in `domain/`. Domain errors contain no text and no `R`.
- The default `values/strings.xml` is English; `values-ru/strings.xml` holds the Russian translation.
- Keys describe meaning: `auth_login_action`, `error_network` — not `text1`, not a copy of the text.
- Format arguments are passed to `stringResource(id, arg)`, not `String.format`, so the locale is respected.
- `UiText.Dynamic` is allowed only for messages already localized by the server; prefer `Resource`.
- `asString(context)` is allowed only in non-composable contexts (Toast, notifications); composable code uses `asString()`.
- Content descriptions, top bar titles, navigation labels and notification texts use resources too.

**STRICT:** The agent generates **full working UI code** for each selected platform. Business logic is contained solely in the ViewModel. The UI only displays state and dispatches events. No // TODOs, // ..., or stubs. Only working code for a specific feature. **Exception** — user requests a stub.

===============================================================================

## 3. Android — Jetpack Compose (always)

The agent generates `<FeatureName>Screen.kt` and `<FeatureName>View.kt`.

**Screen** is a thin adapter (see [Section 2](#2-ui-rules-compose)).

**View** is full UI with real elements according to the feature description:

```kotlin
@Composable
fun AuthView(
    state: AuthUiState,
    onEvent: (AuthUiEvent) -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        TextField(
            value = state.email,
            onValueChange = { onEvent(AuthUiEvent.EmailChanged(it)) },
            label = { Text(stringResource(R.string.auth_email_label)) },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        TextField(
            value = state.password,
            onValueChange = { onEvent(AuthUiEvent.PasswordChanged(it)) },
            label = { Text(stringResource(R.string.auth_password_label)) },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(16.dp))
        Button(
            onClick = { onEvent(AuthUiEvent.Login) },
            enabled = !state.isLoading,
            modifier = Modifier.fillMaxWidth()
        ) {
            if (state.isLoading) {
                CircularProgressIndicator(Modifier.size(16.dp))
            } else {
                Text(stringResource(R.string.auth_login_action))
            }
        }
        state.error?.let { error ->
            Spacer(Modifier.height(8.dp))
            Text(
                text = error.asString(),
                color = MaterialTheme.colorScheme.error,
            )
        }
    }
}
```

```kotlin
// previews — View only, no ViewModel, no Koin
@Preview(showBackground = true)
@Composable
private fun AuthViewLightPreview() {
    AppTheme(darkTheme = false) {
        AuthView(state = sampleAuthUiState(), onEvent = {})
    }
}

@Preview(showBackground = true, uiMode = UI_MODE_NIGHT_YES)
@Composable
private fun AuthViewDarkPreview() {
    AppTheme(darkTheme = true) {
        AuthView(state = sampleAuthUiState(), onEvent = {})
    }
}
```

- If a Composable component is used in 2+ places in multiple features → it is moved to: `core/ui/common/<ComponentName>.kt`.
- If a Composable component is used in 2+ places inside the feature (not between them) → it is moved to: `feature/<featureName>/presentation/ui/component/<ComponentName>.kt`.

```kotlin
@Composable
fun RecordList(
    records: ImmutableList<Record>,
    onRecordClick: (Long) -> Unit,
    modifier: Modifier = Modifier,
) {
    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        items(
            items = records,
            key = { it.id },
            contentType = { "record" },
        ) { record ->
            RecordCard(
                record = record,
                onClick = { onRecordClick(record.id) },
            )
        }
    }
}
```

- LazyColumn items set `key` as the item id; mixed lists also set `contentType`.

===============================================================================
