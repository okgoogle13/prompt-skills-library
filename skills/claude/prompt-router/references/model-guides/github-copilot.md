---
model: github-copilot
vendor: GitHub
family: Copilot
aliases: [copilot, github-copilot, gh-copilot, copilot-chat, copilot-edits, copilot-workspace, githubcopilot]
last_verified: 2026-11-12
status: current
---

# GitHub Copilot (Chat, Edits, Agent & Custom Instructions)

> ⚠ Einordnung: GitHub Copilot ist ein agentisches Entwickler- und Multi-Model-Ökosystem (VS Code, JetBrains, Visual Studio, Xcode, GitHub CLI `gh copilot`, Web/Workspace). Dieser Guide behandelt die Prompting- und Instruktionspraxis für Copilot Chat, Copilot Edits, Agent Mode sowie Repository- und Custom-Instructions (`.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/prompts/*.prompt.md`).

## Reasoning / Thinking
- **Multi-Model-Auswahl & Auto-Routing**: Copilot unterstützt über den Modell-Picker in Chat/Edits verschiedene Backend-Modelle (u. a. Anthropic Claude 3.5/3.7 Sonnet, OpenAI GPT-4o/o1/o3-mini/GPT-5, Google Gemini 2.5 Pro/Flash) oder **Auto** (automatisches intelligentes Routing basierend auf Task-Komplexität, Verfügbarkeit und Latenz).
- **Reasoning-Modelle im Harness**: Bei Auswahl von Reasoning-Modellen (z. B. `o1`, `o3-mini`, `claude-3.7-sonnet` mit aktiviertem Thinking) wird die Denktiefe über die Copilot-Harness gesteuert oder läuft modellnativ. Im Prompt selbst werden keine rohen API-Parameter (`reasoning_effort`, `budget_tokens`) übergeben.
- **Keine manuellen CoT-Scaffolds**: Anweisungen wie „Denke Schritt für Schritt“ oder manuelle `<thinking>`-Tags sind unnötig oder kontraproduktiv. Copilot durchläuft bei agentischen Aktionen (Edits/Agent Mode) bereits eigene interne Planungs- und Tool-Aufrufschleifen (Workspace-Suche, Linting, Terminal-Validierung), deren Schritte als einklappbare Zwischenschritte dargestellt werden.
- **Plan-Mode & Dekomposition**: Bei komplexen, dateiübergreifenden Refactorings zuerst eine explizite Plan-Phase anfordern („Erstelle zuerst einen schrittweisen Änderungsplan und warte auf Freigabe vor Code-Änderungen“), um unkontrollierte Edits über das Working Set zu vermeiden.

## Prompting-Stil
- **Präzise Kontext-Variablen statt vager Prosa**:
  - Nutze native Chat-Variablen: `#file:pfad/zur/datei` (oder `#file`), `#folder:pfad`, `#selection` (aktuell markierter Code), `#editor` (aktiver Editor-Inhalt), `#terminalSelection`, `#terminalLastCommand` und `#git`.
  - Chat-Teilnehmer (Participants) gezielt einsetzen: `@workspace` für repo-weite semantische Suche und Architekturfragen, `@terminal` für Shell-/CLI-Kontext, `@vscode` für IDE-Befehle/Settings, `@github` für Pull Requests und Issues.
- **Aktives Kontext-Fenster-Management (Tab-Hygiene)**:
  - Copilot nutzt geöffnete Editor-Tabs und die Datei-Nachbarschaft (Jaccard-Similarity, AST-Verbindungen) als impliziten Kontext. Irrelevante Tabs vor komplexen Prompts schließen, um Context-Window-Verwässerung zu verhindern.
  - Bei Themenwechsel Chat-Thread mit `/clear` leeren oder neuen Thread starten; veraltete Interaktionshistorie degradiert die Ausgabequalität nach 4–6 Turns merklich.
- **Architektur für `.github/copilot-instructions.md`**:
  - Ablage im Repo-Root (`.github/copilot-instructions.md`) für repo-weite persistente Regeln.
  - Stil: deklarativ, modular, stichpunktartig. Keine Floskeln („Du bist ein Senior-Entwickler...“).
  - Schwerpunkte: Technologie-Stack & Versionen, Architektur-Muster (z. B. Feature-Sliced Design, strikte Layer), Code-Konventionen (z. B. „benannte Exports statt Default-Exports“, „strikte TypeScript-Typen ohne any“), Test-Muster (z. B. „Vitest, AAA-Pattern, keine Snapshot-Tests für Business-Logik“) und explizite Negativ-Vorgaben („Keine neuen Drittanbieter-Bibliotheken ohne Rückfrage installieren“).
  - Pfadspezifische Regeln über `.github/instructions/*.instructions.md` mit YAML-Frontmatter (`applyTo: "src/api/**/*.ts"`).
