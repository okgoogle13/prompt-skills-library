---
model: grok-4.7
vendor: xAI
family: Grok
aliases: [grok, grok4.7, grok-4.7-latest, grok47, grok-4-7, grok4-7]
last_verified: 2026-10-13
status: current
---

# Grok 4.7

## Reasoning / Thinking
- Type: **always on**. The reasoning page lists grok-4.7 with "Reasoning cannot be disabled" — there is no `none` (unlike grok-4.3).
- Ladder: `reasoning.effort` (Responses API) or `reasoning_effort` = `low | medium | high | xhigh`, **default `high`**. `xhigh` controls real reasoning depth here ("available on `grok-4.6` and later") — "Maximum reasoning depth, with correspondingly higher latency".
- Intended use per the docs: `low` for latency-sensitive agentic loops and simple tool calling, `medium` for data analysis and long-context reasoning, `high` for hard maths and multi-step problems, `xhigh` for the hardest cases. The best-practices guide asks you to set effort **explicitly on every request** rather than letting the default decide.
- **Readable reasoning summaries** are documented by xAI only for grok-4.7 (streaming deltas `response.reasoning_summary_text.delta`).
- **Encrypted reasoning always comes back:** on the Responses API grok-4.7 returns `reasoning.encrypted_content` on every response, even without `include`. Reasoning items must be sent back unchanged in `input` of the next request, otherwise the model loses its line of reasoning and the prompt cache breaks. Chat Completions has no field for this.
- Reasoning tokens are billed too (`reasoning_tokens` in `usage`). `presencePenalty`, `frequencyPenalty` and `stop` return an error.

## Prompting style
- Positioning: "frontier model for coding, agentic tasks, and knowledge work"; xAI recommends grok-4.7 for code **and** chat ("It is the most capable model we've built").
- Best-practices guide: **state** the task, constraints and output format directly ("state the task, constraints, and output format directly"); deliberately re-tune a prompt tuned for another model for Grok.
- **Use the Responses API** — per the guide, Chat Completions is "deprecated" and drops encrypted reasoning across turns.
- Sampling: explicitly set `temperature` 0.7 and `top_p` 0.95 and rarely deviate from them ("Grok models don't respond well to other sampling settings").
- Caching: set `prompt_cache_key` (Responses API) or `x-grok-conv-id` (Chat Completions) per conversation; put static content (system prompt, few-shots, reference documents) first, and only append to the conversation instead of reordering it. For long agent loops, also use context compaction.
- Per the announcement the model works longer on hard tasks and checks its work more carefully — planning and self-checking can be left to the model. There is no model-specific prompting guide beyond the best-practices guide; further style rules are (unverified).

## Strengths & weaknesses (prompt-relevant)
- Strengths: per the announcement, a new, larger base model than grok-4.6 with a longer RL run on tasks spanning many hours; better at verifying its own work and at handling long context; better document and presentation creation; same price and speed as grok-4.6; full flagship throughput ceiling (150 rps / 50M tpm).
- Manufacturer-stated benchmarks (not independently verified, `xhigh`): CursorBench 4.0 46.3%, Terminal-Bench 4.0 37.6%, Harvey Legal Agent Benchmark 19.6%; DeepSWE v1.1 71.0% (at `high`).
- Weaknesses/quirks: reasoning cannot be switched off (fixed latency/cost floor); **price cliff at 200k prompt tokens** — from there the doubled rate applies to all tokens in the request; **Batch API "Not supported"**; no EU region.

## Output & format conventions
- 500,000 tokens context; input text + image, output text only; "No text output limit". Knowledge cutoff May 2026.
- `max_output_tokens` limits only the visible response (reasoning does not count), default 128,000; treat responses with `status: "incomplete"` as truncated. Do not control length via `stop`.
- Function calling, structured outputs and reasoning: each yes; server-side tools Web Search, X Search and Code Execution. Real-time knowledge only with search tools enabled.
- Prices per 1M tokens: input $2.00 (<200k) / $4.00 (≥200k), cached input $0.50 / $1.00, output $6.00 / $12.00. Rate limits 150 rps / 50M tpm. Regions us-east-1, us-west-2, us-central-1; additionally US regional endpoint `https://us.api.x.ai/v1` (+10% token price).
- "Grok 4.7 Fast" (same model, double price) exists only in Cursor and Grok Build, **not** on the public xAI API.
- The model page lists no aliases; `grok-4.7-latest` is only a repo convenience following xAI's `<modelname>-latest` convention; the bare ID `grok-4.7` is the verified address.

