---
model: gemini-2.5-pro
vendor: Google
family: Gemini
aliases: [gemini-2.5-pro-preview-06-05, gemini25pro, gemini-25-pro, gemini2.5pro]
last_verified: 2026-10-13
status: legacy
successor: gemini-3.1-pro-preview
---

# Gemini 2.5 Pro

## Reasoning / Thinking
- **Type: always on (thinking model, cannot be disabled).** Gemini 2.5 Pro is a "thinking model"; thinking cannot be deactivated — the configuration table explicitly says "N/A: Cannot disable thinking". `thinkingBudget = 0` is not supported.
- **Depth control via `thinkingBudget`** (part of `generationConfig` / `thinkingConfig`): value range for 2.5 Pro **128 to 32,768 tokens**. The default is **dynamic thinking** (`thinkingBudget = -1`): the model automatically adjusts effort to the complexity of the request. The budget is a guideline, not a hard limit. Applies to `generateContent` ("Gemini 2.5 series models don't support `thinkingLevel`; use `thinkingBudget` instead"); in the Interactions API the thinking table lists gemini-2.5-pro with `thinking_level` "low, medium, high".
- **Thought summaries via `includeThoughts: true`**: delivers "thought summaries" — processed versions of the internal reasoning, structured with headings and key details (incl. notes on tool use). Accessible in the response via the `parts` that carry the boolean field `thought`. The raw thoughts are not disclosed.
- **Thought signatures**: encrypted representations of the internal thinking process. On 2.5 Pro they are returned when thinking is active and the request contains function calling with function declarations. When editing the conversation history or using the REST API, the signatures must be passed back manually to keep the thinking context across multiple turns; the Google GenAI SDK does this automatically.
- **Deep Think**: an extended reasoning mode that weighs multiple hypotheses before answering (for highly complex math/coding cases); according to the I/O 2025 announcement, available separately (trusted testers / Vertex AI; status May 2025), not the standard API mode of 2.5 Pro.

## Prompting style
- **Moderately prescriptive, instruction-faithful.** Google recommends "clear and specific instructions" as the foundation; phrase instructions as a question/task/entity operation, avoid vague requests.
- **System instructions** for role, constraints and output format; in the recommended prompt structure the system instruction comes first, then context/background, then few-shot examples, then the concrete task, and finally a clarifying instruction.
- **Few-shot examples are explicitly critical**: "always include few-shot examples … Prompts without few-shot examples are likely to be less effective." Recommended: 2–5 varied, specific examples with **identical formatting** across all examples.
- **Structure via delimiters**: XML tags (e.g. `<context>`, `<task>`) or Markdown headings to separate prompt parts; consistency matters more than the specific format choice.
- **Very large context:** input token limit **1,048,576 tokens** (≈1M). With long context, place large context blocks first and put the actual question at the end; use transitional phrasing such as "Based on the information above…".
- **Known quirk (knowledge cutoff):** since the cutoff is January 2025, Google recommends writing the current date and, where relevant, the cutoff explicitly into the system instruction for factual accuracy, and stressing strict reliance on the provided context.
- Note: the docs' warning against lowering temperature below the default explicitly refers to **Gemini 3.x**, not to 2.5 Pro; transferability to 2.5 Pro (unverified).

## Strengths & weaknesses (prompt-relevant)
- **Strengths:** "state-of-the-art thinking model" for complex reasoning in code, math and STEM, and for analysing large datasets, codebases and documents via long context. Coding and agentic tasks are core use cases. Multimodal input (text, image, audio, video, PDF).
- **Weaknesses / limits:** thinking cannot be disabled → for very simple/latency-critical tasks, thinking tokens are unavoidable (cost/latency); Flash/Flash-Lite is intended for such cases (unverified, inferred from the family positioning). No image/audio output (output is text only); knowledge cutoff January 2025 → events after that must be provided via context/grounding.

