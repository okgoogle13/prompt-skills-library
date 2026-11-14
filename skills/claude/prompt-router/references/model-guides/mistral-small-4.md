---
model: mistral-small-4
vendor: Mistral AI
family: Mistral
aliases: [mistral-small, mistral-small-latest, mistral-small-2603, small-4, small4, Mistral-Small-4-119B-2603]
last_verified: 2026-10-13
status: current
---

# Mistral Small 4

## Reasoning / Thinking
- Type: **hybrid, switchable per request** via `reasoning_effort` — per the vendor one model that unifies Instruct, Reasoning (formerly Magistral) and Devstral. The official chat template accepts exactly **two** values and otherwise aborts with `reasoning_effort must be either "none" or "high"`. No token budget, no `thinking` object.
- **Default is `"none"`**: if the field is missing, the template sets it to `none` itself. A carried-over prompt therefore runs without reasoning unless the control is set explicitly.
- `"none"`: per the vendor "equivalent to the same chat style of Mistral Small 3.2" — fast, light answers. `"high"`: "Deep, step-by-step reasoning for complex problems, with equivalent verbosity to previous Magistral models"; vendor recommendation `high` for complex prompts.
- Sampling is **coupled to the mode**: `temperature` 0.7 with `"high"`, 0.0–0.7 depending on the task with `"none"` (the official examples use 0.1).
- Multi-turn requirement: replay the complete assistant message **including `ThinkChunk`** into the history — "Do not strip ThinkChunk from assistant messages before replaying them. … significantly degrades output quality."
- `reasoning_effort` also applies on `/v1/agents` and `/v1/conversations`, there in the field `completion_args`.

## Prompting style
- **System prompt as the primary control surface**: the vendor card lists "System Prompt: Strong adherence and support for system prompts", and all official usage examples load the bundled `SYSTEM_PROMPT.txt` as the system message (placeholders `{today}` / `{yesterday}` are filled in beforehand).
- Self-hosting pitfall: if there is no system message, the official chat template **adds its own** default system prompt (Le Chat persona, date and tool rules). Anyone wanting neutral behavior should supply their own system prompt. Whether the API does the same is not documented (unverified).
- Role-first framing from the official prompting docs: "You are a <role>, your task is to <task>."; structure instructions hierarchically, structure via Markdown and/or XML-like tags, few-shot as example turns in the history.
- Plan for literalness: "Mistral Small 4 can follow your instructions to the letter." Spell out scope, stop conditions and output form.
- Documented anti-patterns of the prompting docs: vague quantities and fuzzy words, contradictory rules (use a decision tree instead), having the model count, requesting unnecessary output tokens, numeric rating scales instead of word scales.

## Strengths & weaknesses (prompt-relevant)
- Architecture: MoE with 128 experts, 4 active; 119B total parameters. Active parameters: model card and HF card say **6.5B**, the announcement "6B active parameters per token (8B including embedding and output layers)" — the figures differ.
- Text + image in, text out. Multilingual: the HF card says "dozens of languages" (incl. English, French, Spanish, German, Chinese, Japanese, Korean, Arabic).
- Agentic and coding use are part of the design: "native function calling and JSON output"; per the deprecated table it replaces, among others, `magistral-small-*` and `devstral-small-2507`.
- Terse reasoning output: per the vendor, Small 4 with reasoning matches or beats GPT-OSS 120B on all three benchmarks shown, "while generating significantly shorter outputs"; on LiveCodeBench with 20% less output. Prompts that force long justifications work against this.
- Cost: $0.15 input / $0.015 cached input / $0.6 output per 1M tokens — one tenth of the input and 8% of the output price of Mistral Medium 3.5. `"high"` increases output tokens.
- Knowledge date: the official system prompt says "Your knowledge base was last updated on Friday, November 1, 2024." Mistral publishes no separate cutoff (unverified). Maximum output token limit: not documented (unverified).

## Output & format conventions
- Context window 256k. API names per model card: `mistral-small-2603` (fixed) and `mistral-small-latest` (per lifecycle docs "Latest version, across generations"; "Using an alias may expose you to silent updates in model behavior and pricing"). For reproducible prompts pin `mistral-small-2603`.
- Response form depends on the mode: with `"high"`, `message.content` is a list of `ThinkChunk` and `TextChunk`; with `"none"` a plain `str`. In streaming, `delta.content` is first a list (thinking), then a transition chunk with a closing `ThinkChunk` plus the first `TextChunk`, then a plain string.
- Features per model card: Chat Completions, Function Calling, Agents & Conversations, Built-In Tools, Structured Outputs, **Predicted Outputs**, Document QnA, Prefix (assistant prefill), Batching.
- Self-hosting template markers: `[SYSTEM_PROMPT]`, `[INST]`, `[AVAILABLE_TOOLS]`, `[MODEL_SETTINGS]{"reasoning_effort": …}[/MODEL_SETTINGS]`, `[THINK]`, `[TOOL_CALLS]…[ARGS]`, `[TOOL_RESULTS]`, `[IMG]`. Only the roles `user`, `assistant`, `system`, `tool`; the conversation must start with `user` or `system`.
- Image placement in the template: images only in user and tool messages; system messages are plain text; assistant messages contain only text and thinking. If a user turn consists of exactly one text block followed by an image block, the template moves the image to the front.
- vLLM serving per HF card: `--tool-call-parser mistral --enable-auto-tool-choice --reasoning-parser mistral`.

