"""
root_files.py
-------------
Dateien im Projektstamm:
  - pyproject.toml    → Paket-Konfiguration & Dependencies (wird von uv gelesen)
  - .gitignore        → Was Git ignorieren soll
  - .python-version   → Pinnt die Python-Version für uv

Paket-Management: uv + venv
  uv liest pyproject.toml direkt – keine requirements.txt oder environment.yml nötig.

📝 ANPASSEN: Füge Pakete unter [project] dependencies oder [project.optional-dependencies]
              in pyproject.toml hinzu. Danach: uv pip install -e ".[dsc]" erneut ausführen.
"""


def get_files(project_name: str, project_slug: str, project_type: str, package_name: str = "") -> list[tuple[str, str]]:
    pkg = package_name or project_slug.replace("-", "_")
    return [
        ("pyproject.toml",    _pyproject_toml(project_name, pkg, project_type)),
        (".gitignore",        _gitignore()),
        (".python-version",   "3.10\n"),
        ("Makefile",          _makefile(pkg, project_type)),
        ("PROCESS_LOG.md",    _process_log(project_name)),
        ("ROADMAP.md",        _roadmap(project_name)),
        ("CLAUDE.md",         _claude_md(project_name, project_slug, project_type)),
    ]


def _pyproject_toml(project_name: str, project_slug: str, project_type: str) -> str:
    return f"""\
# pyproject.toml
# --------------
# Zentrale Projektkonfiguration: Metadaten, Dependencies, Build-System, Tool-Settings.
# uv liest diese Datei direkt – keine requirements.txt oder environment.yml nötig.
#
# Setup (einmalig, nach dem Klonen / Erstellen):
#   uv venv                          → erstellt .venv/
#   .venv\\Scripts\\activate           → Umgebung aktivieren (Windows)
#   source .venv/bin/activate        → Umgebung aktivieren (Mac/Linux)
#   uv pip install -e ".[{project_type.lower()}]"  → installiert alle Dependencies + dieses Paket
#
# Neue Pakete hinzufügen:
#   Eintrag in dependencies[] unten ergänzen, dann:
#   uv pip install -e ".[{project_type.lower()}]"  → erneut ausführen

[build-system]
requires      = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name        = "{project_slug}"
version     = "0.1.0"
description = "{project_name} – {project_type} Project"
requires-python = ">=3.10"

dependencies = [
  "pandas>=2.0",
  "numpy>=1.24",
  "matplotlib>=3.7",
  "seaborn>=0.12",
  "scikit-learn>=1.3",
  "jupyter>=1.0",
  "ipykernel>=6.0",
  "pyyaml>=6.0",
  "joblib>=1.3",
  "python-dotenv>=1.0",
  "rich>=13.0",
  "pyarrow>=14.0",
  "wgnd @ git+https://github.com/kaywiegand/wgnd-toolkit.git@main",
]

[project.optional-dependencies]
dsc = [
  "xgboost>=2.0",
  "shap>=0.43",
  "optuna>=3.0",
]
dan = [
  "plotly>=5.0",
  "folium>=0.15",
]
dev = [
  "pytest>=7.0",
  "pytest-cov>=4.0",
  "black>=23.0",
  "ruff>=0.1",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.black]
line-length    = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
select      = ["E", "F", "I"]
"""


def _gitignore() -> str:
    return """\
# .gitignore – Python / Data Science (uv + venv)
# ------------------------------------------------
# WICHTIG: Daten und Modelle NICHT in Git einchecken!
# uv.lock wird NICHT ignoriert – Lockfile gehört in Git!

# ── Daten ──────────────────────────────────────────────────────────────────
data/raw/
data/interim/
data/processed/
*.csv
*.xlsx
*.parquet
*.feather
*.h5
*.hdf5

# ── Modelle & Artefakte ────────────────────────────────────────────────────
models/
*.pkl
*.joblib
*.pt
*.pth

# ── Python ─────────────────────────────────────────────────────────────────
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg
*.egg-info/
dist/
build/
.eggs/
*.so

# ── Virtuelle Umgebung (uv erstellt .venv/) ────────────────────────────────
.venv/
.env
*.env

# ── Jupyter ────────────────────────────────────────────────────────────────
.ipynb_checkpoints/
*.ipynb_metadata

# ── IDE & OS ───────────────────────────────────────────────────────────────
.vscode/settings.json
.idea/
.DS_Store
Thumbs.db
*.swp
*.swo

# ── Public (optional – kommentiere aus, wenn du Public-Artefakte tracken willst) ───
# public/img/
# public/md/
"""


def _makefile(package_name: str, project_type: str) -> str:
    extras = project_type.lower()
    return f"""\
# Makefile – {package_name}
# -------------------------
# Shortcuts für Entwicklung & Setup.
# Verwendung: make <target>
#
# Voraussetzung: uv installiert (pip install uv)

.PHONY: setup install kernel test lint clean help

setup: ## Virtuelle Umgebung erstellen + Dependencies installieren
\tuv venv
\t. .venv/bin/activate && uv pip install -e ".[{extras},dev]"
\t@echo ""
\t@echo "✅ Setup fertig. Umgebung aktivieren mit:"
\t@echo "   source .venv/bin/activate"

install: ## Dependencies (neu) installieren
\t. .venv/bin/activate && uv pip install -e ".[{extras},dev]"

kernel: ## Jupyter Kernel registrieren
\t. .venv/bin/activate && python -m ipykernel install --user --name {package_name} --display-name "Python ({package_name})"
\t@echo "✅ Kernel '{package_name}' registriert."

test: ## Tests ausführen
\t. .venv/bin/activate && pytest tests/ -v

lint: ## Code prüfen (ruff + black)
\t. .venv/bin/activate && ruff check src/ && black --check src/

format: ## Code formatieren (black)
\t. .venv/bin/activate && black src/

clean: ## Umgebung + Cache aufräumen
\trm -rf .venv __pycache__ src/*.egg-info .pytest_cache
\tfind . -type d -name __pycache__ -exec rm -rf {{}} + 2>/dev/null || true
\t@echo "✅ Aufgeräumt."

help: ## Alle verfügbaren Targets anzeigen
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {{FS = ":.*?## "}}; {{printf "  \\033[36m%-12s\\033[0m %s\\n", $$1, $$2}}'
"""


