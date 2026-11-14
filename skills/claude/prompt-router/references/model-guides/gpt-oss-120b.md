---
model: gpt-oss-120b
vendor: OpenAI
family: gpt-oss
aliases: [gpt-oss, gpt-oss-20b]
last_verified: 2026-10-13
status: current
---

# gpt-oss-120b (also applies to gpt-oss-20b)

## Reasoning / Thinking
- Effort levels `low | medium | high` (both sizes). The level is set **in the system message**, not via an API parameter: "To control the reasoning you can specify in the system message the reasoning level as low, medium, or high" — recommended line `Reasoning: high`. Default: "By default, the model will do medium level reasoning."
- The chain-of-thought comes raw in the **`analysis` channel**. It is not subject to the same safety standards as the final answer: "You should not show the chain-of-thought to your users, as they might contain harmful content."
- Multi-turn rule: "In general, you should drop any previous CoT content on subsequent sampling" — once a turn has ended with a `final` message. Exception for tool calling: previous CoT stays in the history so the model can keep reasoning.
- No `none`/`minimal`, no `xhigh`/`max`, no token budget documented.

## Prompting Style
- **Harmony format is mandatory**: "gpt-oss should not be used without using the harmony format, as it will not work correctly." Via inference providers (e.g. Ollama) or an API the format is rendered automatically; in your own stack use the `openai-harmony` renderer or the Transformers chat template instead of setting tokens by hand.
- **Roles and precedence**: `system > developer > user > assistant > tool`.
- **System message = metadata, not the usual system prompt**: identity line ("You are ChatGPT, a large language model trained by OpenAI."), knowledge cutoff, current date, reasoning level, valid channels (`analysis`, `commentary`, `final`) and, if applicable, built-in tools (`browser`, `python`).
- **Developer message = the actual instructions**: "It contains the instructions that are provided to the model and optionally a list of function tools available for use." Task instructions go under `# Instructions`, function tools under `# Tools`, output schemas under `# Response Formats`.
- **Watch the chat template**: "Note that the `Developer` role in Harmony maps to the `system` prompt in the chat template." If you work via the Transformers chat template (or a provider), write the instructions into the `system` message; only with raw Harmony rendering do they belong in the `developer` message.
- **Function tools** are declared in a TypeScript-like `namespace functions { … }` block (comments as descriptions); the model addresses the call via `to=functions.<name>` and can set the argument format (e.g. `json`) via `<|constrain|>`; the tool result returns to the assistant as a `tool` message in the `commentary` channel.

## Strengths & Weaknesses (prompt-relevant)
- Open weights under **Apache 2.0**. 120b: 117B total / 5.1B active, "Most powerful open-weight model, fits into an H100 GPU" (≥ 60 GB VRAM or multi-GPU per the Transformers guide). 20b: 21B total / 3.6B active, "Medium-sized open-weight model for low latency", approx. 16 GB VRAM with MXFP4. Both share format, channels, effort control and limits — the prompt contract is identical.
- **Text only** in and out; no image or audio input. Knowledge cutoff **1 Jun 2024** — supply time-critical facts in the context.
- Weakness: `# Response Formats` "will, however, only influence the model's behavior but doesn't guarantee the full adherence to the schema" — enforce schema adherence in self-hosting via constrained sampling or validation.
- Built-in tools `browser` (search/open/find) and `python` (stateful Jupyter, 120 s timeout) exist only if your own stack implements them.
- Benchmark and quality comparisons against the API models are not claimed here (unverified).

## Output & Format Conventions
- Three channels: **`final`** = solely for the end user; **`analysis`** = CoT, never display; **`commentary`** = function-tool calls (usually also built-in calls) and occasionally preambles that describe the plan before several tool calls.
- Stop tokens: `<|return|>` = final answer complete, `<|call|>` = tool call; `<|end|>` closes individual messages. When saving to history, replace the closing `<|return|>` with `<|end|>`.
- Context window **131,072** tokens, max. output **131,072** (both sizes).
- OpenAI API page: endpoints Responses and Batch (no Chat Completions), features streaming, structured outputs, function calling; tools function calling, code interpreter, MCP, web search. Only snapshot `gpt-oss-120b` or `gpt-oss-20b`.

## Migration Notes
- **TO gpt-oss**: the central step is redistributing roles — move task instructions, persona and rules from the existing system prompt into the developer role (`# Instructions`); use the system message only for metadata and the `Reasoning: <level>` line. With the chat template/provider, the `system` message lands in the developer role automatically. Put tool schemas in the `# Tools` section of the developer message and output schemas under `# Response Formats` (plus validation). Replace API effort parameters (`reasoning.effort`, thinking budgets) with the `Reasoning:` line; map `xhigh`/`max` to `high` and `none`/`minimal` to `low`. Whether manual "think step by step" scaffolding still helps alongside the analysis channel is not documented (unverified). Image/audio inputs and very long contexts (> 131K) must be solved differently.
- **Availability**: primarily open weights (download via Hugging Face, linked from the model page). The OpenAI API rate-limit table shows **0 RPM / 0 TPM** for Build, Launch and Grow — do not assume production use via the OpenAI API.
- **AWAY FROM gpt-oss**: remove Harmony tokens, channel parsing and CoT-stripping logic; move developer instructions back into the system prompt or the instruction role of the target provider; translate the `Reasoning:` line into the target's effort/thinking parameter; rewrite `namespace functions` declarations into JSON-schema tools; replace `# Response Formats` with native Structured Outputs; do not carry over the identity line "You are ChatGPT …".

## Sources
- https://developers.openai.com/api/docs/models/gpt-oss-120b — "Most powerful open-weight model, fits into an H100 GPU", Apache 2.0, 117B / 5.1B active, 131,072 context and output, cutoff 1 Jun 2024, effort low/medium/high, text→text, endpoints Responses + Batch, features/tools, rate limits 0 RPM / 0 TPM, snapshot, no deprecation notice, Hugging Face download.
- https://developers.openai.com/api/docs/models/gpt-oss-20b — "Medium-sized open-weight model for low latency", 21B / 3.6B active, same limits, effort levels, endpoints and rate limits as 120b.
- https://developers.openai.com/cookbook/articles/openai-harmony — Harmony requirement, role precedence, contents of system and developer messages, `Reasoning: high`, default medium, channels final/analysis/commentary, CoT not to be shown and dropped in the following turn (tool exception), `namespace functions`, `<|constrain|>`, response formats without guarantee, built-in tools, stop tokens.
- https://developers.openai.com/cookbook/articles/gpt-oss/run-transformers — chat template renders Harmony, "`Developer` role in Harmony maps to the `system` prompt in the chat template", VRAM requirements (20b approx. 16 GB MXFP4, 120b ≥ 60 GB / one H100).
