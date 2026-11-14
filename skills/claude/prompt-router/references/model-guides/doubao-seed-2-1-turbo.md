---
model: doubao-seed-2-1-turbo
vendor: ByteDance
family: Doubao
aliases: [doubao-seed-2-1-turbo-260628, dola-seed-2-1-turbo-260628, doubao-seed-2.1-turbo, seed-2.1-turbo]
last_verified: 2026-10-13
status: current
---

# Doubao Seed 2.1 Turbo

## Reasoning / Thinking
- Type: **deep thinking on by default**. `thinking.type` platform-wide knows `enabled | disabled | auto`; doubao-seed-2-1-turbo-260628 (Ark) and dola-seed-2-1-turbo-260628 (BytePlus) appear in the support list only with `enabled` (default) and `disabled` — **no `auto`**.
- Depth via `reasoning_effort` (Chat API) or `reasoning.effort` (Responses API). On Ark the same line applies as for 2.1 Pro: all seven levels are accepted, **default `high`**, `minimal` = off, `none` → `minimal`, **`xhigh`/`max` → `high`**. The Ark model page summarizes this as four effective modes `minimal | low | medium | high`. On BytePlus the effort table row for the dola ID is listed without default and mapping — there, always set `reasoning_effort` explicitly (default unverified).
- **Thinking summary active by default** (Ark and BytePlus): `reasoning_content` contains only a summary, `encrypted_content` the encrypted original. `reasoning_effort` only affects the raw chain-of-thought; raw tokens are billed. Higher package latency according to the docs — raise `timeout`.
- Tool calling: **play back `encrypted_content` unchanged** (precedence over `reasoning_content`; returning only the summary lowers quality in agent runs, returning nothing raises no error); in the Responses API `previous_response_id` handles this.
- Maximum chain-of-thought 256k tokens; it shares the output budget with the answer.

## Prompting style
- The deep-thinking recommendations apply identically on Ark and BytePlus: add **goal, scenario and audience** instead of only naming the task; **reduce or avoid step-by-step decomposition and examples** (they narrow the reasoning logic); **reduce system prompts** and pass everything via `role: user`.
- Structured output: put the format in `response_format` (`json_schema`, `strict: true`); in the prompt neither stress "output JSON" nor repeat the schema, but describe the substantive content; omit `frequency_penalty`/`presence_penalty` in this case.
- Images go as an `image_url` content part in the same user message as the text (example on the Ark model page).

## Strengths & weaknesses (prompt-relevant)
- Positioning per release note: **cost-effective low-latency variant for large-scale production**, fully featured, "on par" with doubao-seed-2-1-pro; intended for high volumes of online calls in coding, agent and multimodal tasks and for deployments where cost, throughput and batch take priority. The Seed2.1 page names Pro and Turbo as the two sizes of the family.
- According to the Ark model page: coding across the whole development chain, including long-running repo-level coding agents; end-to-end agent execution with more flexible fallbacks and better use of external CLIs; VLM with more stable **GUI operation across mobile, desktop and web** and finer image/video understanding.
- Capability tags: deep thinking, text generation, multimodal understanding (input text, image, video → text; **no audio**), GUI tasks, tool calling, structured output. Full Ark tool matrix (function calling, knowledge base, MCP, web search, image processing, Doubao assistant); BytePlus lists function calling and MCP.
- Weaknesses/quirks: **only 256k context** (Pro 260915 and Lite: 1024k); **500 RPM / 1,000,000 TPM** like Pro (Lite: 30,000 RPM); **default response length 4k**; structured output is beta and not usable with TPM guarantee packages; no `auto`, no real level above `high`. No knowledge cutoff published (unverified).
- Availability: the only Seed 2.1 model on BytePlus ModelArk (international).

## Output & format conventions
- Ark (China) model ID: `doubao-seed-2-1-turbo-260628` (推荐模型 = recommended, 首推 = top pick); base URL in the docs examples `https://ark.cn-beijing.volces.com/api/v3`. BytePlus (international) model ID: **`dola-seed-2-1-turbo-260628`**, region ap-southeast-1 with base URL `https://ark.ap-southeast.bytepluses.com/api/v3` (per BytePlus, eu-west-1 additionally lists only the seed-2-0 and seedream-5-0-lite models). `doubao-seed-2.1-turbo` is only a billing name on the pricing page (as a model ID unverified).
- Lengths (same on Ark and BytePlus): context 256k, max input 256k, max response incl. chain-of-thought 256k at **default 4k**, max chain-of-thought 256k. Limit via `max_completion_tokens` or `max_output_tokens`.
- Structured output: `json_schema` with `strict: true` recommended; `json_object` requires the string `json` in the input; field order follows the schema; `$ref` only local, `oneOf`/`allOf` without semantic guarantee; unsupported keywords throw an error.
- Operations: streaming recommended, otherwise `timeout` above 30 minutes. Caching: implicit via Responses and Chat API, explicit via Responses API (prefix and session cache) — on Ark and BytePlus.
- Volcengine prices per million tokens (0–256k, flat): online 3.00 ¥ input / 0.60 ¥ cache hit / 15.00 ¥ output, cache storage 0.017 ¥ per million tokens/hour; low-latency (fast) 6.00 / 1.20 / 30.00 ¥; low-priority (flex) and batch 1.50 / 0.60 / 7.50 ¥ — i.e. half the Pro price in the online tier. BytePlus prices are not captured here (unverified).

