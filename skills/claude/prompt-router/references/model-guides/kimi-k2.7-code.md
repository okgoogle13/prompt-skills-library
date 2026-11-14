---
model: kimi-k2.7-code
vendor: Moonshot AI
family: Kimi
aliases: [kimi-k2.7-code-highspeed, kimi-k2.7, k2.7-code, kimi-k2-7-code]
last_verified: 2026-10-13
status: current
---

# Kimi K2.7 Code (also applies to kimi-k2.7-code-highspeed)

## Reasoning / Thinking
- Type: **thinking always on, cannot be switched off**. `thinking.type: "disabled"` returns an error; the parameter reference says you do not need to pass `thinking` at all — "just switch the `model`, and the model always emits `reasoning_content`". There is no non-thinking/instant mode.
- **Preserved Thinking is enforced**: `thinking.keep` is treated as `"all"`, whether omitted or set; any other value is an error. Therefore the historical `reasoning_content` of every earlier assistant message MUST stay unchanged in `messages` — not only within a tool loop, but across turns.
- **No `reasoning_effort`** (only kimi-k3 has that control). Thinking depth cannot be steered by parameter; Moonshot states roughly 30% fewer thinking tokens on average versus K2.6, or a 30% reduced overthinking tendency.
- `reasoning_content` and `content` share `max_tokens` (default 32,768); for multi-step tool calls the thinking guide recommends `max_tokens >= 16000` and streaming. In a stream `reasoning_content` always arrives before `content`.
- `kimi-k2.7-code-highspeed` is, per the parameter reference, the same model with identical parameter constraints and identical thinking behaviour; only output speed differs.

## Prompting style
- No K2.7-specific prompting guide; the general platform recommendations apply: set a role in the system message, separate sections with delimiters (triple quotes, XML tags, headings), spell out working steps explicitly, few-shots for styles that are hard to describe, length targets as paragraph or bullet counts rather than word counts ("The model can't read your mind").
- **No sampling controls**: temperature, top_p, n and the penalties are fixed (see below). Variance and format fidelity must come from the prompt, `response_format` and tool schemas; Moonshot advises not passing the defaults at all.
- **Tools**: `tool_choice` only `"auto"` (default) or `"none"` — `"required"` and forcing a specific tool return an error. If you want to force a tool, phrase it in the prompt. Keep the `reasoning_content` of the running tool loop in context (omitting it is not an error, but per the quickstart it degrades continuity and tool-call quality).
- Moonshot handles repeated identical tool calls client-side platform-wide: check the message layout (append the assistant message unchanged, `tool_call_id` exact), then `<system-reminder>` hints from 3 repeats, escalating at 5 and again at 8 identical repeats — in the agent loop, not in the static system prompt.
- Agent framework: per the model card K2.7 Code "best with Kimi Code CLI as its agent framework".

## Strengths & weaknesses (prompt-relevant)
- Strengths: dedicated coding model; follows instructions in long contexts more reliably than K2.6 and reaches higher success rates on long-horizon coding (announcement: sequences of 4,000+ tool calls and 12+ hours of continuous execution). Image and video input (images png/jpeg/webp/gif, videos incl. mp4/mov/avi), including in tool results.
- Structured output: per Moonshot the **most stable** support on the platform, including nested objects/arrays as well as `anyOf`/`oneOf`/`$ref`/`additionalProperties: true`; usually holds the schema even without `strict`. For structured-output calls Moonshot explicitly recommends `kimi-k2.7-code` over `kimi-k2.6`.
- Weaknesses: no `tool_choice: "required"`; no public image URLs (only base64 or file upload, request body max. 100 MB); no separately billed cache write and no TTL choice (per the caching FAQ only kimi-k3); video chat is experimental per the model card and only available via the official API; `partial=true` with complex schemas can break the structure.
- High-speed variant: per the quickstart currently resource-limited, speed may fluctuate.

## Output & format conventions
- Context window 262,144 tokens (256K); `max_tokens` default 32,768. Modalities text/image/video → text.
- **Fixed sampling parameters**: temperature 1.0, top_p 0.95, n 1, presence_penalty 0, frequency_penalty 0 — any other value is an error.
- `response_format`: `json_schema` with `strict: true` (Moonshot: "Always explicitly set strict: true"); parse only `choices[0].message.content`, never `reasoning_content` or the whole response object.
- Interface: Chat Completions (OpenAI-compatible). The Responses API and the `model` enum of the Messages API reference list only `kimi-k3`; Moonshot's Claude Code guide nonetheless uses `kimi-k2.7-code` via the Anthropic endpoint `https://api.moonshot.ai/anthropic` (as the HAIKU tier).
- Prices per 1M tokens: `kimi-k2.7-code` $0.19 cache-hit / $0.95 cache-miss / $4.00 output; `kimi-k2.7-code-highspeed` $0.38 / $1.90 / $8.00. Highspeed delivers about 180 tokens/s, up to 260 tokens/s with short context.
- Open weights (`moonshotai/Kimi-K2.7-Code`, Modified MIT): 1T parameters total / 32B active, MoE with 384 experts (8 selected, 1 shared), MoonViT vision encoder, native INT4, same architecture as K2.5/K2.6. For vLLM/SGLang the card recommends temperature 1.0 and top_p 0.95; instant mode is not supported.