- **Wiederverwendbare Prompt-Dateien (`.github/prompts/*.prompt.md`)**:
  - Wiederkehrende Arbeitsabläufe (z. B. Migrationen, neue API-Endpunkte, Test-Generierung) in `.github/prompts/<name>.prompt.md` ablegen.
  - Markdown-Links im Prompt-File (`[schema](../prisma/schema.prisma)`) werden von Copilot als Kontext-Dateien aufgelöst.
- **Aufgaben granular zerlegen & Done-Bedingung setzen**:
  - Grosse Vorhaben in kleine, testbare Einzelschritte aufteilen (z. B. erst Schema/Typen, dann Service-Logik, dann Tests, dann UI).
  - Jede Aufgabe mit einer konkreten, überprüfbaren Done-Bedingung versehen (z. B. „Ändere `src/auth.ts` so, dass `npm run test:auth` fehlerfrei durchläuft; verändere keine öffentlichen Methoden-Signaturen“).

## Stärken & Schwächen (prompt-relevant)
- **Stärken**:
  - Tiefe IDE-Verzahnung in VS Code, JetBrains, Visual Studio und Xcode;
  - Starkes Multi-File-Editing über Copilot Edits mit interaktiver Diff-Prüfung;
  - Schneller semantischer Workspace-Index (`@workspace`) ohne manuelles Copy-Paste von Datei-Inhalten;
  - Flexible Anpassbarkeit durch Repo-Instructions, pfadspezifische Instructions und Prompt-Files;
  - Modellvielfalt (Wechsel zwischen GPT, Claude und Gemini je nach Aufgabentyp).
- **Schwächen / Eigenheiten**:
  - Neigt bei offenen oder vagen Prompts dazu, existierende Utility-Funktionen zu ignorieren und Duplikate zu schreiben;
  - Kann bei umfangreichen Repositories ohne `#file`-Eingrenzung veraltete oder irrelevante Code-Stellen als Referenz heranziehen;
  - Kontext-Drift in langen Chat-Sessions;
  - Prompt-Caching und Token-Budgets sind durch die IDE-Harness vorgegeben und nicht direkt über API-Header beeinflussbar.

## Output- & Format-Konventionen
- Markdown mit standardisiertem Fenced-Code-Block-Highlighting; Pfad- und Zeilen-Referenzen im Format `dateiname:zeile`.
- Edits erzeugt Copilot bevorzugt als Inline-Diffs oder Multi-File-Änderungssätze im Working Set, nicht als reinen Fließtext.
- Spezifische Slash-Commands zur Steuerung: `/explain` (Code erklären), `/fix` (Bugs/Probleme im markierten Code beheben), `/tests` (Unit-Tests generieren), `/doc` (Dokumentation/Docstrings schreiben), `/setupTests` (Test-Framework einrichten), `/clear` (Kontext zurücksetzen).

## Migrations-Hinweise
- **ZU GitHub Copilot migrieren**:
  - System-Prompts, Agenten-Instruktionen oder Regel-Dateien (z. B. `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) in `.github/copilot-instructions.md` konsolidieren.
  - Dateipfade im Prompt von `@path` (Claude Code) oder absoluten Pfaden auf `#file:pfad/zur/datei` umstellen.
  - Manuelle CoT-Formulierungen („Think step by step“, „Scratchpad“) entfernen; stattdessen `#file`-Kontext, Typ-Verträge und terminierende Test-Befehle angeben.
  - Wiederkehrende Workflows als Prompt-Files in `.github/prompts/<name>.prompt.md` strukturieren.
- **VON GitHub Copilot wegmigrieren**:
  - Kontext-Variablen (`#file:...`, `#selection`, `#codebase`) in die Zielkonvention übersetzen (`@path` für Claude Code, `source_docs/...` für Antigravity/Gemini CLI, oder Dateiinhalte direkt einbetten).
  - Spezifische Chat-Participants (`@workspace`, `@terminal`) und Slash-Commands (`/fix`, `/tests`) durch explizite Ziel-Anweisungen und Tool-Aufrufe ersetzen.
  - Regeln aus `.github/copilot-instructions.md` in die systemspezifische Anweisungsdatei (z. B. `CLAUDE.md`, `AGENTS.md` oder System-Prompt) überführen.

## Quellen
- https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot — Offizieller Guide zu Prompt Engineering für Copilot (Kontext bereitstellen, Single Responsibility, Beispiele, Dekomposition).
- https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot — Konfiguration von `.github/copilot-instructions.md` und pfadspezifischen Instruktionen (`.github/instructions/*.instructions.md`).
- https://docs.github.com/en/copilot/customizing-copilot/creating-prompt-files-for-github-copilot — Erstellung und Nutzung von Prompt-Dateien (`.github/prompts/*.prompt.md`).
- https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/asking-github-copilot-questions-in-your-ide — Nutzung von `@workspace`, `#file`, `#selection`, `#editor`, Slash-Commands (`/fix`, `/tests`, `/explain`).
- https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/choosing-the-model-for-copilot-chat — Multi-Model-Picker, Auto-Routing, Claude-, GPT- und Gemini-Backend-Optionen.
