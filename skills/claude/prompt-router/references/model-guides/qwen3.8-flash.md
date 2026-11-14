---
model: qwen3.8-flash
vendor: Alibaba
family: Qwen
aliases: [qwen38-flash, qwen3-8-flash]
last_verified: 2026-10-13
status: current
---

# Qwen3.8-Flash

## Reasoning / Thinking
- Type: **hybrid, on by default** — the deep-thinking page lists the "Qwen3.8 Flash series" as "Hybrid thinking mode, thinking mode enabled by default". A request without a thinking field thinks; turn it off per request with `enable_thinking: false`.
- Parameter placement depends on the SDK: in the OpenAI Python SDK `enable_thinking`/`thinking_budget` go via `extra_body`; in the Node.js SDK as top-level parameters.
- `thinking_budget` caps the reasoning tokens; default per the API reference = the model's maximum chain-of-thought length, for qwen3.8-flash **262,144 tokens** (the console shows a different default of 4,000, range 1–32,768).
- Reasoning comes back in `reasoning_content`, the answer in `content`. `preserve_thinking` is explicitly documented for qwen3.8-flash — without the flag, earlier reasoning in the history is ignored.
- Thinking costs context: max input 983,616 tokens in thinking mode versus 991,808 without; max output 131,072.
- Anthropic-compatible Messages endpoint: `thinking: {type: "enabled" | "disabled"}`; depth via `output_config.effort`, for qwen3.8-flash default `xhigh`, valid `xhigh`/`medium`/`low`; `max` and `high` map to `xhigh`. `budget_tokens` is "to be deprecated". There `max_tokens` covers the answer **and** the chain of thought together for qwen3.8-flash. What happens on this endpoint when the `thinking` field is missing is not stated on the page (unverified).

## Prompting style
- **No model-specific prompting page.** Officially there is only Alibaba's generic prompt-engineering guide: a frame of Context, Objective, Style, Tone, Audience, Response; few-shot examples for consistent form; step lists for complex tasks; rare delimiters (`###`, `===`) for separation. Anything beyond that is unverified for this model.
- Because thinking runs by default, control depth via `thinking_budget` or `effort` instead of "think step by step" scaffolding in the prompt text.
- JSON: in `json_object` mode the word **"JSON"** (case-insensitive) must appear in the system or user message, otherwise an error is raised; in `json_schema` mode it is not required.
- Build for caching: recurring content first, variable content last (implicit prefix cache from 1,024 tokens).

## Strengths & weaknesses (prompt-relevant)
- Positioning per the release note: "the latest multimodal model from the Qwen family"; input image/text/video, output text; "fully compatible with both OpenAI and Anthropic API protocols" (the model page names Claude Code and Codex as integrated developer tools).
- The cheapest of the three Qwen text tiers that Alibaba's recommendation list features (qwen3.8-max, qwen3.7-plus, qwen3.8-flash); price without length tiers across the full 1M window (reference Beijing/Global $0.113 input / $0.382 output per 1M tokens).
- Enabled per the model page: Function Calling, Structured Outputs, Partial Mode and Context Cache in all regions; Web Search only Beijing and Singapore; Batch only Beijing; **no fine-tuning**.
- Open base: the official Qwen model card calls qwen3.8-flash "the official version based on Qwen3.8-Flash-Next with more production features". The open model natively has 262,144 context (up to 1M via YaRN); its sampling recommendations (thinking: `temperature` 1.0, `top_p` 0.95, `top_k` 20; non-thinking: 0.7 / 0.80 / 20, `presence_penalty` 1.5) apply to the open weights — whether they apply to the hosted API is unverified.
- Not published (unverified): knowledge cutoff, pinned snapshot ids, benchmarks versus qwen3.8-max.

## Output & format conventions
- Context window 1,000,000 tokens; max input 991,808 (without thinking) or 983,616 (with); max output 131,072; max chain-of-thought 262,144.
- Structured output: `response_format` with `json_object` (keyword required) or `json_schema` (the Qwen3.8-Flash series is listed among schema-capable models). Limitations per the structured-output page: `json_schema` for models in the Singapore region is "not supported yet" (the model page marks structured outputs there as supported — contradictory, test before production); multimodal inputs automatically fall back to `json_object`, without a schema guarantee. Anthropic endpoint: `output_config.format` with strict enforcement for the Qwen3.8 series.
- Partial mode (prefix completion): the model page marks it as supported, but the partial-mode page does not list qwen3.8-flash and documents Qwen prefill only for non-thinking mode — prefill combined with thinking is unverified.
- Context cache: implicitly active by default and cannot be disabled, minimum prefix 1,024 tokens; explicit via `cache_control: {"type": "ephemeral"}`, valid for 5 minutes with reset on hit.
- IDs: `qwen3.8-flash` (Model Studio names no dated snapshots). The docs URL slug `qwen3-8-flash` is **not** the API id. Anthropic endpoint: only `/v1/messages`, no `/v1/models` — configure the id manually.

