---
model: claude-opus-4-8
vendor: Anthropic
family: Claude
aliases: [opus-4.8, claude-opus-4.8, opus4.8, opus-4-8]
last_verified: 2026-10-13
status: legacy
successor: claude-opus-5-5
---

# Claude Opus 4.8

## Reasoning / Thinking
- Type: **adaptive, off by default**. Without a `thinking` field the request runs without thinking; `thinking: {type: "adaptive"}` switches it on, `{type: "disabled"}` is allowed (no thinking). `thinking: {type: "enabled", budget_tokens: N}` returns 400.
- Depth control via `output_config.effort`: `low | medium | high | xhigh | max`, default `high`. Start with `xhigh` for coding/agentic cases, at least `high` for intelligence-critical tasks; `medium`/`low` only once evals confirm quality. `max` can tend toward overthinking. According to the docs, effort matters more for this model than for any earlier Opus.
- Adheres strictly to effort, especially at the lower end: at `low`/`medium` it sticks to what was requested; on medium-difficulty tasks at `low` there is a risk of under-thinking → raise effort rather than prompting around it (only under latency pressure, a targeted hint about multistep reasoning).
- Adaptive thinking triggering is controllable: with large, complex system prompts the model may think more often than desired — add a note to think only for multistep problems and otherwise answer directly.
- `thinking.display` defaults to `"omitted"` (empty thinking blocks). For visible summaries set `display: "summarized"`.
- Non-default values for `temperature`/`top_p`/`top_k` return 400 on every request — control via prompt + effort.
- At `xhigh`/`max`, set a large `max_tokens` (start at 64k) so there is room for thinking across subagents and tool calls.

## Prompting style
- According to the docs, it runs well without changes on existing Opus 4.7 prompts; on the API side, since 4.7 only the 1M context as default and mid-conversation system messages have been added.
- Calibrates response length to perceived task complexity (short for simple lookups, long for open-ended analysis). Where the product needs a fixed length, add a concise instruction; positive examples work better than prohibitions.
- Produces more regular, higher-quality progress updates in long agentic runs. Remove existing "after every N tool calls" scaffolding; where needed, describe the length/content of updates explicitly and give examples.
- Interprets prompts literally (especially at low effort), does not silently generalize instructions to other cases and does not infer unstated requirements — state the scope explicitly ("apply to every section, not just the first").
- Prefers reasoning over tool calls and starts fewer subagents by default. Higher effort (`high`/`xhigh`) increases tool use; additionally explain in the prompt when and why a tool (e.g. web search) should be used, and explicitly state when subagents make sense.
- Interactive coding products: state the task, intent and constraints fully in the first user turn — the model is more autonomous than its predecessors and thinks more after each user turn; specifications added step by step cost tokens and sometimes quality.
- Mid-conversation system messages (no beta header needed): append `{"role":"system"}` directly after a user turn in `messages[]` instead of changing the top-level system prompt (this preserves the prompt cache); Claude API, Amazon Bedrock, Google Cloud.
- Frontend: a persistent default house style (cream background, serif display type, terracotta/amber accent). Generic counter-instructions only shift the palette — specify a concrete alternative or have it propose several directions in advance.

## Strengths & weaknesses (prompt-relevant)
- Strengths according to the docs: long agentic runs, knowledge work, vision and memory tasks; at release better at bug finding than earlier models (higher recall and higher precision in internal evals).
- Prose: direct, opinionated style with few validation pleasantries and sparing emoji use — if the product needs a warmer voice, specify the tone explicitly.
- Weaknesses/quirks: adheres to effort strictly (under-thinking risk on medium-difficulty tasks at `low`/`medium`); under-use of tools/subagents without explicit triggers; higher token consumption in interactive multi-turn sessions than in autonomous single-turn runs.
- Code review: follows "only high-severity" / "be conservative" filters literally → measured recall can drop. Use the pattern "report everything (with confidence and severity), filter in a separate step" or name the threshold concretely.

