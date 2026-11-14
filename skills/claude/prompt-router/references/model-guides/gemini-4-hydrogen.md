---
model: gemini-4-hydrogen
vendor: Google
family: Gemini
aliases: [hydrogen, gemini-hydrogen, gemini4-hydrogen, 4-hydrogen, gemini-4-h2, gemini-hydrogen-4]
last_verified: 2026-11-13
status: current
---

# Gemini 4 Hydrogen

## Reasoning / Thinking
- Type: **native reasoning, always active**. Depth controllable exclusively via the string enum `thinking_level` (`low | medium | high | xhigh`), **default `high`** (optimised for code and agentic workflows).
- `minimal` is **not** supported for Gemini 4 Hydrogen and returns an error (`400 INVALID_ARGUMENT`) — paths from older Flash models (e.g. `gemini-3.6-flash`, `gemini-3.5-flash-lite`) that use `minimal` must be raised to `low`.
- `thinking_budget` (token budget), as with all Gemini 4 models, is no longer supported and must not be passed. The levels are relative allowances for reasoning depth, not strict token guarantees.
- Level choice per the Google / DeepMind docs:
  - `low`: Lowest latency (sub-6s response times) and minimal token usage; ideal for high-throughput tasks, fact retrieval, text analysis and light classification. For complex architecture or deep debugging, quality can drop.
  - `medium`: Balanced reasoning depth for advanced text processing, concept comparisons and non-critical code snippets.
  - `high` (default): Standard recommendation for everyday agentic workflows, repository navigation, software engineering and multi-step problem solving.
  - `xhigh`: Maximum reasoning depth through test-time compute scaling for especially hard multi-step problems, complex root-cause analyses, mathematical and scientific proofs and formal verification. Pushes benchmarks to frontier level, but needs noticeably more thinking and output tokens.
- **`max_output_tokens` as a hard ceiling**: `max_output_tokens` limits the **sum** of generated thinking tokens and actual output. If the value is set too low (e.g. < 32k), the model can use up the entire allowance in reasoning and cut the answer short. Google recommends at least 32,768 tokens (standard synchronous: 65,536).
- **Long decode**: For answers beyond 64k tokens, Gemini 4 Hydrogen supports long decode up to 1,048,576 tokens (minus input) via `background: true` and `max_output_tokens > 65536`. Continuation hops are orchestrated server-side; the text content of the `model_output` steps is concatenated.
- **Thought signatures and state management**: In multi-turn conversations and tool calls, the encrypted reasoning context is carried via thought signatures. The recommended default is server-side state management via `previous_interaction_id` of the Interactions API (`store=true`). For stateless requests, all generated thought blocks must be carried unchanged in the conversation history.
- Billing: the total of output and thinking tokens ($1.50 input / $7.50 output per 1M tokens).

## Prompting style
- **Direct, precise and lean**: "Be concise. Gemini responds best to direct, clear instructions." Elaborate prompt engineering for older non-reasoning models (such as manual "Think step by step" or nested CoT templates) leads, per the docs, to the model over-analysing ("over-analyze") and should be removed entirely.
- **Default tone is sober**: The model answers compactly and factually by default. If detailed, didactic or conversational answers are wanted, this style must be requested explicitly in the prompt.
- **Long-context structure**: For large amounts of data (documents, codebases, tables), put the reference data **at the start** and the concrete task or instruction at the **end, after the data block**, introduced by clear anchors ("Based on the preceding information...").
- **No sampling parameters**: Remove `temperature`, `top_p` and `top_k` completely from generation configs. They are ignored; manual settings below 1.0 can trigger looping on demanding reasoning and coding tasks.
- **No assistant prefill**: Remove prefilled model responses (`prefilled model turns`). Enforce structure and formatting via system instructions or `response_schema` (Structured Outputs) instead.
- **Workhorse in agentic loops**: Define clear goal contracts, maximum iteration limits and verifiable done criteria (e.g. "produce diff, run test suite, stop when green"), since Hydrogen acts ideally as a fast worker in iterative feedback loops.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Google's high-performance "workhorse" and execution model of the Gemini 4 generation: significantly faster and more responsive than older Flash models (such as `gemini-3.8-flash`), with outstanding reasoning strength at `high` and `xhigh`;
  - Excellent in fast feedback loops, when writing code patches, running terminal commands and iterative unit tests;
  - High reliability in function calling and tool use;
  - Unified 1M token context window with transparent pricing ($1.50 in / $7.50 out);
  - Ideal execution worker in multi-model architectures (e.g. under `gemini-4-argon` / Antigravity orchestrator).
