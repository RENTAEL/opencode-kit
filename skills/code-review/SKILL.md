---
name: code-review
description: "Review code changes for security, performance, and correctness. Trigger with a PR URL or diff, \"review this before I merge\", \"is this code safe?\", or when checking a change for N+1 queries, injection risks, missing edge cases, or error handling gaps."
allowed-tools: Read, Glob, Grep
argument-hint: <PR URL, diff, or file path>
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, yazÃƒâ€žÃ‚Â±lan kodun commit'lenmeden veya push'lanmadan ÃƒÆ’Ã‚Â¶nce sistematik
  biÃƒÆ’Ã‚Â§imde incelenmesini saÃƒâ€žÃ…Â¸lar. Hem "review isteÃƒâ€žÃ…Â¸i hazÃƒâ€žÃ‚Â±rlama" (requesting) hem de
  "review feedback'ini yanÃƒâ€žÃ‚Â±tlama" (receiving) sÃƒÆ’Ã‚Â¼reÃƒÆ’Ã‚Â§lerini kapsar.
  Kod kalitesi, gÃƒÆ’Ã‚Â¼venlik, test coverage, mimari uyum ve dokÃƒÆ’Ã‚Â¼mantasyon kontrol edilir.

  NE ZAMAN: Commit ÃƒÆ’Ã‚Â¶ncesi (kendi kendine review), PR aÃƒÆ’Ã‚Â§madan ÃƒÆ’Ã‚Â¶nce, bÃƒÆ’Ã‚Â¼yÃƒÆ’Ã‚Â¼k deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸ikliklerde.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    Review checklist raporu, yanÃƒâ€žÃ‚Â±tlanmÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸ feedback listesi, dÃƒÆ’Ã‚Â¼zeltilmiÃƒâ€¦Ã…Â¸ kod.
-->


# Code Review Skill

## Ãƒâ€žÃ‚Â°ki Mod

Bu skill iki farklÃƒâ€žÃ‚Â± durumda devreye girer:

| Mod | Ne Zaman | Ne Yapar |
|-----|----------|----------|
| **A ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Pre-Commit Review** | Commit ÃƒÆ’Ã‚Â¶ncesi, kendi kendinle | Checklist ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±r, commit'e hazÃƒâ€žÃ‚Â±r mÃƒâ€žÃ‚Â± karar ver |
| **B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Feedback Response** | BaÃƒâ€¦Ã…Â¸kasÃƒâ€žÃ‚Â± review yaptÃƒâ€žÃ‚Â±, feedback geldi | Her yorumu sÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±flandÃƒâ€žÃ‚Â±r, yanÃƒâ€žÃ‚Â±tla, dÃƒÆ’Ã‚Â¼zelt |

---

## MOD A: Pre-Commit Review (Kendi Kendine)

### 1. Diff'i ÃƒÆ’Ã¢â‚¬Â¡ek ve Analiz Et

```bash
git diff HEAD          # staged olmayan deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklikler
git diff --staged      # staged deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklikler
git diff main...HEAD   # branch'in tÃƒÆ’Ã‚Â¼m deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklikleri
```

Her deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸en dosyayÃƒâ€žÃ‚Â± gÃƒÆ’Ã‚Â¶zden geÃƒÆ’Ã‚Â§ir. PR'da yorum almak istemediÃƒâ€žÃ…Â¸in Ãƒâ€¦Ã…Â¸eyleri Ãƒâ€¦Ã…Â¸imdi dÃƒÆ’Ã‚Â¼zelt.

---

### 2. Checklist ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SÃƒâ€žÃ‚Â±rayla Uygula

#### ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ Kritik (bunlar varsa commit yok)

- [ ] Hardcoded secret, API key, password var mÃƒâ€žÃ‚Â±?
  ```bash
  git grep -i "password\|secret\|api_key\|token" -- '*.ts' '*.js' '*.py' '*.env'
  ```
