# Dead code detection: CI files, configs, and temp files

Source-code tools miss this whole category because nothing imports these files;
tools consume them by naming convention. So "unused" here means "the tool that
would read this file is gone, disabled, or pointed elsewhere."

Run the scanner first, then verify with the checks below:

```bash
python scripts/hygiene_scan.py /path/to/repo
```

## Temp and junk files (Tier 1 almost always)

The scanner flags these by pattern: `*.log`, `*.tmp`, `*.bak`, `*.orig`,
`*.rej`, `*.swp`, `*~`, `.DS_Store`, `Thumbs.db`, `core.*` dumps, `*.pyc`
outside `__pycache__`, stray archives (`*.zip`, `*.tar.gz`) in source dirs, and
editor autosaves. Two verifications before Tier 1:

1. `git check-ignore <file>`: if git already ignores it, it is local clutter,
   not repo dead weight; mention it but focus on *committed* junk
   (`git ls-files` filtered by the same patterns).
2. Make sure it is not a fixture: a `.log` file inside `tests/fixtures/` may be
   test input. Grep the filename across the repo first.

Also suggest adding the committed-junk patterns to `.gitignore` so they stay gone.

## CI-related dead files

Signals the scanner and you should check:

- **Multiple CI systems present.** `.travis.yml`, `Jenkinsfile`, `.circleci/`,
  `azure-pipelines.yml`, and `.github/workflows/` in the same repo usually means
  a migration left corpses. The live one is the one with recent git history:
  `git log -1 --format=%cs -- <ci-file>` for each; a two-year-old Travis file
  next to actively edited GitHub workflows is Tier 1 material.
- **Workflows that can never trigger**: `on.push.branches` pointing at branches
  that no longer exist (`git branch -r`), path filters matching deleted
  directories, or `if: false` guards.
- **Orphaned CI helper scripts**: files under `ci/`, `scripts/`, `.github/` that
  no workflow, Makefile, Dockerfile, or package.json script references. Grep the
  script filename across all workflow YAML, Makefiles, and manifests; zero hits
  is a strong signal.
- **Disabled workflows**: names like `*.yml.disabled`, `*.yml.bak`, or
  workflows whose every job has a false condition.

CI files are cheap to keep and expensive to wrongly delete (a workflow may run
on a schedule, on tags only, or via `workflow_call` from another repo). Anything
tag-triggered, scheduled, or reusable is Tier 2 minimum unless the user confirms.

## Unused config files

The core trick: map each config file to the tool that consumes it, then check
whether that tool is still present in dependencies, CI, or scripts.

Common tool-to-config pairs the scanner checks:

| Config file | Dead if... |
|---|---|
| `.babelrc`, `babel.config.js` | no babel packages in package.json and no bundler using it |
| `tslint.json` | tslint absent (it is deprecated; likely replaced by ESLint) |
| `.flowconfig` | flow-bin absent |
| `bower.json`, `.bowerrc` | almost always dead; bower is retired |
| `.eslintrc*` duplicates | more than one at the same level, or eslint absent |
| `tox.ini`, `setup.cfg` sections | tools they configure absent from dev deps |
| `Procfile` | no Heroku deploy in CI or docs |
| `.dockerignore` | no Dockerfile anywhere |
| `docker-compose*.yml` services | service builds a path that no longer exists |
| `webpack.config.js`, `gulpfile.js`, `Gruntfile.js` | the corresponding tool absent |
| `.env.example` keys | variables no source file reads |

Verification per candidate: grep the tool name in every manifest
(package.json, pyproject.toml, Gemfile, go.mod), in CI YAML, and in Makefiles.
Absent everywhere = Tier 1. Present only in an old lockfile = Tier 2.

Config keys *inside* live files (unused env vars, dead feature flags in YAML)
are Tier 2 by default: apps read config dynamically, so grep each key as a
string in source before promoting to Tier 1.

## Report placement

These findings get their own section in the audit report, after "Unused
dependencies":

```
## Stale CI, configs, and junk files
<table: file | category (temp/ci/config) | why it is dead | evidence>
```
