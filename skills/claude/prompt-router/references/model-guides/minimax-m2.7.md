---
model: minimax-m2.7
vendor: MiniMax
family: MiniMax
aliases: [minimax-m2.7-highspeed, m2.7, minimax-m27, "MiniMaxAI/MiniMax-M2.7"]
last_verified: 2026-10-13
status: current
---

# MiniMax-M2.7 (incl. M2.7-highspeed)

## Reasoning / Thinking
- Type: **thinking always on, cannot be switched off**. On both endpoints for M2.x: `thinking` omitted or `adaptive` → thinking on; `{"type": "disabled"}` is "accepted but ignored; thinking remains on". No depth control: `output_config.effort` / `reasoning_effort` only act on M3.1-Flash-Preview, "Other models ignore this field".
- Return: on the Anthropic path as a `thinking` content block; on the OpenAI path by default as `<think>…</think>` in the `content` field, separated into `reasoning_content` with `reasoning_split=true`. `reasoning_split` neither turns thinking on nor off.
- Multi-turn: the complete assistant message must go back into the history ("must be append to the conversation history to maintain the continuity of the reasoning chain") — Anthropic path the complete `response.content` list, OpenAI path `content` including `<think>` tags unchanged.
- Self-hosting: reasoning is handled via SGLang's `--reasoning-parser minimax-append-think`, tool calls via `--tool-call-parser minimax-m2`; where the trace then appears in the response depends, per the vendor, on the SGLang version.

## Prompting style
- **No model-specific prompting page any more.** The former "Usage Tips" page under `token-plan/` redirects to the M-Plan overview; MiniMax's earlier advice (task at the end, labelled sections, various few-shot examples) is therefore (unverified) for M2.7.
- Confirmed by the Hugging Face model card: sampling `temperature=1.0`, `top_p=0.95`, `top_k=40` and the default system prompt "You are a helpful assistant. Your name is MiniMax-M2.7 and is built by MiniMax." Note: the hosted API has a `top_p` default of 0.9 and ignores `top_k` on the Anthropic path.
- Visible CoT scaffolding is redundant, since the model thinks anyway; whether it lowers quality is (unverified).

## Strengths & weaknesses (prompt-relevant)
- Per the vendor a model "for agents, software engineering, and complex productivity tasks"; the model card names Agent Teams, complex skills and dynamic tool search, as well as, among others, SWE-Pro 56.22% and Terminal Bench 2 57.0% (vendor figures).
- **Text and tool calls only**: "The M2.7, M2.5, M2.1, and M2 series support text and tool-call content blocks only" — no image/video input.
- Context **204,800 tokens**. M2.7 approx. 60 tps; M2.7-highspeed "Same performance, faster and more agile" at approx. 100 tps — same prompts, same guide.
- Open weights (`MiniMaxAI/MiniMax-M2.7`, MiniMax-M2.7 License; commercial use with attribution and prior-approval obligations). Parameter count and knowledge cutoff are not stated on the official pages (unverified). Structured outputs/JSON schema mode are not documented (unverified).
- Thinking cannot be switched off: for latency-critical chat or completion cases without reasoning, M2.7 is structurally at a disadvantage versus M3 with `disabled`.

## Output & format conventions
- Model IDs (API, exact spelling): `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`.
- `max_tokens` (Anthropic) or `max_completion_tokens` (OpenAI; `max_tokens` deprecated there): recommended 65536, maximum 204800. Thinking tokens count — set too small → `stop_reason: "max_tokens"` with no text, or `finish_reason: "length"` with empty `content`.
- `temperature` [0, 2], default 1; `top_p` default **0.9** (M2.x). Anthropic path: `stop_sequences` and `top_k` are ignored, `tool_choice` only `auto`/`none`.
- Caching: passive prefix caching (from 512 input tokens, order tool list → system prompts → user messages) **and** explicit `cache_control` on the Anthropic path — 5-minute TTL, extended on use, max. 4 breakpoints, 20-block lookback; cache writes are billed extra.
- Prices per 1M tokens (pay-as-you-go): M2.7 $0.30 input / $1.20 output / $0.06 cache read / $0.375 cache write; M2.7-highspeed $0.60 / $2.40 / $0.06 / $0.375.

