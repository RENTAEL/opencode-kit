---
name: github
description: "**HiÃƒÆ’Ã‚Â§bir commit `code-review` skill ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmadan atÃƒâ€žÃ‚Â±lmaz.** Bu kural ihlal edilemez. \"KÃƒÆ’Ã‚Â¼ÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â¼k deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklik\" veya \"sadece bir satÃƒâ€žÃ‚Â±r\" istisnasÃƒâ€žÃ‚Â± yoktur."
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, tÃƒÆ’Ã‚Â¼m git iÃƒâ€¦Ã…Â¸lemlerini (commit, push, branch yÃƒÆ’Ã‚Â¶netimi, PR oluÃƒâ€¦Ã…Â¸turma)
  standart, gÃƒÆ’Ã‚Â¼venli ve tutarlÃƒâ€žÃ‚Â± biÃƒÆ’Ã‚Â§imde yÃƒÆ’Ã‚Â¶netir. Commit ÃƒÆ’Ã‚Â¶ncesi otomatik olarak
  `code-review` skill'ini ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±r. Conventional Commits standardÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± uygular.
  "ÃƒÆ’Ã¢â‚¬Â¡alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â±yor, attÃƒâ€žÃ‚Â±m" yerine "incelendi, standarda uygun, dokÃƒÆ’Ã‚Â¼mante edildi, atÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â±" der.

  NE ZAMAN: Herhangi bir git iÃƒâ€¦Ã…Â¸lemi yapÃƒâ€žÃ‚Â±lacaÃƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±nda ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â commit, push, branch oluÃƒâ€¦Ã…Â¸turma,
            PR aÃƒÆ’Ã‚Â§ma, tag. Bu skill atlanarak doÃƒâ€žÃ…Â¸rudan git komutu ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmaz.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    Clean commit history, PR aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±klamasÃƒâ€žÃ‚Â±, gÃƒÆ’Ã‚Â¼ncellenmiÃƒâ€¦Ã…Â¸ CHANGELOG.
-->


# GitHub Skill

## Temel Kural

**HiÃƒÆ’Ã‚Â§bir commit `code-review` skill ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmadan atÃƒâ€žÃ‚Â±lmaz.**  
Bu kural ihlal edilemez. "KÃƒÆ’Ã‚Â¼ÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â¼k deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklik" veya "sadece bir satÃƒâ€žÃ‚Â±r" istisnasÃƒâ€žÃ‚Â± yoktur.

---

## Commit StandardÃƒâ€žÃ‚Â± ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conventional Commits

### Format

```
<type>(<scope>): <subject>

[body ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â opsiyonel]

[footer ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â opsiyonel]
```

### Type Listesi

| Type | Ne Zaman KullanÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±r |
|------|-------------------|
| `feat` | Yeni ÃƒÆ’Ã‚Â¶zellik |
| `fix` | Bug dÃƒÆ’Ã‚Â¼zeltmesi |
| `refactor` | DavranÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸ deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸meden kod dÃƒÆ’Ã‚Â¼zenlemesi |
| `style` | Formatlama, boÃƒâ€¦Ã…Â¸luk (iÃƒâ€¦Ã…Â¸levsel deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklik yok) |
| `test` | Test ekleme veya dÃƒÆ’Ã‚Â¼zenleme |
| `docs` | DokÃƒÆ’Ã‚Â¼mantasyon deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ikliÃƒâ€žÃ…Â¸i |
| `chore` | Build, dependency, config gÃƒÆ’Ã‚Â¼ncellemesi |
| `perf` | Performans iyileÃƒâ€¦Ã…Â¸tirmesi |
| `ci` | CI/CD pipeline deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ikliÃƒâ€žÃ…Â¸i |
| `revert` | ÃƒÆ’Ã¢â‚¬â€œnceki commit'i geri alma |

### Scope (Opsiyonel ama ÃƒÆ’Ã¢â‚¬â€œnerilir)

Etkilenen modÃƒÆ’Ã‚Â¼l, komponent veya katman:
```
feat(auth): add refresh token rotation
fix(userService): handle null email in validation
refactor(Button): extract loading state to hook
chore(deps): upgrade react to 19.2.0
```

### Subject KurallarÃƒâ€žÃ‚Â±

- **Ãƒâ€žÃ‚Â°mperative mood** kullan (TÃƒÆ’Ã‚Â¼rkÃƒÆ’Ã‚Â§e: emir kipi): "add" not "added", "fix" not "fixed"
- **KÃƒÆ’Ã‚Â¼ÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â¼k harf** ile baÃƒâ€¦Ã…Â¸la
- **Nokta ile bitirme**
- **72 karakter** sÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±
- **Ne** deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸tiÃƒâ€žÃ…Â¸ini yaz, **neden** body'de aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±kla

