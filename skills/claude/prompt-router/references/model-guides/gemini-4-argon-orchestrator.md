---
model: gemini-4-argon-orchestrator
vendor: Google
family: Gemini
aliases: [argon-orchestrator, gemini-argon-orchestrator, gemini4-argon-orchestrator, orchestrator-argon, argon-orch]
last_verified: 2026-11-13
status: current
---

# Gemini 4 Argon Orchestrator

> ⚠ Einordnung: Gemini 4 Argon Orchestrator beschreibt das multi-modell- und agentengestützte Orchestrierungs-Paradigma (etwa in Google Antigravity oder vergleichbaren Agent-Harnesses). Hierbei agiert das Flaggschiff-Reasoning-Modell Gemini 4 Argon (`gemini-4-argon`) als zentraler Stratege, Architekt und Koordinator, während spezialisierte High-Speed-Worker (typischerweise `gemini-4-hydrogen`) für operative Code-Änderungen, Tool-Ausführungen, Datei-Sweeps und Testläufe angesteuert werden. Dieser Guide beschreibt, wie Prompts formuliert werden müssen, um diese Aufgabenteilung, iterative Planungsschleifen und strikte Governance optimal zu steuern.

## Reasoning / Thinking
- **Duale Modell-Hierarchie**: Der Orchestrator operiert auf `gemini-4-argon` mit nativem Reasoning (`thinking_level`: `high` für die initiale Architektur-, Dekompositions- und Planungsphase; `medium` für fortlaufendes Monitoring, Rollen-Delegation und Code-Review).
- **Subagenten-Steuerung**: Die vom Orchestrator angesteuerten Ausführungs-Subagents (typischerweise `gemini-4-hydrogen`) operieren autonom mit eigener Denktiefe (`high` für Coding/Debugging, `low` für Scans und Extraktion). Rohe API-Parameter für Subagents gehören nicht in den Orchestrator-Prompt.
- **Spec-First Pattern (Mandatory Planning Phase)**: Der Prompt muss den Orchestrator dazu verpflichten, vor Schreiboperationen oder Subagent-Delegationen einen formalen Spezifikations- oder Änderungsplan (`plan.md` / Architecture Artifact) zu entwerfen und auf Benutzerfreigabe zu warten. Dies verhindert unkontrollierten Tokenverbrauch und Fehlallokationen von Subagenten.
- **Keine manuellen CoT-Scaffoldings**: Anweisungen wie „Denke Schritt für Schritt" sind überflüssig; der Orchestrator nutzt das tiefe native Reasoning von Argon zur Abhängigkeitsanalyse und Strukturierung des Problemraums.
- **Quoten- & Token-Schonung**: Das Paradigma spart gezielt teure Argon-Thinking-Tokens, indem aufwändige Terminal-Befehle, Datei-Sweeps und repetitive Code-Generierungen an Hydrogen-Subagents delegiert werden.

