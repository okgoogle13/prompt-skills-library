---
model: mistral-large-3
vendor: Mistral AI
family: Mistral
aliases: [mistral-large, mistral-large-latest, mistral-large-2512, large-3, large3, Mistral-Large-3-675B-Instruct-2512]
last_verified: 2026-10-13
status: current
---

# Mistral Large 3

## Reasoning / Thinking
- Type: **no reasoning mode**. The vendor card literally states under "Limitations" "Not a dedicated reasoning model"; the docs model card lists neither a `reasoning_effort` nor a thinking parameter. The announcement of 2 Dec 2025 promised a reasoning version ("A reasoning version is coming soon!") — it is not included in this model. Since 6 Oct 2026 Mistral Large 4 (Public Preview) exists with `reasoning_effort`; Large 3 itself remains without a reasoning feature per the model card.
- Depth therefore comes **exclusively from the prompt**: explicit step-by-step / chain-of-thought in the system or user prompt. There is no control to turn up.
- Confusion risk within the same house: per the reasoning docs **Mistral Medium 3.5** (`mistral-medium-3-5`), **Mistral Small 4** (`mistral-small-latest`) and **Mistral Large 4** (`mistral-large-4-0`) support "adjustable reasoning via the `reasoning_effort` parameter" — Large 3 does not. A prompt that relies on `reasoning_effort` does not come from Large 3; within the Large line only Large 4 qualifies for that.
- Instead of a reasoning control, sampling is steered: "Use a temperature below 0.1 for daily-driver and production environments"; higher temperatures only for creative cases.

## Prompting style
- **The system prompt is the primary control surface**: "Define a clear environment and use case, including guidance on how to effectively leverage tools in agentic systems."
- Role-first framing from the official prompting docs: "You are a <role>, your task is to <task>." Structure instructions hierarchically into sections/subsections and write them as if "you're writing for someone with no prior context".
- Structure via **Markdown and/or XML-like tags** (justified by "Readable", "Parsable", "Familiar"). Few-shot either as an "Examples" section or as artificial user/assistant turns. System = general context, user = context of the current interaction; without a system role concatenate both into the user turn.
- **Keep tools lean**: "limit their number to the minimum required for the use case", "Avoiding overloading the model with an excessive number of tools."
- Images: keep aspect ratio near **1:1**; crop very narrow/wide images beforehand.
- Documented anti-patterns: vague quantitative adjectives ("too long", "too short", "many", "few") and woolly words ("things", "stuff", "interesting", "better"), contradictory instructions (use decision trees instead), having the model count (pass character/token counts as input), unnecessary output tokens, numeric 1–5 scales (use word scales such as "Very Good", "Neutral" instead).

## Strengths & weaknesses (prompt-relevant)
- Strengths: "state-of-the-art, open-weight, general-purpose multimodal model" under Apache 2.0; per the announcement of 2 Dec 2025 at the time "our most capable model to date" and "one of the best permissive open weight models in the world", with image understanding and "best-in-class performance on multilingual conversations" across "40+ native languages". The vendor-provided optimised checkpoint runs, per the announcement, on a single 8×A100 or 8×H100 node via vLLM. Cheap for its class: $0.5/M input, $1.5/M output.
- Architecture: granular MoE with 675B total and 41B active parameters (673B/39B language model + 2.5B vision encoder).
- Weaknesses: "Not a dedicated reasoning model" and "Behind vision-first models in multimodal tasks"; the very low temperature recommendation (<0.1) forces recalibration of creative setups.
- Upgrade-path trap: Mistral's own legacy table points **Mistral Large 2.1 (`mistral-large-2411`) to Mistral Medium 3.5**, not to Large 3 (deprecation 27 Feb 2026, retirement 31 May 2026). Only Large 2.0 (`mistral-large-2407`) and Large 1.0 (`mistral-large-2402`) point to Large 3.

## Output & format conventions
- **256k context window** (docs model card and vendor card agree). A **maximum output token limit is officially not documented (unverified)**; the only value the vendor shows is `max_tokens = 262144` (constant `MAX_TOK`) in the vendor card's example code.
- Features supported per the model card: function calling, structured outputs, Chat Completions (`/v1/chat/completions`), document QnA, prefix (assistant prefill), batching, agents & conversations, built-in tools.
- Multimodal input (text + image) is supported; enforce format fidelity via structured outputs or prefix prefill rather than prose requests.
- Production API ID: `mistral-large-2512`; per the model card `mistral-large-latest` is currently an alias for it (as of 2026-10-13) — also after Large 4's preview launch. Per the lifecycle docs `-latest` points to the "Latest version, across generations" and can change silently — pin `mistral-large-2512` for reproducible prompts.

