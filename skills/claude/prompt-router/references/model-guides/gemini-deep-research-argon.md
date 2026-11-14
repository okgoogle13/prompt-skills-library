---
model: gemini-deep-research-argon
vendor: Google
family: Gemini
aliases: [deep-research-argon, gemini-dr-argon, argon-deep-research, gemini-argon-deep-research]
last_verified: 2026-11-07
status: current
---

# Gemini Deep Research (Argon)

> ⚠ Einordnung: Deep Research ist ein **Agent** der Interactions API, kein Modellname. Eine dokumentierte Bindung „Deep Research läuft auf `gemini-4-argon`“ konnte **nicht** belegt werden (unbelegt). Dieser Guide beschreibt (a) den Deep-Research-Agenten und (b) wie ein Prompt zu formulieren ist, wenn Argon als Planer/Synthese-Modell gewählt oder der Agent mit Argon-Ergebnissen weiterverarbeitet wird. Vor Produktiveinsatz in AI Studio / Doku prüfen.

## Reasoning / Thinking
- Der Deep-Research-Agent plant selbstständig Teilfragen, führt iterativ viele Suchen aus, liest Quellen und synthetisiert einen zitierten Bericht. `thinking_level` wird für den Agenten nicht gesetzt (nicht dokumentiert, unbelegt).
- Für Argon selbst (Folgeverarbeitung, Review des Berichts): `thinking_level` `low | medium | high`, Default `medium`, `minimal` ungültig; `max_output_tokens` ≥ 32.768 (siehe Guide `gemini-4-argon`).
- Läuft **asynchron**: `client.interactions.create(agent=..., input=..., background=True)`, danach Status per `client.interactions.get(id)` pollen (`completed` / `failed`); Ergebnis in `outputs[-1].text`. Synchrones `generateContent` ist nicht der Weg.
- Agent-IDs laut Recherche: `deep-research-preview-04-2026` (schnell/effizient, UI-Streaming) und `deep-research-max-preview-04-2026` (maximale Gründlichkeit). Ein älteres Beispiel nennt `deep-research-pro-preview-12-2025`. IDs sind Preview und können wechseln — gegen die aktuelle Doku prüfen.

## Prompting-Stil
- **Forschungsauftrag, kein Chat**: Ziel, Leitfrage, Umfang (Zeitraum, Region, Branche), gewünschte Berichtsgliederung und Quellenanforderungen in einem Prompt. Gliederung explizit vorgeben (z. B. „1. Marktlage, 2. Preismodelle, 3. Änderungen der letzten 6 Monate“).
- **Collaborative Planning**: `collaborative_planning=True` liefert zuerst einen Forschungsplan zur Freigabe; Korrekturen per `previous_interaction_id` zurückspielen (Parametername laut Recherche, vor Einsatz verifizieren).
- Kein manuelles „Think step by step“; der Agent plant selbst. Konkrete, eng umrissene Fragen statt vager Themen.
- Eigene Dokumente/PDFs können als multimodaler Input beigelegt werden; Aufgabe/Fragen ans Ende nach den Referenzdaten.
- Standard-Ton ist sachlich-knapp; Ausführlichkeit/Leserschaft explizit nennen.
- Unsicherheit zulassen: ausdrücklich erlauben, „nicht belegbar“ zu schreiben statt zu raten.

## Stärken & Schwächen (prompt-relevant)
- Stärken: mehrstufige Recherche mit Dutzenden Suchschritten, zitierte strukturierte Berichte, interaktive Planfreigabe.
- Schwächen: Laufzeit mehrere Minuten; Preview-Status; Bindung an Argon/3.8 Flash nicht belegt; Kosten/Token schwer vorab abschätzbar (unbelegt).

## Output- & Format-Konventionen
- Ausgabe: Markdown-Bericht mit Quellenangaben als Text im letzten Output.
- Kein Prefill, keine Sampling-Parameter (`temperature`, `top_p`, `top_k`, `candidate_count` entfernen).

## Migrations-Hinweise
- **VON Deep Research (Argon) weg**: Hintergrund-/Polling-Logik und `collaborative_planning` entfernen; Zielsystem ohne Agenten braucht explizite Rechercheschritte, Such-Tool und Quellenregeln im Prompt; Gliederung bleibt als Ausgabevertrag erhalten.
- **ZU Deep Research (Argon) migrieren**: Prompt auf Leitfrage + Umfang + Gliederung + Quellenregeln reduzieren; CoT- und Tool-Anweisungen („suche zuerst …“) streichen; asynchronen Aufruf (`background=True`) verwenden; optional Plan-Freigabe einbauen; Ergebnis nach Bedarf mit `gemini-4-argon` (`thinking_level: high`) nachprüfen.

## Quellen
- https://ai.google.dev/gemini-api/docs/deep-research — Deep-Research-Agent, Interactions API, `background=True`, Polling, Agent-IDs, Collaborative Planning (per Websuche zusammengefasst, nicht direkt abgerufen).
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — Argon-Modellkarte (siehe Guide `gemini-4-argon`).
