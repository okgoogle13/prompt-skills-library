---
model: gemini-3.1-pro-preview
vendor: Google
family: Gemini
aliases: [gemini-3.1-pro, 3.1-pro, gemini-pro-3.1, gemini-3.1-pro-preview-customtools]
last_verified: 2026-10-13
status: current
---

# Gemini 3.1 Pro Preview

## Reasoning / Thinking
- Type: **always on, depth via `thinking_level`** (`low | medium | high`; default `high`, dynamic). No deactivation documented. `high` = "Maximizes reasoning depth" — noticeably longer time until the first non-thinking token, but more carefully considered output.
- `minimal` exists across the family, but in the per-model table of the thinking docs (`generate-content/thinking`) it is explicitly marked **"Not supported"** for Gemini 3.1 Pro → on Pro, **`low` is the floor** ("Minimizes latency and cost. Best for simple instruction following, chat, or high-throughput applications").
- `thinking_budget` is only still accepted for backward compatibility; Google recommends migrating to `thinking_level`. Both parameters must not be set together, and the levels are "relative allowances for thinking rather than strict token guarantees" — no token guarantee.
- **Thought signatures**: strictly validated for function calling — "The 'Current Turn' includes all Model (functionCall) and User (functionResponse) steps that occurred since the last standard User text message"; missing signatures → 400. Not enforced for plain text/chat, but recommended to preserve reasoning quality across follow-up turns.

## Prompting style
- **Terse and direct.** Gemini 3.x rewards "direct, clear instructions" rather than elaborate prompt engineering; verbose scaffolding tends to hurt.
- For large data contexts, place the actual question/instruction **at the end**, after the data block.
- Replace hand-written chain-of-thought ("think step by step") with `thinking_level: "high"` — native reasoning instead of prompt scaffolding.
- **Keep `temperature` at its default of 1.0**: "For all Gemini 3 models, we strongly recommend keeping the temperature parameter at its default value of 1.0"; values < 1.0 can trigger loops or degraded performance on complex reasoning/math tasks. No recommendation on the Pro pages for `top_p`/`top_k` (unverified).
- The default tone is direct/sober — request a conversational style explicitly if needed.
- Set `media_resolution` per content type: images → `media_resolution_high` (max. 1120 tokens), PDFs → `media_resolution_medium` (560 tokens; more rarely yields gains), video → `low`/`medium` (70 tokens/frame), `high` (280 tokens/frame) only for text-heavy video.

