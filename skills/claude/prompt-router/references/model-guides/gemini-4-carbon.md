---
model: gemini-4-carbon
vendor: Google
family: Gemini
aliases: [carbon, gemini-carbon, gemini4-carbon, 4-carbon, carbon-4]
last_verified: 2026-11-13
status: current
---

# Gemini 4 Carbon

> ⚠ Note: Gemini 4 Carbon (`gemini-4-carbon`) is Google's most capable frontier reasoning model for extreme reasoning depth, long-lived autonomous agents, complex software architecture, high-precision cybersecurity (vulnerability lifecycle) and scientific proof. Compared with `gemini-4-argon`, Carbon invests significantly more test-time compute and verification steps per turn, to drastically minimise errors on demanding problems.

## Available interfaces & platforms
Gemini 4 Carbon is available through the following official interfaces and developer environments:
1. **Google AI Studio (web UI & developer console)**:
   - Directly in the web interface (`aistudio.google.com`) for prompt prototyping, system-instruction design and multimodal tests (PDF, code, audio, video up to 1M tokens).
   - Control of reasoning depth via the `thinking_level` dropdown (`low`, `medium`, `high`).
   - Generation of API keys for the paid tier (pay-as-you-go).
2. **Gemini API & Google GenAI SDK (`google-genai`)**:
   - Standard REST API and official SDKs (Python, Node.js, Go, Java) using the model ID `gemini-4-carbon`.
   - **Interactions API**: supports stateful sessions via `previous_interaction_id` (`store=true`) and asynchronous long decode up to 1M tokens with `background: true`.
3. **Google Antigravity (agent IDE & swarm orchestrator)**:
   - Integrated as the primary architect and review model for multi-agent workflows (`/swarm`, Antigravity orchestrator).
   - Used for overarching system architecture, plan approvals (`plan.md`) and safety-critical code audits, while execution subagents (typically `gemini-4-hydrogen`) handle operational edits.
4. **Google Cloud / Vertex AI**:
   - Enterprise Model Garden and Vertex AI Studio for enterprise customers with private VPC connectivity, IAM governance, SLA guarantees and regional data residency.
5. **Google Workspace & Gemini for Business / Google AI Ultra**:
   - Available to Google AI Ultra subscribers in the Gemini web and mobile app, in Google Workspace (Docs, Sheets, Drive) and in the AI Mode of Google Search.
6. **IDE extensions & Android Studio**:
   - Integrated into Android Studio and modern IDE assistants for in-depth code refactorings, thread-safety analyses and memory-leak diagnostics.

## Reasoning / Thinking
- Type: **native reasoning with extended verification, always active**. Depth controllable exclusively via the string enum `thinking_level` (`low | medium | high`), **default `medium`**. `minimal` is not supported and throws an error (`400 INVALID_ARGUMENT`).
- `thinking_budget` (token budget) is no longer supported and must not be passed. The levels are relative allowances; Carbon uses significantly more thought tokens per level than Argon or Hydrogen, to weigh alternatives and formally verify code paths.
- Recommended level choice:
  - `low`: Faster processing and lower token costs; suited to structured extraction, comparative analyses and lighter programming tasks.
  - `medium` (default): Balanced depth for demanding software engineering, complex API integrations and multi-step logic.
  - `high`: Maximum reasoning depth for cryptographic analyses, deep root-cause debugging (race conditions, memory leaks), zero-day vulnerability audits (SEC-bench) and mathematical proof.
- **`max_output_tokens` as a hard ceiling**: Limits the **sum** of thinking tokens and actual text output. Since Carbon reasons very thoroughly, `max_output_tokens` must be set to at least **32,768**, ideally **65,536** tokens (standard synchronous limit), to prevent the answer from being cut short.
- **Long decode**: For very large outputs beyond 64k tokens, Carbon supports long decode up to 1,048,576 tokens (minus input) via `background: true` and `max_output_tokens > 65536`.
- **Thought signatures**: Encrypted representation of the reasoning state; for multi-turn and function calling, manage it server-side via `previous_interaction_id` or carry it unchanged in `contents` when stateless.
- Billing: the total of output and thinking tokens is charged ($2.00 or $4.00 input / $10.00 or $20.00 output per 1M tokens).

