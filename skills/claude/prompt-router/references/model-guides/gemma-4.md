---
model: gemma-4
vendor: Google
family: Gemma
aliases: [gemma, gemma4, gemma-4-12b, gemma-4-12b-it, gemma-4-31b, gemma-4-31b-it, gemma-4-26b-a4b, gemma-4-26b-a4b-it, gemma-4-e4b, gemma-4-e4b-it, gemma-4-e2b, gemma-4-e2b-it, gemma_4]
last_verified: 2026-10-13
status: current
---

# Gemma 4

## Reasoning / Thinking
- Type: **switchable (on/off), for open weights via the prompt rather than an API parameter** (exception: the hosted Gemini API, see below). Google describes the family as "highly capable reasoners, with configurable thinking modes"; the model card names a "Built-in reasoning mode that lets the model think step-by-step before answering".
- Switched via the control token `<|think|>` **in the system turn**: `<|turn>system\n<|think|><turn|>` = thinking on; omit the token = off. Via Transformers the equivalent is `processor.apply_chat_template(…, enable_thinking=True)`.
- The thoughts come back as a separate channel (`<|channel>thought … <channel|>`). Per the docs, `skip_special_tokens=False` is mandatory for reading them out; `parse_response` splits the result into `thinking` and `answer`.
- On 12B, 26B A4B and 31B the chat template carries an **empty thinking token** in the OFF case (`<|turn>model\n<|channel>thought\n<channel|>`) — it stabilises the output by suppressing unwanted thought channels. Hand-built prompt strings without this detail deviate from the trained format.
- **Multi-turn rule:** the thoughts of the previous turn must be stripped from the history before the next request. Exception: within a model turn containing function calls, the thoughts must **not** be removed between the calls. Switching thinking off mid-conversation = remove `<|think|>` when stripping.
- No depth control (budget, effort levels): per the Gemini API docs, Gemma 4 supports only on/off "strictly". In the hosted Gemini API this is switched via `thinking_level` — `"high"` = on, `"minimal"` = off; the docs name no further levels.

## Prompting style
- **Most important change compared with Gemma 3: a real system role.** "Gemma 4 introduces built-in support for the system role." System instructions belong again in their own `<|turn>system` turn rather than at the start of the first user message.
- The turn format is also new: brackets `<|turn>` / `<turn|>`, roles `system` / `user` / `model`. The Gemma 3 tokens `<start_of_turn>` / `<end_of_turn>` do not apply here. In practice, always use `apply_chat_template()` instead of setting tokens by hand.
- Multimodal: placeholders `<|image|>` and `<|audio|>` mark the insertion points; the embeddings sit between `<|image>`/`<image|>` or `<|audio>`/`<audio|>`. The model card recommends placing **image content before the text**.
- Tools are declared, not explained in prose: `<|tool>declaration:function_name{description:…,parameters:{…}}<tool|>`; the model replies with `<|tool_call>call:…<tool_call|>`, and the result goes back as `<|tool_response>response:…<tool_response|>`. For function calling the docs explicitly recommend active thinking ("By utilizing an internal reasoning process, the model significantly enhances its function-calling accuracy").
- Manual CoT scaffolding ("Think step by step", few-shot reasoning examples) has become superfluous — choreography carried over from the Gemma 3 days can be deleted and replaced by the thinking switch.