### Body (Neden DeÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ti?)

```
feat(auth): add refresh token rotation

Statik refresh token'lar ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±rsa sÃƒÆ’Ã‚Â¼resiz eriÃƒâ€¦Ã…Â¸im saÃƒâ€žÃ…Â¸lar.
Rotation ile her kullanÃƒâ€žÃ‚Â±mda yeni token ÃƒÆ’Ã‚Â¼retilir, eskisi geÃƒÆ’Ã‚Â§ersiz kÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±r.
RFC 6749 gÃƒÆ’Ã‚Â¼venlik ÃƒÆ’Ã‚Â¶nerisi doÃƒâ€žÃ…Â¸rultusunda implement edildi.
```

### Breaking Change

```
feat(api)!: change user ID format from integer to UUID

BREAKING CHANGE: TÃƒÆ’Ã‚Â¼m /api/users/:id endpoint'leri artÃƒâ€žÃ‚Â±k UUID string
bekliyor. Integer ID kullanan client'lar gÃƒÆ’Ã‚Â¼ncellenmeli.

Migration guide: docs/migrations/integer-to-uuid.md
```

---

## Tam Ãƒâ€žÃ‚Â°Ãƒâ€¦Ã…Â¸ AkÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â±

### 1. Branch OluÃƒâ€¦Ã…Â¸tur

```bash
# Format: <type>/<kÃƒâ€žÃ‚Â±sa-aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±klama>
git checkout -b feat/user-registration
git checkout -b fix/token-refresh-null-check
git checkout -b refactor/button-loading-state
```

Branch isimlendirme kurallarÃƒâ€žÃ‚Â±:
- Lowercase, kebab-case
- Type ile baÃƒâ€¦Ã…Â¸lar (`feat/`, `fix/`, `refactor/`, `hotfix/`)
- `main` veya `master`'a direkt commit atÃƒâ€žÃ‚Â±lmaz

---

### 2. Code Review ÃƒÆ’Ã¢â‚¬Â¡alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±r

Commit atmadan ÃƒÆ’Ã‚Â¶nce **`code-review` skill'ini aÃƒÆ’Ã‚Â§ ve MOD A'yÃƒâ€žÃ‚Â± uygula**.

```bash
# ÃƒÆ’Ã¢â‚¬â€œnce ne deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸tiÃƒâ€žÃ…Â¸ini kontrol et
git status
git diff --staged
```

Code review checklist tamamlanmadan 3. adÃƒâ€žÃ‚Â±ma geÃƒÆ’Ã‚Â§ilmez.

---

### 3. Stage ve Commit

```bash
# Ãƒâ€žÃ‚Â°lgili dosyalarÃƒâ€žÃ‚Â± stage'e al ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hepsini deÃƒâ€žÃ…Â¸il, mantÃƒâ€žÃ‚Â±klÃƒâ€žÃ‚Â± gruplar halinde
git add src/services/userService.ts src/services/userService.test.ts

# Commit at ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â standarda gÃƒÆ’Ã‚Â¶re
git commit -m "feat(userService): add createUser with password hashing

Yeni kullanÃƒâ€žÃ‚Â±cÃƒâ€žÃ‚Â± kaydÃƒâ€žÃ‚Â± iÃƒÆ’Ã‚Â§in service katmanÃƒâ€žÃ‚Â± eklendi.
bcrypt ile password hash'leniyor (saltRounds: 12).
Duplicate email durumunda DuplicateEmailError fÃƒâ€žÃ‚Â±rlatÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±yor.

Testler: userService.test.ts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 8 test, hepsi geÃƒÆ’Ã‚Â§iyor"
```

**Atomik commit'ler:**
- Bir commit, bir mantÃƒâ€žÃ‚Â±ksal deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklik
- Migration + model + service = 3 ayrÃƒâ€žÃ‚Â± commit
- "misc fixes" veya "wip" commit'leri yasak

---

### 4. Her Commit SonrasÃƒâ€žÃ‚Â± Kontrol

```bash
git log --oneline -5    # Son commit'lere bak
git show HEAD           # Son commit'in diff'ini kontrol et
```

Commit mesajÃƒâ€žÃ‚Â± yanlÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸sa hemen dÃƒÆ’Ã‚Â¼zelt (push ÃƒÆ’Ã‚Â¶ncesinde):
```bash
git commit --amend -m "fix(auth): handle null refresh token in rotation"
```

---

### 5. Push

```bash
# Ãƒâ€žÃ‚Â°lk push ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â upstream set et
git push -u origin feat/user-registration

# Sonraki push'lar
git push
```

