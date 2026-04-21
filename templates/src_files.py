"""
src_files.py
------------
Python-Quelldateien mit initialem Inhalt.

Jeder Eintrag in get_files() gibt (pfad, inhalt) zurück.
Der Pfad ist relativ zum Projektstamm.

📝 ANPASSEN: Ändere den initialen Inhalt der einzelnen Files,
              füge neue Files hinzu oder entferne welche.
"""

from datetime import datetime


def get_files(project_name: str, project_slug: str, project_type: str) -> list[tuple[str, str]]:
    """
    Gibt alle src-Python-Dateien als (pfad, inhalt)-Liste zurück.
    """
    base_path = f"src/{project_slug}"
    files = [
        (f"{base_path}/__init__.py", _init_py(project_name)),
        (f"{base_path}/config.py", _config_py(project_name, project_slug)),
        (f"{base_path}/settings.py", _settings_py()),
        (f"{base_path}/utils.py", _utils_py()),
        (f"{base_path}/data/__init__.py", ""),
        (f"{base_path}/data/load_data.py", _load_data_py()),
        (f"{base_path}/data/make_dataset.py", _make_dataset_py()),
        (f"{base_path}/features/__init__.py", ""),
        (f"{base_path}/features/build_features.py", _build_features_py()),
        (f"{base_path}/visualization/__init__.py", ""),
        (f"{base_path}/visualization/plot_metrics.py", _plot_metrics_py()),
    ]

    if project_type.upper() == "DSC":
        files += [
            (f"{base_path}/modeling/__init__.py", ""),
            (f"{base_path}/modeling/baseline.py", _baseline_py()),
            (f"{base_path}/modeling/train_model.py", _train_model_py()),
            (f"{base_path}/evaluation/__init__.py", ""),
            (f"{base_path}/evaluation/evaluate_model.py", _evaluate_model_py()),
        ]

    if project_type.upper() == "DAN":
        # DAN: nur __init__.py in Unterordnern – keine vorgefertigten Python-Files
        # Begruendung: kleine Projekte, eigene Scripts werden bei Bedarf ergaenzt
        files = [
            (f"{base_path}/__init__.py", _init_py(project_name)),
            (f"{base_path}/config.py", _config_py(project_name, project_slug)),
            (f"{base_path}/settings.py", _settings_py()),
            (f"{base_path}/notebook.py", _notebook_py(project_slug)),
            (f"{base_path}/utils.py", _utils_py()),
            (f"{base_path}/data/__init__.py", ""),
            (f"{base_path}/features/__init__.py", ""),
            (f"{base_path}/visualization/__init__.py", ""),
            (f"{base_path}/analytics/__init__.py", ""),
        ]

    return files


# ─────────────────────────────────────────────────────────────────────────────
# File-Inhalte
# ─────────────────────────────────────────────────────────────────────────────

def _init_py(project_name: str) -> str:
    return f'"""{ project_name } – Source Package."""\n'


def _config_py(project_name: str, project_slug: str) -> str:
    return f'''"""
config.py
---------
Zentrale Projektkonfiguration: Pfade, Konstanten, Umgebungsvariablen.

Importiere dieses Modul in Notebooks oder Scripts:
    from {project_slug}.config import PATHS, PROJECT_NAME
"""

from pathlib import Path

# ─── Projektname ───────────────────────────────────────────────────────────
PROJECT_NAME = "{project_name}"
RANDOM_SEED = 42

# ─── Verzeichnisse ─────────────────────────────────────────────────────────
# Basis ist das Verzeichnis, in dem config.py liegt → 2 Ebenen nach oben
_SRC = Path(__file__).resolve().parent.parent.parent

PATHS = {{
    "root":      _SRC,
    "data":      _SRC / "data",
    "raw":       _SRC / "data" / "raw",
    "interim":   _SRC / "data" / "interim",
    "processed": _SRC / "data" / "processed",
    "models":    _SRC / "models",
    "reports":   _SRC / "reports",
    "figures":   _SRC / "reports" / "figures",
    "configs":   _SRC / "configs",
}}

# ─── Modell-Konstanten ──────────────────────────────────────────────────────
TEST_SIZE   = 0.2
VAL_SIZE    = 0.1
N_CV_FOLDS  = 5
'''


