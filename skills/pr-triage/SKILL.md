---
name: pr-triage
description: "**DÃƒÆ’Ã‚Â©clencheurs** :"
---
# PR Triage

## Quand utiliser

| Skill | Usage | Output |
|-------|-------|--------|
| `/pr-triage` | Trier, reviewer, commenter les PRs | Tableau d'action + reviews + commentaires postÃƒÆ’Ã‚Â©s |
| `/repo-recap` | RÃƒÆ’Ã‚Â©cap gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©ral pour partager avec l'ÃƒÆ’Ã‚Â©quipe | RÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© Markdown (PRs + issues + releases) |

**DÃƒÆ’Ã‚Â©clencheurs** :
- Manuellement : `/pr-triage` ou `/pr-triage all` ou `/pr-triage 42 57`
- Proactivement : quand >5 PRs ouvertes sans review, ou PR stale >14j dÃƒÆ’Ã‚Â©tectÃƒÆ’Ã‚Â©e

---

## Langue

- VÃƒÆ’Ã‚Â©rifier l'argument passÃƒÆ’Ã‚Â© au skill
- Si `en` ou `english` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ tableaux et rÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© en anglais
- Si `fr`, `french`, ou pas d'argument ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ franÃƒÆ’Ã‚Â§ais (dÃƒÆ’Ã‚Â©faut)
- Note : les commentaires GitHub (Phase 3) restent TOUJOURS en anglais (audience internationale)

---

Workflow en 3 phases : audit automatique ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ deep review opt-in ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commentaires avec validation obligatoire.

## PrÃƒÆ’Ã‚Â©conditions

```bash
git rev-parse --is-inside-work-tree
gh auth status
```

Si l'un ÃƒÆ’Ã‚Â©choue, stop et expliquer ce qui manque.

---

## Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Audit (toujours exÃƒÆ’Ã‚Â©cutÃƒÆ’Ã‚Â©e)

### Data Gathering (commandes en parallÃƒÆ’Ã‚Â¨le)

```bash
# IdentitÃƒÆ’Ã‚Â© du repo
gh repo view --json nameWithOwner -q .nameWithOwner

# PRs ouvertes avec mÃƒÆ’Ã‚Â©tadonnÃƒÆ’Ã‚Â©es complÃƒÆ’Ã‚Â¨tes (ajouter body pour cross-rÃƒÆ’Ã‚Â©fÃƒÆ’Ã‚Â©rence issues)
gh pr list --state open --limit 50 \
  --json number,title,author,createdAt,updatedAt,additions,deletions,changedFiles,isDraft,mergeable,reviewDecision,statusCheckRollup,body

# Collaborateurs (pour distinguer "nos PRs" des externes)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Fallback collaborateurs** : si `gh api .../collaborators` ÃƒÆ’Ã‚Â©choue (403/404) :
```bash
# Extraire les auteurs des 10 derniers PRs mergÃƒÆ’Ã‚Â©s
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
Si toujours ambigu, demander ÃƒÆ’Ã‚Â  l'utilisateur via `AskUserQuestion`.

Pour chaque PR, rÃƒÆ’Ã‚Â©cupÃƒÆ’Ã‚Â©rer reviews existantes ET fichiers modifiÃƒÆ’Ã‚Â©s :

```bash
gh api "repos/{owner}/{repo}/pulls/{num}/reviews" \
  --jq '[.[] | .user.login + ":" + .state] | join(", ")'

# Fichiers modifiÃƒÆ’Ã‚Â©s (nÃƒÆ’Ã‚Â©cessaire pour overlap detection)
gh pr view {num} --json files --jq '[.files[].path] | join(",")'
```

**Note rate-limiting** : la rÃƒÆ’Ã‚Â©cupÃƒÆ’Ã‚Â©ration des fichiers est N appels API (1 par PR). Pour repos avec 20+ PRs, prioriser les PRs candidates ÃƒÆ’Ã‚Â  l'overlap (mÃƒÆ’Ã‚Âªme domaine fonctionnel, mÃƒÆ’Ã‚Âªme auteur).

**Note** : `author` est un objet `{login: "..."}` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â toujours extraire `.author.login`.

### Analyse

**Classification taille** :
| Label | Additions |
|-------|-----------|
| XS | < 50 |
| S | 50ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“200 |
| M | 200ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“500 |
| L | 500ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1000 |
| XL | > 1000 |

Format taille : `+{additions}/-{deletions}, {files} files ({label})`

**DÃƒÆ’Ã‚Â©tections** :
- **Overlaps** : comparer les listes de fichiers entre PRs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â si >50% de fichiers en commun ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ cross-reference
- **Clusters** : auteur avec 3+ PRs ouvertes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ suggÃƒÆ’Ã‚Â©rer ordre de review (plus petite en premier)
- **Staleness** : aucune activitÃƒÆ’Ã‚Â© depuis >14j ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flag "stale"
- **CI status** : via `statusCheckRollup` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `clean` / `unstable` / `dirty`
- **Reviews** : approved / changes_requested / aucune

