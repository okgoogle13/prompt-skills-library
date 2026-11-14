---
model: gemini-2.5-flash
vendor: Google
family: Gemini
aliases: [gemini25flash, gemini-25-flash, gemini2.5flash]
last_verified: 2026-10-13
status: legacy
successor: gemini-3.8-flash
---

# Gemini 2.5 Flash

## Reasoning / Thinking
- Type: **adaptive / can be switched off**. Gemini 2.5 Flash is the first Flash model with thinking capability; by default "Dynamic Thinking" runs (the model itself decides the depth of thinking based on perceived task complexity).
- Control on the `generateContent` API via the parameter `thinkingBudget` (tokens). Valid range for 2.5 Flash: **0 to 24576**. There: "Gemini 2.5 series models don't support `thinkingLevel`; use `thinkingBudget` instead". In the Interactions API, by contrast, the thinking table lists `gemini-2.5-flash` with `thinking_level` `low, medium, high` (default: "On").
  - `thinkingBudget = 0` → **thinking fully disabled** (no thought content).
  - `thinkingBudget = -1` → **Dynamic Thinking** (the model adjusts the budget to complexity itself).
  - Positive integer → fixed budget; higher values allow deeper reasoning for complex tasks.
  - Default (parameter not set) → Dynamic Thinking.
- Difference from **Gemini 2.5 Pro**: the Pro range is **128 to 32768**, and thinking **cannot be disabled** on Pro; 2.5 Flash can run entirely without thinking via budget 0. Pro is meant for maximum intelligence/complex reasoning, Flash for price-performance in low-latency/high-volume tasks.
- Billing: thinking tokens are counted — "response pricing is the sum of output tokens and thinking tokens". Thought summaries are available on both the free and paid tier.

## Prompting style
- Moderately prescriptive, but structure- and context-sensitive: Google recommends **clear, specific instructions** with a defined input type, constraints (length/scope limits), response format and necessary context directly in the prompt.
- **System instructions** serve for role/persona, output format, tone and constraints; XML tags such as `<role>`, `<constraints>`, `<task>` are recommended as structuring aids.
- **Few-shot examples**: "We recommend to always include few-shot examples in your prompts." Examples should be specific, varied and consistently formatted; overloading with examples reduces the effect (overfitting risk).
- Split complex tasks via separate instructions, chaining (output → next step) or aggregation (parallel partial operations).
- **Cost/latency focus**: for simple tasks (fact retrieval, classification) thinking is not needed — `thinkingBudget = 0` keeps cost and latency minimal. If you want long outputs, limit the depth of thinking via the prompt to reserve more tokens for the answer.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**: best price-performance ratio for low-latency, high-volume and agentic tasks with reasoning; 1,048,576-token context window (long context: put the entire context first, the question at the end); structured output and function calling supported; thinking can optionally be enabled.
- **Weaknesses / prompt-relevant quirks**: for maximum intelligence/complex reasoning, 2.5 Pro is superior. With thinking active, cost and latency rise (thinking tokens count). Reports of `max_output_tokens` not being respected or token repetition in structured output exist in community forums — (unverified; no primary source).

## Output & format conventions
- Supported inputs: **text, images, video, audio** (context window 1,048,576 tokens). Output: **text** (max. **65,536** output tokens).
- Format control: natural-language format instructions, completion strategy (pre-supply partial output), **structured output** (JSON schema) and delimiters via XML tags/Markdown headers. Function calling is supported.
- Knowledge cutoff: **January 2025**.

## Migration notes
- **Status caveat**: since 18 Sep 2026, 2.5 models (incl. 2.5 Flash-Lite) are only accessible to existing users who had used them before; they are **not** deprecated, and no shutdown date has been announced. For new projects Google names "3.5 Flash-Lite or 3.8 Flash".
- **Successor caveat (`gemini-3.8-flash`)**: no zero-thinking path — `thinkingBudget = 0` has no equivalent there; the floor is `thinking_level: low` (`minimal` throws an error); image segmentation (pixel masks) is, according to Google, not supported in Gemini 3.x — do not migrate segmentation workloads to the successor (Google still recommends 2.5 Flash with thinking switched off for these); `temperature`/`top_p`/`top_k` must be removed there.
- **AWAY FROM 2.5 Flash** (e.g. to 2.5 Pro or Gemini 3.x): on 2.5 Pro thinking **can no longer be switched off** (minimum budget 128, range up to 32768); sensible for complex reasoning/coding/agentic work, but higher cost/latency. Recheck output limit and behavior. For Gemini 3.x, Google recommends replacing CoT prompt engineering with `thinking_level` and simplified prompts, and removing any explicitly set low temperature.
- **TO 2.5 Flash**: switch from older previews to the stable alias `gemini-2.5-flash` — only possible if the project is an existing user. When migrating from 2.0 Flash: thinking is new; for the same cost/latency as 2.0, consider setting `thinkingBudget = 0`. For pure cost reduction, 2.5 Flash-Lite is likewise only accessible to existing users; for new projects Google names "3.5 Flash-Lite or 3.8 Flash", and explicitly names `gemini-3.5-flash-lite` as the "Strong migration path from Gemini 2.5 Flash".

## Sources
- https://ai.google.dev/gemini-api/docs/generate-content/thinking — `thinkingBudget` table: 2.5 Flash 0–24576, 0 disables thinking, -1 = Dynamic Thinking, default Dynamic; 2.5 Pro 128–32768 and not switchable off; "Gemini 2.5 series models don't support `thinkingLevel`; use `thinkingBudget` instead"; thinking tokens in billing; thought summaries on free and paid tier.
- https://ai.google.dev/gemini-api/docs/thinking — Interactions API thinking table: `gemini-2.5-flash` "On", `thinking_level` `low, medium, high`; `gemini-3.8-flash` without `minimal`.
- https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash — model ID, context window 1,048,576, output limit 65,536, inputs text/image/video/audio, knowledge cutoff January 2025, structured output and function calling supported; note on the access restriction to existing users ("not deprecated", "For any new projects, use our latest models: 3.5 Flash-Lite or 3.8 Flash").
- https://ai.google.dev/gemini-api/docs/changelog — 18 Sep 2026: access to the 2.5 models restricted to users who used them previously; not deprecated.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6 — 3.5 Flash-Lite as "Strong migration path from Gemini 2.5 Flash"; sampling parameters from 3.6 Flash onward "deprecated and ignored".
- https://ai.google.dev/gemini-api/docs/gemini-3 — Gemini 3 migration from 2.5: replace CoT with `thinking_level`, remove explicit temperature, image segmentation "not supported in Gemini 3 Pro or Gemini 3 Flash" with the recommendation to use 2.5 Flash with thinking off instead.
- https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 — "Image segmentation is not supported in Gemini 3.x. For segmentation workloads, continue using Gemini 2.5 Flash with thinking off."
- https://ai.google.dev/gemini-api/docs/prompting-strategies — prompting style: clear/specific instructions, system instructions with XML tags, few-shot recommendation, task decomposition, output format control, long-context ordering.
- https://developers.googleblog.com/en/start-building-with-gemini-25-flash/ — budget 0 for lowest cost/latency vs. 2.0 Flash; simple tasks without thinking; long outputs by limiting thinking depth.
- https://developers.googleblog.com/en/gemini-2-5-thinking-model-updates/ — GA status, new pricing structure (uniform rate), migration path to `gemini-2.5-flash`/Flash-Lite, Pro for maximum intelligence.