## Output & format conventions
- **Text-only output** (no image/audio output). Output token limit **65,536 tokens**.
- **Structured outputs / JSON** are supported — best demonstrate the format by example rather than only describing it; specify the desired formatting via few-shot examples or completion-style prompts.
- Name constraints explicitly: length specifications ("summarize in one sentence"), format (table, list, JSON), scope and what **not** to do.
- Supported features include: function calling, code execution, structured outputs, caching, batch API, search grounding, URL context, file search.

## Migration notes
- **Successor caveat:** the `successor` named in the frontmatter, `gemini-3.1-pro-preview`, is a **preview model** (per the deprecation table the replacement for the 2.5 Pro preview snapshots with shutdown date 2 Dec 2025); a GA ID of the form `gemini-3.1-pro` does not exist (404 on the model page). As of 2026-10-13, Gemini 2.5 Pro is therefore the only stable Pro model — the successor is the documented development path, but not a stable migration target for production. Also, according to the Gemini 3 family docs, Gemini 3 Pro does not support image segmentation (not named for 3.1 Pro; transfer unverified) — do not migrate segmentation workloads to the successor.
- **Access restricted since 18 Sep 2026:** Google limits access to the 2.5 models to users who have already actively used them ("limiting access to the 2.5 models to users who have actively used them in the past"); according to Google the models are not deprecated and continue to be served "until further notice" (no shutdown date). For new projects Google names "3.5 Flash-Lite or 3.8 Flash" — if you have not used 2.5 Pro before, you can no longer choose it as a target; then refer to this recommendation or the preview `gemini-3.1-pro-preview`.
- **AWAY FROM Gemini 2.5 Pro** (e.g. to Gemini 3.x): check model-specific prompt guidance — for Gemini 3.x Google explicitly warns against lowering temperature below the default. Thinking control can differ between generations (re-verify parameters/defaults). Check output limits and cutoff dates of the target models.
- **TO Gemini 2.5 Pro** (e.g. from a non-thinking model): expect **dynamic thinking** to be active by default and thinking not to be switchable off — plan for cost/latency from thinking tokens or set `thinkingBudget` (128–32,768). With function calling, watch **thought signatures** and return them via REST/your own history management. Add few-shot examples for format fidelity; use the large context (up to ~1M tokens), placing the question at the end. Account for the January 2025 knowledge cutoff (current date/grounding in the system instruction).

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro — model code, input limit 1,048,576, output limit 65,536, knowledge cutoff January 2025, inputs (audio/image/video/text/PDF), output text, supported features, positioning as thinking model.
- https://ai.google.dev/gemini-api/docs/generate-content/thinking — thinking not switchable off on 2.5 Pro ("N/A: Cannot disable thinking"), `thinkingBudget` 128–32,768, default dynamic (-1), "Gemini 2.5 series models don't support `thinkingLevel`", `includeThoughts`/thought summaries, thought signatures with function calling.
- https://ai.google.dev/gemini-api/docs/thinking — Interactions API: thinking table lists gemini-2.5-pro with default "On" and `thinking_level` "low, medium, high".
- https://ai.google.dev/gemini-api/docs/changelog — entry 18 Sep 2026: access to the 2.5 models restricted to existing users, not deprecated, for new projects 3.5 Flash-Lite or 3.8 Flash.
- https://ai.google.dev/gemini-api/docs/deprecations — `gemini-2.5-pro` without shutdown date; `gemini-3.1-pro-preview` as replacement for the 2.5 Pro preview snapshots (03-25 / 05-06 / 06-05).
- https://ai.google.dev/gemini-api/docs/gemini-3 — Gemini 3 family docs (deprecated per banner, still accessible as of 2026-10-13): image segmentation "not supported in Gemini 3 Pro or Gemini 3 Flash".
- https://ai.google.dev/gemini-api/docs/prompting-strategies — prompt design: clear instructions, few-shot requirement, delimiters/structure, prompt construction, long context (question at end), date/cutoff in the system instruction, Gemini 3.x temperature warning.
- https://developers.googleblog.com/en/gemini-2-5-thinking-model-updates/ — thinking budget control as a family feature, coding/agentic tasks as core use case, 06-05 stable.
- https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-updates-io-2025/ — Deep Think mode (multiple hypotheses), GA positioning of 2.5 Pro.
