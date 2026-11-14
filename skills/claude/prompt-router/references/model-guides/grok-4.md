---
model: grok-4
vendor: xAI
family: Grok
aliases: [grok4, grok-4-latest, grok-4-0709, xai.grok-4]
last_verified: 2026-10-13
status: legacy
successor: grok-4.3
---

# Grok 4

## Reasoning / Thinking
- **Type: reasoning model with no off switch.** xAI lists `grok-4-0709` in the retirement table among the reasoning models (routing to `grok-4.3` with `low`, not with `none`), OCI states "Has Reasoning: Yes". No official source documents a switch to turn it off; that there is no non-reasoning mode at all is beyond that (unverified — secondary source only; the xAI model pages for grok-4 are offline).
- **Depth control: not parameterisable.** The original `grok-4` does **not** support `reasoning_effort`. If the parameter is sent via the API, the model returns an error response. (Note: `reasoning_effort` is documented by xAI for other models — per OCI for Grok 3 mini, per the model page for `grok-4.3` (`none`…`xhigh`, default `low`), per the reasoning page for `grok-4.5`/`grok-4.6`/`grok-4.7`; for `grok-4.20` no `reasoning_effort` is documented — and not for `grok-4`.)
- **Practical depth control:** since no effort switch exists, reasoning depth is controlled indirectly via the output budget — for demanding reasoning tasks raise the `max_tokens`/maximum output limit so there is enough room for internal thinking tokens.
- **Thinking traces not retrievable:** that Grok 4 does not disclose its internal reasoning and returns no separate `reasoning_content`/chain-of-thought field is (unverified — secondary source only; the xAI model pages for grok-4 are offline).

## Prompting style
- **Tool-augmented reasoning is native.** Grok 4 was trained via reinforcement learning to use tools while reasoning — including a code interpreter and web browsing — and to formulate its own search queries autonomously. Prompts should therefore clearly say *which* tools/sources it may use, rather than prescribing every intermediate step.
- **Live search is opt-in, not automatic.** Web search runs via the tools parameter (e.g. `tools=[web_search()]` in the xAI SDK or `{"type": "web_search"}` in the Responses API). Without an enabled search tool Grok has no access to current events, per the model overview.
- **Feature set:** function calling and structured outputs are supported; multimodal input of text and images (output: text).
- **System prompt quirks:** specific statements from xAI about system prompt fidelity or instruction following *for grok-4 specifically* are not available from primary sources (unverified). xAI only explicitly highlights "strict prompt adherence" and the lowest hallucination rate for Grok 4.20, and strong instruction following for Grok 4.3 — not retroactively for grok-4.

## Strengths & weaknesses (prompt-relevant)
- **Strengths:** strong multi-step reasoning, multimodal understanding and access to current information (via tool/web integration); agentic use possible, since the model autonomously uses code interpreter and browser. Trained on verifiable data across many domains.
- **Weaknesses / limitations (prompt-relevant):**
  - No fine control over reasoning depth (`reasoning_effort` unavailable) — less control over latency vs. thoroughness than with grok-4.3 and the 4.5+ models.
  - No documented reasoning trace → harder to debug (unverified, see above).
  - `presence_penalty`, `frequency_penalty` and `stop` are not usable with xAI reasoning models — so do not plan on them for output control with grok-4.
  - Knowledge cutoff November 2024; for newer facts the search tool is required.

## Output & format conventions
- Returns the final answer; request structured output via Structured Outputs (JSON schema) rather than manually parsed free-text formats.
- Format requirements (table, JSON, length) belong explicitly in the prompt; to limit response length use `max_tokens`, since `stop` sequences are not available.
- **Context window:** per xAI's announcement the Grok 4 API offers **256,000 tokens** (text + images). On third-party platforms the usable window is sometimes lower — Oracle OCI lists "128,000 tokens" for `xai.grok-4`; that is a platform-specific limit.

## Migration notes
- **Retired (xAI API):** `grok-4-0709` was withdrawn on 15 May 2026, 12:00 PT; the slug still resolves, and since then xAI automatically serves requests to it with `grok-4.3` at `reasoning_effort: low` (billed at grok-4.3 prices) — an unchanged grok-4 prompt therefore already runs on shallower reasoning. 15 Aug 2026 is only the retirement date on Oracle OCI (`xai.grok-4`).
- **AWAY FROM Grok 4 (xAI recommendation: grok-4.3; alternatively Grok 4.20):**
  - grok-4.3: `none`/`low`/`medium`/`high` (default `low` per the model page); no `reasoning_effort` is documented for grok-4.20. If deeper reasoning is needed, set `medium`/`high` explicitly rather than accepting the routed `low`.
  - Much larger context window available (grok-4.3 and grok-4.20: 1,000,000 tokens).
  - xAI promotes strict prompt adherence and low hallucination rates for Grok 4.20 → existing defensively worded prompts can often be trimmed.
  - For code and chat xAI now recommends grok-4.7 (500k context, no `none`, default `high`).
- **TO Grok 4 (from a non-reasoning or older Grok model):**
  - No longer possible on the xAI API — requests land on grok-4.3 (see above); on OCI retired since 15 Aug 2026 as well. The following points apply only to any remaining deployments on other platforms (unverified).
  - Model always thinks — make no assumption that an effort/thinking switch can be set; `reasoning_effort` causes an error and must be removed from requests.
  - Remove `presence_penalty`/`frequency_penalty`/`stop` from existing requests (not allowed on reasoning models).
  - For live web access, explicitly enable the search tool; do not rely on automatic browsing.
  - Prompts can become shorter and more goal-oriented (goal instead of step-by-step micromanagement), since the model handles tool selection and search queries itself.

## Sources
- https://x.ai/news/grok-4 — official Grok 4 announcement (9 Jul 2025): RL training for tool use (code interpreter, web browsing, own search queries), verifiable training data across many domains, Grok 4 API with "a 256,000 context window" and multimodal understanding.
- https://docs.x.ai/developers/migration/may-15-retirement — Retirement of `grok-4-0709` on 15 May 2026 12:00 PT, slug still resolves, routing to `grok-4.3` with `low`, billing at grok-4.3 prices, grok-4.3 recommended for reasoning workloads.
- https://docs.x.ai/developers/model-capabilities/text/reasoning — `reasoning_effort` documented for grok-4.7/4.6/4.5 (not for grok-4); errors for `presencePenalty`/`frequencyPenalty`/`stop` on reasoning models.
- https://docs.x.ai/developers/tools/web-search — Web search via the `web_search` tool (xAI SDK and Responses API).
- https://docs.x.ai/developers/models — current roster without grok-4; no real-time knowledge without enabled search tools; recommendation grok-4.7 for code and chat.
- https://docs.x.ai/developers/models/grok-4.3 — Efforts `none`–`xhigh`, default `low`, 1M context, "strong tool calling and instruction following".
- https://docs.x.ai/developers/models/grok-4.20-0309-reasoning — 1M context, no effort levels listed, "the lowest hallucination rate on the market with strict prompt adherence".
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/xai-grok-4.htm — Oracle OCI docs: reasoning yes, `reasoning_effort` not supported (error when passed; present for Grok 3 mini), increase output limit for reasoning, function calling + structured outputs, knowledge cutoff November 2024, platform-side 128k, deprecation 15 May 2026 / retirement 15 Aug 2026.
