# DAN / DSC Scaffolding Generator

> Erstellt in Sekunden eine vollständige, standardisierte Projektstruktur
> für Data Analytics (DAN) und Data Science (DSC) Projekte.

---

## 📋 Inhaltsverzeichnis

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
- **Python-Quelldateien** mit Docstrings und Starter-Code
- **YAML-Konfigurationen** mit Kommentaren
- **Test-Dateien** (pytest) mit Beispiel-Tests
- **README.md** im neuen Projekt mit Workflow-Tabellen und Erklärtexten
- **pyproject.toml**, **.gitignore**, **environment.yml**, **requirements.txt**

---

## Voraussetzungen

- Python 3.10 oder neuer
- Keine externen Pakete nötig – der Generator verwendet nur die Python-Standardbibliothek

Prüfe deine Python-Version im Terminal:
```bash
python --version
```

---

## Verwendung (Schritt für Schritt in VS Code)

### Schritt 1: Diesen Generator-Ordner in VS Code öffnen

1. VS Code öffnen
2. **Datei → Ordner öffnen** (oder `Strg + K`, `Strg + O`)
3. Den Ordner `dan-dsc-scaffolder` auswählen → **Ordner auswählen**

Du siehst jetzt links im Explorer:
```
dan-dsc-scaffolder/
├── generator.py
├── README.md
└── templates/
    ├── config_files.py
    ├── docs_files.py
    ├── ...
```

### Schritt 2: Terminal öffnen

- **Ansicht → Terminal** oder Tastenkürzel **Strg + `** (Backtick)
- Ein Terminal-Fenster öffnet sich unten in VS Code

### Schritt 3: Generator ausführen

Tippe folgenden Befehl ein und passe die Werte an:

```bash
python generator.py --name "Mein Projekt" --path "." --type DSC
```

**Was die Argumente bedeuten:**

| Argument | Bedeutung | Beispiel |
|----------|-----------|---------|
| `--name` | Projektname (darf Leerzeichen enthalten) | `"House Price Prediction"` |
| `--path` | Wo soll der Projektordner erstellt werden? | `"."` = aktueller Ordner |
| `--type` | Projekttyp | `DSC` oder `DAN` |
| `--slug` | [optional] Technischer Name (wird auto-generiert) | `"house_price"` |

### Schritt 4: Neues Projekt in VS Code öffnen

Nach dem Generator-Lauf:

1. **Datei → Ordner öffnen**
2. Den neu erstellten Projektordner wählen
3. Das Projekt ist bereit!

### Schritt 5: Im neuen Projekt – Umgebung einrichten

Im Terminal des **neuen** Projekts:

```bash
# Option A: Conda
conda env create -f environment.yml
conda activate <dein-project-slug>

# Option B: pip
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt

# Projektpaket installieren (WICHTIG für Imports in Notebooks!)
pip install -e .

# Jupyter Kernel registrieren
python -m ipykernel install --user --name <dein-project-slug> --display-name "Python (<dein-project-slug>)"
```

> **Was ist `pip install -e .`?**
> Das installiert dein `src/<slug>/` Paket im "editable mode".
> Danach kannst du in jedem Notebook schreiben:
> `from <slug>.config import PATHS` – und Python findet das Paket.

### Schritt 6: Kernel im Notebook wählen

1. Notebook in VS Code öffnen (z.B. `notebooks/00_introduction.ipynb`)
2. Oben rechts siehst du „Select Kernel" oder einen Kernel-Namen
3. Klicke darauf → „Python Environments" → deinen Slug wählen
4. Falls nicht sichtbar: Terminal → Befehl aus Schritt 5 wiederholen

---

## Argumente

```
usage: generator.py [-h] --name NAME [--slug SLUG] --path PATH --type {DSC,DAN}

Pflichtargumente:
  --name, -n    Projektname (kann Leerzeichen und Sonderzeichen enthalten)
  --path, -p    Übergeordnetes Verzeichnis für das neue Projekt
  --type, -t    DSC oder DAN

Optionale Argumente:
  --slug, -s    Python-Bezeichner (nur a-z, 0-9, _). Automatisch aus --name abgeleitet.
  --help, -h    Diese Hilfe anzeigen