## Output & format conventions
- Assistant prefill (last assistant turn) returns 400 — use Structured Outputs (`output_config.format`) or a system prompt instruction instead.
- 1M context window as default (no beta header), up to 128K output tokens; via the Message Batches API up to 300K with beta header `output-300k-2026-03-24`. The SDK requires streaming above `max_tokens` > 21,333 (`.stream()` / `get_final_message()`).
- Read tool-call `input` with a standard JSON parser, no raw-string matching.
- Tokenizer as Opus 4.7: compared with models before Opus 4.7, roughly 1× to 1.35× as many tokens for the same text.
- Prices per MTok: input $5, output $25, 5m cache write $6.25, 1h cache write $10, cache read $0.50; batch 50% discount. Minimum cacheable prefix: **1,024 tokens**. Reliable knowledge cutoff Jan 2026.
- Computer use: `computer_toolset_20260801` (Claude API, Google Cloud) and the older `computer_20251124`; on the Claude API and Google Cloud additionally the browser-use tool. Images up to 2,576px / 3.75 MP; according to the docs, 1080p is a good balance of performance and cost.
- Model IDs: `claude-opus-4-8` (Claude API, Google Cloud, Microsoft Foundry, Claude Platform on AWS), Bedrock `anthropic.claude-opus-4-8`.

## Migration notes
- **Lifecycle**: legacy according to the vendor (status *Active (legacy)*, retirement not before 28 May 2027); Anthropic recommends migrating to Claude Opus 5.5 (`claude-opus-5-5`).
- **AWAY FROM Opus 4.8 (to Opus 5.5)**: requests without a `thinking` field always think there — re-size `max_tokens` (thinking plus text) and output costs; `thinking: {type: "disabled"}`, forced `tool_choice` (`any`/`tool`) and, on Claude API/Google Cloud, `computer_20251124` return 400; the effort default drops to `medium` (set explicitly, re-sweep); the cache minimum drops to 512 tokens; Priority Tier is discontinued; text between tool calls comes as a `thinking` block instead of a `text` block.
- **AWAY FROM Opus 4.8 (to other/older models)**: possibly re-add more prescriptive scaffolding and explicit step-by-step instructions; roll back prefill only if the target guide allows it; `effort`/`xhigh` may not be available → control depth via the prompt.
- **MIGRATING TO Opus 4.8**: from Opus 4.7, a model ID swap plus prompt re-tuning is enough; instruction updates can be moved to mid-conversation system messages (Opus 4.7 rejects `role: "system"` in `messages` with 400); remove the context beta header. From 4.6 or older additionally: `budget_tokens` → adaptive thinking + effort, remove `temperature`/`top_p`/`top_k`, remove prefills, recalibrate costs and `max_tokens` for the new tokenizer and high-resolution images (up to about 3× image tokens). Then behavior: concise instruction where length matters, remove progress scaffolding, make tool/subagent triggers explicit, start at `xhigh` for effort, and check style prompts against the more direct tone.

## Sources
- https://platform.claude.com/docs/en/models/opus-4-8/overview — id `claude-opus-4-8` and platform IDs, 1M context, 128K output / 300K batch beta, $5/$25 plus cache prices, thinking "Adaptive", default effort `high`, knowledge cutoff Jan 2026, status *Active (legacy)*, retirement not before 28 May 2027, recommendation to migrate to Opus 5.5.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 — runs on Opus 4.7 prompts, length calibration by complexity, effort recommendations and strict effort adherence (under-thinking at `low`), controllable thinking triggering, reasoning before tool calls, fewer subagents, more regular progress updates, literal instruction following, direct prose style, interactive coding products ("more autonomous than prior models"), code-review severity filter, frontend house style, computer use.
- https://platform.claude.com/docs/en/build-with-claude/effort — effort levels incl. `xhigh`/`max`, default `high`, Opus 4.8 recommendation (start `xhigh` for coding/agentic), 64k `max_tokens` at `xhigh`/`max`.
- https://platform.claude.com/docs/en/build-with-claude/thinking — model table (no field: thinking off, `adaptive` on, `budget_tokens` 400, `disabled` off), `display` default `omitted`, sampling parameters → 400, prefill → 400 from Claude 4.6, SDK streaming requirement above `max_tokens` > 21,333.
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages — no beta header needed, Opus 4.8 supported (Claude API, Amazon Bedrock, Google Cloud), placement rules.
- https://platform.claude.com/docs/en/build-with-claude/context-windows — 1M as default without beta header for Opus 4.8.
- https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-4-8 — path from Opus 4.8 to Opus 5.5 (thinking on requests without field, 512 instead of 1,024 cache minimum, Priority Tier), sections on Opus 4.7 (mid-conversation system messages, context header) and 4.6 and older (sampling, `budget_tokens`, prefill, tokenizer 1× to 1.35×, high-res images, JSON parsing of tool inputs).
