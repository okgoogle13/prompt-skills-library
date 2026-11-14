---
model: muse-spark-1.2
vendor: Meta
family: Muse
aliases: [muse-spark-1.2-contributor, spark-1.2, muse-spark-1-2]
last_verified: 2026-10-13
status: legacy
successor: muse-spark-1.3
---

# Muse Spark 1.2

## Reasoning / Thinking
- Type: **always on, cannot be turned off**. `reasoning_effort: "none"` is not supported for Muse Spark and returns HTTP 400 ("Not supported by Muse Wonder or Muse Spark"); on the Messages API the same applies to `thinking: {type: "disabled"}`. Every zero-thinking path must be mapped to `minimal` or `low`.
- Parameter depends on protocol: `reasoning_effort` (Chat Completions) or `reasoning.effort` (Responses API), on the Messages API `output_config.effort` (`low`–`xhigh`). Levels for 1.2: `minimal | low | medium | high | xhigh` — **no `max`**; per the reasoning docs that is only enabled for `muse-wonder-1.0` and `muse-spark-1.3`.
- **No published default**: without the parameter "the model still reasons at a model-determined level" — which level that is appears nowhere (unverified). Set effort explicitly in the prompt contract.
- Chain of thought is private; reasoning tokens count against `max_tokens` or `max_output_tokens` and are billed at the output rate. Reasoning is preserved across turns only on Responses (`previous_response_id` or `include: ["reasoning.encrypted_content"]`) and Messages (`thinking`/`redacted_thinking` replay); Chat Completions "reasons from scratch". The protocol docs apply to all Model API models; 1.2-specific deviations are not documented (unverified).
- `logprobs` is not supported (HTTP 400) — "Muse Spark is a reasoning model".

## Prompting style
- **`developer` role instead of `system`**: Meta's build blog recommends "Prefer a `developer` message over the `system` to set tone, format, and standing rules". The blog refers to Muse Spark 1.1 and predates 1.2 — the recommendation is applied here family-wide; a 1.2-specific confirmation is missing (unverified).
- **Couple effort to the task**: "match effort to the task"; per the same blog, `reasoning_effort=xhigh` can deliver a whole artifact in one pass for cleanly scoped tasks (also 1.1 context).
- **Complex instructions are workable**: per the launch blog 1.2 follows "complex instructions more precisely than its predecessor" and uses planning, goal conditioning and context compaction for long tasks.
- **Tool descriptions carry the load**: "Write clear, specific descriptions for the tool and for each parameter. The model uses them to decide when and how to call the tool."
- **Caching via ordering**: prefix caching is automatic; "put stable content first … and put variable content last".

## Strengths & weaknesses (prompt-relevant)
- Classification: per the model overview "the previous version" of the Muse Spark line; `muse-spark-1.3` is "the latest version" and "Recommended for new work". Meta names no deprecation.
- Strengths: coding focus — "a coding-focused update to Muse Spark 1.1" with improvements in code generation, debugging, codebase understanding and end-to-end workflows; the model page promises "higher first-attempt accuracy and more reliable tool calling". Agentic long runs (kernel case study with 1,000+ tool calls over up to 24 hours).
- Strengths: "robust audio-visual understanding to enable video-heavy workflows" (multimodal blog). **Audio**: Meta explicitly points audio workloads to 1.2 ("For audio, use Muse Spark 1.2"), because audio is not fully supported in 1.3.
- Weakness: on the Model API `tool_choice` accepts only `"auto"` — `"required"`, `"none"` and named functions end in HTTP 400; phrase tool requirements in the prompt instead.
- More verbose than 1.3: per Meta, 1.3 uses "~20% fewer tool calls and ~25% fewer tokens" and is "less verbose" — 1.2 prompts therefore often contain brevity and turn-saving instructions.
- No published knowledge cutoff and no published output-token limit (unverified).

## Output & format conventions
- Context window **1,048,576 tokens**; input text, image, video, audio and PDF, output text only.
- Structured output via `response_format` (`json_schema`, Chat Completions) or `text.format` (Responses); decoding is schema-constrained. Schema limits as for 1.3: depth 10, 5,000 properties, 120,000 characters, 1,000 enum values (default, raisable per app), no recursive schemas. Function-tool arguments are only schema-guided even with `strict: true` — validate server-side.
- Tool calling: `parallel_tool_calls` defaults to `true`; tool names must match `^[a-zA-Z0-9_.-]+$` with at most one dot.
- Three protocols (Responses, Chat Completions, Messages) with the same models, same auth and same price; search grounding only on the Responses API.
- Prices per 1M tokens identical to 1.3: standard $1.25 / $0.15 (cached) / $4.25; contributor (`muse-spark-1.2-contributor`) $0.10 / $0.002 / $0.20 — contributor mode lets Meta use the content to train models.

