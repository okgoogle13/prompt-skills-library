---
model: kimi-k2.6
vendor: Moonshot AI
family: Kimi
aliases: [k2.6, kimi-k2-6, moonshotai/Kimi-K2.6]
last_verified: 2026-10-13
status: current
---

# Kimi K2.6

## Reasoning / Thinking
- Type: **switchable**. `thinking.type`: `"enabled"` (default) | `"disabled"`; with the OpenAI SDK via `extra_body={"thinking": {"type": "disabled"}}`. K2.6 is thus the only current Kimi API model with a non-thinking mode (kimi-k3 and kimi-k2.7-code always think).
- `thinking.keep`: `null` (default — historical `reasoning_content` from earlier turns is ignored, shorter context, lower cost) | `"all"` (Preserved Thinking). `keep` only affects earlier turns, not whether thinking happens in the current turn; Moonshot recommends `keep: "all"` together with `type: "enabled"`.
- **No `reasoning_effort`** — thinking depth is on/off only, not graded.
- `reasoning_content` and `content` share `max_tokens` (default 32,768); for multi-step tool calls the thinking guide recommends `max_tokens >= 16000` and streaming. In a stream `reasoning_content` always arrives before `content`.
- Within a tool loop, send the entire `reasoning_content` back; omitting it is not an error, but per the quickstart it degrades continuity and tool-call quality.

## Prompting style
- No K2.6-specific prompting guide; the general platform recommendations apply: set a role in the system message, separate sections with delimiters (triple quotes, XML tags, headings), spell out working steps explicitly, few-shots for styles that are hard to describe, length targets as paragraph or bullet counts rather than word counts ("The model can't read your mind").
- **No sampling controls**: temperature is fixed by mode, top_p/n/penalties are fixed (see below). Variance and format fidelity must come from the prompt, `response_format` and tool schemas; Moonshot advises not passing the defaults.
- **Tools**: `tool_choice` only `"auto"` (default) or `"none"`; per the parameter reference `"required"` is generally unsupported on kimi-k2.6 and returns an error; the quickstart justifies the restriction with active thinking. Forcing tool use therefore belongs in the prompt instruction.
- Moonshot handles repeated identical tool calls client-side platform-wide: check the message layout, then `<system-reminder>` hints from 3 repeats, escalating at 5 and again at 8 — in the agent loop, not in the static system prompt.
- Agent framework: per the model card K2.6 "best with Kimi Code CLI as its agent framework".

## Strengths & weaknesses (prompt-relevant)
- Strengths: general-purpose model for text, image and video, dialogue and agent tasks; long-horizon coding across languages (Rust, Go, Python) and domains (frontend, DevOps, performance) (announcement: 4,000+ tool calls, over 12 hours of continuous execution); coding-driven design from prompts and visual templates; agent swarm up to 300 sub-agents × 4,000 steps.
- Structured output weakness: with complex schemas, per Moonshot occasionally unstable — `content` may be wrapped in a Markdown code block, `oneOf`/`$ref` are not strictly followed, with `strict=false` or `partial=true` fields appear outside the schema, and empty strings sometimes appear instead of `null`. Moonshot recommends simple schemas, a second validation layer, and `kimi-k2.7-code` for structured output.
- Other weaknesses: no public image URLs (only base64 or file upload, request body max. 100 MB); no separately billed cache write and no TTL choice (per the caching FAQ only kimi-k3); video chat is experimental per the model card and only via the official API.
- The built-in web search `$web_search` is being retired platform-wide (shutdown 20 Oct 2026); the K2.6 quickstart also names it as temporarily incompatible with thinking mode. Replacements are the REST APIs `/v1/tools/search`, `/v1/tools/search_pro`, `/v1/tools/fetch`.

## Output & format conventions
- Context window 262,144 tokens (256K); `max_tokens` default 32,768. Modalities text/image/video → text.
- **Fixed sampling parameters**: temperature 1.0 (thinking) or 0.6 (non-thinking), top_p 0.95, n 1, presence_penalty 0, frequency_penalty 0 — any other value is an error.
- `response_format`: `json_schema` with `strict: true` (Moonshot: "Always explicitly set strict: true"); parse only `choices[0].message.content` and on K2.6 strip Markdown markers before parsing.
- Interface: Chat Completions (OpenAI-compatible). The Responses API and the `model` enum of the Messages API reference list only `kimi-k3`.
- Prices per 1M tokens: $0.16 cache-hit / $0.95 cache-miss input, $4.00 output.
- Open weights (`moonshotai/Kimi-K2.6`, Modified MIT): 1T parameters total / 32B active, MoE with 384 experts (8 selected, 1 shared), MoonViT vision encoder, native INT4. For vLLM/SGLang the card recommends temperature 1.0 (thinking) or 0.6 (instant) and top_p 0.95; instant mode there via `chat_template_kwargs: {"thinking": False}`.

