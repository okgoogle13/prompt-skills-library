---
model: gemma-3
vendor: Google
family: Gemma
aliases: [gemma3, gemma-3-27b, gemma-3-27b-it, gemma-3-12b-it, gemma-3-4b-it, gemma-3-1b-it, gemma3-27b, gemma_3]
last_verified: 2026-10-13
status: legacy
successor: gemma-4
---

# Gemma 3

## Reasoning / Thinking
- Type: **none** (no dedicated "thinking" or reasoning mode). Gemma 3 is an open-weight model (freely available weights, pre-trained and instruction-tuned) and has no built-in chain-of-thought or thinking switch like newer "thinking" models.
- Step-by-step reasoning has to be triggered classically through prompting: explicit instructions such as "Think step by step" or "Justify your answer before the result", or few-shot examples. The official prompt-formatting documentation mentions **neither** chain-of-thought **nor** zero-/few-shot techniques explicitly (unverified whether a specific CoT format is recommended).
- Available sizes: 270M (since 2025-08-14), 1B, 4B, 12B, 27B. The reference variant here is **gemma-3-27b-it** (largest instruction-tuned model); the prompt and turn format is identical across all sizes.

## Prompting style
- **Moderately prescriptive, but format-bound.** The instruction-tuned model is fine-tuned to a fixed turn format; the control tokens are "reserved in and specific to our tokenizer" and must be used exactly.
- Official chat/prompt format (turn tokens):
  - `<start_of_turn>` opens a turn, `<end_of_turn>` ends it.
  - Role markers directly after `<start_of_turn>`: `user` or `model`.
  - Structure:
    ```
    <start_of_turn>user
    [Content]<end_of_turn>
    <start_of_turn>model
    ```
  - The last turn ends with `<start_of_turn>model` **without** a closing tag, so that the model generates.
- **System prompt handling:** There is **no** dedicated `system` role or system turn — "the `system` role or a system turn is not supported." System or persona instructions are instead placed **at the start of the first user message** (official example: "Only reply like a pirate. What is the answer to life the universe and everything?"). Some HuggingFace chat templates technically accept a `system` field, but it is inserted into the first user message internally; the Google documentation remains authoritative.
- **Instruction following:** good enough that system-level instructions placed directly in the user prompt are reliably interpreted — a separate system role is therefore not necessary.
- **Known quirk (BOS token):** The tokenizer pipeline typically adds a `<bos>` token at the start of the sequence; however, the official formatting page does **not** explicitly show `<bos>` in its examples. With raw inference (without `apply_chat_template`), take care not to insert the BOS token twice (unverified in detail).

## Strengths & weaknesses (prompt-relevant)
- **Strengths:**
  - Multimodal: processes text **and** images as input and produces text as output (images are normalised to 896×896 and encoded at 256 tokens each) — applies to 4B/12B/27B.
  - Multilingual: support for over 140 languages → prompts need not necessarily be in English.
  - Long context: 128K tokens (4B/12B/27B), 32K tokens for 1B and 270M; output shares this limit with input.
  - Strong performance on multilingual, STEM and multimodal benchmarks.
- **Weaknesses:**
  - Can poorly capture subtle nuance, sarcasm or figurative language → make this explicit in the prompt for such cases.
  - Can produce factually incorrect or outdated statements (hallucinations) → verify critical facts externally, or require source grounding in the prompt.
  - No built-in reasoning → specify CoT or few-shot manually for complex tasks.
  - Training data cutoff per model card **August 2024** → include time-critical facts in the prompt.

## Output & format conventions
- Plain text output; the model closes its turn with `<end_of_turn>`.
- Structured output (JSON, tables, Markdown) is reliably achievable via explicit format instructions in the user prompt (general instruction following; a specific JSON-schema or structured-output feature is not documented in the primary sources — unverified).
- Sampling and generation parameters: the official documentation gives no numeric sampling values (unverified); the Gemma 3 model card contains no recommendation for temperature, top_k or top_p.

## Migration notes
- **Lifecycle:** Google lists Gemma 3 under "Previous Gemma models" on the Gemma overview; the Gemma 3 prompt documentation is labelled "Legacy" in the navigation; Gemma 4 is the current generation. The release page announces no deprecation or end of support for Gemma 3 — as a target, Gemma 3 remains usable, but is no longer the current generation.
- **Typical changes when migrating AWAY from Gemma 3:**
  - To models with a dedicated `system` field (e.g. OpenAI/Anthropic): move the system instructions embedded in the first user message back into a real system prompt field.
  - Remove Gemma-specific control tokens (`<start_of_turn>`, `<end_of_turn>`) — per Google they are "reserved in and specific to our tokenizer"; other models use their own templates.
  - Do not carry over sampling values: the Gemma values are Gemma-specific; whether and which sampling parameters the target accepts is determined by the target guide.
- **Typical changes when migrating TO Gemma 3:**
  - Resolve separate `system` messages and move them to the **start of the first user message** (no system role available).
  - Switch to the exact turn-token format, or use the `apply_chat_template()` function of the Transformers library instead of setting tokens manually (this avoids, among other things, a doubled `<bos>`).
  - Do not expect a thinking mode — add explicit CoT or few-shot prompting for reasoning tasks.
  - Sampling: official numeric values not published (unverified) — do not enforce any values.
  - Image input is possible (4B/12B/27B), but 1B is text-only; for 270M the model card shows no image input (unverified).

## Sources
- https://ai.google.dev/gemma/docs/core/prompt-structure — official turn-token structure (`<start_of_turn>`/`<end_of_turn>`, `user`/`model`), missing `system` role, embedding of the system instruction in the first user message, tokenizer-specific control tokens.
- https://huggingface.co/google/gemma-3-27b-it — model card: sizes 1B/4B/12B/27B, 128K context, multimodal (896×896 / 256 tokens), 140+ languages, no documented thinking mode, weaknesses (sarcasm/figurative language, factual errors), bfloat16/`device_map="auto"`.
- https://ai.google.dev/gemma/docs/core/model_card_3 — official model card: context 128K (4B/12B/27B) or 32K (1B/270M), output within the same limit, sizes incl. 270M, 896×896 images at 256 tokens each, 140+ languages, training data cutoff August 2024, no numeric sampling values.
- https://ai.google.dev/gemma/docs/releases — release dates (Gemma 3 1B/4B/12B/27B on 2025-03-10, 270M on 2025-08-14, Gemma 4 from 2026-03-31); no deprecation or end-of-support announcement for Gemma 3.
- https://ai.google.dev/gemma/docs/core — Gemma overview (Gemma 4): Gemma 3 under "Previous Gemma models", navigation "Legacy Prompt and system instructions [Gemma 1, 2, and 3]".
