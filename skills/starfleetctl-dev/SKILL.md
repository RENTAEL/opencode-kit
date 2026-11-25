---
name: starfleetctl-dev
description: "Handwerkliche Grundregeln stehen in `AGENTS.md` im Repo. Dieser Skill ist die **Ablauf-Korrektur** dazu ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â was in welcher Reihenfolge passieren muss, damit eine ÃƒÆ’Ã¢â‚¬Å¾nderung wirklich bei der Flotte ankommt."
---
# starfleetctl-dev ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â working on the starfleetctl source

Handwerkliche Grundregeln stehen in `AGENTS.md` im Repo. Dieser Skill ist die
**Ablauf-Korrektur** dazu ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â was in welcher Reihenfolge passieren muss, damit eine
ÃƒÆ’Ã¢â‚¬Å¾nderung wirklich bei der Flotte ankommt.

Die **konkreten Pfade/Orte dieser Workspace** (mpbt-Dev-Clone, Worktrees, Bootstrap,
Ports) und die **Testbed-Kurzanleitung** stehen im Skill
**`starfleetctl-dev-workspace`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â lade beide zusammen, wenn du in dieser Workspace
am starfleetctl-Source arbeitest. Dieser Skill hier ist der generische Teil.

## Zwei Kopien ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â wer entwickelt, wer deployed

`starfleet-bootstrap` clont/aktualisiert das Repo nach `.starfleet-ai/src/starfleetctl`.
Das ist der **Deployment-Clone** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â der `go:embed`-Input des Binaries. **Dort wird nie
entwickelt**; jeder Handgriff dort wird beim nÃƒÆ’Ã‚Â¤chsten `git merge --ff-only`
ÃƒÆ’Ã‚Â¼berschrieben.

Entwickelt wird in einem **eigenen Clone** des Repos (in dieser Workspace: siehe
`starfleetctl-dev-workspace`), auf einem **eigenen Branch** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nicht direkt auf `master`.

| | Dev-Clone | Deployment-Clone |
|---|---|---|
| Zweck | Entwicklung, Branches, Tests | Produktiv-Deployment |
| Angefasst von | dir | nur `git pull` durch den Bootstrap |

### Welche Datei ist die Originalquelle? ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â die Verwechslung, die wirklich passiert

**FÃƒÆ’Ã‚Â¼r Skills und Plugins ist die Originalquelle IMMER `fragments/` im Repo.** Die
Kopien unter `.claude/skills/` und `.opencode/plugins/` sind **generierte Artefakte**.

