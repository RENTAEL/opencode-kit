# Android Development AI Skill

An Android development skill for Android projects, following Google's official architecture guidance adapted to the conventions described below.

This repository is based on:
- https://github.com/dpconde/claude-android-skill
- https://github.com/AlexGladkov/claude-code-agents/blob/main/claude/agents/coding/kotlin/kotlin-multiplatform-developer.md

## Overview

This skill provides the agent with comprehensive knowledge of the project's Android development patterns, including:

- **Clean Architecture** with UI, Domain, and Data layers
- **Jetpack Compose** patterns and best practices
- **Single-module feature-first package structure** (no multi-module, no convention plugins)
- **Offline-first architecture** with Room and reactive streams (when both local and remote sources exist)
- **Dependency injection** with Koin
- **Comprehensive testing** strategies

## Installation

1. Clone this repository into your AI-agent `skills` directory.
2. AI-agent will automatically detect and load the skill when you work on Android projects.

This skill is supported to be placed into the standard agents dirs like:
- `<project-root>/.claude/skills/`,
- `<project-root>/.opencode/skills/`,
- `~/.claude/skills/`,
- `~/.config/opencode/skills/`.

Example path to the skill: `<project-root>/.opencode/skills/android-dev-ai-skill/SKILL.md`

## Usage

The skill automatically activates when you request Android-related tasks. Simply ask:

- "Create a new feature package for history"
- "Add the domain layer for feature"
- "Implement data layer"
- "Create new screen to display info about the app"

The AI-agent will follow instructions, patterns and best practices defined in [SKILL.md](SKILL.md).

## Core Principles

This skill teaches AI-agent to follow these key Android development principles:

1. **Clean architecture**: Strict separation of Data, Domain, and Presentation layers
2. **Feature-first structure**: Each feature is self-contained with clear boundaries
3. **Offline-first** (Local + Remote): Local database is the source of truth, synchronized with remote data. Local-only and remote-only features use the contract from `references/rules-core.md` 2.4.
4. **Unidirectional data flow**: Intents flow down, State flows up (MVI/UDF pattern)
5. **Reactive streams**: Kotlin Flow for persisted data, `Result` for one-shot operations

## Architecture Overview

### Clean Architecture

```
┌────────────────────────────────────────────────────┐
│               Presentation Layer                   │
│  ┌──────────────┐    ┌─────────────────────────┐   │
│  │   Screen     │◄───│      ViewModel          │   │
│  │  (Compose)   │    │  (StateFlow<State>)     │   │
│  │  Event -->   │───►│  onEvent(Event)         │   │
│  └──────────────┘    └───────────┬─────────────┘   │
├──────────────────────────────────┼─────────────────┤
│                  Domain Layer    │                 │
│              ┌───────────────────▼──────┐          │
│              │       Use Cases          │          │
│              │  (combine/transform)     │          │
│              └───────────┬──────────────┘          │
├──────────────────────────┼─────────────────────────┤
│                  Data Layer                        │
│  ┌───────────────────────▼──────────────────────┐  │
│  │              Repository                      │  │
│  │    (offline-first, single source of truth)   │  │
│  └─────────┬─────────────────────┬──────────────┘  │
│            │                     │                 │
│  ┌─────────▼─────────┐  ┌───────▼──────────────┐   │
│  │  Local DataSource │  │  Remote DataSource   │   │
│  │   (Room + DAO)    │  │     (Retrofit)       │   │
│  └───────────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────────┘
```

### Feature-First Structure (single `:app` module)

```
app/src/main/java/<basePackage>/
├── App.kt                    # Koin startup
├── MainActivity.kt           # Entry point
├── navigation/               # AppNavGraph and navigation config
├── core/                     # Shared code (di, network, database, preferences, ui)
└── feature/                  # Business features
    └── <featureName>/
        ├── data/             # Repositories, local and remote sources
        ├── domain/           # Models, interfaces, use cases
        ├── presentation/     # mvi/, viewmodel/, ui/
        └── di/               # Koin module
```

## Technology Stack

This skill configures projects with:

- **Language**: Kotlin
- **UI**: Jetpack Compose
- **Architecture**: Clean Architecture + Feature-First Structure + MVI with UDF
- **DI**: Koin
- **Database**: Room (manual migrations, Paging 3)
- **UI text**: `UiText` + `strings.xml` (English base, `values-ru`)
- **Immutable state**: `@Immutable` `UiState` with `kotlinx.collections.immutable`
- **Network**: Retrofit + Kotlinx Serialization
- **Async**: Kotlin Coroutines + Flow
- **Testing**: kotlinx-coroutines-test, mockk, Turbine, Room testing, Compose UI tests
- **Build**: Gradle, single module, version catalog

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [Android Developer Documentation](https://developer.android.com)
- [Kotlin Documentation](https://kotlinlang.org/docs/home.html)
- [Android Architecture Guidelines](https://developer.android.com/topic/architecture)
- [Jetpack Compose Pathway](https://developer.android.com/courses/pathways/compose)
- [Jetpack Compose Best Practices](https://developer.android.com/jetpack/compose)
