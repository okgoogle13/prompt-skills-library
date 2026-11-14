---
model: deepseek-v4.1-flash
vendor: DeepSeek
family: DeepSeek
aliases: [deepseek-flash, v4.1-flash, deepseek-v4-1-flash]
last_verified: 2026-10-13
status: current
---

# DeepSeek-V4.1-Flash

## Reasoning / Thinking
- **One hybrid model behind `deepseek-flash`** (model version DeepSeek-V4.1-Flash): non-thinking and thinking in one ID; thinking is **on by default** (default effort `high`). OpenAI format: `thinking: {"type": "enabled"|"disabled"}` (in the OpenAI SDK via `extra_body`) plus `reasoning_effort` `none|low|high|max` (`none` = thinking off). Anthropic format: the same `thinking` switch (`budget_tokens` is ignored), effort via `output_config: {"effort": "low|high|max"}`. Responses API: `reasoning: {"effort": "none|low|high|max"}`.
- Effort mapping for requested levels: minimal→low, low→low, medium→high, high→high, **xhigh→high**, max→max, ultra→max. `/models` reports the levels `low|high|max` for `deepseek-flash`, default `high`.
- On the model side, effort is a **numeric budget of 1–100** (low = 50, high = 75, max = 100), rendered as a `<｜System｜>Reasoning Effort: {budget} (range 1-100, …)` prefix — only in thinking mode and only at the start of the conversation. The API offers only low/high/max; intermediate values via the API are not documented (unverified).
- `reasoning_content` comes alongside `content`. Without `tools` it need not be sent back (the API ignores it); **with `tools`** the `reasoning_content` of all prior turns must be returned to the API in full — including for turns without a tool call — otherwise HTTP 400.
- Sampling: in thinking mode `temperature`, `presence_penalty`, `frequency_penalty` have no effect (no error). `top_p` acts **only** in thinking mode (effectively 0.95–1.0, smaller values → 0.95); in non-thinking mode it is fixed at 1.0.
- `tool_choice: required` or a named tool returns HTTP 400 in thinking mode — forcing a tool works only with `thinking: {"type": "disabled"}`.

## Prompting style
- System prompt sits directly after BOS: `<｜begin▁of▁sentence｜>{system}<｜User｜>{user}<｜Assistant｜>`; in thinking mode the template places the effort prefix before it as a `<｜System｜>` block. **New compared with V4:** system messages in the middle of the conversation (`<｜System｜>`). On the Anthropic messages endpoint, `/models` reports `system_prompt_update: in-history` — the last system message in the conversation is the complete effective system prompt and replaces all earlier ones.
- **JSON needs three things**: `response_format: {"type": "json_object"}`, the word "json" plus an example of the target format in the system or user prompt, and enough `max_tokens`. Without a JSON instruction in the prompt the model may generate whitespace up to the token limit. No `json_schema`.
- Prefill via Chat Prefix Completion (beta): last message `role: "assistant"` with `prefix: True` against `https://api.deepseek.com/beta`, combined with `stop` against trailing prose.
- **Images (new compared with V4-Flash)**: `image_url` blocks (http(s) URL or base64 data URL) or `file` blocks (Files API `file_id` or `file_data`); `detail` `low` (downscaled to 512×512) | `high` | `original` | `auto`. Images only in user messages — in system or assistant messages HTTP 400. Anthropic endpoint: `image` block with `source.type` `base64|url|file`.
- Context caching runs automatically, only hits on a full match of a persisted cache unit and works "best-effort"; "static before variable" is only inferred from the examples (unverified).
- Tool-call markup (only relevant when hand-writing examples or for local inference): DSML **with a leading space** — `<｜DSML｜ calls>`, `<｜DSML｜ invoke name="…">`, `<｜DSML｜ parameter name="…" string="true|false">`. Local recommendation: `temperature` 1.0, `top_p` 0.95 or 1.0, 1M context, `max_tokens` ≥ 256K.