## Prompting style
- **Direct, precise and goal-oriented**: "Be concise. Gemini responds best to direct, clear instructions." Manual chain-of-thought instructions ("Think step by step", pseudo-scratchpads) are counterproductive and cause needless latency or over-analysis, because the model autonomously runs deep verification loops.
- **Define strict specifications and contracts**: Carbon excels when given formal constraints, invariants, type definitions and acceptance criteria.
- **Default tone is analytical and factual**: Answers are compact by default and focused on solving the problem. Detailed didactic explanations must be requested explicitly.
- **Long-context structure**: Reference data (codebases, logs, schemas) at the **start**; concrete task and check criteria at the **end, after the data block**.
- **No sampling parameters**: Remove `temperature`, `top_p` and `top_k` completely from generation configs (they are ignored, or values below 1.0 cause looping in mathematical proofs).
- **No assistant prefill**: Remove prefilled model responses; set structure via `response_schema` (Structured Outputs) or system instructions.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - **Leader on maximum reasoning depth**: Outperforms `gemini-4-argon` and all previous models on demanding benchmarks (Artificial Analysis Intelligence Index, Terminal-Bench, HLE);
  - **Cybersecurity & vulnerability lifecycle**: Excellent results in automated vulnerability search (CWE-bench, SEC-bench Pro) and root-cause patching;
  - **Robust architecture planning**: Ideal as the central strategist in multi-agent systems (Antigravity `/swarm`), since it oversees complex dependencies without error;
  - Unified 1M token context window with automatic implicit caching (95% discount from 4,096 tokens).
- **Weaknesses and quirks**:
  - **Higher latency and token usage**: Through intensive internal verification, Carbon needs more time and generates more thinking tokens than Argon; for routine coding or simple text tasks, `gemini-4-hydrogen` or `gemini-4-argon` is far more economical;
  - **No explicit caching any more**: Manual cache creation (`caches.create`) has been superseded;
  - **No image or audio output**: Input is multimodal (text, image, audio, video, PDF), output is text only;
  - **Knowledge cutoff**: March 2026 (January 2025 for specialist domains); bring in up-to-date facts via Google Search grounding.

## Output & format conventions
- Context window: **1,048,576 tokens** (shared between input, thinking and output).
- Maximum output tokens: 65,536 synchronous; up to 1,048,576 tokens in long-decode mode (`background: true`).
- Input: text, image, video, audio, PDF. Output: text only.
- Features: Structured Outputs (`response_schema`), function calling (with `call_id` and `name`), implicit caching (95% discount from 4k tokens), code execution, Google Search grounding, Maps grounding, URL Context, Batch API (50% discount), Flex and Priority inference.
- Prices (per 1M tokens):
  - Until 30 Nov 2026 (introductory price): input $2.00 (cached $0.10), output $10.00.
  - From 1 Dec 2026 (regular): input $4.00 (cached $0.20), output $20.00.
  - No permanent free tier.

## Migration notes
- **FROM gemini-4-carbon**:
  - Map `thinking_level` into the target format (`reasoning_effort` for OpenAI o3/GPT-5, `budget_tokens` or adaptive `effort` for Claude Opus/Sonnet);
  - When switching to models without native reasoning, add manual CoT templates ("Step by step") back in;
  - Put sampling parameters (`temperature`, `top_p`) back into the request configuration;
  - Resolve server-side session state (`previous_interaction_id`) and keep the history client-side;
  - Scale back long-decode assumptions above 64k tokens to the limits of the target model.
- **TO gemini-4-carbon**:
  - Set model ID to `gemini-4-carbon`.
  - Configure `thinking_level` (`low | medium | high`; default is `medium`; raise `minimal` mandatorily to `low`).
  - Raise `max_output_tokens` to at least 32,768 (better 65,536), since Carbon's deep reasoning phase would otherwise cut off the actual output.
  - Remove manual CoT instructions ("Think step by step") completely.
  - Remove `temperature`, `top_p`, `top_k`, `thinking_budget` and `candidate_count`.
  - Delete explicit caching (`caches.create`) — implicit caching applies automatically from 4,096 tokens.
  - Switch multi-turn interactions to `previous_interaction_id` of the Interactions API, or pass thought signatures through unchanged.

## Sources
- https://aistudio.google.com/learn/gemini-4-carbon-developer-guide — official developer guide in Google AI Studio: model specifications, available interfaces (AI Studio, Gemini API, Antigravity, Vertex AI, Workspace/Ultra), thinking levels, long decode and best practices.
- https://ai.google.dev/gemini-api/docs/models/gemini-4-carbon — official model card for Gemini 4 Carbon: unified 1M token context, 64k standard / 1M long decode, modalities, feature matrix.
- https://deepmind.google/models/model-cards/gemini-4-carbon/ — DeepMind model card: top scores in software engineering, cybersecurity audits (SEC-bench, CWE-bench), autonomous multi-step reasoning and extended test-time verification.
- https://ai.google.dev/gemini-api/docs/pricing — official price tiers: introductory prices until 30 Nov 2026 ($2.00 in / $10.00 out), regular prices from 1 Dec 2026 ($4.00 in / $20.00 out).
- https://ai.google.dev/gemini-api/docs/thinking — official documentation on the reasoning system: thinking levels (`low`, `medium`, `high`), thought signatures and behaviour with `max_output_tokens`.

