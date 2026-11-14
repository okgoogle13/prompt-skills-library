---
model: grok-4.6
vendor: xAI
family: Grok
aliases: [grok4.6, grok-4.6-latest, grok46, grok-4-6, grok4-6]
last_verified: 2026-10-13
status: current
---

# Grok 4.6

## Reasoning / Thinking
- Type: **always on**. For `grok-4.6` (as for `grok-4.5` and `grok-4.7`) the docs state "Reasoning cannot be disabled" — there is no `none`. Depth is controlled only via `reasoning_effort` (Chat Completions) or `reasoning.effort` (Responses API): `low | medium | high | xhigh`, default `high`.
- Intended use per the docs: `low` for latency-sensitive agentic loops and simple tool calling, `medium` for complex data analysis and long-context reasoning, `high` for very hard problems, maths and multi-step logic, `xhigh` for the hardest cases where quality matters more than response time.
- According to the reasoning page, `xhigh` controls real reasoning depth on "`grok-4.6` and later" (so also `grok-4.7`); `grok-4.20-multi-agent` uses it to control the number of agents. On `grok-4.5`, `xhigh` is **silently treated as `high`** per the reasoning page — no error, just less thinking time.
- Reasoning tokens are counted in and appear as `reasoning_tokens` in `usage`. xAI only documents readable reasoning summaries for `grok-4.7`; for grok-4.6 this is (unverified). What is verified is the encrypted carry-over via `include: ["reasoning.encrypted_content"]` (Responses API); returning the raw chain of thought is documented nowhere (unverified).
- `presence_penalty`, `frequency_penalty` and `stop` **cannot be combined** with reasoning models — requests containing them return an error (the docs write them as `presencePenalty`/`frequencyPenalty`).

## Prompting style
- Positioning: "frontier model for coding, agentic tasks, and knowledge work"; for code and chat xAI now recommends `grok-4.7`. Trained on agentic RL tasks (knowledge work, general coding, kernel optimisation, web development, CAD).
- Prompt at the **goal level** rather than step by step: per the announcement, it is strong at turning a rough product idea into a first runnable version (researching an unknown domain, structuring the app, building core features) and at running "more self-testing and verification" over long task chains — so leave planning and self-checking to the model.
- **Caching is the central operational prompt rule**: set `prompt_cache_key` (Responses API) or header `x-grok-conv-id` (Chat Completions) so requests in one conversation route to the same server — cache entries live per server. Keep the prompt prefix stable.
- For long agent loops, also plan for context compaction; server-side search tools (Web Search, X Search) must be explicitly enabled, otherwise the model has no real-time knowledge.
- Beyond these documented points xAI publishes no prompt engineering guide for this model — further style rules are (unverified).

