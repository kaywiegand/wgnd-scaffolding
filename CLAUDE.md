# CLAUDE.md — wgnd-scaffolding

> **Globale Arbeitsanweisungen:** `../CLAUDE.md`
> **Globaler Backlog:** `../BACKLOG.md`
> **Projektübersicht:** `../PROJECTS.md`

**Beim Start dieser Session mitgeben:**
```
/Users/kaywiegand/Workspace/CLAUDE.md
/Users/kaywiegand/Workspace/BACKLOG.md
/Users/kaywiegand/Workspace/PROJECTS.md
```
Oder direkt clonen: `git@github.com:kaywiegand/wgnd-workspace.git`

Lies diese drei Files beim Start immer zuerst.

> **Hinweis Git & Privatsphäre:**
> Diese `CLAUDE.md` enthält nur technische Projekt-Infos — sie kann bedenkenlos
> eingecheckt werden. Persönliche Präferenzen, Arbeitsstil und projektübergreifender
> Kontext gehören ausschließlich in `../CLAUDE.md` (Workspace-Ebene, nicht im Repo).

---

## Projekt-Kontext

`wgnd-scaffolding` ist ein Python-CLI-Tool das in Sekunden eine vollständige,
standardisierte Projektstruktur für Data-Projekte erstellt.

**Einstiegspunkt:** `generator.py` — CLI-Orchestrator
**Paketmanager:** `uv`
**Projekttypen:** `DA` (Data Analysis) · `DS` (Data Science)

### Aktueller Aufruf

```bash
python generator.py --name "NY Taxi Routes" --path "." --type DA
#                   ^^^^^ Pflicht           ^^^^^ Pflicht  ^^^^^ Pflicht
#                   --slug optional, wird automatisch aus name abgeleitet
```

### Slug-Ableitung (aktuell)

Aus `"NY Taxi Routes 2024!"` → `ny_taxi_routes_2024`
**Regel:** nur Kleinbuchstaben, Ziffern, Unterstriche — Bindestriche nicht erlaubt → das ist Bug #2.

---

## Dateistruktur

```
wgnd-scaffolding/
├── generator.py              ← CLI-Einstiegspunkt & Orchestrator
├── README.md
└── templates/
    ├── __init__.py
    ├── notebook_helper.py    ← Erstellt gültiges .ipynb-JSON
    ├── structure.py          ← Ordner-Liste
    ├── root_files.py         ← pyproject.toml, .gitignore, Makefile
    ├── notebooks_da.py       ← DA-Notebook-Definitionen
    ├── notebooks_ds.py       ← DS-Notebook-Definitionen
    ├── src_files.py          ← Python-Quelldateien
    ├── config_files.py       ← YAML-Konfigurationen (nur DS)
    ├── test_files.py         ← pytest Test-Dateien
    ├── docs_files.py         ← Docs & HTML-Report
    └── readme_template.py    ← README.md des generierten Projekts
```

---

## Offene Issues (aus ../BACKLOG.md)

Kurzreferenz — Wahrheit und Details immer im `../BACKLOG.md`:

| # | Issue | Prio | Datei |
| :--- | :--- | :--- | :--- |
| 2 | Bindestriche im Slug erlauben (`zh-tram-flow`) | H | `generator.py` |
| 5 | Slug = Pflichtfeld + Ordnername · Name = optional | H | `generator.py` |
| 3 | MD-Files beim Setup erstellen: `ROADMAP.md`, `PROCESS_LOG.md`, `CLAUDE.md` | H | `templates/root_files.py` oder neues `templates/docs_files.py` |
| 4 | `projekt_decision.md` aus Template entfernen | M | `templates/` durchsuchen |
| 1 | ~~Neue Projekttyp-Variante: DE + DA + DS Mischform~~ → ✅ obsolet: DS = voller Zyklus (siehe `../docs/CONVENTIONS.md`) | — | erledigt 2026-07-03 |

**Reihenfolge heute:** #2 → #5 → #3 → #4 · Issue #1 ist für spätere Session.

---

## Ziel-Verhalten nach den Fixes

```bash
# Neuer Aufruf:
python generator.py --slug zh-tram-flow --type DA --name "Zürich Tram Flow"
#                   ^^^^^ Pflicht             ^^^^^ Pflicht  ^^^^^ Optional

# Ergebnis:
zh-tram-flow/           ← Ordner nach Slug benannt (nicht nach Name)
├── CLAUDE.md                 ← neu: automatisch mit Verweis auf ../CLAUDE.md
├── PROCESS_LOG.md            ← neu: Template mit Grundstruktur
├── ROADMAP.md                ← neu: Template mit Grundstruktur
├── README.md                 ← wie bisher
├── notebooks/
├── src/zh-tram-flow/   ← slug auch hier
└── ...
```

---

## Arbeitsweise

- Vor jeder Änderung: betroffene Datei in `templates/` vollständig lesen
- Erst Plan zeigen, dann auf Bestätigung warten
- Keine Templates löschen ohne Rückfrage — immer erst sichern
- Nach erledigten Issues: `../BACKLOG.md` sofort aktualisieren
