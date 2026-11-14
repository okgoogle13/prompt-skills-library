---
model: doubao-seed-2-1-lite
vendor: ByteDance
family: Doubao
aliases: [doubao-seed-2-1-lite-260915, doubao-seed-2.1-lite, seed-2.1-lite]
last_verified: 2026-10-13
status: current
---

# Doubao Seed 2.1 Lite

## Reasoning / Thinking
- Type: **deep thinking on by default**. `thinking.type` platform-wide knows `enabled | disabled | auto`, but doubao-seed-2-1-lite-260915 appears in the support list only with `enabled` (default) and `disabled` — **no `auto`**. A request without a `thinking` field thinks.
- Depth via `reasoning_effort` (Chat API) or `reasoning.effort` (Responses API). All seven levels are accepted (`none | minimal | low | medium | high | xhigh | max`), **default `high`**; `minimal` switches thinking off, `none` is mapped to `minimal`, and **`xhigh`/`max` silently land on `high`**. The 2.0 models that Lite replaces, by contrast, run with default `medium`.
- **Thinking summary active by default**: `reasoning_content` (summary) and `encrypted_content` (encrypted original) come back. `reasoning_effort` only affects the raw chain-of-thought; billing is on the raw tokens (`usage.completion_tokens_details.reasoning_tokens`). According to the docs, the summary increases package latency — raise `timeout`.
- Tool calling: **play back `encrypted_content` unchanged** — it takes precedence over `reasoning_content`; according to the docs, returning only the summary lowers quality in multi-turn/agent runs, while returning nothing raises no error. The Responses API handles this via `previous_response_id`.
- Maximum chain-of-thought 256k tokens; it counts against the same output budget as the answer.

## Prompting style
- The Ark "prompt optimization recommendations" for deep-thinking models apply: add **goal, scenario and audience** (language/tool, readership, occasion, objective) instead of just naming the task.
- **Reduce or avoid decomposition and examples** — step-by-step instructions and few-shot examples, according to the docs, narrow the reasoning logic.
- **Reduce system prompts**: put all prompt information directly into the user prompt (`role: user`).
- Structured output (appendix 3 of the docs): do not stress "output JSON" in the prompt and do not repeat the schema structure; instead describe the substantive content of the task — the format belongs in `response_format`.
- Images go as an `image_url` content part alongside the text in the same user message (example on the Ark page for the Turbo sibling); audio input format and audio-specific prompt rules are not checked here (unverified).

## Strengths & weaknesses (prompt-relevant)
- **Omni-modal**: according to the release note and model page, native, unified processing of text, image/video and audio (input text, image, video, audio → output text). In the Ark model list, Lite is the only 2.1 model in the table for audio understanding.
- **1M context** (1024k context / 1024k input) and **30,000 RPM / 5,000,000 TPM** — 60× the RPM ceiling of 2.1 Pro and Turbo (500 RPM each).
- According to the Ark model page, compared with Doubao-Seed-2.0-lite/260428 it improves coding, agents, general reasoning, long-text and multimodal understanding; named scenarios: education, office work, content analysis, development assistance. Concrete benchmark values for Lite are not on the pages checked (unverified).
- Capability tags: deep thinking, text generation, multimodal understanding, GUI tasks, tool calling, structured output; full tool matrix (function calling, knowledge base, MCP, web search, image processing, Doubao assistant — all except function calling only via the Responses API).
- Weaknesses/quirks: **default response length 4k** despite the 256k ceiling; structured output is **beta** and not usable with TPM guarantee packages; no `auto` thinking, no real level above `high`. No knowledge cutoff published (unverified).
- Availability: only Volcengine Ark (China); the BytePlus ModelArk list (international) does not list a Lite variant.

## Output & format conventions
- Model ID: `doubao-seed-2-1-lite-260915` (Ark: 推荐模型, 首推 = recommended, top pick). Context window 1024k, max input 1024k, max response 256k with **default 4k**, max chain-of-thought 256k. `doubao-seed-2.1-lite` appears only as a billing name on the pricing page; as a callable model ID it is not verified (unverified).
- Output length via `max_completion_tokens` (Chat API) or `max_output_tokens` (Responses API) — covers chain-of-thought **plus** answer.
- Structured output: `json_schema` with `strict: true` recommended; `json_object` requires the string `json` in the input; field order follows the schema; `$ref` only local (`#`), `oneOf`/`allOf` without semantic guarantee; unsupported keywords throw an error; do not combine `frequency_penalty`/`presence_penalty`.
- Operations: streaming recommended, otherwise `timeout` above 30 minutes. APIs: Chat Completions, Responses, Batch (`/v3/batch/chat/completions`), tokenization. Caching: implicit via Responses and Chat API, explicit via Responses API (prefix and session cache).
- Volcengine prices per million tokens, flat across 0–1024k: online 0.80 ¥ input / 12.00 ¥ audio input / 0.16 ¥ cache hit / 2.40 ¥ audio cache hit / 2.70 ¥ output, cache storage 0.017 ¥ per million tokens/hour. Low-latency (fast): 1.60 / 24.00 / 0.32 / 4.80 / 5.40 ¥. Low-priority (flex) and batch: 0.40 / 6.00 / 0.16 / 2.40 / 1.35 ¥. Audio input costs 15× text input.

