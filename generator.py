#!/usr/bin/env python3
"""
generator.py
============
DA / DS Project Scaffolding Generator

Verwendung:
    python generator.py --name "Mein Projekt" --path "C:/Projects" --type DS
    python generator.py --name "Restaurant Analysis" --path "./projects" --type DA

Argumente:
    --name      Projektname (z.B. "Restaurant Analysis Q3 2024")
    --slug      [optional] URL-sicherer Bezeichner (z.B. "restaurant_analysis")
                Wenn weggelassen, wird automatisch aus --name abgeleitet.
    --path      Übergeordnetes Verzeichnis, IN dem das Projekt erstellt wird
    --type      Projekttyp: DS (Data Science) oder DA (Data Analysis)

Beispiele:
    # DS-Projekt im aktuellen Verzeichnis
    python generator.py --name "House Price Prediction" --path "." --type DS

    # DA-Projekt in einem bestimmten Ordner, mit eigenem Slug
    python generator.py --name "Market Analysis 2024" --slug "market_2024" \\
                        --path "C:/Users/dein_name/Projects" --type DA
"""

import argparse
import re
import subprocess
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
from templates.notebooks_ds   import get_notebooks as get_notebooks_ds, get_notebook_index as get_index_ds
from templates.notebooks_da   import get_notebooks as get_notebooks_da, get_notebook_index as get_index_da


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

    Beispiel: "DA Telefonica Churn"   -> "DA_Telefonica_Churn"
              "DA_Telefonica-Churn"   -> "DA_Telefonica-Churn"
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
            "DA / DS Project Scaffolding Generator\n"
            "Erstellt eine vollständige Projektstruktur für Data Science / Analysis."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Beispiele:\n"
            "  python generator.py --slug zh-tram-flow --path . --type DA\n"
            "  python generator.py --slug house-price --name \"House Price Prediction\" --path ../projects --type DS\n"
        ),
    )
    parser.add_argument(
        "--slug", "-s",
        required=True,
        help="Technischer Projektbezeichner — wird Ordnername und Paketname (z.B. 'zh-tram-flow'). "
             "Erlaubt: Kleinbuchstaben, Ziffern, Unterstriche, Bindestriche.",
    )
    parser.add_argument(
        "--name", "-n",
        default=None,
        help="[optional] Lesbarer Projektname für Docs und README (z.B. 'Zürich Tram Flow'). "
             "Fällt auf --slug zurück wenn nicht angegeben.",
    )
    parser.add_argument(
        "--path", "-p",
        required=True,
        help="Übergeordnetes Verzeichnis, IN dem das Projekt erstellt wird",
    )
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["DS", "DA", "ds", "da"],
        help="Projekttyp: DS (Data Science) oder DA (Data Analysis)",
    )
    return parser


# ─── Hauptfunktion ─────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    project_slug = args.slug.strip()
    project_name = args.name.strip() if args.name else project_slug
    project_type = args.type.upper()
    parent_dir   = Path(args.path).expanduser().resolve()

    # Slug validieren — Bindestriche erlaubt (z.B. zh-tram-flow)
    if not re.match(r"^[a-z_][a-z0-9_-]*$", project_slug):
        err(f"Ungültiger Slug: '{project_slug}'")
        err("Nur Kleinbuchstaben, Ziffern, Unterstriche und Bindestriche erlaubt. Darf nicht mit Ziffer beginnen.")
        sys.exit(1)

    # package_name: Python-importierbarer Name (Bindestriche → Unterstriche)
    package_name = project_slug.replace("-", "_")
    # folder_name: Projektordner = slug (kein Typ-Prefix)
    folder_name  = project_slug
    project_dir  = parent_dir / folder_name

    # ── Header ausgeben ────────────────────────────────────────────────────
    head("DA/DS Scaffolding Generator")
    sep()
    info(f"Projektname : {project_name}")
    info(f"Slug        : {project_slug}")
    info(f"Paket       : {package_name}  (src/{package_name}/)")
    info(f"Ordner      : {folder_name}")
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
    folders = get_folders(package_name, project_type)
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
    root_files = get_root_files(project_name, project_slug, project_type, package_name)
    for rel_path, content in root_files:
        try:
            write_file(project_dir, rel_path, content)
        except Exception as e:
            errors.append(f"Root '{rel_path}': {e}")
            err(f"Fehler bei '{rel_path}': {e}")

    # ── 3. README.md ──────────────────────────────────────────────────────
    head("3/5  README.md")
    try:
        nb_index = get_index_ds() if project_type == "DS" else get_index_da()
        readme_content = get_readme(project_name, project_slug, project_type, package_name, nb_index)
        write_file(project_dir, "README.md", readme_content)
    except Exception as e:
        errors.append(f"README.md: {e}")
        err(f"Fehler bei README.md: {e}")

    # ── 4. Source-Dateien ─────────────────────────────────────────────────
    head("4/5  Source-Dateien (src/ · configs/ · tests/ · docs/)")
    all_source_files = (
        get_src_files(project_name, package_name, project_type)
        + get_config_files(project_name, project_slug, project_type)
        + get_test_files(package_name, project_type)
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
    if project_type == "DS":
        notebooks = get_notebooks_ds(project_name, project_slug)
    else:
        notebooks = get_notebooks_da(project_name, project_slug)

    for rel_path, content in notebooks:
        try:
            write_file(project_dir, rel_path, content)
        except Exception as e:
            errors.append(f"Notebook '{rel_path}': {e}")
            err(f"Fehler bei '{rel_path}': {e}")

    # ── Git-Repository ──────────────────────────────────────────────────────
    head("Git-Repository")
    if (project_dir / ".git").exists():
        info("Bereits ein Git-Repository — kein init nötig.")
    else:
        try:
            subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "chore: init project scaffold"],
                cwd=project_dir, check=True, capture_output=True,
            )
            ok("git init + Erstcommit")
        except FileNotFoundError:
            warn("git nicht gefunden — Repository manuell initialisieren.")
        except subprocess.CalledProcessError as e:
            errors.append(f"git init: {e}")
            err(f"Git-Init fehlgeschlagen: {e.stderr.decode(errors='replace') if e.stderr else e}")

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
     {C.CYAN}python -m ipykernel install --user --name {package_name} --display-name "Python ({package_name})"{C.RESET}

  8. Notebook öffnen:
     {C.CYAN}notebooks/00_introduction.ipynb{C.RESET}
     → Oben rechts Kernel wählen: "{package_name}"

  Viel Erfolg! 🚀
""")


if __name__ == "__main__":
    main()
