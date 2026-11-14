---
model: llama-4-maverick
vendor: Meta
family: Llama
aliases: [llama4-maverick, llama-4-maverick-17b, llama-4-maverick-17b-128e-instruct, llama4:maverick]
last_verified: 2026-10-13
status: current
---

# Llama 4 Maverick

## Reasoning / Thinking
- Type: **none** (not a dedicated reasoning/thinking model). The official docs and model card describe Maverick as an instruction-tuned, natively multimodal model without an extended-thinking or dedicated chain-of-thought mode. No thinking tokens or separate reasoning channel are documented.
- MoE architecture: **mixture-of-experts** with **17B active parameters**, **128 experts** and **400B total parameters**. Only ~17B active parameters are computed per token, which reduces inference/training latency. Context window: **1M tokens**.
- Prompting step-by-step reasoning: since there is no native reasoning mode, chain-of-thought must be forced classically via the prompt (e.g. "Think step by step", explicitly requesting intermediate steps/justifications). Exact best-practice phrasings are (unverified) — the primary sources document no specific CoT trigger phrase.

## Prompting style
- Prescriptiveness: medium. Maverick is designed to be **"steerable" (easy to steer)** — per the model card, responses can be easily adapted to specific developer goals. An effective system prompt reduces false refusals and templated language.
- Official prompt format / chat template (header tokens):
  - `<|begin_of_text|>` — start of the prompt.
  - `<|header_start|>` … `<|header_end|>` — enclose the role of a message.
  - `<|eot|>` — End of Turn; signals that the model has finished the turn.
  - `<|end_of_text|>` — ends generation ("Model will cease to generate more tokens"); per the docs it is only produced by the base (pretrained) models — instruct turns end with `<|eot|>`.
  - Supported roles: `system`, `user`, `assistant`, `tool` (called `ipython` in the prompt).
  - Example turn structure (verbatim from the docs):
    ```
    <|begin_of_text|><|header_start|>system<|header_end|>
    [system content]<|eot|><|header_start|>user<|header_end|>
    [user content]<|eot|><|header_start|>assistant<|header_end|>
    ```
- System prompt style: the recommended system prompt begins verbatim with "You are an expert conversationalist who responds to the best of your ability…" and ends with "You are Llama 4. Your knowledge cutoff date is August 2024. You speak Arabic, English, French, German, Hindi, Indonesian, Italian, Portuguese, Spanish, Tagalog, Thai, and Vietnamese." Recommendation: adapt this base prompt for your own use cases.
- Instruction following / quirks: the system prompt explicitly advises against using "templated language" or phrases with moral authority ("it's important to", "it's crucial to"); the model should not refuse political prompts. This steering demonstrably serves to reduce false refusals.

## Strengths & weaknesses (prompt-relevant)
- Strengths:
  - Natively multimodal (text + image as input, text-only output); per Meta, the best multimodal model in its class.
  - Strong benchmark values per the model card: MMLU Pro 80.5 (Instruct); MATH 61.2 and MBPP (code) 77.6 (pretrained table) — good for coding, mathematics and knowledge tasks.
  - Efficient MoE design (only 17B active) → lower latency with large total capacity; very large 1M-token context window.
- Weaknesses:
  - Multilingual performance with gaps (e.g. TydiQA 31.7 vs. Llama 3.1 405B 34.3).
  - Image understanding only in English; only tested with up to **5 images** per input — beyond that, risk mitigation falls to the developer.
  - No native reasoning mode → complex multi-step logic must be structured via the prompt.

## Output & format conventions
- Text-only output (no image output). Input may combine text + image.
- Image input: up to 5 images; dynamic tiling in 336×336-pixel tiles with separator tokens `<|tile_x_separator|>` and `<|tile_y_separator|>`.
- Tool/function calling formats (two variants):
  - Python-style: `[get_weather(city="San Francisco"), get_weather(city="Seattle")]`
  - JSON-style: `[{"name": "get_weather", "parameters": {"city": "San Francisco"}}]`
  - Tool outputs are returned via the `ipython` role.
  - Function definitions belong in the **system message**.
  - Hard rule (verbatim): **"NEVER combine text and function calls in the same response"** — i.e. either running text or a function call, never both in one response.
- Multilingual (text): Arabic, English, French, German, Hindi, Indonesian, Italian, Portuguese, Spanish, Tagalog, Thai, Vietnamese.
- Knowledge cutoff: August 2024.

## Migration notes
- Typical changes when migrating AWAY FROM this model:
  - When moving to a reasoning model, manually forced CoT instructions may become unnecessary; prompts may need to be trimmed.
  - The header-token format (`<|header_start|>`/`<|eot|>`) is Llama 4-specific and must be switched to the chat template of the target family.
  - The strict rule "no text + function call mixed" may not apply on the target model — check the tool-handling logic.
- Typical changes when migrating TO this model:
  - Switch from the Llama 3 format to the Llama 4 format (`<|header_start|>`/`<|header_end|>`/`<|eot|>`) — the token names differ (the Llama 3 token names are not verified in the primary sources (unverified)).
  - Adopt/adapt the recommended "expert conversationalist" system prompt to reduce false refusals and filler phrases.
  - Move function definitions into the system message; ensure tool calls are never mixed with running text in the same response.
  - Structure multimodal inputs via `apply_chat_template` or `AutoProcessor`; watch the 5-image limit and English-only image understanding.

## Sources
- https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama4 — official prompt format: header tokens, roles incl. `ipython`, turn structure, function-calling formats and the rule "NEVER combine text and function calls", recommended system prompt, tiling separator tokens, languages, no reasoning mode.
- https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct — official Meta model card: MoE architecture (17B active / 400B total / 128 experts), 1M-token context, knowledge cutoff August 2024, steerability/system prompt, benchmark strengths and multilingual weaknesses, multimodal image input (up to 5 images), `apply_chat_template`/`AutoProcessor`.
- https://ai.meta.com/blog/llama-4-multimodal-intelligence/ — Meta announcement "The Llama 4 herd": positioning of Maverick, MoE size figures, model family (Scout/Maverick).
