---
model: qwen3.8-2.4t-a95b
vendor: Alibaba
family: Qwen
aliases: ["Qwen/Qwen3.8-2.4T-A95B", "Qwen/Qwen3.8-2.4T-A95B-FP8"]
last_verified: 2026-10-13
status: current
---

# Qwen3.8-2.4T-A95B (Open Weights)

## Reasoning / Thinking
- Type: **thinking only, cannot be turned off**. The deep-thinking page lists `qwen3.8-2.4t-a95b` as the only open-source Qwen3.8 model under "Supports thinking mode only"; the model card says thinking is required for all interactions, every response begins with a `<think>` block, and `enable_thinking` "should not be turned off".
- Depth control per the model card via `reasoning_effort` with `xhigh` (default, complex tasks), `medium` and `low` (speed/cost) — in the example code as a **top-level argument** of the Chat Completions call, not in `chat_template_kwargs`. The Model Studio docs instead name `thinking_budget` for the "Qwen3.8 … series" without listing this model individually; whether `thinking_budget` takes effect here is therefore not verified for this model (unverified).
- `preserve_thinking` is **on by default** per the model card (earlier reasoning stays in the history); for self-hosting in `extra_body["chat_template_kwargs"]`, on Qwen Cloud directly in `extra_body`. The deep-thinking page does **not** list the model among `preserve_thinking`-capable models — for the hosted API the behavior is therefore unverified.
- **Documented discrepancy on reasoning length:** Model Studio gives a max chain-of-thought of **131,072** tokens, while the model card recommends (where the framework allows separate limits) **262,144** reasoning tokens plus 131,072 for the final answer. Do not silently adopt one number — set the limit matching your runtime (Model Studio vs. self-hosting).
- Whether the Qwen3.8 open-source models support only streaming on Model Studio is not stated in the docs (the streaming-only note names only older open-source versions such as qwen3.5-27b) — unverified.

## Prompting style
- **No model-specific prompting page.** Officially there is only Alibaba's generic prompt-engineering guide, explicitly not bound to any model: Context, Objective, Style, Tone, Audience, Response; few-shot examples; numbered step lists for complex tasks; rare delimiters (`###`, `===`, `>>>`). Everything else is unverified for this model.
- Because the model always thinks, depth belongs in `reasoning_effort`, not in the prompt text; "think step by step" scaffolding merely duplicates the built-in reasoning.
- Sampling per the model card: `temperature 1.0`, `top_p 0.95`, `top_k 20`, `min_p 0.0`, `presence_penalty 0.0`, `repetition_penalty 1.0`. `presence_penalty` may be raised to 0–2 against repetition, but higher values can cause language mixing and slightly worse performance. Which parameters take effect depends on the inference framework.
- For agentic tasks the model card explicitly recommends generous output length.

## Strengths & weaknesses (prompt-relevant)
- Architecture: sparse MoE with hybrid attention (Gated DeltaNet + Gated Attention), 2.4T parameters, ~95B active, 512 experts (10 routed + 1 shared per token). Per Model Studio, the open-source version of Qwen's current flagship (release 12 Aug 2026).
- Vendor-reported benchmarks (not independently verified; the card itself calls them harness-dependent, partly in-house): GPQA Diamond 92.6, PaperBench 93.0, OSWorld 86.1, CodeArena global #4.
- Enabled on Model Studio: Function Calling, Structured Outputs, Web Search, Prefix Completion, Context Cache; **not**: batch inference, fine-tuning. Regions: Beijing and Singapore.
- Weaknesses/quirks: **text only** (the card excludes multimodal inputs); **no non-thinking path** — every request produces reasoning output. The Hugging Face license tag reads "qwen3.8-max" (not an Apache license). Knowledge cutoff, language coverage and hardware requirements are not published (unverified).

