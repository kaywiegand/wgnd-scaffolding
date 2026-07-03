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

    DA: schlank - kein models/, configs/, docs/
    DS: volle Struktur
    """
    today = datetime.today().strftime("%Y-%m-%d")

    if project_type.upper() == "DA":
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
            "public/img",
            "public/md",
        ]

    # DS: volle Struktur
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
        "public/img",
        "public/md",
        "docs",
    ]


# Ordner, die explizit LEER bleiben sollen (nur .gitkeep)
ALWAYS_EMPTY_DIRS = [
    "data/raw",
    "data/interim",
    "data/processed",
    "public/img",
    "public/md",
]