## Migration notes
- **TO kimi-k3**: per the FAQ, only swap `model` and keep returning the complete assistant messages (incl. `reasoning_content`) unchanged; optionally set `reasoning_effort` (`low|high|max`, default `max` — choose deliberately rather than inheriting the most expensive default). On K3, `tool_choice: "required"` becomes possible, a cache write is billed separately, and context grows to 1M.
- **FROM kimi-k2.6 here**: remove the `thinking` configuration (only `{"type":"enabled","keep":"all"}` would be valid), drop the 0.6-temperature assumption of the K2.6 non-thinking mode (non-thinking prompts have no equivalent here), and rework the pipeline so historical `reasoning_content` goes back in `messages` — for K2.6 that was optional without `keep: "all"`. Complex JSON schemas that were simplified on K2.6 or guarded by Markdown stripping can be specified more strictly here.
- **TO kimi-k2.6**: `tool_choice: "required"` exists on neither model; simplify structured output on K2.6 (no `oneOf`/`$ref`) and plan a second validation layer.
- **FROM other providers**: remove sampling and effort controls (temperature, top_p, reasoning budgets) without replacement — they are fixed or absent; rephrase tool forcing as prompt instructions; express prefill as a final assistant message with `partial: true` (Partial Mode; per the structured-output guide usable on kimi-k2.7-code, but not structure-faithful with complex schemas); switch image URLs to base64 or file upload.
- **FROM kimi-k2.7-code**: explicitly request thinking in the target if it does not always think; keep `reasoning_content` return only if the target documents it; plan sampling parameters again as real levers.

## Sources
- https://platform.kimi.ai/docs/models.md — Roster: `kimi-k2.7-code` "dedicated coding model … Context 256k", `kimi-k2.7-code-highspeed` at about 180 or up to 260 tokens/s; both not in the deprecation table.
- https://platform.kimi.ai/docs/api/models-overview.md — Parameter matrix: `thinking` only `{"type":"enabled","keep":"all"}`, no `reasoning_effort`, no `tool_choice: "required"`, temperature/top_p/n/penalties fixed; highspeed = same model with identical constraints; FAQ on the switch kimi-k2.7-code → kimi-k3; when switching from kimi-k2.6, historical `reasoning_content` must be returned.
- https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart.md — Positioning (instruction fidelity in long contexts, 30% less overthinking), no non-thinking mode, `max_tokens` default 32768, fixed sampling values, `tool_choice` only auto/none, keep `reasoning_content` in tool loops, image/video formats, no image URLs, 100 MB request limit, highspeed resource note.
- https://platform.kimi.ai/docs/guide/use-thinking-models.md — Thinking always on, Preserved Thinking enforced (`thinking.keep` treated as `"all"`), historical `reasoning_content` MUST be retained, `reasoning_content` + `content` ≤ `max_tokens`, `max_tokens >= 16000` and streaming recommended.
- https://platform.kimi.ai/docs/guide/response_format.md — `kimi-k2.7-code` with the most stable structured-output support (`anyOf`/`oneOf`/`$ref`/`additionalProperties: true`), recommendation of kimi-k2.7-code for structured output, `strict: true`, parse only `content`, `partial=true` only with simple schemas.
- https://platform.kimi.ai/docs/guide/prompt-best-practice.md — General platform prompting recommendations (role, delimiters, steps, few-shots, length control).
- https://platform.kimi.ai/docs/guide/tool-call-repeat.md — Message-layout check and reminder escalation at 3 / 5 / 8 identical tool calls.
- https://platform.kimi.ai/docs/pricing/chat-k3.md and https://platform.kimi.ai/docs/guide/context-caching.md — Prices and 262,144-token context for both variants; cache write only for kimi-k3, not for the K2.x models.
- https://platform.kimi.ai/docs/api/messages.md, https://platform.kimi.ai/docs/api/responses.md and https://platform.kimi.ai/docs/guide/claude-code-kimi.md — `model` enum of the Messages API and Responses API only `kimi-k3`; Claude Code setup with `kimi-k2.7-code` as HAIKU tier via `https://api.moonshot.ai/anthropic`.
- https://platform.kimi.ai/docs/platform-changelog.md — June 2026: release of Kimi K2.7 Code via the Open Platform API, followed by the HighSpeed variant.
- https://huggingface.co/moonshotai/Kimi-K2.7-Code — official model card: built on K2.6, about 30% fewer thinking tokens, 1T / 32B active, 384 experts, MoonViT, native INT4, Modified MIT; enforced thinking and preserve-thinking, video experimental, temperature 1.0 / top_p 0.95 recommended, no instant mode, "works best with Kimi Code CLI as its agent framework".
- https://forum.moonshot.ai/t/here-comes-kimi-k2-7-code-better-coding-with-more-efficiency/441 — official announcement of 16 Jun 2026: long-horizon coding with 4,000+ tool calls and 12+ hours, about 30% fewer thinking tokens than K2.6, HighSpeed about 180 / up to 260 tokens/s, fixed sampling parameters.
