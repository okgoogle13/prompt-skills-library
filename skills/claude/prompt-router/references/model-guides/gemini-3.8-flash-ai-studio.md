---
model: gemini-3.8-flash-ai-studio
vendor: Google
family: Gemini
aliases: [gemini-3.8-flash-studio, ai-studio-flash, ai-studio-gemini-3.8-flash, gemini-3.8-ai-studio, flash-ai-studio, aistudio-flash]
last_verified: 2026-11-07
status: current
---

# Gemini 3.8 Flash in Google AI Studio

> ⚠ Einordnung: Modell ist `gemini-3.8-flash` (siehe Guide `gemini-3.8-flash`); dieser Guide betrifft nur die **AI-Studio-Oberfläche** (Playground, Run Settings, „Get code“). Die UI-Details stammen aus Websuche-Zusammenfassungen, nicht aus direkt abgerufener Doku; Bezeichnungen und Defaults der UI können sich ändern (unbelegt). Standard-Defaults im Studio vor Übernahme in Prompts/Code prüfen.

## Reasoning / Thinking
- Run Settings enthalten **Thinking level** mit `low | medium | high`; `minimal` nicht unterstützt (Fehler). Der Default im Studio wird je Quelle als `medium` oder `high` genannt (unbelegt) — API-Default laut Modell-Guide ist `medium`; Level im Studio explizit setzen, damit Studio und Code übereinstimmen.
- Thinking-Tokens werden als Output-Tokens abgerechnet; `low` für einfache Textaufgaben senkt Latenz und Kosten.
- Max-Output-Tokens deckelt Thinking + Antwort gemeinsam; zu niedrig gesetzte Werte können die Antwort abschneiden (Empfehlung ≥ 32.768, Modell-Limit 65.536).

## Prompting-Stil
- **System Instructions** (eigenes Feld) für Rolle, Format, Ton und Grenzen; Aufgabe/Daten in den User-Turn. Kurze, direkte, strukturierte Regeln; keine CoT-Scaffolds („Denke Schritt für Schritt“).
- Bei langen Daten: Referenzmaterial zuerst, Frage/Aufgabe ans Ende nach dem Datenblock.
- **Temperature**: AI Studio erlaubt `0.0–2.0` (UI-Schieberegler). Für Gemini-3-Modelle empfiehlt Google **1.0 beizubehalten**; niedrigere Werte können Loops/Qualitätsverlust auslösen. Beispiele im Netz mit `0.2` sind generisch, nicht Google-Empfehlung für 3.8 Flash.
- Kein Assistant-Prefill: „Prefill“ im Studio-Chat nicht als Formatsteuerung nutzen; Format über System Instructions oder **Structured Output** erzwingen.
- Tonalität nüchtern-knapp; ausführlichere Antworten explizit anfordern.
- `top_p`/`top_k` nicht verstellen.

## Stärken & Schwächen (prompt-relevant)
- Stärken: schnelles Prototyping, Run Settings (Thinking, Temperature, Structured Output, Grounding), „Get code“ erzeugt `google-genai`-Code mit `GenerateContentConfig`.
- Schwächen: Studio-Chat ist kein Produktions-Setup: Studio-Defaults und Session-State können vom API-Default abweichen; Thought Signatures/Multi-Turn mit Function Calling im eigenen Code selbst handhaben bzw. `previous_interaction_id` nutzen; Free-/Paid-Tier-Limits und Preise unterscheiden sich (Preise siehe Modell-Guide, unbelegt für Studio-Free-Tier).

## Output- & Format-Konventionen
- **Structured Output** im Run-Settings-Panel: JSON-Schema eingeben bzw. generieren; garantiert schemakonforme Antworten für Parsing.
- **Grounding with Google Search** im Panel zuschaltbar (Quellen/Citations); zusätzlich URL Context und Code Execution unter Tools (Verfügbarkeit im UI unbelegt).
- Multimodale Eingaben (Text, Bild, Video, Audio, PDF) per Upload; `media_resolution` für dichte Dokumente (`high`) prüfen.
- Einstellungen vor Übernahme mit **Get code** in Python/JS-Code übersetzen lassen und gegen den Prompt prüfen.

## Migrations-Hinweise
- **VON AI Studio (3.8 Flash) weg**: Run-Settings in Parameter des Zielsystems überführen (Thinking level → Effort/Budget, System Instructions → System-Prompt, Structured Output → Schema-/JSON-Modus des Ziels); Studio-spezifische Defaults nicht annehmen; Prefill ggf. wieder verfügbar.
- **ZU AI Studio (3.8 Flash) migrieren**: Prompt aufteilen in System Instructions (stabile Regeln) und User-Turn (Aufgabe/Daten); CoT streichen; Thinking level explizit setzen; Temperature auf 1.0 lassen; `top_p`/`top_k`/`candidate_count`/Prefill entfernen; Format über Structured Output; nach Test per **Get code** exportieren.

## Quellen
- https://aistudio.google.com — Run Settings, Thinking level, System Instructions, Structured Output, Grounding (per Websuche zusammengefasst, nicht direkt abgerufen).
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash — Modellkarte (siehe Guide `gemini-3.8-flash`).
