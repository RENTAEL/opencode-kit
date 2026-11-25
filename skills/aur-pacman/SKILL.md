---
name: aur-pacman
description: "Manage Arch Linux packages with pacman ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the package manager."
---
# Skill: aur-pacman

## Purpose

Manage Arch Linux packages with pacman ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the package manager.

## Basic Operations

```bash
pacman -Syu              # full system update
pacman -S pkgname        # install package
pacman -R pkgname        # remove package
pacman -Rs pkgname       # remove + unused dependencies
pacman -U /path/to/pkg.tar.zst  # install local file
```

## Search & Query

```bash
pacman -Ss keyword       # search remote repos
pacman -Qs keyword       # search installed packages
pacman -Si pkgname       # remote package info
pacman -Qi pkgname       # installed package info
pacman -Ql pkgname       # files owned by package
pacman -Qo /path/file    # which package owns file
pacman -Fl pattern       # list files in a sync-DB package (Files DB; not pkgfile)
pacman -Qdt              # orphaned packages
pacman -Qmq              # foreign packages (typically AUR)
```

## Cache Management

```bash
paccache -r              # remove old cached versions (keep last 3)
pacman -Sc               # remove unused cached packages
pacman -Scc              # clean everything from cache
```

## Useful Flags

- `--noconfirm` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip prompts
- `--needed` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't reinstall up-to-date packages
- `--overwrite glob` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â overwrite conflicting files
- `--print` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print what would be done (dry run)

## Database

```bash
pacman -Syy              # force refresh all databases
pacman-key --init        # initialize keyring
pacman-key --populate    # load default keys
```

## Related

- `aur-helpers` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â yay, paru wrappers
