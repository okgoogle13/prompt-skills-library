---
model: gemini-4-neon
vendor: Google
family: Gemini
aliases: [neon, gemini-neon, gemini4-neon, 4-neon, neon-4]
last_verified: 2026-11-19
status: current
tier: active
profile: Repo-level debugging and multi-file refactoring; paid tier only; xhigh overthinks simple prompts.
---

# Gemini 4 Neon

## Reasoning / Thinking
- Type: **native dynamic reasoning, always active**. Depth controllable exclusively via `thinking_level` (`low | medium | high | xhigh`), **default `high`**. `minimal` is not supported and returns an error.
- `thinking_budget` (token budget), as with all Gemini 4 models, is no longer supported and must not be passed. The levels are relative allowances for reasoning depth, not strict token guarantees.
- Level choice per the Google / AI Studio docs:
  - `low`: Fewest tokens and lowest latency; suited to cost- and latency-sensitive workloads such as fast chat and high-throughput processing, while still capable on agentic tasks.
  - `medium`: Lower token use and faster responses for interactive coding, live UI prototyping, responsive chat, and latency-sensitive tool calls.
  - `high` (default): Balanced intelligence and speed; Google's recommended default for most tasks, including complex coding, agentic execution, tool calling, and multimodal knowledge work.
  - `xhigh`: Maximum reasoning depth and most tokens; reserve for hard, multi-step engineering, analytical, and scientific problems where `high` falls short and higher latency/token spend are acceptable. Using `xhigh` on simpler prompts (such as text or JSON extraction) can cause overthinking or exhaust `max_output_tokens`.
- **`max_output_tokens` as a hard ceiling**: `max_output_tokens` caps the **sum** of generated thinking tokens and final output tokens without changing how `thinking_level` allocates reasoning. If the model hits the cap while thinking, it stops with status `incomplete` and returns truncated or empty output (while still billing generated thinking tokens). Keep the default **65,536** (or omit `max_output_tokens`) for standard tasks, and raise it rather than capping low (to reduce cost or latency, lower `thinking_level`).
- **Long decode**: Synchronous foreground calls (both streaming and non-streaming) support up to **65,536** tokens per hop. For outputs beyond 64K up to **1,048,576** tokens (minus input tokens), set `background: true` and `max_output_tokens > 65536` (Google recommends `131,072` or `262,144` starting points) so servers continue in 64K-token hops, or use client-side continuation (`previous_interaction_id` + `continuation_token`). Note: setting `background: true` without `max_output_tokens > 65536` stops at 65,536 tokens.
- **Thought signatures and state management**: Encrypted reasoning continuity across turns. The recommended default is server-side state via `previous_interaction_id` on the Interactions API (`store=true`). For stateless `generateContent` histories, pass all prior model turns and thought blocks/signatures unchanged; never copy a thought signature across parallel `functionCall` parts.
- Billing: every processed token is billed, including thinking tokens and internal tool system instructions and function declarations when using grounding ($3.00 input / $15.00 output per 1M tokens).

