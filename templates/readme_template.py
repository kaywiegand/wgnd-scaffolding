"""
readme_template.py
------------------
Generiert die README.md des neuen Projekts.

Die README enthält:
  - Projektstruktur mit Erklärungen
  - Workflow-Tabellen (DS/DA)
  - Daten-Naming-Conventions
  - Setup-Anleitung
  - Wie man Notebooks ausführt

📝 ANPASSEN: Ändere Texte, Tabellen oder Abschnitte nach Bedarf.
"""

from datetime import datetime


def get_readme(project_name: str, project_slug: str, project_type: str, package_name: str = "") -> str:
    pkg = package_name or project_slug.replace("-", "_")
    if project_type.upper() == "DA":
        return _readme_da(project_name, project_slug, pkg)
    return _readme_ds(project_name, project_slug, pkg)


def _readme_da(project_name: str, project_slug: str, package_name: str) -> str:
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    return f"""\
# {project_name}

> **Typ:** DA &nbsp;|&nbsp; **Erstellt:** {today} &nbsp;|&nbsp; **Version:** 0.1.0

---

## Schnellstart

### 1. Virtuelle Umgebung erstellen & aktivieren

```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\\Scripts\\activate      # Windows
```

### 2. Dependencies + Projektpaket installieren

```bash
uv pip install -e ".[da]"
```

### 3. Jupyter Kernel registrieren

```bash
python -m ipykernel install --user --name {package_name} --display-name "Python ({package_name})"
```

Oder einfach: `make setup && make kernel`

### 4. Los geht\'s!

Oeffne `notebooks/00_introduction.ipynb` und fange an.

---

## Projektstruktur

```
{project_slug}/
|
+-- PROCESS_LOG.md          # Projektverlauf & AI-Kontext-Einstieg
+-- ROADMAP.md              # Phasen & offene Tasks
+-- CLAUDE.md               # Claude Code Anweisungen
+-- README.md
+-- pyproject.toml          # Paketkonfiguration & Dependencies
+-- Makefile                # Shortcuts (make setup, make kernel, ...)
+-- .gitignore
|
+-- data/                   # NICHT in Git! (.gitignore)
|   +-- raw/                # Rohdaten - NIEMALS veraendern!
|   +-- interim/            # Zwischenergebnisse
|   +-- processed/          # Finale, analysefertige Daten
|
+-- notebooks/
|   +-- 00_introduction.ipynb
|   +-- 01_exploration.ipynb
|   +-- 02_preparation.ipynb
|   +-- 03_analysis.ipynb
|   +-- 04_insights.ipynb
|
+-- src/{package_name}/     # Python-Paket (importierbar nach uv install)
|   +-- config.py           # Zentrale Pfade & Konstanten
|   +-- settings.py         # Plot-Theme, Logging
|   +-- notebook.py         # Zentraler Import-Einstieg fuer Notebooks
|   +-- utils.py            # Hilfsfunktionen
|   +-- data/
|   +-- features/
|   +-- visualization/
|   +-- analytics/
|
+-- tests/
+-- public/
    +-- index.html
    +-- img/
    +-- md/
```

---

## Konfiguration

### Pfade (`src/{package_name}/config.py`)

```python
from {package_name}.config import PATHS

PATHS["raw"]       # data/raw/
PATHS["processed"] # data/processed/
PATHS["figures"]   # public/img/
```

### Notebook-Einstieg

```python
from {package_name}.notebook import *
setup_plotting()
```

---

## Tests ausfuehren

```bash
pytest
pytest --cov=src/{package_name} --cov-report=term-missing
```

---

_Generiert mit dem wgnd-scaffolding Generator._
"""


# ─── DS README (kept for DS type) ─────────────────────────────────────────────

def _readme_ds(project_name: str, project_slug: str, package_name: str) -> str:
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    return f"""\
# {project_name}

> **Typ:** DS &nbsp;|&nbsp; **Erstellt:** {today} &nbsp;|&nbsp; **Version:** 0.1.0

---

## Schnellstart

### 1. Virtuelle Umgebung erstellen & aktivieren

```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\\Scripts\\activate      # Windows
```

### 2. Dependencies installieren

```bash
uv pip install -e ".[ds]"
```

### 3. Kernel registrieren

```bash
python -m ipykernel install --user --name {package_name} --display-name "Python ({package_name})"
```

Oder einfach: `make setup && make kernel`

---

## Projektstruktur

```
{project_slug}/
+-- PROCESS_LOG.md          # Projektverlauf & AI-Kontext-Einstieg
+-- ROADMAP.md              # Phasen & offene Tasks
+-- CLAUDE.md               # Claude Code Anweisungen
+-- README.md
+-- pyproject.toml
+-- Makefile
+-- .gitignore
+-- data/raw/  interim/  processed/
+-- notebooks/
|   +-- 00_introduction.ipynb
|   +-- 01_exploration.ipynb
|   +-- 02_preparation.ipynb
|   +-- 03_analysis.ipynb
|   +-- 04_insights.ipynb
+-- src/{package_name}/
|   +-- config.py  settings.py  notebook.py  utils.py
|   +-- data/  features/  modeling/  evaluation/  visualization/
+-- tests/
+-- configs/  default.yaml  data.yaml  model.yaml
+-- models/{today}/
+-- public/  index.html  img/  md/
```

---

## Notebook-Einstieg

```python
from {package_name}.notebook import *
setup_plotting()
```

---

{_workflow_section("DS")}

---

_Generiert mit dem wgnd-scaffolding Generator._
"""


def _workflow_section(project_type: str) -> str:
    if project_type.upper() == "DS":
        return """\
### DS Workflow

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
### DA Workflow

| Schritt | 01 · Exploration | 02 · Preprocessing | 03 · Advanced Analytics | 04 · Business Insights |
|---------|------------------|--------------------|------------------------|------------------------|
| | Introduction & Context | Data Cleaning (Imputation & Formats) | Market Segmentation | Strategy Recommendations |
| | Metric Definition | Handling Nested / JSON Fields | Competition Analysis | Visualization of Key Findings |
| | Data Acquisition | Geographic Filtering | Pricing & Rating Correlation | Expansion Risk Assessment |
| | Exploratory Data Analysis | Outlier Handling | Cuisine / Category Gap Analysis | ROI Estimation (Hypothetical) |
| | Outlier Detection | Feature Engineering | Weighted Rating Calculation | Final Executive Summary |
| | Key Findings & Hypotheses | Data Export for Deep Dive | Cluster Analysis | Storytelling for Stakeholders |"""