def _process_log(project_name: str) -> str:
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    return f"""\
# PROCESS_LOG.md – {project_name}

> Projektverlauf und AI-Kontext-Einstieg.
> Dieses File ist der Einstiegspunkt für neue Claude-Sessions.

---

## Projekt-Übersicht

| Feld | Inhalt |
| :--- | :--- |
| Projektname | {project_name} |
| Erstellt | {today} |
| Status | 🔜 Setup |
| Nächster Schritt | EDA starten |

---

## Verlauf

### {today} – Projekt aufgesetzt

- Projektstruktur mit wgnd-scaffolding generiert.
- Nächste Schritte: Daten laden, erste EDA.

---
"""


def _roadmap(project_name: str) -> str:
    return f"""\
# ROADMAP.md – {project_name}

## Phase 1 – Setup & Daten
- [ ] Projektstruktur aufsetzen
- [ ] Datenquellen identifizieren
- [ ] Rohdaten laden und prüfen

## Phase 2 – EDA
- [ ] Explorative Datenanalyse
- [ ] Erste Visualisierungen
- [ ] Hypothesen formulieren

## Phase 3 – Modell / Analyse
- [ ] Feature Engineering
- [ ] Modell / Analyse umsetzen
- [ ] Ergebnisse bewerten

## Phase 4 – Abschluss
- [ ] Report / Dashboard
- [ ] README finalisieren
- [ ] Repo aufräumen und archivieren
"""


def _claude_md(project_name: str, project_slug: str, project_type: str) -> str:
    return f"""\
# CLAUDE.md – {project_name}

> Projektspezifische Anweisungen für Claude Code.
> Ergänzt die globale CLAUDE.md aus dem wgnd-workspace.

---

## Projekt

| Feld | Inhalt |
| :--- | :--- |
| Slug | `{project_slug}` |
| Typ | {project_type} |
| Stack | Polars · Plotly · Jupyter |

## Kontext-Einstieg

1. `PROCESS_LOG.md` lesen — aktueller Projektstand
2. `ROADMAP.md` lesen — offene Phasen und Tasks
3. Globale `CLAUDE.md` aus `/Users/kaywiegand/Workspace/` gilt weiterhin

## Projektspezifische Hinweise

_Hier projektspezifische Overrides ergänzen, z.B. besondere Datenquellen,
Naming-Konventionen oder Abhängigkeiten zu anderen Repos._
"""


def _environment_yml_UNUSED(project_slug: str, project_type: str) -> str:  # kept for reference
    extras = ""
    if project_type.upper() == "DSC":
        extras = """\
  - xgboost>=2.0
  - shap>=0.43
  - optuna>=3.0
"""
    else:
        extras = """\
  - plotly>=5.0
  - folium>=0.15
"""
    return f"""\
# environment.yml
# ---------------
# Conda-Umgebungsdefinition.
#
# Neue Umgebung erstellen:
#   conda env create -f environment.yml
#
# Bestehende Umgebung aktualisieren (nach Änderungen hier):
#   conda env update -f environment.yml --prune
#
# Umgebung aktivieren:
#   conda activate {project_slug}

name: {project_slug}

channels:
  - conda-forge
  - defaults

dependencies:
  - python=3.10
  - pip

  # Daten & Analyse
  - pandas>=2.0
  - numpy>=1.24
  - scikit-learn>=1.3
  - joblib>=1.3

  # Visualisierung
  - matplotlib>=3.7
  - seaborn>=0.12

  # Notebooks
  - jupyter>=1.0
  - ipykernel>=6.0

  # Konfiguration
  - pyyaml>=6.0
  - python-dotenv>=1.0

  # Typ-spezifische Pakete
{extras}
  # Dev-Tools
  - pytest>=7.0
  - black>=23.0
  - ruff>=0.1

  # pip-Pakete (nicht in conda verfügbar)
  - pip:
    - pytest-cov>=4.0
"""


def _requirements_txt_UNUSED(project_type: str) -> str:  # kept for reference
    extras = ""
    if project_type.upper() == "DSC":
        extras = """\
# DSC-spezifisch
xgboost>=2.0
shap>=0.43
optuna>=3.0
"""
    else:
        extras = """\
# DAN-spezifisch
plotly>=5.0
folium>=0.15
"""
    return f"""\
# requirements.txt
# ----------------
# pip-Installation aller Projekt-Abhängigkeiten.
#
# Installieren mit:
#   pip install -r requirements.txt
#
# Tipp: Installiere danach das Projektpaket selbst:
#   pip install -e .

# Kern
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
joblib>=1.3

# Visualisierung
matplotlib>=3.7
seaborn>=0.12

# Notebooks
jupyter>=1.0
ipykernel>=6.0

# Konfiguration
pyyaml>=6.0
python-dotenv>=1.0

{extras}
# Dev-Tools
pytest>=7.0
pytest-cov>=4.0
black>=23.0
ruff>=0.1
"""
