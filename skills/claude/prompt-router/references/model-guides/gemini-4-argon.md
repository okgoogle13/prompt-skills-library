---
model: gemini-4-argon
vendor: Google
family: Gemini
aliases: [gemini-4, argon, gemini-argon, gemini4, gemini4-argon, 4-argon, argan]
last_verified: 2026-11-05
status: current
---

# Gemini 4 Argon

## Reasoning / Thinking
- Type: **native reasoning, always active**. Depth controllable exclusively via the string enum `thinking_level` (`low | medium | high`), **default `medium`**. `minimal` is not supported and throws an error.
- `thinking_budget` (token budget) is no longer supported on Gemini 4 Argon and must not be passed. The levels are relative allowances for reasoning depth, not strict token guarantees.
- Recommended level choice per the docs:
  - `low`: Lowest latency and token usage; suited to simpler tasks, text analysis and light research. For hard coding or reasoning tasks, quality can drop.
  - `medium` (default): Balanced; standard recommendation for almost all production workloads, including complex software engineering and agentic pipelines.
  - `high`: Maximum reasoning depth for difficult mathematics, natural sciences, complex architecture refactorings and autonomous multi-step agents.
- **`max_output_tokens` as a hard ceiling**: `max_output_tokens` limits the **sum** of generated thinking tokens and actual output. If the value is set too low (e.g. < 32k), the model can use up the entire allowance in reasoning and cut the answer short. Google recommends at least 32,768 tokens (standard synchronous: 65,536).
- **Long decode**: For answers beyond 64k tokens, Gemini 4 Argon supports long decode up to 1,048,576 tokens (minus input). This requires `background: true` and `max_output_tokens > 65536`. Continuation hops (in steps of up to 64k) are orchestrated server-side; in the Interaction object the text content of all `model_output` steps must be concatenated.
- **Thought signatures and state management**: In multi-turn conversations and tool calls, the encrypted reasoning context is carried via thought signatures. The recommended default is server-side state management via `previous_interaction_id` of the Interactions API (`store=true`). For stateless requests, all generated thought blocks must be carried unchanged in the conversation history.
- Billing: the total of output and thinking tokens is charged ($10 or $20 per 1M tokens, depending on the price period).

## Prompting style
- **Direct, precise and lean**: "Be concise. Gemini responds best to direct, clear instructions." Elaborate prompt engineering for older non-reasoning models (such as manual "Think step by step" or nested CoT templates) causes, per the docs, the model to "over-analyze" and should be removed entirely.
- **Default tone is sober**: The model answers compactly and factually by default. If detailed, didactic or conversational answers are wanted, this style must be requested explicitly in the prompt.
- **Long-context structure**: For large amounts of data (documents, codebases, tables), put the reference data **at the start** and the concrete task or instruction at the **end, after the data block**, introduced by clear anchors ("Based on the preceding information...").
- **No sampling parameters**: Remove `temperature`, `top_p` and `top_k` completely from the generation configs. If passed, the API ignores them; manual settings below 1.0 can trigger looping on demanding reasoning and maths tasks.
- **No assistant prefill**: Remove prefilled model responses (`prefilled model turns`). Instead enforce structure and formatting via system instructions or `response_schema` (Structured Outputs).
- **Agentic scope**: For complex or open-ended tasks, define clear stop criteria, maximum iteration limits and room for action, to avoid uncontrolled further iteration in reasoning.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**: Google's flagship reasoning model for high-end software development, autonomous multi-step agents, in-depth mathematical and scientific problem solving, and demanding enterprise knowledge work (financial analysis, legal drafting). General availability (GA) since 13 Oct 2026. Offers long decode up to 1M output tokens, agentic video understanding (dynamic frame analysis) and native integration into Antigravity managed agents.
- **Weaknesses and quirks**:
  - **No explicit context caching**: The traditional explicit caching (`cachedContents` / `caches.create`) is no longer supported. Instead, automatic implicit caching applies (from 4,096 tokens) with a 95% discount on hits.
  - **Latency with deep reasoning**: Complex reasoning at level `high` or long-decode tasks can take several minutes. HTTP client timeouts must be raised to at least 15 minutes, or `background: true` must be used.
  - **High token usage**: Long reasoning can produce significantly more tokens than Flash models; for simple extraction and classification tasks, `gemini-3.8-flash` or `thinking_level: "low"` is more economical.
  - **Missing modalities**: No native image generation, no audio generation, no Live API (WebSockets).
  - **Knowledge cutoff**: March 2026 (with individual domains back to January 2025). Time-critical data must be supplied via Google Search grounding or the context.

