"""
readme_template.py
------------------
Generiert die README.md des neuen Projekts.

Die README enthält:
  - Projektstruktur mit Erklärungen
  - Workflow-Tabellen (DSC/DAN)
  - Daten-Naming-Conventions
  - Setup-Anleitung
  - Wie man Notebooks ausführt

📝 ANPASSEN: Ändere Texte, Tabellen oder Abschnitte nach Bedarf.
"""

from datetime import datetime


def get_readme(project_name: str, project_slug: str, project_type: str) -> str:
    if project_type.upper() == "DAN":
        return _readme_dan(project_name, project_slug)
    return _readme_dsc(project_name, project_slug)


def _readme_dan(project_name: str, project_slug: str) -> str:
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    return f"""\
# {project_name}

> **Typ:** DAN &nbsp;|&nbsp; **Erstellt:** {today} &nbsp;|&nbsp; **Version:** 0.1.0

---

## Schnellstart

### 1. Repository klonen / Ordner oeffnen

```bash
# In VS Code: Datei -> Ordner oeffnen -> diesen Projektordner waehlen
```

### 2. uv installieren (einmalig, falls noch nicht vorhanden)

```bash
pip install uv
```

### 3. Virtuelle Umgebung erstellen

```bash
uv venv
```

### 4. Umgebung aktivieren

```bash
# Windows:
.venv\\Scripts\\activate

# Mac / Linux:
source .venv/bin/activate
```

### 5. Dependencies + Projektpaket installieren

```bash
uv pip install -e ".[dan]"
```

> Das `-e` steht fuer "editable" - dein `src/{project_slug}/` Paket wird direkt aus dem
> Quellcode importiert. Die eckigen Klammern `[dan]` installieren die DAN-Zusatzpakete
> aus `pyproject.toml`.

### 6. Jupyter Kernel registrieren

```bash
python -m ipykernel install --user --name {project_slug} --display-name "Python ({project_slug})"
```

### 7. Los geht\'s!

Oeffne `notebooks/00_introduction.ipynb` und fange an.

---

## Projektstruktur

```
{project_name}/
|
+-- pyproject.toml          # Paketkonfiguration & Dependencies
+-- .gitignore
+-- .python-version         # Python-Version fuer uv (3.10)
+-- README.md
|
+-- data/                   # NICHT in Git! (.gitignore)
|   +-- raw/                # Rohdaten - NIEMALS veraendern!
|   +-- interim/            # Zwischenstands (gefiltert, teilbereinigt)
|   +-- processed/          # Finale, analysefertige Daten
|
+-- notebooks/
|   +-- 00_introduction.ipynb
|   +-- 01_exploration.ipynb
|   +-- 02_preprocessing.ipynb
|   +-- 03_advanced_analytics.ipynb
|   +-- 04_business_report.ipynb
|   +-- project_decision_log.md
|
+-- src/
|   +-- {project_slug}/     # Das Python-Paket
|       +-- __init__.py
|       +-- config.py       # Zentrale Pfade & Konstanten
|       +-- settings.py     # Plot-Theme, Farben, Logging
|       +-- utils.py        # Hilfsfunktionen
|       +-- data/
|       +-- features/
|       +-- visualization/
|       +-- analytics/
|
+-- tests/
|   +-- test_data.py
|   +-- test_features.py
|
+-- reports/
    +-- figures/            # Exportierte Plots
    +-- tables/             # Exportierte Tabellen
    +-- index.html          # Executive Summary HTML
```

---

## Konfiguration

### Pfade (`src/{project_slug}/config.py`)

```python
from {project_slug}.config import PATHS

PATHS["raw"]       # data/raw/
PATHS["processed"] # data/processed/
PATHS["figures"]   # reports/figures/
```

### Plotting einrichten

```python
from {project_slug}.settings import setup_plotting, logger

setup_plotting()
logger.info("Notebook gestartet")
```

---

## Tests ausfuehren

```bash
pytest
pytest --cov=src/{project_slug} --cov-report=term-missing
```

---

_Generiert mit dem DAN/DSC Scaffolding Generator._
"""


