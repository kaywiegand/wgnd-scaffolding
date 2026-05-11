# wgnd Scaffolding Generator

> Erstellt in Sekunden eine vollständige, standardisierte Projektstruktur
> für Data Analytics (DAN) und Data Science (DSC) Projekte.

---

## Inhaltsverzeichnis

1. [Was macht der Generator?](#was-macht-der-generator)
2. [Voraussetzungen](#voraussetzungen)
3. [Verwendung (Schritt für Schritt in VS Code)](#verwendung-schritt-für-schritt-in-vs-code)
4. [Argumente](#argumente)
5. [Beispiele](#beispiele)
6. [Generator anpassen](#generator-anpassen)
7. [Dateistruktur des Generators](#dateistruktur-des-generators)

---

## Was macht der Generator?

Der Generator legt mit einem einzigen Befehl ein komplettes Datenprojekt an:

- **Ordnerstruktur** nach Cookiecutter Data Science Standard
- **Jupyter Notebooks** mit vorbereiteten Markdown-Headings (Workflow-Struktur)
- **Python-Quelldateien** mit Docstrings und Starter-Code (`config.py`, `settings.py`, `notebook.py`, `utils.py`)
- **YAML-Konfigurationen** (nur DSC)
- **Test-Dateien** (pytest)
- **README.md** im neuen Projekt
- **PROCESS_LOG.md**, **ROADMAP.md**, **CLAUDE.md** — Projektdokumentation und AI-Kontext
- **pyproject.toml**, **.gitignore**, **Makefile**

---

## Voraussetzungen

- Python 3.10 oder neuer
- `uv` als Paketmanager

```bash
pip install uv   # einmalig
```

---

## Verwendung (Schritt für Schritt in VS Code)

### Schritt 1: Generator-Ordner in VS Code öffnen

1. VS Code öffnen
2. **Datei → Ordner öffnen** → den Ordner `wgnd-scaffolding` auswählen

Du siehst jetzt links im Explorer:

```
wgnd-scaffolding/
├── generator.py
├── README.md
└── templates/
    ├── config_files.py
    ├── src_files.py
    ├── ...
```

### Schritt 2: Terminal öffnen

**Ansicht → Terminal** oder **Strg + `**

### Schritt 3: Generator ausführen

```bash
python generator.py --name "Mein Projekt" --path "." --type DAN
```

**Argumente:**

| Argument | Bedeutung | Beispiel |
|----------|-----------|---------|
| `--slug` | **Pflicht** — Ordnername und Paketname überall | `"dansc_zh-tram-flow"` |
| `--path` | Wo soll der Projektordner erstellt werden? | `"."` = aktueller Ordner |
| `--type` | Projekttyp | `DAN` oder `DSC` |
| `--name` | [optional] Lesbarer Name nur für Docs/README | `"Zürich Tram Flow"` |

### Schritt 4: Neues Projekt in VS Code öffnen

1. **Datei → Ordner öffnen** → den neu erstellten Projektordner wählen

### Schritt 5: Umgebung einrichten

Im Terminal des **neuen** Projekts:

```bash
uv venv                                    # .venv/ erstellen

source .venv/bin/activate                  # Mac/Linux
.venv\Scripts\activate                     # Windows

uv pip install -e ".[dan]"                 # DAN-Projekt
# oder:
uv pip install -e ".[dsc]"                 # DSC-Projekt

python -m ipykernel install --user \
    --name <slug> \
    --display-name "Python (<slug>)"
```

> Alternativ: `make setup` im Projektordner erledigt alles auf einmal.

### Schritt 6: Kernel im Notebook wählen

1. Notebook öffnen (z.B. `notebooks/01_exploration.ipynb`)
2. Oben rechts → **Select Kernel** → deinen Slug wählen

### Schritt 7: Erste Notebook-Zelle

```python
from <slug>.notebook import *
setup_plotting()
```

Danach in einer zweiten Zelle die projektspezifischen Konstanten setzen:

```python
DATA_PATH     = PATHS["raw"]
DATA_FILENAME = "meine_datei.csv"
```

---

## Argumente

```
usage: generator.py [-h] --slug SLUG [--name NAME] --path PATH --type {DSC,DAN}

Pflichtargumente:
  --slug, -s    Technischer Bezeichner — Ordnername, Paketname, überall (a-z, 0-9, _, -)
  --path, -p    Übergeordnetes Verzeichnis für das neue Projekt
  --type, -t    DSC oder DAN

Optionale Argumente:
  --name, -n    Lesbarer Projektname für Docs und README. Fällt auf --slug zurück.
  --help, -h    Diese Hilfe anzeigen
```

### Namens-Logik

Der Generator leitet drei technische Namen aus deinen Eingaben ab:

| Name | Herkunft | Beispiel | Verwendung |
| :--- | :--- | :--- | :--- |
| **Slug** | `--slug` (Pflicht) | `zh-tram-flow` | Eindeutiger Bezeichner, Git-Repo-Name |
| **Paketname** | Slug, Bindestriche → Unterstriche | `zh_tram_flow` | `src/zh_tram_flow/`, Python-Imports |
| **Ordnername** | `{type}_{slug}` | `dan_zh-tram-flow` | Projektordner auf dem Filesystem |
| **Projektname** | `--name` (optional) | `Zürich Tram Flow` | README-Titel, Docs — fällt auf Slug zurück |

**Slug-Regeln:** Kleinbuchstaben, Ziffern, Unterstriche und Bindestriche erlaubt. Darf nicht mit Ziffer beginnen. Kurz halten — nur das Thema, ohne Typ-Prefix.

**Ordner umbenennen:** Den Projektordner (`dan_zh-tram-flow`) kannst du später manuell umbenennen, z.B. in `dansc_zh-tram-flow` wenn das Projekt Analytics und Science kombiniert.

---

## Beispiele

```bash
# DAN-Projekt — Slug reicht, Ordner wird automatisch dan_zh-tram-flow
python generator.py --slug zh-tram-flow --path "." --type DAN

# DSC-Projekt mit optionalem lesbarem Namen für Docs
python generator.py --slug house-price \
                    --name "House Price Prediction" \
                    --path "../projects" \
                    --type DSC

# Ergebnis: Ordner dsc_house-price, Paket house_price, Kernel "Python (house_price)"
python generator.py --slug zomato --name "Zomato Market Analysis" \
                    --path "." --type DAN
```

---

## Was wird generiert?

### Projektdokumentation (Root-Ebene)

| File | Zweck |
| :--- | :--- |
| `PROCESS_LOG.md` | Projektverlauf und AI-Kontext-Einstieg — wird am Anfang jeder Claude-Session gelesen |
| `ROADMAP.md` | Phasen und offene Tasks — Checkliste durch das Projekt |
| `CLAUDE.md` | Projektspezifische Anweisungen für Claude Code — ergänzt die globale CLAUDE.md |
| `README.md` | Projektbeschreibung für Menschen — GitHub-Startseite |

### Ordnerstruktur (DAN)

```
<slug>/
├── PROCESS_LOG.md      ← Projektverlauf & AI-Kontext-Einstieg
├── ROADMAP.md          ← Phasen & offene Tasks
├── CLAUDE.md           ← projektspezifische Claude-Anweisungen
├── README.md           ← Projektbeschreibung
├── pyproject.toml      ← Dependencies & Paket-Konfiguration
├── Makefile            ← Shortcuts (make setup, make kernel, ...)
├── .gitignore
├── src/<slug>/
│   ├── __init__.py
│   ├── config.py       ← PATHS, PROJECT_NAME, RANDOM_SEED
│   ├── settings.py     ← setup_plotting() mit Theme, pd-Optionen, autoreload
│   ├── notebook.py     ← zentraler Import-Einstiegspunkt für alle Notebooks
│   ├── utils.py        ← timer, ensure_dir, GeoBounds, get_geo_mask
│   ├── data/
│   ├── features/
│   ├── visualization/
│   └── analytics/
├── notebooks/
│   ├── 00_introduction.ipynb
│   ├── 01_exploration.ipynb
│   ├── 02_preparation.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_insights.ipynb
├── data/
│   ├── raw/            ← Rohdaten (nicht in Git)
│   ├── interim/        ← Zwischenergebnisse (nicht in Git)
│   └── processed/      ← Finale Daten (nicht in Git)
├── reports/
│   ├── figures/        ← Exportierte Plots
│   └── index.html      ← Executive Summary Template
└── tests/
```

### `notebook.py` — was drin steckt

```python
# src/<slug>/notebook.py — wird automatisch generiert
from <slug>.notebook import *   # lädt alles auf einmal:

# Verfügbar nach dem Import:
# pd, np, plt, sns, Path
# inspect, inspect_missing, inspect_duplicates, inspect_outliers,
# inspect_outlier_detail, inspect_correlations
# success, warn, info_box, show_df
# PATHS, PROJECT_NAME, RANDOM_SEED, setup_plotting
```

### `pyproject.toml` — Dependencies

```toml
dependencies = [
  "pandas>=2.0",
  "numpy>=1.24",
  "matplotlib>=3.7",
  "seaborn>=0.12",
  "pyarrow>=14.0",
  "rich>=13.0",
  "wgnd @ git+https://github.com/kaywiegand/wgnd-toolkit.git@main",
]
```

**wgnd-Toolkit updaten** (nach Push ins wgnd-toolkit):

```bash
uv pip install -e ".[dan]" --refresh-package wgnd
# → Kernel neu starten
```

---

## Generator anpassen

Der Generator ist **modular** aufgebaut — jede Datei in `templates/` ist für einen Teil der Projektstruktur zuständig:

```
templates/
├── structure.py        ← Ordner-Liste
├── notebooks_dsc.py    ← DSC-Notebooks
├── notebooks_dan.py    ← DAN-Notebooks
├── src_files.py        ← Python-Quelldateien (config, settings, notebook, utils, ...)
├── config_files.py     ← YAML-Konfigurationen (nur DSC)
├── test_files.py       ← pytest Test-Dateien
├── root_files.py       ← pyproject.toml, .gitignore, Makefile
├── docs_files.py       ← Dokumentation
├── readme_template.py  ← README.md des neuen Projekts
└── notebook_helper.py  ← (intern) Erstellt gültiges .ipynb-JSON
```

### Neues Notebook hinzufügen

In `templates/notebooks_dan.py`:

```python
def get_notebooks(project_name, project_slug):
    return [
        ...
        ("notebooks/05_mein_notebook.ipynb", _nb_mein_notebook()),
    ]

def _nb_mein_notebook() -> str:
    cells = [
        ("markdown", "# 05 · Mein Notebook"),
        ("code", "from {slug}.notebook import *\nsetup_plotting()"),
    ]
    return make_notebook(cells)
```

### Neue Python-Datei in `src/` hinzufügen

In `templates/src_files.py`:

```python
def get_files(project_name, project_slug, project_type):
    files = [
        ...
        (f"{base_path}/meine_datei.py", _meine_datei()),
    ]
    return files

def _meine_datei() -> str:
    return '"""meine_datei.py – Beschreibung."""'
```

---

## Dateistruktur des Generators

```
wgnd-scaffolding/
├── generator.py              # CLI-Einstiegspunkt & Orchestrator
├── README.md                 # Diese Datei
└── templates/
    ├── __init__.py
    ├── notebook_helper.py    # Erstellt gültiges .ipynb-JSON
    ├── structure.py          # Alle Ordner die erstellt werden
    ├── root_files.py         # pyproject.toml, .gitignore, Makefile, PROCESS_LOG, ROADMAP, CLAUDE
    ├── notebooks_dsc.py      # DSC-Notebook-Definitionen
    ├── notebooks_dan.py      # DAN-Notebook-Definitionen
    ├── src_files.py          # Python-Quelldateien
    ├── config_files.py       # YAML-Konfigurationen
    ├── test_files.py         # pytest Test-Dateien
    ├── docs_files.py         # Docs & HTML-Report
    └── readme_template.py    # README.md des generierten Projekts
```

---

_Entwickelt für DAN- und DSC-Projekte im Wiegand-Workflow._
