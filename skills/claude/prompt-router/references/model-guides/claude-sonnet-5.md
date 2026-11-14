---
model: claude-sonnet-5
vendor: Anthropic
family: Claude
aliases: [sonnet-5, claude-sonnet5, sonnet5]
last_verified: 2026-10-13
status: legacy
successor: claude-sonnet-5-5
---

# Claude Sonnet 5

## Reasoning / Thinking
- Type: **adaptive, on by default**. Requests without a `thinking` field think — a change from Sonnet 4.6, where the same requests ran without thinking. Switch off with `thinking: {type: "disabled"}` (no effort cap, unlike Opus 5).
- `thinking: {type: "enabled", budget_tokens: N}` is removed (400) — on Sonnet 4.6 only deprecated; there is no transitional fallback here anymore. Depth is controlled via `output_config.effort`.
- Effort levels `low | medium | high | xhigh | max`, default `high` (as Sonnet 4.6); `xhigh` is new in the Sonnet class. Rough migration mapping: Sonnet 5 at `medium` ≈ Sonnet 4.6 at `high`; Sonnet 5 at `high` ≈ Sonnet 4.6 at `max`.
- Effort levels are followed strictly, especially at the lower end: at `low`/`medium` the model does only what was requested. If reasoning is shallow, raise effort rather than prompting around it.
- Sampling parameters `temperature`/`top_p`/`top_k` at non-default values → 400 (new for the Sonnet class).
- `max_tokens` caps thinking **plus** response text: with a tight budget, a truncated response consisting almost entirely of thinking is at risk, with `stop_reason: "max_tokens"`.

## Prompting style
- **Literal instruction following**, especially at low effort: no silent generalization, no inference of unstated requirements. If a rule should apply broadly, spell out its scope ("apply to every section, not just the first").
- **Verbosity is task-calibrated** rather than fixed — short answers for simple lookups, long ones for open-ended analysis. For fixed product lengths, prompt explicitly; positive examples of the desired brevity work better than negative instructions.
- **Remove progress scaffolding**: forced interim reports ("summarize after every 3 tool calls") are superfluous; if the form does not fit, describe the updates explicitly and give examples.
- **Tool use**: more agentic out of the box than Sonnet 4.6 (readily reaches for tools and self-verification loops). **With thinking switched off** it reaches for tools less often — then add an explicit nudge to the system prompt. `high`/`xhigh` markedly increase tool use.
- **The adaptive-thinking trigger is controllable**: where thinking blocks appear too often (happens with large/complex system prompts), counteract via the prompt and measure the effect.
- **Tone**: prose style shifts compared with 4.6; re-evaluate style prompts against the new baseline. If you previously used `temperature` for stylistic variety, switch to system prompt instructions.
- **Frontend/design**: with open briefs it tends toward a fixed default style. Generic prohibitions only shift it; what works is either a concrete specification (palette, typography, layout) or "propose 4 directions first, then implement one" — the latter is the recommended route to variety, since `temperature` is not available.
- **Interactive coding products**: use `xhigh`/`high`, add autonomous modes and reduce necessary user interactions; state the task, intent and constraints fully in the first turn.

## Strengths & weaknesses (prompt-relevant)
- Strengths: coding and agentic tasks (largest gain over Sonnet 4.6); runs on existing Sonnet 4.6 prompts out of the box; high-resolution vision; computer use with `computer_20251124` up to 2,576px / 3.75 MP (1080p as a good performance/cost compromise, 720p or 1366×768 for cost-sensitive cases).
- Weaknesses/quirks: severity filters in review prompts ("only high-severity", "be conservative") are followed more faithfully than before — precision rises, measured recall can fall, even though bug finding is better. Countermeasure: have everything reported (with confidence + severity) and filter in a separate step.
- Risk of under-thinking at `low` on medium-difficulty tasks.

## Output & format conventions
- 1M context window, 128k output tokens; via the Message Batches API up to 300k output with beta header `output-300k-2026-03-24`.
- **New tokenizer**: the same text yields roughly 30% more tokens than on Sonnet 4.6 (content-dependent). `max_tokens` limits tuned for 4.6 can truncate equivalent outputs; re-measure token counts and cost baselines.
- `thinking.display` defaults to `"omitted"` (Sonnet 4.6: `"summarized"`) — if you stream reasoning, set `display: "summarized"` explicitly.
- No assistant prefill — use Structured Outputs (`output_config.format`) or system prompt instructions.
- Price per the model table $2 / MTok input, $10 / MTok output; reliable knowledge cutoff Jan 2026.
- Mid-conversation system messages (`role: "system"` within `messages`) are **not** supported on Sonnet 5 — there the top-level `system` prompt remains the route. Per-message effort and mid-conversation tool changes are likewise missing; an effort change only works via the top-level value and restarts the prompt cache.
- Minimum cacheable prompt: 1,024 tokens.

## Migration notes
- **AWAY FROM Sonnet 5**: scopes that were spelled out because of the literalness may be terser on the target model; re-evaluate tone and variety instructions (possibly `temperature` again instead of prompting); re-size tokenizer-dependent `max_tokens` values; `xhigh` is often not available outside the current generation.
- **MIGRATING TO Sonnet 5**: replace `budget_tokens` with adaptive thinking + `effort`; remove `temperature`/`top_p`/`top_k` and steer tone/variety via the prompt; replace assistant prefill; note that a request without a `thinking` field now thinks (check `max_tokens`, or set `disabled` explicitly); set `display: "summarized"` if reasoning is shown; re-measure token baselines because of ~30% more tokens; remove progress scaffolding; switch the review harness from severity filters to "report everything, filter later"; for setups that previously ran without thinking, test thinking on with a lower effort. On Amazon Bedrock, send forced `tool_choice` together with `thinking: {type: "disabled"}`. (unverified: Bedrock detail not confirmed on the pages checked)
- **Lifecycle**: Sonnet 5 is *Legacy* (still available, status "Active (legacy)"); Anthropic recommends migrating to Claude Sonnet 5.5 (`claude-sonnet-5-5`; checklist in the Sonnet 5.5 guide). Retirement not before 30 Jun 2027 (Anthropic platforms).

## Sources
- https://platform.claude.com/docs/en/models/sonnet-5/overview — documented: id `claude-sonnet-5`, 1M context, 128k output, $2/$10, knowledge cutoff Jan 2026, adaptive thinking, effort default `high`, 300k output beta on the Batches API, sampling parameters → 400; status Legacy ("Active (legacy)"), successor Claude Sonnet 5.5, retirement not before 30 Jun 2027.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 — adaptive thinking on by default, `budget_tokens` → 400, sampling parameters → 400, ~30% more tokens from the new tokenizer, effort mapping to Sonnet 4.6, literalness, verbosity, tool triggering (also with thinking off), progress updates, tone, design defaults, code-review recall, computer use `computer_20251124` up to 2,576px.
- https://platform.claude.com/docs/en/build-with-claude/effort — effort levels incl. `xhigh`/`max` for Sonnet 5, default `high`, recommendations per level, effort change breaks the prompt cache.
- https://platform.claude.com/docs/en/build-with-claude/thinking — Sonnet 5 row of the model table (adaptive thinking on by default, `budget_tokens` → 400, `disabled` switches thinking off without effort cap), `display` default `"omitted"` (Sonnet 4.6: `"summarized"`), switching thinking off.
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages — mid-conversation system messages not available on Sonnet 5; use the top-level `system`.
- https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5 — section "Feature support": per-message effort, mid-conversation system messages and tool changes not available on Sonnet 5, cache minimum 1,024 tokens.