## Output & format conventions
- Model Studio: context window 1,000,000; max input 991,808 or 983,616 in thinking mode; max output 131,072; max CoT 131,072. Input/output text only.
- Self-hosting (model card): native context **262,144**, extendable to 1,010,000 tokens; the card documents no concrete YaRN flags for this (unverified). Serving via SGLang, vLLM, TokenSpeed; the example commands (`vllm serve "Qwen/Qwen3.8-2.4T-A95B"`, SGLang `--model-path …`) name neither a reasoning nor a tool-call parser (unverified). Weights in BF16; `Qwen/Qwen3.8-2.4T-A95B-FP8` is the official FP8 variant (block-wise FP8, block size 128, per the card nearly identical performance).
- Structured output on Model Studio: the "Qwen3.8 open-source series" is listed under `json_object` (the word "JSON" must appear in the prompt), **not** under `json_schema` — strict schema enforcement is not verified for this model.
- Prefix completion is marked as supported on the model page, but the partial-mode page does not list the Qwen3.8 open-source series; how prefill interacts with mandatory thinking is unverified.

## Migration notes
- **TO qwen3.8-2.4t-a95b**: the most important break — **thinking cannot be turned off.** `enable_thinking: false`, non-thinking prefill routes and latency assumptions from a non-thinking source model all break; size `max_tokens` for reasoning plus answer again (131,072 vs. 262,144 CoT depending on runtime, see discrepancy above). Remove explicit CoT requests and control depth via `reasoning_effort` (not `thinking_budget`). Remove image/video input — the model is text-only. Replace `temperature 0`/greedy settings with the card values 1.0 / 0.95 / 20. Anyone who needs `json_schema` strict mode has no verified path here — describe the schema in the prompt and write "JSON" into the prompt (`json_object`).
- **AWAY FROM qwen3.8-2.4t-a95b**: remove the `reasoning_effort` / `chat_template_kwargs` / `preserve_thinking` wiring; if the target has no built-in reasoning, write reasoning and self-check steps back into the prompt. When moving to smaller contexts, redesign chunking.
- The hosted counterpart is **qwen3.8-max**: per the model card, the official version built on this model, with vision input, non-thinking support, 1M default context and built-in tools. Anyone who needs those features migrates there rather than to the open weights; the two are **not** interchangeable.

## Sources
- https://www.alibabacloud.com/help/en/model-studio/qwen3-8-2-4t-a95b — model page (as of 11 Oct 2026): id `qwen3.8-2.4t-a95b`, text in/text out, 1M context, max input 991,808 / 983,616 (thinking), max output 131,072, max CoT 131,072, regions Beijing/Singapore, supported (function calling, structured outputs, web search, prefix completion, context cache) and unsupported features (batch, fine-tuning); no prompting guidance.
- https://www.alibabacloud.com/help/en/model-studio/deep-thinking — `qwen3.8-2.4t-a95b` under "Supports thinking mode only"; `thinking_budget` for the Qwen3.8 series (not model-specific); `preserve_thinking` list without this model; streaming-only note names only older open-source versions.
- https://www.alibabacloud.com/help/en/model-studio/newly-released-models — entry of 12 Aug 2026: open-source version of the current flagship, sparse MoE 2.4T / ~95B active, hybrid attention, benchmarks.
- https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B — official model card: architecture, text-only, thinking mandatory and not switchable, `reasoning_effort` xhigh/medium/low (top-level), `preserve_thinking` on by default, sampling 1.0/0.95/20/0.0, 262,144 reasoning + 131,072 answer, native context 262,144 (up to 1,010,000), SGLang/vLLM/TokenSpeed, relation to Qwen3.8-Max, license tag, benchmark caveats.
- https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8 — official FP8 variant (block-wise FP8, block size 128, nearly identical performance, text-only, always thinking).
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output — "Qwen3.8 open-source series" only under `json_object` (keyword "JSON" required), not under `json_schema`.
- https://www.alibabacloud.com/help/en/model-studio/partial-mode — prefix continuation via last assistant message with `partial: true`; Qwen3.8 open-source series not in the model list.
- https://www.alibabacloud.com/help/en/model-studio/prompt-engineering-guide — generic, not model-specific prompt frame (Context, Objective, Style, Tone, Audience, Response), few-shot, step lists, delimiters.
