---
model: perplexity-deep-research
vendor: Perplexity
family: Perplexity
aliases: [perplexity-dr, sonar-deep-research, perplexity-deep, pplx-deep-research, deep-research-perplexity]
last_verified: 2026-11-07
status: current
---

# Perplexity Deep Research (Sonar Deep Research / Agent API, high effort)

> ⚠ The Perplexity docs were checked only via web-search summaries, not fetched directly. Verify effort names and parameters before use (unverified). Per research, the Agent API with `high`/`xhigh` replaces the standalone `sonar-deep-research`.

## Reasoning / Thinking
- Autonomous multi-step research: iterative searching, reading, refining queries, closing gaps, synthesizing many sources (sometimes dozens of tool steps, runtimes of several minutes).
- Agent API: `effort` `high` (expert synthesis, comparison reports) and `xhigh`/`ultra` (exhaustive deep research; name `ultra` unverified).
- Legacy: `sonar-deep-research` with `reasoning_effort` (low/medium/high; unverified).

## Prompting style
- **Rubric instead of question**: give a multi-part goal with structure ("Competitive analysis X vs. Y: 1. positioning, 2. pricing models, 3. releases in the last 6 months").
- Formulate the seed query specifically (technical terms, time periods, entities); the `input` determines the first search.
- `instructions` for standing rules: language, format, citation style (inline domain citations instead of raw URLs), permission to say "no evidence found". Custom `instructions` replace the effort level's default system prompt.
- Control domains, time window and region via `search_domain_filter`, `search_recency_filter`, `search_mode` (`web | academic | sec`), not only via text.
- Limit scope (time period, region, industry), otherwise research sprawls; state priorities and exclusions.
- Do not force citations through prose formatting; phrase instructions around "what to deliver", not "how to search".

## Strengths & weaknesses (prompt-relevant)
- Strengths: broad source coverage, cited report, suited to comparison and market analysis.
- Weaknesses: long runtime, high token/search cost; with vague briefs an unfocused report; latency too high for interactive use.

## Output & format conventions
- Long Markdown report with sources; set the structure as the output contract in the prompt. Check streaming / asynchronous operation per API (unverified).

## Migration notes
- **AWAY FROM Perplexity Deep Research**: keep report structure and source rules as the output contract; move filter parameters into the target's retrieval design; a target without search needs context or a search tool, plus added multi-step instructions.
- **TO Perplexity Deep Research**: condense the prompt into goal + scope + structure + source rules; remove search and CoT instructions; move time/domain constraints into filters; add a "no evidence" clause; set high `effort` and plan for runtime.

## Sources
- https://docs.perplexity.ai — effort levels `high`/`xhigh`, deep-research behavior, `instructions` vs. `input` (summarized via web search).
