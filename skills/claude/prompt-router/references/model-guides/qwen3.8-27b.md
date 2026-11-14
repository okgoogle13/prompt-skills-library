---
model: qwen3.8-27b
vendor: Alibaba
family: Qwen
aliases: ["Qwen/Qwen3.8-27B", "Qwen/Qwen3.8-27B-FP8", qwen38-27b]
last_verified: 2026-10-13
status: current
---

# Qwen3.8-27B (Open Weights)

## Reasoning / Thinking
- Type: **hybrid, on by default**. The deep-thinking page lists `qwen3.8-27b` under "Hybrid thinking mode, thinking mode enabled by default"; per the model card the output begins with a `<think>` block.
- Turn it off per request: for self-hosting `"enable_thinking": False` in `extra_body["chat_template_kwargs"]`; on Qwen Cloud pass `enable_thinking` directly (not in `chat_template_kwargs`). In the OpenAI Python SDK Qwen fields belong in `extra_body`; in the Node.js SDK they are top-level.
- Depth control per the model card via `reasoning_effort`: `xhigh` (default), `medium`, `low` — as a **top-level argument** of the Chat Completions call. The card warns that lower effort does not necessarily shorten multi-step agentic tasks, and can lead to insufficient analysis, more failures and retries. The Model Studio docs additionally name `thinking_budget` for the Qwen3.8 series without listing this model individually (model-specific: unverified).
- `preserve_thinking` is **on by default** per the model card (reasoning from all earlier turns is kept); `False` keeps only the reasoning of the last user turn. The deep-thinking page does not list the model among `preserve_thinking`-capable models — unverified on the hosted API.
- Reasoning length documented consistently: Model Studio max CoT **262,144**; the model card recommends up to 262,144 reasoning and 131,072 answer tokens. Whether Model Studio allows only streaming for this model is not documented (unverified).

## Prompting style
- **No model-specific prompting page.** Officially only Alibaba's generic prompt-engineering guide: Context, Objective, Style, Tone, Audience, Response; few-shot examples; numbered step lists; rare delimiters (`###`, `===`, `>>>`). Anything beyond that is unverified for this model.
- **Two separate sampling sets** per the model card: thinking `temperature 1.0`, `top_p 0.95`, `top_k 20`, `min_p 0.0`, `presence_penalty 0.0`, `repetition_penalty 1.0`; instruct/non-thinking `temperature 0.7`, `top_p 0.80`, `top_k 20`, `min_p 0.0`, `presence_penalty 1.5`, `repetition_penalty 1.0`. `presence_penalty` is adjustable between 0 and 2; higher values can cause language mixing. Parameter support varies by framework.
- In thinking mode control depth via `reasoning_effort` rather than "think step by step" text; for agentic tasks plan generous output length (per the card).

## Strengths & weaknesses (prompt-relevant)
- Dense 27B model with vision encoder, 64 layers with interleaved Gated DeltaNet and Gated Attention blocks; per Model Studio "native vision-language" (released 17 Aug 2026), compared with 3.6-27B focused on coding and office scenarios across text and image inputs, plus more reliable end-to-end tasks.
- Input text, image and video (the card also mentions hour-long video processing); output text only. License Apache-2.0.
- Enabled on Model Studio: Function Calling, Structured Outputs, Web Search, Prefix Completion, Context Cache; **not**: batch inference, fine-tuning. Regions: Beijing and Singapore.
- Quirks: static YaRN can degrade performance on short texts — enable only when long-context capacity is really needed. The card does not document the tool-call format or parser flags (unverified). Knowledge cutoff and language coverage are not published (unverified).