## Prompting style
- **Direct, precise and lean**: State goals clearly and concisely without unnecessary persuasive filler or manual chain-of-thought scaffolding ("Think step by step"); native reasoning handles internal planning automatically. Use consistent delimiters (XML-style tags or Markdown headings) and place critical constraints and output requirements in system instructions or at the start of the prompt.
- **Default tone**: Direct and efficient by default; explicitly request conversational or detailed didactic output if needed (documented for Gemini reasoning models; exact Neon-specific phrasing `(unverified)`).
- **Long-context and implicit-cache structure**: Place large shared system instructions, tool definitions, and reference documents at the **beginning** of the prompt and the concrete query or task at the **end** (introduced with a transition such as `"Based on the information above..."`) to preserve instruction priority and maximise implicit cache hits (minimum 4,096 tokens, 95% discount).
- **No sampling parameters**: Remove `temperature`, `top_p`, and `top_k` completely from requests. In-range custom values are ignored with deprecation headers; out-of-range values return a `400` validation error.
- **No assistant prefill / use native tools & schemas**: Remove prefilled model turns. Declare tools natively via function calling instead of instructing the model in system text to emit custom raw-text JSON tool calls with zero declared tools (which can trigger `MALFORMED_FUNCTION_CALL`), and constrain JSON output via Structured Outputs (`response_schema`).
- **Agentic discipline**: Built for multi-step coding and tool workflows with reduced redundant file reads, reliable context compaction, and low fabrication; define clear acceptance criteria, tool boundaries, and stop conditions.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Sits between `gemini-4-hydrogen` and `gemini-4-carbon`, adapted from `gemini-4-carbon`: delivers frontier-level reasoning with faster end-to-end task completion and leaner token usage (32% lower cost per task than Carbon at default `high`, per Antigravity testing), GA since 18 Nov 2026.
  - Strong benchmark performance (Nov 2026): #3 overall on Artificial Analysis Intelligence Index v5.0.1 (61 at `xhigh`), #1 on Artificial Analysis Coding Agent Index (58.6) and Zapier AutomationBench (56.3%), plus strong results on CursorBench 4.1 (65.4%), Terminal-bench 4.1 (65.2%), SEC-bench Pro (90.5%), CWE-Bench v2 (70.7%), and GraphWalks 256k–1M BFS (95.2%).
  - Well-suited to repo-level debugging and multi-file refactoring, dense multimodal knowledge work (legal, finance, spreadsheets, charts), STEM reasoning, defensive cybersecurity (dual-use offensive cyberdefense available to defenders via Google's Fairwind Program), and standalone or orchestrator-paired Antigravity workflows.
- **Weaknesses and quirks**:
  - **Paid tier only**: Not available on the Gemini API Free tier, nor on Antigravity Free or Google AI Plus plans (requires paid tier / Google AI Ultra, paid Google AI Pro or eligible device trials, or Gemini Enterprise).
  - **No explicit context caching**: `cachedContents` / `caches.create` is not supported. Automatic implicit caching applies from 4,096 tokens (95% discount); in multi-turn agent loops, the full previous request is cached only when the new turn adds at least 2,050 tokens.
  - **Antigravity IDE/App context cap**: While the Gemini API provides a 1,048,576-token unified context window, Google Antigravity lists Neon's context window as up to 512K tokens.
  - **Latency on hard prompts / `xhigh`**: Hard prompts can take several minutes; use `background: true` or raise HTTP client read timeouts to 15–20 minutes.
  - **Missing output modalities**: No native image generation, no audio generation, no Live API (WebSockets).
  - **Knowledge cutoff**: March 2026 (some specialist domains may be less up to date). Supply time-critical facts via Google Search grounding or context.

## Output & format conventions
- Unified context window: **1,048,576 tokens** in the Gemini API (shared across input, thinking, and output); up to **512K tokens** in Google Antigravity.
- Maximum output tokens: **65,536** synchronous per hop (both streaming and non-streaming); up to **1,048,576** tokens (minus input tokens) in long-decode mode (`background: true` or client-side continuation).
- Input modalities: text, image, video (with agentic video understanding), audio, PDF, and Microsoft Office / OpenDocument files (Word, PowerPoint, Excel) with multimodal file processing and slicing. Output: text only.
- Supported features: Structured Outputs (`response_schema`), function calling, implicit context caching (from 4,096 tokens, 95% discount), code execution, Computer use, File search, Grounding with Google Search & Google Maps, URL context, Batch API (50% discount), Flex inference (50% discount), Priority inference.
- Prices (per 1M tokens in USD, flat across the 1M window, paid tier only, no introductory discount):
  - Standard: input **$3.00** (cached **$0.15**), output (including thinking tokens) **$15.00**.
  - Batch / Flex: input **$1.50** (cached **$0.075**), output **$7.50**.
  - Priority: input **$5.40** (cached **$0.27**), output **$27.00**.
  - Grounding with Google Search / Google Maps: 5,000 free requests/month shared across Gemini 3+, then $14 per 1,000 requests (Search capped at 1,500 requests/day).

## Migration notes
- **FROM gemini-4-neon**:
  - Map `thinking_level` (`low | medium | high | xhigh`) to the target model's reasoning parameter (for `gemini-4-carbon` / `gemini-4-argon`, cap `xhigh` at `high` and note default shifts from `high` to `medium`; for OpenAI / Claude models, map to `reasoning_effort` or `effort`/`budget_tokens`); if migrating to a non-reasoning model, reintroduce explicit step-by-step scaffolding.
  - Restore sampling parameters (`temperature`, `top_p`) only if required by the target model.
  - Convert server-side Interactions API state (`previous_interaction_id`) to client-side message history when moving off Google APIs, and drop thought-signature carry-over.
  - Scale down long-decode output expectations (>64K tokens) and Office/OpenDocument slicing assumptions to what the target model supports.
- **TO gemini-4-neon**:
  - Set model ID to `gemini-4-neon` on a **paid-tier** project (no free tier).
  - Configure `thinking_level` (`low | medium | high | xhigh`; default is `high`; raise `minimal` from Flash-Lite / Gemini 3 models to at least `low`).
  - Remove hardcoded low `max_output_tokens` caps (e.g. 8,192) and keep the **65,536** default (or use `background: true` with `max_output_tokens > 65536` for long decode); tune cost/latency via `thinking_level` instead.
  - Remove manual CoT scaffolding, `temperature`, `top_p`, `top_k`, `thinking_budget`, prefilled model turns, and explicit caching (`cachedContents` / `caches.create`).
  - Declare tools natively via function calling (never emulate tools via raw-text JSON instructions with zero declared tools) and enforce JSON formats with `response_schema`.
  - Switch multi-turn sessions to `previous_interaction_id` on the Interactions API (or resend prior thought blocks/signatures unchanged without duplicating them across parallel `functionCall` parts) and set client timeouts to 15–20 minutes for synchronous heavy runs.

## Sources
- https://aistudio.google.com/docs/models/gemini-4-neon — official model page: model ID `gemini-4-neon`, 1,048,576 unified context window, 65,536 synchronous / 1M long decode, modalities, capability matrix (no explicit caching, no image/audio generation, no Live API), GA November 2026.
- https://aistudio.google.com/docs/whats-new-gemini-4-neon — "What's new in Gemini 4 Neon": positioning between Hydrogen and Carbon, `thinking_level` (`low | medium | high | xhigh`, default `high`), long decode with `background=True`, paid-tier-only requirement, migration checklist (removing sampling params and explicit caching, declaring native tools to avoid `MALFORMED_FUNCTION_CALL`, thought signatures, 15-minute timeouts).
- https://aistudio.google.com/docs/pricing — official pricing: paid tier only, Standard ($3.00 input / $0.15 cached / $15.00 output incl. thinking tokens), Batch & Flex ($1.50 / $0.075 / $7.50), Priority ($5.40 / $0.27 / $27.00), grounding tool pricing.
- https://aistudio.google.com/docs/changelog — release notes (18 Nov 2026): GA of `gemini-4-neon` alongside multimodal Office/OpenDocument file processing and slicing; earlier notes on removed sampling parameters and prefilled model turns.
- https://deepmind.google/models/model-cards/gemini-4-neon/ — DeepMind model card (published 18 Nov 2026): adapted from `gemini-4-carbon`, March 2026 knowledge cutoff, benchmarks (AA Index v5.0.1 61, CursorBench 4.1 65.4%, SEC-bench Pro 90.5%, GraphWalks 95.2%), safety evaluations, and distribution channels.
- https://aistudio.google.com/docs/thinking — thinking guide: `thinking_level` comparison across Gemini 4 models, `max_output_tokens` hard-ceiling behaviour (`incomplete` status), 64K foreground cap across streaming/non-streaming for Neon, and thought signatures.
- https://aistudio.google.com/docs/long-decode — long decode guide: server-side continuation hops, ~5K-token streaming chunks after 64K, 15–20 minute read timeouts, and `max_output_tokens` starting recommendations.
- https://aistudio.google.com/docs/caching — context caching guide: implicit caching only on Gemini 4 (from 4,096 tokens, 95% discount, 2,050-token delta rule in multi-turn agent loops) and prefix placement advice.
- https://aistudio.google.com/docs/choosing-a-model — model comparison and upgrade path from `gemini-3.1-pro-preview` to `gemini-4-neon`.
- https://aistudio.google.com/docs/prompting-strategies — prompt design strategies: directness, consistent XML/Markdown delimiters, default concise output, long-context placement at prompt start, and removal of `temperature`/`top_p`/`top_k`.
- https://antigravity.google/docs/models/ — Antigravity model availability: `Gemini 4 Neon` context window up to 512K in Antigravity, `xhigh` CLI flag (`--model gemini-4-neon-xhigh`), plan eligibility.
- https://antigravity.google/blog/gemini-4-neon-in-google-antigravity — Antigravity launch post (18 Nov 2026): AA Coding Agent Index #1 (58.6), AutomationBench #1 (56.3%), 32% lower cost per task than Carbon at `high`.
