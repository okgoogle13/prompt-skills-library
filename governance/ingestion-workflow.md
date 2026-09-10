# Ingestion workflow

How to convert external source material into canonical repo artifacts.

## Two-stage pipeline

### Stage 1 — Scrape and normalize

1. Use **Firecrawl** for article and docs pages (primary tool)
2. Use **Browserbase** only when a page requires interaction or is hard to scrape
3. For each URL:
   - Strip nav, footer, repeated boilerplate, and unrelated chrome
   - Preserve: title, URL, retrieval date, headings, code blocks, and schema examples
   - Save as one normalized markdown file per source in `knowledge/`
   - Use frontmatter: `source_url`, `retrieved_date`, `source_class`, `priority`

### Stage 2 — Convert to artifacts

1. Chunk the normalized file by heading
2. Classify each chunk as one of:
   - `principle` — a rule or guideline
   - `pattern` — a reusable structure or technique
   - `warning` — a known failure mode or anti-pattern
   - `example` — a worked example or before/after
   - `schema` — a metadata or template structure
   - `workflow` — a step-by-step process
3. Extract reusable items into structured prompt cards or skill cards using `schemas/prompt-card.yaml`
4. Generate runtime variants as needed:
   - `canonical` — the base, model-agnostic version
   - `gemini-chrome` — short, page-context-aware, user-facing
   - `claude` — longer, critique-oriented, document-aware
   - `local-llm` — shorter, stricter format constraints, more examples, no implicit reasoning
   - `antigravity` — orchestration-oriented, XML-tagged

## Scraping manifest

See `sources/registry.md` for the current list of approved source URLs and their ingestion status.

## Naming for ingested files

`knowledge/<class>/<source-slug>.md`

Examples:
- `knowledge/canonical/anthropic/claude-prompting-best-practices.md`
- `knowledge/library-design/promptquorum-build-a-prompt-library.md`
- `knowledge/local-llms/promptquorum-local-model-prompting.md`
- `knowledge/local-llms/suedbroecker-local-llm-cheat-sheet.md`

## Frontmatter template

```yaml
---
source_url: ""
retrieved_date: ""
source_class: "canonical" # canonical | library-design | local-llms | examples
priority: "foundation"     # foundation | supplementary | experimental
status: "raw"              # raw | normalized | converted
adapted_to_artifacts: []   # list of prompt-card or skill-card IDs derived from this source
---
```