## Migration notes
- **TO kimi-k3**: per the FAQ, swap `model`, remove the K2.x `thinking` configuration, optionally set `reasoning_effort` (`low|high|max`, default `max`), and in multi-turn and tool flows return the full assistant message including `reasoning_content` unchanged (required on K3, optional on K2.6 without `keep: "all"`). Non-thinking prompts have no equivalent on K3 — K3 always thinks; the next lever is `reasoning_effort: "low"`.
- **TO kimi-k2.7-code**: remove `thinking` (only `{"type":"enabled","keep":"all"}` would be valid), drop the 0.6-temperature assumption and mandatorily return historical `reasoning_content`; simplified JSON schemas may use `oneOf`/`$ref` again there.
- **FROM other providers**: remove sampling and effort controls without replacement; map a "fast" goal without reasoning to `thinking.type: "disabled"` — there is no graded reasoning budget; rephrase `tool_choice: "required"` or forced tools as prompt instructions; switch image URLs to base64 or file upload; simplify complex schemas.
- **FROM kimi-k2.6**: map the thinking switch onto the target's mechanism; keep Markdown stripping and second validation only if the target documents similar weaknesses; plan sampling parameters again as real levers.

## Sources
- https://platform.kimi.ai/docs/models.md — Roster: `kimi-k2.6` "Supports both visual and text input, thinking and non-thinking modes, and dialogue and Agent tasks. Context 256k"; not in the deprecation table.
- https://platform.kimi.ai/docs/api/models-overview.md — Parameter matrix: `thinking` enabled/disabled/`keep: "all"`, no `reasoning_effort`, no `tool_choice: "required"`, temperature 1.0/0.6 fixed, top_p/n/penalties fixed; FAQ "Switching from `kimi-k2.6` to `kimi-k3`"; `extra_body` example.
- https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart.md — Positioning as general-purpose model, long-horizon coding, `max_tokens` default 32768, `thinking` default, fixed sampling values, `tool_choice` only auto/none with active thinking, keep `reasoning_content` in tool loops, `$web_search` incompatibility with thinking, no image URLs, 100 MB request limit.
- https://platform.kimi.ai/docs/guide/use-thinking-models.md — `thinking.type`/`thinking.keep` with defaults, Preserved Thinking, `reasoning_content` + `content` ≤ `max_tokens`, `max_tokens >= 16000` and streaming recommended.
- https://platform.kimi.ai/docs/guide/response_format.md — K2.6 instabilities with complex schemas (Markdown code block, `oneOf`/`$ref`, fields outside the schema, empty strings), recommendation of kimi-k2.7-code for structured output, `strict: true`.
- https://platform.kimi.ai/docs/guide/prompt-best-practice.md — general platform prompting recommendations (role, delimiters, steps, few-shots, length control).
- https://platform.kimi.ai/docs/guide/tool-call-repeat.md — Message-layout check and reminder escalation at 3 / 5 / 8 identical tool calls.
- https://platform.kimi.ai/docs/pricing/chat-k3.md and https://platform.kimi.ai/docs/guide/context-caching.md — $0.16 / $0.95 / $4.00 per 1M tokens, 262,144-token context; cache write only for kimi-k3, not for kimi-k2.6.
- https://platform.kimi.ai/docs/guide/use-web-search.md and https://platform.kimi.ai/docs/pricing/websearch.md — `$web_search` retired, shutdown 20 Oct 2026; replacement `/v1/tools/search`, `/v1/tools/search_pro`, `/v1/tools/fetch`.
- https://platform.kimi.ai/docs/api/messages.md and https://platform.kimi.ai/docs/api/responses.md — `model` enum or supported model respectively only `kimi-k3`.
- https://platform.kimi.ai/docs/platform-changelog.md — April 2026: release of Kimi K2.6 via the Open Platform API.
- https://huggingface.co/moonshotai/Kimi-K2.6 — official model card: key features (long-horizon coding, coding-driven design, agent swarm 300 × 4,000), 1T / 32B active, 384 experts, MoonViT, native INT4, Modified MIT; video experimental, temperature 1.0 / 0.6 and top_p 0.95 recommended, preserve-thinking off by default, "works best with Kimi Code CLI as its agent framework".
- https://forum.moonshot.ai/t/meet-kimi-k2-6-advancing-open-source-coding/369 — official announcement of 21 Apr 2026: 4,000+ tool calls and over 12 hours of continuous execution, agent swarm 300 × 4,000 steps.
