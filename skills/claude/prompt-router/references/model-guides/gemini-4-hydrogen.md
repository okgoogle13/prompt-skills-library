---
model: gemini-4-hydrogen
vendor: Google
family: Gemini
aliases: [hydrogen, gemini-hydrogen, gemini4-hydrogen, 4-hydrogen, gemini-4-h2, gemini-hydrogen-4]
last_verified: 2026-11-13
status: current
---

# Gemini 4 Hydrogen

## Reasoning / Thinking
- Typ: **Natives Reasoning, immer aktiv**. Tiefe ausschließlich über das String-Enum `thinking_level` steuerbar (`low | medium | high | xhigh`), **Default `high`** (optimiert für Code- und agentische Workflows).
- `minimal` wird für Gemini 4 Hydrogen **nicht** unterstützt und liefert einen Fehler (`400 INVALID_ARGUMENT`) — Pfade von älteren Flash-Modellen (z. B. `gemini-3.6-flash`, `gemini-3.5-flash-lite`), die `minimal` nutzen, müssen zwingend auf `low` angehoben werden.
- `thinking_budget` (Token-Budget) wird wie bei allen Gemini-4-Modellen nicht mehr unterstützt und darf nicht übergeben werden. Die Stufen sind relative Allowances für die Überlegungstiefe, keine strikten Token-Garantien.
- Stufenwahl laut Google / DeepMind Doku:
  - `low`: Geringste Latenz (sub-6s Antwortzeiten) und minimaler Tokenverbrauch; ideal für High-Throughput-Tasks, Faktenabruf, Textanalyse und leichte Klassifikationen. Bei komplexer Architektur oder tiefem Debugging kann die Qualität abfallen.
  - `medium`: Ausgewogene Denktiefe für fortgeschrittene Textverarbeitung, Konzeptvergleiche und unkritische Code-Snippets.
  - `high` (Default): Standardempfehlung für alltägliche agentische Workflows, Repository-Navigation, Software-Engineering und Multi-Step-Problemlösung.
  - `xhigh`: Maximale Denktiefe durch Test-Time-Compute-Skalierung für besonders harte Multi-Step-Probleme, komplexe Root-Cause-Analysen, mathematische/naturwissenschaftliche Beweise und formale Verifikation. Pushed Benchmarks auf Frontier-Niveau, benötigt jedoch spürbar mehr Thinking- und Output-Tokens.
- **`max_output_tokens` als harte Obergrenze**: `max_output_tokens` begrenzt die **Summe** aus generierten Thinking-Tokens und tatsächlichem Output. Wird der Wert zu niedrig angesetzt (z. B. < 32k), kann das Modell das gesamte Kontingent im Reasoning aufbrauchen und die Antwort vorzeitig abbrechen. Google empfiehlt mindestens 32.768 Tokens (Standard synchronous: 65.536).
- **Long Decode**: Für Antworten jenseits von 64k Tokens unterstützt Gemini 4 Hydrogen Long Decode bis zu 1.048.576 Tokens (minus Input) über `background: true` und `max_output_tokens > 65536`. Die Fortsetzungs-Hops werden serverseitig orchestriert; Textinhalte der `model_output`-Steps werden aneinandergehängt.
- **Thought Signatures & State-Management**: Bei mehrstufigen Konversationen und Tool-Calls wird der verschlüsselte Reasoning-Kontext über Thought Signatures transportiert. Empfohlener Standard ist die serverseitige Zustandsverwaltung via `previous_interaction_id` der Interactions API (`store=true`). Bei zustandslosen Requests müssen alle generierten Thought-Blöcke unverändert in der Konversationshistorie mitgeführt werden.
- Abrechnung: Berechnet wird die Gesamtsumme aus Ausgabe- und Denk-Tokens ($1.50 Input / $7.50 Output pro 1M Tokens).

