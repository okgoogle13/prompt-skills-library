---
model: claude-haiku-4-5
vendor: Anthropic
family: Claude
aliases: [haiku-4.5, claude-haiku-4.5, haiku4.5, haiku-4-5, claude-haiku-4-5-20251001]
last_verified: 2026-10-13
status: legacy
successor: claude-haiku-5-5
---

# Claude Haiku 4.5

## Reasoning / Thinking
- Type: **Extended Thinking (manual)** via `thinking: {type: "enabled", budget_tokens: N}`; `budget_tokens` at least 1,024 and less than `max_tokens`. Without a `thinking` field no thinking runs; `{type: "adaptive"}` → 400 (`adaptive thinking is not supported on this model`).
- The **`effort` parameter is not supported** (model page: default effort "Not supported") — unlike Haiku 5.5 and the Opus models from 4.5, the Sonnet models from 4.6 and the Fable models. Depth is controlled only via `budget_tokens`. The specific error when sending `effort` is not described on the pages checked (unverified).
- Budget tuning per the docs: for simple tasks start near 1,024 and increase gradually; for complex ones from about 16,000; run budgets above 32k via the Batch API. The budget is a target, not a hard cap; `max_tokens` remains the ceiling.
- **No interleaved thinking** (the beta header is accepted on the Claude API but ignored). Forced `tool_choice` (`any`/`tool`) cannot be combined with extended thinking (error); only `auto` or `none`.
- Thinking blocks: only those of the last assistant turn are kept; the API removes older ones automatically. `thinking.display` defaults to `"summarized"`.
- Sampling: `temperature`, `top_p`, `top_k` are accepted; **with thinking active**, `temperature` and `top_k` are incompatible and `top_p` is allowed only between 0.95 and 1.

## Prompting style
- Clear, direct, explicit instructions: Claude 4 and later models communicate more concisely and directly and need explicit instructions rather than implied expectations.
- Keep it short and simple; for complex multi-step reasoning a larger model is better suited. (unverified)
- Use Structured Outputs for fixed output formats; assistant prefill only works with thinking turned off.

## Strengths & weaknesses (prompt-relevant)
- Strengths: fast, cost-efficient model of the 4.5 generation ($1 / $5 per MTok); according to the model overview, Haiku 5.5 now has the lowest latency ("Fastest") and lower list prices. Good for high-volume, clearly bounded tasks. (unverified: usage profile)
- Weaknesses: no `effort`, no adaptive and no interleaved thinking; 200K context; reliable knowledge cutoff Feb 2025 (training data cutoff Jul 2025). Lower reasoning depth than Opus/Sonnet — structure complex logic explicitly in the prompt. (unverified)

## Output & format conventions
- 200K context window, up to 64K output tokens; no 300k batch output beta. Input: text and images → text; images at the standard resolution tier (downscaling above 1,568 px on the long edge or 1,568 visual tokens).
- Structured Outputs are supported (`output_config.format`). On Amazon Bedrock only via the legacy integration (InvokeModel), not via "Claude in Amazon Bedrock".
- Assistant prefill is accepted with thinking turned off; with thinking active, prefill is not possible.
- Computer use via `computer_20250124` with beta header `computer-use-2025-01-24`; the browser-use tool is not supported.
- Prices per MTok: input $1, output $5, 5m cache write $1.25, 1h cache write $2, cache read $0.10; batch −50%. Minimum cacheable prompt: 4,096 tokens.
- Model IDs: Claude API `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`); Amazon Bedrock `anthropic.claude-haiku-4-5` (InvokeModel `anthropic.claude-haiku-4-5-20251001-v1:0`); Google Cloud `claude-haiku-4-5@20251001`; Microsoft Foundry and Claude Platform on AWS `claude-haiku-4-5`.

## Migration notes
- **Lifecycle**: the model overview and model page list Haiku 4.5 as **legacy** (status "Active (legacy)", successor Claude Haiku 5.5); the deprecations table lists `claude-haiku-4-5-20251001` as Active with retirement not before 15 Oct 2026. Before migrating TO Haiku 4.5, check the current status on the deprecations page.
- **AWAY FROM Haiku 4.5 (to Haiku 5.5)**: according to Anthropic, existing Haiku 4.5 prompts run well without changes; the mandatory changes are API-side — `budget_tokens` → adaptive thinking + effort, remove sampling parameters and prefill, replace `computer_20250124`, plan for ~30% more tokens and thinking within `max_tokens` (details in the `claude-haiku-5-5` guide).
- **AWAY FROM Haiku 4.5 (to Opus/Sonnet)**: `effort` and adaptive thinking become available — depth can be controlled more finely; depending on the target model, its own restrictions apply (sampling, prefill, `budget_tokens`).
- **MIGRATING TO Haiku 4.5**: remove the `effort` parameter from requests; replace adaptive thinking with `enabled` + `budget_tokens` (otherwise 400); cap context at 200K and output at 64K; thinking text comes back as a summary again; simplify prompts and narrow the task scope. (unverified: last point)

## Sources
- https://platform.claude.com/docs/en/models/haiku-4-5/overview — legacy status ("Active (legacy)"), successor Haiku 5.5, model IDs per platform including alias, 200K context, 64K output, $1/$5 plus cache prices, thinking "Extended", default effort "Not supported", knowledge cutoff Feb 2025 / training Jul 2025, retirement not before 15 Oct 2026.
- https://platform.claude.com/docs/en/build-with-claude/thinking — configuration matrix (no field means no thinking, `adaptive` 400, `enabled` = extended thinking), `display` default `"summarized"` for older models, sampling and prefill rules with thinking active, no interleaved thinking, only last turn kept, `tool_choice` restriction in manual mode.
- https://platform.claude.com/docs/en/build-with-claude/extended-thinking — `budget_tokens` ≥ 1,024 and < `max_tokens`, budget tuning (1,024 / 16,000 / batch above 32k), interleaved header on Haiku 4.5 ignored, migration to adaptive thinking.
- https://platform.claude.com/docs/en/build-with-claude/effort — `supportedModels` without Haiku 4.5 (includes Haiku 5.5, Opus from 4.5, Sonnet from 4.6, Fable).
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs — `claude-haiku-4-5-20251001` supported, `output_config.format`, on Bedrock only via the legacy integration.
- https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide — Haiku 4.5 accepts sampling parameters and prefill with thinking, `computer_20250124` + `computer-use-2025-01-24`, standard image tier, no browser-use tool on Haiku 4.5, Haiku 4.5→5.5 checklist, Claude 4+ models need explicit instructions.
- https://platform.claude.com/docs/en/models/haiku-5-5/whats-new-haiku-5-5 — cache minimum 4,096 tokens on Haiku 4.5.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 — existing Haiku 4.5 prompts run well on Haiku 5.5 without changes.
- https://platform.claude.com/docs/en/about-claude/model-deprecations — `claude-haiku-4-5-20251001` Active, retirement not before 15 Oct 2026.
- https://platform.claude.com/docs/en/models/overview — Haiku 4.5 under "Legacy models (still available)", Haiku 5.5 "Fastest".
