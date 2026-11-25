---
name: issue-triage
description: "**DÃƒÆ’Ã‚Â©clencheurs** :"
---
# Issue Triage

## Quand utiliser

| Skill | Usage | Output |
|-------|-------|--------|
| `/issue-triage` | Trier, analyser, commenter les issues | Tableaux d'action + deep analysis + commentaires postÃƒÆ’Ã‚Â©s |
| `/repo-recap` | RÃƒÆ’Ã‚Â©cap gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©ral pour partager avec l'ÃƒÆ’Ã‚Â©quipe | RÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© Markdown (PRs + issues + releases) |

**DÃƒÆ’Ã‚Â©clencheurs** :
- Manuellement : `/issue-triage` ou `/issue-triage all` ou `/issue-triage 42 57`
- Proactivement : quand >10 issues ouvertes sans triage, ou issue stale >30j dÃƒÆ’Ã‚Â©tectÃƒÆ’Ã‚Â©e

---

## Langue

- VÃƒÆ’Ã‚Â©rifier l'argument passÃƒÆ’Ã‚Â© au skill
- Si `en` ou `english` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ tableaux et rÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© en anglais
- Si `fr`, `french`, ou pas d'argument ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ franÃƒÆ’Ã‚Â§ais (dÃƒÆ’Ã‚Â©faut)
- Note : les commentaires GitHub (Phase 3) restent TOUJOURS en anglais (audience internationale)

---

Workflow en 3 phases : audit automatique ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ deep analysis opt-in ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commentaires avec validation obligatoire.

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

# Issues ouvertes avec mÃƒÆ’Ã‚Â©tadonnÃƒÆ’Ã‚Â©es complÃƒÆ’Ã‚Â¨tes
gh issue list --state open --limit 100 \
  --json number,title,author,createdAt,updatedAt,labels,assignees,body,comments

# PRs ouvertes (pour cross-rÃƒÆ’Ã‚Â©fÃƒÆ’Ã‚Â©rence)
gh pr list --state open --limit 50 --json number,title,body

# Issues fermÃƒÆ’Ã‚Â©es rÃƒÆ’Ã‚Â©cemment (pour dÃƒÆ’Ã‚Â©tection doublons)
gh issue list --state closed --limit 20 \
  --json number,title,labels,closedAt

# Collaborateurs (pour protÃƒÆ’Ã‚Â©ger les issues des mainteneurs)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Fallback collaborateurs** : si `gh api .../collaborators` ÃƒÆ’Ã‚Â©choue (403/404) :
```bash
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
Si toujours ambigu, demander ÃƒÆ’Ã‚Â  l'utilisateur via `AskUserQuestion`.

**Note** : `author` est un objet `{login: "..."}` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â toujours extraire `.author.login`.

### Analyse ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 6 dimensions

**1. CatÃƒÆ’Ã‚Â©gorisation** (labels existants > infÃƒÆ’Ã‚Â©rence titre/body) :
- **Bug** : mots-clÃƒÆ’Ã‚Â©s `crash`, `error`, `fail`, `broken`, `regression`, `wrong`, `unexpected`
- **Feature** : `add`, `implement`, `support`, `new`, `feat:`
- **Enhancement** : `improve`, `optimize`, `better`, `enhance`, `refactor`
- **Question/Support** : `how`, `why`, `help`, `unclear`, `docs`, `documentation`
- **Duplicate Candidate** : voir dimension 3 ci-dessous

**2. Cross-ref PRs** :
- Scanner `body` de chaque PR ouverte pour `fixes #N`, `closes #N`, `resolves #N` (case-insensitive, regex)
- Construire un map : `issue_number -> [PR numbers]`
- Une issue liÃƒÆ’Ã‚Â©e ÃƒÆ’Ã‚Â  une PR mergÃƒÆ’Ã‚Â©e ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ recommander fermeture

