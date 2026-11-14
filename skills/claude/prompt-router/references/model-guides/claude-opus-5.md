---
model: claude-opus-5
vendor: Anthropic
family: Claude
aliases: [opus-5, claude-opus5, opus5]
last_verified: 2026-10-13
status: legacy
successor: claude-opus-5-5
---

# Claude Opus 5

## Reasoning / Thinking
- Type: **adaptive, on by default**. A request without a `thinking` field thinks — unlike Opus 4.8/4.7, where the same request ran without thinking. `{type: "adaptive"}` is equivalent to omitting the field.
- Turning thinking off via `thinking: {type: "disabled"}` is allowed **only up to effort `high`**; combined with `xhigh`/`max` → 400.
- `thinking: {type: "enabled", budget_tokens: N}` is removed (400). Depth is controlled solely via `output_config.effort` (`low | medium | high | xhigh | max`, default `high`).
- Raw chain of thought is never returned; `display: "summarized"` returns a summary, default `"omitted"` returns empty thinking fields.
- Sampling parameters `temperature`/`top_p`/`top_k` at non-default values → 400.
- `max_tokens` is a hard limit over thinking **plus** response text — re-size for workloads that previously had no thinking. At `xhigh`/`max` start with ≥ 64k.

## Prompting style
- **Explicit instead of implicit**: Opus 5 interprets prompts literally, does not silently generalize an instruction to other cases and does not infer unstated requirements. Spell out the scope.
- **Remove verification instructions**: the model checks its work unprompted. Carried-over "double-check your answer" / "include a final verification step" lines cause over-verification — removing them lowers cost without losing quality.
- **Specify length explicitly**: `effort` controls thinking volume, not visible response length — lowering it does not reliably shorten answers. Add a short concise instruction; in long system prompts, additionally add a `<tone_preference>` reminder at the end.
- **Limit scope**: the model sometimes expands tasks with unrequested steps; narrow tasks need an explicit scope rule.
- **Cap delegation**: Opus 5 delegates to subagents more readily than its predecessors — name criteria or set a hard upper limit.
- **Remove progress scaffolding**: staged choreography ("summarize after every 3 tool calls") is superfluous; describe the cadence and form of updates instead.
- For long agentic runs: give the complete task specification **up front** in one turn and let it run.
- **Do not request reasoning in the response text**: prompts, skills and tool descriptions that have the model write out its thinking/reasoning — verbatim or in a fixed format (a `<thinking>`, `<reasoning>` or scratchpad section before the answer, a `reasoning`/`thinking`/`trace` field in JSON output or tool input, a reasoning log, reasoning "verbatim"/"in full") — can be refused with `stop_reason: "refusal"` and `stop_details.category: "reasoning_extraction"`. Instead, request a short justification, the evidence, or a summary of the steps taken; if the reasoning itself is needed, keep thinking on and read the thinking blocks with `display: "summarized"`. This category has no fallback model (change the prompt rather than resending), and a refusal before any output is billed.

## Strengths & weaknesses (prompt-relevant)
- Strengths: difficult agentic coding tasks (multi-file features, larger refactors, end-to-end work) without stubs/placeholders; code review with high precision **and** recall, even at low effort; vision (charts, documents, diagrams, UI replication); office artifacts (multi-sheet spreadsheets with formulas, slide decks); multi-agent coordination with writer-verifier patterns; consistent instruction following across the full 1M window.
- `low`/`medium` deliver strong quality at a fraction of the tokens and latency — the primary cost lever; re-sweep effort defaults carried over from predecessor models.
- Weaknesses/quirks: longer visible answers and longer written deliverables than predecessors; pronounced narration in agentic sessions; narratively verbose self-corrections; severity filters in review prompts ("only high-severity") are followed literally and lower measured recall.
- With thinking turned off, two artifacts: tool calls occasionally land as **text** instead of a `tool_use` block (the turn counts as successful, but the call never runs), and internal XML tags can leak into the visible response. The primary countermeasure per the docs: leave thinking on and lower effort instead.

