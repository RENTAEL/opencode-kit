---
name: aur-helpers
description: "Use AUR helper tools to search, build, install, and manage AUR packages."
---
# Skill: aur-helpers

## Purpose

Use AUR helper tools to search, build, install, and manage AUR packages.

## yay

```bash
yay -S pkgname           # search + install from AUR/official
yay -Syu                 # system update + AUR update
yay -R pkgname           # remove package
yay -Q                   # query installed
yay -Ps                  # print system stats
yay -Yc                  # clean unneeded deps
yay -G pkgname           # get PKGBUILD from AUR
yay --gendb              # generate dev DB
```

## paru

```bash
paru -S pkgname          # search + install
paru -Syu                # full system update with AUR
paru -R pkgname          # remove
paru -G pkgname          # get PKGBUILD
paru --report            # show outdated AUR packages
paru --clean             # remove build files
paru -Pg                 # print config
```

## Key Differences

| Feature | yay | paru |
|---------|-----|------|
| Config | ~/.config/yay/config.json | /etc/paru.conf / ~/.paru.conf |
| Language | Go | Rust |
| PKGBUILD review | show-diff by default | diff by default |
| Dev mode | yay -G | paru -G |

## Safety

- **Always review the PKGBUILD** before building ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â helpers don't replace human review
- Use `--noconfirm` carefully ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it skips all prompts including diffs
- Check for suspicious sources, install paths, or post-install scripts
- Use a scanner (`traur`, `ks-aur-scanner`) before installing unfamiliar packages
- Prefer building in a chroot: `yay -S --builddir /tmp/pkg pkgname`
- AUR helpers are [officially unsupported](https://bbs.archlinux.org/viewtopic.php?pid=828310#p828310)

## Related

- `aur-pacman` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â underlying pacman commands
- `aur-pkgbuild` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â understanding PKGBUILDs
- `aur-rpc` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the JSON RPC helpers query under the hood