# ─── DSC README (kept for DSC type) ───────────────────────────────────────────

def _readme_dsc(project_name: str, project_slug: str) -> str:
    """DSC README - original volle Version."""
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    return f"""\
# {project_name}

> **Typ:** DSC &nbsp;|&nbsp; **Erstellt:** {today} &nbsp;|&nbsp; **Version:** 0.1.0

---

## Schnellstart

### 1. Virtuelle Umgebung erstellen & aktivieren

```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\\Scripts\\activate  # Windows
```

### 2. Dependencies installieren

```bash
uv pip install -e ".[dsc]"
```

### 3. Kernel registrieren

```bash
python -m ipykernel install --user --name {project_slug} --display-name "Python ({project_slug})"
```

---

## Projektstruktur

```
{project_name}/
+-- pyproject.toml
+-- .gitignore
+-- .python-version
+-- README.md
+-- data/raw/  interim/  processed/
+-- notebooks/
|   +-- 00_introduction.ipynb
|   +-- 01_exploration.ipynb
|   +-- 02_preprocessing.ipynb
|   +-- 03_modeling.ipynb
|   +-- 04_evaluation.ipynb
|   +-- 05_reporting.ipynb
+-- src/{project_slug}/
|   +-- config.py  settings.py  utils.py
|   +-- data/  features/  modeling/  evaluation/  visualization/
+-- tests/
+-- configs/  default.yaml  data.yaml  model.yaml
+-- models/{today}/
+-- reports/  figures/  tables/  index.html
+-- docs/  project_decision_log.md
```

---

{_workflow_section("DSC")}

---

_Generiert mit dem DAN/DSC Scaffolding Generator._
"""


def _workflow_section(project_type: str) -> str:
    if project_type.upper() == "DSC":
        return """\
### DSC Workflow

| Schritt | 01 · Exploration | 02 · Preprocessing | 03 · Modeling | 04 · Evaluation |
|---------|------------------|--------------------|---------------|-----------------|
| | Project Introduction & Context | Data Splitting & Export | Baseline Model Definition | Test Data Evaluation |
| | Metric Definition | Data Cleaning | Model Training | Model Interpretation |
| | Data Acquisition | Data Filtering | Hyperparameter Tuning | Error Analysis |
| | Exploratory Data Analysis | Outlier Handling | Master Pipeline Definition | Feature Importance Analysis |
| | Outlier Detection (Train Data) | Data Distribution Adjustment | Validation Strategy | Residual Analysis |
| | Key Findings & Hypotheses | Feature Engineering | Prediction Generation | Business Interpretation |
| | | Feature Scaling & Normalization | Final Pipeline Export | Prediction Usability Assessment |
| | | Feature Reduction / Selection | | |

**Wichtige Regel:** Train/Test-Split immer **als erstes** in `02_preprocessing`,
bevor irgendeine Bereinigung stattfindet → verhindert Data Leakage!"""
    else:
        return """\
### DAN Workflow

| Schritt | 01 · Exploration | 02 · Preprocessing | 03 · Advanced Analytics | 04 · Business Insights |
|---------|------------------|--------------------|------------------------|------------------------|
| | Introduction & Context | Data Cleaning (Imputation & Formats) | Market Segmentation | Strategy Recommendations |
| | Metric Definition | Handling Nested / JSON Fields | Competition Analysis | Visualization of Key Findings |
| | Data Acquisition | Geographic Filtering | Pricing & Rating Correlation | Expansion Risk Assessment |
| | Exploratory Data Analysis | Outlier Handling | Cuisine / Category Gap Analysis | ROI Estimation (Hypothetical) |
| | Outlier Detection | Feature Engineering | Weighted Rating Calculation | Final Executive Summary |
| | Key Findings & Hypotheses | Data Export for Deep Dive | Cluster Analysis | Storytelling for Stakeholders |"""
