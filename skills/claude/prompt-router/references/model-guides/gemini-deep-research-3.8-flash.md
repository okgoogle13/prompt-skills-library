---
model: gemini-deep-research-3.8-flash
vendor: Google
family: Gemini
aliases: [deep-research-3.8-flash, gemini-dr-flash, flash-deep-research, gemini-3.8-flash-deep-research, deep-research-flash]
last_verified: 2026-11-07
status: current
---

# Gemini Deep Research (3.8 Flash)

> ⚠ Einordnung: Deep Research ist ein **Agent** der Interactions API, kein Modellname. Eine dokumentierte Bindung „Deep Research läuft auf `gemini-3.8-flash`“ konnte **nicht** belegt werden (unbelegt). Dieser Guide beschreibt den Agenten und die Prompt-Anpassungen für ein schnelleres/günstigeres Setup mit Gemini 3.8 Flash als Hilfsmodell (Planung, Zusammenfassung, Nachbearbeitung). Vor Produktiveinsatz in der Doku prüfen.

## Reasoning / Thinking
- Agent: asynchron per `client.interactions.create(agent=..., input=..., background=True)`, Polling über `client.interactions.get(id)`; Ergebnis in `outputs[-1].text`. Für den schnellen Lauf ist `deep-research-preview-04-2026` die naheliegende Wahl (laut Recherche auf Geschwindigkeit/Effizienz getrimmt); `deep-research-max-preview-04-2026` für maximale Gründlichkeit.
- Gemini 3.8 Flash als Hilfsmodell: `thinking_level` `low | medium (Default) | high`; `minimal` wirft Fehler; `thinking_budget` nicht zusammen mit `thinking_level`. `low` für Extraktion/Zusammenfassung des Berichts, `medium`/`high` für Quellenabgleich und Tool-Schleifen.
- Thought Signatures bei Function Calling zurückreichen (sonst 400), oder `previous_interaction_id` nutzen.

## Prompting-Stil
- Wie beim Argon-Setup: Leitfrage, Umfang, Gliederung, Quellenregeln; Collaborative Planning optional.
- Für Flash: **kürzere, atomare Aufträge**; große Rechercheaufgaben in Teilfragen zerlegen und parallel starten statt einem Mammutauftrag (Empfehlung abgeleitet, unbelegt).
- Kein handgeschriebenes Chain-of-Thought; Anweisungen direkt und knapp.
- `temperature` bei 1.0 belassen, `top_p`/`top_k` entfernen, kein Prefill, `candidate_count` entfernen.
- Tonalität nüchtern; ausführlichere Berichte explizit anfordern.

## Stärken & Schwächen (prompt-relevant)
- Stärken: niedrige Kosten und Latenz ($0.75 In / $3.75 Out pro 1M Tokens bis 31.12.2026, danach $1.50 / $7.50), 1.048.576 Kontext, 65.536 Output, gute agentische Tool-Nutzung.
- Schwächen: geringere Denktiefe als Argon bei sehr harten Syntheseaufgaben (Einschätzung, unbelegt); Agent-Bindung nicht belegt; Preview-Agent-IDs.

## Output- & Format-Konventionen
- Markdown-Bericht mit Quellen; Structured Outputs für die Nachbearbeitung (Zusammenfassung, Tabellen) mit `response_schema`.

## Migrations-Hinweise
- **VON Deep Research (3.8 Flash) weg**: Hintergrund-Polling und Agent-ID entfernen; Rechercheschritte, Such-Tool und Quellenregeln explizit in den Zielprompt schreiben; `thinking_level` auf Effort/Budget des Ziels mappen.
- **ZU Deep Research (3.8 Flash) migrieren**: Prompt auf Ziel, Umfang, Gliederung und Quellenregeln kürzen; CoT/„suche zuerst“-Scaffolding streichen; `background=True` und Polling einbauen; Sampling-Parameter/Prefill entfernen; bei komplexen Themen auf `deep-research-max-…` oder Argon-Nachprüfung eskalieren.

## Quellen
- https://ai.google.dev/gemini-api/docs/deep-research — Agent-IDs, Interactions API, Hintergrundmodus (per Websuche zusammengefasst).
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash — siehe Guide `gemini-3.8-flash`.
