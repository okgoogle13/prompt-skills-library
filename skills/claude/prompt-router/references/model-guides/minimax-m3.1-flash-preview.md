---
model: minimax-m3.1-flash-preview
vendor: MiniMax
family: MiniMax
aliases: [minimax-m3.1, minimax-m3.1-flash, m3.1-flash-preview, m3.1-flash, minimax-m3-1-flash-preview]
last_verified: 2026-10-13
status: current
---

# MiniMax-M3.1-Flash-Preview

## Reasoning / Thinking
- Type: **thinking always on, depth via effort ladder**. "Thinking is on by default and needs no configuration"; it cannot be switched off. `thinking: {"type": "disabled"}` or effort `none` returns HTTP 400 with `model "MiniMax-M3.1-Flash-Preview" requires adaptive thinking; thinking.type="disabled" (including reasoning.effort=none) is not allowed (2013)`. If `thinking` is sent, it must be `{"type": "adaptive"}`.
- Depth: `low`, `medium`, `high`, `xhigh`, `max` — higher levels think more thoroughly, produce more output tokens and more latency. **Default when unspecified is `max`.** Field name per protocol: Anthropic-compatible `output_config.effort`, OpenAI-compatible `reasoning_effort`, OpenAI Responses `reasoning.effort`. Per the vendor, latency/tokens are reduced via a lower level, not by switching off.
- Return of thinking: Anthropic path as a `thinking` content block (with `signature`); OpenAI path **always** separated into `reasoning_content`, `content` contains only the answer. `reasoning_split=false` (thinking as `<think>` in `content`) is currently not supported for this model.
- Multi-turn: return thinking blocks unchanged ("preserve them unchanged in later turns, especially in tool-use conversations"); on the OpenAI path `reasoning_content` must be kept in full. The OpenAI SDK page refers this model's tool use and interleaved thinking to the M3 tool-use guide.

## Prompting style
- **No model-specific prompting page.** The former "M-series Usage Tips" page has been removed (HTTP 404, as of 2026-10-13); recommendations such as "task at the end" or "label sections" are (unverified) for this model.
- Officially there are only the general "Better Prompts" notes of the MiniMax Code app, in which the model debuted: describe the desired result, not just steps; for coding tasks name stack, constraints and validation criteria; for research give output format and source requirements. These are product notes, not model notes.
- Depth control belongs in the effort parameter, not in prompt text; whether additional "think thoroughly" instructions do anything at high effort is (unverified).

## Strengths & weaknesses (prompt-relevant)
- Per the vendor the newest M-series language model "for agentic reasoning, tool use, coding, and long-context tasks"; "Frontier multimodal coding model with 1M context window and tunable thinking depth". Input text, image and video (as M3).
- **Preview with restricted access**: "available only through M Plan and MiniMax Code for now"; called with a Subscription Key, no pay-as-you-go price published. The M-Plan FAQ recommends pay-as-you-go for production — there M3 is the counterpart.
- Cost/quota lever: the higher the thinking depth, the more thinking content and the more M-Plan usage — the `max` default is the most expensive level.
- Not published: parameter count, benchmarks, output speed, knowledge cutoff (unverified). Passive prompt caching is listed by MiniMax only for M3 and M2.x, not for this model (unverified); explicit `cache_control` likewise only for M2.x.

## Output & format conventions
- Model ID (API, exact spelling): `MiniMax-M3.1-Flash-Preview`. Context window 1,000,000 tokens. MiniMax's Claude Code guide uses `MiniMax-M3.1-Flash-Preview[1m]`.
- `max_tokens` (Anthropic) or `max_completion_tokens` (OpenAI; `max_tokens` deprecated there): recommended 131,072, maximum 524,288. Thinking tokens count — set too small → `stop_reason: "max_tokens"` with no text, or `finish_reason: "length"` with empty `content`.
- `temperature` [0, 2], default 1; `top_p` default 0.95. Anthropic path: `stop_sequences` and `top_k` are ignored, `tool_choice` only `auto`/`none`. Structured outputs/JSON schema mode are not documented (unverified).
- Endpoints: `https://api.minimax.io/anthropic` (recommended) and `https://api.minimax.io/v1`. Image up to 10 MB, video up to 50 MB per URL/base64, larger videos via the Files API (`mm_file://{file_id}`); token estimation via `POST /anthropic/v1/messages/count_tokens`.