## Strengths & weaknesses (prompt-relevant)
- Strengths per the API model card: "optimized for software engineering behavior and usability, as well as agentic workflows requiring precise tool usage and reliable multi-step execution"; per the DeepMind card suited to "agentic performance, advanced coding, long context and/or multimodal understanding, algorithmic development". Benchmarks: ARC-AGI-2 77.1%, LiveCodeBench Pro 2887 Elo, MMMLU 92.6%.
- **Preview, not GA** (the API model page and model list place `gemini-3.1-pro-preview` under "Preview") — no stable production contract; ID/behavior may change. For a stable Google target, GA models are the safer choice.
- Knowledge cutoff: Jan 2025 (model table in the family guide).
- Not supported: Live API, image generation, audio generation. On image segmentation the family guide says: "Image segmentation capabilities (returning pixel-level masks for objects) are not supported in Gemini 3 Pro or Gemini 3 Flash" — 3.1 Pro is not named there, but according to the model card it is based on Gemini 3 Pro (transfer unverified) → do not migrate such workloads to Gemini 3.1 Pro (Gemini 2.5 is legacy here; verify the target's segmentation support beforehand).
- Long context remains error-prone: per the DeepMind card, MRCR v2 reaches 84.9% at 128k average, but only 26.3% at 1M pointwise — 1M context does not mean reliable recall at 1M.
- The DeepMind card refers detailed limitations to the Gemini 3 Pro card; none are stated inline.

## Output & format conventions
- Exact ID `gemini-3.1-pro-preview`; a GA/stable ID `gemini-3.1-pro` is not documented on ai.google.dev.
- Separate endpoint `gemini-3.1-pro-preview-customtools` (public preview, 23 Feb 2026; same prices, no provisioned throughput): "better at prioritizing your custom tools", but "quality fluctuations in some use cases which don't benefit from such tools" — choose it only for agents that mix bash and custom tools (Google FAQ: when the model ignores custom tools in favor of bash).
- Context: **1,048,576 input tokens**, **65,536 output tokens** (DeepMind card: "up to 1M" / "64K token output").
- Input: text, image, video, audio, PDF. Output: text only.
- Supported: caching, code execution, function calling, structured outputs, thinking, Batch API, search and Maps grounding. **Structured outputs can be combined with built-in tools** (Google Search, URL Context, Code Execution, function calling) — this was not possible before.
- Price is tiered by context length (paid tier, per 1M tokens): input $2.00 (≤ 200k) / $4.00 (> 200k), output $12.00 (≤ 200k) / $18.00 (> 200k), context caching $0.20 / $0.40 plus $4.50 per 1M tokens/hour storage; batch = 50% discount. The **200k threshold** is the relevant cost edge for prompt design.
- Remove `candidate_count` — per Google "unsupported in Gemini 3 and later" (https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6).

## Migration notes
- **AWAY FROM gemini-3.1-pro-preview**: re-add explicit reasoning instructions and set an explicit `temperature` (the 1.0 default assumption is Gemini-specific); map `thinking_level` onto the effort/budget control of the target; remove thought-signature and `media_resolution` plumbing; drop the assumption "structured outputs + built-in tools at the same time" if the target cannot mix JSON mode with search/code execution.
- **TO gemini-3.1-pro-preview** (especially from `gemini-2.5-pro`): (1) delete hand-built chain-of-thought scaffolding and use `thinking_level: "high"` instead (or `medium`/`low` as the cost trade-off); (2) remove explicit low-temperature settings — keep the default 1.0, otherwise loop/degradation risk; (3) replace `thinking_budget` with `thinking_level` (relative allowance, no token guarantee, never both at once); (4) retest dense document pipelines with `media_resolution_high` (images) / `media_resolution_medium` (PDFs); (5) pass thought signatures back through **every** function-calling turn — return all signatures accumulated since the last user text message, otherwise 400; (6) token consumption changes (PDFs more expensive, video cheaper) → re-baseline costs against the 200k price tier; (7) do **not** migrate image segmentation workloads; (8) factor the preview status into the target choice.

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview — exact ID, preview versions `gemini-3.1-pro-preview` and `gemini-3.1-pro-preview-customtools` (incl. "better at prioritizing your custom tools" / "quality fluctuations"), preview status, 1,048,576 / 65,536 tokens, modalities, feature matrix (incl. unsupported: Live API / image / audio), optimization quote on software engineering and agentic workflows.
- https://ai.google.dev/gemini-api/docs/generate-content/gemini-3 — `thinking_level` values and `high` default, thought signature validation ("Current Turn"), temperature 1.0 recommendation, `media_resolution` per modality with token counts, structured outputs with built-in tools, prompting rules (brevity, instruction at the end), 2.5→3 migration checklist.
- https://ai.google.dev/gemini-api/docs/gemini-3 — default `high` (dynamic) for Gemini 3.1 Pro, `thinking_budget` backward compatibility and prohibition on combining, temperature warning, knowledge cutoff Jan 2025, "image segmentation … not supported".
- https://ai.google.dev/gemini-api/docs/generate-content/thinking — per-model table: for Gemini 3.1 Pro `minimal` is "Not supported"; `low`/`medium`/`high` supported, default `high` (dynamic); thinking not switchable off on 3.1 Pro.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6 — migration checklist: `candidate_count` "unsupported in Gemini 3 and later".
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-pro — Vertex model page: `gemini-3.1-pro-preview` (public preview, 19 Feb 2026) and `gemini-3.1-pro-preview-customtools` (public preview, 23 Feb 2026, no provisioned throughput), purpose of the custom-tools endpoint.
- https://deepmind.google/models/model-cards/gemini-3-1-pro/ — official model card (19 February 2026): 1M input / 64K output, intended uses, ARC-AGI-2 77.1%, LiveCodeBench Pro 2887 Elo, MMMLU 92.6%, MRCR v2 84.9% (128k) / 26.3% (1M pointwise), "based on Gemini 3 Pro", reference to the Gemini 3 Pro card for limitations.
- https://ai.google.dev/gemini-api/docs/pricing — context-length-tiered prices with 200k threshold, caching rates incl. storage, 50% batch discount; `gemini-3.1-pro-preview-customtools` priced the same.
- https://ai.google.dev/gemini-api/docs/models — official model list; `gemini-3.1-pro-preview` is among the preview models; no GA Pro ID of the 3.x series listed.
