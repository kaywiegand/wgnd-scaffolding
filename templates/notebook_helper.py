"""
notebook_helper.py
------------------
Hilfsfunktionen zum Erzeugen gültiger Jupyter Notebook (.ipynb) Dateien.

Ein Notebook besteht aus einer Liste von "Cells" (Zellen).
Jede Zelle ist entweder:
  - 'markdown' : Text, Überschriften, Erklärungen
  - 'code'     : Python-Code

Verwendung:
    cells = [
        ("markdown", "# Mein Notebook\n\nBeschreibung"),
        ("code", "import pandas as pd"),
        ("markdown", "## Abschnitt 1"),
    ]
    content = make_notebook(cells)
"""

import json
import uuid


def make_notebook(cells: list[tuple[str, str]]) -> str:
    """
    Erstellt ein gültiges Jupyter Notebook als JSON-String.

    Args:
        cells: Liste von (cell_type, source) Tupeln.
               cell_type ist 'markdown' oder 'code'.
               source ist der Zellen-Inhalt als String.

    Returns:
        JSON-String des Notebooks (direkt als .ipynb speicherbar)
    """
    notebook_cells = []

    for cell_type, source in cells:
        if cell_type == "markdown":
            cell = {
                "cell_type": "markdown",
                "id": str(uuid.uuid4())[:8],
                "metadata": {},
                "source": source,
            }
        else:  # code
            cell = {
                "cell_type": "code",
                "id": str(uuid.uuid4())[:8],
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source,
            }
        notebook_cells.append(cell)

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "version": "3.10.0",
            },
        },
        "cells": notebook_cells,
    }

    return json.dumps(notebook, indent=2, ensure_ascii=False)
