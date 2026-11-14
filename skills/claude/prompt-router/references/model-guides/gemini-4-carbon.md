---
model: gemini-4-carbon
vendor: Google
family: Gemini
aliases: [carbon, gemini-carbon, gemini4-carbon, 4-carbon, carbon-4]
last_verified: 2026-11-13
status: current
---

# Gemini 4 Carbon

> ⚠ Einordnung: Gemini 4 Carbon (`gemini-4-carbon`) ist Googles leistungsfähigstes Frontier-Reasoning-Modell für extreme Denktiefe, langlebige autonome Agenten, komplexe Software-Architektur, hochpräzise Cybersicherheit (Vulnerability Lifecycle) und wissenschaftliche Beweisführung. Im Vergleich zu `gemini-4-argon` investiert Carbon signifikant mehr Test-Time-Compute und Verifikationsschritte pro Turn, um Fehler bei anspruchsvollen Problemstellungen drastisch zu minimieren.

## Verfügbare Schnittstellen & Plattformen (Interfaces)
Gemini 4 Carbon ist über folgende offizielle Schnittstellen und Entwicklerumgebungen verfügbar:
1. **Google AI Studio (Web-UI & Developer Console)**:
   - Direkt im Web-Interface (`aistudio.google.com`) für Prompt-Prototyping, System-Instruction-Design und multimodale Tests (PDF, Code, Audio, Video bis 1M Tokens).
   - Steuerung der Denktiefe über das `thinking_level`-Dropdown (`low`, `medium`, `high`).
   - Generierung von API-Keys für den Paid Tier (Pay-as-you-go).
2. **Gemini API & Google GenAI SDK (`google-genai`)**:
   - Standardmäßige REST-API und offizielle SDKs (Python, Node.js, Go, Java) unter Verwendung der Modell-ID `gemini-4-carbon`.
   - **Interactions API**: Unterstützt zustandsbehaftete Sitzungen über `previous_interaction_id` (`store=true`) sowie asynchrones Long Decode bis 1M Tokens mit `background: true`.
3. **Google Antigravity (Agent IDE & Swarm Orchestrator)**:
   - Integriert als primäres Architekten- und Review-Modell für Multi-Agent-Workflows (`/swarm`, Antigravity Orchestrator).
   - Wird für übergeordnete Systemarchitektur, Planfreigaben (`plan.md`) und sicherheitskritische Code-Audits eingesetzt, während Ausführungs-Subagents (typischerweise `gemini-4-hydrogen`) operative Edits übernehmen.
4. **Google Cloud / Vertex AI**:
   - Enterprise Model Garden und Vertex AI Studio für Unternehmenskunden mit privater VPC-Anbindung, IAM-Governance, SLA-Garantien und regionaler Datenhaltung.
5. **Google Workspace & Gemini for Business / Google AI Ultra**:
   - Verfügbar für Google AI Ultra Abonnenten in der Gemini Web-/Mobile-App, in Google Workspace (Docs, Sheets, Drive) sowie im AI Mode der Google Suche.
6. **IDE-Erweiterungen & Android Studio**:
   - Integriert in Android Studio und moderne IDE-Assistenten für tiefgehende Code-Refactorings, Thread-Sicherheitsanalysen und Speicherleck-Diagnosen.

## Reasoning / Thinking
- Typ: **Natives Reasoning mit erweiterter Verifikation, immer aktiv**. Tiefe ausschließlich über das String-Enum `thinking_level` steuerbar (`low | medium | high`), **Default `medium`**. `minimal` wird nicht unterstützt und wirft einen Fehler (`400 INVALID_ARGUMENT`).
- `thinking_budget` (Token-Budget) wird nicht mehr unterstützt und darf nicht übergeben werden. Die Stufen sind relative Allowances; Carbon nutzt pro Stufe deutlich mehr Thought-Tokens als Argon oder Hydrogen, um Alternativen abzuwägen und Code-Pfade formal zu verifizieren.
- Empfohlene Stufenwahl:
  - `low`: Schnellere Bearbeitung und geringere Tokenkosten; geeignet für strukturierte Extraktion, vergleichende Analysen und leichtere Programmieraufgaben.
  - `medium` (Default): Ausgewogene Tiefe für anspruchsvolles Software-Engineering, komplexe API-Integrationen und Multi-Step-Logik.
  - `high`: Maximale Denktiefe für kryptografische Analysen, tiefes Root-Cause-Debugging (Race Conditions, Memory Leaks), Zero-Day-Vulnerability-Audits (SEC-bench) und mathematische Beweisführung.
