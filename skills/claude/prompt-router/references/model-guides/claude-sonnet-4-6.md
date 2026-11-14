---
model: claude-sonnet-4-6
vendor: Anthropic
family: Claude
aliases: [sonnet-4.6, claude-sonnet-4.6, sonnet4.6, sonnet-4-6]
last_verified: 2026-10-13
status: legacy
successor: claude-sonnet-5-5
---

# Claude Sonnet 4.6

## Reasoning / Thinking
- Type: **adaptive, but off by default** — a request without a `thinking` field runs without thinking; switch it on with `thinking: {type: "adaptive"}`. `{type: "enabled", budget_tokens: N}` is deprecated (do not use in new code; in legacy code only as a transitional token cap), `{type: "disabled"}` turns thinking off.
- Depth control via `output_config.effort`: `low | medium | high | max`, default `high`. `max` is supported, `xhigh` is not (in the Sonnet class only from Sonnet 5). Docs recommendation: set effort **explicitly** (otherwise unexpected latency), `medium` as the recommended default for most applications including agentic coding, `low` for chat and high-volume/latency-critical workloads.
- For chat/classification: `thinking: {type: "disabled"}` + `effort: "low"` gives comparable or better performance at low latency. (unverified)
- `thinking.display` defaults to `"summarized"` (readable summary; Sonnet 5/5.5: `"omitted"`).
- Sampling: restrictions apply only with thinking active — `temperature` and `top_k` are then incompatible, `top_p` only between 0.95 and 1; without thinking, non-default values are allowed (unlike from Sonnet 5 on, where they always return 400).
- Per-message effort and mid-conversation system messages do not exist on Sonnet 4.6; a change of effort via the top-level value restarts the prompt cache.

## Prompting style
- Claude 4.6 models are more proactive and can overtrigger on instructions that older models needed — soften thoroughness and tool-pressure phrasing ("If in doubt, use [tool]", "CRITICAL: You MUST use this tool …"); if behavior remains too aggressive, lower effort.
- At release: the best balance of speed and intelligence, good for high-volume production workloads. (unverified)
- Always read tool-call `input` with a JSON parser (escaping can differ), never with a raw-string match.

## Strengths & weaknesses (prompt-relevant)
- Strengths: 1M context window; fast, cost-efficient execution with strong instruction following. (unverified)
- Weaknesses/quirks: at higher `effort`, more exploration/tokens — `medium` is the default recommended by the docs; excessive tool/skill activation with overly aggressive prompts.

## Output & format conventions
- Assistant prefill (last assistant turn) returns 400 — use Structured Outputs (`output_config.format`) or a system prompt instruction.
- 1M context window, up to 128K output tokens (synchronous Messages API); Message Batches API up to 300K with beta header `output-300k-2026-03-24`; stream large outputs.
- `output_format` (top-level, deprecated) → `output_config.format`.
- Older tokenizer: Sonnet 5 and 5.5 produce roughly 30% more tokens for the same text. Images up to 1,568 px on the long edge or 1,568 tokens per image. Minimum cacheable prompt 1,024 tokens.
- Price per MTok: $3 input / $15 output, cache read $0.30. Reliable knowledge cutoff August 2025.

## Migration notes
- **AWAY FROM Sonnet 4.6**: to Opus for the hardest/longest tasks; to Haiku for pure speed/cost — Haiku 4.5 has no `effort` parameter (remove it there), Haiku 5.5 supports it. For the successor Sonnet 5.5: thinking runs there without a `thinking` field, `budget_tokens` and non-default sampling return 400, `display` defaults to `"omitted"`, token counts rise by ~30% (details in the Sonnet 5.5 guide).
- **MIGRATING TO Sonnet 4.6**: from Sonnet 4.5, set `effort` **explicitly** (4.6 defaults to `high` → otherwise higher latency/cost). `budget_tokens` → adaptive. Remove `interleaved-thinking-2025-05-14` (adaptive interleaves automatically), replace `fine-grained-tool-streaming-2025-05-14` with `eager_input_streaming: true` per tool; remove `effort-2025-11-24` (unverified). Switch back from `client.beta.messages` to `client.messages` (unverified). Remove prefills. Soften aggressive tool language.
- **Lifecycle**: Sonnet 4.6 is *Legacy* (still available, status "Active (legacy)"); Anthropic recommends migrating to Claude Sonnet 5.5 (`claude-sonnet-5-5`). Retirement not before 17 Feb 2027 (Anthropic platforms).

## Sources
- https://platform.claude.com/docs/en/models/sonnet-4-6/overview — Sonnet 4.6: 1M context, 128K output (batch beta 300K), adaptive thinking (extended deprecated), default effort `high`, $3/$15, cache read $0.30, knowledge cutoff Aug 2025, status legacy, migration recommendation to Sonnet 5.5, retirement not before 17 Feb 2027.
- https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide — section "Migrating from Claude Sonnet 4.5 or earlier": prefill → 400 (as on 4.6), read tool input with a JSON parser, set effort explicitly, remove `interleaved-thinking-2025-05-14`, replace `fine-grained-tool-streaming-2025-05-14` with `eager_input_streaming: true`, `output_format` → `output_config.format`; plus the thinking table (4.6: no field means off, default `display` `"summarized"`), cache minimum 1,024, ~30% more tokens and image limits of 1,568 px versus Sonnet 5.5.
- https://platform.claude.com/docs/en/build-with-claude/effort — effort levels (max for Sonnet 4.6, no xhigh); section "Recommended effort levels for Claude Sonnet 4.6" (medium recommended, set effort explicitly); per-message effort not on Sonnet 4.6, top-level change breaks the cache; model list with Haiku 5.5, without Haiku 4.5.
- https://platform.claude.com/docs/en/build-with-claude/thinking — configuration table (Sonnet 4.6: no field means no thinking, `enabled` deprecated, `disabled` possible), `display` default `"summarized"`, sampling rules of older models, prefill → 400 from Claude 4.6.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — "Migration considerations" (Claude 4.6 models more proactive, overtriggering; prefill replacement) and tool-overtriggering examples ("CRITICAL: You MUST …", "If in doubt …").
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages — model list for mid-conversation system messages (Sonnet 4.6 not included).