- [ ] SQL injection vektÃƒÆ’Ã‚Â¶rÃƒÆ’Ã‚Â¼ var mÃƒâ€žÃ‚Â±? (raw query + user input)
- [ ] Authentication veya authorization bypass riski var mÃƒâ€žÃ‚Â±?
- [ ] Testler geÃƒÆ’Ã‚Â§iyor mu?
  ```bash
  npm test
  ```
- [ ] Build kÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±yor mu?
  ```bash
  npm run build
  ```
- [ ] BaÃƒâ€¦Ã…Â¸ka modÃƒÆ’Ã‚Â¼lleri kÃƒâ€žÃ‚Â±ran breaking change var mÃƒâ€žÃ‚Â±? (notify et)

#### ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ ÃƒÆ’Ã¢â‚¬â€œnemli (bunlar varsa ya dÃƒÆ’Ã‚Â¼zelt ya bilinÃƒÆ’Ã‚Â§li geÃƒÆ’Ã‚Â§)

- [ ] Yeni public fonksiyon/endpoint'in JSDoc veya tipi var mÃƒâ€žÃ‚Â±?
- [ ] Hata yÃƒÆ’Ã‚Â¶netimi yapÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â± mÃƒâ€žÃ‚Â±? (try-catch, error boundary, 404/500 handling)
- [ ] Konsola debug log bÃƒâ€žÃ‚Â±rakÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â± mÃƒâ€žÃ‚Â±? (`console.log`, `print`, `debugger`)
- [ ] Yeni env variable varsa `.env.example`'a eklendi mi?
- [ ] Herhangi bir TODO veya FIXME bÃƒâ€žÃ‚Â±rakÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â± mÃƒâ€žÃ‚Â±? (bilinÃƒÆ’Ã‚Â§liyse ticket numarasÃƒâ€žÃ‚Â± ekle)
- [ ] Code coverage dÃƒÆ’Ã‚Â¼Ãƒâ€¦Ã…Â¸tÃƒÆ’Ã‚Â¼ mÃƒÆ’Ã‚Â¼?
  ```bash
  npm test -- --coverage
  ```
- [ ] Yeni baÃƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±mlÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±k eklendiyse gÃƒÆ’Ã‚Â¼venlik kontrolÃƒÆ’Ã‚Â¼ yapÃƒâ€žÃ‚Â±ldÃƒâ€žÃ‚Â± mÃƒâ€žÃ‚Â±?
  ```bash
  npm audit
  ```

#### ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Âµ Kalite (mÃƒÆ’Ã‚Â¼kemmel kod iÃƒÆ’Ã‚Â§in)