- **`max_output_tokens` als harte Obergrenze**: Begrenzt die **Summe** aus Thinking-Tokens und eigentlichem Text-Output. Da Carbon sehr gründlich nachdenkt, muss `max_output_tokens` zwingend auf mindestens **32.768**, idealerweise **65.536** Tokens gesetzt werden (Standard-Synchronlimit), um ein vorzeitiges Abschneiden der Antwort zu verhindern.
- **Long Decode**: Für gigantische Ausgaben jenseits von 64k Tokens unterstützt Carbon Long Decode bis zu 1.048.576 Tokens (minus Input) via `background: true` und `max_output_tokens > 65536`.
- **Thought Signatures**: Verschlüsselte Repräsentation des Denkzustands; bei Multi-Turn und Function Calling via `previous_interaction_id` serverseitig verwalten oder stateless unverändert in `contents` mitführen.
- Abrechnung: Berechnet wird die Gesamtsumme aus Ausgabe- und Denk-Tokens ($2.00 bzw. $4.00 In / $10.00 bzw. $20.00 Out pro 1M Tokens).

## Prompting-Stil
- **Direkt, präzise und zielorientiert**: „Be concise. Gemini responds best to direct, clear instructions." Manuelle Chain-of-Thought-Anweisungen („Think step by step", Pseudo-Scratchpads) sind kontraproduktiv und führen zu unnötiger Latenz oder Over-Analyzing, da das Modell autonom tiefgreifende Verifikationsschleifen durchläuft.
- **Strikte Spezifikation & Verträge definieren**: Carbon brilliert, wenn formale Constraints, Invarianten, Typdefinitionen und Akzeptanzkriterien vorgegeben werden.
- **Standard-Tonalität ist analytisch-sachlich**: Antworten sind standardmäßig kompakt und auf die Problemlösung fokussiert. Ausführliche didaktische Erklärungen müssen explizit angefordert werden.
- **Long-Context-Struktur**: Referenzdaten (Codebases, Protokolle, Schemata) an den **Anfang**; konkrete Aufgabenstellung und Prüfkriterien an das **Ende nach dem Datenblock**.
- **Keine Sampling-Parameter**: `temperature`, `top_p` und `top_k` vollständig aus Generation-Configs entfernen (werden ignoriert oder erzeugen bei Werten < 1.0 Looping bei mathematischen Beweisen).
- **Kein Assistant-Prefill**: Vorgefüllte Modellantworten entfernen; Struktur über `response_schema` (Structured Outputs) oder System-Instructions vorgeben.

## Stärken & Schwächen (prompt-relevant)
- **Stärken**:
  - **Spitzenreiter bei maximaler Denktiefe**: Übertrifft `gemini-4-argon` und alle vorherigen Modelle auf anspruchsvollen Benchmarks (Artificial Analysis Intelligence Index, Terminal-Bench, HLE);
  - **Cybersicherheit & Vulnerability-Lifecycle**: Exzellente Ergebnisse bei automatisierter Schwachstellensuche (CWE-bench, SEC-bench Pro) und Root-Cause-Patching;
  - **Robuste Architekturplanung**: Ideal als zentraler Stratege in Multi-Agent-Systemen (Antigravity `/swarm`), da es komplexe Abhängigkeiten fehlerfrei überblickt;
  - Unified 1M Token Context Window mit automatischem impliziten Caching (95 % Rabatt ab 4.096 Tokens).
- **Schwächen & Eigenheiten**:
  - **Höhere Latenz und Tokenverbrauch**: Durch intensive interne Verifikation benötigt Carbon mehr Zeit und generiert mehr Thinking-Tokens als Argon; für Routine-Coding oder einfache Textaufgaben ist `gemini-4-hydrogen` oder `gemini-4-argon` deutlich wirtschaftlicher;
  - **Kein explizites Caching mehr**: Manuelle Cache-Erstellung (`caches.create`) ist abgelöst;
  - **Keine Bild-/Audioausgabe**: Input multimodal (Text, Bild, Audio, Video, PDF), Output rein textbasiert;
  - **Knowledge Cutoff**: März 2026 (Januar 2025 für Spezialdomänen); tagesaktuelle Fakten via Google Search Grounding einbinden.

