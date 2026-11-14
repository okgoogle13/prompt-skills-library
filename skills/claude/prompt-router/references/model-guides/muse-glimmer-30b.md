---
model: muse-glimmer-30b
vendor: Meta
family: Muse
aliases: [muse-glimmer, glimmer, muse_glimmer, "meta-models/Muse-Glimmer-30B", muse-glimmer-30b-gguf]
last_verified: 2026-10-13
status: current
---

# Muse Glimmer 30B

## Reasoning / Thinking
- Type: **always on, but a separate channel**. Before the answer, the model writes a private chain of thought as an `assistant to=self` turn; the user-facing answer follows in a separate `assistant to=user` turn.
- Depth via `reasoning_strength` (`xhigh | high | medium | low`, default `high`) — not a sampling parameter. Two officially documented routes: (a) preferably as a chat-template argument to `apply_chat_template`, or in llama.cpp via `--chat-template-kwargs '{"reasoning_strength":"low"}'` (per request `chat_template_kwargs`) — the template renders from this the line `Reasoning strength: <value>` into the system turn; (b) per the HF model card, directly as the line `Reasoning strength: <value>` in the system prompt — the prompt-side lever when no template kwargs can be passed. What happens when (a) and (b) are used together is not documented (unverified) — use only one route. OpenAI's `reasoning_effort` is not implemented in llama.cpp and controls nothing.
- Pass earlier traces back via the `reasoning_content` field on the assistant message — the template renders it as the `to=self` turn. On vLLM set `--reasoning-parser muse_glimmer`, otherwise the thinking channel leaks into `content` instead of `message.reasoning`.
- Reasoning traces can get long (Meta gives no concrete token lengths anywhere, unverified): plan for `"stream": true` (request timeouts) and leave `max_tokens` generous — too small cuts off mid-reasoning before the final answer arrives.

## Prompting style
- **Rule No. 1: always `apply_chat_template()`** with `add_generation_prompt=True` (for images use `AutoProcessor` instead of a bare tokenizer). Hand-built prompt strings cost quality: the template sets the system metadata block, the reasoning-strength line and `<|eom|>` vs. `<|eot|>` for consecutive same-role turns. In llama.cpp also `--jinja` — without it tool calling and reasoning separation break.
- System prompt: state the task concretely and the constraints (format, length limit, tone) **up front**. Explicitly avoid "meta-instructions about how the model works internally" — i.e. no instructions about how the model should think internally.
- Sampling per the prompting guide and HF model card: `temperature 1.0`, `top_p 0.95`, `top_k 64`. Warning (vLLM recipe): "Don't run this model greedy. Sending `"temperature": 0` overrides the published settings."

## Strengths & weaknesses (prompt-relevant)
- Strengths: agentic end-to-end tasks (DeepSearch QA, MCP-Atlas, τ-Bench, SWE-Bench), reliable tool use with precise schemas, multi-step reasoning across long workflows, error diagnosis/recovery, multimodal input, 100+ languages. 30B dense: 4-bit under 20 GB (24–32 GB GPUs), bf16 serving ~72 GB VRAM.
- Weaknesses/quirks: **exactly one tool call per turn, no parallel calls** — every tool result must come back before the next tool is chosen. Text + image in, text only out. There is no official limitations section beyond this (unverified).

## Output & format conventions
- Context: 128K default ("longer contexts supported"), native 131072 (llama.cpp: `-c 131072 -np 1 -a muse-glimmer --jinja`). **Max output tokens nowhere officially stated (unverified)** — only the hint to set `max_tokens` for trace + answer with headroom.
- Control tokens: `<|begin_of_text|>`/`<|end_of_text|>`, `<|start|>` (opens a turn: role + optional `to=`), `<|message|>` (separates header from content), `<|eot|>` (end of turn), `<|eom|>` (turn continues), `<|image|>` (image sentinel).
- Tool calls in the native ATEM format, rendered from OpenAI-style schemas in the template's `tools` argument: `<|start|>assistant to=<tool><|message|><atem:function_calls><atem:invoke name="…"><atem:parameter name="…">…</atem:parameter></atem:invoke></atem:function_calls><|eot|>`. Behind an OpenAI-compatible vLLM/llama.cpp server (parser `muse_glimmer`, with underscores) this arrives as a normal `tool_calls` — never write ATEM by hand.
- Structured output / JSON-schema mode and assistant prefill are not officially documented (unverified). No Meta Model API id exists (the Model API hosts, per the overview as of 2026-10-13, `muse-wonder-1.0`, `muse-spark-*`, `muse-image-1.0`, `muse-voice-transcribe-1.0` and `sam-3.1`, but no Glimmer; Meta names Fireworks AI, OpenRouter and Together AI among launch partners, whose model ids are not documented, unverified) — the production identifier is the HF repo `meta-models/Muse-Glimmer-30B` (plus `-GGUF`, `-assistant` as DFlash draft, `-ExecuTorch-PTE`), Apache 2.0.