## Migration notes
- **FROM grok-4.6 to grok-4.7**: price, context (500k), effort ladder and default (`high`) are identical — effort values can be carried over. New: reasoning summaries when streaming, and `reasoning.encrypted_content` always returned on the Responses API; clients that keep their own history must send the reasoning items back unchanged. Knowledge cutoff is newly documented (May 2026).
- **FROM grok-4.3 / grok-4.5 to grok-4.7**: (1) `none` does not exist — lift zero-thinking paths to `low` and recalculate latency/cost. (2) The default jumps from `low` on grok-4.3 to `high`; without an explicit `reasoning_effort`, cost and latency rise. (3) Coming from grok-4.3: context shrinks from 1M to 500k, eu-west-1 and the 20% batch discount drop away, price rises to $2.00/$6.00. (4) Coming from grok-4.5: `xhigh` now actually runs — re-measure cost.
- **TO grok-4.7 in general**: remove `presence_penalty`/`frequency_penalty`/`stop`, control format via structured outputs; move to the Responses API; set `temperature` 0.7 / `top_p` 0.95; add `prompt_cache_key`; keep prompts under the 200k cliff.
- **FROM grok-4.7**: rework pipelines that consume summaries or the automatically returned encrypted reasoning; per the reasoning page, on grok-4.5 `xhigh` is silently treated as `high`.

## Sources
- https://docs.x.ai/developers/models/grok-4.7 — Model page: id `grok-4.7` with no aliases, 500k context, text+image→text, function calling/structured outputs/reasoning yes, efforts `low`/`medium`/`high`/`xhigh` with default `high`, Batch API "Not supported", price table with 200k tier, 150 rps / 50M tpm, regions us-east-1/us-west-2/us-central-1.
- https://docs.x.ai/developers/grok-4-7 — Developer page: knowledge cutoff May 2026, "No text output limit", tools, `prompt_cache_key` recommendation, context compaction, always-returned `reasoning.encrypted_content`, Fast variant only in Cursor/Grok Build, US endpoint +10%, default model of Grok Build.
- https://docs.x.ai/developers/model-capabilities/text/reasoning — "Reasoning cannot be disabled", effort table and use recommendations, `xhigh` from grok-4.6, summaries only for grok-4.7, "Always returned for grok-4.7", errors for `presencePenalty`/`frequencyPenalty`/`stop`, billing of reasoning tokens.
- https://docs.x.ai/developers/model-capabilities/text/best-practices — Responses API instead of (deprecated) Chat Completions, return reasoning items, set effort explicitly, `temperature` 0.7 / `top_p` 0.95, `max_output_tokens` default 128,000, name task/constraints/format directly, caching rules.
- https://docs.x.ai/developers/models — Recommendation "Code: Grok 4.7 / Chat: Grok 4.7", cutoff May 2026, price table, alias convention, real-time knowledge only with search tools.
- https://docs.x.ai/developers/release-notes — "Grok 4.7" entry (September): availability as `grok-4.7`, prices, effort ladder, always-returned encrypted reasoning, US endpoint, Fast variant.
- https://x.ai/news/grok-4-7 — Announcement of 21 Sep 2026: larger base model, longer RL run, better self-verification and long-context handling, same price/speed as grok-4.6, manufacturer benchmarks.
- https://docs.x.ai/developers/advanced-api-usage/regions — US endpoint `https://us.api.x.ai/v1` serves grok-4.7 and grok-4.6, token price +10%.
- https://docs.x.ai/developers/advanced-api-usage/prompt-caching/maximizing-cache-hits — `x-grok-conv-id` or `prompt_cache_key` route a conversation to the same server.
- https://docs.x.ai/developers/advanced-api-usage/context-compaction — Context compaction for long agent loops.