| Artefakt | Originalquelle | generierte Kopie |
|---|---|---|
| Skill `starfleet*` | `fragments/starfleet-skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **nicht editieren** |
| opencode-Plugin | `fragments/opencode-plugins/<name>.ts` | `.opencode/plugins/<name>.ts` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **nicht editieren** |

**Was beim Editieren der generierten Kopie passiert:** `fixStarfleetSkills()`
(`internal/bootstrap/checks.go`) vergleicht byte-genau gegen den eingebetteten Stand
und **schreibt beim nÃƒÆ’Ã‚Â¤chsten `./starfleet-bootstrap` die Fragment-Fassung zurÃƒÆ’Ã‚Â¼ck** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
kein Fehler, kein Abbruch, der Edit ist einfach weg.

Vor dem Editieren eines `starfleet*`-Skills also prÃƒÆ’Ã‚Â¼fen:

```sh
ls <dev-clone>/fragments/starfleet-skills/
# taucht der Name dort auf, ist das Fragment die Quelle ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â dort editieren.
```

### Kopplungskette ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â warum ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Kopie manuell aktualisieren" nichts bringt

```
dev-clone  commit + PUSH ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬â€œÃ‚Âº origin/master
                                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ git fetch + merge --ff-only
                                   ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
                     .starfleet-ai/src/starfleetctl/    (go:embed-INPUT)
                                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ go build (bettet Fragmente/Skills ein)
                                   ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
                     .starfleet-ai/bin/starfleetctl
                                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ self-install
                                   ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
                     .claude/skills/*, .opencode/plugins/*   (was Agenten laden)
```

Daraus folgt zwingend:

- Wer `.starfleet-ai/src/` von Hand ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾hochzieht", erreicht **nichts** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â erst der
  **Neu-Bau** bettet den neuen Stand ein.
- Wer eine Plugin-Datei nur manuell nach `.opencode/plugins/` kopiert, erreicht
  **nichts** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â der nÃƒÆ’Ã‚Â¤chste `self-install` ÃƒÆ’Ã‚Â¼berschreibt sie aus dem Build.
- Solange der Commit nicht auf `origin/master` ist, gibt es **nichts zum Ziehen**.

**Letzte Stufe ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â eine LAUFENDE Session liest Skills nicht neu.** opencode scannt die
Skills **einmal pro Prozess** (im Log `init count=N` bei jedem Prozessstart) und hÃƒÆ’Ã‚Â¤lt
sie im Speicher; auch ein erneuter `skill`-Tool-Aufruf liefert den Stand vom
Prozessstart. Ein geÃƒÆ’Ã‚Â¤nderter Skill wirkt daher erst in einem **neuen opencode-Prozess**
ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â d.h. Ship-Neustart (`session stop` + `ship-run`). Zwei Fallstricke:

- `sop-reload` (in-place `session.clear` + re-prompt) lÃƒÆ’Ã‚Â¤uft im **selben** Prozess und
  lÃƒÆ’Ã‚Â¤dt nur den SOP-Index neu ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **nicht** die Skills.
- Auch wenn beim Neustart **dieselbe Session wieder aufgenommen** wird (`--session
  <id>`), ist der Skill-Registry trotzdem neu: der **Prozess** ist neu, die
  Konversations-Historie bleibt. Skills sind also aktuell, sobald der Prozess neu ist.

## 0. Claim, bevor du anfasst

Es darf **immer nur ein Schiff gleichzeitig** den starfleetctl-Source ÃƒÆ’Ã‚Â¤ndern. Vorher
per comms ankÃƒÆ’Ã‚Â¼ndigen, welchen Bereich du anfasst (`internal/web`, `internal/filestore`,
ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦). Ein Task-Status `done` ist **kein** Claim.

## 1. Bauen ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `make all` ist Pflicht, nicht optional

```sh
cd <dev-clone>
make all          # baut Binary + check-plugin, Tests mÃƒÆ’Ã‚Â¼ssen grÃƒÆ’Ã‚Â¼n sein
```

`make all` lÃƒÆ’Ã‚Â¤uft durch Compile **und** Link ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â siehe ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Pitfall: Build meldet grÃƒÆ’Ã‚Â¼n, Link
ist kaputt".

## 2. Deployen ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `./starfleet-bootstrap`

Am Workspace-Root, **nicht** im Source:

```sh
./starfleet-bootstrap
```

Der Bootstrap pullt `origin/master` in den Deployment-Clone, baut das Binary neu,
deployt es nach `.starfleet-ai/bin/starfleetctl` und installiert Fragmente/Skills/
Plugins; am Ende `sop reindex`.

**Ist das Binary nicht ÃƒÆ’Ã‚Â¼berschreibbar** (`text file busy`), den laufenden Server
**nicht** killen. Stattdessen das alte Binary lÃƒÆ’Ã‚Â¶schen und neu deployen:

```sh
rm -f .starfleet-ai/src/starfleetctl/starfleetctl   # rm umgeht text-file-busy
./starfleet-bootstrap
```

## 3. Daemons neu starten ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â in dieser Reihenfolge

Nach jedem Binary-Wechsel laufen die Daemons **mit dem alten Binary**, bis man sie
explizit neu startet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â der hÃƒÆ’Ã‚Â¤ufigste Grund fÃƒÆ’Ã‚Â¼r ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ich habe doch deployed":

```sh
./.starfleet-ai/bin/starfleetctl web restart           # HTTP-UI
./.starfleet-ai/bin/starfleetctl timer worker restart
./.starfleet-ai/bin/starfleetctl model-proxy restart    # nur bei Go-ÃƒÆ’Ã¢â‚¬Å¾nderungen
```

Reihenfolge: **erst `bootstrap`, dann die Daemons.** `web restart` beendet die
laufende Web-OberflÃƒÆ’Ã‚Â¤che (Arbeitswerkzeug des Praetors/der Web-Console-Schiffe) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
HÃƒÆ’Ã‚Â¤ufungen vermeiden, einen Restart pro auslieferbarem Zustand, nicht pro Commit. FÃƒÆ’Ã‚Â¼r
reine **Plugin**-ÃƒÆ’Ã¢â‚¬Å¾nderungen genÃƒÆ’Ã‚Â¼gt ein `PLUGIN_VERSION`-Bump; fÃƒÆ’Ã‚Â¼r reine Go-ÃƒÆ’Ã¢â‚¬Å¾nderungen
reicht `make all` + `model-proxy restart`.

## 4. Verifizieren ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nie ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾fertig" melden ohne Messung

Vier Checks, **live gegen das laufende System**:

```sh
# 1. Ist das neue Binary wirklich das deployte?
stat -c '%y %n' .starfleet-ai/bin/starfleetctl
stat -c '%y %n' <dev-clone>/starfleetctl
#    Binary-Zeitstempel muss >= Quell-Zeitstempel sein.

# 2. LÃƒÆ’Ã‚Â¤uft der Daemon mit dem neuen Binary?
go version -m /proc/<pid>/exe | grep vcs.revision   # exakter Commit des laufenden Prozesses
ps -eo pid,etimes,cmd | grep 'starfleetctl web start' | grep -v grep

# 3. Funktioniert die ÃƒÆ’Ã¢â‚¬Å¾nderung am laufenden System?
curl -s -D- -o /dev/null http://127.0.0.1:8080/ | head -20
#    Bei einem Frontend-Fix: die ausgelieferte Datei prÃƒÆ’Ã‚Â¼fen, nicht nur den Source.

# 4. Ist alles committed und gepusht?
cd <dev-clone>
git status --short          # muss leer sein
git rev-parse HEAD origin/master   # muss identisch sein
```

Erst wenn **alle vier** passen, darf ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾fertig" gemeldet werden ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â sonst Task
`in-progress`.

### Bei Fragment-/Plugin-ÃƒÆ’Ã¢â‚¬Å¾nderungen zusÃƒÆ’Ã‚Â¤tzlich: Inhalt vergleichen, nicht Version lesen

Ein Versions-String ist **kein Nachweis**. Der eigentliche Beweis ist der
Byte-Vergleich Source vs. ausgeliefert:

```sh
diff -q <dev-clone>/fragments/opencode-plugins/starfleet-dispatch.ts \
        .opencode/plugins/starfleet-dispatch.ts   # "identisch" = deployed
```

Und die **Wirksamkeit**, nicht nur die Ankunft: hat die neue Logik eine beobachtbare
Wirkung? Sonst ist ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾deployed" nur eine Behauptung ÃƒÆ’Ã‚Â¼ber Bytes.

`index.html` oder Fragmente werden nur durch `./starfleet-bootstrap` ausgeliefert ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
ein reines `make all` ÃƒÆ’Ã‚Â¤ndert die ausgelieferte SPA **nicht**.

## Pitfall: Build meldet grÃƒÆ’Ã‚Â¼n, Link ist kaputt

Ein entferntes `size_t ConnectionInfoSize = 0;` kompiliert in allen
ÃƒÆ’Ã…â€œbersetzungseinheiten, erst der **Link** bricht ab (`undefined reference`). Ein reiner
Compile-Lauf meldet ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾erfolgreich". Und: der Build eine Sekunde **vor** dem letzten
Speichern deployt den vorherigen Stand. Deshalb Schritt 1 und 4 der Verifikation.

Merksatz: **`ninja` kompiliert, `ninja install` linkt und installiert. Beides zÃƒÆ’Ã‚Â¤hlt.**

## Pitfall: uncommittete Arbeit gilt als nicht existent

Nach jeder ÃƒÆ’Ã¢â‚¬Å¾nderung `git status --short`. **Und: committet ist nicht gepusht.** FÃƒÆ’Ã‚Â¼r
Fragmente/Skills/Plugins ist der *gepushte* Stand auf `origin/master` die
Voraussetzung ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â der Bootstrap sieht nur, was auf `origin` liegt. Eine committete,
aber nicht gepushte ÃƒÆ’Ã¢â‚¬Å¾nderung liefert dieselbe Fehlermeldung wie gar keine.

## Pitfall: Temp-Dateien im Source

`.bak`, `before.txt`, `after.txt` o.ÃƒÆ’Ã‚Â¤. gehÃƒÆ’Ã‚Â¶ren **nicht** in den Source (sondern unter
`_WORK_/<projekt>/tmp/`). Vor dem Commit `git status --short` prÃƒÆ’Ã‚Â¼fen.

## Pitfall: Frontend ohne Cache-Header

Die Web-SPA wird ohne `Cache-Control`/`ETag`/`Last-Modified` ausgeliefert ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nach einem
Deploy kann der Browser alten JS-Code zeigen. Beim Debuggen von ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾geht nicht" zuerst
einen **Hard-Reload** anfordern, und immer prÃƒÆ’Ã‚Â¼fen, ob der Fehler im **Backend** oder im
**ausgelieferten Frontend** liegt (die ausgelieferte Datei holen und darin suchen).

## 5. Modell-Proxy niemals direkt killen ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â immer `model-proxy restart`

Der **model-proxy** ist ein eigener Daemon, den starfleetctl verwaltet.

```sh
./.starfleet-ai/bin/starfleetctl model-proxy restart|stop|start
```

**Niemals** `kill`/`pkill`/`systemctl stop` gegen den Proxy ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â das hinterlÃƒÆ’Ã‚Â¤sst
inkonsistente ZustÃƒÆ’Ã‚Â¤nde (verbliebene Sockets, hÃƒÆ’Ã‚Â¤ngende Verbindungen). Der offizielle
`restart` gibt Ressourcen sauber frei und lÃƒÆ’Ã‚Â¤dt die aktuelle Config
(`.starfleet-ai/conf/model-proxy.yaml`) neu. Ein reines `model-proxy restart` reicht
**nur** fÃƒÆ’Ã‚Â¼r Config-ÃƒÆ’Ã¢â‚¬Å¾nderungen (yaml); bei Go-ÃƒÆ’Ã¢â‚¬Å¾nderungen erst `make all` + `bootstrap`.

Verifikation nach restart: `model-proxy status`; die Ausgabe muss fÃƒÆ’Ã‚Â¼r alle Provider
`ok` zeigen.

## 6. Branch + Testbed, bevor etwas auf `master`/live geht

**Jede ÃƒÆ’Ã¢â‚¬Å¾nderung zuerst auf einem eigenen Branch, im isolierten Testbed durchtesten ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
erst danach auf `master` und live deployen.**

1. **Eigener Branch/Worktree** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nicht auf `master` arbeiten.
2. **Bauen** (`make all`) und eine **isolierte Instanz** hochziehen (eigene Workspace,
   eigene Ports, eigene IdentitÃƒÆ’Ã‚Â¤t) und die ÃƒÆ’Ã¢â‚¬Å¾nderung **end-to-end** durchspielen ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
   inklusive des Fehlerfalls, den sie behebt.
3. **Erst danach**: Merge auf `master`, dann `./starfleet-bootstrap` + Daemon-Restart.

Ein Testbed-Harness existiert in dieser Workspace; die konkreten Befehle stehen im
Skill **`starfleetctl-dev-workspace`** (Abschnitt ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Isoliertes Testbed").

Warum so streng: der Fix lÃƒÆ’Ã‚Â¤uft live durch den model-proxy; ein Proxy-/Daemon-Bug kann
die **ganze Flotte** lahmlegen. Isoliert testen kostet Minuten, ein Live-Ausfall kostet
die Flotte.

## 7. NIEMALS `pkill -f starfleetctl` (Incident 2026-10-13)

FÃƒÆ’Ã‚Â¼r ein manuelles Deployment **niemals** einen breiten `pkill`-Befehl verwenden ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
weder `pkill -f starfleetctl` noch `kill`/`systemctl`
gegen die laufende Instanz. **Vor dem Kopieren das alte Binary lÃƒÆ’Ã‚Â¶schen** (`rm -f`),
das umgeht das text-file-busy und ist die einzige zulÃƒÆ’Ã‚Â¤ssige Methode:

```sh
rm -f .starfleet-ai/bin/starfleetctl
cp <dev-clone>/starfleetctl .starfleet-ai/bin/starfleetctl
```

**Warum das so gefÃƒÆ’Ã‚Â¤hrlich ist ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â gemessen am 2026-10-13:** `pkill -9 -f "starfleetctl"`
matcht die **volle** Kommandozeile. Damit trifft es nicht nur die eigene Instanz,
sondern **jeden** laufenden Wrapper `starfleetctl run --client opencode ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` **aller
Schiffe** gleichzeitig, den `timer worker` und den `web`-Daemon. Der `run`-Wrapper ist
der **Vordergrund-Prozessgruppen-FÃƒÆ’Ã‚Â¼hrer auf dem pts**; wird er gekillt, ÃƒÆ’Ã‚Â¼berlebt
`opencode --session ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` (kein ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾starfleetctl" in der Kommandozeile) **verwaist** und hÃƒÆ’Ã‚Â¤lt
fd 0/1/2 weiter auf dem pts. Der Kernel gibt die Vordergrund-Kontrolle an die shell
zurÃƒÆ’Ã‚Â¼ck ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ das Terminal ist ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾total kaputt". Blast radius ist **flottenweit**, nicht lokal.

Merksatz: **Der Prozess, den man treffen will, und der Prozess, den man trifft, sind
bei `pkill -f` nie garantiert derselbe.** `rm -f` + `cp` hat diesen Nebeneffekt nicht.

## Melden

Report mit `starfleetctl reports submit ... --task-ref <slug>`, Body mit **Messwerten**
statt Behauptungen. Antwort auf comms an den Absender **und** an McKinley (die
web-console), wenn die Web-OberflÃƒÆ’Ã‚Â¤che betroffen ist.
