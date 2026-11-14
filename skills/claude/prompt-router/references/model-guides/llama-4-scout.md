---
model: llama-4-scout
vendor: Meta
family: Llama
aliases: [llama4-scout, llama-4-scout-17b-16e, llama-4-scout-17b-16e-instruct, meta-llama-4-scout]
last_verified: 2026-10-13
status: current
---

# Llama 4 Scout

## Reasoning / Thinking
- **Type: none (not a dedicated reasoning/thinking model).** The official model cards and prompt formats list no extended/adaptive thinking mode and no thinking tokens; Llama 4 Scout is a natively multimodal, instruction-tuned standard model without a separate thinking mode.
- **Architecture: mixture-of-experts (MoE).** 17B active parameters, 109B total parameters, 16 experts. Only 17B parameters are active per token. Uses an `iRoPE` architecture and scaled softmax (inference-time temperature scaling) for length generalisation.
- **Very long context:** per the model card and prompt-format page up to 10M tokens of context; per the Meta blog Scout is "both pre-trained and post-trained with a 256K context length". This range suits multi-document analysis, very large codebases and long histories.
- **Prompting step-by-step reasoning:** since there is no native thinking mode, chain-of-thought is achieved via classic prompting — i.e. instruct it explicitly in the system or user prompt (e.g. "Think through the problem step by step before answering"). Per the model card (instruct table) Scout reaches, among others, 74.3 MMLU Pro and 57.2 GPQA Diamond.

## Prompting style
- **Prescriptiveness: medium to high via the system prompt.** Meta explicitly recommends a well-designed system prompt to reduce "false refusals" and "preachy" tone.
- **Official prompt format / chat template** with special tokens:
  - `<|begin_of_text|>` — marks the start of the prompt.
  - `<|header_start|>{role}<|header_end|>` — encloses the role (`system`, `user`, `assistant`, `ipython` for tool responses).
  - `<|eot|>` — end of turn, signals the end of a message/response.
  - `<|end_of_text|>` — ends generation ("Model will cease to generate more tokens"); per the docs it is only produced by the base (pretrained) models — instruct turns end with `<|eot|>`.
  - Example structure: `<|begin_of_text|><|header_start|>system<|header_end|>{system_prompt}<|eot|><|header_start|>user<|header_end|>{prompt}<|eot|><|header_start|>assistant<|header_end|>`
- **Official system prompt template (excerpt):** "You are an expert conversationalist who responds to the best of your ability…" The template advises avoiding phrases of moral superiority (e.g. "it's important to", "it's crucial to"), not lecturing, and not refusing prompts on political/social topics.
- **Instruction following:** instruction-tuned via lightweight SFT → online RL → lightweight DPO. Good steerability of tone and format via the system prompt.
- **Known quirks:** without a good system prompt the model tends toward standardised/lecturing language. Image understanding is validated only for English, although the model is multilingual.
- **Differences from Maverick:** both share 17B active parameters and the same prompt format. Scout = 16 experts / 109B total / up to 10M context / runs on a single GPU (INT4-quantised on 1× H100); Maverick = 128 experts / 400B total / 1M context / higher reasoning performance, needs multiple GPUs. The Llama 4 prompt-format page documents one shared format for the Llama 4 models without distinguishing Scout and Maverick; Maverick tends to deliver stronger reasoning results, Scout scores with longer context and resource efficiency.

## Strengths & weaknesses (prompt-relevant)
- **Strengths:**
  - Extremely long context (up to 10M tokens, instruct) — prompts can contain very large inputs.
  - Native multimodality (early fusion): text + up to 5 images tested as input. "Best-in-class" for image grounding / visual localisation.
  - Strongly multilingual (pre-training on 200 languages, more than 100 of them with over 1B tokens each).
  - Efficient: runs on a single server GPU.
- **Weaknesses / limitations:**
  - Output is **text only** (no image/audio output).
  - Image understanding officially validated for **English** only.
  - No native reasoning mode — complex multi-step tasks require explicit CoT prompting; below Maverick on pure reasoning benchmarks.
  - Knowledge cutoff **August 2024**.
  - Without system-prompt tuning, risk of lecturing tone / unnecessary refusals.

## Output & format conventions
- **Output modality:** text only. Responses end with `<|eot|>`.
- **Function/tool calling:** two official formats: Python/list format (`[get_weather(city="San Francisco")]`) and JSON format. Tool results are returned via the `ipython` role.
- **Image input conventions:** images are split into 336×336-pixel tiles; large images use tile separator tokens (`<|tile_x_separator|>`, `<|tile_y_separator|>`), small images under 336×336 need no separators.
- **Structured outputs** (JSON, Markdown, tables) are controlled via the system/user prompt (no documented schema mode; reliability not verified); Meta does not specify recommended sampling parameters (e.g. temperature) in the model card (no concrete temperature values verified). Code examples use `bfloat16` and `attn_implementation="flex_attention"`.

## Migration notes
- **Typical changes when migrating AWAY FROM Llama 4 Scout:**
  - To Maverick: same prompt format and same active parameter count — no template rework needed; however, note the context limit drops from 10M to 1M and plan for hardware requirements. Reasoning-heavy prompts benefit.
  - To a dedicated reasoning model: remove or adapt explicit CoT instructions from the prompt; the prompt format/special tokens differ entirely.
  - For >1M-token workflows check the target's context window; otherwise chunk/retrieve.
- **Typical changes when migrating TO Llama 4 Scout:**
  - From Llama 3: switch the prompt format to the Llama 4 tokens (`<|header_start|>`/`<|header_end|>`/`<|eot|>`); context rises to up to 10M (Llama 3 context length not verified here).
  - Design the system prompt per Meta's template to avoid lecturing tone / false refusals.
  - Multimodal inputs (up to 5 images) are possible; phrase image prompts in English where possible.
  - For multi-step reasoning add explicit step-by-step instructions (no auto-thinking).
  - Account for the August 2024 knowledge cutoff; feed current facts via tool/RAG context.

## Sources
- https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama4 — official prompt format, special tokens, roles incl. `ipython`, system-prompt template, function-calling formats, image tiling/separator tokens, knowledge cutoff August 2024, no reasoning mode.
- https://ai.meta.com/blog/llama-4-multimodal-intelligence/ — MoE architecture (17B active, 16 experts, 109B total for Scout), 10M-token context, pre- and post-training with 256K context length, iRoPE, early-fusion multimodality, multilingual support, image count, image grounding, training methodology, single-GPU capability.
- https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct — official model card: no reasoning mode, system-prompt recommendation, 10M context, MoE figures, supported languages, up to 5 images, knowledge cutoff August 2024, benchmark values (Instruct: 74.3 MMLU Pro / 57.2 GPQA Diamond), code notes (`flex_attention`, `bfloat16`).
