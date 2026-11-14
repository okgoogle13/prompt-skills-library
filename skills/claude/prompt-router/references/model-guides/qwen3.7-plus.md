---
model: qwen3.7-plus
vendor: Alibaba
family: Qwen
aliases: [qwen3.7-plus-2026-05-26, qwen37-plus, qwen3-7-plus]
last_verified: 2026-10-13
status: current
---

# Qwen3.7-Plus

## Reasoning / Thinking
- Type: **hybrid, on by default** — the deep-thinking page lists the "Qwen3.7 Plus series" (`qwen3.7-plus`, `qwen3.7-plus-2026-05-26`) as "Hybrid thinking mode, thinking mode enabled by default". Turn it off per request with `enable_thinking: false`.
- Parameter placement depends on the SDK: in the OpenAI Python SDK `enable_thinking`/`thinking_budget` go via `extra_body`; in the Node.js SDK as top-level parameters.
- `thinking_budget` caps the reasoning tokens; default per the API reference = the model's maximum chain-of-thought length, per the model page **262,144 tokens** (the console shows a different default of 4,000, range 1–32,768).
- Reasoning comes back in `reasoning_content`; `preserve_thinking` is documented for `qwen3.7-plus` and the snapshot — without the flag, earlier reasoning in the history is ignored.
- Thinking costs context: max input 983,616 tokens in thinking mode versus 991,808 without; max output 131,072 in both modes.
- Anthropic-compatible Messages endpoint: qwen3.7-plus is listed under Qwen-Plus, but the `output_config.effort` values are documented only for qwen3.8-max/-flash (and other providers) — which `effort` values qwen3.7-plus accepts is unverified. There qwen3.7-plus falls under "Other models": `max_tokens` limits only the answer, not the thinking; the page points generically to `thinking.budget_tokens` (itself "to be deprecated").

## Prompting style
- **No model-specific prompting page.** Officially there is only Alibaba's generic prompt-engineering guide: a frame of Context, Objective, Style, Tone, Audience, Response; few-shot examples for consistent form; step lists for complex tasks; rare delimiters (`###`, `===`). Anything beyond that is unverified for this model.
- Thinking runs by default — control depth via `thinking_budget` instead of CoT instructions in the prompt text.
- JSON: in `json_object` mode the word **"JSON"** (case-insensitive) must appear in the system or user message, otherwise an error is raised; in `json_schema` mode it is not required.
- Keep context under 256k tokens where possible: above that the price triples (see output). Put stable content first so the implicit prefix cache (from 1,024 tokens) kicks in.

## Strengths & weaknesses (prompt-relevant)
- Positioning per the model page: cost-efficient Plus model of the Qwen3.7 series with stronger vision-language and agent capabilities for coding, tool use and productivity; core feature "multi‑modal interactive hybrid agent capabilities" — perceive real scenes, read screens and operate GUIs, generate code from visual mockups, navigate mobile apps end to end. Input image/text/video, output text.
- Alibaba's recommendation list features qwen3.7-plus as the Plus text model alongside qwen3.8-max and qwen3.8-flash; a Qwen3.8-Plus is not listed on the official pages.
- Enabled: Function Calling, Prefix Completion and Context Caching in all regions; Structured Outputs and Web Search everywhere **except the US scope**; Batch only Beijing and Singapore; **no fine-tuning**.
- Not published (unverified): knowledge cutoff, recommended sampling parameters, benchmarks versus qwen3.8-max/-flash.

## Output & format conventions
- Context window 1,000,000 tokens; max input 991,808 (without thinking) or 983,616 (with); max output 131,072; max chain-of-thought 262,144.
- **Length-tiered pricing**: up to 256k input tokens e.g. Singapore $0.4 input / $1.6 output per 1M, from 256k to 1M $1.2 / $4.8 — factor 3; the same tier applies to cache prices.
- Structured output: `json_object` (keyword required) or `json_schema` (the Qwen3.7-Plus series is listed among schema-capable models). Limitations: in the US scope the model page lists no structured outputs at all; the structured-output page lists `json_schema` for Singapore as "not supported yet" (the model page marks Singapore as supported — contradictory, test before production); multimodal inputs automatically fall back to `json_object`, without a schema guarantee. Anthropic endpoint: strict `json_schema` enforcement for the Qwen3.7 series.
- Prefix completion (partial mode): last assistant message with `partial: true`; documented under "Qwen-Plus (non-thinking mode): Qwen3.7-Plus series" — so only with `enable_thinking: false`.
- Context cache: implicitly active by default and cannot be disabled, minimum prefix 1,024 tokens; explicit via `cache_control: {"type": "ephemeral"}`, valid for 5 minutes with reset on hit.
- IDs: `qwen3.7-plus` (per the model page functionally identical to the snapshot `qwen3.7-plus-2026-05-26`). The docs URL slug `qwen3-7-plus` is **not** the API id. Anthropic endpoint: no `/v1/models`, configure the id manually.