## Output- & Format-Konventionen
- Context Window: **1.048.576 Tokens** (geteilt zwischen Input, Thinking und Output).
- Maximale Ausgabetoken: 65.536 synchron; bis zu 1.048.576 Tokens im Long-Decode-Modus (`background: true`).
- Input: Text, Bild, Video, Audio, PDF. Output: Nur Text.
- Features: Structured Outputs (`response_schema`), Function Calling (mit `call_id` und `name`), Implizites Caching (95 % Rabatt ab 4k Tokens), Code Execution, Google Search Grounding, Maps Grounding, URL Context, Batch API (50 % Rabatt), Flex- und Priority-Inference.
- Preise (pro 1M Tokens):
  - Bis 30.11.2026 (Einführungspreis): Input $2.00 (Cached $0.10), Output $10.00.
  - Ab 01.12.2026 (Regulär): Input $4.00 (Cached $0.20), Output $20.00.
  - Kein permanenter Free Tier.

## Migrations-Hinweise
- **VON gemini-4-carbon weg**:
  - `thinking_level` in das Zielformat übertragen (`reasoning_effort` bei OpenAI o3/GPT-5, `budget_tokens` bzw. adaptiver `effort` bei Claude Opus/Sonnet);
  - Bei Wechsel zu Modellen ohne natives Reasoning manuelle CoT-Schablonen („Schritt für Schritt") wieder ergänzen;
  - Sampling-Parameter (`temperature`, `top_p`) wieder in die Request-Konfiguration aufnehmen;
  - Server-seitigen Session-State (`previous_interaction_id`) auflösen und Historie client-seitig führen;
  - Long-Decode-Annahmen über 64k Tokens auf die Limits des Zielmodells zurückstutzen.
- **ZU gemini-4-carbon migrieren**:
  - Modell-ID auf `gemini-4-carbon` setzen.
  - `thinking_level` konfigurieren (`low | medium | high`; Default ist `medium`; `minimal` zwingend auf `low` anheben).
  - `max_output_tokens` auf mindestens 32.768 (besser 65.536) anheben, da Carbons tiefe Denkphase sonst den eigentlichen Output abschneidet.
  - Manuelle CoT-Anweisungen („Denke Schritt für Schritt") restlos entfernen.
  - `temperature`, `top_p`, `top_k`, `thinking_budget` und `candidate_count` entfernen.
  - Explizites Caching (`caches.create`) streichen — implizites Caching greift automatisch ab 4.096 Tokens.
  - Multi-Turn-Interaktionen auf `previous_interaction_id` der Interactions API umstellen oder Thought Signatures unverändert durchreichen.

## Quellen
- https://aistudio.google.com/learn/gemini-4-carbon-developer-guide — Offizieller Entwicklerleitfaden in Google AI Studio: Modell-Spezifikationen, verfügbare Schnittstellen (AI Studio, Gemini API, Antigravity, Vertex AI, Workspace/Ultra), Thinking-Levels, Long Decode und Best Practices.
- https://ai.google.dev/gemini-api/docs/models/gemini-4-carbon — Offizielle Modellkarte für Gemini 4 Carbon: Unified 1M Token Context, 64k Standard / 1M Long Decode, Modalitäten, Feature-Matrix.
- https://deepmind.google/models/model-cards/gemini-4-carbon/ — DeepMind Model Card: Spitzenwerte bei Software-Engineering, Cybersecurity-Audits (SEC-bench, CWE-bench), autonomer Multi-Step-Reasoning und erweiterte Test-Time-Verification.
- https://ai.google.dev/gemini-api/docs/pricing — Offizielle Preisstaffel: Einführungspreise bis 30.11.2026 ($2.00 In / $10.00 Out), Normalpreise ab 01.12.2026 ($4.00 In / $20.00 Out).
- https://ai.google.dev/gemini-api/docs/thinking — Offizielle Dokumentation zum Reasoning-System: Thinking Levels (`low`, `medium`, `high`), Thought Signatures und Verhalten bei `max_output_tokens`.

