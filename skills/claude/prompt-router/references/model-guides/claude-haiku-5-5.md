---
model: claude-haiku-5-5
vendor: Anthropic
family: Claude
aliases: [haiku, haiku-5.5, claude-haiku-5.5, haiku5.5]
last_verified: 2026-10-13
status: current
---

# Claude Haiku 5.5

## Reasoning / Thinking
- Type: **adaptive, on by default**. Requests without a `thinking` field think (Haiku 4.5: no field, no thinking). Omit `thinking` or send `{type: "adaptive"}`.
- `thinking: {type: "enabled", budget_tokens: N}` → 400. Haiku 5.5 is the **first Haiku model with effort**: `output_config.effort` = `low | medium | high | xhigh | max`, default **`medium`** (an explicitly set default behaves like an omitted parameter).
- Turning thinking off: `thinking: {type: "disabled"}` works **only at `low`, `medium` and `high`**; at `xhigh`/`max` → 400 (`output_config.effort 'xhigh' is not supported when thinking is disabled on this model.`). According to the docs, lowering effort is a better lever than turning thinking off; a prompt instruction "answer directly" did not suppress thinking in Anthropic's tests.
- Thinking tokens count against `max_tokens` (up to 128,000): limits set too tight end with `stop_reason: "max_tokens"` after a `thinking` block, with no text.
- Thinking blocks from earlier assistant turns stay in context and are billed as input (Haiku 4.5 kept only those of the last turn).
- `thinking.display` defaults to `"omitted"`: blocks come with an empty `thinking` field and only the `signature`; `display: "summarized"` returns the summary (Haiku 4.5: summarized by default).
- Forced `tool_choice` (`any` or a named tool) is accepted, but the response then starts directly with the tool call **without** a thinking block.
- Sampling: `temperature` only `1`, `top_p` only `0.99`; any other value, any `top_k`, and `temperature` together with `top_p` → 400.
- Thinking blocks are bound to the generating account (or a linked one); replaying them through another account silently discards them. A returned block is only valid as long as `system`, `tools` and earlier `messages` are unchanged, otherwise 400 (for accounts created before 31 Aug 2026 only with `thinking.block_binding.prefix_mismatch_behavior` set).

## Prompting style
- Anthropic: existing **Haiku 4.5 prompts should run well unchanged** — make adjustments targeted to observed behavior, not blanket changes.
- **effort instead of a thinking budget**: compare two to three levels on your own evals. `low` for chat, short tool tasks and simple high-volume requests; `medium` (default) for most tasks, including agentic coding; `high` for knowledge work, longer agent tasks and strict instruction following; `xhigh`/`max` only where the gain is measurable, and then compare against Sonnet 5.5.
- **Search**: with search tools, give the current date in the system prompt or tool description; at `low` and with long system prompts, additionally include the docs note that training data is outdated and "latest" facts must be searched for. Avoid blanket "always search" instructions (more unnecessary searches, no better answers).
- **Long agent prompts at `low`**: tendency toward premature stopping and unverified code changes — add the docs building blocks "keep working until done, no unrequested extras" and "run a real test/build/typecheck before reporting done", or raise effort (costs more output tokens).
- **Chatbots**: add a sentence that the system prompt rules apply throughout the whole conversation, even when users argue or insist; for important instruction following additionally use `high`.
- **Mid-turn user input**: never put it in `tool_result` blocks (the model may ignore it as untrusted); instead send it as a text block after the last `tool_result` in the user turn; harness hints go in a separate mid-conversation system message.
- Introduce new system prompt lines only in **new** conversations; ongoing conversations receive changes in the latest turn or as an appended system message (otherwise 400 because the prefix changed).

## Strengths & weaknesses (prompt-relevant)
- Strengths: built for high-volume, latency-critical tasks such as classification, routing, extraction and sub-agents; according to the model overview, the lowest latency in the current lineup ("Fastest") and the lowest prices; adaptive thinking + effort, 1M context; browser-use tool (`browser_toolset_20260801`) on the Claude API and Google Cloud.
- Weaknesses/quirks: at `low`, searches more often skipped, premature stopping and skipped checks; with thinking off **plus** JSON output via Structured Outputs, a needed tool call is sometimes skipped (remedies: adaptive thinking, omit `output_config.format` when a tool is mandatory, force `tool_choice`, or use the docs line "JSON applies only to the final answer"); reasoning-like text in the visible answer, more often with thinking off or at `low` (remedy: adaptive + `medium`); at `xhigh` in multi-turn chats, occasionally the whole answer ends up in thinking and the visible text is empty.
- Safety classifiers can refuse: `stop_reason: "refusal"` with `stop_details.category` (`cyber`, `frontier_llm`, `bio`, `general_harms`) — new compared with Haiku 4.5; **no** server-side fallback, and resending usually yields the same refusal.

