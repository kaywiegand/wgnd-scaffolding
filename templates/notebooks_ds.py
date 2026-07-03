"""
notebooks_ds.py
---------------
Notebook-Definitionen für den Typ: DS (Data Science)

Jeder Eintrag in get_notebooks() ist ein Tupel:
    (dateipfad_relativ, notebook_json_string)

Die Notebook-Zellen bestehen aus Markdown-Headlines, die die Arbeitsstruktur
aus dem DS-Workflow vorstrukturieren. Code-Zellen sind als leere Starter vorbereitet.

📝 ANPASSEN: Füge Zellen hinzu, entferne Zellen oder ändere Überschriften
              in den jeweiligen cell-Listen unten.
"""

from .notebook_helper import make_notebook


def get_notebooks(project_name: str, project_slug: str) -> list[tuple[str, str]]:
    """
    Gibt alle DS-Notebooks als (pfad, inhalt)-Liste zurück.
    """
    return [
        ("notebooks/00_introduction.ipynb", _nb_introduction(project_name)),
        ("notebooks/01_exploration.ipynb", _nb_exploration()),
        ("notebooks/02_preprocessing.ipynb", _nb_preprocessing()),
        ("notebooks/03_modeling.ipynb", _nb_modeling()),
        ("notebooks/04_evaluation.ipynb", _nb_evaluation()),
        ("notebooks/05_reporting.ipynb", _nb_reporting()),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Einzelne Notebook-Definitionen
# ─────────────────────────────────────────────────────────────────────────────

def _nb_introduction(project_name: str) -> str:
    cells = [
        ("markdown", f"# {project_name}\n## 00 · Introduction & Project Context"),
        ("markdown", "## 🎯 Problem Statement\n\n> _Beschreibe hier das Business-Problem in 2–3 Sätzen._"),
        ("markdown", "## 📐 Success Metrics\n\n| Metrik | Zielwert | Begründung |\n|--------|----------|------------|\n| _z.B. RMSE_ | _< 0.05_ | _..._ |"),
        ("markdown", "## 📦 Data Sources\n\n| Quelle | Format | Beschreibung |\n|--------|--------|--------------|\n| _..._ | _CSV_ | _..._ |"),
        ("markdown", "## 📋 Hypotheses\n\n1. _Hypothese 1_\n2. _Hypothese 2_"),
        ("code", "# Imports & Setup\nimport sys\nsys.path.insert(0, '../src')\n\nimport pandas as pd\nimport numpy as np\nfrom pathlib import Path"),
    ]
    return make_notebook(cells)


def _nb_exploration() -> str:
    cells = [
        ("markdown", "# 01 · Exploratory Data Analysis (EDA)"),
        ("markdown", "## 📥 Data Acquisition\n\n> _Daten laden und ersten Überblick verschaffen._"),
        ("code", "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom pathlib import Path\n\nfrom wgnd.core.theme import setup\nfrom wgnd.inspect import (\n    inspect,\n    inspect_missing,\n    inspect_outliers,\n    inspect_outlier_detail,\n    inspect_correlations,\n)\n\nsetup()\n\nDATA_RAW = Path('../data/raw')\n\n# df_raw = pd.read_csv(DATA_RAW / 'your_file.csv')\n# df_raw.head()"),
        ("markdown", "## 🔍 Data Overview\n\n> _Vollständige EDA-Übersicht mit wgnd.inspect._"),
        ("code", "# df_eda = df_raw.copy()\n# inspect(df_eda)   # alle Sektionen auf einmal\n#\n# Einzelne Sektionen:\n# inspect(df_eda, sections=['dimensions', 'dtypes', 'missing'])"),
        ("markdown", "## 📊 Univariate Analysis\n\n> _Verteilungen einzelner Features analysieren._"),
        ("code", "# inspect_missing(df_eda)\n# Platzhalter: weitere Histogramme, Value Counts, etc."),
        ("markdown", "## 🔗 Bivariate / Multivariate Analysis\n\n> _Beziehungen zwischen Features und Target untersuchen._"),
        ("code", "# inspect_correlations(df_eda, target='your_target_col')\n# inspect_correlations(df_eda, target='your_target_col', show_pairplot=True)"),
        ("markdown", "## 🚨 Outlier Detection (Training Data)\n\n> _Ausreißer identifizieren – noch NICHT entfernen!_"),
        ("code", "# inspect_outliers(df_eda)\n# inspect_outlier_detail(df_eda, 'your_col', hue='your_target_col')"),
        ("markdown", "## 💡 Key Findings & Hypotheses\n\n| # | Finding | Implikation |\n|---|---------|-------------|\n| 1 | _..._ | _..._ |\n| 2 | _..._ | _..._ |"),
    ]
    return make_notebook(cells)


def _nb_preprocessing() -> str:
    cells = [
        ("markdown", "# 02 · Preprocessing & Feature Engineering"),
        ("markdown", "## ✂️ Data Splitting & Export\n\n> _Train/Test-Split als erstes – verhindert Data Leakage!_"),
        ("code", "from sklearn.model_selection import train_test_split\n\n# X = df_eda.drop(columns=['target'])\n# y = df_eda['target']\n# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"),
        ("markdown", "## 🧹 Data Cleaning\n\n> _NaN-Handling, Typkorrekturen, Duplikate._"),
        ("code", "# df_impute = X_train.copy()\n# Platzhalter: fillna, astype, drop_duplicates"),
        ("markdown", "## 🔎 Data Filtering\n\n> _Unplausible Werte und Duplikate entfernen._"),
        ("code", "# Platzhalter: Masken anwenden, Integritätsfehler bereinigen"),
        ("markdown", "## 📉 Outlier Handling\n\n> _Ausreißer nach definierten Regeln behandeln._"),
        ("code", "# df_clean = df_impute.copy()\n# Platzhalter: IQR-Clipping, Winsorizing, etc."),
        ("markdown", "## 📐 Data Distribution Adjustment\n\n> _Schiefverteilungen korrigieren (Log-Transform, etc.)._"),
        ("code", "# Platzhalter: Log-Transform, Box-Cox"),
        ("markdown", "## ⚙️ Feature Engineering\n\n> _Neue Features aus bestehenden Daten ableiten._"),
        ("code", "# Platzhalter: neue Spalten, Interaktionsterme, Encoding"),
        ("markdown", "## 📏 Feature Scaling & Normalization"),
        ("code", "from sklearn.preprocessing import StandardScaler\n\n# scaler = StandardScaler()\n# X_train_scaled = scaler.fit_transform(X_train)\n# X_test_scaled = scaler.transform(X_test)"),
        ("markdown", "## 🗜️ Feature Reduction & Selection"),
        ("code", "# Platzhalter: PCA, VIF, SelectKBest, RFE"),
        ("markdown", "## 💾 Export Preprocessed Data"),
        ("code", "from pathlib import Path\nDATA_PROCESSED = Path('../data/processed')\n\n# X_train_scaled.to_csv(DATA_PROCESSED / 'X_train.csv', index=False)\n# X_test_scaled.to_csv(DATA_PROCESSED / 'X_test.csv', index=False)"),
    ]
    return make_notebook(cells)


def _nb_modeling() -> str:
    cells = [
        ("markdown", "# 03 · Modeling"),
        ("markdown", "## 🏁 Baseline Model\n\n> _Einfachstes sinnvolles Modell als Referenzpunkt definieren._"),
        ("code", "# from sklearn.dummy import DummyRegressor\n# baseline = DummyRegressor(strategy='mean')\n# baseline.fit(X_train, y_train)"),
        ("markdown", "## 🏋️ Model Training\n\n> _Kandidaten-Modelle trainieren und grob vergleichen._"),
        ("code", "# Platzhalter: RandomForest, XGBoost, LinearRegression, etc."),
        ("markdown", "## 🔧 Hyperparameter Tuning"),
        ("code", "# from sklearn.model_selection import GridSearchCV\n# Platzhalter: param_grid, GridSearchCV, best_params_"),
        ("markdown", "## 🔗 Master Pipeline Definition\n\n> _Preprocessing + Modell in einer sklearn Pipeline kapseln._"),
        ("code", "from sklearn.pipeline import Pipeline\n\n# pipeline = Pipeline([\n#     ('preprocessor', preprocessor),\n#     ('model', best_model)\n# ])"),
        ("markdown", "## ✅ Validation Strategy\n\n> _Cross-Validation, Walk-Forward, etc._"),
        ("code", "# from sklearn.model_selection import cross_val_score\n# scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='neg_mean_squared_error')"),
        ("markdown", "## 🔮 Prediction Generation (Inference)"),
        ("code", "# y_pred = pipeline.predict(X_test)"),
        ("markdown", "## 💾 Final Pipeline Export"),
        ("code", "import joblib\nfrom pathlib import Path\nfrom datetime import datetime\n\nMODELS_DIR = Path('../models') / datetime.today().strftime('%Y-%m-%d')\nMODELS_DIR.mkdir(parents=True, exist_ok=True)\n\n# joblib.dump(pipeline, MODELS_DIR / 'pipeline.pkl')"),
    ]
    return make_notebook(cells)


def _nb_evaluation() -> str:
    cells = [
        ("markdown", "# 04 · Evaluation"),
        ("markdown", "## 📊 Test Data Evaluation\n\n> _Finale Bewertung ausschließlich auf Test-Daten._"),
        ("code", "# from sklearn.metrics import mean_squared_error, r2_score\n# mse = mean_squared_error(y_test, y_pred)\n# r2 = r2_score(y_test, y_pred)"),
        ("markdown", "## 🔍 Model Interpretation"),
        ("code", "# Platzhalter: SHAP, LIME, Permutation Importance"),
        ("markdown", "## ❌ Error Analysis\n\n> _Wo liegen die größten Fehler? Gibt es Muster?_"),
        ("code", "# residuals = y_test - y_pred\n# Platzhalter: Fehlerverteilung plotten"),
        ("markdown", "## 📌 Feature Importance Analysis"),
        ("code", "# Platzhalter: model.feature_importances_, SHAP values"),
        ("markdown", "## 📈 Residual Analysis"),
        ("code", "# Platzhalter: Residuals vs Fitted, QQ-Plot"),
        ("markdown", "## 💼 Business Interpretation\n\n> _Was bedeuten die Ergebnisse für das Business-Problem?_"),
        ("markdown", "## 🎯 Prediction Usability Assessment\n\n> _Ist das Modell gut genug für den produktiven Einsatz?_\n\n| Kriterium | Erfüllt? | Kommentar |\n|-----------|----------|-----------|\n| Ziel-Metrik erreicht | ✅ / ❌ | _..._ |\n| Overfitting | ✅ / ❌ | _..._ |\n| Fairness | ✅ / ❌ | _..._ |"),
    ]
    return make_notebook(cells)


def _nb_reporting() -> str:
    cells = [
        ("markdown", "# 05 · Reporting & Storytelling"),
        ("markdown", "## 📋 Executive Summary\n\n> _3–5 Sätze: Was war das Problem, was haben wir getan, was ist das Ergebnis?_"),
        ("markdown", "## 📊 Key Visualizations\n\n> _Die wichtigsten Plots für die Präsentation._"),
        ("code", "# Platzhalter: finale Plots, Exportieren nach public/img/"),
        ("markdown", "## 📝 Recommendations\n\n| Empfehlung | Priorität | Aufwand |\n|------------|-----------|--------|\n| _..._ | Hoch | _..._ |"),
        ("markdown", "## 🔭 Next Steps & Open Questions"),
    ]
    return make_notebook(cells)