**Push ÃƒÆ’Ã‚Â¶ncesi:**
```bash
# Testler son kez ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±r
npm test

# Main'den geride mi? Rebase et
git fetch origin
git rebase origin/main
```

---

### 6. Pull Request OluÃƒâ€¦Ã…Â¸tur

GitHub CLI ile (PR Ãƒâ€¦Ã…Â¸ablonu inline ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `.github/PR_TEMPLATE.md` yoksa aÃƒâ€¦Ã…Â¸aÃƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±dakini kullan):

```bash
gh pr create \
  --title "feat(auth): user registration with email verification" \
  --base main \
  --label "feature" \
  --body "## Ne DeÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ti?
<2-3 cÃƒÆ’Ã‚Â¼mle: ne yapÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â±, neden>

## NasÃƒâ€žÃ‚Â±l Test Edildi?
- [ ] Unit testler: \`npm test\` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â X/X geÃƒÆ’Ã‚Â§iyor
- [ ] Integration test: manuel doÃƒâ€žÃ…Â¸rulandÃƒâ€žÃ‚Â±
- [ ] Edge case'ler test edildi

## Checklist
- [ ] Code review (MOD A) tamamlandÃƒâ€žÃ‚Â±
- [ ] Testler geÃƒÆ’Ã‚Â§iyor
- [ ] Breaking change varsa CHANGELOG gÃƒÆ’Ã‚Â¼ncellendi
- [ ] Yeni env variable varsa \`.env.example\`'a eklendi
- [ ] \`documentation-sync\` skill ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â± (API deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ikliÃƒâ€žÃ…Â¸i varsa)

## Ãƒâ€žÃ‚Â°lgili
- Closes #Ãƒâ€žÃ‚Â°SSUE_NUMARASI"
```

> **Not:** Ekip `.github/PR_TEMPLATE.md` oluÃƒâ€¦Ã…Â¸turursa, body kÃƒâ€žÃ‚Â±smÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± `--body "$(cat .github/PR_TEMPLATE.md)"` ile deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸tir.

---

### 7. CHANGELOG GÃƒÆ’Ã‚Â¼ncelle

Her PR iÃƒÆ’Ã‚Â§in `CHANGELOG.md`'nin `[Unreleased]` bÃƒÆ’Ã‚Â¶lÃƒÆ’Ã‚Â¼mÃƒÆ’Ã‚Â¼ne ekle:

```markdown
## [Unreleased]

### Added
- User registration endpoint (POST /api/auth/register) with email verification

### Fixed
- Null refresh token causing 500 error on token rotation

### Changed
- User ID format migrated from integer to UUID (breaking)
```

---

## ÃƒÆ’Ã¢â‚¬â€œzel Durumlar

### Hotfix (Production Emergency)
```bash
# Main'den hotfix branch aÃƒÆ’Ã‚Â§
git checkout -b hotfix/null-pointer-login main

# DÃƒÆ’Ã‚Â¼zelt ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ test ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commit
git commit -m "fix(auth): prevent null pointer when user session expires"

# Hem main'e hem aktif development branch'e merge
git checkout main && git merge hotfix/null-pointer-login
git checkout develop && git merge hotfix/null-pointer-login
```

### Commit Geri Alma (Push ÃƒÆ’Ã¢â‚¬â€œncesi)
```bash
git reset HEAD~1 --soft    # Commit geri al, deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklikler staged kalÃƒâ€žÃ‚Â±r
```

### Tag ve Release
```bash
git tag -a v1.2.0 -m "Release v1.2.0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user registration feature"
git push origin v1.2.0
```

---

## Yasaklar

- `git push --force` (force push) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sadece personal branch'te, hiÃƒÆ’Ã‚Â§bir zaman `main`'e
- `git commit -m "fix"` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â anlamsÃƒâ€žÃ‚Â±z commit mesajÃƒâ€žÃ‚Â±
- `git add .` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â staging kontrol edilmeden hepsini ekleme
- `git commit --no-verify` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pre-commit hook'larÃƒâ€žÃ‚Â± atlama
- Direkt `main`'e push ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pull request olmadan

---

## HÃƒâ€žÃ‚Â±zlÃƒâ€žÃ‚Â± Referans

```bash
# Tam iÃƒâ€¦Ã…Â¸ akÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â±
git checkout -b feat/my-feature           # 1. Branch
# ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ code-review skill (MOD A)             # 2. Review
git add <ilgili dosyalar>                  # 3. Stage
git commit -m "feat(scope): description"  # 4. Commit
git push -u origin feat/my-feature        # 5. Push
gh pr create --title "..." --body "..."   # 6. PR
```
