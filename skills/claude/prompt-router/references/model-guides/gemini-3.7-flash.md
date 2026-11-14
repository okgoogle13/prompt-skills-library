---
model: gemini-3.7-flash
vendor: Google
family: Gemini
aliases: [gemini-3.7, gemini-3-7-flash, 3.7-flash, gemini-flash-3.7]
last_verified: 2026-10-13
status: legacy
successor: gemini-3.8-flash
---

# Gemini 3.7 Flash

## Reasoning / Thinking
- Type: **string enum, no token budget**. `thinking_level` with `low | medium | high`; default is `medium`. `minimal` is invalid here ("`minimal` is not supported and returns an error"). Meaning per the docs: `low` = shorter time-to-answer for latency-critical cases, `medium` = best quality for most tasks, `high` = maximum thinking and maximum tool use, with higher token consumption and higher cost.
- Note the family break: the `medium` default for 3.7 Flash appears in "What's new in Gemini 3.7 Flash" and on the model card. The wording "The default thinking effort is now `medium`, changed from `high` in Gemini 3 Flash Preview" comes from the Gemini 3.5 Flash guide and does not name 3.7 Flash itself. Other 3.x models still default to `high` (Gemini 3.1 Pro, Gemini 3 Flash) or `minimal` (Gemini 3.1 Flash-Lite).
- `thinking_budget` is legacy: the Gemini 3 checklists replace it with the string enum `thinking_level`. It is still accepted in Gemini 3 for backward compatibility, but must not appear together with `thinking_level` in the same request (400 error); levels are relative allowances, not token guarantees.
- Reasoning state runs via **thought signatures** (encrypted representations of the internal reasoning). On the legacy `generateContent`, the complete, unchanged history including thought signatures must be sent back; the Interactions API does this automatically (`previous_interaction_id`).

## Prompting style
- **Short and direct**: "Be concise. Gemini 3.x responds best to direct, clear instructions." Explicit warning: "Verbose or complex prompt engineering techniques designed for older models may cause the model to over-analyze."
- No handwritten chain-of-thought — instead use `thinking_level: "medium"`/`"high"` with a simpler prompt.
- For long context / large data, place the concrete question or instruction **at the end, after the data block** (anchor such as "Based on the preceding information...").
- Function calling: format inline instructions in function responses with `\n\n` — the docs list this rule under "Audit function calling", not as a general prompt rule.
- Sampling: for Gemini 3 Google recommends the temperature default `1.0` ("may lead to unexpected behavior, such as looping or degraded performance"). Since Gemini 3.6 Flash, `temperature`, `top_p` and `top_k` are "deprecated and ignored" for this and all following models — remove them from the generation config.
- Tone: "By default, Gemini 3 and 3.1 is less verbose and prefers direct, efficient answers." — explicitly request a conversational style (family statement; not separately confirmed for 3.7 Flash). For dense documents set `media_resolution` per item (`low|medium|high|ultra_high`); the docs advise testing `media_resolution_high` for PDFs ("test the new `media_resolution_high` setting to ensure continued accuracy").