## Output & format conventions
- Model Studio: context window 1,000,000; max input 991,808 or 983,616 in thinking mode; max output 131,072; max CoT 262,144. The docs warn that usable length may vary with parameter combinations.
- Self-hosting (model card): native context **262,144**, with YaRN up to 1,000,000 (`factor` matched to the typical length, e.g. 2.0 for ~524,288). Serving via SGLang, vLLM, TokenSpeed; long context only with override flags (vLLM `VLLM_ALLOW_LONG_MAX_MODEL_LEN=1` + `--max-model-len` + `--hf-overrides`, SGLang `SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1` + `--context-length` + `--json-model-override-args`). FP8 variant: `Qwen/Qwen3.8-27B-FP8`.
- Structured output on Model Studio: the "Qwen3.8 open-source series" is listed under `json_object` (the word "JSON" must appear in the prompt), **not** under `json_schema` — strict schema enforcement is not verified for this model.
- Prefix completion: the model page marks it as supported, but the partial-mode page does not list the Qwen3.8 open-source series; interplay with thinking unverified — for prefill routes, set `enable_thinking: false` to be safe.

## Migration notes
- **TO qwen3.8-27b**: thinking runs unless turned off — a prompt ported from a non-thinking model suddenly reasons; re-size `max_tokens`, latency and cost, or set `enable_thinking: false` (self-hosting in `chat_template_kwargs`, Qwen Cloud directly). **Couple the sampling set to the mode**: thinking 1.0/0.95/20, instruct 0.7/0.80/20 with `presence_penalty 1.5` — do not carry over `temperature 0` from the source. Remove CoT scaffolding and set `reasoning_effort`. Coming from a 1M-context model and self-hosting: without YaRN you only get 262,144 tokens. `json_schema` strict mode is unverified — describe the schema in the prompt and write "JSON" into the prompt.
- **AWAY FROM qwen3.8-27b**: remove `enable_thinking` / `reasoning_effort` / `preserve_thinking` / `chat_template_kwargs`; if the target has no built-in reasoning, write explicit reasoning steps into the prompt; video input drops out on many targets.
- As a dense 27B model it is not the flagship of the series: for maximum quality the counterparts are the hosted **qwen3.8-max** or the open **qwen3.8-2.4t-a95b** (thinking only, text only). This tiering is derived from the model pages, not a vendor ranking (unverified).

## Sources
- https://www.alibabacloud.com/help/en/model-studio/qwen3-8-27b — model page (as of 11 Oct 2026): id `qwen3.8-27b`, input image/text/video → text, 1M context, max input 991,808 / 983,616 (thinking), max output 131,072, max CoT 262,144, regions Beijing/Singapore, supported and unsupported features (batch, fine-tuning), note on parameter-dependent lengths.
- https://www.alibabacloud.com/help/en/model-studio/deep-thinking — `qwen3.8-27b` as hybrid with thinking on by default; parameter placement `extra_body` (Python) vs. top-level (Node.js); `thinking_budget` for the Qwen3.8 series; `preserve_thinking` list without this model.
- https://www.alibabacloud.com/help/en/model-studio/newly-released-models — entry of 17 Aug 2026: 27B native vision-language dense, focus on coding/office versus 3.6-27B.
- https://huggingface.co/Qwen/Qwen3.8-27B — official model card: architecture, image/video input, thinking default and switching off via `chat_template_kwargs` or directly on Qwen Cloud, `reasoning_effort` xhigh/medium/low (top-level) with the effort warning, `preserve_thinking`, both sampling sets, output lengths, native context 262,144 / YaRN up to 1M incl. flags, YaRN caveat, FP8 repo, Apache-2.0.
- https://huggingface.co/Qwen/Qwen3.8-27B-FP8 — official FP8 quantization of Qwen/Qwen3.8-27B (Apache-2.0).
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output — "Qwen3.8 open-source series" only under `json_object` (keyword "JSON" required), not under `json_schema`.
- https://www.alibabacloud.com/help/en/model-studio/partial-mode — prefix continuation via last assistant message with `partial: true`; Qwen3.8 open-source series not in the model list.
- https://www.alibabacloud.com/help/en/model-studio/prompt-engineering-guide — generic, not model-specific prompt frame, few-shot, step lists, delimiters.
