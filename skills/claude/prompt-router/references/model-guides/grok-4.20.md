---
model: grok-4.20
vendor: xAI
family: Grok
aliases: [grok-4.20-0309-reasoning, grok-4.20-reasoning, grok-4.20-reasoning-latest, grok-4.20-0309, grok-4.20-beta-latest]
last_verified: 2026-10-13
status: current
---

# Grok 4.20

This guide covers the vendor alias `grok-4.20`, which according to xAI points to `grok-4.20-0309-reasoning`. The sibling slugs `grok-4.20-0309-non-reasoning` and `grok-4.20-multi-agent-0309` are separate models with their own behaviour; they are described below but not listed as aliases of this guide.

## Reasoning / Thinking
- Type: **reasoning chosen by model selection, not by parameter.** `grok-4.20-0309-reasoning` carries "Reasoning: Yes", `grok-4.20-0309-non-reasoning` "Reasoning: No" — to turn thinking on or off, switch the slug.
- Effort levels for the reasoning variant: not listed on the model page, and the summary table of the reasoning page does not name them. Whether `reasoning_effort` takes effect, is ignored or raises an error is unverified; the default depth is likewise unverified.
- **Multi-agent variant** (`grok-4.20-multi-agent`): here `reasoning.effort` controls "how many agents collaborate on a request rather than reasoning depth" — `low`/`medium` = 4 agents, `high`/`xhigh` = 16 (in the xAI SDK `agent_count` 4 or 16). The same effort value therefore means something entirely different than on grok-4.5/4.6/4.7.
- Class rule: "`presencePenalty`, `frequencyPenalty`, and `stop` cannot be used with reasoning models. Requests that include them return an error." Reasoning tokens are billed on top.
- xAI describes readable reasoning summaries only for grok-4.7; for grok-4.20 no readable reasoning trace is documented (unverified).

## Prompting Style
- Vendor description: "a high-performance model with industry-leading speed and agentic tool calling capabilities. It combines the lowest hallucination rate on the market with strict prompt adherence" (vendor claim, not independently verified). It follows that instructions should be precise and literal; ambiguity is less likely to be resolved charitably (inference, unverified).
- xAI publishes no model-specific prompting guidance for grok-4.20; any further style claim is unverified.
- Control tool selection via tool descriptions ("helps the model decide when to use it"); parallel tool calling is on, and `parallel_tool_calls: false` turns it off. Enforce format via Structured Outputs (`response_format.type: "json_schema"`, "guaranteed to match your schema", limits 2,048 / 256 / 64).
- Multi-agent: xAI recommends setting the scope explicitly (which dimensions should be covered), requesting structured output such as comparison tables, naming the desired sources/perspectives, splitting deep topics across follow-up turns, and supplying context such as constraints or target market.
- Caching is automatic from the start of the `messages` array; keep the static prefix stable and set `x-grok-conv-id` or `prompt_cache_key`.

## Strengths & Weaknesses (prompt-relevant)
- Strengths: **1M-token context**; inexpensive ($1.25 input / $2.50 output per 1M under 200k, identical for all three variants); **Batch API supported** with a 20% discount; a non-reasoning variant for latency-critical paths; multi-agent for deep research with server-side tools (`web_search`, `x_search`, `code_execution`, `collections_search`, remote MCP).
- Weaknesses/quirks: no documented effort control; no published knowledge cutoff and no output limit; `logprobs`/`top_logprobs` are silently ignored for "`grok-4.20` and newer"; only us-east-1/us-west-2. The model overview recommends grok-4.7 for code and chat, not 4.20.
- Multi-agent additionally: **beta** ("The API interface and behavior may change"); "Client-side tools (function calling) and custom tools are not currently supported"; `max_tokens` not supported; does **not** run over Chat Completions, only the xAI SDK / Responses API; only tool calls and the leader agent's final answer come back; all agent tokens and tool calls are billed; rate limit only 9 rps / 2.5M tpm.

