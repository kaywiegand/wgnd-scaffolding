"""
test_files.py
-------------
Initiale Test-Dateien für pytest.

📝 ANPASSEN: Füge neue Test-Dateien hinzu oder ändere den initialen Inhalt.
"""


def get_files(project_slug: str, project_type: str) -> list[tuple[str, str]]:
    files = [
        ("tests/__init__.py", ""),
        ("tests/test_data.py", _test_data(project_slug)),
        ("tests/test_features.py", _test_features(project_slug)),
    ]
    if project_type.upper() == "DSC":
        files.append(("tests/test_modeling.py", _test_modeling(project_slug)))
    return files


def _test_data(project_slug: str) -> str:
    return f'''"""
test_data.py
------------
Tests für Datenladen und Validierung.
Ausführen mit: pytest tests/
"""

import pytest
import pandas as pd
from {project_slug}.data.make_dataset import validate_dataframe, basic_clean


def test_validate_dataframe_passes():
    df = pd.DataFrame({{"a": [1, 2], "b": [3, 4]}})
    assert validate_dataframe(df, ["a", "b"]) is True


def test_validate_dataframe_raises_on_missing_col():
    df = pd.DataFrame({{"a": [1, 2]}})
    with pytest.raises(ValueError, match="Fehlende Spalten"):
        validate_dataframe(df, ["a", "missing_col"])


def test_basic_clean_removes_duplicates():
    df = pd.DataFrame({{"a": [1, 1, 2], "b": [3, 3, 4]}})
    cleaned = basic_clean(df)
    assert len(cleaned) == 2


def test_basic_clean_normalizes_columns():
    df = pd.DataFrame({{"Col A": [1], "Col-B": [2]}})
    cleaned = basic_clean(df)
    assert "col_a" in cleaned.columns
'''


def _test_features(project_slug: str) -> str:
    return f'''"""
test_features.py
----------------
Tests für Feature Engineering.
"""

import pytest
import pandas as pd
from {project_slug}.features.build_features import add_date_features


def test_add_date_features_creates_columns():
    df = pd.DataFrame({{"date": ["2024-01-15", "2024-06-30"]}})
    result = add_date_features(df, "date")
    assert "date_year" in result.columns
    assert "date_month" in result.columns
    assert "date_dow" in result.columns


def test_add_date_features_correct_values():
    df = pd.DataFrame({{"date": ["2024-01-15"]}})
    result = add_date_features(df, "date")
    assert result["date_year"].iloc[0] == 2024
    assert result["date_month"].iloc[0] == 1
'''


def _test_modeling(project_slug: str) -> str:
    return f'''"""
test_modeling.py  (DSC)
-----------------------
Tests für Modelltraining und Evaluation.
"""

import pytest
import numpy as np
from {project_slug}.modeling.baseline import get_regression_baseline
from {project_slug}.evaluation.evaluate_model import regression_metrics


def test_baseline_trains_and_predicts():
    model = get_regression_baseline()
    X = np.array([[1], [2], [3]])
    y = np.array([1.0, 2.0, 3.0])
    model.fit(X, y)
    preds = model.predict(X)
    assert len(preds) == 3


def test_regression_metrics_keys():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.1, 1.9, 3.1])
    metrics = regression_metrics(y_true, y_pred)
    assert "MAE" in metrics
    assert "RMSE" in metrics
    assert "R2" in metrics
'''
