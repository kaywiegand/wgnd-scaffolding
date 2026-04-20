"""
structure.py
------------
Definiert alle Ordner, die im Projekt erstellt werden.
Passe diese Liste an, um die Projektstruktur zu erweitern oder zu ändern.

Ordner ohne Dateien erhalten automatisch eine .gitkeep-Datei,
damit sie in Git getrackt werden können.
"""

from datetime import datetime


def get_folders(project_slug: str, project_type: str) -> list[str]:
    """
    Gibt eine Liste aller zu erstellenden Ordner zurueck.

    DAN: schlank - kein models/, configs/, docs/
    DSC: volle Struktur
    """
    today = datetime.today().strftime("%Y-%m-%d")

    if project_type.upper() == "DAN":
        return [
            "data/raw",
            "data/interim",
            "data/processed",
            "notebooks",
            f"src/{project_slug}/data",
            f"src/{project_slug}/features",
            f"src/{project_slug}/visualization",
            f"src/{project_slug}/analytics",
            "tests",
            "reports/figures",
            "reports/tables",
        ]

    # DSC: volle Struktur
    return [
        "data/raw",
        "data/interim",
        "data/processed",
        "notebooks",
        f"src/{project_slug}/data",
        f"src/{project_slug}/features",
        f"src/{project_slug}/visualization",
        f"src/{project_slug}/modeling",
        f"src/{project_slug}/evaluation",
        "tests",
        "configs",
        f"models/{today}",
        "reports/figures",
        "reports/tables",
        "docs",
    ]


# Ordner, die explizit LEER bleiben sollen (nur .gitkeep)
ALWAYS_EMPTY_DIRS = [
    "data/raw",
    "data/interim",
    "data/processed",
    "reports/figures",
    "reports/tables",
]