```

### Was ist der Slug?

Der Slug ist der technische Name deines Python-Pakets. Er wird verwendet:
- Als Ordnername in `src/<slug>/`
- Als Name der Conda-Umgebung
- Als Import-Name in Notebooks: `from <slug>.config import PATHS`

**Regeln:** Nur Kleinbuchstaben, Ziffern und Unterstriche. Kein Leerzeichen. Darf nicht mit einer Ziffer beginnen.

**Automatische Ableitung:** Aus `"My Cool Project 2024!"` wird automatisch `my_cool_project_2024`.

---

## Beispiele

```bash
# DSC-Projekt im aktuellen Ordner
python generator.py --name "House Price Prediction" --path "." --type DSC

# DAN-Projekt in einem bestimmten Verzeichnis
python generator.py --name "Restaurant Analysis Q3 2024" \
                    --path "C:/Users/max/Projects" \
                    --type DAN

# Mit eigenem Slug (z.B. kürzer halten)
python generator.py --name "Zomato Market Analysis" \
                    --slug "zomato" \
                    --path "../projects" \
                    --type DAN

# Windows – Pfad mit Backslashes in Anführungszeichen
python generator.py --name "Churn Prediction" \
                    --path "C:\Users\max\Dokumente\Projekte" \
                    --type DSC
```

---

## Generator anpassen

Der Generator ist **modular** aufgebaut. Jede Datei in `templates/` ist für
einen bestimmten Teil der Projektstruktur zuständig:

```
templates/
├── structure.py        ← Ordner-Liste anpassen
├── notebooks_dsc.py    ← DSC-Notebooks: Zellen, Headlines
├── notebooks_dan.py    ← DAN-Notebooks: Zellen, Headlines
├── src_files.py        ← Python-Quelldateien mit Starter-Code
├── config_files.py     ← YAML-Konfigurationen
├── test_files.py       ← pytest Test-Dateien
├── root_files.py       ← pyproject.toml, .gitignore, environment.yml
├── docs_files.py       ← Dokumentation, Executive Summary HTML
├── readme_template.py  ← README.md des neuen Projekts
└── notebook_helper.py  ← (Intern) Erstellt gültiges .ipynb-JSON
```

### Neues Notebook hinzufügen

In `templates/notebooks_dsc.py` (oder `_dan.py`):

```python
def get_notebooks(project_name, project_slug):
    return [
        ...
        ("notebooks/06_mein_neues_notebook.ipynb", _nb_mein_notebook()),  # ← hinzufügen
    ]

def _nb_mein_notebook() -> str:
    cells = [
        ("markdown", "# 06 · Mein Notebook"),
        ("markdown", "## Abschnitt 1"),
        ("code", "import pandas as pd"),
    ]
    return make_notebook(cells)
```

### Neue Python-Datei in src/ hinzufügen

In `templates/src_files.py`:

```python
def get_files(project_name, project_slug, project_type):
    files = [
        ...
        (f"{base_path}/meine_neue_datei.py", _meine_datei()),  # ← hinzufügen
    ]
    return files

def _meine_datei() -> str:
    return '''"""meine_neue_datei.py – Beschreibung."""'''
```

### Neuen Ordner hinzufügen

In `templates/structure.py` in der `get_folders()`-Funktion:

```python
folders = [
    ...
    "mein_neuer_ordner/unterordner",  # ← hinzufügen
]
```

---

## Dateistruktur des Generators

```
dan-dsc-scaffolder/
│
├── generator.py              # CLI-Einstiegspunkt & Orchestrator
├── README.md                 # Diese Datei
│
└── templates/
    ├── __init__.py           # Macht templates/ zu einem Python-Paket
    ├── notebook_helper.py    # Erstellt gültiges .ipynb-JSON
    ├── structure.py          # Alle Ordner die erstellt werden
    ├── root_files.py         # pyproject.toml, .gitignore, environment.yml
    ├── notebooks_dsc.py      # DSC-Notebook-Definitionen
    ├── notebooks_dan.py      # DAN-Notebook-Definitionen
    ├── src_files.py          # Python-Quelldateien (config, utils, data, ...)
    ├── config_files.py       # YAML-Konfigurationen
    ├── test_files.py         # pytest Test-Dateien
    ├── docs_files.py         # Docs & HTML-Report
    └── readme_template.py    # README.md des generierten Projekts
```

---

_Entwickelt für DAN- und DSC-Projekte nach dem Cookiecutter Data Science Standard._
