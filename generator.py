#!/usr/bin/env python3
"""
generator.py
============
DAN / DSC Project Scaffolding Generator

Verwendung:
    python generator.py --name "Mein Projekt" --path "C:/Projects" --type DSC
    python generator.py --name "Restaurant Analysis" --path "./projects" --type DAN

Argumente:
    --name      Projektname (z.B. "Restaurant Analysis Q3 2024")
    --slug      [optional] URL-sicherer Bezeichner (z.B. "restaurant_analysis")
                Wenn weggelassen, wird automatisch aus --name abgeleitet.
    --path      Übergeordnetes Verzeichnis, IN dem das Projekt erstellt wird
    --type      Projekttyp: DSC (Data Science) oder DAN (Data Analytics)

Beispiele:
    # DSC-Projekt im aktuellen Verzeichnis
    python generator.py --name "House Price Prediction" --path "." --type DSC

    # DAN-Projekt in einem bestimmten Ordner, mit eigenem Slug
    python generator.py --name "Market Analysis 2024" --slug "market_2024" \\
                        --path "C:/Users/dein_name/Projects" --type DAN
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# ─── Template-Module importieren ───────────────────────────────────────────
from templates.structure      import get_folders, ALWAYS_EMPTY_DIRS
from templates.root_files     import get_files as get_root_files
from templates.src_files      import get_files as get_src_files
from templates.config_files   import get_files as get_config_files
from templates.test_files     import get_files as get_test_files
from templates.docs_files     import get_files as get_docs_files
from templates.readme_template import get_readme
from templates.notebooks_dsc  import get_notebooks as get_notebooks_dsc
from templates.notebooks_dan  import get_notebooks as get_notebooks_dan


# ─── Farb-Codes für die Konsolen-Ausgabe ───────────────────────────────────
class C:
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

def ok(msg: str)    -> None: print(f"  {C.GREEN}✓{C.RESET}  {msg}")
def info(msg: str)  -> None: print(f"  {C.CYAN}→{C.RESET}  {msg}")
def warn(msg: str)  -> None: print(f"  {C.YELLOW}⚠{C.RESET}  {msg}")
def err(msg: str)   -> None: print(f"  {C.RED}✗{C.RESET}  {msg}")
def head(msg: str)  -> None: print(f"\n{C.BOLD}{C.CYAN}{msg}{C.RESET}")
def sep()           -> None: print(f"  {'─' * 55}")


# ─── Hilfsfunktionen ───────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """
    Wandelt einen beliebigen Projektnamen in einen Python-kompatiblen
    Bezeichner um.

    Beispiel: "My Cool Project 2024!" → "my_cool_project_2024"
    """
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    # Python-Identifier darf nicht mit Zahl beginnen
    if slug and slug[0].isdigit():
        slug = "project_" + slug
    return slug or "project"


def dir_name_from(name: str) -> str:
    """
    Erstellt einen filesystem-sicheren Ordnernamen aus dem Projektnamen.
    Behaelt Gross/Kleinschreibung und Bindestriche - ersetzt nur OS-ungueltiges.

    Beispiel: "DAN Telefonica Churn"  -> "DAN_Telefonica_Churn"
              "DAN_Telefonica-Churn"  -> "DAN_Telefonica-Churn"
    """
    safe = name.strip()
    import re as _re
    safe = _re.sub(r'[/\\\\:*?"<>|]', "_", safe)
    safe = _re.sub(r"\s+", "_", safe)
    return safe or "project"


def write_file(base: Path, rel_path: str, content: str) -> None:
    """Schreibt eine Datei mit dem angegebenen Inhalt."""
    target = base / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    ok(f"  {rel_path}")


def create_gitkeep(folder: Path) -> None:
    """Erstellt eine .gitkeep-Datei in einem leeren Ordner."""
    (folder / ".gitkeep").touch()


# ─── Argument-Parser ───────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generator.py",
        description=(
            "DAN / DSC Project Scaffolding Generator\n"
            "Erstellt eine vollständige Projektstruktur für Data Science / Analytics."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Beispiele:\n"
            "  python generator.py --name \"House Price\" --path . --type DSC\n"
            "  python generator.py --name \"Market Analysis\" --path ./projects --type DAN\n"
        ),
    )
    parser.add_argument(
        "--name", "-n",
        required=True,
        help="Projektname (z.B. 'Restaurant Analysis 2024')",
    )
    parser.add_argument(
        "--slug", "-s",
        default=None,
        help="[optional] Python-Bezeichner für das Paket (z.B. 'restaurant_analysis'). "
             "Wird automatisch aus --name abgeleitet, wenn nicht angegeben.",
    )
    parser.add_argument(
        "--path", "-p",
        required=True,
        help="Übergeordnetes Verzeichnis, IN dem das Projekt erstellt wird",
    )
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["DSC", "DAN", "dsc", "dan"],
        help="Projekttyp: DSC (Data Science) oder DAN (Data Analytics)",
    )
    return parser


# ─── Hauptfunktion ─────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    project_name = args.name.strip()
    project_type = args.type.upper()
    project_slug = args.slug.strip() if args.slug else slugify(project_name)
    parent_dir   = Path(args.path).expanduser().resolve()

    # Slug validieren
    if not re.match(r"^[a-z_][a-z0-9_]*$", project_slug):
        err(f"Ungültiger Slug: '{project_slug}'")
        err("Nur Kleinbuchstaben, Ziffern und Unterstriche erlaubt. Darf nicht mit Ziffer beginnen.")
        sys.exit(1)

    project_dir_name = dir_name_from(project_name)
    project_dir = parent_dir / project_dir_name

    # ── Header ausgeben ────────────────────────────────────────────────────
    head("DAN/DSC Scaffolding Generator")
    sep()
    info(f"Projektname : {project_name}")
    info(f"Slug        : {project_slug}")
    info(f"Typ         : {project_type}")
    info(f"Ziel        : {project_dir}")
    sep()

    # ── Übergeordnetes Verzeichnis prüfen ──────────────────────────────────
    if not parent_dir.exists():
        try:
            parent_dir.mkdir(parents=True)
            ok(f"Übergeordnetes Verzeichnis erstellt: {parent_dir}")
        except Exception as e:
            err(f"Kann Verzeichnis nicht erstellen: {parent_dir}")
            err(str(e))
            sys.exit(1)

    # ── Projektverzeichnis prüfen ──────────────────────────────────────────
    if project_dir.exists():
        warn(f"Verzeichnis existiert bereits: {project_dir}")
        antwort = input("  Überschreiben? Bestehende Dateien werden ersetzt. [j/N] ").strip().lower()
        if antwort not in ("j", "ja", "y", "yes"):
            info("Abgebrochen.")
            sys.exit(0)
    else:
        project_dir.mkdir(parents=True)
        ok(f"Projektverzeichnis erstellt: {project_dir}")

    errors: list[str] = []

    # ── 1. Ordner erstellen ────────────────────────────────────────────────
    head("1/5  Ordner erstellen")
    folders = get_folders(project_slug, project_type)
    for folder_rel in folders:
        folder_abs = project_dir / folder_rel
        try:
            folder_abs.mkdir(parents=True, exist_ok=True)
            # Leere Daten-Ordner erhalten .gitkeep
            if any(folder_rel.startswith(d) for d in ALWAYS_EMPTY_DIRS):
                create_gitkeep(folder_abs)
            ok(folder_rel + "/")
        except Exception as e:
            errors.append(f"Ordner '{folder_rel}': {e}")
            err(f"Fehler bei '{folder_rel}': {e}")

    # ── 2. Root-Dateien schreiben ──────────────────────────────────────────
    head("2/5  Root-Dateien")
    root_files = get_root_files(project_name, project_slug, project_type)
    for rel_path, content in root_files:
        try:
            write_file(project_dir, rel_path, content)
        except Exception as e:
            errors.append(f"Root '{rel_path}': {e}")
            err(f"Fehler bei '{rel_path}': {e}")

    # ── 3. README.md ──────────────────────────────────────────────────────
    head("3/5  README.md")
    try:
        readme_content = get_readme(project_name, project_slug, project_type)
        write_file(project_dir, "README.md", readme_content)
    except Exception as e:
        errors.append(f"README.md: {e}")
        err(f"Fehler bei README.md: {e}")

    # ── 4. Source-Dateien ─────────────────────────────────────────────────
    head("4/5  Source-Dateien (src/ · configs/ · tests/ · docs/)")
    all_source_files = (
        get_src_files(project_name, project_slug, project_type)
        + get_config_files(project_name, project_slug, project_type)
        + get_test_files(project_slug, project_type)
        + get_docs_files(project_name, project_type)
    )
    for rel_path, content in all_source_files:
        try:
            write_file(project_dir, rel_path, content)
        except Exception as e:
            errors.append(f"Source '{rel_path}': {e}")
            err(f"Fehler bei '{rel_path}': {e}")

    # ── 5. Notebooks ──────────────────────────────────────────────────────
    head("5/5  Notebooks")
    if project_type == "DSC":
        notebooks = get_notebooks_dsc(project_name, project_slug)
    else:
        notebooks = get_notebooks_dan(project_name, project_slug)

    for rel_path, content in notebooks:
        try:
            write_file(project_dir, rel_path, content)
        except Exception as e:
            errors.append(f"Notebook '{rel_path}': {e}")
            err(f"Fehler bei '{rel_path}': {e}")

    # ── Abschlussbericht ──────────────────────────────────────────────────
    sep()
    if errors:
        head("⚠️  Abgeschlossen mit Fehlern")
        for e in errors:
            err(e)
    else:
        head("✅  Projekt erfolgreich erstellt!")

    print(f"""
{C.BOLD}Nächste Schritte in VS Code:{C.RESET}

  1. Ordner öffnen:
     {C.CYAN}Datei → Ordner öffnen → {project_dir}{C.RESET}

  2. Terminal öffnen (Strg + ` oder Ansicht → Terminal)

  3. uv installieren (einmalig, falls noch nicht vorhanden):
     {C.CYAN}pip install uv{C.RESET}

  4. Virtuelle Umgebung erstellen:
     {C.CYAN}uv venv{C.RESET}

  5. Umgebung aktivieren:
     {C.CYAN}.venv\\Scripts\\activate{C.RESET}   (Windows)
     {C.CYAN}source .venv/bin/activate{C.RESET}  (Mac/Linux)

  6. Dependencies + Projektpaket installieren:
     {C.CYAN}uv pip install -e ".[{project_type.lower()}]"{C.RESET}

  7. Jupyter Kernel registrieren:
     {C.CYAN}python -m ipykernel install --user --name {project_slug} --display-name "Python ({project_slug})"{C.RESET}

  8. Notebook öffnen:
     {C.CYAN}notebooks/00_introduction.ipynb{C.RESET}
     → Oben rechts Kernel wählen: "{project_slug}"

  Viel Erfolg! 🚀
""")


if __name__ == "__main__":
    main()