- [ ] Fonksiyon isimleri ne yaptÃƒâ€žÃ‚Â±klarÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± anlatÃƒâ€žÃ‚Â±yor mu?
- [ ] Bir fonksiyon birden fazla Ãƒâ€¦Ã…Â¸ey yapÃƒâ€žÃ‚Â±yor mu? (bÃƒÆ’Ã‚Â¶lmeli)
- [ ] Kod kopyalandÃƒâ€žÃ‚Â± mÃƒâ€žÃ‚Â±? (copy-paste ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ extract to function)
- [ ] Magic number veya string var mÃƒâ€žÃ‚Â±? (constant'a extract et)
- [ ] Tip kullanÃƒâ€žÃ‚Â±mÃƒâ€žÃ‚Â± yeterince katÃƒâ€žÃ‚Â± mÃƒâ€žÃ‚Â±? (`any` var mÃƒâ€žÃ‚Â±?)

---

### 3. Review KartÃƒâ€žÃ‚Â± OluÃƒâ€¦Ã…Â¸tur

Commit mesajÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±n yanÃƒâ€žÃ‚Â±na veya PR aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±klamasÃƒâ€žÃ‚Â±na eklemek iÃƒÆ’Ã‚Â§in:

```markdown
## Self-Review ÃƒÆ’Ã¢â‚¬â€œzeti

**DeÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklik:** <ne yaptÃƒâ€žÃ‚Â±m, neden>
**Test Durumu:** ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ TÃƒÆ’Ã‚Â¼m testler geÃƒÆ’Ã‚Â§iyor / ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â X test skip edildi (gerekÃƒÆ’Ã‚Â§e: ...)
**Checklist:**
  - ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ Kritik: Temiz
  - ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ ÃƒÆ’Ã¢â‚¬â€œnemli: [varsa not]
  - ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Âµ Kalite: [varsa not]

**ÃƒÆ’Ã¢â‚¬â€œzellikle dikkat ÃƒÆ’Ã‚Â§ekilmek istenen:**
- <reviewer'Ãƒâ€žÃ‚Â±n bakmasÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± istediÃƒâ€žÃ…Â¸in yer>

**BilinÃƒÆ’Ã‚Â§li atlanan kÃƒâ€žÃ‚Â±sayollar (deliberate shortcuts):**
- <varsa gerekÃƒÆ’Ã‚Â§esiyle>
```

---

## MOD B: Feedback Response (BaÃƒâ€¦Ã…Â¸kasÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±n Review'Ãƒâ€žÃ‚Â±)

### 1. Her Yorumu SÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±flandÃƒâ€žÃ‚Â±r

Gelen her review yorumu iÃƒÆ’Ã‚Â§in:

```
[KRITIK]  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Blokerlik eder, merge edilemez ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hemen dÃƒÆ’Ã‚Â¼zelt
[ÃƒÆ’Ã¢â‚¬â€œNEMLI]  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ GÃƒÆ’Ã‚Â¼ÃƒÆ’Ã‚Â§lÃƒÆ’Ã‚Â¼ ÃƒÆ’Ã‚Â¶neri, iyi gerekÃƒÆ’Ã‚Â§en yoksa uygula
[ÃƒÆ’Ã¢â‚¬â€œNERI]   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Takdire baÃƒâ€žÃ…Â¸lÃƒâ€žÃ‚Â±, aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±k tartÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸ma gerekebilir
[SORU]    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Bilgi isteÃƒâ€žÃ…Â¸i ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±kla veya kod ile dÃƒÆ’Ã‚Â¼zelt
[NIT]     ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ KÃƒÆ’Ã‚Â¼ÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â¼k stil/isimlendirme, senin tercihine baÃƒâ€žÃ…Â¸lÃƒâ€žÃ‚Â±
```

### 2. Her Yorumu YanÃƒâ€žÃ‚Â±tla

**HiÃƒÆ’Ã‚Â§bir yorum cevapsÃƒâ€žÃ‚Â±z bÃƒâ€žÃ‚Â±rakÃƒâ€žÃ‚Â±lmaz.**

```markdown
Yorum: "Bu fonksiyonun timeout'u yok, servis yanÃƒâ€žÃ‚Â±t vermezse ne olur?"
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±f: [KRÃƒâ€žÃ‚Â°TÃƒâ€žÃ‚Â°K]
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Cevap: "HaklÃƒâ€žÃ‚Â±sÃƒâ€žÃ‚Â±n. 5 saniyelik timeout + retry ekledim. T3 commit'inde gÃƒÆ’Ã‚Â¶rebilirsin."
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Aksiyon: DÃƒÆ’Ã‚Â¼zeltildi ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦

Yorum: "Belki burada Map yerine Set kullanabilirsin"
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±f: [ÃƒÆ’Ã¢â‚¬â€œNERÃƒâ€žÃ‚Â°]
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Cevap: "Set burada doÃƒâ€žÃ…Â¸ru olur, key'e ihtiyacÃƒâ€žÃ‚Â±mÃƒâ€žÃ‚Â±z yok. DeÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸tirdim."
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Aksiyon: DÃƒÆ’Ã‚Â¼zeltildi ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦

Yorum: "Bu isimlendirme bana semantik gelmiyor"
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±f: [NIT]
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Cevap: "AnladÃƒâ€žÃ‚Â±m mantÃƒâ€žÃ‚Â±Ãƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± ama `processUserData` yerine `normalizeUserInput` daha aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±klayÃƒâ€žÃ‚Â±cÃƒâ€žÃ‚Â± ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸tirdim."
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Aksiyon: DÃƒÆ’Ã‚Â¼zeltildi ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦
```

### 3. DÃƒÆ’Ã‚Â¼zeltmeleri Grupla ve Commit At

Her dÃƒÆ’Ã‚Â¼zeltme grubunu ayrÃƒâ€žÃ‚Â± bir commit olarak at (`github` skill commit standardÃƒâ€žÃ‚Â±na gÃƒÆ’Ã‚Â¶re):

```bash
# Her dÃƒÆ’Ã‚Â¼zeltme ayrÃƒâ€žÃ‚Â± commit
git commit -m "fix: add timeout and retry to userService.fetchProfile"
git commit -m "refactor: use Set instead of Map in deduplication logic"
git commit -m "refactor: rename processUserData to normalizeUserInput"
```

### 4. Re-Review Ãƒâ€žÃ‚Â°ste

TÃƒÆ’Ã‚Â¼m dÃƒÆ’Ã‚Â¼zeltmeler tamamlandÃƒâ€žÃ‚Â±Ãƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±nda review'Ãƒâ€žÃ‚Â± gÃƒÆ’Ã‚Â¼ncelle:

```markdown
## DÃƒÆ’Ã‚Â¼zeltme ÃƒÆ’Ã¢â‚¬â€œzeti

Toplam yorum: 8
- DÃƒÆ’Ã‚Â¼zeltildi: 7
- Reddedildi (gerekÃƒÆ’Ã‚Â§eyle): 1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "NIT yorumu: mevcut isimlendirme proje konvansiyonuyla uyumlu"

ÃƒÆ’Ã¢â‚¬â€œnemli deÃƒâ€žÃ…Â¸iÃƒâ€¦Ã…Â¸iklikler:
- Timeout + retry mekanizmasÃƒâ€žÃ‚Â± eklendi (gÃƒÆ’Ã‚Â¼venlik aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±sÃƒâ€žÃ‚Â±ndan kritik)
- 2 refactor (netlik iÃƒÆ’Ã‚Â§in)

Re-review iÃƒÆ’Ã‚Â§in hazÃƒâ€žÃ‚Â±r.
```

---

## Kurallar

- **KÃƒâ€žÃ‚Â±rmÃƒâ€žÃ‚Â±zÃƒâ€žÃ‚Â± item varsa commit yok.** Ãƒâ€žÃ‚Â°stisna yok.
- **"Sonra dÃƒÆ’Ã‚Â¼zeltilir" yasak.** Ya Ãƒâ€¦Ã…Â¸imdi dÃƒÆ’Ã‚Â¼zelt ya da ticket aÃƒÆ’Ã‚Â§, ticket numarasÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± koda ekle.
- **Her review yorumu yanÃƒâ€žÃ‚Â±tlanÃƒâ€žÃ‚Â±r.** "Tamam" veya sessizlik kabul edilmez ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ya "dÃƒÆ’Ã‚Â¼zelttim" ya "katÃƒâ€žÃ‚Â±lmÃƒâ€žÃ‚Â±yorum, ÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â¼nkÃƒÆ’Ã‚Â¼..."
- **Review kendini kandÃƒâ€žÃ‚Â±rmak iÃƒÆ’Ã‚Â§in deÃƒâ€žÃ…Â¸il, kodu korumak iÃƒÆ’Ã‚Â§in.** Checklist'i hÃƒâ€žÃ‚Â±zlÃƒâ€žÃ‚Â±ca geÃƒÆ’Ã‚Â§iÃƒâ€¦Ã…Â¸tirme.
- **Gelen feedback kiÃƒâ€¦Ã…Â¸isel deÃƒâ€žÃ…Â¸il.** Yorum koda yapÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±yor, sana deÃƒâ€žÃ…Â¸il.