## Migration notes
- **TO Mistral Small 4**: Mistral names Small 4 as the alternative for `mistral-small-2506`, `mistral-small-2503`, `mistral-small-2501`, `mistral-small-2409`, `mistral-small-2402`, `magistral-small-2509`, `magistral-small-2507`, `magistral-small-2506`, `devstral-small-2507`, `open-mixtral-8x7b`, `open-mixtral-8x22b`, `mistral-saba-2502` and Mathstral 7B — set the target id accordingly.
- Coming from **Magistral Small**: set `reasoning_effort: "high"` **explicitly**, otherwise the prompt silently runs on `none` and loses its reasoning. Replace hand-parsed `[THINK]` tags with `ThinkChunk` handling and set `temperature` to 0.7.
- Coming from **Mistral Small 3.x** or `devstral-small-2507`: per the vendor `"none"` matches the Small 3.2 chat style; for complex or agentic tasks set `"high"` deliberately and then rebuild response parsing around the chunk list.
- **AWAY FROM Mistral Small 4**: remove `reasoning_effort`, `ThinkChunk` parsing and the replay rule; goals without a reasoning control need explicit step-by-step scaffolding in the prompt again. Recalibrate the mode-coupled sampling values. Replace Mistral specifics (prefix prefill, Predicted Outputs, built-in tools, `completion_args`). For targets below 256k, re-plan the context budget; for text-only targets, remove image parts.
- Within the family: Mistral Medium 3.5 and Mistral Large 4 (`mistral-large-4-0`) also accept `reasoning_effort`, so a prompt with this field may come from any of the three.

## Sources
- https://docs.mistral.ai/models/mistral-small-4-0-26-03 — official model card: release 16 Mar 2026, GA, Apache 2.0, v26.03, "119B parameters with 6.5B active", 256k context, API names `mistral-small-2603` and `mistral-small-latest`, $0.15 / $0.6 per 1M, feature list incl. Predicted Outputs.
- https://docs.mistral.ai/models — line-up (Small 4 as featured) and deprecated table with Mistral Small 4 as the alternative for the Small, Magistral Small, Devstral Small, Mixtral, Saba and Mathstral models listed above.
- https://docs.mistral.ai/capabilities/reasoning — `mistral-small-latest` and `mistral-large-4-0` with `reasoning_effort`, semantics of `none`/`high`, chunk response form, streaming sequence, multi-turn replay warning, `completion_args` on Agents/Conversations.
- https://huggingface.co/mistralai/Mistral-Small-4-119B-2603 — official vendor card: MoE 128/4, 119B / 6.5B active, text + image in, "Strong adherence and support for system prompts", "follow your instructions to the letter", recommended temperature per mode, mode comparison with Small 3.2 and Magistral, benchmarks against GPT-OSS 120B, vLLM flags.
- https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/raw/main/chat_template.jinja — official chat template: default `reasoning_effort = 'none'`, the `none`/`high` value check, default system prompt when no system message is present, markers, role and ordering rules, image placement.
- https://huggingface.co/mistralai/Mistral-Small-4-119B-2603/raw/main/SYSTEM_PROMPT.txt — official system prompt with knowledge-base date 1 Nov 2024 and tool-use rules.
- https://mistral.ai/news/mistral-small-4/ — announcement: unifies Magistral, Devstral and Mistral Small, "6B active parameters per token (8B including embedding and output layers)", mode description, shorter outputs than GPT-OSS 120B, API name `mistral-small-latest`.
- https://docs.mistral.ai/inference/pricing — standard tier: Small 4 $0.15 input / $0.015 cached / $0.6 output; Medium 3.5 $1.5 / $0.15 / $7.5 per 1M tokens.
- https://docs.mistral.ai/inference/model-lifecycle — alias levels (`-latest` "Latest version, across generations") and the warning about silent alias updates.
- https://docs.mistral.ai/inference/prompting — cross-model prompting guidance: role framing, structure, Markdown/XML tags, few-shot, anti-patterns.