- **Weaknesses and quirks**:
  - **No explicit context caching**: Traditional manual caching (`cachedContents` / `caches.create`) is no longer supported. Instead, automatic implicit caching applies (from 4,096 tokens) with a 95% discount on hits.
  - **Token usage at `xhigh`**: At the highest level `xhigh`, significantly more tokens can be used and latency can rise; for pure extraction or simple text tasks choose `thinking_level: "low"`.
  - **Missing output modalities**: No native image or audio generation, no Live API (WebSockets).
  - **Knowledge cutoff**: March 2026 (with individual domains back to January 2025). Time-critical data must be supplied via Google Search grounding or the context.

## Output & format conventions
- Unified context window: **1,048,576 tokens** (shared between input, thinking and output).
- Maximum output tokens: 65,536 synchronous; up to 1,048,576 tokens (minus input tokens) in asynchronous long-decode mode (`background: true`).
- Input modalities: text, image, video, audio, PDF. Output: text only.
- Supported features: Structured Outputs (`response_schema`), function calling, implicit caching (from 4k tokens, 95% discount), code execution, Google Search grounding, Maps grounding, URL Context, File Search, Batch API (50% discount), Flex and Priority inference.
- Function calling: every `FunctionResponse` must carry `call_id` and the exact `name`, with exactly one response per call.
- Prices (per 1M tokens): input $1.50 (cached $0.075), output $7.50 (incl. thinking tokens). No permanent free tier.

## Migration notes
- **FROM gemini-4-hydrogen**:
  - Map `thinking_level` to the target format (`reasoning_effort` for OpenAI o3/GPT-5, `budget_tokens` or adaptive `effort` for Claude Sonnet/Opus); if the target model has no native reasoning, add explicit chain-of-thought scaffolding ("Step by step") back into the prompt.
  - Put sampling parameters (`temperature`, `top_p`) back into the generation config.
  - Resolve server-side session state (`previous_interaction_id`) and manage conversation history client-side.
  - Scale back long-decode assumptions above 64k output tokens to the output limits of the target model.
- **TO gemini-4-hydrogen**:
  - Set model ID to `gemini-4-hydrogen`.
  - Configure `thinking_level` (`low | medium | high | xhigh`; default is `high`; raise `minimal` from older models mandatorily to `low`).
  - Check `max_output_tokens` and raise it to at least 32,768 (or keep the default 65,536), so reasoning does not truncate the actual output.
  - Remove manual CoT instructions ("Think step by step", "Reflect in detail") and verbose scaffolding from the prompt, and choose `thinking_level: "high"` or `"xhigh"` instead.
  - Remove explicit caching (`caches.create`) from the code — implicit caching applies automatically from 4,096 tokens.
  - Remove `temperature`, `top_p`, `top_k`, `thinking_budget` and `candidate_count` completely from requests.
  - Switch multi-turn interactions and function calling to `previous_interaction_id` of the Interactions API, or carry thought signatures through unchanged.
  - Define verbosity and tone explicitly when migrating from more conversational models.

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-4-hydrogen — official model card: model ID `gemini-4-hydrogen`, unified 1M token context window, 64k standard / 1M long decode, modalities, feature matrix, GA status November 2026.
- https://ai.google.dev/gemini-api/docs/latest-model — "What's new in Gemini 4 Hydrogen": positioning as high-throughput workhorse, thinking levels (`low`, `medium`, `high`, `xhigh`), removal of `temperature`/`top_p`/`top_k` and `thinking_budget`, default `thinking_level: high`.
- https://ai.google.dev/gemini-api/docs/pricing — official pricing: flat rate $1.50 input ($0.075 cached input), $7.50 output (incl. thinking tokens), batch API 50% discount.
- https://deepmind.google/models/model-cards/gemini-4-hydrogen/ — DeepMind model card: evaluation for fast software engineering, agentic multi-step workflows, Artificial Analysis Intelligence Index (~51 on `high`, ~54 on `xhigh`), knowledge cutoff March 2026.
- https://ai.google.dev/gemini-api/docs/thinking — official documentation on the reasoning system: thinking levels (`low`, `medium`, `high`, `xhigh`), thought signatures, billing of thinking tokens and behaviour with `max_output_tokens`.