**Liens PR ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Â Issues** :
- Scanner le `body` de chaque PR pour `fixes #N`, `closes #N`, `resolves #N` (case-insensitive)
- Si trouvÃƒÆ’Ã‚Â©, afficher dans le tableau : `Fixes #42` dans la colonne Action/Status

**CatÃƒÆ’Ã‚Â©gorisation** :

_Nos PRs_ : auteur dans la liste des collaborateurs

_Externes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PrÃƒÆ’Ã‚Âªtes_ : additions ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1000 ET files ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 10 ET `mergeable` ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â  `CONFLICTING` ET CI clean/unstable

_Externes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ProblÃƒÆ’Ã‚Â©matiques_ : un des critÃƒÆ’Ã‚Â¨res suivants :
- additions > 1000 OU files > 10
- OU `mergeable` == `CONFLICTING` (conflit de merge)
- OU CI dirty (statusCheckRollup contient des ÃƒÆ’Ã‚Â©checs)
- OU overlap avec une autre PR ouverte (>50% fichiers communs)

### Output ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Tableau de triage

```
## PRs ouvertes ({count})

### Nos PRs
| PR | Titre | Taille | CI | Status |
| -- | ----- | ------ | -- | ------ |

### Externes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PrÃƒÆ’Ã‚Âªtes pour review
| PR | Auteur | Titre | Taille | CI | Reviews | Action |
| -- | ------ | ----- | ------ | -- | ------- | ------ |

### Externes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ProblÃƒÆ’Ã‚Â©matiques
| PR | Auteur | Titre | Taille | ProblÃƒÆ’Ã‚Â¨me | Action recommandÃƒÆ’Ã‚Â©e |
| -- | ------ | ----- | ------ | -------- | ------------------ |

### RÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â©
- Quick wins : {PRs XS/S prÃƒÆ’Ã‚Âªtes ÃƒÆ’Ã‚Â  merger}
- Risques : {overlaps, tailles XL, CI dirty}
- Clusters : {auteurs avec 3+ PRs}
- Stale : {PRs sans activitÃƒÆ’Ã‚Â© >14j}
- Overlaps : {PRs qui touchent les mÃƒÆ’Ã‚Âªmes fichiers}
```

0 PRs ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ afficher `Aucune PR ouverte.` et terminer.

### Copie automatique

AprÃƒÆ’Ã‚Â¨s affichage du tableau de triage, copier dans le presse-papier :
```bash
# Cross-platform clipboard
clip() {
  if command -v pbcopy &>/dev/null; then pbcopy
  elif command -v xclip &>/dev/null; then xclip -selection clipboard
  elif command -v wl-copy &>/dev/null; then wl-copy
  else cat
  fi
}

clip <<'EOF'
{tableau de triage complet}
EOF
```
Confirmer : `Tableau copiÃƒÆ’Ã‚Â© dans le presse-papier.` (FR) / `Triage table copied to clipboard.` (EN)

---

## Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Deep Review (opt-in)

### SÃƒÆ’Ã‚Â©lection des PRs

