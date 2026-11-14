---
model: gpt-6-sol
vendor: OpenAI
family: GPT
aliases: [gpt6-sol, 6-sol]
last_verified: 2026-10-13
status: current
---

# GPT-6 Sol

## Reasoning / Thinking
- `reasoning.effort` (Responses) or `reasoning_effort` (Chat Completions) accepts `none | low | medium (Default) | high | xhigh | max`. Unlike GPT-6 Astra and GPT-6.1 Sol, GPT-6 Sol explicitly supports `none`; `minimal` is not listed.
- `reasoning.mode`: `standard` (Default) or `pro` — per the reasoning guide, supported for GPT-5.6 and GPT-6 models in the Responses API; mode and effort are independent, and pro tokens are billed at the standard rates.
- `reasoning.context`: the docs list `all_turns` support only for GPT-5.6 models and GPT-6.1 Sol; for GPT-6 Sol it is not documented (unverified) — check the effective mode in the `reasoning.context` field of the response rather than assuming reasoning persistence across turns.
- Mid-conversation effort changes via `configuration_update` are documented for "the GPT-6 model family in standard, single-agent mode"; the docs do not name GPT-6 Sol explicitly as included (unverified).

## Prompting Style
- No dedicated prompting guide for GPT-6 Sol. The GPT-6 prompts count as "a starting point across the GPT-6 model family", but address "behavior observed with GPT-6 Astra" — any transfer to GPT-6 Sol is (unverified) and must be checked with evals.
- Building blocks from this guide, if the evals support them: grant autonomy explicitly ("bias towards action"), request approval only after a "concrete, reviewable result", spell out precedence of user instructions over skills, explicitly request prose, limit test scope for small changes.
- Tie tool instructions to the API path: built-in tools and function calling run through the Responses API; in Chat Completions only function calling and only with `reasoning_effort: "none"`.

## Strengths & Weaknesses (prompt-relevant)
- Positioning: "Built to power complex coding and agentic workflows". In the model catalogue under "More models", not in the flagship group; the model page points to "GPT-6.1 Sol … for the newer Sol model".
- OpenAI names `gpt-6-sol` as the recommended replacement for the deprecated `gpt-5.1` and `gpt-5.3-codex` (shutdown 1 Apr 2027) — a typical migration target from older coding setups.
- Advantage over 6.1 Sol: the `none` effort as a low-latency path, and function calling in Chat Completions (only with `none`).
- Quirks: on 25 Sep 2026 OpenAI fixed an image-encoding bug that had degraded image understanding; re-run evals with image input from the earlier period. Multi-agent beta and Ultrafast mode are listed on the fetched pages only for other models (including GPT-6.1 Sol), not for GPT-6 Sol.
- Not supported: Realtime, Assistants, fine-tuning, embeddings, image/video/audio endpoints, moderation, legacy completions.

## Output & Format Conventions
- Context window **1,050,000** tokens, max. input **922,000**, max. output **128,000**; knowledge cutoff **20 Apr 2026**; input text + image, output text only. Only snapshot: `gpt-6-sol`.
- Endpoints: `v1/chat/completions`, `v1/responses`, `v1/batch`. Features: streaming, structured_outputs, function_calling, file_search, image_input, web_search, prompt_caching. Hosted tools (Responses): web_search, file_search, image_generation, code_interpreter, hosted_shell, apply_patch, skills, computer_use, mcp, tool_search.
- Prices per 1M tokens: input $2, cached input $0.2 (10% of the input rate), cache writes $2.5 (1.25x), output $10. Above 272K input tokens: 2x input/cache rates and 1.5x output for the entire request. Batch/Flex 50%, Fast 2x; EU data residency with Standard, Fast, Flex and Batch (+10% regional surcharge).
- Prompt caching follows the rules for "GPT-5.6 and later": lifetime via `prompt_cache_options.ttl` (`"30m"`), not `prompt_cache_retention`.

## Migration Notes
- **AWAY FROM gpt-6-sol**: map effort onto the target guide's ladder; carry over `none` only if the target documents it. Chat Completions function calling with `none` breaks on targets that allow tools only via Responses. Rewrite `reasoning.mode`, `configuration_update` and `prompt_cache_options.ttl` into target equivalents; scale the 1.05M-token context budget back to the target window.
- **TO gpt-6.1-sol** (per OpenAI "the newer Sol model"): OpenAI requires "review the migration guidance before switching to GPT-6.1 Sol". (1) `none` → `low`; start `minimal` with `low`. (2) Move function calling from Chat Completions to the Responses API. (3) With effort ≠ `none`, remove `temperature`, `top_p`, `top_logprobs` (and additionally `logprobs` on Chat Completions). (4) Newly usable: multi-agent beta, Ultrafast mode, `all_turns`.
- **TO gpt-6-sol** (e.g. from `gpt-5.1` or `gpt-5.3-codex`, official replacement): set effort explicitly (default `medium`); move tool workloads with reasoning to the Responses API; per the GPT-6 migration guide, remove sampling parameters and logprobs when effort ≠ `none`; coming from GPT-5.5 or earlier, `prompt_cache_retention` → `prompt_cache_options.ttl: "30m"`.

## Sources
- https://developers.openai.com/api/docs/models/gpt-6-sol — model page: id/snapshot `gpt-6-sol`, "Built to power complex coding and agentic workflows", reference to GPT-6.1 Sol as "newer Sol model", effort levels `none`…`max` (default `medium`), function calling in Chat Completions only with `none`, EU residency, 1,050,000 / 922,000 / 128,000, cutoff 20 Apr 2026, prices and factors, endpoints, features, tools.
- https://developers.openai.com/api/docs/guides/latest-model — "Using GPT-6" (rolling page, as of 2026-10-13): note "If you already use `gpt-6-sol`, review the migration guidance before switching to GPT-6.1 Sol", limitations (`none` supported on GPT-6 Sol), migration quickstart (tool calling, unsupported parameters, `prompt_cache_options.ttl`), prompting best practices with Astra reference.
- https://developers.openai.com/api/docs/guides/reasoning — default `medium` for GPT-6 Sol, `reasoning.mode` for GPT-5.6/GPT-6, `all_turns` support listed only for GPT-5.6 and GPT-6.1 Sol, `configuration_update` for the GPT-6 family.
- https://developers.openai.com/api/docs/deprecations — entry 1 Oct 2026: `gpt-5.3-codex` and `gpt-5.1` → `gpt-6-sol`, shutdown 1 Apr 2027.
- https://developers.openai.com/api/docs/models/all — placement under "More models"; flagship group = GPT-6 Astra / GPT-6.1 Sol / GPT-6 Luna.
- https://developers.openai.com/api/docs/guides/prompt-caching — `prompt_cache_options.ttl` (`"30m"`) for GPT-5.6 and later.
- https://developers.openai.com/api/docs/guides/responses-multi-agent — multi-agent beta listed for GPT-6.1 Sol and GPT-5.6, not for GPT-6 Sol.
- https://developers.openai.com/api/docs/changelog — 22 Sep 2026: release of `gpt-6-sol` (Responses and Chat Completions, $2 / $0.20 / $10); 25 Sep 2026: fix of the image-encoding bug for GPT-6 Sol/Luna.