## Strengths & weaknesses (prompt-relevant)
- Strengths: agentic coding and knowledge work in the top group; Artificial Analysis Intelligence Index 61 (Fable 5 Max leads the announcement's table with 62); best listed value on Harvey LAB (15.8%); research in unknown domains; very high throughput (150 rps / 50M tokens per minute).
- Weaknesses/quirks: reasoning cannot be switched off → a fixed latency and cost floor; on the announcement's coding benchmarks other models lead (DeepSWE v1.1 65.9% vs. GPT-5.6 Sol Max 73%; FrontierCode v1.1 61.3% vs. Fable 5 Max 63.6%; CursorBench v3.2 69.9% vs. Fable 5 Max 70.5%).
- **200k price cliff**: once the prompt reaches 200k tokens, the entire request (input *and* output) is billed at double the rate — keep context deliberately below the threshold.
- 500k context is only half of `grok-4.3` (1M); regions `us-east-1`, `us-west-2` and `us-central-1` — no EU region (`grok-4.3` has `eu-west-1` for that); additionally US regional endpoint `https://us.api.x.ai/v1` (+10% token price).

## Output & format conventions
- Context window 500,000 tokens; input text + image, output text only. Knowledge cutoff: not published (unverified). Function calling, structured outputs and reasoning: each yes.
- Batch API: "Not supported" per the model page — batch jobs must run as real-time requests.
- Output limit: the release notes explicitly state "no text output limit"; no max-output figure is published. Therefore limit length via max tokens — `stop` sequences are not allowed here.
- Prices per 1M tokens: input $2.00 (<200k) / $4.00 (≥200k), cached input $0.50 / $1.00, output $6.00 / $12.00. The announcement additionally mentions a "fast variant" at double the price.
- Alias convention: `<modelname>` = newest stable version, `<modelname>-latest` = newest version, `<modelname>-<date>` = pinned release. For Grok 4.6 neither a dated ID nor a `-latest` alias is published; the bare ID `grok-4.6` is the only verified address. `grok-4.6-latest` appears in the registry only as a convenience alias following xAI's `<modelname>-latest` convention.

## Migration notes
- **FROM Grok 4.6**: target `grok-4.7` (recommended by xAI for code and chat) has identical price, context and the same effort ladder with default `high`; there `reasoning.encrypted_content` comes back on every response on the Responses API — send reasoning items back unchanged in the next `input`. Target `grok-4.5`: remove `xhigh`, it is silently downgraded to `high` per the reasoning page. Target `grok-4.3` brings 1M context, a `none` effort level (default there `low`), `eu-west-1` and a batch discount, but leaves the frontier coding tier. In all cases check `prompt_cache_key`/`x-grok-conv-id` assumptions.
- **TO Grok 4.6 migrating** (typically from `grok-4`, which has been deprecated since 15 May 2026 12:00 PT and is redirected to `grok-4.3` with `low` effort): (1) set `reasoning_effort` explicitly instead of budgeting thinking depth indirectly via max_tokens — default is `high`, `low` for tool loops, `xhigh` for maximum depth. (2) Structure long prompts to stay clear of the 200k price cliff, even though 500k context is available. (3) Add `prompt_cache_key` or `x-grok-conv-id` plus context compaction for long agent runs — a new operational surface. (4) Carry encrypted reasoning across turns via `include`. (5) Keep `presence_penalty`/`frequency_penalty`/`stop` out of requests. (6) Web/X search are server-side tools that must still be requested explicitly. (7) Drop over-prescriptive step lists; instead give goal + constraints, and the model verifies itself. (8) Re-plan batch jobs — the Batch API does not serve grok-4.6.

## Sources
- https://docs.x.ai/developers/models/grok-4.6 — Model spec: ID `grok-4.6` with no aliases, blurb "frontier model for coding, agentic tasks, and knowledge work", 500k context, text+image→text, function calling/structured outputs/reasoning, efforts `low`–`xhigh` with default `high`, Batch API "Not supported", full price table incl. 200k cliff, 150 rps / 50M tpm, regions us-east-1, us-west-2 and us-central-1.
- https://docs.x.ai/developers/model-capabilities/text/reasoning — Reasoning contract: cannot be switched off, effort table for grok-4.7/4.6/4.5/4.20-multi-agent, `xhigh` "available on `grok-4.6` and later" and silently downgraded to `high` on grok-4.5, summaries only for grok-4.7, `include: ["reasoning.encrypted_content"]`, `reasoning_tokens`, unsupported sampling parameters (`presencePenalty`/`frequencyPenalty`/`stop`).
- https://docs.x.ai/developers/release-notes — "Grok 4.6" entry (August): 500k context, "no text output limit", prices, effort low/medium/high (default)/xhigh.
- https://docs.x.ai/developers/models — Recommendation "Code: Grok 4.7 / Chat: Grok 4.7", cutoff named only for Grok 4.7, alias convention (`-latest`, `-<date>`), real-time knowledge only with search tools enabled.
- https://docs.x.ai/developers/advanced-api-usage/regions — US endpoint `https://us.api.x.ai/v1` serves grok-4.7 and grok-4.6, token price +10%.
- https://docs.x.ai/developers/advanced-api-usage/prompt-caching/maximizing-cache-hits — `x-grok-conv-id` (Chat Completions) or `prompt_cache_key` (Responses API) route a conversation to the same server; cache entries live per server.
- https://docs.x.ai/developers/advanced-api-usage/context-compaction — Context compaction for long agent loops.
- https://docs.x.ai/developers/models/grok-4.7 — Comparison model: identical price, 500k context, same effort ladder with default `high`.
- https://docs.x.ai/developers/models/grok-4.3 — Comparison model: `grok-4.3` with 1M context, region `eu-west-1`, Batch API supported, default effort `low`.
- https://x.ai/news/grok-4-6 — Announcement (12 Aug 2026): agentic RL training (knowledge work, coding, kernel optimisation, web, CAD), "more self-testing and verification" over long task chains, product idea→first version, Intelligence Index 61 (Fable 5 Max 62), Harvey LAB 15.8% (best value), DeepSWE/FrontierCode/CursorBench comparison, $2/$6 per 1M tokens plus "fast variant" at double the price.
- https://docs.x.ai/developers/migration/may-15-retirement — Retirement table: `grok-4-0709` deprecated 15 May 2026 12:00 PT, routing to `grok-4.3` with `low` effort; `none` effort for other redirect targets verified.
