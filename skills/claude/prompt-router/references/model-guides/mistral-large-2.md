---
model: mistral-large-2
vendor: Mistral AI
family: Mistral
aliases: [mistral-large-2407, mistral-large-2.0]
last_verified: 2026-10-13
status: legacy
successor: mistral-large-3
---

# Mistral Large 2

## Reasoning / Thinking
- Type: **none** (not a dedicated reasoning/thinking model). Mistral Large 2 (mistral-large-2407) is a classic instruct model without a separate "extended thinking" mode, without visible/hidden reasoning tokens and without adaptive thinking budgets.
- Step-by-step reasoning is triggered classically via the prompt: explicitly request chain-of-thought (e.g. "Think step by step", "Justify first, answer at the end"). Mistral generally recommends structuring instructions clearly and, where needed, supplying few-shot examples with the desired reasoning path.
- The model was specifically trained for **stronger mathematical and logical reasoning** and code — but that is training quality, not a separate reasoning mode.
- Hallucination behaviour: the model was "fine-tuned to be more cautious and discerning" and trained to acknowledge "when it cannot find solutions or does not have sufficient information".

## Prompting style
- **Prescriptiveness / system prompt fidelity:** Mistral explicitly highlights "drastically improved instruction-following and conversational capabilities", with particular strength in "following precise instructions and handling long multi-turn conversations".
- **Recommended prompt structure (official):** define the role first ("You are a <role>, your task is…"), structure instructions hierarchically into clear sections/subsections, write them out in full (as if the reader has no prior knowledge). **Markdown or XML-like tags** are recommended as markup.
- **System vs. user prompt:** the `system` prompt provides base context and behaviour rules, the `user` prompt the task-specific instruction. If no system role is available, the instructions can be concatenated directly into the user message.
- **Official prompt format / [INST] convention:** Mistral Large 2 uses the **Tokenizer V3**. The documented raw template is:
  `<s>[INST] user message[/INST] assistant message</s>[INST] new user message[/INST]`
  — with `<s>`/`</s>` as BOS/EOS, `[INST]`/`[/INST]` as control tokens and one space after each of `[INST]` and `[/INST]`. The **system prompt is by default prepended to the last user message** (followed by two line breaks). Via the API/`mistral_common` this format is generated automatically — manual templating is only needed for self-hosting.
- **Known quirks:** Mistral warns against using subjective terms without definition, building contradictions into long prompts (decision trees work better), asking the model to count tokens, or using purely numeric scales (worded scales perform better).
- **Tool use / function calling:** improved function calling, incl. **parallel and sequential** function calls. The API supports `tools` and the `tool_choice` parameter (`tool_choice="any"` forces a call); parallel calls may come back in any order.

## Strengths & weaknesses (prompt-relevant)
- **Strengths:**
  - Very good, precise **instruction following** and stable **long multi-turn conversations**.
  - **Code (80+ languages)** and **maths/reasoning** at a high level.
  - **Multilingual** (incl. French, German, Spanish, Italian, Portuguese, Arabic, Hindi, Russian, Chinese, Japanese, Korean).
  - **Large context window: 128k tokens.**
  - **Reliable function calling** (parallel + sequential).
  - **Trained for brevity** — follows brevity requests well.
- **Weaknesses / watch-outs:**
  - No native reasoning mode — complex multi-step logic must be triggered via CoT/prompt structure (unverified whether this matches current dedicated reasoning models).
  - Like all LLMs, prone to errors on counting/token-based tasks; Mistral explicitly advises against these.
  - Contradictory or long unstructured prompts degrade instruction following — a clear hierarchy is needed.

## Output & format conventions
- **Conciseness as design goal:** Mistral stresses "conciseness is paramount". Outputs tend to be brief; request detailed answers explicitly where needed.
- **Structured outputs / JSON:** for machine-readable output Mistral recommends JSON output and offers a **Structured Outputs** feature to enforce consistent JSON schemas.
- **Formatting standard:** Markdown or XML-like tags for structuring inputs and outputs are officially recommended.
- **Few-shot:** example dialogues (alternating user/assistant messages) improve format and behaviour fidelity.
- Vision/multimodality: for mistral-large-2407 **not** listed as a capability in the model card (text model).

## Migration notes
- **Typical changes when migrating AWAY FROM Mistral Large 2 (2407):**
  - Vendor replacement per the model card and legacy table is **Mistral Large 3 (`mistral-large-2512`)**; `mistral-large-latest` no longer points to 2407. For reproducibility pin `mistral-large-2512` instead of `-latest` (which, per the lifecycle docs, can change silently across generations). The intermediate version Large 2.1 (`mistral-large-2411`) is itself retired: deprecation 27 Feb 2026, retirement date 31 May 2026, replacement per the model card Mistral Medium 3.5. `mistral-large-2407` has been retired since **30 Mar 2025**; per the lifecycle docs requests to retired IDs fail with 404 — pinning to 2407 no longer helps.
  - When switching to a **dedicated reasoning model**, remove explicit CoT instructions where applicable (unverified).
- **Typical changes when migrating TO Mistral Large 2:**
  - 2407 has not been available via the Mistral API since 30 Mar 2025 (requests return 404); the model card still links the weights (license MRL).
  - Observe the **[INST] format / Tokenizer V3** if self-hosting: the system prompt is prepended to the last user message; with API use `mistral_common` handles this automatically.
  - Switch function calling to the Mistral schema (`tools` + `tool_choice`; parallel calls possible, order not guaranteed).
  - Since the model is trained for brevity: if the previous model was expected to give detailed answers, explicitly request the output length where needed.
  - Restructure prompts around **a clear hierarchy + Markdown/XML tags**.
  - A 128k context allows simpler RAG/chunking strategies.

## Sources
- https://mistral.ai/news/mistral-large-2407/ — Official announcement "Large Enough": 123B parameters, 128k context, languages/code languages, improved instruction following & multi-turn, function calling (parallel/sequential), conciseness as design goal, hallucination reduction.
- https://docs.mistral.ai/models/mistral-large-2-0-24-07 — Official model card: API ID `mistral-large-2407`, 128k context, 123B parameters, retirement date 30 Mar 2025, replacement Mistral Large 3, weights linked under MRL, no vision capability.
- https://docs.mistral.ai/studio/conversations/chat-completion/prompting — Official prompting recommendations: role definition, hierarchy, system vs. user prompt, Markdown/XML tags, few-shot, JSON/Structured Outputs, anti-patterns.
- https://docs.mistral.ai/resources/cookbooks/concept-deep-dive-tokenization-chat_templates — Tokenizer V3 chat template: `[INST]/[/INST]` convention, `<s>`/`</s>`, placement of the system prompt.
- https://docs.mistral.ai/resources/changelogs — Changelog: release 24 Jul 2024, alias `mistral-large-latest`, successor `mistral-large-2411`.
- https://docs.mistral.ai/models — Legacy table: 2407 → Mistral Large 3 (deprecation 30 Nov 2024, retirement 30 Mar 2025), 2411 → Mistral Medium 3.5 (deprecation 27 Feb 2026, retirement 31 May 2026).
- https://docs.mistral.ai/models/mistral-large-2-1-24-11 — Model card Large 2.1: "Use Mistral Medium 3.5 for new integrations".
- https://docs.mistral.ai/inference/model-lifecycle — retired IDs return 404; `-latest` points across generations to the newest version and can change silently.
- https://docs.mistral.ai/resources/cookbooks/mistral-function_calling-function_calling — Function-calling details: `tool_choice` (incl. `"any"`), parallel tool calls.
