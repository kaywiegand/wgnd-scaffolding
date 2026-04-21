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
| `--name` | Projektname (darf Leerzeichen enthalten) | `"NY Taxi Routes"` |
| `--path` | Wo soll der Projektordner erstellt werden? | `"."` = aktueller Ordner |
| `--type` | Projekttyp | `DAN` oder `DSC` |
| `--slug` | [optional] Technischer Name (wird auto-generiert) | `"ny_taxi_routes"` |

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
usage: generator.py [-h] --name NAME [--slug SLUG] --path PATH --type {DSC,DAN}

Pflichtargumente:
  --name, -n    Projektname (kann Leerzeichen enthalten)
  --path, -p    Übergeordnetes Verzeichnis für das neue Projekt
  --type, -t    DSC oder DAN

Optionale Argumente:
  --slug, -s    Python-Bezeichner (nur a-z, 0-9, _). Automatisch aus --name abgeleitet.
  --help, -h    Diese Hilfe anzeigen
```

### Was ist der Slug?

Der Slug ist der technische Name des Python-Pakets:
- Ordnername in `src/<slug>/`
- Import-Name in Notebooks: `from <slug>.notebook import *`

**Regeln:** Nur Kleinbuchstaben, Ziffern und Unterstriche. Kein Leerzeichen. Darf nicht mit Ziffer beginnen.

**Automatische Ableitung:** Aus `"NY Taxi Routes 2024!"` wird `ny_taxi_routes_2024`.

---

## Beispiele

```bash
# DAN-Projekt im aktuellen Ordner
python generator.py --name "NY Taxi Routes" --path "." --type DAN

# DSC-Projekt in einem bestimmten Verzeichnis
python generator.py --name "House Price Prediction" \
                    --path "../projects" \
                    --type DSC

# Mit eigenem Slug (kürzer halten)
python generator.py --name "Zomato Market Analysis" \
                    --slug "zomato" \
                    --path "." \
                    --type DAN
```

---

## Was wird generiert?

### Ordnerstruktur (DAN)

```
<slug>/
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
│   ├── raw/
│   ├── interim/
│   └── processed/
├── reports/figures/
├── models/
├── tests/
├── pyproject.toml
├── Makefile
└── .gitignore
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
    ├── root_files.py         # pyproject.toml, .gitignore, Makefile
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