## Output & format conventions
- Unified context window: **1,048,576 tokens** (shared between input, thinking and output).
- Maximum output tokens: 65,536 synchronous; up to 1,048,576 tokens (minus input tokens) in asynchronous long-decode mode (`background: true`).
- Input modalities: text, image, video (with agentic video understanding), audio, PDF. Output: text only.
- Supported features: Structured Outputs (also in combination with built-in tools such as Google Search, Maps grounding, URL Context and code execution), function calling, implicit caching (from 4k tokens, 95% discount), Batch API (50% discount), Computer Use, File Search, Flex and Priority inference.
- Prices (per 1M tokens):
  - Until 30 Nov 2026 (introductory price): input $2.00 (cached $0.10), output $10.00.
  - From 1 Dec 2026 (regular): input $4.00 (cached $0.20), output $20.00.
  - No free tier available.

## Migration notes
- **FROM gemini-4-argon**:
  - Map `thinking_level` to the effort or budget parameter of the target model (`reasoning_effort` for OpenAI o3/GPT-5, `budget_tokens` or adaptive `effort` for Claude Sonnet/Opus); if the target model has no native reasoning, add explicit chain-of-thought scaffolding ("Step by step") back into the prompt.
  - Put sampling parameters (`temperature`, `top_p`) back into the request config.
  - Resolve server-side session state (`previous_interaction_id`) and manage the conversation history client-side.
  - Scale back long-decode assumptions above 64k output tokens to the output limits of the target model (often 4k, 8k, 16k or 64k).
  - Switch automatic caching to the provider-specific caching API (e.g. Anthropic cache-control headers).
- **TO gemini-4-argon**:
  - Set model ID to `gemini-4-argon`.
  - Configure `thinking_level` (`low | medium | high`; default is `medium`; raise `minimal` from older Flash models to `low` mandatorily).
  - Check `max_output_tokens` and raise it to at least 32,768 (or keep the default 65,536), so reasoning does not truncate the actual output; for extremely long outputs use `background: true` with values > 65,536.
  - Remove manual CoT instructions ("Think step by step", "Reflect in detail") and verbose scaffolding from the prompt, and choose `thinking_level: "high"` instead.
  - Remove explicit caching (`caches.create`) from the code — implicit caching applies automatically from 4,096 tokens.
  - Remove `temperature`, `top_p`, `top_k`, `candidate_count` and prefill turns completely from requests.
  - Raise client timeouts to at least 15 minutes or use asynchronous background execution.
  - Switch multi-turn interactions and function calling to `previous_interaction_id` of the Interactions API.
  - Define verbosity and style explicitly when migrating from more conversational models.

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — official model card: model ID gemini-4-argon, unified 1M token context window, 64k standard / 1M long decode, modalities, feature matrix, GA status October 2026.
- https://ai.google.dev/gemini-api/docs/latest-model — "What's new in Gemini 4 Argon": positioning as flagship reasoning model, migration checklist (removing temperature/top_p/top_k, raising max_output_tokens to at least 32k, replacing explicit caching with implicit 95%-discount caching, previous_interaction_id), long-decode architecture via background=True, default thinking_level medium.
- https://ai.google.dev/gemini-api/docs/pricing — official price tiers: introductory prices until 30 Nov 2026 ($2.00 input, $0.10 cached input, $10.00 output incl. thinking tokens), regular prices from 1 Dec 2026 ($4.00 in / $0.20 cached / $20.00 out), no free tier.
- https://ai.google.dev/gemini-api/docs/changelog — release notes of 13 Oct 2026: general availability (GA) of Gemini 4 Argon (gemini-4-argon).
- https://deepmind.google/models/model-cards/gemini-4-argon/ — DeepMind model card: evaluation for complex software development, agentic multi-step workflows, mathematics, natural sciences, knowledge cutoff March 2026 (January 2025 for specialist domains) and documented latency/token characteristics.
- https://ai.google.dev/gemini-api/docs/thinking — official documentation on the reasoning system: thinking levels (low, medium, high), thought signatures, billing of thinking tokens and behaviour with max_output_tokens.
- https://ai.google.dev/gemini-api/docs/long-decode — official guide to long decode: generation of up to 1M tokens via server-side continuation hops with background=true.

