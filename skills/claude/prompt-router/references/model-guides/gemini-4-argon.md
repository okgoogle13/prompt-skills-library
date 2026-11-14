---
model: gemini-4-argon
vendor: Google
family: Gemini
aliases: [gemini-4, argon, gemini-argon, gemini4, gemini4-argon, 4-argon, argan]
last_verified: 2026-11-05
status: current
---

# Gemini 4 Argon

## Reasoning / Thinking
- Typ: **Natives Reasoning, immer aktiv**. Tiefe ausschließlich über das String-Enum `thinking_level` steuerbar (`low | medium | high`), **Default `medium`**. `minimal` wird nicht unterstützt und wirft einen Fehler.
- `thinking_budget` (Token-Budget) wird auf Gemini 4 Argon nicht mehr unterstützt und darf nicht übergeben werden. Die Stufen sind relative Allowances für die Überlegungstiefe, keine strikten Token-Garantien.
- Empfohlene Stufenwahl laut Doku:
  - `low`: Geringste Latenz und Tokenverbrauch; geeignet für einfachere Aufgaben, Textanalyse und leichte Recherche. Bei harten Coding- oder Reasoning-Aufgaben kann die Qualität abfallen.
  - `medium` (Default): Ausgewogen; Standardempfehlung für fast alle produktiven Workloads inkl. komplexem Software Engineering und agentischen Pipelines.
  - `high`: Maximale Denktiefe für schwierige Mathematik, Naturwissenschaften, komplexe Architektur-Refactorings und autonome Multi-Step-Agenten.
- **`max_output_tokens` als harte Obergrenze**: `max_output_tokens` begrenzt die **Summe** aus generierten Thinking-Tokens und tatsächlichem Output. Wird der Wert zu niedrig angesetzt (z. B. < 32k), kann das Modell das gesamte Kontingent im Reasoning aufbrauchen und die Antwort vorzeitig abbrechen. Google empfiehlt mindestens 32.768 Tokens (Standard synchronous: 65.536).
- **Long Decode**: Für Antworten jenseits von 64k Tokens unterstützt Gemini 4 Argon Long Decode bis zu 1.048.576 Tokens (minus Input). Dies erfordert `background: true` und `max_output_tokens > 65536`. Die Fortsetzungs-Hops (in Schritten von bis zu 64k) werden serverseitig orchestriert; im Interaction-Objekt müssen die Textinhalte aller `model_output`-Steps aneinandergehängt werden.
- **Thought Signatures & State-Management**: Bei mehrstufigen Konversationen und Tool-Calls wird der verschlüsselte Reasoning-Kontext über Thought Signatures transportiert. Empfohlener Standard ist die serverseitige Zustandsverwaltung via `previous_interaction_id` der Interactions API (`store=true`). Bei zustandslosen Requests müssen alle generierten Thought-Blöcke unverändert in der Konversationshistorie mitgeführt werden.
- Abrechnung: Berechnet wird die Gesamtsumme aus Ausgabe- und Denk-Tokens ($10 bzw. $20 pro 1M Tokens).