## Migration notes
- **FROM M2.7 to MiniMax-M3** (recommended by the vendor for new projects with multimodal or 1M needs): set `thinking` **explicitly** to `adaptive` — on the Anthropic path it is otherwise off on M3, whereas on M2.7 it was always on. A `disabled` that was previously sent without effect does actually switch thinking off on M3. `cache_control` breakpoints no longer act on M3 per the support matrix — base cost on passive caching. Raise limits (context up to 1M, `max_tokens` up to 524288); the `top_p` default changes from 0.9 to 0.95. Image/video input becomes possible.
- **FROM M2.7 to M3.1-Flash-Preview**: set effort explicitly (default `max`); `reasoning_split=false` does not work there — thinking arrives in `reasoning_content` instead of `<think>` in `content`.
- **TO M2.7**: remove image/video content or convert it to text beforehand; trim context to ≤ 204,800 tokens and `max_tokens` to ≤ 204,800. `thinking: disabled` and effort parameters have no effect — budget latency for always-on thinking. For recurring prefixes set explicit `cache_control` breakpoints.
- **FROM M2.7 to other providers**: remove `<think>` parsing and `reasoning_split`/`reasoning_details`, adapt history handling to the target; `stop_sequences`/`top_k`, which had no effect here, become effective again there.

## Sources
- https://platform.minimax.io/docs/guides/text-generation — Supported Models: M2.7 and M2.7-highspeed (204,800 context, approx. 60 / 100 tps, "Same performance, faster and more agile"), "MiniMax-M3, MiniMax-M2.7, and MiniMax-M2.7-highspeed also remain available"; older models in the legacy accordion.
- https://platform.minimax.io/docs/release-notes/models — Mar. 18, 2026: "Released MiniMax-M2.7 series (MiniMax-M2.7 / M2.7-highspeed)".
- https://platform.minimax.io/docs/faq/models — M2.7 and M2.7-highspeed under "Available Models" (not retired).
- https://platform.minimax.io/docs/api-reference/text-anthropic-api — Thinking-control table (M2.x: "Accepted but ignored; thinking remains on"), text/tool-call blocks only for M2.x, thinking tokens in `max_tokens`, ignored `stop_sequences`/`top_k`, multi-turn rule.
- https://platform.minimax.io/docs/api-reference/text-chat-anthropic — `max_tokens` 65536/204800 for non-M3 models, `top_p` 0.9 for M2.x, `output_config.effort` "Other models ignore this field", `tool_choice` only `auto`/`none`.
- https://platform.minimax.io/docs/api-reference/text-chat-openai — `thinking` for M2.x not switchable off, `reasoning_effort` ignored, `reasoning_split` as output switch (`<think>` in `content` vs. `reasoning_content`), `max_completion_tokens` 65536/204800.
- https://platform.minimax.io/docs/api-reference/text-openai-api — `<think>` content fully retained in `content`; `finish_reason: "length"` with empty `content` when the limit is too small.
- https://platform.minimax.io/docs/api-reference/text-prompt-caching — passive caching incl. the M2.7 series; cache comparison: explicit caching for M2.7/M2.5/M2.1/M2, 5-minute TTL.
- https://platform.minimax.io/docs/api-reference/anthropic-api-compatible-cache — `cache_control` mechanics (max. 4 breakpoints, 20-block lookback), supported models incl. M2.7/M2.7-highspeed.
- https://platform.minimax.io/docs/guides/pricing-paygo — M2.7 $0.3/$1.2/$0.06/$0.375; M2.7-highspeed $0.6/$2.4/$0.06/$0.375.
- https://platform.minimax.io/docs/guides/local-deploy-m2-7 — "For a new project that needs native multimodal input or a 1M-token context, use MiniMax-M3", SGLang parsers `minimax-append-think` / `minimax-m2`, license note.
- https://huggingface.co/MiniMaxAI/MiniMax-M2.7 — official model card: Agent Teams/Skills, SWE-Pro 56.22%, Terminal Bench 2 57.0%, sampling `temperature=1.0`/`top_p=0.95`/`top_k=40`, default system prompt.
- https://platform.minimax.io/docs/guides/text-m3-function-call — "must be append to the conversation history …", do not alter `<think>` content in `content` (guide aimed at M3; transfer to M2.7 documented via the SDK pages).