**3. DÃƒÆ’Ã‚Â©tection doublons** :
- Normaliser les titres : lowercase, strip prÃƒÆ’Ã‚Â©fixes (`bug:`, `feat:`, `[bug]`, `[feature]`, etc.)
- **Jaccard sur mots des titres** : si score > 60% entre deux issues ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ candidat doublon
- **Keywords body overlap** > 50% ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ renforcement du signal
- Comparer aussi avec issues fermÃƒÆ’Ã‚Â©es rÃƒÆ’Ã‚Â©centes (20 derniÃƒÆ’Ã‚Â¨res)
- Un faux positif peut ÃƒÆ’Ã‚Âªtre confirmÃƒÆ’Ã‚Â©/ÃƒÆ’Ã‚Â©cartÃƒÆ’Ã‚Â© en Phase 2

**4. Classification risque** :
- **Rouge** : mots-clÃƒÆ’Ã‚Â©s `CVE`, `vulnerability`, `injection`, `auth bypass`, `security`, `exploit`, `unsafe`, `credentials`, `leak`, `RCE`, `XSS`
- **Jaune** : `breaking change`, `migration`, `deprecation`, `remove API`, `breaking`, `incompatible`
- **Vert** : tout le reste

**5. Staleness** :
- >30j sans activitÃƒÆ’Ã‚Â© (updatedAt) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **Stale**
- >90j sans activitÃƒÆ’Ã‚Â© ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **Very Stale**
- Calculer depuis la date actuelle

**6. Recommandations d'action** :
- `Accept & Prioritize` : issue claire, reproducible, dans scope
- `Label needed` : issue sans label
- `Comment needed` : info manquante, body insuffisant
- `Linked to PR` : une PR ouverte rÃƒÆ’Ã‚Â©fÃƒÆ’Ã‚Â©rence cette issue
- `Duplicate candidate` : candidat doublon identifiÃƒÆ’Ã‚Â© (prÃƒÆ’Ã‚Â©ciser avec `#N`)
- `Close candidate` : stale + aucune activitÃƒÆ’Ã‚Â© rÃƒÆ’Ã‚Â©cente, ou hors scope (jamais si auteur est collaborateur)
- `PR merged ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ close` : PR liÃƒÆ’Ã‚Â©e est mergÃƒÆ’Ã‚Â©e, issue encore ouverte

### Output ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 5 tableaux

```
## Issues ouvertes ({count})

### Critiques (risque rouge)
| # | Titre | Auteur | ÃƒÆ’Ã¢â‚¬Å¡ge | Labels | Action |
| - | ----- | ------ | --- | ------ | ------ |

### LiÃƒÆ’Ã‚Â©es ÃƒÆ’Ã‚Â  une PR
| # | Titre | Auteur | PR(s) liÃƒÆ’Ã‚Â©e(s) | Status PR | Action |
| - | ----- | ------ | ------------- | --------- | ------ |

### Actives
| # | Titre | Auteur | CatÃƒÆ’Ã‚Â©gorie | ÃƒÆ’Ã¢â‚¬Å¡ge | Labels | Action |
| - | ----- | ------ | --------- | --- | ------ | ------ |

### Doublons candidats
| # | Titre | Doublon de | SimilaritÃƒÆ’Ã‚Â© | Action |
| - | ----- | ---------- | ---------- | ------ |

### Stale
| # | Titre | Auteur | DerniÃƒÆ’Ã‚Â¨re activitÃƒÆ’Ã‚Â© | Action |
| - | ----- | ------ | ----------------- | ------ |

### RÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â©
- Total : {N} issues ouvertes
- Critiques : {N} (risque sÃƒÆ’Ã‚Â©curitÃƒÆ’Ã‚Â© ou breaking)
- LiÃƒÆ’Ã‚Â©es ÃƒÆ’Ã‚Â  PR : {N}
- Doublons candidats : {N}
- Stale (>30j) : {N} | Very Stale (>90j) : {N}
- Sans labels : {N}
- Quick wins (ÃƒÆ’Ã‚Â  fermer ou labeler rapidement) : {liste}
```

0 issues ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ afficher `Aucune issue ouverte.` et terminer.

**Note** : `ÃƒÆ’Ã¢â‚¬Å¡ge` = jours depuis `createdAt`, format `{N}j`. Si >30j, afficher en **gras**.

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

## Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Deep Analysis (opt-in)

### SÃƒÆ’Ã‚Â©lection des issues

