# OUTPUT FORMAT (STRICT)

Output MUST contain:

## 1. Summary

What is generated, which layers, which repository contract, use cases, paging, migrations.

## 2. Folder tree

Full structure of all created files and directories.

## 3. Source code (in order)

Domain error → Models → DTO → Mapper → Repository interface → RepositoryImpl → DataSources → UseCases → UiState → UiEvent → UiEffect → Ui model → UiMapper → ViewModel → DI module → UiText/strings (if created or changed)

## 4. Tests

UseCaseTest → ViewModelTest → Repository/DaoTest → Compose ViewTest

## 5. UI

Screen → View → Composable components → Previews

## 6. Architecture validation

Run through the checklist from [validation-checklist.md](validation-checklist.md). Each item: ✅ / ❌ with an explanation for each ❌.