## Migration notes
- **TO qwen3.8-flash**: the most important break — **thinking runs unless `enable_thinking: false` is set.** For prompts from non-thinking models: re-size latency, cost and `max_tokens` (on the Anthropic endpoint the chain of thought consumes the same `max_tokens`), strip explicit CoT requests and control depth via `thinking_budget`/`effort`. From Claude prompts: replace `budget_tokens` with `output_config.effort`; `high`/`max` land on `xhigh` (default, highest level); set moderate depth explicitly to `medium`. Assistant prefill: set `enable_thinking: false` or switch to structured output (strict only without image/video input). Multi-turn: `preserve_thinking` decides whether earlier reasoning arrives.
- **AWAY FROM qwen3.8-max**: same parameter surface (`enable_thinking`, `thinking_budget` with the same 262,144 default, `preserve_thinking`, `effort` scale, 1M window, 131,072 output) — the prompt can stay structurally the same; quality differences between Max and Flash are not officially quantified (unverified), so test on your own eval set. Web Search is missing outside Beijing and Singapore.
- **AWAY FROM qwen3.8-flash**: `enable_thinking`, `thinking_budget`, `preserve_thinking`, `reasoning_content`, `partial: true` and `cache_control` are specific to Model Studio — re-map them against the target guide rather than copying 1:1. The "JSON" keyword requirement is a Qwen quirk; check the target's schema dialect. The 1M window shrinks on many targets — redesign chunking; video input often drops out.
- Not to be confused: `qwen-flash` is a separate, still-offered model (functionally `qwen-flash-2025-07-28`, max output 32,768, thinking **off** by default per the deep-thinking page) and **not** an alias of qwen3.8-flash.

## Sources
- https://www.alibabacloud.com/help/en/model-studio/qwen3-8-flash — model page: 1M context, max input 991,808 / 983,616 (thinking), max output 131,072, max CoT 262,144, input image/text/video → text, OpenAI and Anthropic compatibility, Claude Code/Codex; feature table per region (function calling, structured outputs, partial mode, context cache everywhere; web search only Beijing/Singapore; batch only Beijing; no fine-tuning); prices per region without length tiers; no knowledge cutoff, no snapshot ids.
- https://www.alibabacloud.com/help/en/model-studio/newly-released-models — entry 26 Aug 2026 `qwen3.8-flash`: "the latest multimodal model from the Qwen family", OpenAI- and Anthropic-compatible.
- https://www.alibabacloud.com/help/en/model-studio/models — recommended text models: qwen3.8-max, qwen3.7-plus, qwen3.8-flash.
- https://www.alibabacloud.com/help/en/model-studio/deep-thinking — "Qwen3.8 Flash series (Hybrid thinking mode, thinking mode enabled by default)", `preserve_thinking` for qwen3.8-flash, `thinking_budget` default = max CoT (console: 4,000), `extra_body` (Python) vs. top-level (Node.js), qwen-flash "thinking mode not enabled by default".
- https://www.alibabacloud.com/help/en/model-studio/anthropic-api-messages — qwen3.8-flash listed under Qwen-Flash; `output_config.effort` default xhigh, values xhigh/medium/low, max/high → xhigh; `budget_tokens` "to be deprecated"; `max_tokens` covers answer and chain of thought for qwen3.8-flash; strict `json_schema` enforcement for the qwen3.8 series; no `/v1/models`.
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output — Qwen3.8-Flash series among the `json_schema` models; Singapore "not supported yet"; multimodal inputs fall back to `json_object`; "JSON" keyword requirement in `json_object` mode.
- https://www.alibabacloud.com/help/en/model-studio/partial-mode — list of partial-mode models (Qwen-Flash only up to Qwen3.7-Flash, each non-thinking); qwen3.8-flash not listed.
- https://www.alibabacloud.com/help/en/model-studio/context-cache — qwen3.8-flash in the cache lists, minimum prefix 1,024 tokens, implicit cache not disableable, explicit cache 5 minutes with reset on hit.
- https://www.alibabacloud.com/help/en/model-studio/qwen-flash — versionless id `qwen-flash` = `qwen-flash-2025-07-28`, max output 32,768; separate model.
- https://www.alibabacloud.com/help/en/model-studio/prompt-engineering-guide — generic, not model-specific prompt frame (Context, Objective, Style, Tone, Audience, Response), few-shot, step lists, delimiters.
- https://huggingface.co/Qwen/Qwen3.8-Flash-Next — official Qwen model card of the open base model: qwen3.8-flash as the "official version based on Qwen3.8-Flash-Next", native 262,144 context (YaRN up to 1M), sampling recommendations for thinking/non-thinking.
