---
model: perplexity-deep-research
vendor: Perplexity
family: Perplexity
aliases: [perplexity-dr, sonar-deep-research, perplexity-deep, pplx-deep-research, deep-research-perplexity]
last_verified: 2026-11-07
status: current
---

# Perplexity Deep Research (Sonar Deep Research / Agent API, hoher Effort)

> ⚠ Die Perplexity-Doku wurde nur über Websuche-Zusammenfassungen geprüft, nicht direkt abgerufen. Effort-Namen und Parameter vor Einsatz verifizieren (unbelegt). Laut Recherche ersetzt die Agent API mit `high`/`xhigh` das eigenständige `sonar-deep-research`.

## Reasoning / Thinking
- Autonome Mehrschritt-Recherche: iteratives Suchen, Lesen, Anfragen verfeinern, Lücken schließen, Synthese vieler Quellen (teils Dutzende Tool-Schritte, Laufzeit mehrere Minuten).
- Agent API: `effort` `high` (Expertensynthese, Vergleichsberichte) und `xhigh`/`ultra` (erschöpfende Tiefenrecherche; Name `ultra` unbelegt).
- Legacy: `sonar-deep-research` mit `reasoning_effort` (low/medium/high; unbelegt).

## Prompting-Stil
- **Rubrik statt Frage**: mehrteiliges Ziel mit Gliederung vorgeben („Wettbewerbsanalyse X vs. Y: 1. Positionierung, 2. Preismodelle, 3. Releases der letzten 6 Monate“).
- Seed-Query spezifisch formulieren (Fachbegriffe, Zeiträume, Entitäten); der `input` bestimmt die erste Suche.
- `instructions` für Standing Rules: Sprache, Format, Zitatstil (Inline-Domain-Zitate statt Roh-URLs), Erlaubnis „keine Belege gefunden“. Eigene `instructions` ersetzen das Standard-System-Prompt des Effort-Levels.
- Domänen, Zeitfenster und Region über `search_domain_filter`, `search_recency_filter`, `search_mode` (`web | academic | sec`) steuern, nicht nur per Text.
- Umfang begrenzen (Zeitraum, Region, Branche), sonst ufert die Recherche aus; Prioritäten und Ausschlüsse nennen.
- Zitate nicht per Prosa-Format erzwingen; Anweisungen nicht zum „Wie suchen“, sondern zum „Was liefern“ formulieren.

## Stärken & Schwächen (prompt-relevant)
- Stärken: breite Quellenabdeckung, zitierter Bericht, geeignet für Vergleichs- und Marktanalysen.
- Schwächen: lange Laufzeit, hoher Token-/Suchaufwand; bei vagen Aufträgen unfokussierter Bericht; Latenz für interaktive Nutzung zu hoch.

## Output- & Format-Konventionen
- Langer Markdown-Bericht mit Quellen; Gliederung als Ausgabevertrag im Prompt festlegen. Streaming/Asynchronbetrieb je API prüfen (unbelegt).

## Migrations-Hinweise
- **VON Perplexity Deep Research weg**: Berichtsgliederung und Quellenregeln als Ausgabevertrag erhalten; Filter-Parameter in das Retrieval-Konzept des Ziels überführen; Ziel ohne Suche braucht Kontext oder Such-Tool, Mehrschritt-Anweisungen ergänzen.
- **ZU Perplexity Deep Research migrieren**: Prompt zu Ziel + Umfang + Gliederung + Quellenregeln verdichten; Such- und CoT-Anweisungen streichen; Zeit-/Domänenvorgaben in Filter verlagern; „kein Beleg“-Klausel ergänzen; hohen `effort` setzen und Laufzeit einplanen.

## Quellen
- https://docs.perplexity.ai — Effort-Level `high`/`xhigh`, Deep-Research-Verhalten, `instructions` vs. `input` (per Websuche zusammengefasst).
