"""
docs_files.py
-------------
Dokumentations-Dateien:
  - docs/project_decision_log.md  → Entscheidungs-Tagebuch

📝 ANPASSEN: Füge weitere Docs-Dateien hinzu.
"""


def get_files(project_name: str, project_type: str = "DSC") -> list[tuple[str, str]]:
    if project_type.upper() == "DAN":
        # DAN: decision_log liegt in notebooks/ (kein docs/ Ordner)
        return [
            ("notebooks/project_decision_log.md", _decision_log(project_name)),
            ("reports/index.html", _report_index(project_name)),
        ]
    return [
        ("docs/project_decision_log.md", _decision_log(project_name)),
        ("reports/index.html", _report_index(project_name)),
    ]


def _decision_log(project_name: str) -> str:
    return f"""\
# Project Decision Log – {project_name}

> Hier dokumentierst du alle wichtigen Entscheidungen im Projekt.
> Das hilft dir später (und anderen), nachzuvollziehen, WARUM etwas so gebaut wurde.

## Wie du dieses Log verwendest

| Feld | Beschreibung |
|------|-------------|
| **Datum** | Wann wurde die Entscheidung getroffen? |
| **Kontext** | Was war die Situation / das Problem? |
| **Entscheidung** | Was wurde entschieden? |
| **Alternativen** | Was wurde abgelehnt und warum? |
| **Konsequenzen** | Was folgt daraus? Was muss geändert werden? |

---

## Entscheidungen

### [DATUM] – Projektstartup

- **Kontext:** Projekt aufgesetzt mit dem DAN/DSC Scaffolding Generator.
- **Entscheidung:** Projektstruktur basierend auf Cookiecutter Data Science Template.
- **Alternativen:** Manuelle Struktur, keine Standardisierung.
- **Konsequenzen:** Einheitliche Struktur, leichtere Zusammenarbeit.

---

### [DATUM] – [Titel der Entscheidung]

- **Kontext:** _..._
- **Entscheidung:** _..._
- **Alternativen:** _..._
- **Konsequenzen:** _..._

---
"""


def _report_index(project_name: str) -> str:
    return f"""\
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} – Executive Summary</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px;
               margin: 40px auto; padding: 0 20px; color: #333; }}
        h1   {{ color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 8px; }}
        h2   {{ color: #555; margin-top: 32px; }}
        .placeholder {{ background: #f5f5f5; border-left: 4px solid #2E86AB;
                        padding: 12px 16px; margin: 16px 0; border-radius: 0 4px 4px 0; }}
    </style>
</head>
<body>
    <h1>{project_name}</h1>
    <p><em>Executive Summary Report – generiert aus reports/</em></p>

    <h2>🎯 Problem Statement</h2>
    <div class="placeholder">Platzhalter – hier das Business-Problem beschreiben.</div>

    <h2>📊 Key Findings</h2>
    <div class="placeholder">Platzhalter – die 3 wichtigsten Erkenntnisse.</div>

    <h2>📈 Ergebnisse</h2>
    <div class="placeholder">Platzhalter – Metriken, Modell-Performance oder Analyse-Resultate.</div>

    <h2>📋 Empfehlungen</h2>
    <div class="placeholder">Platzhalter – konkrete nächste Schritte.</div>

    <h2>🖼️ Visualisierungen</h2>
    <div class="placeholder">Platzhalter – Plots aus reports/figures/ hier einbinden.</div>
</body>
</html>
"""
