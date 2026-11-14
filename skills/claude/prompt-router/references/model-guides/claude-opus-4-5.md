---
model: claude-opus-4-5
vendor: Anthropic
family: Claude
aliases: [opus-4.5, claude-opus-4.5, opus4.5, claude-opus-4-5-20251101]
last_verified: 2026-10-13
status: legacy
successor: claude-opus-5-5
---

# Claude Opus 4.5

## Reasoning / Thinking
- Type: **extended thinking only, off by default**. It is switched on manually with `thinking: {type: "enabled", budget_tokens: N}`; `thinking: {type: "adaptive"}` returns 400.
- Opus 4.5 is the only extended-thinking model with the `effort` parameter: effort and `budget_tokens` work together — first choose the effort level for the task, then set the thinking budget according to the reasoning depth needed. Default `high`; `xhigh` and `max` are not listed for Opus 4.5.
- `thinking.display` returns summarized thinking by default (`"summarized"`).
- Interleaved thinking (thinking between tool calls) needs a beta header in manual mode (`interleaved-thinking-2025-05-14`) and changes how the budget is counted.
- With thinking active: `temperature`/`top_k` are incompatible, `top_p` only between 0.95 and 1; forced tool use (`tool_choice` `any`/`tool`) is not possible, only `auto`/`none`; no assistant prefill.
- **Without extended thinking** Opus 4.5 is particularly sensitive to the word "think" and variants — use alternatives such as "consider", "evaluate" or "reason through".

## Prompting style
- **Soften aggressive language**: Opus 4.5 responds more strongly to the system prompt than earlier models; tool/skill instructions written to counter undertriggering lead to overtriggering. "CRITICAL: You MUST use this tool when…" → "Use this tool when…".
- **Curb overengineering**: tendency toward extra files, unnecessary abstractions and unrequested flexibility — keep solutions minimal via instruction.
- **Word choice with thinking off**: replace "think" and variants in prompts with "consider", "evaluate" or "reason through" (see above).
- **Prefill is allowed** while thinking is off — a pattern that is rejected with 400 from Opus 4.6 onward.
- **Give frontend specifications**: without design instructions the model falls back on generic patterns ("AI slop" aesthetic); specify typography, colors and interactions explicitly.

## Strengths & weaknesses (prompt-relevant)
- Strengths: improved vision, especially for image processing and data extraction across multiple images; more reliable reading of screenshots and UI elements in computer use; complex web apps with strong frontend design.
- Weaknesses/quirks: overtriggering with overly emphatic tool language, overengineering, sensitivity to "think" without thinking; smaller window than all later Opus models.
- Reliable knowledge cutoff May 2025 (training data cutoff August 2025).

## Output & format conventions
- 200K context window (roughly 150k words), 64K output tokens; the Batches API 300K output beta does not exist for Opus 4.5. Input text and images, output text.
- Dated model ID: `claude-opus-4-5-20251101`; `claude-opus-4-5` is a convenience alias that points to the dated ID. Google Cloud: `claude-opus-4-5@20251101`; Bedrock only via InvokeModel (`anthropic.claude-opus-4-5-20251101-v1:0`).
- Tokenizer of the generation before Opus 4.7: the same text needs up to ~35% more tokens from Opus 4.7 onward.
- Structured Outputs via `output_config.format`; the older `output_format` is deprecated and needs the beta header `structured-outputs-2025-11-13`, otherwise 400.
- The `effort` parameter no longer needs a beta header (`effort-2025-11-24` can be dropped).

## Migration notes
- **Lifecycle**: legacy, status Active; retirement not before 24 Nov 2026 — the earliest date of the Opus models still available. Anthropic recommends migrating to Claude Opus 5.5.
- **AWAY FROM Opus 4.5 to Opus 4.6+/Opus 5.5**: remove assistant prefills (from 4.6 → 400) and replace them with Structured Outputs or the system prompt; read tool-call `input` with a JSON parser (changed escaping from 4.6); switch from `client.beta.messages.create()` to `client.messages.create()`; remove the beta headers `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14` and `interleaved-thinking-2025-05-14`; `output_format` → `output_config.format`; `budget_tokens` → adaptive thinking plus effort (mandatory from 4.7). Then work through all steps from Opus 4.6 (sampling parameters, thinking display, tokenizer, image tokens) and, for Opus 5.5, thinking always on, effort default `medium` and the ban on forced tool use.
- **MIGRATING TO Opus 4.5** (from newer models): replace adaptive thinking with `thinking: {type: "enabled", budget_tokens: N}` and set effort at most to `high`; trim prompts and outputs to the 200K context / 64K output limits; with thinking active, avoid forced tool use, prefill and non-default `temperature`/`top_k`; reword "think" in prompts when thinking is off.

## Sources
- https://platform.claude.com/docs/en/models/opus-4-5/overview — legacy status, model ID `claude-opus-4-5-20251101` with alias `claude-opus-4-5`, platform IDs, 200K context, 64K output, thinking "Extended", effort default `high`, knowledge cutoff May 2025, retirement not before 24 Nov 2026, migration recommendation to Opus 5.5.
- https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-45 — breaking changes from 4.5 (prefill, tool-parameter escaping) and recommended steps (adaptive thinking, remove beta namespace and beta headers, `output_config.format`).
- https://platform.claude.com/docs/en/about-claude/model-deprecations — `claude-opus-4-5-20251101` status Active, retirement "Not sooner than November 24, 2026".
- https://platform.claude.com/docs/en/about-claude/models/overview — Opus 4.5 in the list "Legacy models (still available)"; alias before the 4.6 generation as a convenience pointer to the dated ID; 200K tokens ≈ 150k words.
- https://platform.claude.com/docs/en/build-with-claude/effort — Opus 4.5 as the only extended-thinking model with effort, interplay with `budget_tokens`, `xhigh`/`max` not listed for Opus 4.5, no beta header needed.
- https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting — Opus 4.5: extended thinking only, default off, `adaptive` → 400.
- https://platform.claude.com/docs/en/build-with-claude/thinking — `display` default `summarized` on older models, interleaved thinking in manual mode via beta header, sampling/prefill/forced-tool-use limits with thinking active, 64K output without batch extension.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — Opus 4.5-specific: "think" sensitivity without extended thinking, system prompt responsiveness/overtriggering, overengineering, vision, frontend design.