## Strengths & weaknesses (prompt-relevant)
- DeepMind's positioning: "Our most intelligent open models, built from Gemini 3 research and technology to maximize intelligence-per-parameter". Apache 2.0; weights available via Google AI Studio, Hugging Face, Kaggle, Ollama, Vertex AI and Cloud Run, as well as vLLM, llama.cpp, MLX, LM Studio and Unsloth.
- Five variants with clearly different profiles: E2B (2.3 B effective) and E4B (4.5 B effective) for edge, mobile and browser; 12B Unified (11.95 B, encoder-free, multimodal); 26B A4B as MoE (25.2 B total / 3.8 B active, "designed for high-throughput, advanced reasoning"); 31B dense (30.7 B). The prompt contract is identical across all sizes; only the empty thinking token distinguishes the large models from E2B/E4B.
- Benchmarks per DeepMind (31B IT Thinking): Arena AI Text 1452 Elo, MMLU Multilingual 85.2%, MMMU Pro 76.9%, AIME 2026 89.2%, LiveCodeBench 80.0%, GPQA Diamond 84.3%, τ2-bench 86.4%. Google places 31B as #3 and 26B as #6 of open models on the Arena AI text leaderboard.
- Languages: "out-of-the-box support for 35+ languages, pre-trained on 140+ languages" — prompts need not be in English, but beyond the 35 supported languages quality is not guaranteed.
- Weaknesses per the model card: can produce factually incorrect or outdated statements; "might struggle to grasp subtle nuances, sarcasm, or figurative language" → make this explicit in the prompt rather than assuming it implicitly. Per the function-calling docs: "A Gemma model cannot execute code on its own" — the application must validate and execute tool calls.
- Training data cutoff per model card **January 2025** — for time-critical facts, supply context rather than relying on model knowledge.

## Output & format conventions
- Context window: 128K for E2B/E4B, 256K for 12B Unified, 26B A4B and 31B. Maximum output length: not published (unverified).
- Input text and image for all variants (variable resolution and aspect ratio); audio natively for E2B, E4B and 12B; the model overview additionally names video. Output is plain text only.
- Structured output: Google lists "structured JSON output" as a built-in capability. There is no server-side schema enforcement for open weights — format fidelity comes from the prompt or the serving stack (unverified whether an official schema mode is documented).
- Recommended sampling configuration per the model card, explicitly "across all use cases": `temperature=1.0`, `top_p=0.95`, `top_k=64`.
- **IDs are variant-specific** — an artifact with the bare id `gemma-4` does not exist; `gemma-4` here is only the family entry. Official repos: `google/gemma-4-E2B-it`, `google/gemma-4-E4B-it`, `google/gemma-4-12B-it`, `google/gemma-4-26B-A4B-it`, `google/gemma-4-31B-it`.
- Gemini API (hosted; per the pricing page free tier only, paid tier "Not available"): `gemma-4-31b-it`, `gemma-4-26b-a4b-it`. There the system instruction goes via the field `system_instruction` / `systemInstruction`, and thinking via `thinking_level`.
- In addition, MTP variants (Multi-Token Prediction) for E2B, E4B, 31B and 26B A4B have existed since 2026-04-16; a prompt contract deviating from the standard one is not documented (unverified).

## Migration notes
- **FROM Gemma 4**: remove all Gemma 4 tokenizer tokens (`<|turn>`/`<turn|>`, `<|think|>`, `<|channel>`, `<|image|>`/`<|audio|>`, the tool tokens); translate tool declarations from the token syntax into the target provider's JSON-schema format; the `enable_thinking`, `parse_response` and thought-stripping logic falls away; for target models without thinking, add explicit CoT or few-shot prompting back in; do not carry over Gemma sampling (temperature 1.0 / top_p 0.95 / top_k 64) — whether and which sampling parameters the target allows is determined solely by the target guide (some targets reject non-default values or require their removal); for target models without a system role, including Gemma 3, move the system instructions back to the start of the first user message.
- **TO Gemma 4**: coming from Gemma 3, replace the entire turn format (`<start_of_turn>`/`<end_of_turn>` → `<|turn>`/`<turn|>`), most safely via `apply_chat_template()` rather than by hand; lift embedded system instructions into a real `system` turn; replace manual "Step by step" CoT with `<|think|>` or `enable_thinking=True`; in multi-turn operation implement thought stripping (exception: tool sequences within a turn); set `skip_special_tokens=False` when decoding, otherwise the reasoning parser does not work; for 12B/26B/31B write the empty thinking token in the OFF case. Coming from API models: there is no effort or budget control, only on/off (Gemini API: `thinking_level` `high`/`minimal`) — cost control runs through variant choice and the thinking switch. Put image content before the text. Context grows from 128K to 256K compared with Gemma 3 (12B/26B/31B); for E2B/E4B it remains 128K.