## Strengths & weaknesses (prompt-relevant)
- Strengths: "Significantly higher quality on real-world software engineering and agentic benchmarks, improving issue resolution and reducing failed agent loops"; "higher-fidelity desktop and web application code directly from design mocks, with strong gains in design adherence". Model card: 43.6% on FrontierCode 1.1, 97.0% on GDM-MRCR v2 (8-needle) at 128k context; target profile agentic workflows, coding, enterprise automation. Knowledge cutoff: March 2026.
- Weaknesses/quirks: general foundation-model limits including hallucinations; "occasional slowness or timeout issues"; some domains only covered up to January 2025; jailbreak resistance still a work in progress per Google.
- Modality gaps: no image generation, no audio generation, Live API "Not supported". Image segmentation (pixel masks) is "not supported in Gemini 3.x" per Google — do not migrate segmentation workloads to Gemini 3.x (Gemini 2.5 is legacy here; verify the target's segmentation support beforehand). Google itself still recommends Gemini 2.5 Flash with thinking switched off for this, which, however, has been open only to existing users since 18 Sep 2026.

## Output & format conventions
- **Deprecated since 8 Oct 2026** (GA was 13 Aug 2026): "API requests to `gemini-3.7-flash` are automatically routed to `gemini-3.8-flash`"; the endpoint is not shut down, but it is no longer selectable in Google AI Studio. A prompt targeting `gemini-3.7-flash` is in practice executed by 3.8 Flash. Context: **1,048,576 input tokens**, **65,536 output tokens** (docs shorthand: "a 1M token context window, 64k max output tokens").
- Input: text, image, video, audio, PDF — output: text only. Supported: structured outputs, function calling, caching, code execution, search grounding, URL context, file search, Maps grounding, computer use (preview), batch/flex/priority. Not supported: Live API, image generation, audio generation.
- Structured outputs can be combined with built-in tools: "Gemini 3 models allow you to combine Structured Outputs with built-in tools, including Grounding with Google Search, URL Context, Code Execution, and Function Calling." (family statement for Gemini 3, not phrased specifically for 3.7 Flash.)
- **No assistant prefill**: since Gemini 3.6 Flash, a request ending with a non-empty `model` turn returns a 400 error; `candidate_count` is not supported from Gemini 3 onward. Enforce the desired output form via a response schema or system instruction.
- Historical (the pricing page no longer lists 3.7 Flash): launch per the changelog with an introductory price until 31 Dec 2026; the concrete values (input $0.75 / output $3.75 per 1M tokens, then $1.50 / $7.50) can no longer be officially verified (unverified).

## Migration notes
- **Status caveat**: deprecated since 8 Oct 2026, replaced by `gemini-3.8-flash`; all API requests to `gemini-3.7-flash` are automatically routed there. No shutdown date; the endpoint stays reachable.
- **AWAY FROM gemini-3.7-flash**: re-add explicit step-by-step/CoT scaffolding; translate `thinking_level` into the effort/budget control of the target model; set temperature explicitly again (the 1.0 default is not a portable assumption); remove thought-signature plumbing; materialize the conversation history client-side, since `previous_interaction_id` has no equivalent; prefill is allowed again elsewhere. For `gemini-3.8-flash` the change is essentially only the model string, because 3.7 requests already run there.
- **TO gemini-3.7-flash**: do not choose it as a target any more — requests land on `gemini-3.8-flash`; migrate there directly. For existing prompts: remove `temperature`/`top_p`/`top_k`; `thinking_budget` → `thinking_level` (a 2.5 zero budget becomes `low`, **not** `minimal`); remove `candidate_count`; rewrite prefill turns into instructions or the response schema; standardize multi-turn on `previous_interaction_id` (Interactions API, `store=true`); trim verbose prompts and resolve CoT into `thinking_level`; retest dense PDFs with `media_resolution_high`; check function calling — multimodal content belongs *in* the function-response parts, format inline instructions there with `\n\n`, and thought signatures from the tool turn must be returned. Do not migrate image-segmentation prompts here.

## Sources
- https://ai.google.dev/gemini-api/docs/models — official model list; no longer lists 3.7 Flash since the deprecation, lists 3.8 Flash as the newest Flash version.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.7 — "What's new in Gemini 3.7 Flash" (kept as reference, with deprecation note): thinking_level values and `medium` default, meaning of the levels, coding/agentic/web-design improvements, "a 1M token context window, 64k max output tokens".
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6#api-changes-and-parameter-updates — API changes from 3.6 Flash "and all future Gemini model releases": sampling parameters "deprecated and ignored", prefill turn → 400, `candidate_count` "unsupported in Gemini 3 and later".
- https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash — model page: since Oct 2026 carries the deprecated notice with auto-routing to `gemini-3.8-flash`; 1,048,576 input / 65,536 output, modalities, capability list, no Live API, "`minimal` is not supported and returns an error".
- https://deepmind.google/models/model-cards/gemini-3-7-flash/ — DeepMind model card: published 13 Aug 2026; knowledge cutoff March 2026 (individual domains January 2025), 1M in / 64K out, FrontierCode 1.1 43.6%, GDM-MRCR v2 (8-needle) @128k 97.0%, documented limitations (hallucinations, "occasional slowness or timeout issues", "we are continually working to improve jailbreak resistance").
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 — Gemini 3.5 Flash guide (family level, does not name 3.7 Flash): "The default thinking effort is now `medium`, changed from `high` in Gemini 3 Flash Preview", brevity guidance ("Be concise. Gemini 3.x responds best to direct, clear instructions."), verbosity and long-context rule, media_resolution levels, full unchanged history incl. thought signatures on `generateContent`, "Image segmentation is not supported in Gemini 3.x".
- https://ai.google.dev/gemini-api/docs/latest-model — Gemini 3.8 Flash guide: migration checklist with `thinking_budget` → `thinking_level` and the `\n\n` rule under "Audit function calling".
- https://ai.google.dev/gemini-api/docs/generate-content/thinking — `thinking_budget` "accepted for backwards compatibility" in Gemini 3, default level per model (3.1 Pro `high`, 3 Flash `high`, 3.1 Flash-Lite `minimal`).
- https://ai.google.dev/gemini-api/docs/migrate-to-interactions — Interactions API as the recommended surface ("we recommend the Interactions API for all new development"), `previous_interaction_id` and `store=true` semantics.
- https://ai.google.dev/gemini-api/docs/gemini-3 — family guidance: temperature default 1.0, 400 error for `thinking_level` + `thinking_budget`, Gemini 2.5 migration points incl. the `media_resolution_high` counter-test, structured outputs combinable with built-in tools, missing image segmentation ("not supported in Gemini 3 Pro or Gemini 3 Flash").
- https://ai.google.dev/gemini-api/docs/changelog — 13 Aug 2026 GA of 3.7 Flash with introductory price until 31 Dec 2026; 8 Oct 2026 deprecation with automatic routing to `gemini-3.8-flash`; 18 Sep 2026 access restriction of the 2.5 models to existing users.
- https://ai.google.dev/gemini-api/docs/deprecations — `gemini-3.7-flash` (release 13 Aug 2026), replacement `gemini-3.8-flash`, "the endpoint is not shutting down and automatically routes API requests to `gemini-3.8-flash`".