## Prompting-Stil
- **Direkt, präzise und schlank**: „Be concise. Gemini responds best to direct, clear instructions." Aufwändiges Prompt-Engineering für ältere Nicht-Reasoning-Modelle (wie manuelles „Think step by step" oder verschachtelte CoT-Schablonen) führt laut Doku dazu, dass das Modell überanalysiert („over-analyze") und sollte restlos entfernt werden.
- **Standard-Tonalität ist nüchtern**: Das Modell antwortet standardmäßig kompakt und sachlich. Wenn ausführliche, didaktische oder konversationelle Antworten erwünscht sind, muss dieser Stil explizit im Prompt angefordert werden.
- **Long-Context-Struktur**: Bei großen Datenmengen (Dokumente, Codebases, Tabellen) die Referenzdaten **an den Anfang** und die konkrete Aufgabe/Instruktion ans **Ende nach dem Datenblock** stellen, eingeleitet durch eindeutige Anker („Basierend auf den vorstehenden Informationen...").
- **Keine Sampling-Parameter**: `temperature`, `top_p` und `top_k` vollständig aus den Generation-Configs entfernen. Sie werden ignoriert; manuelle Eingriffe unter 1.0 können bei anspruchsvollen Reasoning- und Coding-Aufgaben Looping auslösen.
- **Kein Assistant-Prefill**: Vorgefüllte Modellantworten (`prefilled model turns`) entfernen. Struktur und Formatierung stattdessen über System-Instructions oder `response_schema` (Structured Outputs) durchsetzen.
- **Workhorse in agentischen Loops**: Klare Zielverträge, maximale Iterationsgrenzen und überprüfbare Done-Kriterien (z. B. „Diff erzeugen, Testsuite ausführen, beenden wenn grün") definieren, da Hydrogen ideal als schneller Worker in iterativen Feedbackschleifen agiert.

## Stärken & Schwächen (prompt-relevant)
- **Stärken**:
  - Googles hochperformantes „Workhorse"- und Execution-Modell der Gemini-4-Generation: signifikant schneller und reaktionsfreudiger als ältere Flash-Modelle (wie `gemini-3.8-flash`), bei herausragender Reasoning-Stärke auf `high` und `xhigh`;
  - Exzellent in schnellen Feedback-Schleifen, beim Schreiben von Code-Patches, Ausführen von Terminal-Befehlen und iterativen Unit-Tests;
  - Hohe Zuverlässigkeit bei Function Calling und Tool-Use;
  - Unified 1M Token Context Window mit transparenter Preisgestaltung ($1.50 In / $7.50 Out);
  - Idealer Ausführungs-Worker in Multi-Model-Architekturen (z. B. unter `gemini-4-argon` / Antigravity Orchestrator).
- **Schwächen & Eigenheiten**:
  - **Kein explizites Context Caching**: Traditionelles manuelles Caching (`cachedContents` / `caches.create`) wird nicht mehr unterstützt. Stattdessen greift automatisches, implizites Caching (ab 4.096 Tokens) mit 95 % Rabatt auf Treffer.
  - **Tokenverbrauch auf xhigh**: Auf der höchsten Stufe `xhigh` können signifikant mehr Tokens anfallen und die Latenz steigen; für reine Extraktions- oder einfache Textaufgaben sollte `thinking_level: "low"` gewählt werden.
  - **Fehlende Modalitäten im Output**: Keine native Bild- oder Audiogenerierung, keine Live API (WebSockets).
  - **Knowledge Cutoff**: März 2026 (mit einzelnen Domänen bis Januar 2025). Zeitkritische Daten müssen über Google Search Grounding oder den Kontext bereitgestellt werden.

## Output- & Format-Konventionen
- Unified Context Window: **1.048.576 Tokens** (geteilt zwischen Input, Thinking und Output).
- Maximale Ausgabetoken: 65.536 Tokens synchron; bis zu 1.048.576 Tokens (abzüglich Input-Tokens) im asynchronen Long-Decode-Modus (`background: true`).
- Input-Modalitäten: Text, Bild, Video, Audio, PDF. Output: Nur Text.
- Unterstützte Features: Structured Outputs (`response_schema`), Function Calling, Implizites Caching (ab 4k Tokens, 95 % Rabatt), Code Execution, Google Search Grounding, Maps Grounding, URL Context, File Search, Batch API (50 % Rabatt), Flex- und Priority-Inference.
- Function Calling: Jedes `FunctionResponse` muss `call_id` und den exakten `name` tragen, mit genau einer Response pro Call.
- Preise (pro 1M Tokens): Input $1.50 (Cached $0.075), Output $7.50 (inkl. Thinking-Tokens). Kein permanenter Free Tier.

## Migrations-Hinweise
- **VON gemini-4-hydrogen weg**:
  - `thinking_level` in das Zielformat überführen (`reasoning_effort` bei OpenAI o3/GPT-5, `budget_tokens` bzw. adaptiver `effort` bei Claude Sonnet/Opus); falls das Zielmodell kein natives Reasoning besitzt, wieder explizites Chain-of-Thought-Scaffolding („Schritt für Schritt") im Prompt ergänzen.
  - Sampling-Parameter (`temperature`, `top_p`) wieder in die Generation-Config einfügen.
  - Server-seitigen Session-State (`previous_interaction_id`) auflösen und Konversationshistorie client-seitig verwalten.
  - Long-Decode-Annahmen über 64k Tokens Output auf die Ausgabelimits des Zielmodells zurückstutzen.
- **ZU gemini-4-hydrogen migrieren**:
  - Modell-ID auf `gemini-4-hydrogen` setzen.
  - `thinking_level` konfigurieren (`low | medium | high | xhigh`; Default ist `high`; von älteren Modellen stammendes `minimal` zwingend auf `low` anheben).
  - `max_output_tokens` überprüfen und auf mindestens 32.768 erhöhen (oder Default 65.536 belassen), damit Reasoning den eigentlichen Output nicht abschneidet.
  - Manuelle CoT-Anweisungen („Denke Schritt für Schritt", „Reflektiere ausführlich") und verbose Scaffolding aus dem Prompt streichen und stattdessen `thinking_level: "high"` oder `"xhigh"` wählen.
  - Explizites Caching (`caches.create`) aus dem Code entfernen — Implizites Caching greift automatisch ab 4.096 Tokens.
  - `temperature`, `top_p`, `top_k`, `thinking_budget` und `candidate_count` restlos aus Requests entfernen.
  - Multi-Turn-Interaktionen und Function Calling auf `previous_interaction_id` der Interactions API umstellen oder Thought Signatures unverändert mitführen.
  - Ausführlichkeit und Tonalität explizit definieren, falls von gesprächigeren Modellen migriert wird.

## Quellen
- https://ai.google.dev/gemini-api/docs/models/gemini-4-hydrogen — Offizielle Modellkarte: Modell-ID `gemini-4-hydrogen`, Unified 1M Token Context Window, 64k Standard / 1M Long Decode, Modalitäten, Feature-Matrix, GA-Status November 2026.
- https://ai.google.dev/gemini-api/docs/latest-model — „What's new in Gemini 4 Hydrogen": Positionierung als High-Throughput-Workhorse, Thinking-Levels (`low`, `medium`, `high`, `xhigh`), Entfernung von `temperature`/`top_p`/`top_k` und `thinking_budget`, Default `thinking_level: high`.
- https://ai.google.dev/gemini-api/docs/pricing — Offizielle Preisstaffel: Flat-Pricing $1.50 Input ($0.075 Cached Input), $7.50 Output (inkl. Thinking-Tokens), Batch API 50 % Rabatt.
- https://deepmind.google/models/model-cards/gemini-4-hydrogen/ — DeepMind Model Card: Evaluierung für schnelles Software-Engineering, agentische Multi-Step-Workflows, Artificial Analysis Intelligence Index (~51 auf high, ~54 auf xhigh), Knowledge Cutoff März 2026.
- https://ai.google.dev/gemini-api/docs/thinking — Offizielle Dokumentation zum Reasoning-System: Thinking Levels (`low`, `medium`, `high`, `xhigh`), Thought Signatures, Abrechnung von Thinking-Tokens und Verhalten bei `max_output_tokens`.