def _settings_py() -> str:
    return '''"""
settings.py
-----------
Visuelle und Logging-Konfiguration:
  - wgnd Theme (Matplotlib / Seaborn)
  - Farbpaletten
  - Logging-Format
"""

import logging
import matplotlib.pyplot as plt
import seaborn as sns

# ─── Farben ────────────────────────────────────────────────────────────────
PALETTE_PRIMARY  = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B"]
PALETTE_SEABORN  = "muted"

# ─── Plot-Stil ─────────────────────────────────────────────────────────────
FIGSIZE_DEFAULT  = (10, 6)
FIGSIZE_WIDE     = (14, 6)
DPI              = 120


def setup_plotting() -> None:
    """Setzt wgnd-Theme, Notebook-Optionen und autoreload."""
    import pandas as pd
    from wgnd.core.theme import setup as wgnd_setup

    wgnd_setup()
    plt.rcParams.update({
        "figure.figsize": FIGSIZE_DEFAULT,
        "figure.dpi":     DPI,
    })
    pd.set_option("display.notebook_repr_html", True)
    pd.set_option("display.max_rows", 10)
    pd.set_option("display.max_columns", None)

    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip:
            ip.run_line_magic("load_ext", "autoreload")
            ip.run_line_magic("autoreload", "2")
    except Exception:
        pass


# ─── Logging ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("project")
'''


def _notebook_py(project_slug: str) -> str:
    return f'''"""
notebook.py
-----------
Zentraler Einstiegspunkt für alle Notebooks.
Importiere einmalig am Anfang jedes Notebooks:

    from {project_slug}.notebook import *
    setup_plotting()
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from wgnd.inspect import (
    inspect,
    inspect_missing,
    inspect_duplicates,
    inspect_outliers,
    inspect_outlier_detail,
    inspect_correlations,
)
from wgnd.core._output import success, warn, info_box, show_df

from {project_slug}.config import PATHS, PROJECT_NAME, RANDOM_SEED
from {project_slug}.settings import setup_plotting

__all__ = [
    "pd", "np", "plt", "sns", "Path",
    "inspect", "inspect_missing", "inspect_duplicates",
    "inspect_outliers", "inspect_outlier_detail", "inspect_correlations",
    "success", "warn", "info_box", "show_df",
    "PATHS", "PROJECT_NAME", "RANDOM_SEED", "setup_plotting",
]
'''


def _utils_py() -> str:
    return '''"""
utils.py
--------
Allgemeine Hilfsfunktionen:
  - Timer / Decorator
  - Datei-Helfer
  - Logging-Shortcut
"""

import time
import logging
from pathlib import Path
from functools import wraps

logger = logging.getLogger(__name__)


def timer(func):
    """Decorator: misst und loggt die Laufzeit einer Funktion."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} abgeschlossen in {elapsed:.2f}s")
        return result
    return wrapper


def ensure_dir(path: Path) -> Path:
    """Erstellt Verzeichnis, falls nicht vorhanden. Gibt Pfad zurück."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(directory: Path, pattern: str = "*") -> list[Path]:
    """Gibt alle Dateien in einem Verzeichnis zurück, die dem Muster entsprechen."""
    return sorted(Path(directory).glob(pattern))
'''


