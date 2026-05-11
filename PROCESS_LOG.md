# PROCESS_LOG.md – wgnd-scaffolding

> Projektverlauf und AI-Kontext-Einstieg.
> Dieses File ist der Einstiegspunkt für neue Claude-Sessions.

---

## Projekt-Übersicht

| Feld | Inhalt |
| :--- | :--- |
| Projektname | wgnd-scaffolding |
| Zweck | Projektstruktur-Generator für DAN/DSC/DE Projekte |
| Status | 🟢 stabil, einsatzbereit |
| Nächster Schritt | Backlog #7/#8 — neue Projekttypen DE und DANSC |

---

## Verlauf

### 2026-05-11 – Grundlegende Überarbeitung (Session mit Kay)

**Naming Convention neu definiert:**
- `--slug` ist jetzt Pflichtfeld (war: optional, wurde aus `--name` abgeleitet)
- `--name` ist optional — nur für Docs/README, fällt auf Slug zurück
- `package_name` = Slug mit Bindestrichen → Unterstrichen (z.B. `zh_tram_flow`) — für `src/`-Ordner und Python-Imports
- Projektordner = Slug direkt (kein Typ-Prefix mehr — `dan_`, `dsc_` entfernt)

**Bugs gefixt:**
- Slug-Validierung ließ keine Bindestriche zu → jetzt erlaubt
- Ordnername wurde aus `--name` statt `--slug` abgeleitet → auf Slug umgestellt
- `src/<slug>/` hatte Bindestriche → nicht importierbar, jetzt `src/<package_name>/`
- Python-Imports in generierter README verwendeten Slug statt package_name → gefixt

**Neue Features:**
- `PROCESS_LOG.md`, `ROADMAP.md`, `CLAUDE.md` werden automatisch im neuen Projekt erstellt
- `project_decision_log.md` entfernt — wird durch `PROCESS_LOG.md` ersetzt

**Repo-Naming Convention dokumentiert:**
- `wgnd-` für eigene Tools
- `sf_` für StackFuel-Kontext
- Kein Typ-Prefix für Portfolio-Projekte — Topic ist der Name
- Hyphens sind Standard (GitHub-Konvention)

---
