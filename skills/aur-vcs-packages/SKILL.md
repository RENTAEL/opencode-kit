---
name: aur-vcs-packages
description: "Create and maintain VCS packages that build from live repository sources."
---
# Skill: aur-vcs-packages

## Purpose

Create and maintain VCS packages that build from live repository sources.

## Naming

- Append VCS suffix: `-git`, `-svn`, `-hg`, `-bzr`, `-darcs`, `-cvs`
- Example: `pkgname=my-app-git`
- Do **not** use a VCS suffix when the package fetches a specific release/tag and is not a rolling trunk build

## Source Array

Live trunk (checksums skipped ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â content changes):

```bash
makedepends=('git')   # include the VCS tool
source=("$pkgname::git+https://github.com/user/repo.git#branch=main")
sha256sums=('SKIP')
```

Pinned tag / commit (prefer a fixed tag **object** hash; force-pushed tag names are unsafe):

```bash
_tag=1234567890abcdef1234567890abcdef12345678  # git rev-parse "v$pkgver"
source=("git+https://github.com/user/repo.git?signed#tag=$_tag")
# Pinning a tag/commit allows real checksums ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run updpkgsums / makepkg -g
b2sums=('ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦')
```

Do **not** write `_tag=$(git rev-parse ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦)` in the PKGBUILD ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that runs at parse time before clone. Hardcode the hash and bump it with `pkgver`.

General form: `source=('[folder::][vcs+]url[#fragment]')`. Do not put `$pkgver` in the optional `folder` name ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `pkgver()` may rewrite it mid-build.

## Relations

```bash
conflicts=('my-app')
provides=("my-app=${pkgver}")
# Avoid replaces=() for VCS packages ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it causes unnecessary problems
```

## Dynamic pkgver()

Declare a static `pkgver` as a starting value; makepkg runs `pkgver()` after `prepare()` and rewrites it. Preferred format: `RELEASE.rREVISION` (the `r` delimiter keeps ordering when upstream cuts a first release).

Git with annotated tags (use `--abbrev=7`):

```bash
pkgver() {
  cd "$srcdir/$pkgname"
  git describe --long --abbrev=7 | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}
# ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 2.0.r6.ga17a017
```

Git with any tags:

```bash
pkgver() {
  cd "$srcdir/$pkgname"
  git describe --long --tags --abbrev=7 | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}
```

No tags (revision count + short hash):

```bash
pkgver() {
  cd "$srcdir/$pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short=7 HEAD)"
}
```

Fallback when tags appear later (bashism):

```bash
pkgver() {
  cd "$srcdir/$pkgname"
  ( set -o pipefail
    git describe --long --abbrev=7 2>/dev/null | sed 's/\([^-]*-g\)/r\1/;s/-/./g' ||
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short=7 HEAD)"
  )
}
```

## Important Rules

- **Do NOT commit mere pkgver bumps** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only commit structural PKGBUILD changes
- VCS packages are NOT "out of date" just because upstream has new commits
- Internet connection required at build time (note this in comments)
- Use `SKIP` for **mutable** VCS sources (branch/trunk); pinned `#tag=` / `#commit=` may use real checksums
- Always test that `makepkg -o` (download + prepare) succeeds
- Shallow clones are intentionally unsupported by makepkg

## Related

- `aur-pkgbuild` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PKGBUILD structure
- `aur-submission` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â submitting the package
- Wiki: https://wiki.archlinux.org/title/VCS_package_guidelines