def _load_data_py() -> str:
    return '''"""
load_data.py
------------
Funktionen zum Laden von Rohdaten.
Gibt immer einen unveränderlichen df_raw zurück – nie direkt bearbeiten!
"""

import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_csv(filepath: str | Path, **kwargs) -> pd.DataFrame:
    """
    Lädt eine CSV-Datei und gibt einen unveränderlichen DataFrame zurück.

    Args:
        filepath: Pfad zur CSV-Datei.
        **kwargs: Weitere Argumente für pd.read_csv().

    Returns:
        df_raw: Unveränderlicher Rohdaten-DataFrame.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")

    df = pd.read_csv(filepath, **kwargs)
    logger.info(f"Geladen: {filepath.name} → {df.shape[0]:,} Zeilen, {df.shape[1]} Spalten")
    return df


def load_excel(filepath: str | Path, sheet_name: str | int = 0, **kwargs) -> pd.DataFrame:
    """Lädt eine Excel-Datei."""
    df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
    logger.info(f"Geladen: {Path(filepath).name} → {df.shape}")
    return df
'''


def _make_dataset_py() -> str:
    return '''"""
make_dataset.py
---------------
Verarbeitet Rohdaten zu analysierbaren Datensätzen.
Ruft typischerweise load_data → Validierung → Basisbereinigung auf.
"""

import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_dataframe(df: pd.DataFrame, required_cols: list[str]) -> bool:
    """
    Prüft, ob alle erwarteten Spalten vorhanden sind.

    Args:
        df: DataFrame zum Prüfen.
        required_cols: Liste der Pflichtspalten.

    Returns:
        True wenn valide, sonst wird ein ValueError geworfen.
    """
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Fehlende Spalten: {missing}")
    logger.info(f"Validierung erfolgreich: {len(required_cols)} Spalten geprüft.")
    return True


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basisbereinigung: Duplikate entfernen, Spaltennahmen normalisieren.

    Args:
        df: Eingabe-DataFrame (wird nicht verändert).

    Returns:
        Bereinigter DataFrame.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Duplikate entfernt: {before - len(df)} Zeilen")
    return df
'''


def _build_features_py() -> str:
    return '''"""
build_features.py
-----------------
Feature Engineering: neue Features aus bestehenden Daten ableiten.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def add_date_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Extrahiert Jahr, Monat, Wochentag aus einer Datumsspalte.

    Args:
        df: Eingabe-DataFrame.
        date_col: Name der Datumsspalte.

    Returns:
        DataFrame mit neuen Datums-Features.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[f"{date_col}_year"]  = df[date_col].dt.year
    df[f"{date_col}_month"] = df[date_col].dt.month
    df[f"{date_col}_dow"]   = df[date_col].dt.dayofweek
    logger.info(f"Datums-Features aus '{date_col}' erstellt.")
    return df
'''


def _plot_metrics_py() -> str:
    return '''"""
plot_metrics.py
---------------
Standardisierte Plots für Reports und Notebooks.
Alle Funktionen geben eine matplotlib Figure zurück.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path


def plot_distribution(series: pd.Series, title: str = "", save_path: Path = None) -> plt.Figure:
    """Histogramm + KDE einer numerischen Reihe."""
    fig, ax = plt.subplots()
    sns.histplot(series.dropna(), kde=True, ax=ax)
    ax.set_title(title or series.name)
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


def plot_correlation_matrix(df: pd.DataFrame, title: str = "Korrelationsmatrix",
                            save_path: Path = None) -> plt.Figure:
    """Heatmap der Korrelationsmatrix."""
    fig, ax = plt.subplots(figsize=(12, 8))
    mask = np.triu(np.ones_like(df.corr(), dtype=bool))
    sns.heatmap(df.corr(), mask=mask, annot=True, fmt=".2f",
                cmap="coolwarm", ax=ax, linewidths=0.5)
    ax.set_title(title)
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig
'''


def _baseline_py() -> str:
    return '''"""
baseline.py  (DSC)
------------------
Definition des Baseline-Modells.
Das Baseline-Modell ist das einfachste sinnvolle Modell –
es dient als untere Grenze für alle komplexeren Ansätze.
"""

from sklearn.dummy import DummyRegressor, DummyClassifier
import logging

logger = logging.getLogger(__name__)


def get_regression_baseline(strategy: str = "mean"):
    """Gibt ein Dummy-Regressionsmodell zurück."""
    model = DummyRegressor(strategy=strategy)
    logger.info(f"Baseline Regressor: strategy='{strategy}'")
    return model


def get_classification_baseline(strategy: str = "most_frequent"):
    """Gibt ein Dummy-Klassifikationsmodell zurück."""
    model = DummyClassifier(strategy=strategy)
    logger.info(f"Baseline Classifier: strategy='{strategy}'")
    return model
'''


