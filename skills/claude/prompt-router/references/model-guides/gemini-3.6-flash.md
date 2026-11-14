---
model: gemini-3.6-flash
vendor: Google
family: Gemini
aliases: [gemini-3.6, gemini-3-6-flash, 3.6-flash, gemini-flash-3.6, gemini3.6flash, gemini-3.5-flash]
last_verified: 2026-10-13
status: legacy
successor: gemini-3.8-flash
---

# Gemini 3.6 Flash

## Reasoning / Thinking
- Type: **dynamic thinking, on by default**. Control via the string enum `thinking_level` with `minimal | low | medium | high`, default **`medium`** (thinking table: "On (medium)"). Unlike `gemini-3.8-flash`, 3.6 Flash knows the level `minimal`.
- `minimal` corresponds, per the docs, to the "no thinking" setting for most requests, but does not guarantee that thinking is switched off ("`minimal` does not guarantee that thinking is off"). A genuine zero-thinking path such as `thinkingBudget = 0` on Gemini 2.5 Flash does not exist.
- `thinking_budget` is superseded: "Replace `thinking_budget` with `thinking_level`". Both parameters in the same request return a 400 error. The levels are "relative allowances for thinking rather than strict token guarantees".
- `max_output_tokens` counts thought tokens and cuts off hard, even mid-reasoning. To reduce cost or latency, Google recommends lowering `thinking_level` rather than setting a small `max_output_tokens`.
- Thought signatures carry reasoning continuity across turns. In stateful operation (`store: true` + `previous_interaction_id`) the server manages them; stateless, all `thought` blocks must be returned unchanged. Billing: "response pricing is the sum of output tokens and thinking tokens".

## Prompting style
- **Terse and direct**: "Be concise. Gemini 3.x responds best to direct, clear instructions." Verbose prompt-engineering techniques for older models can, according to the docs, make the model "over-analyze"; replace hand-written CoT chains with `thinking_level`.
- **Request conversational tone**: Gemini 3.x responds by default in a less verbose and direct way; explicitly request a conversational tone in the prompt.
- **Long context**: data first, the concrete question or instruction at the end, introduced by an anchor such as "Based on the preceding information...".
- **No sampling control**: `temperature`, `top_p` and `top_k` are "deprecated and ignored"; future model generations respond with HTTP 400. For more determinism, Google instead recommends a system instruction with explicit rules.
- **No assistant prefill**: if the request ends with a non-empty `model` turn, a 400 error is returned. Enforce the output form via `system_instruction` or structured outputs.
- **UI work**: human raters preferred earlier models for visual layout and styling; Google advises compensating via "explicit design guidelines" in the prompt.

## Strengths & weaknesses (prompt-relevant)
- Strengths per Google: fewer reasoning steps, turns and tool calls than Gemini 3.5, and less "execution loop spiraling"; code with fewer unwanted edits and debugging loops; better instruction following (fewer unwanted file changes on diagnostic tasks); strong multimodal and spatial reasoning (charts, blueprints, web layouts). The model page names code generation, agentic execution and spatial reasoning as focus areas.
- Quirk "upfront programmatic inspection": runs diagnostic scripts before changes more often than 3.5 Flash. This improves accuracy on complex tasks but can cost additional exploratory steps on routine front-end work. Google does not name an official countermeasure via the prompt.
- Model card: "workhorse model" with better token efficiency than 3.5 Flash, based on Gemini 3.5 Flash; fields of use agentic workflows, complex video reasoning, coding, enterprise workflows.
- Weaknesses per the model card: usual hallucinations, jailbreak resistance still a work in progress, occasional slowness or timeouts, slight regression in the tone of refusals compared with 3.5 Flash. Knowledge cutoff **March 2026**, in some domains only January 2025 — put time-critical facts in the prompt.
- Image segmentation (pixel masks) is, according to Google, not supported in Gemini 3.x.

## Output & format conventions
- 1,048,576 input tokens / 65,536 output tokens. Input: text, image, video, audio, PDF → output text only.
- Supported: structured outputs, function calling, caching, code execution, search grounding, URL context, file search, grounding with Google Maps, computer use (preview), batch, flex and priority inference. **Not** supported: audio generation, image generation, Live API.
- Function calling: multimodal assets belong in the response payload; inline instructions in function responses are formatted with `\n\n`. `Malformed_Function_Call` errors associated with text before the tool call are a documented failure pattern.
- Price per 1M tokens (paid tier): input $0.75 / output $3.75 until 31 Dec 2026, from 1 Jan 2027 $1.50 / $7.50; batch $0.375 / $1.875 until 31 Dec 2026, then $0.75 / $3.75 — the same tier as `gemini-3.8-flash`.