## Migration notes
- **TO doubao-seed-2.1-lite** (Ark names Lite as the recommended target for doubao-seed-2-0-pro-260215 and doubao-seed-2-0-lite-260215; EOS 24 Nov 2026 and 22 Oct 2026 respectively, each 14:00 UTC+8; per Ark, endpoints not migrated are automatically switched to the recommended model or shut down): (1) set `reasoning_effort` explicitly — the 2.0 models defaulted to `medium`, Lite to `high`; without setting it, thinking tokens, cost and latency rise. (2) Raise length assumptions: 2.0 had 224k input and 128k response/chain-of-thought, Lite has 1024k and 256k; chunking scaffolding can go. (3) The thinking summary is now default (not listed for 2.0-pro-260215/-lite-260215): `reasoning_content` is only a summary, so pass `encrypted_content` through in tool chains. (4) Recalculate prices — 2.0-lite was tiered by input length, Lite is flat. (5) Prompt rules as for all Ark deep-thinking models: remove reasoning scaffolding and few-shot examples, add goal/scenario, put format in `response_format`.
- **Pro ↔ Lite**: identical parameter surface (same `thinking.type`, effort and summary rules, same lengths for Pro 260915) — a prompt rewrite is usually unnecessary; reassess: quality on highly complex tasks (Pro is positioned for this per the release note; a direct Pro-vs-Lite comparison is unverified), price (output 2.70 ¥ instead of 30.00 ¥), throughput (30,000 instead of 500 RPM), and audio, which only Lite accepts.
- **AWAY FROM doubao-seed-2.1-lite**: carry audio content over only if the target documents audio input (Pro and Turbo accept only text/image/video according to the Ark model pages). For Lite → Turbo, plan the context down to 256k. `thinking.type`, `reasoning_effort` and `encrypted_content` are Ark-specific — map thinking control onto the target guide anew; re-add removed CoT scaffolding, examples and role separation if the target is not an always-on reasoner; check throughput against the target's limits.

## Sources
- https://docs.volcengine.com/docs/ark/model-list?lang=zh — Ark model list (status 2026.10.09): `doubao-seed-2-1-lite-260915` under 推荐模型 with capability tags, 1024k context / 1024k input / 256k response at default 4k / 256k chain-of-thought, 30000 RPM / 5000000 TPM; Lite in the audio-understanding table; tool and caching matrix; 2.0 limits (224k input, 128k response) and 500 RPM of 2.1 Pro/Turbo for comparison.
- https://docs.volcengine.com/docs/ark/deep-thinking?lang=zh — deep-thinking page (status 2026.10.09): `thinking.type` support (Lite only `enabled`/`disabled`), effort table (2.1 models default `high`, 2.0 models default `medium`, mapping `minimal`/`none`/`xhigh`/`max`), thinking-summary model list with `reasoning_content`/`encrypted_content` and return rules, latency and timeout notes, prompt optimization recommendations.
- https://docs.volcengine.com/docs/ark/structured-output-beta?lang=zh — structured output (beta, status 2026.09.22): `json_schema`/`json_object`, schema restrictions, beta and TPM-package caveat, penalty warning, prompt recommendations (appendix 3).
- https://docs.volcengine.com/docs/ark/model-pricing?lang=zh — pricing page (status 2026.10.10): `doubao-seed-2.1-lite` in the online, low-latency, low-priority and batch tables incl. audio columns; tiered 2.0-lite prices as contrast.
- https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh — release announcements (status 2026.10.13): `doubao-seed-2-1-lite-260915` as 新发布 (newly released) under 202609, omni-modal (text, vision, audio) with 1M context, improved coding/agent tasks; `doubao-seed-2-1-pro-260628` under 202606 positioned for highly complex coding/agent tasks.
- https://docs.volcengine.com/docs/ark/model-deprecation-notice?lang=zh — deprecations (status 2026.10.09): batch 10, Lite as recommended target for doubao-seed-2-0-pro-260215 and -lite-260215, EOS dates and automatic switch or shutdown.
- https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seed-2-1-lite — Ark model page: 260915 as 首推, input text/image/video/audio → text, prices incl. fast tier, supported APIs (incl. batch), improvement over Doubao-Seed-2.0-lite/260428 and usage scenarios.
- https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seed-2-1-pro — Ark model page Pro: input text/image/video → text (no audio).
- https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seed-2-1-turbo — Ark model page Turbo: input text/image/video → text (no audio); request example with `image_url` and `text` content parts in one user message.
- https://docs.byteplus.com/en/docs/modelark/model-list — BytePlus ModelArk model list (status 2026-10-13): from the 2.1 series only `dola-seed-2-1-turbo-260628`, no Lite variant.