**Si argument passÃƒÆ’Ã‚Â©** :
- `"all"` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ toutes les issues ouvertes
- NumÃƒÆ’Ã‚Â©ros (`"42 57"`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ uniquement ces issues
- Pas d'argument ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ proposer via `AskUserQuestion`

**Si pas d'argument**, afficher :

```
question: "Quelles issues voulez-vous analyser en profondeur ?"
header: "Deep Analysis"
multiSelect: true
options:
  - label: "Toutes ({N} issues)"
    description: "Analyse approfondie de toutes les issues avec agents en parallÃƒÆ’Ã‚Â¨le"
  - label: "Critiques uniquement"
    description: "Focus sur les {M} issues ÃƒÆ’Ã‚Â  risque rouge/jaune"
  - label: "Doublons candidats"
    description: "Confirmer ou ÃƒÆ’Ã‚Â©carter les {K} doublons dÃƒÆ’Ã‚Â©tectÃƒÆ’Ã‚Â©s"
  - label: "Stale uniquement"
    description: "DÃƒÆ’Ã‚Â©cision close/keep sur les {J} issues stale"
  - label: "Passer"
    description: "Terminer ici ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â juste l'audit"
```

Si "Passer" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fin du workflow.

### ExÃƒÆ’Ã‚Â©cution de l'analyse

Pour chaque issue sÃƒÆ’Ã‚Â©lectionnÃƒÆ’Ã‚Â©e, lancer un agent via **Task tool en parallÃƒÆ’Ã‚Â¨le** :

```
subagent_type: general-purpose
model: sonnet
prompt: |
  Analyze GitHub issue #{num}: "{title}" by @{author}

  **Metadata**: Created {createdAt}, last updated {updatedAt}, labels: {labels}

  **Body**:
  {body}

  **Existing comments** ({comments_count} total, showing last 5):
  {last_5_comments}

  **Context**:
  - Linked PRs: {linked_prs or "none"}
  - Duplicate candidate of: {duplicate_of or "none"}
  - Risk classification: {risk_color}

  Analyze this issue and return a structured report:
  ### Scope Assessment
  What is this issue actually asking for? Is it clearly defined?

  ### Missing Information
  What's needed to act on this? (reproduction steps, version, environment, etc.)

  ### Risk & Impact
  Security risk? Breaking change? Who's affected?

  ### Effort Estimate
  XS (<1h) / S (1-4h) / M (1-2d) / L (3-5d) / XL (>1 week)

  ### Priority
  P0 (critical, act now) / P1 (high, this sprint) / P2 (medium, backlog) / P3 (low, someday)

  ### Recommended Action
  One of: Accept & Prioritize, Request More Info, Mark Duplicate (#N), Close (Stale), Close (Out of Scope), Link to Existing PR

  ### Draft Comment
  Draft a GitHub comment in English using the appropriate template from templates/issue-comment.md.
  Be specific, helpful, and constructive.
```

Si issue a >50 commentaires, rÃƒÆ’Ã‚Â©sumer les 5 derniers uniquement.

AgrÃƒÆ’Ã‚Â©ger tous les rapports. Afficher un rÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© aprÃƒÆ’Ã‚Â¨s toutes les analyses.

---

## Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Actions (validation obligatoire)

### Types d'actions possibles

- **Commenter** : `gh issue comment {num} --body-file -`
- **Labeler** : `gh issue edit {num} --add-label "{label}"` (skip si label dÃƒÆ’Ã‚Â©jÃƒÆ’Ã‚Â  prÃƒÆ’Ã‚Â©sent)
- **Fermer** : `gh issue close {num} --reason "not planned"` (jamais sans validation)

### GÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©ration des drafts

Pour chaque issue analysÃƒÆ’Ã‚Â©e, gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rer les actions (commentaire + labels + fermeture si applicable) en utilisant `templates/issue-comment.md`.

**RÃƒÆ’Ã‚Â¨gles** :
- Langue des commentaires : **anglais** (audience internationale)
- Ton : professionnel, constructif, factuel
- Ne jamais re-labeler une issue qui a dÃƒÆ’Ã‚Â©jÃƒÆ’Ã‚Â  ce label
- Ne jamais proposer "close" pour une issue d'un collaborateur
- Toujours afficher le draft AVANT tout `gh issue comment`

### Affichage et validation

**Afficher TOUS les drafts** au format :

```
---
### Draft ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Issue #{num}: {title}

**Actions proposÃƒÆ’Ã‚Â©es** : {Commentaire | Label: "bug" | Fermeture}

**Commentaire** :
{commentaire complet}

---
```

Puis demander validation via `AskUserQuestion` :

```
question: "Ces actions sont prÃƒÆ’Ã‚Âªtes. Lesquelles voulez-vous exÃƒÆ’Ã‚Â©cuter ?"
header: "ExÃƒÆ’Ã‚Â©cuter"
multiSelect: true
options:
  - label: "Toutes ({N} actions)"
    description: "Commenter + labeler + fermer selon les drafts"
  - label: "Issue #{x} ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â {title_truncated}"
    description: "ExÃƒÆ’Ã‚Â©cuter uniquement les actions pour cette issue"
  - label: "Aucune"
    description: "Annuler ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ne rien faire"
```

(GÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rer une option par issue + "Toutes" + "Aucune")

### ExÃƒÆ’Ã‚Â©cution

Pour chaque action validÃƒÆ’Ã‚Â©e, exÃƒÆ’Ã‚Â©cuter dans l'ordre : commenter ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ labeler ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fermer.

```bash
# Commenter
gh issue comment {num} --body-file - <<'COMMENT_EOF'
{commentaire}
COMMENT_EOF

# Labeler (si applicable)
gh issue edit {num} --add-label "{label}"

# Fermer (si applicable)
gh issue close {num} --reason "not planned"
```

Confirmer chaque action : `Commentaire postÃƒÆ’Ã‚Â© sur issue #{num}: {title}`

Si "Aucune" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `Aucune action exÃƒÆ’Ã‚Â©cutÃƒÆ’Ã‚Â©e. Workflow terminÃƒÆ’Ã‚Â©.`

---

## Gestion des cas limites

| Situation | Comportement |
|-----------|--------------|
| 0 issues ouvertes | `Aucune issue ouverte.` + terminer |
| Issue sans body | CatÃƒÆ’Ã‚Â©goriser par titre, recommander `Comment needed` |
| >50 commentaires | RÃƒÆ’Ã‚Â©sumer les 5 derniers uniquement |
| Faux positif doublon | Phase 2 confirme/ÃƒÆ’Ã‚Â©carte ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ne pas agir sur suspicion seule |
| Labels dÃƒÆ’Ã‚Â©jÃƒÆ’Ã‚Â  prÃƒÆ’Ã‚Â©sents | Ne pas re-labeler, signaler "label dÃƒÆ’Ã‚Â©jÃƒÆ’Ã‚Â  appliquÃƒÆ’Ã‚Â©" |
| Issue d'un collaborateur | Jamais `close candidate` automatique |
| Rate limit GitHub API | RÃƒÆ’Ã‚Â©duire `--limit`, notifier l'utilisateur |
| PR mergÃƒÆ’Ã‚Â©e liÃƒÆ’Ã‚Â©e ÃƒÆ’Ã‚Â  issue ouverte | Recommander fermeture de l'issue |
| Issue sans activitÃƒÆ’Ã‚Â© >90j | Very Stale ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â proposer fermeture avec message bienveillant |
| Duplicate confirmed in Phase 2 | Poster commentaire + fermer en faveur de l'issue originale |

---

## Notes

- Toujours dÃƒÆ’Ã‚Â©river owner/repo via `gh repo view`, jamais hardcoder
- Utiliser `gh` CLI (pas `curl` GitHub API) sauf pour la liste des collaborateurs
- `updatedAt` peut ÃƒÆ’Ã‚Âªtre null sur certaines issues ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ traiter comme `createdAt`
- Ne jamais poster ou fermer sans validation explicite de l'utilisateur dans le chat
- Les commentaires draftÃƒÆ’Ã‚Â©s doivent ÃƒÆ’Ã‚Âªtre visibles AVANT tout `gh issue comment`
- SimilaritÃƒÆ’Ã‚Â© Jaccard = |intersection mots| / |union mots| (exclure stop words : a, the, is, in, of, for, to, with, on, at, by)