## Migration notes
- **TO qwen3.7-plus**: **thinking runs by default** — prompts from non-thinking models gain latency and reasoning cost; set `enable_thinking: false` or size `thinking_budget` and strip CoT instructions from the prompt. Assistant prefill works only with thinking disabled. Large contexts above 256k cost three times as much — design retrieval/chunking so requests stay below that. From Claude prompts: do not carry over `effort` levels blindly (for qwen3.7-plus: unverified); on the Anthropic endpoint `max_tokens` covers only the response. Strict schemas are unavailable in the US scope and with image/video input.
- **AWAY FROM qwen3.8-max or -flash, up or down**: the same OpenAI/DashScope parameters (`enable_thinking`, `thinking_budget`, `preserve_thinking`) and the same limits (1M / 131,072 / 262,144); differences lie in the length-tier pricing, the documented partial mode and the Anthropic `effort` values (documented for 3.8, not here).
- **AWAY FROM qwen3.7-plus**: `enable_thinking`, `thinking_budget`, `preserve_thinking`, `reasoning_content`, `partial: true` and `cache_control` are specific to Model Studio — re-map them against the target guide rather than copying 1:1. The "JSON" keyword requirement is a Qwen quirk; check the target's schema dialect. Whether the target handles GUI/screen-agent tasks is stated in the target guide, not here.
- Not to be confused: `qwen-plus` is a separate, still-offered model (functionally `qwen-plus-2025-12-01`, max output 32,768, thinking **off** by default per the deep-thinking page) and **not** an alias of qwen3.7-plus.

## Sources
- https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus — model page: ids `qwen3.7-plus` / snapshot `qwen3.7-plus-2026-05-26` (functionally identical), positioning as a cost-efficient Plus model with "multi‑modal interactive hybrid agent capabilities" (GUI, screens, mobile apps, code from images), input image/text/video → text, 1M context, max input 991,808 / 983,616, output 131,072, CoT 262,144, feature table per region (US scope without structured outputs/web search, batch only Beijing/Singapore, no fine-tuning), price tiers ≤256k vs. 256k–1M.
- https://www.alibabacloud.com/help/en/model-studio/newly-released-models — entry 1 Jun 2026 `qwen3.7-plus`, `qwen3.7-plus-2026-05-26`: cost-efficient Plus model of the Qwen3.7 series; no Qwen3.8-Plus listed.
- https://www.alibabacloud.com/help/en/model-studio/models — recommended text models: qwen3.8-max, qwen3.7-plus, qwen3.8-flash.
- https://www.alibabacloud.com/help/en/model-studio/deep-thinking — "Qwen3.7 Plus series (Hybrid thinking mode, thinking mode enabled by default)", `preserve_thinking` for qwen3.7-plus and snapshot, `thinking_budget` default = max CoT (console: 4,000), `extra_body` vs. top-level, qwen-plus "thinking mode not enabled by default".
- https://www.alibabacloud.com/help/en/model-studio/anthropic-api-messages — qwen3.7-plus listed under Qwen-Plus; `effort` values documented only for other models; "Other models": `max_tokens` does not limit thinking; strict `json_schema` enforcement for the qwen3.7 series; no `/v1/models`.
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output — Qwen3.7-Plus series among the `json_schema` models; Singapore "not supported yet"; multimodal inputs fall back to `json_object`; "JSON" keyword requirement.
- https://www.alibabacloud.com/help/en/model-studio/partial-mode — "Qwen-Plus (non-thinking mode): Qwen3.7-Plus series", `partial: true` on the last assistant message.
- https://www.alibabacloud.com/help/en/model-studio/context-cache — qwen3.7-plus in the cache lists, minimum prefix 1,024 tokens, implicit cache not disableable, explicit cache 5 minutes with reset on hit.
- https://www.alibabacloud.com/help/en/model-studio/qwen-plus — versionless id `qwen-plus` = `qwen-plus-2025-12-01`, max output 32,768; separate model.
- https://www.alibabacloud.com/help/en/model-studio/prompt-engineering-guide — generic, not model-specific prompt frame (Context, Objective, Style, Tone, Audience, Response), few-shot, step lists, delimiters.
