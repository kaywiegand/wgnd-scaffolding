"""
notebooks_da.py
---------------
Notebook-Definitionen fuer den Typ: DA (Data Analysis)

Notebooks:
  00_introduction.ipynb      - Project Facts, Context, Workflow, Conventions
  01_exploration.ipynb       - EDA + Discovery
  02_preparation.ipynb       - Preparation + Preprocessing, Export
  03_analysis.ipynb          - Import, Analysis + Analytics
  04_insights.ipynb          - Business Communication + Insights

ANPASSEN: Aendere Zellen-Inhalte in den jeweiligen _nb_*()-Funktionen.
"""

from .notebook_helper import make_notebook


def _specs(project_name: str) -> list[tuple[str, str, object]]:
    """
    Single Source of Truth: Reihenfolge · Dateiname (ohne .ipynb) · Zweck · Zell-Builder.
    get_notebooks() und get_notebook_index() leiten beide hieraus ab — keine Drift.
    """
    return [
        ("00_introduction", "Projekt-Facts, Kontext, Workflow, Conventions", lambda: _nb_introduction(project_name)),
        ("01_exploration",  "EDA + Discovery",                               _nb_exploration),
        ("02_preparation",  "Preparation + Preprocessing, Export",           _nb_preparation),
        ("03_analysis",     "Import, Analysis + Analytics",                  _nb_analysis),
        ("04_insights",     "Business Communication + Insights",             _nb_insights),
    ]


def get_notebooks(project_name: str, project_slug: str) -> list[tuple[str, str]]:
    """Gibt alle DA-Notebooks als (pfad, inhalt)-Liste zurück."""
    return [(f"notebooks/{name}.ipynb", build()) for name, _purpose, build in _specs(project_name)]


def get_notebook_index(project_name: str = "") -> list[tuple[str, str]]:
    """
    Leichtgewichtige Liste (dateiname, zweck) für README-Tree + Notebooks-Tabelle.
    Baut keine Notebook-Inhalte (Builder werden nicht aufgerufen).
    """
    return [(name, purpose) for name, purpose, _build in _specs(project_name)]


def _nb_introduction(project_name: str) -> str:
    cells = [
        ("markdown", f"# {project_name}"),
        ("markdown",
         "## Project Facts\n\n"
         "| Feld | Wert |\n"
         "|------|------|\n"
         "| **Business-Frage** | _TODO_ |\n"
         "| **Stakeholder** | _TODO_ |\n"
         "| **Methode** | _TODO_ |\n"
         "| **Hauptdatenquelle** | _TODO_ |\n"
         "| **Ziel-Metrik** | _TODO_ |\n"
         "| **Out of Scope** | _TODO_ |"),
        ("markdown",
         "## Project Context\n\n"
         "### Scenario\n\n_Lorem ipsum dolor sit amet._\n\n"
         "### Mission\n\n_Lorem ipsum dolor sit amet._\n\n"
         "### Scope / Hypotheses\n\n* _Lorem ipsum_\n* _Lorem ipsum_"),
        ("markdown",
         "### Methode & Metrics\n\n"
         "| Metrik | Zielwert | Begruendung |\n"
         "|--------|----------|-------------|\n"
         "| _z.B. Marktanteil_ | _> 15 %_ | _..._ |"),
        ("markdown",
         "### Data Dictionary\n\n"
         "| Spaltennummer | Spaltenname | Datenniveau | Beschreibung |\n"
         "| :--- | :--- | :--- | :--- |\n"
         "| 1 | `\'Lorem\'` | kategorisch (nominal) | Lorem ipsum (`0`= lorem, `1`= ipsum) |\n"
         "| 2 | `\'Ipsum\'` | kontinuierlich (`datetime`) | Lorem ipsum |\n"
         "| 3 | `\'Dolor\'` | kontinuierlich (`int`) | Lorem ipsum |"),
        ("markdown",
         "## Workflow\n\n"
         "### Phases\n\n"
         "| Phase | 01 Exploration & Discovery | 02 Preparation & Preprocessing | 03 Analysis & Analytics | 04 Communication & Insights |\n"
         "|-------|-------------------|---------------------|------------------|------------------|\n"
         "| | Data Acquisition  | Data Cleaning       | Statistical Analysis | Insight Delivery |\n"
         "| | Initial Profiling | Outlier Handling    | Pattern Recognition  | Data Storytelling |\n"
         "| | Quality Audit     | Transformation      | Hypothesis Testing   | Strategic Advice |\n"
         "| | Key Findings      | Feature Engineering | Result Aggregation   | Executive Summary|"),
        ("markdown",
         "### Conventions\n\n"
         "| Variable | Phase | Zustand |\n"
         "|----------|-------|---------|\n"
         "| `df_raw` | Loading | Originalzustand – schreibgeschützt |\n"
         "| `df_eda` | Exploration | Initiale Daten zur explorativen Analyse |\n"
         "| `df_edit` | Preparation & Processing | Bereinigt, transformiert & aggregiert (Arbeitsbasis) |\n"
         "| `df_final` | Analysis & Reporting | Finaler Output für Insights und Visualisierungen |\n\n"
         "> **Best Practice:** Nutze für jeden Transformationsschritt `.copy()`, "
         "um die Traceability zu gewährleisten und `df_raw` niemals zu überschreiben."),
    ]
    return make_notebook(cells)




