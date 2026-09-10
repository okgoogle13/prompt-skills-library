# Source registry

Canonical list of approved source URLs, their classification, priority, and ingestion status.

Add new sources here before scraping. Review monthly.

## Foundation sources

| Source | URL | Class | Priority | Status |
|---|---|---|---|---|
| Anthropic Claude prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | canonical | foundation | pending |
| Anthropic llms.txt | https://platform.claude.com/llms.txt | canonical | foundation | pending |
| PromptQuorum: build a prompt library | https://www.promptquorum.com/prompt-engineering/build-a-prompt-library | library-design | foundation | pending |
| PromptQuorum: fundamentals of prompt optimization | https://www.promptquorum.com/prompt-engineering/fundamentals-of-prompt-optimization | library-design | foundation | pending |
| PromptQuorum: prompt engineering for local models | https://www.promptquorum.com/local-llms/prompt-engineering-for-local-models | local-llms | foundation | pending |
| Suedbroecker: local LLMs and autonomous agents cheat sheet | https://suedbroecker.net/2026/06/15/prompting-cheat-sheet-for-local-llms-and-autonomous-agents/ | local-llms | foundation | pending |

## Supplementary sources

| Source | URL | Class | Priority | Status |
|---|---|---|---|---|
| Anthropic interactive tutorial (GitHub) | https://github.com/anthropics/prompt-eng-interactive-tutorial/tree/master/Anthropic%201P | examples | supplementary | pending |
| PromptQuorum: prompt engineering hub | https://www.promptquorum.com/prompt-engineering | examples | supplementary | pending |
| PromptQuorum: local LLMs hub | https://www.promptquorum.com/local-llms | examples | supplementary | pending |
| PromptQuorum: best local LLMs for coding | https://www.promptquorum.com/local-llms/best-local-llms-for-coding | local-llms | supplementary | pending |
| Towards AI: prompt engineering cookbook | https://pub.towardsai.net/the-prompt-engineering-cookbook-principles-tactics-and-patterns-that-actually-work-aa1d60faef99 | library-design | supplementary | pending |

## Status values

- `pending` — approved for scraping, not yet ingested
- `raw` — scraped but not yet normalized
- `normalized` — cleaned markdown in `knowledge/`
- `converted` — artifacts extracted into `schemas/` or `skills/`
- `deprecated` — source is outdated or superseded

## Adding new sources

Before adding:
1. Confirm it is credible, structured, and evidence-based
2. Confirm it is not already covered by an existing foundation source
3. Add it here with status `pending` before scraping
4. Follow the ingestion workflow in `governance/ingestion-workflow.md`
