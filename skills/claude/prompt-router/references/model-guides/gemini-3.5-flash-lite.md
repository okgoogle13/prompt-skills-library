---
model: gemini-3.5-flash-lite
vendor: Google
family: Gemini
aliases: [gemini-flash-lite, gemini-3-5-flash-lite, 3.5-flash-lite, gemini-flash-lite-3.5, gemini3.5flashlite]
last_verified: 2026-10-13
status: current
---

# Gemini 3.5 Flash-Lite

## Reasoning / Thinking
- Type: **dynamic thinking with a minimal default**. Control via the string enum `thinking_level` with `minimal | low | medium | high`, default **`minimal`** (thinking table: "On (minimal)").
- `minimal` corresponds, per the docs, to the "no thinking" setting for most requests, but does not guarantee that thinking is switched off ("`minimal` does not guarantee that thinking is off").
- Level choice per the migration checklist: for extraction, routing and classification at high volume keep `minimal`; for autonomous subagents with tool calls, code execution or multi-step reasoning set `medium` or `high`, "to prevent premature tool termination". For document parsing Google advises testing `minimal` against `high` depending on document complexity.
- `thinking_budget` is superseded; `thinking_level` and `thinking_budget` in the same request return a 400 error. The levels are "relative allowances for thinking rather than strict token guarantees".
- Thought signatures: in stateful operation (`store: true` + `previous_interaction_id`) the server manages them; stateless, all `thought` blocks must be returned unchanged. Thinking tokens are billed as output, and `max_output_tokens` counts them.

## Prompting style
- **Terse and direct**: "Be concise. Gemini 3.x responds best to direct, clear instructions." According to the docs, verbose prompt-engineering techniques from older models can cause the model to "over-analyze".
- **Request conversational tone**: Gemini 3.x is by default not very verbose; explicitly ask for a conversational tone.
- **Long context**: data first, question or instruction at the end, introduced by "Based on the preceding information...".
- **No sampling control**: `temperature`, `top_p` and `top_k` are "deprecated and ignored"; future model generations return HTTP 400. For more determinism, Google suggests a system instruction with explicit rules.
- **No assistant prefill**: a request ending with a non-empty `model` turn returns 400. Enforce the output form via `system_instruction` or structured outputs.
- **Subagent prompts**: because the default is `minimal`, the thinking depth for planning and tool tasks must be raised actively via `thinking_level`; Google explicitly names this for "autonomous planning and complex subagent tasks".

## Strengths & weaknesses (prompt-relevant)
- Strengths per Google: highest throughput in the 3.5 family for data parsing and document extraction; more reliable tool execution with code execution, search and MCP; more precise document parsing and structured data extraction; front-end JavaScript and table processing via lightweight code execution; more stable multi-turn instruction following and persona consistency than Gemini 3.1 Flash-Lite; computer use as a built-in tool.
- Compared with Gemini 2.5 Flash, Google names a "Strong migration path" with higher scores on HLE (18.0% vs. 11.0%) and CharXIV (74.5% vs. 63.7%).
- Model card: based on Gemini 3.1 Flash-Lite; optimized for latency-critical, high-volume tasks such as translation and classification, and for agentic workflows.
- Weaknesses per the model card: usual hallucinations, jailbreak resistance still a work in progress, occasional slowness or timeouts. Knowledge cutoff **March 2026**, in some domains only January 2025.
- Image segmentation (pixel masks) is, according to Google, not supported in Gemini 3.x.

## Output & format conventions
- 1,048,576 input tokens / 65,536 output tokens. Input: text, image, video, audio, PDF → output text only.
- Supported: structured outputs, function calling, caching, code execution, search grounding, URL context, file search, grounding with Google Maps, computer use (preview), batch, flex and priority inference. **Not** supported: audio generation, image generation, Live API.
- Function calling: same rules as for 3.6 Flash — multimodal assets go into the response payload, inline instructions in function responses are formatted with `\n\n`.
- Price per 1M tokens (paid tier): input $0.30, output $2.50 (incl. thinking tokens); batch $0.15 / $1.25; context caching $0.03 plus $1.00 storage per 1M tokens/hour.