## Migration notes
- **FROM MiniMax-M3 to this model**: remove `thinking: {"type": "disabled"}` (otherwise HTTP 400); set effort **explicitly** instead of inheriting the expensive `max` default; replace prompt-based depth control with the effort level. On the OpenAI path do not rely on `<think>` in `content` any more — thinking arrives in `reasoning_content`, `reasoning_split=false` does not work. Swap the API key for a Subscription Key.
- **BACK TO MiniMax-M3** (e.g. for pay-as-you-go/production): remove the effort fields — M3 ignores them silently; control depth again via `thinking` on/off plus prompt text, and set `thinking` explicitly (M3 default flips between endpoints).
- **FROM other providers**: a switched-off reasoning of the source cannot be mapped 1:1 — the nearest equivalent is level `low`; resize latency and `max_tokens`. Remove visible CoT scaffolding ("think step by step"). Do not plan on Claude `cache_control` breakpoints being effective.
- **AWAY FROM this model**: map `output_config.effort`/`reasoning_effort` onto the target's ladder (level names are not standardised); adapt thinking-block/`reasoning_content` handling to the target; check image/video input.

## Sources
- https://platform.minimax.io/docs/guides/text-generation — Model table (1M context, "tunable thinking depth"), "latest M-series language model …", "available only through M Plan and MiniMax Code for now", thinking always on, effort levels with default `max` and field names per protocol, `reasoning_content` on the OpenAI path, 400 errors for `disabled`/`none`.
- https://platform.minimax.io/docs/api-reference/text-chat-anthropic — Messages schema: model ID, `thinking` only `adaptive`, `output_config.effort` (default `max`, `none` → 400), `max_tokens` 131072/524288, `top_p` 0.95, `temperature` [0, 2], `tool_choice` only `auto`/`none`.
- https://platform.minimax.io/docs/api-reference/text-anthropic-api — Thinking-control table, full error message (2013), "preserve them unchanged in later turns", thinking tokens in `max_tokens`, ignored `stop_sequences`/`top_k`, media limits, `count_tokens`.
- https://platform.minimax.io/docs/api-reference/text-chat-openai — `reasoning_effort` ("Only `MiniMax-M3.1-Flash-Preview` supports real thinking-depth tuning"), `reasoning_split=false` not supported, `max_completion_tokens` 131072/524288, `max_tokens` deprecated.
- https://platform.minimax.io/docs/api-reference/text-openai-api — `reasoning_content` fully retained, thinking tokens in `max_tokens` (`finish_reason: "length"`), reference to the tool-use/interleaved-thinking guide for M3.1.
- https://platform.minimax.io/docs/api-reference/text-prompt-caching — Cache comparison: passive caching for M3 and M2.x, explicit only for M2.x (M3.1 not listed).
- https://platform.minimax.io/docs/m-plan/faq — M3.1 Flash Preview in all M-Plan tiers, higher thinking depth consumes more, "Pay-as-you-go is recommended for production use", Subscription Keys separate from pay-as-you-go keys.
- https://platform.minimax.io/docs/m-plan/claude-code — `MiniMax-M3.1-Flash-Preview[1m]`, "always enables thinking and cannot turn it off".
- https://platform.minimax.io/docs/guides/pricing-paygo — Pay-as-you-go table lists only M3 and M2.7 (no M3.1 price).
- https://agent.minimax.io/docs/code/get-started/first-task — "Better Prompts" notes of the MiniMax Code app.
- https://agent.minimax.io/docs/changelog — v3.0.74 (2026-09-28): M3.1-Flash-Preview debuts in MiniMax Code; CLI: default model `MiniMax-M3.1-Flash-Preview`.