## Strengths & weaknesses (prompt-relevant)
- Multimodal MoE with 552B backbone parameters in a causal encoder-decoder architecture: 8B active during prefill, 16B during decode; the KV cache is, according to the vendor, 1/4 of the HBM or 1/8 of the SSD of the previous generation — designed for input-heavy agent workloads. Natively text + image, output text only.
- Strengths (max effort, vendor figures): agentic coding — Terminal-Bench 2.1 90.6 (V4-Pro 87.9), DeepSWE v1.1 74.2 (V4-Pro 62.7); Codeforces 3471; GPQA Diamond 90.9. DeepSeek ranks V4.1-Flash ahead of V4-Pro ("ahead of V4-Pro on performance, cost, speed & total runtime").
- **Weakness in factual knowledge**: SimpleQA-Verified (base) 42.3 vs. 55.2 for V4-Pro base; HLE 36.8 vs. 42.7 for V4-Pro. Clearly behind Opus-5.0 on the heavy agent benchmarks (Terminal-Bench 3.0 30.0 vs. 43.3, Terminal-Bench 4.0 31.2 vs. 51.8). Knowledge-heavy prompts need their own grounding.
- JSON output occasionally returns empty `content` (adjust the prompt); FIM completion only in non-thinking mode.

## Output & format conventions
- **1M context, max. 384K output** (`/models`: 1048576 / 393216 tokens). `max_tokens` defaults: 8K (non-thinking) / 64K (thinking) / 128K (`reasoning_effort: max`).
- Features: JSON output, tool calls (`strict` mode as beta via `/beta`), Responses API, Anthropic API, Chat Prefix Completion (beta), FIM (beta, non-thinking only), vision. `response_format` only `text|json_object`; up to 16 `stop` sequences; `top_logprobs` 0–20; `frequency_penalty`/`presence_penalty` deprecated and ineffective.
- Vision limits: JPEG/PNG/GIF/WebP; at most 1024 tokens per image; up to 600 images per request; request body 48 MiB; single image 32 MiB (64 MiB via Files API `file_id`).
- Price per 1M tokens (peak / off-peak): input cache-hit $0.006 / $0.003, cache-miss $0.30 / $0.15, output $1.20 / $0.60; concurrency limit 2500. Peak = Mon–Fri 01:00–04:00 and 06:00–10:00 UTC.
- Base URLs: `https://api.deepseek.com` (OpenAI SDK), `https://api.deepseek.com/anthropic` (Anthropic SDK; `claude-haiku*`/`claude-sonnet*` and unknown model names → `deepseek-flash`, `claude-opus*` → `deepseek-v4-pro`), `https://api.deepseek.com/beta` (prefix completion, `strict` tools). The legacy IDs `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are, per the vendor, temporarily routed to V4.1-Flash and billed at the Flash price.
- Anthropic endpoint: `thinking` without `budget_tokens`, `output_config` only `effort`; `top_k`, `cache_control`, `container`, `mcp_servers` are ignored; `document`, `search_result`, `redacted_thinking` and MCP blocks are not supported.

## Migration notes
- **FROM V4-Flash (`deepseek-v4-flash`) TO V4.1-Flash**: keep base_url, set `model` to `deepseek-flash` — the old ID only runs during the transition. Prompt deltas: change hand-written DSML examples from `<｜DSML｜tool_calls>` to `<｜DSML｜ calls>`/`<｜DSML｜ invoke>`/`<｜DSML｜ parameter>`; image workarounds (pasted OCR/alt text) can give way to real image blocks; system updates may come as a later system message.
- **FROM V4-Pro TO V4.1-Flash**: same API parameters, same effort levels, same 1M/384K, but a different template (see above). Secure knowledge-heavy prompts with reference material (SimpleQA/HLE is lower). Anthropic endpoint: `in-history` instead of `leading-only`.
- **FROM `deepseek-chat`/`deepseek-reasoner` (V3/R1 era, retired since 24 Jul 2026, 15:59 UTC)**: the chat-vs-reasoner model split becomes a mode flag (`thinking: disabled` or `reasoning_effort: none` for former chat prompts); remove `frequency_penalty`/`presence_penalty`; R1 temperature tips (0.6) have no effect in thinking mode; in tool loops pass `reasoning_content` back instead of stripping it; remove chunking scaffolding for old context windows.
- **AWAY FROM V4.1-Flash**: map `thinking`/`reasoning_effort`/`output_config.effort` onto the effort ladder of the target guide and adjust the `reasoning_content` return; if the target can do `json_schema`, turn the in-prompt JSON example into a real schema; replace `prefix: True` with the target's prefill equivalent; carry image blocks over only if the target guide documents vision (V4-Pro: it does not); merge later system messages into the leading system message if the target does not accept them (V4-Pro: `leading-only`).
- Lifecycle: the routing of the legacy IDs is marked as "temporary"; a V4.1-Pro has been announced, date unverified.

## Sources
- https://api-docs.deepseek.com/news/news260910 — release announcement 2026-09-10: 552B MoE, causal encoder-decoder with 8B/16B active, KV cache 1/4 HBM / 1/8 SSD, model name `deepseek-flash`, retirement of V4-Flash/V4-Flash-Vision-Exp with temporary routing, "ahead of V4-Pro" statement, V4.1-Pro announced.
- https://api-docs.deepseek.com/updates — change log 2026-09-10: benchmarks (Terminal-Bench 2.1 90.6, DeepSWE v1.1 74.2, Codeforces 3471, GPQA Diamond 90.9, HLE 36.8), switch to `deepseek-flash`, V4-Pro continues after 2026-09-14.
- https://api-docs.deepseek.com/quick_start/pricing — model table: version DeepSeek-V4.1-Flash, 1M / 384K, thinking as default, feature matrix incl. vision and FIM non-thinking only, peak/off-peak prices and times, concurrency 2500, footnote on the legacy IDs.
- https://api-docs.deepseek.com/api/list-models — `deepseek-flash`: 1048576 / 393216 tokens, `input_modalities` text + image, effort `low|high|max` with default `high`, `system_prompt_update: in-history` (V4-Pro: `leading-only`).
- https://api-docs.deepseek.com/guides/thinking_mode — toggle and effort in OpenAI, Anthropic (`output_config.effort`) and Responses format, effort mapping incl. minimal/xhigh/ultra, `top_p` only in thinking mode, `reasoning_content` rules with/without `tools` incl. 400.
- https://api-docs.deepseek.com/api/create-chat-completion — model values `deepseek-flash`/`deepseek-v4-pro`, `reasoning_effort` enum, `max_tokens` defaults and maximum, `response_format` text/json_object, 16 stops, `tool_choice` 400 in thinking mode, image content parts with `detail`, deprecated penalties.
- https://api-docs.deepseek.com/guides/vision — image formats, three input paths, `detail` levels, at most 1024 tokens per image, limits (600 images, 48 MiB body, 32/64 MiB single image), images only in user messages, Anthropic `image` block.
- https://api-docs.deepseek.com/guides/anthropic_api — mapping haiku/sonnet/unknown → `deepseek-flash`, opus → `deepseek-v4-pro`; field support (`thinking` without `budget_tokens`, `output_config` only `effort`, ignored fields, unsupported blocks).
- https://api-docs.deepseek.com/guides/json_mode — `json_object`, mandatory literal "json", example in the prompt, `max_tokens` note, occasional empty `content`.
- https://api-docs.deepseek.com/guides/chat_prefix_completion — prefill via assistant role with `prefix: True` on the `/beta` base URL, combination with `stop`.
- https://api-docs.deepseek.com/guides/kv_cache — automatic caching, hits only on a full match of a cache unit, "best-effort"; the ordering recommendation "static before variable" is not explicitly stated there.
- https://api-docs.deepseek.com/guides/tool_calls — `strict` mode (beta) via `/beta`, in both thinking and non-thinking mode.
- https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash — model card: 552B MoE, causal encoder-decoder (8B/16B active), native image processing, effort 1–100, base benchmarks (SimpleQA-Verified 42.3 vs. 55.2 V4-Pro base), instruct comparison with Opus-5.0 and V4-Pro (HLE, Terminal-Bench 3.0/4.0), recommended local sampling parameters, MIT license.
- https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/encoding/README.md — the three template changes vs. V4 (DSML with leading space, numeric effort low=50/high=75/max=100, `<｜System｜>` in the middle of the conversation), BOS template, effort prefix only in thinking mode at the start of the conversation.