## Migration notes
- **Status**: GA since 21 Jul 2026, no shutdown date announced. For new projects Google names "3.5 Flash-Lite or 3.8 Flash" as the "latest models". There is no newer Flash-Lite text model; `gemini-3.1-flash-lite` (shutdown no earlier than 7 May 2027) names `gemini-3.5-flash-lite` as its replacement.
- **TO gemini-3.5-flash-lite**: swap the ID; choose `thinking_level` deliberately (`minimal` for throughput, `medium`/`high` for subagents with tools); remove `temperature`/`top_p`/`top_k`, `candidate_count` and prefilled model turns; check function calling under the same rules as 3.6 Flash; keep thought signatures or switch to `previous_interaction_id`; remove verbose prompt engineering and CoT scaffolding.
- Specifically **from `gemini-2.5-flash`**: replace `thinkingBudget` with `thinking_level`; a budget of `0` most closely maps to `minimal`, which however does not guarantee that thinking is off; remove explicitly set temperature. Do not migrate segmentation workloads — Google still recommends Gemini 2.5 Flash with thinking switched off for these.
- Specifically **from `gemini-3.1-flash-lite`**: same `minimal` default; Google names better persona consistency and instruction following across multiple turns.
- **AWAY FROM gemini-3.5-flash-lite**: translate `thinking_level` into the control of the target — to `gemini-3.8-flash`, `minimal` is raised to `low`, because `minimal` throws an error there; remove thought-signature and `previous_interaction_id` logic if the target does not know them; set sampling parameters only if the target guide requires them; reassess cost and latency.

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite — model page: ID `gemini-3.5-flash-lite` (stable, July 2026), 1,048,576 input / 65,536 output, input text/image/video/audio/PDF → text, capability list incl. computer use (preview), unsupported features, focus on subagents and document parsing.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6 — "What's new in Gemini 3.6 Flash and 3.5 Flash-Lite": default `minimal`, price $0.30 / $2.50, strengths (throughput, tool reliability, document parsing, persona consistency), "Strong migration path from Gemini 2.5 Flash" with HLE and CharXIV values, sampling deprecation and prefill 400, checklist "Migrate to gemini-3.5-flash-lite" (`minimal` for throughput, `medium`/`high` "to prevent premature tool termination").
- https://ai.google.dev/gemini-api/docs/thinking — thinking table (`gemini-3.5-flash-lite`: "On (minimal)", `minimal, low, medium, high`), thought signature handling stateful/stateless, thinking tokens in billing, `max_output_tokens` incl. thought tokens.
- https://ai.google.dev/gemini-api/docs/generate-content/thinking — `thinkingLevel` table (3.5 & 3.1 Flash-Lite: `minimal` default), "`minimal` does not guarantee that thinking is off", 2.5 Flash budget 0 to 24576.
- https://ai.google.dev/gemini-api/docs/gemini-3 — "relative allowances for thinking rather than strict token guarantees", 400 error for `thinking_level` + `thinking_budget`.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 — best practices for all Gemini 3.x (brevity, verbosity, long-context rule), "Image segmentation is not supported in Gemini 3.x" with the recommendation to use Gemini 2.5 Flash with thinking off.
- https://ai.google.dev/gemini-api/docs/models — model list: Gemini 3.5 Flash-Lite (stable) and the note "For any new projects, use our latest models: 3.5 Flash-Lite or 3.8 Flash".
- https://ai.google.dev/gemini-api/docs/deprecations — `gemini-3.5-flash-lite` (21 Jul 2026, no shutdown date announced); `gemini-3.1-flash-lite` with shutdown 7 May 2027 and replacement `gemini-3.5-flash-lite`.
- https://ai.google.dev/gemini-api/docs/changelog — 21 Jul 2026: GA of Gemini 3.5 Flash-Lite as "low-latency, highly cost-effective subagent option".
- https://ai.google.dev/gemini-api/docs/pricing — 3.5 Flash-Lite prices: $0.30 / $2.50, batch $0.15 / $1.25, caching $0.03 plus $1.00 storage per 1M tokens/hour.
- https://deepmind.google/models/model-cards/gemini-3-5-flash-lite/ — model card: based on Gemini 3.1 Flash-Lite, focus on translation, classification and agentic workflows, limitations (hallucinations, jailbreak, slowness/timeouts), knowledge cutoff March 2026 (partly January 2025).