## Migration notes
- **Status caveat**: Google lists 3.6 Flash as "Our previous-generation Flash model"; the newest Flash version is `gemini-3.8-flash`. 3.6 Flash is **not** deprecated, remains "available for production use", and no shutdown date is announced. Google explicitly names it as an alternative if the higher token consumption of 3.8 Flash is not needed ("Alternatively, Gemini 3.6 Flash remains supported"). When switching to 3.8 Flash, note: `minimal` throws an error there.
- **`gemini-3.5-flash` resolves to this guide**: 3.5 Flash has been deprecated since 8 Oct 2026, and API requests are automatically routed to `gemini-3.6-flash`; Google calls 3.6 Flash the "Direct replacement for `gemini-3.5-flash`". A prompt tuned for 3.5 Flash therefore already runs on 3.6 Flash; the `medium` default is unchanged, only the model string needs updating.
- **TO gemini-3.6-flash**: swap the ID; remove `temperature`/`top_p`/`top_k`, `candidate_count` and prefilled model turns; replace `thinking_budget` with `thinking_level` (the checklist names `"medium"` or `"high"`); check function calling (multimodal assets in the response payload, inline instructions in function responses with `\n\n`); keep thought signatures or switch to `previous_interaction_id`; remove verbose prompt-engineering leftovers and CoT scaffolding; for UI tasks add explicit design guidelines. The selection table maps 3.6 Flash to the workloads of Gemini 3.5 Flash, Gemini 3 Flash (preview) and Gemini 3.1 Pro; the deprecation list names it as the replacement for `gemini-3-flash-preview`. Do not migrate segmentation workloads here.
- **AWAY FROM gemini-3.6-flash**: translate `thinking_level` into the control of the target (to 3.8 Flash: `minimal` → `low`, re-measure token consumption); remove `previous_interaction_id` and thought-signature logic if the target does not know them; set sampling parameters only if the target guide requires them; re-enrich terse prompts only if the target needs explicit scaffolding.

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash — model page: ID `gemini-3.6-flash` (stable), 1,048,576 input / 65,536 output, input text/image/video/audio/PDF → text, full capability list incl. computer use (preview) and unsupported features, focus areas "code generation, agentic execution, and spatial reasoning".
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6 — "What's new in Gemini 3.6 Flash and 3.5 Flash-Lite": "previous-generation releases … remain available for production use", default `medium`, token and turn reduction, code and instruction improvements, "Upfront programmatic inspection", UI styling note with "explicit design guidelines", sampling deprecation ("deprecated and ignored", HTTP 400 in future), prefill → 400 with `system_instruction`/structured outputs as replacement, migration checklist, selection table (3.5 Flash, 3 Flash Preview, 3.1 Pro).
- https://ai.google.dev/gemini-api/docs/thinking — thinking table (`gemini-3.6-flash`: "On (medium)", `minimal, low, medium, high`), `max_output_tokens` incl. thought tokens, stateful vs. stateless thought signature handling, "response pricing is the sum of output tokens and thinking tokens".
- https://ai.google.dev/gemini-api/docs/generate-content/thinking — `thinkingLevel` table (3.6 Flash: `minimal` supported, `medium` default), "`minimal` does not guarantee that thinking is off", default level 3.6 Flash `medium`.
- https://ai.google.dev/gemini-api/docs/gemini-3 — Gemini 3 family: "relative allowances for thinking rather than strict token guarantees", 400 error for `thinking_level` + `thinking_budget` in the same request.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 — best practices for all Gemini 3.x ("Be concise…", low default verbosity, long-context rule with "Based on the preceding information..."), "Image segmentation is not supported in Gemini 3.x", 3.5 Flash deprecated and routed to 3.6 Flash, 3.6 Flash as "Direct replacement for `gemini-3.5-flash`".
- https://ai.google.dev/gemini-api/docs/latest-model — Gemini 3.8 Flash guide: "can use more tokens on longer running and complex tasks, by design", "Alternatively, Gemini 3.6 Flash remains supported", `minimal` not supported on 3.8 Flash.
- https://ai.google.dev/gemini-api/docs/models — model list: Gemini 3.6 Flash "Our previous-generation Flash model" (stable), Gemini 3.8 Flash as the newest Flash version.
- https://ai.google.dev/gemini-api/docs/deprecations — `gemini-3.6-flash` (21 Jul 2026, no shutdown date announced); `gemini-3.5-flash` with auto-routing to `gemini-3.6-flash`; `gemini-3.6-flash` as the recommended replacement for `gemini-3-flash-preview`.
- https://ai.google.dev/gemini-api/docs/changelog — 21 Jul 2026 GA of 3.6 Flash and deprecation of the sampling parameters; 8 Oct 2026 deprecation of `gemini-3.5-flash` with automatic routing to `gemini-3.6-flash`.
- https://ai.google.dev/gemini-api/docs/pricing — price tier for 3.6 Flash: $0.75 / $3.75 until 31 Dec 2026, then $1.50 / $7.50; batch $0.375 / $1.875 → $0.75 / $3.75.
- https://deepmind.google/models/model-cards/gemini-3-6-flash/ — model card (21 Jul 2026): "workhorse model", token efficiency relative to 3.5 Flash, based on Gemini 3.5 Flash, fields of use, limitations (hallucinations, jailbreak, slowness/timeouts), knowledge cutoff March 2026 (partly January 2025), slight tone regression.