## Migration notes
- **AWAY FROM Muse Glimmer**: write explicit chain-of-thought instructions back into the prompt; translate ATEM blocks into the target's function-call format; remove the `reasoning_strength`/`reasoning_content` wiring; re-enable parallel tool calls where the target supports them.
- **TO Muse Glimmer** (typical source: Llama 4): turn syntax `<|header_start|>role<|header_end|>` → `<|start|>role<|message|>` (+ `<|eom|>` for consecutive turns); `ipython` role and Python/JSON calls (`[get_weather(city="…")]`) → recipient-tagged turns `to=<tool>` with ATEM; batched tool requests → sequential turns (only one call per turn); drop "think step by step" scaffolding and set `reasoning_strength` instead (template argument, or for a pure prompt migration the system-prompt line `Reasoning strength: <value>`); image machinery (`<|image_start|>`/`<|patch|>`/`<|tile_x_separator|>`) → one `<|image|>` + `AutoProcessor`; **context regression 10M (Scout) / 1M (Maverick) → ~131K** ⇒ chunking/retrieval needed; remove `temperature 0`, add 1.0 / 0.95 / 64; no hand-built prompt strings any more.
- Note: Meta nowhere declares Llama 4 deprecated and documents no Llama→Muse migration path. Treat Glimmer (as of 2026-10-13) as the current open Meta model; for >131K context keep Scout in view.

## Sources
- https://dev.meta.ai/docs/muse-glimmer/prompting — special-token table, `to=user`/`to=self`/`to=<tool>`, ATEM format, "one tool call per turn", `reasoning_strength` + `reasoning_content`, `apply_chat_template` requirement, sampling 1.0/0.95/64, system-prompt rules.
- https://dev.meta.ai/docs/muse-glimmer — architecture (dense, decoder-only, multimodal with vision encoder), 30B, Apache 2.0, text + image in / text out, 128K default, launch-partner list (incl. Fireworks AI, OpenRouter, Together AI).
- https://dev.meta.ai/docs/muse-glimmer/llama-cpp — native context 131072, `--jinja`, `-a muse-glimmer`, `-c`/`-np`, `--chat-template-kwargs`, `reasoning_effort` not implemented.
- https://dev.meta.ai/docs/muse-glimmer/vllm — ~72 GB VRAM, tool-call parser and `--reasoning-parser muse_glimmer`, greedy warning, streaming/`max_tokens` note.
- https://dev.meta.ai/resources/blog/build-with-muse-glimmer — `apply_chat_template`/`add_generation_prompt`, `to=self`/`to=user` flow, 128K, 4-bit under 20 GB for 24–32 GB GPUs, speculative decoding.
- https://dev.meta.ai/docs/muse-glimmer/get-the-model — the four official Hugging Face repos and GGUF file names incl. vision projector and DFlash draft.
- https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model — distillation lineage from Muse Spark, agentic strengths/benchmarks, 100+ languages, no limitations section.
- https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama4 — Llama 4 page with all migration deltas: header tokens, `ipython` role, tool-output format, image tokens, Scout 10M / Maverick 1M.
- https://dev.meta.ai/docs/overview — Model API hosts (as of 2026-10-13) `muse-wonder-1.0`, `muse-spark-1.3`/`1.2`/`1.1`, `muse-spark-1.3-contributor`/`1.2-contributor`, `muse-image-1.0`, `muse-voice-transcribe-1.0`, `sam-3.1`; Muse Glimmer runs only from the open weights (no Model API id).
- https://dev.meta.ai/llama/docs/deployment/versioning — Llama 4 Scout/Maverick not deprecated; no documented Llama→Muse migration path.
- https://huggingface.co/meta-models/Muse-Glimmer-30B — official model card (Meta Superintelligence Lab): ~29.6B parameters incl. vision encoder, 131,072+ context, Apache 2.0, sampling 1.0/0.95/64, 100+ languages, best practice "Reasoning strength can be defined as part of the system prompt as `Reasoning strength: <value>`".