def _train_model_py() -> str:
    return '''"""
train_model.py  (DSC)
---------------------
Modelltraining und Pipeline-Export.
"""

import joblib
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def train(pipeline, X_train, y_train):
    """
    Trainiert eine sklearn-Pipeline.

    Args:
        pipeline: sklearn Pipeline oder Estimator.
        X_train:  Trainings-Features.
        y_train:  Trainings-Labels.

    Returns:
        Trainierte Pipeline.
    """
    logger.info("Training gestartet …")
    pipeline.fit(X_train, y_train)
    logger.info("Training abgeschlossen.")
    return pipeline


def export_model(pipeline, models_dir: Path, filename: str = "pipeline.pkl") -> Path:
    """
    Serialisiert die Pipeline mit joblib.

    Args:
        pipeline:   Trainierte Pipeline.
        models_dir: Zielverzeichnis.
        filename:   Dateiname (Standard: pipeline.pkl).

    Returns:
        Pfad zur gespeicherten Datei.
    """
    models_dir = Path(models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    out_path = models_dir / filename
    joblib.dump(pipeline, out_path)
    logger.info(f"Modell exportiert: {out_path}")
    return out_path
'''


def _evaluate_model_py() -> str:
    return '''"""
evaluate_model.py  (DSC)
------------------------
Metriken, Fehleranalyse, Interpretation.
"""

import pandas as pd
import numpy as np
import logging
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error,
    r2_score, accuracy_score, classification_report
)

logger = logging.getLogger(__name__)


def regression_metrics(y_true, y_pred) -> dict:
    """Berechnet gängige Regressions-Metriken."""
    metrics = {
        "MAE":  mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2":   r2_score(y_true, y_pred),
    }
    for k, v in metrics.items():
        logger.info(f"  {k}: {v:.4f}")
    return metrics


def classification_metrics(y_true, y_pred) -> dict:
    """Berechnet gängige Klassifikations-Metriken."""
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "report":   classification_report(y_true, y_pred),
    }
    logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
    return metrics
'''


def _segment_analysis_py() -> str:
    return '''"""
segment_analysis.py  (DAN)
--------------------------
Marktsegmentierung und Cluster-Analyse.
"""

import pandas as pd
import numpy as np
import logging
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def kmeans_segmentation(df: pd.DataFrame, features: list[str],
                        n_clusters: int = 4, random_state: int = 42) -> pd.DataFrame:
    """
    Führt K-Means-Clustering auf ausgewählten Features durch.

    Args:
        df:           Eingabe-DataFrame.
        features:     Spalten für das Clustering.
        n_clusters:   Anzahl Cluster.
        random_state: Reproduzierbarkeit.

    Returns:
        DataFrame mit neuer Spalte 'cluster'.
    """
    df = df.copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features].dropna())

    km = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    df.loc[df[features].dropna().index, "cluster"] = km.fit_predict(X_scaled)
    logger.info(f"K-Means abgeschlossen: {n_clusters} Cluster erstellt.")
    return df


def weighted_score(df: pd.DataFrame, score_cols: dict[str, float]) -> pd.Series:
    """
    Berechnet einen gewichteten Score aus mehreren Spalten.

    Args:
        df:          Eingabe-DataFrame.
        score_cols:  {spaltenname: gewicht} – Gewichte müssen sich auf 1 summieren.

    Returns:
        pd.Series mit gewichtetem Score.
    """
    score = sum(df[col] * weight for col, weight in score_cols.items())
    logger.info(f"Weighted Score berechnet aus: {list(score_cols.keys())}")
    return score
'''