## Prompting-Stil
- **Goal-Oriented Prompting („Give Goals, Not Steps")**: Keine Micro-Management-Befehle auf Dateizeilenebene formulieren („Öffne Datei X, ändere Zeile 40..."). Stattdessen High-Level-Ziele, architektonische Rahmenbedingungen, Schnittstellenverträge und Qualitätsstandards vorgeben (z. B. „Untersuche den Authentifizierungs-Absturz in den Logs, entwerfe einen fehlertoleranten Fix gemäß unserer Error-Handling-Konventionen, delegiere die Implementierung an Subagents und verifiziere sie über die lokale Testsuite").
- **Klare Rollen- und Aufgabenteilung (Architect $\rightarrow$ Engineer $\rightarrow$ QA)**:
  - *Architect (Argon Orchestrator)*: Systemdesign, Schnittstellen, Datenfluss, Abhängigkeitsanalyse, Delegation und finale Freigabe.
  - *Engineer (Hydrogen Subagent)*: Modulare Umsetzung, Einhaltung von PEP 8/TypeScript-Konventionen, chirurgische Datei-Edits.
  - *QA / Verification (Hydrogen Subagent)*: Test-Suiten ausführen, Regressionsprüfung, Diff-Validierung.
- **Artifacts-as-Accounting**: Strikte Done-Kriterien und Nachweispflichten definieren. Der Orchestrator darf eine Aufgabe erst als erledigt melden, wenn überprüfbare Artefakte vorliegen: 1) Genehmigter Plan (`plan.md`), 2) Git-Diff-Zusammenfassung der Subagents, 3) Erfolgreiche lokale Testlogs, 4) Keine Verletzung von Style- oder Architekturregeln.
- **Session- & Context-Hygiene („Single Ticket / Single Mission")**: Unzusammenhängende Aufgaben nicht in einem einzigen Thread anhäufen. Repository-Regeln, Stilvorgaben und Tool-Policies nicht in jedem Prompt wiederholen, sondern deklarativ in `AGENTS.md`, `GEMINI.md` oder Custom Skills verankern.
- **Fehlerbehandlung & Bidirektionale Steuerung**: Im Prompt festlegen, dass Subagenten bei unerwarteten Testfehlschlägen oder Architekturkonflikten sofort an den Orchestrator zurückmelden, statt eigenmächtig weitreichende Workarounds zu implementieren.

## Stärken & Schwächen (prompt-relevant)
- **Stärken**:
  - Höchste Erfolgsquote bei komplexen, dateiübergreifenden Refactorings, System-Migrationen und langlebigen agentischen Workflows;
  - Massive Token- und Quoten-Ersparnis gegenüber monolithischer Ausführung auf reinen Frontier-Modellen;
  - Strukturierte, nachvollziehbare Entwicklung durch explizite Plan- und Verifikationsartefakte;
  - Automatische Fehlerbehebung durch strategische Re-Planung bei fehlschlagenden Subagent-Schritten.
- **Schwächen & Eigenheiten**:
  - **Overhead bei Trivialaufgaben**: Für simple Ein-Datei-Änderungen oder schnelle Einzeiler ist die Orchestrierung zu schwerfällig; hierfür direkt `gemini-4-hydrogen` ansteuern;
  - **Harness-Abhängigkeit**: Setzt eine Umgebung voraus, die Subagenten oder Swarm-Prozesse unterstützt (z. B. Google Antigravity, Multi-Agent Harnesses);
  - **Latenz in der Planungsphase**: Durch das tiefe Reasoning von Argon benötigt die initiale Planerstellung Zeit.

## Output- & Format-Konventionen
- Ausgabe-Formate: Strukturierte Markdown-Pläne (Implementation Blueprint, `plan.md`), isolierte Worker-Briefings und zusammenfassende Verifikations-Reports mit Git-Diffs und Test-Ergebnissen.
- Keine Sampling-Parameter (`temperature`, `top_p`, `top_k` entfernen).
- Steuerung über Antigravity Orchestrator-Tools, Subagent-Invocations (`invoke_subagent`, `swarm`) oder CLI-Harness.

## Migrations-Hinweise
- **VON gemini-4-argon-orchestrator weg**:
  - Multi-Agent- und Delegationsanweisungen in sequenzielle Einzelschritt-Prompts für monolithische Modelle auflösen;
  - Spezifische Antigravity-Artefakt-Vorgaben (`plan.md`, Swarm-Briefings) durch manuelle Checklisten ersetzen;
  - Code-Generierung und Architektur-Planung wieder in einem einzigen Prompt zusammenführen.
- **ZU gemini-4-argon-orchestrator migrieren**:
  - Monolithische Prompts („Schreibe die Datei X neu und teste sie") in ein zielorientiertes Orchestrierungs-Briefing umwandeln;
  - Verbindliche „Spec-First"-Klausel einfügen (erst Analyse und Planungsartefakt vor Codeänderungen);
  - Rollenteilung verankern: Argon steuert Planung und Review, delegiert Datei-Edits und Testläufe an schnelle Worker (`gemini-4-hydrogen`);
  - Verifizierbare Done-Bedingung über konkrete Nachweise (Git-Diff, Test-Reports) festlegen;
  - Repo-weite Regeln in `AGENTS.md` / `GEMINI.md` auslagern, um den User-Prompt schlank zu halten.

## Quellen
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — Offizielle Modellkarte für Gemini 4 Argon als Frontier Reasoning Engine.
- https://ai.google.dev/gemini-api/docs/latest-model — Google DeepMind: Multi-Model-Orchestration, Dynamisches Routing und Quotenmanagement in Agentic Workflows.
- https://antigravity.google/docs/orchestration — Antigravity Agent Orchestrator Guide: Spec-First Pattern, Artifacts-as-Accounting, Multi-Tier Subagent Delegation (Argon Architect / Hydrogen Worker).
- https://deepmind.google/models/model-cards/gemini-4-argon/ — DeepMind Model Card: Evaluierung für komplexe Software-Architektur und agentische Steuerung.
- https://ai.google.dev/gemini-api/docs/models/gemini-4-hydrogen — Offizielle Modellkarte für Gemini 4 Hydrogen als Execution Engine.