def _nb_exploration() -> str:
    cells = [
        ("markdown", "# Exploratory Data Analysis (EDA) & Discovery"),
        ("markdown", "## Data Acquisition\n\n### Preparation\n\n#### Imports"),
        ("code",
         "import pandas as pd\n"
         "import numpy as np\n"
         "import matplotlib.pyplot as plt\n"
         "import seaborn as sns\n"
         "from pathlib import Path\n\n"
         "from wgnd.core.theme import setup\n"
         "from wgnd.inspect import (\n"
         "    inspect,\n"
         "    inspect_missing,\n"
         "    inspect_outliers,\n"
         "    inspect_outlier_detail,\n"
         "    inspect_correlations,\n"
         ")\n\n"
         "setup()"),
        ("markdown", "#### Settings"),
        ("code", "%load_ext autoreload\n%autoreload 2"),
        ("markdown", "#### Constants"),
        ("code", "DATA_RAW = Path(\'../data/raw\')"),
        ("markdown", "### Data Gathering"),
        ("code",
         "df_raw = pd.read_csv(DATA_RAW / \'your_file.csv\')\n"
         "df_raw.head()"),
        ("markdown", "## Analysis\n\n### Basic Statistical Analysis\n\n> _Vollständige EDA-Übersicht mit wgnd.inspect._"),
        ("code", "df_eda = df_raw.copy()\ninspect(df_eda)   # alle Sektionen auf einmal\n\n# Einzelne Sektionen:\n# inspect(df_eda, sections=['dimensions', 'dtypes', 'missing'])"),
        ("markdown", "### Data Completeness\n\n* Quality Check\n* Duplicates\n* Missing Values"),
        ("code", "inspect_missing(df_eda)"),
        ("markdown", "### Data Integrity\n\n* Invalid Data Detection\n* Plausibility Check"),
        ("code", "# Platzhalter: Wertebereichs-Checks"),
        ("markdown", "### Data Distribution\n\n* Numerical Features\n* Categorical Features\n* Bivariate Analysis"),
        ("code", "# Platzhalter: Histogramme, Value Counts, Scatter Plots"),
        ("markdown", "### Data Relationships\n\n* Correlations"),
        ("code", "inspect_correlations(df_eda)\n# inspect_correlations(df_eda, target='your_target_col', show_pairplot=True)"),
        ("markdown", "### Outlier Detection"),
        ("code", "inspect_outliers(df_eda)\n# inspect_outlier_detail(df_eda, 'your_col')"),
        ("markdown", "### Features Inspection\n\n* Engineering"),
        ("code", "# Platzhalter: erste Feature-Ideen"),
        ("markdown",
         "## Key Findings\n\n"
         "| # | Finding | Implikation |\n"
         "|---|---------|-------------|\n"
         "| 1 | _..._ | _..._ |\n"
         "| 2 | _..._ | _..._ |"),
    ]
    return make_notebook(cells)