## Sources
- https://ai.google.dev/gemma/docs/core — model overview: five architectures (E2B/E4B, 12B encoder-free, 26B MoE "high-throughput, advanced reasoning", 31B dense), 128K/256K context, modalities incl. video, "built-in support for the system role", "configurable thinking modes", built-in function calling.
- https://ai.google.dev/gemma/docs/core/model_card_4 — parameter counts (2.3 B / 4.5 B effective, 11.95 B, 25.2 B total with 3.8 B active, 30.7 B), context per size, audio only E2B/E4B/12B, "35+ languages … pre-trained on 140+", training data cutoff January 2025, Apache 2.0, "Built-in reasoning mode", limitations (factual errors, sarcasm/figurative language).
- https://ai.google.dev/gemma/docs/core/prompt-formatting-gemma4 — complete control-token table: `<|turn>`/`<turn|>`, roles `system`/`user`/`model`, `<|image|>`/`<|audio|>`, `<|tool>`/`<|tool_call>`/`<|tool_response>`/`<|"|>`, `<|think|>`, `<|channel>`/`<channel|>`; multi-turn stripping rule and the tool-call exception.
- https://ai.google.dev/gemma/docs/capabilities/thinking — `enable_thinking=True` in the chat template, ON/OFF templates for E2B/E4B vs. 12B/26B/31B, empty thinking token for output stabilisation, `parse_response` and `skip_special_tokens=False`, switching thinking off mid-conversation by removing `<|think|>`; only ON/OFF states, no depth control; repo IDs of all five `-it` checkpoints (`google/gemma-4-E2B-it` … `google/gemma-4-31B-it`).
- https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4 — syntax for tool declaration, tool call and tool response, recommendation of active thinking for higher function-calling accuracy, "A Gemma model cannot execute code on its own".
- https://ai.google.dev/gemma/docs/releases — release dates: E2B/E4B/31B/26B A4B on 2026-03-31, MTP variants on 2026-04-16, 12B Unified on 2026-06-03; "text, audio and image input and long up to 256K context window".
- https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/ — size designations, 128K/256K, "natively trained on over 140 languages", Apache 2.0, "function-calling, structured JSON output, and native system instructions", Arena AI placements #3/#6, distribution channels.
- https://deepmind.google/models/gemma/gemma-4/ — positioning sentence "Our most intelligent open models …", 140 languages, benchmark values for "Gemma 4 31B IT Thinking".
- https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api — hosted Gemini API IDs `gemma-4-31b-it` / `gemma-4-26b-a4b-it`, `system_instruction`, thinking "strictly" on/off only via `thinking_level` `high`/`minimal`.
- https://ai.google.dev/gemini-api/docs/pricing — Gemma 4: free tier "Free of charge", paid tier "Not available".
- https://huggingface.co/google/gemma-4-31B-it — official repo ID scheme; best practices: `temperature=1.0`, `top_p=0.95`, `top_k=64` "across all use cases", `<|think|>` at the start of the system prompt, image content before the text.
- https://ai.google.dev/gemma/docs/core/prompt-structure — Gemma 3 comparison basis for the migration notes: turn tokens `<start_of_turn>`/`<end_of_turn>`, only the roles `user`/`model`, "the `system` role or a system turn is not supported" (system instruction belongs at the start of the first user message).
- https://ai.google.dev/gemma/docs/core/model_card_3 — Gemma 3 comparison basis for the context jump: "Total input context of 128K tokens for the 4B, 12B, and 27B sizes", 32K for 1B/270M.