## Migration notes
- **Pro ↔ Turbo**: same parameter surface (same `thinking.type`, effort, summary and return rules, same response/chain-of-thought limits) — the prompt itself usually needs no rework. Reassess only: context (Pro 260915: 1024k, Turbo: 256k — Pro→Turbo prompts with more than 256k input must be chunked again), price and latency; secure quality differences with your own evaluation (the release note only says "on par").
- **TO doubao-seed-2.1-turbo**: (1) remove reasoning scaffolding and few-shot examples, add goal/scenario, slim down the system prompt. (2) Set `reasoning_effort` explicitly — `xhigh`/`max` from other providers silently land on `high`; on BytePlus no default is documented. (3) Fast paths via `thinking: {"type":"disabled"}` or `reasoning_effort: "minimal"`, since there is no `auto`. (4) Set `max_completion_tokens`/`max_output_tokens` against the 4k default. (5) Move the format into `response_format`. (6) In tool chains pass `encrypted_content` through. (7) Adjust concurrency to 500 RPM / 1M TPM. (8) Internationally always use the `dola-` ID and the BytePlus base URL. (9) Audio inputs drop out — only Lite is documented for audio within the family.
- **AWAY FROM doubao-seed-2.1-turbo**: `thinking.type`, `reasoning_effort` and `encrypted_content` are Ark-specific — map thinking control onto the target guide anew instead of copying it 1:1 or removing it wholesale; re-add removed CoT scaffolding, examples and role separation if the target is not an always-on reasoner; translate `response_format` into the structured-output form of the target.

## Sources
- https://docs.volcengine.com/docs/ark/model-list?lang=zh — Ark model list (status 2026.10.09): `doubao-seed-2-1-turbo-260628` under 推荐模型 with capability tags, 256k context / 256k input / 256k response at default 4k / 256k chain-of-thought, 500 RPM / 1000000 TPM; tool and caching matrix; Pro 260915 and Lite with 1024k for comparison; Turbo missing from the audio table.
- https://docs.volcengine.com/docs/ark/deep-thinking?lang=zh — deep-thinking page (status 2026.10.09): `thinking.type` support (Turbo only `enabled`/`disabled`), effort table (Turbo in the same row as Pro: default `high`, mapping), thinking-summary list, return rules for `encrypted_content`, timeout and streaming notes, prompt optimization recommendations.
- https://docs.volcengine.com/docs/ark/structured-output-beta?lang=zh — structured output (beta, status 2026.09.22): `json_schema`/`json_object`, schema restrictions, beta and TPM-package caveat, penalty warning, prompt recommendations (appendix 3).
- https://docs.volcengine.com/docs/ark/model-pricing?lang=zh — pricing page (status 2026.10.10): `doubao-seed-2.1-turbo` in the online, low-latency, low-priority and batch tables; Pro prices as comparison.
- https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh — release announcements (status 2026.10.13): `doubao-seed-2-1-turbo-260628` as 新发布 under 202606 — cost-effective, low latency, fully featured, comparable to doubao-seed-2-1-pro, for production with high call volume.
- https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seed-2-1-turbo — Ark model page: 260628 as 首推, input text/image/video → text, prices incl. fast and flex tiers, `reasoning_effort` with four modes and default `high`, coding/agent/VLM points (GUI across mobile, desktop, web), request example with `image_url`.
- https://seed.bytedance.com/en/seed2_1 — Seed2.1 page: family with the two sizes Pro and Turbo.
- https://docs.byteplus.com/en/docs/modelark/model-list — BytePlus ModelArk model list (status 2026-10-13): `dola-seed-2-1-turbo-260628` as the only 2.1 model, lengths and limits, function calling/MCP, caching, structured output (beta); regions ap-southeast-1/eu-west-1 and base URLs.
- https://docs.byteplus.com/en/docs/modelark/deep-thinking — BytePlus deep-thinking page (status 2026-10-06): dola Turbo with `enabled` (default)/`disabled`, in the thinking-summary list, effort table row without default/mapping, prompt recommendations as on Ark.
