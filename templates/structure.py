"""
structure.py
------------
Definiert alle Ordner, die im Projekt erstellt werden.
Passe diese Liste an, um die Projektstruktur zu erweitern oder zu ändern.

Ordner ohne Dateien erhalten automatisch eine .gitkeep-Datei,
damit sie in Git getrackt werden können.
"""

from datetime import datetime


def get_folders(package_name: str, project_type: str) -> list[str]:
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
            f"src/{package_name}/data",
            f"src/{package_name}/features",
            f"src/{package_name}/visualization",
            f"src/{package_name}/analytics",
            "tests",
            "reports/img",
            "reports/mds",
        ]

    # DSC: volle Struktur
    return [
        "data/raw",
        "data/interim",
        "data/processed",
        "notebooks",
        f"src/{package_name}/data",
        f"src/{package_name}/features",
        f"src/{package_name}/visualization",
        f"src/{package_name}/modeling",
        f"src/{package_name}/evaluation",
        "tests",
        "configs",
        f"models/{today}",
        "reports/img",
        "reports/mds",
        "docs",
    ]


# Ordner, die explizit LEER bleiben sollen (nur .gitkeep)
ALWAYS_EMPTY_DIRS = [
    "data/raw",
    "data/interim",
    "data/processed",
    "reports/img",
    "reports/mds",
]
