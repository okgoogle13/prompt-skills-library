---
model: perplexity-search
vendor: Perplexity
family: Perplexity
aliases: [perplexity, perplexity-standard, perplexity-standard-search, sonar, sonar-pro, perplexity-sonar, pplx-search]
last_verified: 2026-11-07
status: current
---

# Perplexity Standard Search (Sonar / Agent API, niedriger Effort)

> ⚠ Die Perplexity-Doku wurde nur über Websuche-Zusammenfassungen geprüft, nicht direkt abgerufen. Parameternamen (`effort`, `reasoning.effort`, `search_mode`, `search_domain_filter`, `search_recency_filter`) vor Einsatz gegen die aktuelle Doku verifizieren (unbelegt). Laut Recherche löst die Agent API die älteren Sonar-Chat-Completions-Modelle ab.

## Reasoning / Thinking
- Standardsuche = schnelles, live belegtes Web-Grounding mit Inline-Zitaten; Legacy-Modelle `sonar`, `sonar-pro`.
- Agent API: `effort` bündelt Modell, Suche, Tools und Schrittgrenzen: `fast` (Einzelfakt, Definitionen), `low` (Alltagsrecherche, leichte Mehrschritt-Suche), `medium` (Allzweck-Default). Standardsuche entspricht `fast`–`medium`.
- Davon getrennt: `reasoning.effort` steuert interne Denktiefe (providerabhängig, unbelegt).

## Prompting-Stil
- **Kurz, atomar, spezifisch**: Der `input` seedet die erste Suchanfrage. Schwach: „Erzähl mir etwas über Apples Umsatz“; besser: „Apple FY2025 10-K Umsatz nach Segmenten“.
- **Eine Frage pro Request**; mehrteilige Aufträge in separate Requests teilen. Überladene Mehrfach-Anweisungen führen auf niedrigem Effort zu verwirrten Suchpfaden.
- `instructions` (System-Ebene) für Rolle, Format, Sprache und Grundierungsregeln; eigene `instructions` **ersetzen** das Standard-System-Prompt des Effort-Levels.
- **Anti-Halluzination**: ausdrücklich erlauben zu antworten „keine ausreichenden Belege gefunden“.
- **Zitate nicht per Prosa erzwingen**: native Zitatformate nicht bekämpfen; Domänenvorgaben über `search_domain_filter`, Zeitbezug über `search_recency_filter` (z. B. `week`, `month`) statt nur „aktuell“ im Text.
- `search_mode`: `web` (Default), `academic`, `sec`.
- Kein Few-Shot/CoT nötig; Prompt-Text soll Suchbegriffe enthalten, nicht Anweisungen zum Suchen.

## Stärken & Schwächen (prompt-relevant)
- Stärken: Geschwindigkeit, aktuelle Quellen, Inline-Zitate.
- Schwächen: flache Analyse bei komplexen Fragen; bei vagen Prompts schlechte Treffer; keine tiefe Multi-Source-Synthese (dafür `perplexity-deep-research`).

## Output- & Format-Konventionen
- Antwort mit Zitaten/Quellenliste; Format (Liste, Tabelle, kurze Absätze) in `instructions` festlegen.
- Strukturierte Ausgaben: Verfügbarkeit je Modell prüfen (unbelegt).

## Migrations-Hinweise
- **VON Perplexity Search weg**: Suchfilter-Parameter in Tool-/Retrieval-Konfiguration des Ziels übersetzen; Hinweis „nur belegte Fakten“ behalten; wenn das Ziel keine Websuche hat, Such-Tool oder Kontext ergänzen.
- **ZU Perplexity Search migrieren**: Prompt auf eine konkrete, suchbegriffsreiche Frage kürzen; CoT/Rollenspiel streichen; Quellen-/Zeitvorgaben in Filter-Parameter verlagern; „kein Beleg gefunden“-Klausel ergänzen; Format in `instructions`.

## Quellen
- https://docs.perplexity.ai — Agent API, Effort-Level `fast/low/medium`, `instructions` vs. `input`, Prompt-Hinweise (per Websuche zusammengefasst).
