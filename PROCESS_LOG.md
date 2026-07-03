# PROCESS_LOG.md – wgnd-scaffolding

> Projektverlauf und AI-Kontext-Einstieg.
> Dieses File ist der Einstiegspunkt für neue Claude-Sessions.

---

## Projekt-Übersicht

| Feld | Inhalt |
| :--- | :--- |
| Projektname | wgnd-scaffolding |
| Zweck | Projektstruktur-Generator für DA/DS/DE Projekte |
| Status | 🟢 stabil, einsatzbereit |
| Nächster Schritt | Projekttyp-Codes auf DA/DS/DE vereinheitlicht (Backlog #7/#8 obsolet — DS = voller Zyklus) |

---

## Verlauf

### 2026-07-03 — README: Notebooks-Tabelle + Report-Link aus Single Source, Tree-Drift behoben

**Kontext:** `/project-review` auf `zh-tram-data` (Toolchain-Testlauf) fand zwei Lücken im Generator:
(1) die README verwies nie auf `public/index.html` als öffentlichen Einstieg, (2) die Notebook-Liste
war im README-Template hartkodiert und dem Notebook-Generator hinterhergedriftet — der DS-Struktur-Tree
zeigte noch alte Namen (`02_preparation/03_analysis/04_insights` statt `02_preprocessing/03_modeling/…`).

**Änderungen:**

| Datei | Änderung |
|:---|:---|
| `notebooks_da.py` · `notebooks_ds.py` | Neue `_specs()` als **Single Source of Truth** (Reihenfolge · Dateiname · Zweck · Builder). `get_notebooks()` + neues `get_notebook_index()` leiten beide daraus ab. |
| `generator.py` | `get_notebook_index()` importiert, Index vor `get_readme()` berechnet + durchgereicht. |
| `readme_template.py` | Struktur-Tree, verlinkte **Notebooks-Tabelle** und `## Report`-Section (Link auf `public/index.html`) werden aus dem Index generiert — keine hartkodierten Notebook-Listen mehr. |

**Warum Single Source:** zwei Listen für dieselbe Sache driften garantiert (war bereits passiert) —
verstößt gegen das CONVENTIONS-Prinzip „gleicher Fakt nie in zwei Files", hier im Generator-Code selbst.

**Verifiziert:** voller Generatorlauf DA (5 NBs) + DS (6 NBs), README rendert Tree + Tabelle + Report
korrekt, DS-Tree jetzt drift-frei.

**Offen (ins Workspace-`docs/BACKLOG.md`):** #11 — CLI `choices` akzeptiert kein `DE` (`generator.py:145`),
DE-Projekte fallen bei der Arg-Validierung durch, obwohl sie die DA-Struktur erben.

**Nächster Schritt:** Backlog #2/#5/#3 (Slug-Fixes / MD-Generierung) + neu #11 (DE-CLI-Choice).

---

### 2026-07-01 — Web-Root reports/ → public/, mds/ → md/

**Kontext:** `reports/` als Web-Root ist veraltet — Kay nutzt in neuen Projekten
`public/` als Konvention für öffentliche Artefakte. Zusätzlich Drift korrigiert:
Unterordner hieß im Generator `mds/` (Plural), in der Praxis wird `md/` (Singular)
verwendet.

**8 Template-Files + README aktualisiert:**

| Datei | Änderung |
|:---|:---|
| `structure.py` | `reports/img` → `public/img` · `reports/mds` → `public/md` (DA, DS, `ALWAYS_EMPTY_DIRS`) |
| `src_files.py` | `PATHS["reports"]` → `PATHS["public"]` (`_SRC / "public"`), `PATHS["figures"]` → `_SRC / "public" / "img"` |
| `docs_files.py` | `reports/index.html` → `public/index.html`, Platzhalter-Texte auf `public/` |
| `root_files.py` | `.gitignore`-Kommentar → `public/img/` + `public/md/` |
| `notebooks_da.py` | `FIGURES = Path('../public/img')` |
| `notebooks_ds.py` | Kommentar `reports/img/` → `public/img/` |
| `readme_template.py` | Struktur-Diagramme (DA + DS) + PATHS-Beispiel → `public/`, `md/` |
| `README.md` (Generator-Root) | Struktur-Diagramm korrigiert: `reports/figures/` → `public/img/` + `public/md/` |

Bestehende Projekte (z.B. `zh-tram-flow`) werden NICHT migriert — nur der
Generator für neue Projekte betroffen. `docs/portfolio/`-Framework-Docs im
Workspace-Repo wurden parallel angepasst.

**Nächster Schritt:** Backlog-Issues #2/#5/#3 (Slug-Fixes + MD-File-Generierung) — weiterhin offen.

---

### 2026-05-29 — reports/-Struktur als Web-Projekt standardisiert

**Kontext:** Aus der Arbeit an `zh-tram-flow` entstanden — `reports/` wurde dort von
`figures/` + `tables/` auf `img/` + `mds/` + `index.html` umgestellt (Web-Projekt-Ansatz).
Änderung wurde direkt in alle relevanten Templates übertragen.

**7 Template-Files aktualisiert:**

| Datei | Änderung |
|:---|:---|
| `structure.py` | `reports/figures` → `reports/img` · `reports/tables` → `reports/mds` (3 Stellen) |
| `src_files.py` | `PATHS["figures"]` Template → `reports/img` |
| `notebooks_da.py` | `FIGURES = Path('../reports/img')` |
| `notebooks_ds.py` | Kommentar `reports/figures/` → `reports/img/` |
| `docs_files.py` | Placeholder-Verweis `reports/figures/` → `reports/img/` |
| `root_files.py` | `.gitignore`-Kommentar → `img/` + `mds/` |
| `readme_template.py` | Struktur-Diagramm + PATHS-Beispiel (3 Stellen) |

**Commit:** `2286a69` — `refactor(templates): reports/ als Web-Projekt — figures→img, tables→mds`

**Nächster Schritt:** Backlog-Issues #2/#5/#3 (Slug-Fixes + MD-File-Generierung) — aus vorheriger Session noch offen.

---

### 2026-05-11 – Grundlegende Überarbeitung (Session mit Kay)

**Naming Convention neu definiert:**
- `--slug` ist jetzt Pflichtfeld (war: optional, wurde aus `--name` abgeleitet)
- `--name` ist optional — nur für Docs/README, fällt auf Slug zurück
- `package_name` = Slug mit Bindestrichen → Unterstrichen (z.B. `zh_tram_flow`) — für `src/`-Ordner und Python-Imports
- Projektordner = Slug direkt (kein Typ-Prefix mehr — `dan_`, `dsc_` entfernt)

**Bugs gefixt:**
- Slug-Validierung ließ keine Bindestriche zu → jetzt erlaubt
- Ordnername wurde aus `--name` statt `--slug` abgeleitet → auf Slug umgestellt
- `src/<slug>/` hatte Bindestriche → nicht importierbar, jetzt `src/<package_name>/`
- Python-Imports in generierter README verwendeten Slug statt package_name → gefixt

**Neue Features:**
- `PROCESS_LOG.md`, `ROADMAP.md`, `CLAUDE.md` werden automatisch im neuen Projekt erstellt
- `project_decision_log.md` entfernt — wird durch `PROCESS_LOG.md` ersetzt

**Repo-Naming Convention dokumentiert:**
- `wgnd-` für eigene Tools
- `sf_` für StackFuel-Kontext
- Kein Typ-Prefix für Portfolio-Projekte — Topic ist der Name
- Hyphens sind Standard (GitHub-Konvention)

---