## Prompting-Stil
- **Direkt, präzise und schlank**: „Be concise. Gemini responds best to direct, clear instructions." Aufwändiges Prompt-Engineering für ältere Nicht-Reasoning-Modelle (wie manuelles „Think step by step" oder verschachtelte CoT-Schablonen) führt laut Doku dazu, dass das Modell überanalysiert („over-analyze") und sollte restlos entfernt werden.
- **Standard-Tonalität ist nüchtern**: Das Modell antwortet standardmäßig kompakt und sachlich. Wenn ausführliche, didaktische oder konversationelle Antworten erwünscht sind, muss dieser Stil explizit im Prompt angefordert werden.
- **Long-Context-Struktur**: Bei großen Datenmengen (Dokumente, Codebases, Tabellen) die Referenzdaten **an den Anfang** und die konkrete Aufgabe/Instruktion ans **Ende nach dem Datenblock** stellen, eingeleitet durch eindeutige Anker („Basierend auf den vorstehenden Informationen...").
- **Keine Sampling-Parameter**: `temperature`, `top_p` und `top_k` vollständig aus den Generation-Configs entfernen. Werden sie übergeben, ignoriert die API sie; manuelle Eingriffe unter 1.0 können bei anspruchsvollen Reasoning- und Matheaufgaben Looping auslösen.
- **Kein Assistant-Prefill**: Vorgefüllte Modellantworten (`prefilled model turns`) entfernen. Struktur und Formatierung stattdessen über System-Instructions oder `response_schema` (Structured Outputs) durchsetzen.
- **Agentischer Scope**: Bei komplexen oder offenen Aufgabenstellungen klare Abbruchkriterien, maximale Iterationsgrenzen und Handlungsspielräume definieren, um unkontrolliertes Weiteriterieren im Reasoning zu vermeiden.

## Stärken & Schwächen (prompt-relevant)
- **Stärken**: Googles Flaggschiff-Reasoning-Modell für High-End-Softwareentwicklung, autonome Multi-Step-Agenten, tiefgehende mathematische und wissenschaftliche Problemlösung sowie anspruchsvolle Enterprise-Wissensarbeit (Finanzanalysen, juristisches Drafting). Generelle Verfügbarkeit (GA) seit 13. Oktober 2026. Bietet Long Decode bis zu 1 Mio. Output-Tokens, Agentic Video Understanding (dynamische Frame-Analyse) und native Integration in Antigravity Managed Agents.
- **Schwächen & Eigenheiten**:
  - **Kein explizites Context Caching**: Das traditionelle explizite Caching (`cachedContents` / `caches.create`) wird nicht mehr unterstützt. Stattdessen greift automatisches, implizites Caching (ab 4.096 Tokens) mit 95 % Rabatt auf Treffer.
  - **Latenz bei tiefem Reasoning**: Komplexe Denkprozesse auf Stufe `high` oder Long-Decode-Aufgaben können mehrere Minuten dauern. HTTP-Client-Timeouts müssen auf mindestens 15 Minuten angehoben werden, oder es muss auf `background: true` ausgewichen werden.
  - **Hoher Tokenverbrauch**: Durch langes Nachdenken können signifikant mehr Tokens anfallen als bei Flash-Modellen; für einfache Extraktions- und Klassifikationsaufgaben ist `gemini-3.8-flash` oder `thinking_level: "low"` wirtschaftlicher.
  - **Fehlende Modalitäten**: Keine native Bildgenerierung, keine Audiogenerierung, keine Live API (WebSockets).
  - **Knowledge Cutoff**: März 2026 (mit einzelnen Domänen bis Januar 2025). Zeitkritische Daten müssen über Google Search Grounding oder den Kontext bereitgestellt werden.

## Output- & Format-Konventionen
- Unified Context Window: **1.048.576 Tokens** (geteilt zwischen Input, Thinking und Output).
- Maximale Ausgabetoken: 65.536 Tokens synchron; bis zu 1.048.576 Tokens (abzüglich Input-Tokens) im asynchronen Long-Decode-Modus (`background: true`).
- Input-Modalitäten: Text, Bild, Video (mit Agentic Video Understanding), Audio, PDF. Output: Nur Text.
- Unterstützte Features: Structured Outputs (auch in Kombination mit Built-in Tools wie Google Search, Maps Grounding, URL Context und Code Execution), Function Calling, Implizites Caching (ab 4k Tokens, 95 % Rabatt), Batch API (50 % Rabatt), Computer Use, File Search, Flex- und Priority-Inference.
- Preise (pro 1M Tokens):
  - Bis 30.11.2026 (Einführungspreis): Input $2.00 (Cached $0.10), Output $10.00.
  - Ab 01.12.2026 (Regulär): Input $4.00 (Cached $0.20), Output $20.00.
  - Kein Free Tier verfügbar.

## Migrations-Hinweise
- **VON gemini-4-argon weg**:
  - `thinking_level` in den Effort- oder Budget-Parameter des Zielmodells überführen (`reasoning_effort` bei OpenAI/o3/GPT-5, `budget_tokens` bzw. adaptiven `effort` bei Claude Sonnet/Opus); falls das Zielmodell kein natives Reasoning besitzt, wieder explizites Chain-of-Thought-Scaffolding („Schritt für Schritt") im Prompt ergänzen.
  - Sampling-Parameter (`temperature`, `top_p`) wieder in die Request-Config einfügen.
  - Server-seitigen Session-State (`previous_interaction_id`) auflösen und Konversationshistorie client-seitig verwalten.
  - Long-Decode-Annahmen über 64k Tokens Output auf die Ausgabelimits des Zielmodells zurückstutzen (häufig 4k, 8k, 16k oder 64k).
  - Automatisches Caching auf die providerspezifische Caching-API umstellen (z. B. Anthropic Cache-Control-Header).
- **ZU gemini-4-argon migrieren**:
  - Modell-ID auf `gemini-4-argon` setzen.
  - `thinking_level` konfigurieren (`low | medium | high`; Default ist `medium`; `minimal` von älteren Flash-Modellen zwingend auf `low` anheben).
  - `max_output_tokens` überprüfen und auf mindestens 32.768 erhöhen (oder Default 65.536 belassen), damit Reasoning den eigentlichen Output nicht abschneidet; für extrem lange Ausgaben `background: true` mit Werten > 65.536 nutzen.
  - Manuelle CoT-Anweisungen („Denke Schritt für Schritt", „Reflektiere ausführlich") und verbose Scaffolding aus dem Prompt streichen und stattdessen `thinking_level: "high"` wählen.
  - Explizites Caching (`caches.create`) aus dem Code entfernen — Implizites Caching greift automatisch ab 4.096 Tokens.
  - `temperature`, `top_p`, `top_k`, `candidate_count` und Prefill-Turns restlos aus Requests entfernen.
  - Client-Timeouts auf mindestens 15 Minuten anheben oder asynchrone Background-Execution nutzen.
  - Multi-Turn-Interaktionen und Function Calling auf `previous_interaction_id` der Interactions API umstellen.
  - Ausführlichkeit und Stil explizit definieren, falls von gesprächigeren Modellen migriert wird.

## Quellen
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — Offizielle Modellkarte: Modell-ID gemini-4-argon, Unified 1M Token Context Window, 64k Standard / 1M Long Decode, Modalitäten, Feature-Matrix, GA-Status Oktober 2026.
- https://ai.google.dev/gemini-api/docs/latest-model — „What's new in Gemini 4 Argon": Positionierung als Flaggschiff-Reasoning-Modell, Migrations-Checkliste (Entfernen von temperature/top_p/top_k, Anheben von max_output_tokens auf mind. 32k, Ersatz expliziten Cachings durch implizites 95%-Rabatt-Caching, previous_interaction_id), Long-Decode-Architektur via background=True, Default thinking_level medium.
- https://ai.google.dev/gemini-api/docs/pricing — Offizielle Preisstaffel: Einführungspreise bis 30.11.2026 ($2.00 Input, $0.10 Cached Input, $10.00 Output inkl. Thinking-Tokens), Normalpreise ab 01.12.2026 ($4.00 In / $0.20 Cached / $20.00 Out), kein Free Tier.
- https://ai.google.dev/gemini-api/docs/changelog — Release-Notes vom 13. Oktober 2026: General Availability (GA) von Gemini 4 Argon (gemini-4-argon).
- https://deepmind.google/models/model-cards/gemini-4-argon/ — DeepMind Model Card: Evaluierung für komplexe Softwareentwicklung, agentische Multi-Step-Workflows, Mathematik, Naturwissenschaften, Knowledge Cutoff März 2026 (Januar 2025 für Spezialdomänen) und dokumentierte Latenz-/Tokencharakteristiken.
- https://ai.google.dev/gemini-api/docs/thinking — Offizielle Dokumentation zum Reasoning-System: Thinking Levels (low, medium, high), Thought Signatures, Abrechnung von Thinking-Tokens und Verhalten bei max_output_tokens.
- https://ai.google.dev/gemini-api/docs/long-decode — Offizieller Leitfaden zu Long Decode: Generierung von bis zu 1M Tokens über server-seitige Fortsetzungs-Hops mit background=true.