## Migration notes
- **FROM Mistral Large 3**: remove image content parts for text-only targets; re-plan prompt budget if the target has under 256k context; re-calibrate temperature upwards (most targets assume defaults well above 0.1); replace Mistral specifics such as prefix prefill, built-in tools and `/v1/conversations` with target equivalents; the Apache 2.0 self-hosting path lapses for closed-weight targets.
- **FROM Large 3 to Mistral Large 4** (Public Preview, `mistral-large-4-0`): set `reasoning_effort` explicitly — Large 4's default is not documented (unverified) — and at `"high"` review hand-written chain-of-thought; parse `message.content` as a list of `ThinkChunk`/`TextChunk` and replay `ThinkChunk` across all turns; context grows from 256k to 1M; the `temperature` < 0.1 rule is not documented for Large 4 (unverified). `mistral-large-latest` does not reach Large 4 — set the ID explicitly. Per `/models` Large 3 is not deprecated; the vendor documents no replacement by Large 4.
- **TO Mistral Large 3**: set the model ID to `mistral-large-2512` (the vendor's intended path from `mistral-large-2407`/`mistral-large-2402`); context grows to 256k, chunking/RAG splitting may be loosened accordingly; external OCR/vision preprocessing drops away, pass images directly as content parts at roughly 1:1 aspect ratio; lower temperature to <0.1 for production; move environment, use-case and tool instructions into the system prompt and reduce the number of tools; do **not** add thinking/reasoning parameters or "reasoning effort" phrasing — use explicit chain-of-thought prompting instead; remove legacy hand-rolled `[INST]` templating from the Large 2 era and use normal chat messages via the API (which chat template Large 3 expects when self-hosting is not verified here — use the tokenizer/template from the official repo).

## Sources
- https://docs.mistral.ai/models/mistral-large-3-25-12 — official model card: API names `mistral-large-2512` and `mistral-large-latest`, GA, v25.12, 2 Dec 2025, Apache 2.0, 256k context, 41B active / 675B total, $0.5/M in and $1.5/M out, feature list; no reasoning parameter, no max output figure.
- https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512 — official vendor card: temperature <0.1, system-prompt and tool-count guidance, 1:1 image ratio, 256k context, `max_tokens=262144` in example code, MoE 673B/39B + 2.5B vision encoder, limitations "Not a dedicated reasoning model" / "Behind vision-first models in multimodal tasks".
- https://docs.mistral.ai/studio/conversations/chat-completion/prompting — official prompting guidance: role framing, hierarchical structure, Markdown/XML tags, few-shot, system-vs-user split, anti-pattern list.
- https://docs.mistral.ai/models — current line-up (Large 3, Apache 2.0, v25.12, "open-weight, general-purpose multimodal"; Large 3 not in the deprecated table, Large 4 featured) and legacy table: 2407/2402 → Large 3, 2411 → Medium 3.5 (27 Feb 2026, 31 May 2026).
- https://docs.mistral.ai/resources/changelogs — release entry "We released Mistral Large 3 (`mistral-large-2512`)" and the entry of 6 Oct 2026 on Mistral Large 4 (`mistral-large-4`) in Public Preview.
- https://mistral.ai/news/mistral-3/ — announcement of 2 Dec 2025: "most capable model to date", 40+ languages, image understanding, Apache 2.0, 8×A100/8×H100 via vLLM, "A reasoning version is coming soon!".
- https://docs.mistral.ai/studio/conversations/reasoning — reasoning docs: `reasoning_effort` for `mistral-small-latest`, `mistral-medium-3-5` and `mistral-large-4-0`; Large 3 not listed; `ThinkChunk`/`TextChunk` response form and replay rule.
- https://docs.mistral.ai/models/mistral-large-4-0 — model card Mistral Large 4: Public Preview since 6 Oct 2026, API names `mistral-large-4` / `mistral-large-4-0`, 1M context.
- https://docs.mistral.ai/inference/model-lifecycle — alias levels (`-latest` = "Latest version, across generations") and warning about silent alias updates.
