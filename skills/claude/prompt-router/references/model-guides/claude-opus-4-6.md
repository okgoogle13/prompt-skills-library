---
model: claude-opus-4-6
vendor: Anthropic
family: Claude
aliases: [opus-4.6, claude-opus-4.6, opus4.6]
last_verified: 2026-10-13
status: legacy
successor: claude-opus-5-5
---

# Claude Opus 4.6

## Reasoning / Thinking
- Type: **adaptive (extended deprecated), off by default**. Without a `thinking` field there is no thinking; `thinking: {type: "adaptive"}` is recommended. `thinking: {type: "enabled", budget_tokens: N}` still works but is deprecated; `{type: "disabled"}` is allowed. No `thinking.type` is rejected with 400.
- Depth control via `output_config.effort`: `low | medium | high | max`, default `high`. `xhigh` is not listed for Opus 4.6.
- `thinking.display` defaults to `"summarized"`; the first lines of the thinking output are more detailed (useful for prompt engineering).
- More upfront exploration than predecessors, especially at high effort: sometimes gathers a lot of context unasked or pursues several research threads; can think at length, inflating thinking tokens and latency. Countermeasures: limit reasoning by instruction or lower effort. A hard cost cap via `budget_tokens` still works but is deprecated — better lower effort or use `max_tokens` as the hard limit.
- Interleaved thinking is automatic with adaptive thinking (no beta header).
- Sampling parameters: the 400 rule for non-default values only applies from Claude 4.7. On Opus 4.6 the restriction applies only with thinking active: `temperature`/`top_k` are then incompatible, `top_p` only between 0.95 and 1.

## Prompting style
- **Soften aggressive language**: Opus 4.6 responds more strongly to the system prompt than earlier models; prompts written against undertriggering lead to overtriggering. "CRITICAL: You MUST use this tool when…" → "Use this tool when…".
- **Targeted instead of blanket defaults**: replace "Default to using [tool]" with "Use [tool] when it would enhance your understanding of the problem"; remove over-prompting such as "If in doubt, use [tool]".
- **Decision discipline**: against sprawling deliberation, an instruction to choose one approach and stick with it unless contradicting information appears helps.
- **Cap sub-agents**: strong tendency to start sub-agents even where a direct path (e.g. a `grep`) is enough — state explicitly when delegation makes sense and when it does not.
- **Curb overengineering**: tendency toward extra files, unnecessary abstractions and unrequested flexibility — add an instruction to keep solutions minimal.
- **Safeguard risky actions**: without guidance the model may run hard-to-reverse actions (deleting files, force-pushes, posting to external services). Write a confirmation requirement into the prompt for destructive, hard-to-reverse or otherwise visible actions.
- **No assistant prefill**: from Opus 4.6 a prefilled last assistant turn returns 400 — use Structured Outputs or system prompt instructions.

## Strengths & weaknesses (prompt-relevant)
- Strengths: improved vision, especially for image processing and data extraction across multiple images in context; more reliable reading of screenshots and UI elements in computer use; builds complex web apps with strong frontend design.
- Weaknesses/quirks: without design guidance, generic patterns ("AI slop" aesthetic); overtriggering on tools, sub-agent overuse, overengineering, overthinking (see above).
- Reliable knowledge cutoff May 2025 (training data cutoff August 2025).

## Output & format conventions
- 1M context window, 128K output tokens synchronously; via the Message Batches API up to 300K with beta header `output-300k-2026-03-24`. Input text and images, output text.
- Tokenizer of the generation before Opus 4.7: 1M tokens correspond to roughly 750k words; the same texts need up to ~35% more tokens from Opus 4.7 onward.
- No prefill; fixed formats via Structured Outputs (`output_config.format`) or the system prompt.
- Tool-call arguments may be escaped differently than in predecessors (Unicode, slashes) — always read `input` with a JSON parser, never match it as a raw string.
- Forced tool use (`tool_choice` `any`/`tool`) works with adaptive thinking; with extended thinking only `auto`/`none`.
- Bedrock only via the InvokeModel integration (`anthropic.claude-opus-4-6-v1`).

## Migration notes
- **Lifecycle**: legacy, status Active; retirement not before 5 Feb 2027. Anthropic recommends migrating to Claude Opus 5.5.
- **AWAY FROM Opus 4.6 to Opus 4.7+/Opus 5.5**: `budget_tokens` returns 400 from 4.7 → adaptive plus effort, run an effort sweep instead of translating the budget; remove `temperature`/`top_p`/`top_k`; `display` silently becomes `omitted` → set `display: "summarized"` for UI display; new tokenizer (up to ~1.35×): recheck `max_tokens`, compaction triggers and client-side token estimates; image tokens up to ~3× higher, remove coordinate scaling; remove forced progress scaffolding; plan for cyber safeguards. For Opus 5.5 additionally: thinking always on, effort default `medium`, forced tool use rejected.
- **AWAY FROM Opus 4.6 to Opus 4.5**: `adaptive` → 400, only `budget_tokens`; context 200K, output 64K, no `max`/`xhigh`; prefill allowed again (only without active thinking).
- **MIGRATING TO Opus 4.6** (from 4.5 or older): remove prefills; read tool input with a JSON parser; switch to adaptive thinking plus effort; scale back aggressive tool language and anti-laziness prompts; add minimal-change, sub-agent and confirmation rules.

## Sources
- https://platform.claude.com/docs/en/models/opus-4-6/overview — legacy status, model ID `claude-opus-4-6`, 1M context, 128K output (300K batch beta), thinking "Adaptive (extended deprecated)", effort default `high`, knowledge cutoff May 2025, retirement not before 5 Feb 2027, Bedrock InvokeModel ID, migration recommendation to Opus 5.5.
- https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-46 — breaking changes from Opus 4.7 (`budget_tokens`, sampling parameters, thinking display, tokenizer, prefill since 4.6), behavior changes (progress updates, cyber safeguards, high-res images), tool-parameter escaping from 4.6.
- https://platform.claude.com/docs/en/about-claude/model-deprecations — status Active, retirement "Not sooner than February 5, 2027"; sampling-parameter 400 only from Claude 4.7.
- https://platform.claude.com/docs/en/about-claude/models/overview — Opus 4.6 in the list "Legacy models (still available)"; extended thinking on Opus 4.6 deprecated; words per token before the Opus 4.7 tokenizer.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — Opus 4.6-specific: system prompt responsiveness/overtriggering, overthinking and upfront exploration, `budget_tokens` deprecated, sub-agent tendency, overengineering, risky actions, vision, frontend design.
- https://platform.claude.com/docs/en/build-with-claude/effort — effort levels (`max` yes, `xhigh` not for Opus 4.6), default `high`.
- https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting — Opus 4.6: adaptive plus extended (deprecated), default off, no rejected thinking types.
- https://platform.claude.com/docs/en/build-with-claude/thinking — `display` default `summarized` on Opus 4.6, sampling rules of older models, prefill from Claude 4.6 → 400, forced tool use only with adaptive thinking.