## Output & Format Conventions
- 1,000,000 tokens context (all three variants); input text + image, output text only. Max. output and cutoff: not published (unverified).
- Reasoning variant: function calling yes, structured outputs yes, reasoning yes; non-reasoning: reasoning no; Batch API with 20% discount on all.
- Prices per 1M tokens: input $1.25 (<200k) / $2.50 (≥200k), cached input $0.20 / $0.40, output $2.50 / $5.00; from 200k prompt tokens the higher rate applies to all tokens of the request. Rate limits: 37 rps / 10M tpm (reasoning and non-reasoning), 9 rps / 2.5M tpm (multi-agent). Regions us-east-1, us-west-2.
- Vendor aliases of the reasoning variant include `grok-4.20`, `grok-4.20-reasoning`, `grok-4.20-reasoning-latest`, `grok-4.20-0309`, `grok-4.20-beta-latest`, plus various `…-beta`/`…-experimental-beta` strings; non-reasoning includes e.g. `grok-4.20-non-reasoning`; multi-agent includes e.g. `grok-4.20-multi-agent`, `grok-4.20-multi-agent-latest`.
- Date: the release notes report "Grok 4.20 and Grok 4.20 Multi-agent are live" only under "March" without a year — no reliable release date (unverified).

## Migration Notes
- **TO grok-4.20**: (1) Choose the variant deliberately — reasoning slug for thinking tasks, `grok-4.20-0309-non-reasoning` as the zero-thinking path (instead of a `none` effort). (2) Do not plan on `reasoning_effort` as a depth lever; effect unverified. (3) Remove `presence_penalty`/`frequency_penalty`/`stop` on reasoning and multi-agent slugs; control format via Structured Outputs. (4) Replace logic that relies on `logprobs` — the fields are silently ignored. (5) Formulate instructions literally and completely (strict prompt adherence per the vendor). (6) Batch jobs are possible here and 20% cheaper.
- **Switch to multi-agent**: client functions and custom tools drop out — only server-side tools/remote MCP; rebuild Chat Completions integrations onto the Responses API; remove `max_tokens`; move length control into the prompt or schema; recalculate costs because of parallel agents.
- **AWAY FROM grok-4.20** (to grok-4.7/4.6/4.5): context halves to 500k — check chunking; prices rise to $2/$6 per 1M (<200k); reasoning cannot be switched off there and the effort defaults to `high`, so a non-reasoning path must be moved to `low`. **Re-interpret effort semantics**: a `high`/`xhigh` carried over from multi-agent meant 16 agents; there it means reasoning depth. To grok-4.3: same price level and 1M context, but there `reasoning_effort: none` serves as the zero-thinking path instead of a dedicated slug.

## Sources
- https://docs.x.ai/developers/models/grok-4.20-0309-reasoning — model page: id `grok-4.20-0309-reasoning`, alias list incl. `grok-4.20`, description ("industry-leading speed and agentic tool calling", "lowest hallucination rate on the market with strict prompt adherence"), 1M context, text+image→text, function calling/structured outputs/reasoning yes without effort options, Batch with 20% discount, price table, 37 rps / 10M tpm, us-east-1/us-west-2.
- https://docs.x.ai/developers/models/grok-4.20-0309-non-reasoning — "Reasoning: No", own alias list, same prices, limits and regions.
- https://docs.x.ai/developers/models/grok-4.20-multi-agent-0309 — multi-agent model page: aliases, 1M context, Batch with 20% discount, 9 rps / 2.5M tpm.
- https://docs.x.ai/developers/model-capabilities/text/multi-agent — beta notice, `agent_count` 4/16 and effort mapping, supported server tools, no client functions/custom tools, no `max_tokens`, not over Chat Completions, leader answer only, billing of all agents, prompting recommendations.
- https://docs.x.ai/developers/model-capabilities/text/reasoning — summary table (grok-4.20-multi-agent: "Controls agent count (4 or 16)"), class rule `presencePenalty`/`frequencyPenalty`/`stop`, default `high` and non-disableable reasoning for grok-4.5/4.6/4.7, summaries only grok-4.7.
- https://docs.x.ai/developers/models — price roster, `logprobs` note for "`grok-4.20` and newer", recommendation grok-4.7 for code and chat, comparison values grok-4.3/4.5/4.6/4.7.
- https://docs.x.ai/developers/release-notes — "Grok 4.20 and Grok 4.20 Multi-agent are live" under "March" without a year.
- https://docs.x.ai/developers/migration/may-15-retirement — confirms `none` reasoning effort on grok-4.3 as the zero-thinking target.
- https://docs.x.ai/developers/tools/function-calling — tool descriptions, `parallel_tool_calls: false`.
- https://docs.x.ai/developers/model-capabilities/text/structured-outputs — schema guarantee and limits.
- https://docs.x.ai/developers/advanced-api-usage/prompt-caching — automatic caching, `x-grok-conv-id`, `prompt_cache_key`.
