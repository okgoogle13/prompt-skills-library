---
model: deepseek-v3
vendor: DeepSeek
family: DeepSeek
aliases: [deepseek-chat, v3, deepseek-v3-base, deepseek-v3-0324, deepseek-v3-chat]
last_verified: 2026-10-13
status: legacy
successor: deepseek-v4.1-flash
---

# DeepSeek-V3

## Reasoning / Thinking
- **Type: none** (non-reasoning chat model). DeepSeek-V3 is the instruction-tuned chat model of the V3 series and was historically accessed via the model ID `deepseek-chat`. It is **not** a dedicated reasoning model like DeepSeek-R1 and does not return a separate `reasoning_content` trace.
- V3 was trained via **knowledge distillation from DeepSeek-R1** and thereby inherited improved reasoning capabilities, but it is not itself a reasoning model like R1 (unverified) — the chain-of-thought is therefore implicitly trained in, but not exposed as a separate thinking mode.
- **Prompting step-by-step reasoning:** Because V3 has no built-in thinking mode, step-by-step reasoning must be forced explicitly via the prompt — e.g. "Think step by step", structured/hierarchical Markdown prompts, or specifying an outline (problem → solution steps → result) (unverified). Unlike R1, V3 may and should use the **system prompt** to control behavior.
- **Distinction from R1 (`deepseek-reasoner`):** R1 produces a separately delivered chain-of-thought (`reasoning_content`) and, per its model card, should be run without a system prompt; V3 behaves like a classic chat model and follows system prompts. (Note: the API IDs `deepseek-chat` and `deepseek-reasoner` have been retired since 2026-07-24 15:59 UTC (last routed to `deepseek-v4-flash`). Alias semantics per the change log: `deepseek-chat` = V3 (from 2024-12-26), V3-0324 (from 2025-03-24), non-thinking mode of V3.1/V3.1-Terminus/V3.2-Exp/V3.2 (from 2025-08-21), V4-Flash (from 2026-04-24) — the temperature mapping below is only verified for V3-0324. The V3 weights remain available via the open-weights releases.)

## Prompting style
- **Prescriptiveness:** medium-high. V3 behaves more like a classic chat model, responds well to system prompts and to precise, structured instructions (unverified). Clear, hierarchically structured Markdown prompts are recommended (unverified).
- **System prompt fidelity / instruction following:** Good — unlike R1, the system prompt is actively used to fix behavior. The official V3-0324 system prompt template is: `该助手为DeepSeek Chat，由深度求索公司创造。今天是{current date}。`. Inserting the current date into the system prompt is officially intended.
- **Temperature recommendations (official, by use case):**
  - Coding / Math: **0.0**
  - Data Cleaning / Data Analysis: **1.0**
  - General Conversation: **1.3**
  - Translation: **1.3**
  - Creative Writing / Poetry: **1.5**
  - API default: **1.0**.
- **Known quirk — API temperature mapping:** The DeepSeek API scales the `temperature` value internally. Per the V3-0324 model card: for API temperatures 0–1.0, `T_model = T_api × 0.3`; for 1.0–2.0, `T_model = T_api − 0.7`. Concretely: API `temperature=1.0` corresponds to model temperature **0.3**. Anyone running the open weights locally bypasses this mapping and should work directly with the lower raw temperatures (the reference `generate.py` uses e.g. `--temperature 0.7`).

## Strengths & weaknesses (prompt-relevant)
- **Strengths:** Strong MoE model for math, code and multilingual tasks; good at structured output and at following complex system instructions. V3-0324 brought measurable gains (AIME +19.8, GPQA +9.3, MMLU-Pro +5.3) and "improved function calling accuracy".
- **Implicit reasoning, not exposed:** Benefits from the R1 distillation but returns no separately visible reasoning trace — for traceable step-by-step reasoning you must request it in the prompt (or choose R1 instead).
- **Weakness / pitfall:** The API's hidden temperature mapping easily produces results that are more "creative" or more deterministic than the set value suggests — the effective model temperature is noticeably lower than the API value.

## Output & format conventions
- **Feature set (historical endpoint `deepseek-chat`/V3):** Function calling, JSON mode/JSON output, Prefix Completions (beta) and Fill-in-the-Middle (FIM) for code editing.
- **Function calling:** officially supported; the tool calls docs describe function calling and the `strict` mode, which is marked as **beta**.
- **Chat template:** V3 uses a defined chat template; system/user/assistant roles are supported.
- **Structured output:** Easy to control via JSON mode and explicit format instructions in the prompt (Markdown outlines, tables, code blocks).
- **Special templates (V3-0324):** Dedicated prompt templates for file upload (`{file_name}`, `{file_content}`, `{question}`) and web search.

## Migration notes
- **Migrating AWAY FROM DeepSeek-V3:**
  - To **R1 / `deepseek-reasoner`**: reduce system-prompt-based control or move instructions into the user role; expect a separate `reasoning_content`; remove explicit "Think step by step" instructions, since R1 reasons anyway.
  - To **other vendors (OpenAI/Anthropic/Gemini)**: the implicit temperature mapping falls away — recalibrate temperature values (a V3 "API 1.0" corresponded to model 0.3).
- **Migrating TO DeepSeek-V3:**
  - Use the system prompt actively to fix behavior and, if needed, add the DeepSeek date pattern to the system prompt.
  - **Adjust temperature to the official use-case table** and — only for the historical `deepseek-chat` endpoint — account for the API mapping: `temperature=0.0` for deterministic code, up to `1.5` for creative text; when running open weights locally, work with lower raw values.
  - Use hierarchical, structured Markdown prompts and clear step-by-step outlines to elicit step-by-step behavior, since V3 has no automatic thinking mode (unverified).

## Sources
- https://api-docs.deepseek.com/quick_start/parameter_settings — official temperature recommendations by use case (coding 0.0, conversation/translation 1.3, creative 1.5; default 1.0).
- https://huggingface.co/deepseek-ai/DeepSeek-V3 — model card: MoE, 671B total / 37B activated, 128K context, chat vs. base variant, knowledge distillation from the R1 series in post-training.
- https://github.com/deepseek-ai/DeepSeek-V3 — official repo: architecture (MLA, DeepSeekMoE), chat/instruct character, reference `generate.py` with temperature example (0.7).
- https://huggingface.co/deepseek-ai/DeepSeek-V3-0324 — system prompt template, recommended temperature 0.3, API temperature mapping, improvements over V3, file/web-search templates.
- https://api-docs.deepseek.com/guides/tool_calls — function calling, `strict` mode (beta); replaces the taken-offline page `guides/function_calling`.
- https://api-docs.deepseek.com/news/news260424 — retirement of `deepseek-chat`/`deepseek-reasoner` on 2026-07-24 15:59 UTC, routing to `deepseek-v4-flash` until then.
- https://api-docs.deepseek.com/updates — `deepseek-chat` alias history (V3, V3-0324 with improved function calling, V3.1 to V3.2 non-thinking, V4-Flash).
