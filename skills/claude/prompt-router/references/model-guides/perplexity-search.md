---
model: perplexity-search
vendor: Perplexity
family: Perplexity
aliases: [perplexity, perplexity-standard, perplexity-standard-search, sonar, sonar-pro, perplexity-sonar, pplx-search]
last_verified: 2026-11-07
status: current
---

# Perplexity Standard Search (Sonar / Agent API, low effort)

> ⚠ The Perplexity docs were only checked via web search summaries, not fetched directly. Verify the parameter names (`effort`, `reasoning.effort`, `search_mode`, `search_domain_filter`, `search_recency_filter`) against the current docs before use (unverified). According to research, the Agent API replaces the older Sonar chat-completions models.

## Reasoning / Thinking
- Standard search = fast, live-sourced web grounding with inline citations; legacy models `sonar`, `sonar-pro`.
- Agent API: `effort` bundles model, search, tools and step limits: `fast` (single fact, definitions), `low` (everyday research, light multi-step search), `medium` (general-purpose default). Standard search corresponds to `fast`–`medium`.
- Separate from this: `reasoning.effort` controls internal thinking depth (provider-dependent, unverified).

## Prompting style
- **Short, atomic, specific**: The `input` seeds the first search query. Weak: "Tell me something about Apple's revenue"; better: "Apple FY2025 10-K revenue by segment".
- **One question per request**; split multi-part tasks into separate requests. Overloaded multi-instruction prompts lead to confused search paths at low effort.
- `instructions` (system level) for role, format, language and grounding rules; your own `instructions` **replace** the default system prompt of the effort level.
- **Anti-hallucination**: explicitly allow answering with "no sufficient evidence found".
- **Don't force citations via prose**: don't fight the native citation formats; control domains via `search_domain_filter`, time relevance via `search_recency_filter` (e.g. `week`, `month`) instead of just writing "current" in the text.
- `search_mode`: `web` (default), `academic`, `sec`.
- No few-shot/CoT needed; the prompt text should contain search terms, not instructions about searching.

## Strengths & weaknesses (prompt-relevant)
- Strengths: speed, current sources, inline citations.
- Weaknesses: shallow analysis on complex questions; poor results with vague prompts; no deep multi-source synthesis (use `perplexity-deep-research` for that).

## Output & format conventions
- Answer with citations/source list; set the format (list, table, short paragraphs) in `instructions`.
- Structured outputs: check availability per model (unverified).

## Migration notes
- **FROM Perplexity Search**: translate the search filter parameters into the target's tool/retrieval configuration; keep the "only verified facts" note; if the target has no web search, add a search tool or context.
- **TO Perplexity Search**: shorten the prompt to a concrete, search-term-rich question; remove CoT/role-play; move source/time requirements into filter parameters; add a "no evidence found" clause; set the format in `instructions`.

## Sources
- https://docs.perplexity.ai — Agent API, effort levels `fast/low/medium`, `instructions` vs. `input`, prompt tips (summarised via web search).