## Migration notes
- **Status**: Meta lists 1.2 as "the previous version" and recommends 1.3 for new work; 1.2 remains available on the Model API and in Muse Code, no retirement date is given. Exception: for audio Meta still recommends 1.2 (or Muse Voice Transcribe) — do not move audio workloads to 1.3 without testing.
- **TO Muse Spark 1.3 (away from 1.2)**: remove brevity, verbosity and turn-saving instructions (1.3 is terser); effort levels carry over 1:1, add `max` only on standard-tier 1.3; keep audio paths on 1.2 or Muse Voice Transcribe; prompts with many individual steps can be trimmed, because 1.3 follows long instructions more reliably.
- **TO Muse Spark 1.2**: map `max` to `xhigh`; remove `reasoning_effort: "none"`, forced `tool_choice` values and `logprobs` (each HTTP 400); set generous reasoning token budgets; carry the system-prompt layer as a `developer` message; for 1.3 sources, add brevity instructions where needed.
- **AWAY FROM Muse Spark 1.2 to third-party models**: remove Meta-specific fields (`reasoning.summary`, `include: ["reasoning.encrypted_content"]`, `previous_response_id`), revert `developer` to `system` if the target has no developer role, and check the target's audio capabilities.

## Sources
- https://dev.meta.ai/docs/models.md — verifies `muse-spark-1.2` as "the previous version" and `muse-spark-1.3` as "the latest version"/"Recommended for new work", 1,048,576 tokens context, input modalities and text-only output, availability of `muse-spark-1.2`/`muse-spark-1.2-contributor` on the Model API and in Muse Code, and the audio note "For audio, use Muse Spark 1.2".
- https://dev.meta.ai/docs/reasoning.md — verifies the effort levels, `max` only for `muse-wonder-1.0` and `muse-spark-1.3`, HTTP 400 for `none` and `logprobs`, the "model-determined level" default, private chain of thought, token billing and reasoning preservation per protocol.
- https://dev.meta.ai/docs/protocols.md — verifies the three protocols with the same models, auth and prices, reasoning preservation on Responses and Messages (not Chat Completions), and search grounding only on Responses.
- https://dev.meta.ai/docs/protocols/messages.md — verifies `thinking`/`output_config.effort` (`low`–`xhigh`), HTTP 400 for `thinking: {type: "disabled"}` and replay of `redacted_thinking` blocks.
- https://dev.meta.ai/models/muse-spark-1-2 — official model page: "optimized for real coding workflows, with higher first-attempt accuracy and more reliable tool calling", 1M context, price table for both tiers.
- https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2 — launch blog of 5 Aug 2026: "coding-focused update to Muse Spark 1.1", more precise following of complex instructions, planning/goal conditioning/context compaction, kernel case study, availability in Muse Code and Model API.
- https://research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2 — blog of 20 Aug 2026: "robust audio-visual understanding" and video workflows; names no prompting rules and no 1.2-specific limitations.
- https://research.meta.ai/blog/introducing-muse-spark-1-3 — verifies the differences of 1.3 versus 1.2 (~20% fewer tool calls, ~25% fewer tokens, "less verbose", more reliable following of long instructions).
- https://dev.meta.ai/resources/blog/build-with-muse-spark — build blog of 8 Jul 2026 (Muse Spark 1.1): `developer`-instead-of-`system` recommendation, matching effort to the task, one-pass `xhigh` run.
- https://dev.meta.ai/docs/tool-calling.md — verifies that only `tool_choice: "auto"` is supported (otherwise HTTP 400), `parallel_tool_calls` default `true`, naming rules, the recommendation for precise tool and parameter descriptions, and the caveat that arguments are not guaranteed schema-conformant even with `strict: true`.
- https://dev.meta.ai/docs/structured-output.md — verifies `response_format`/`text.format`, schema-constrained decoding, no recursive schemas and the schema limits.
- https://dev.meta.ai/docs/prompt-caching.md — verifies automatic prefix caching and "stable content first".
- https://dev.meta.ai/docs/pricing-rate-limits — verifies the identical prices of 1.2 and 1.3 in standard and contributor mode and the training trade-off of contributor mode.