## Output & format conventions
- 1M context window, 128k output tokens; via the Message Batches API up to 300k with beta header `output-300k-2026-03-24`. Input: text and images → text. Reliable knowledge cutoff Jun 2026.
- **New tokenizer** (as with Claude 4.7+): the same text ≈ 30% more tokens than on Haiku 4.5 — re-measure `max_tokens`, token counts and cost estimates.
- **High-resolution image tier**: downscaling only above 2,576 px on the long edge or 4,784 visual tokens (Haiku 4.5: 1,568 px / 1,568 tokens); a 2000×1500 image costs about 2.5× as many visual tokens.
- **No assistant prefill** (400, also with thinking off) — end `messages` with a user turn; control format via Structured Outputs or tools with enum fields, and suppress preambles via the system prompt.
- Structured Outputs (`output_config.format`) are available on the Claude API among others, **not on Amazon Bedrock** — there, describe the format in the prompt or use a tool without `strict` and validate yourself.
- Responses can begin with `thinking` blocks: select content blocks by `type`, not by position.
- Prices per MTok, tiered by prompt length: up to 100k tokens $0.10 input / $0.50 output, above that $0.50 / $2.50; cache read $0.01 or $0.05; batch −50%. Minimum cacheable prompt: 512 tokens (Haiku 4.5: 4,096).
- Model IDs: Claude API, Google Cloud, Microsoft Foundry, Claude Platform on AWS `claude-haiku-5-5` (fixed ID with no date suffix and no separate alias); Amazon Bedrock `anthropic.claude-haiku-5-5`. Status *Active (latest)*, release 7 Oct 2026, retirement not before 7 Oct 2027.

## Migration notes
- **MIGRATING TO Haiku 5.5 (from Haiku 4.5)**: swap the model ID; re-count prompts and size `max_tokens` with headroom for thinking; replace `enabled`+`budget_tokens` with adaptive thinking + effort (where Haiku 4.5 ran without thinking or with a small budget, choose a lower effort level); read blocks by `type` instead of position; remove `temperature`/`top_p`/`top_k` and steer behavior via the prompt; replace prefill with a closing user turn; replace `computer_20250124` (Claude API/Google Cloud: `computer_toolset_20260801`, Bedrock: `computer_20251124` + `computer-use-2025-11-24`); run replays through the generating account; keep conversations append-only; handle `stop_reason: "refusal"`; on Bedrock, replace Structured Outputs with prompt-described format + your own validation. Priority Tier is not supported on Haiku 5.5 — plan capacity separately.
- **MIGRATING TO Haiku 5.5 (from Haiku 3.5 or older)**: additionally replace `claude-3-5-haiku-20241022` / `claude-3-5-haiku-latest` / `claude-3-haiku-20240307` (all retired on the Claude API); `code_execution_20250522` → `code_execution_20250825` or newer; text editor to `text_editor_20250728`; handle `refusal` and `model_context_window_exceeded`; allow trailing newlines in tool string parameters; revise prompts — Claude 4+ models communicate more concisely and directly and need explicit instructions.
- **AWAY FROM Haiku 5.5 (to Haiku 4.5)**: there is no dedicated guide for this direction; from the Haiku 4.5 specifications it follows: remove effort (not supported there) and control thinking via `enabled`+`budget_tokens` (without a `thinking` field Haiku 4.5 runs without thinking); sampling parameters and prefill (with thinking off) are allowed again there; cap context at 200K and output at 64K.
- Reasoning chain compatibility: Haiku 5.5 reads thinking blocks from Sonnet 5, Opus 4.8, Haiku 4.5 and older models, **not** from Opus 5, Opus 5.5, Sonnet 5.5, Fable or Mythos (silently discarded).

## Sources
- https://platform.claude.com/docs/en/models/haiku-5-5/overview — id `claude-haiku-5-5` and platform IDs, 1M context / 128k output (300k batch beta), tiered prices incl. cache write/read, thinking adaptive, default effort `medium`, latency "Fastest", knowledge cutoff Jun 2026, status *Active (latest)*, release 7 Oct 2026, retirement not before 7 Oct 2027, sampling note, 512-token cache minimum, ~30% more tokens than Haiku 4.5.
- https://platform.claude.com/docs/en/models/haiku-5-5/whats-new-haiku-5-5 — change summary versus Haiku 4.5 (new, breaking, changed), browser-use tool, refusals without fallback, thinking blocks stay in context, cache minimum 512 instead of 4,096.
- https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide — checklists "Every starting model" and "Claude Haiku 3.5 or earlier", model ID table, tokenizer and high-resolution image tier, thinking configuration, sampling and prefill 400, computer-use toolset, account binding, append-only check, no Priority Tier, no Structured Outputs on Bedrock, readability of foreign thinking blocks.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 — Haiku 4.5 prompts run unchanged, effort recommendations per level, `disabled` only up to `high`, search date, JSON output with own tools, early stopping, verification for coding agents, mid-turn user input, system prompt fidelity, reasoning in visible text, refusal categories.
- https://platform.claude.com/docs/en/build-with-claude/effort — Haiku 5.5 supports all five levels, default `medium`, default set explicitly = omitted, per-message effort (beta) and 400 on effort change with thinking off.
- https://platform.claude.com/docs/en/build-with-claude/thinking — configuration matrix (no field adaptive, `enabled` 400, `disabled` up to `high`), `display` default `"omitted"`, retention of earlier thinking blocks, sampling rules.
- https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting — exact error message for `disabled` at `xhigh`/`max`, no thinking block with forced `tool_choice`, prefix-check error.
- https://platform.claude.com/docs/en/models/haiku-4-5/overview — comparison values of the predecessor (200K context, 64K output, extended thinking, effort "Not supported") for the reverse direction.
- https://platform.claude.com/docs/en/models/overview — Haiku 5.5 in the current lineup ("Fastest", "From $0.10 / input MTok"), Haiku 4.5 under "Legacy models (still available)".