## Output & format conventions
- 1M context window as both default **and** maximum (no beta header), 128k output tokens; via the Message Batches API up to 300k output with beta header `output-300k-2026-03-24`.
- No assistant prefill — use Structured Outputs (`output_config.format`) or system prompt instructions.
- Tokenizer as Opus 4.7/4.8: compared with models before Opus 4.7, roughly 1× to 1.35× as many tokens for the same text (content-dependent).
- Safety classifiers can refuse: HTTP 200 with `stop_reason: "refusal"` and `stop_details` — check before reading `content`. Server-side fallbacks via `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`, Claude API only; the older header `server-side-fallback-2026-06-01` accepts only the explicit model list).
- Price $5 / MTok input, $25 / MTok output; reliable knowledge cutoff May 2026.
- Minimum cacheable prefix: **512 tokens** (Opus 4.8: 1,024) — prompts previously considered too short to cache now cache without code changes. When switching from 4.8, a cache-eligibility review is worthwhile.
- Top-level effort (`output_config.effort` on the request) is part of the rendered prompt — a change between requests restarts the prompt cache. A per-message effort change (beta header `mid-conversation-output-config-2026-07-01`, Claude API and Google Cloud only, not Amazon Bedrock) keeps the cache.
- Mid-conversation system messages (`role: "system"` in `messages` directly after a user turn) are supported on Opus 5 without a beta header (Claude API, Amazon Bedrock, Google Cloud) — change instructions without rebuilding the history.

## Migration notes
- **Lifecycle**: legacy according to the vendor (status *Active (legacy)*, retirement not before 24 Jul 2027); Anthropic recommends migrating to Claude Opus 5.5 (`claude-opus-5-5`) — there `thinking: disabled` returns 400 at every level, forced tool use is removed and the effort default drops to `medium`.
- **AWAY FROM Opus 5**: re-add explicit verification and self-check steps if the target model does not check its own work; re-evaluate concise/scope/delegation-cap instructions (they compensate for Opus 5 quirks); remove `fallbacks`, `refusal` and effort specifics; for targets without adaptive thinking, plan for step-by-step scaffolding again or `budget_tokens`.
- **MIGRATING TO Opus 5**: remove `budget_tokens` and all sampling parameters; replace assistant prefill with Structured Outputs; check whether any route combines `thinking: disabled` with `xhigh`/`max` (→ 400: keep thinking on or lower effort to `high`); increase `max_tokens` on routes that previously had no thinking; **remove** verification and progress scaffolding; add concise and scope instructions; cap delegation; re-run the effort sweep rather than adopting old defaults; add `refusal` handling; replace instructions to write out reasoning in the response text with a short justification (`reasoning_extraction`, see Prompting style).

## Sources
- https://platform.claude.com/docs/en/models/opus-5/overview — documented: id `claude-opus-5`, 1M context, 128k output, $5/$25, knowledge cutoff May 2026, effort default `high`, 300k output beta on the Batches API, 512-token cache minimum, legacy status with Opus 5.5 as migration target, retirement not before 24 Jul 2027.
- https://platform.claude.com/docs/en/build-with-claude/thinking — Opus 5: thinking on by default, `disabled` only up to effort `high` (otherwise 400), `budget_tokens` → 400, sampling parameters rejected, `display` default `omitted`, tool calls as text / XML leaks with thinking off.
- https://platform.claude.com/docs/en/models/opus-5-5/migration-guide — for Opus 4.7 and later: `budget_tokens` removed, sampling parameters rejected, tokenizer roughly 1× to 1.35×; differences Opus 5 → Opus 5.5.
- https://platform.claude.com/docs/en/build-with-claude/effort — all five effort levels for Opus 5, default `high`, recommendation to start at `high` with a fresh sweep, `max_tokens` ≥ 64k at `xhigh`/`max`, top-level effort change restarts the cache, per-message effort (beta) keeps it (not on Amazon Bedrock).
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching — minimum cacheable prefix 512 tokens for Opus 5 versus 1,024 for Opus 4.8.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 — verbosity/deliverable length, over-verification, scope expansion, sub-agent cap, self-correction narration, literal instruction following, the two artifacts with thinking off, code-review severity filter, reasoning in the response (`reasoning_extraction`).
- https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback — category `reasoning_extraction` and section "Keep reasoning in thinking blocks": typical triggers, replacement with a short justification or `display: "summarized"`, no fallback model, refusal before any output is billed; server-side fallback Claude API only, `2026-06-01` explicit list only.
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages — no beta header, Opus 5 supported (Claude API, Amazon Bedrock, Google Cloud), placement rules.
- https://platform.claude.com/docs/en/build-with-claude/context-windows — 1M context as default without beta header for Opus 5, up to 128k output per request.