**Si argument passÃƒÆ’Ã‚Â©** :
- `"all"` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ toutes les PRs externes
- NumÃƒÆ’Ã‚Â©ros (`"42 57"`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ uniquement ces PRs
- Pas d'argument ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ proposer via `AskUserQuestion`

**Si pas d'argument**, afficher :

```
question: "Quelles PRs voulez-vous reviewer en profondeur ?"
header: "Deep Review"
multiSelect: true
options:
  - label: "Toutes les externes"
    description: "Review {N} PRs externes avec agents code-reviewer en parallÃƒÆ’Ã‚Â¨le"
  - label: "ProblÃƒÆ’Ã‚Â©matiques uniquement"
    description: "Focus sur les {M} PRs ÃƒÆ’Ã‚Â  risque (CI dirty, trop large, overlaps)"
  - label: "PrÃƒÆ’Ã‚Âªtes uniquement"
    description: "Review {K} PRs prÃƒÆ’Ã‚Âªtes ÃƒÆ’Ã‚Â  merger"
  - label: "Passer"
    description: "Terminer ici ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â juste l'audit"
```

**Note sur les drafts** :
- Les PRs en draft sont EXCLUES des options "Toutes les externes" et "PrÃƒÆ’Ã‚Âªtes uniquement"
- Les PRs en draft sont INCLUSES dans "ProblÃƒÆ’Ã‚Â©matiques uniquement" (car elles nÃƒÆ’Ã‚Â©cessitent attention)
- Pour reviewer un draft : taper son numÃƒÆ’Ã‚Â©ro explicitement (ex: `42`)

Si "Passer" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fin du workflow.

### ExÃƒÆ’Ã‚Â©cution des Reviews

Pour chaque PR sÃƒÆ’Ã‚Â©lectionnÃƒÆ’Ã‚Â©e, lancer un agent `code-reviewer` via **Task tool en parallÃƒÆ’Ã‚Â¨le** :

```
subagent_type: code-reviewer
model: sonnet
prompt: |
  Review PR #{num}: "{title}" by @{author}

  **Metadata**: +{additions}/-{deletions}, {changedFiles} files ({size_label})
  **CI**: {ci_status} | **Reviews**: {existing_reviews} | **Draft**: {isDraft}

  **PR Body**:
  {body}

  **Diff**:
  {gh pr diff {num} output}

  Apply your security-guardian and backend-architect skills for this review.
  Additionally, apply the RTK-specific checklist:
  - LazyLock<Regex> for fixed patterns reused across calls
  - anyhow::Result + .context() (no unwrap())
  - Fallback to raw command on filter failure
  - Exit code propagation
  - Token savings ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥60% in tests with real fixtures
  - No async/tokio dependencies

  Return structured review:
  ### Critical Issues ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´
  ### Important Issues ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡
  ### Suggestions ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¢
  ### What's Good ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦

  Be specific: quote the file:line, explain why it's an issue, suggest the fix.
```

RÃƒÆ’Ã‚Â©cupÃƒÆ’Ã‚Â©rer le diff via :
```bash
gh pr diff {num}
gh pr view {num} --json body,title,author -q '{body: .body, title: .title, author: .author.login}'
```

AgrÃƒÆ’Ã‚Â©ger tous les rapports. Afficher un rÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© aprÃƒÆ’Ã‚Â¨s toutes les reviews.

---

## Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Commentaires (validation obligatoire)

### GÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©ration des drafts

Pour chaque PR reviewÃƒÆ’Ã‚Â©e, gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rer un commentaire GitHub en utilisant le template `templates/review-comment.md`.

**RÃƒÆ’Ã‚Â¨gles** :
- Langue : **anglais** (audience internationale)
- Ton : professionnel, constructif, factuel
- Toujours inclure au moins 1 point positif
- Citer les lignes de code quand pertinent (format `file.rs:42`)

### Affichage et validation

**Afficher TOUS les commentaires draftÃƒÆ’Ã‚Â©s** au format :

```
---
### Draft ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PR #{num}: {title}

{commentaire complet}

---
```

Puis demander validation via `AskUserQuestion` :

```
question: "Ces commentaires sont prÃƒÆ’Ã‚Âªts. Lesquels voulez-vous poster ?"
header: "Poster"
multiSelect: true
options:
  - label: "Tous ({N} commentaires)"
    description: "Poster sur toutes les PRs reviewÃƒÆ’Ã‚Â©es"
  - label: "PR #{x} ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â {title_truncated}"
    description: "Poster uniquement sur cette PR"
  - label: "Aucun"
    description: "Annuler ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ne rien poster"
```

(GÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rer une option par PR + "Tous" + "Aucun")

### Posting

Pour chaque commentaire validÃƒÆ’Ã‚Â© :

```bash
gh pr comment {num} --body-file - <<'REVIEW_EOF'
{commentaire}
REVIEW_EOF
```

Confirmer chaque post : `ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Commentaire postÃƒÆ’Ã‚Â© sur PR #{num}: {title}`

Si "Aucun" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `Aucun commentaire postÃƒÆ’Ã‚Â©. Workflow terminÃƒÆ’Ã‚Â©.`

---

## Gestion des cas limites

| Situation | Comportement |
|-----------|--------------|
| 0 PRs ouvertes | `Aucune PR ouverte.` + terminer |
| PR en draft | Indiquer dans tableau, skip pour review sauf si sÃƒÆ’Ã‚Â©lectionnÃƒÆ’Ã‚Â©e explicitement |
| CI inconnu | Afficher `?` dans colonne CI |
| Review agent timeout | Afficher erreur partielle, continuer avec les autres |
| `gh pr diff` vide | Skip cette PR, notifier l'utilisateur |
| PR trÃƒÆ’Ã‚Â¨s large (>5000 additions) | Avertir : "Review partielle, diff tronquÃƒÆ’Ã‚Â©" |
| Collaborateurs API 403/404 | Fallback sur auteurs des 10 derniers PRs mergÃƒÆ’Ã‚Â©s |

---

## Notes

- Toujours dÃƒÆ’Ã‚Â©river owner/repo via `gh repo view`, jamais hardcoder
- Utiliser `gh` CLI (pas `curl` GitHub API) sauf pour la liste des collaborateurs
- `statusCheckRollup` peut ÃƒÆ’Ã‚Âªtre null ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ traiter comme `?`
- `mergeable` peut ÃƒÆ’Ã‚Âªtre `MERGEABLE`, `CONFLICTING`, ou `UNKNOWN` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ traiter `UNKNOWN` comme `?`
- Ne jamais poster sans validation explicite de l'utilisateur dans le chat
- Les commentaires draftÃƒÆ’Ã‚Â©s doivent ÃƒÆ’Ã‚Âªtre visibles AVANT tout `gh pr comment`