def _nb_preparation() -> str:
    cells = [
        ("markdown", "# Preparation & Preprocessing"),
        ("markdown", "## Data Import"),
        ("code",
         "import pandas as pd\n"
         "import numpy as np\n"
         "from pathlib import Path\n\n"
         "DATA_RAW       = Path(\'../data/raw\')\n"
         "DATA_PROCESSED = Path(\'../data/processed\')\n\n"
         "df_raw = pd.read_csv(DATA_RAW / \'your_file.csv\')\n"
         "df_eda = df_raw.copy()"),
        ("markdown", "## Train Test Split\n\n> Nur fuer DA-Projekte mit Modell-Anteil relevant."),
        ("code",
         "# from sklearn.model_selection import train_test_split\n"
         "# X_train, X_test = train_test_split(df_eda, test_size=0.2, random_state=42)"),
        ("markdown", "## Data Cleaning"),
        ("code",
         "df_impute = df_eda.copy()\n"
         "# Platzhalter: fillna, astype, drop_duplicates"),
        ("markdown", "## Outlier Handling"),
        ("code",
         "df_clean = df_impute.copy()\n"
         "# Platzhalter: IQR-Masken, Extremwerte kappen"),
        ("markdown", "## Feature Engineering"),
        ("code", "# Platzhalter: neue Spalten, Aggregationen, Encoding"),
        ("markdown", "## Data Export"),
        ("code",
         "DATA_PROCESSED.mkdir(parents=True, exist_ok=True)\n"
         "df_clean.to_csv(DATA_PROCESSED / \'cleaned.csv\', index=False)\n"
         "print(f\'Exportiert: {df_clean.shape}\')"),
    ]
    return make_notebook(cells)


def _nb_analysis() -> str:
    cells = [
        ("markdown", "# Analysis & Analytics"),
        ("markdown", "## Business Case\n\n> _Welche Fragen sollen hier beantwortet werden?_"),
        ("code",
         "import pandas as pd\n"
         "import numpy as np\n"
         "import matplotlib.pyplot as plt\n"
         "import seaborn as sns\n"
         "from pathlib import Path\n\n"
         "DATA_PROCESSED = Path(\'../data/processed\')\n"
         "df_clean = pd.read_csv(DATA_PROCESSED / \'cleaned.csv\')"),
        ("markdown", "## Market Segmentation\n\n> _Kundengruppen, Regionen, Kategorien segmentieren._"),
        ("code", "# Platzhalter: Clustering, Pivot-Tabellen"),
        ("markdown", "## Competition Analysis"),
        ("code", "# Platzhalter: Vergleichsplots, Rankings"),
        ("markdown", "## Pricing & Rating Correlation"),
        ("code", "# Platzhalter: corr(), regplot"),
        ("markdown", "## Weighted Rating / Scoring"),
        ("code",
         "# weights = {\'rating\': 0.5, \'reviews\': 0.3, \'price\': 0.2}\n"
         "# df_clean[\'score\'] = sum(df_clean[col] * w for col, w in weights.items())"),
        ("markdown", "## Cluster Analysis"),
        ("code",
         "# from sklearn.cluster import KMeans\n"
         "# Platzhalter: Elbow-Methode, Silhouette Score"),
    ]
    return make_notebook(cells)


def _nb_insights() -> str:
    cells = [
        ("markdown", "# Business Communication & Insights"),
        ("markdown",
         "## Executive Summary\n\n"
         "> _3-5 Saetze: Was war die Frage, was haben wir gefunden, was empfehlen wir?_"),
        ("markdown", "## Key Visualizations\n\n> _Die 3-5 wichtigsten Erkenntnisse als saubere Charts._"),
        ("code",
         "import matplotlib.pyplot as plt\n"
         "from pathlib import Path\n\n"
         "FIGURES = Path(\'../public/img\')\n"
         "FIGURES.mkdir(parents=True, exist_ok=True)\n\n"
         "# Platzhalter: finale Plots exportieren\n"
         "# fig.savefig(FIGURES / \'key_finding.png\', bbox_inches=\'tight\', dpi=150)"),
        ("markdown",
         "## Recommendations\n\n"
         "| Empfehlung | Prioritaet | Aufwand |\n"
         "|------------|------------|---------|\n"
         "| _..._ | Hoch | _..._ |\n"
         "| _..._ | Mittel | _..._ |"),
        ("markdown", "## Next Steps & Open Questions\n\n* _..._\n* _..._"),
        ("markdown",
         "---\n\n"
         "> **Export:** Datei -> Export -> HTML fuer Stakeholder-Report ohne Code-Zellen."),
    ]
    return make_notebook(cells)
