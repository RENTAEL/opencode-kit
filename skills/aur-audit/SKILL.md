---
name: aur-audit
description: "Audit and validate PKGBUILDs before building or submitting to AUR."
---
# Skill: aur-audit

## Purpose

Audit and validate PKGBUILDs before building or submitting to AUR.

## Validation Commands

```bash
namcap PKGBUILD                          # check PKGBUILD
namcap *.pkg.tar.zst                     # check built package
shellcheck --shell=bash --exclude=SC2034,SC2154,SC2164 PKGBUILD
makepkg --printsrcinfo > .SRCINFO        # regenerate before push
makerepropkg *.pkg.tar.zst               # verify reproducible build (devtools)
```

## PKGBUILD Scanners

Third-party scanners catch malicious or dangerous patterns that namcap misses:

- **`traur`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â static analyzer for suspicious PKGBUILD content
- **`ks-aur-scanner`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â KDE-integrated scanner

These are *aids*, not substitutes for manual review.

## Signature Verification

Check whether the PKGBUILD's `source=()` references a `.sig` or `.asc` signature file. If so:

1. Look up keys in `validpgpkeys=()`
2. Import with `gpg --recv-keys <FINGERPRINT>`
3. Verify with `gpg --verify <source>.sig <source>`

Note: signed code can still be malicious ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â review the *content*, not just the signature.

## Diff Before Building

```bash
git show                # inspect last commit
git difftool @~..@ --tool=vimdiff   # full diff view
```

## Common Errors

| Error | Fix |
|-------|-----|
| Missing `depends` | `find-libdeps` (devtools) or `ldd` on binaries, then add to PKGBUILD |
| Missing `makedepends` | Add build-time deps (`base-devel` is assumed) |
| `sha256sums` mismatch | Run `updpkgsums` |
| `pkgver` has hyphen | Replace with underscore (or quote for upstream use) |
| Bad `license` format | Use SPDX: `MIT`, `GPL-3.0-or-later`, `BSD-3-Clause`, `0BSD` |
| `source` URL unreachable | Verify URL; use `name::url` syntax to rename |
| `pkgdesc` self-referencing | "An editor for X" not "X is an editor for" |
| Missing `.SRCINFO` | `makepkg --printsrcinfo > .SRCINFO` |
| Missing LICENSE / REUSE.toml | `pkgctl license setup` then `pkgctl license check` |
| Path with spaces | Quote `"$pkgdir"` and `"$srcdir"` |
| `/usr/libexec/` use | Move to `/usr/lib/$pkgname/` |
| Used `msg`/`msg2`/`error`/`warning`/`plain` | Replace with `printf` or `echo` |
| Hash doesn't match a mutable `git+...` branch | Use `SKIP`, or pin `#tag=`/`#commit=` and store a hardcoded tag object hash (`_tag=ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`) |

## Chroot Testing

```bash
pkgctl build              # builds in clean chroot via systemd-nspawn
extra-x86_64-build        # lower-level alternative from devtools
```

Catches issues that work on your system but fail in clean environments.

## Reproducible Builds

Verify your build is reproducible:

```bash
makerepropkg *.pkg.tar.zst          # devtools
repro -f *.pkg.tar.zst              # archlinux-repro
```

If timestamps are required at build time, set `SOURCE_DATE_EPOCH`.

## Pre-submission Checklist

- [ ] `namcap PKGBUILD` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no errors
- [ ] `namcap *.pkg.tar.zst` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no errors (if built)
- [ ] `shellcheck PKGBUILD` with standard exclusions
- [ ] `.SRCINFO` regenerated
- [ ] `makepkg -s` builds successfully
- [ ] `makepkg --check` tests pass (if applicable)
- [ ] `pkgctl license check` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â clean (REUSE.toml compliant)
- [ ] `traur` / `ks-aur-scanner` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no critical findings
- [ ] PGP signatures (if any) verified
- [ ] Git diff reviewed

## Related

- `aur-pkgbuild` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fixing found issues
- `aur-submission` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â push after audit passes
- `aur-rpc` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify metadata (OutOfDate, votes, popularity) before assuming state
