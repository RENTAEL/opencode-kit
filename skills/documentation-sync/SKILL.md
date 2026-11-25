---
name: documentation-sync
description: "Run after:"
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, kodda yapÃƒâ€žÃ‚Â±lan ÃƒÆ’Ã‚Â¶nemli deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ikliklerden sonra hangi dokÃƒÆ’Ã‚Â¼mantasyon dosyalarÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±n
  eskidiÃƒâ€žÃ…Â¸ini tespit edip gÃƒÆ’Ã‚Â¼nceller. README, API docs, .env.example, CHANGELOG ve mimari
  diyagramlar incelenerek eski bilgiler dÃƒÆ’Ã‚Â¼zeltilir. "Docs ile kod arasÃƒâ€žÃ‚Â±ndaki uÃƒÆ’Ã‚Â§urum"
  problemini kapatÃƒâ€žÃ‚Â±r.

  NE ZAMAN: API eklendiÃƒâ€žÃ…Â¸inde/deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸tiÃƒâ€žÃ…Â¸inde, yeni env variable eklendiÃƒâ€žÃ…Â¸inde,
            bÃƒÆ’Ã‚Â¼yÃƒÆ’Ã‚Â¼k refactor sonrasÃƒâ€žÃ‚Â±, merge ÃƒÆ’Ã‚Â¶ncesi veya sonrasÃƒâ€žÃ‚Â±.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    GÃƒÆ’Ã‚Â¼ncellenmiÃƒâ€¦Ã…Â¸ doc dosyalarÃƒâ€žÃ‚Â± + deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸im ÃƒÆ’Ã‚Â¶zet raporu.
-->

# Documentation Sync Skill

## When to Trigger

Run after:
- A public API endpoint is added, changed, or removed
- A CLI command or flag is modified
- A new environment variable or config key is introduced
- A major component or module is refactored
- A new npm/pip/etc. package is added or removed from dependencies
- Any `README.md` reference becomes inaccurate

## Step-by-Step Process

### 1. Identify What Changed

Review the git diff of the work just completed:

```bash
git diff main --name-only          # Files changed vs main
git diff HEAD~1 --name-only        # Files changed in last commit
```

Categorize changes:
- **API changes** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ affects `docs/api/`, OpenAPI/Swagger specs, `README.md`
- **Config changes** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ affects `.env.example`, `docs/configuration.md`
- **Dependency changes** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ affects `README.md` (setup section), `docs/getting-started.md`
- **Architecture changes** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ affects `docs/architecture.md`, diagrams
- **New features** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ affects `docs/features/`, changelogs

### 2. Audit Existing Docs

For each affected category, check whether corresponding docs exist:

```
docs/
  api/             ÃƒÂ¢Ã¢â‚¬Â Ã‚Â REST/GraphQL endpoint docs
  architecture.md  ÃƒÂ¢Ã¢â‚¬Â Ã‚Â System design, component diagram
  configuration.md ÃƒÂ¢Ã¢â‚¬Â Ã‚Â All env vars and config options
  getting-started.md ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Local setup guide
  features/        ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Per-feature descriptions
CHANGELOG.md       ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Version history
README.md          ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Project overview + quickstart
```

For each doc file that touches the changed area, read it and flag stale sections.

### 3. Update Docs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Priority Order

Update in this order (highest impact first):

#### A. README.md
- Setup instructions still accurate?
- Tech stack section reflects current stack?
- Any removed features still mentioned?

#### B. .env.example / Configuration Docs
For every new env variable added to code, add a corresponding entry:

```bash
# Description of what this does
NEW_VAR_NAME=example_value
```

Document in `docs/configuration.md`:
```markdown
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| NEW_VAR_NAME | Yes | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â | What it controls |
```

#### C. API Docs
For every endpoint change, update the relevant doc:

```markdown
### POST /api/resource

**Changed in:** <date or version>
**Description:** ...
**Request Body:** ...
**Response:** ...
**Breaking Change:** Yes/No
```

#### D. CHANGELOG.md
Append an entry under `## [Unreleased]`:

```markdown
### Added
- <new feature description>

### Changed
- <what was modified and why>

### Fixed
- <bug fixed>

### Removed
- <what was removed>
```

Follow [Keep a Changelog](https://keepachangelog.com) format.

#### E. Architecture Docs
If a new service, module, or significant component was added:
- Update the component list in `docs/architecture.md`
- Note any new external dependencies or integrations
- If a diagram exists (Mermaid, Draw.io), update it

### 4. Verify Internal Links

After editing, do a quick check for broken internal references:

```bash
# Find markdown links pointing to non-existent files
grep -r "\[.*\](.*\.md)" docs/ README.md | grep -v "http"
```

Manually verify the top 5 most-used internal links still resolve.

### 5. Report Changes

Output a summary:

```
## Documentation Sync Complete

**Files Updated:**
- README.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â updated setup section
- docs/configuration.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â added NEW_VAR_NAME
- CHANGELOG.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â added unreleased entry

**Files That May Need Manual Review:**
- docs/architecture.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â diagram may be outdated (manual update needed)

**No changes needed:**
- docs/api/ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no endpoint changes detected
```

## Rules

- **Never delete documentation** without confirming with the user. Archive or mark as deprecated instead.
- **Don't invent information.** If you're unsure what a config variable does, write `# TODO: document this` and flag it.
- **Keep CHANGELOG.md under `[Unreleased]`** until an explicit version bump/release.
- **Every new env variable must appear in `.env.example`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no exceptions.
- **Docs first is fine, but docs-never is not.** Even minimal docs are better than none.
