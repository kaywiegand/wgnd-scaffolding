"""
config_files.py
---------------
YAML-Konfigurationsdateien für das Projekt.

Jeder Eintrag gibt (pfad, inhalt) zurück.

📝 ANPASSEN: Ändere Standardwerte oder füge neue YAML-Felder hinzu.
              YAML verwendet Einrückung (2 Spaces) für Hierarchie –
              KEINE Tabs!
"""


def get_files(project_name: str, project_slug: str, project_type: str) -> list[tuple[str, str]]:
    if project_type.upper() == "DA":
        # DA: keine YAML-Configs - Pfade und Einstellungen leben in config.py / settings.py
        return []
    # DS: drei YAML-Configs
    return [
        ("configs/default.yaml",  _default_yaml(project_name, project_type)),
        ("configs/data.yaml",     _data_yaml()),
        ("configs/model.yaml",    _model_yaml(project_type)),
    ]


def _default_yaml(project_name: str, project_type: str) -> str:
    return f"""\
# default.yaml
# ------------
# Allgemeine Projekteinstellungen.
# Diese Werte können in anderen YAMLs überschrieben werden.

project:
  name: "{project_name}"
  type: "{project_type}"  # DS oder DA
  version: "0.1.0"
  random_seed: 42

logging:
  level: INFO              # DEBUG | INFO | WARNING | ERROR
  format: "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"

output:
  save_figures: true
  figure_format: "png"     # png | svg | pdf
  report_format: "html"
"""


def _data_yaml() -> str:
    return """\
# data.yaml
# ---------
# Pfade zu Datenquellen und -verarbeitungsparametern.
#
# Relative Pfade = relativ zum Projektstamm.
# Tipp: Rohdaten NIE verändern – immer Kopien in interim/ oder processed/ ablegen.

paths:
  raw:       "data/raw"
  interim:   "data/interim"
  processed: "data/processed"

# Quell-Dateien (Dateinamen hier eintragen)
sources:
  main: ""          # z.B. "customers_2024.csv"
  secondary: []     # weitere Quelldateien

# Datentypen für automatisches Casting beim Laden
# Beispiel:
#   dtypes:
#     customer_id: str
#     signup_date: datetime
dtypes: {}

# Split-Parameter
split:
  test_size:       0.20
  validation_size: 0.10
  stratify: null    # Spaltenname für stratifizierten Split oder null
"""


def _model_yaml(project_type: str) -> str:
    if project_type.upper() == "DA":
        return """\
# model.yaml  (DA)
# -----------------
# Konfiguration für Analyse-Algorithmen und Cluster-Parameter.

clustering:
  kmeans:
    n_clusters: 4
    random_state: 42
    n_init: "auto"

scoring:
  # Gewichte für weighted_score() – müssen sich auf 1.0 summieren
  weights:
    rating:  0.5
    reviews: 0.3
    price:   0.2
"""
    else:  # DS
        return """\
# model.yaml  (DS)
# -----------------
# Hyperparameter und Modell-Konfiguration.
#
# Tipp: Verändere hier Hyperparameter, ohne den Code anfassen zu müssen.

baseline:
  strategy: "mean"       # mean | median | most_frequent

random_forest:
  n_estimators: 200
  max_depth: null        # null = unbegrenzt
  min_samples_split: 2
  random_state: 42

xgboost:
  n_estimators: 300
  max_depth: 6
  learning_rate: 0.05
  subsample: 0.8
  colsample_bytree: 0.8
  random_state: 42

cross_validation:
  n_splits: 5
  shuffle: true
  scoring: "neg_mean_squared_error"  # Regressions-Metrik
  # scoring: "accuracy"              # Klassifikations-Metrik
"""
