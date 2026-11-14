---
model: gpt-5.6-terra
vendor: OpenAI
family: GPT
aliases: [terra, gpt5.6-terra, 5.6-terra]
last_verified: 2026-11-13
status: current
---

# GPT-5.6 Terra

## Codex CLI: practical use

- **Availability:** The user's ChatGPT Go Codex CLI picker reports `gpt-5.6-terra` as selectable (2026-11-13). OpenAI's plan documentation also lists GPT-5.6 Terra for Codex on Free and Go, as well as higher eligible plans.
- **Best fit:** balanced everyday coding and agentic work where speed, capability and cost matter: implementing a well-scoped feature, routine debugging, code review, test updates, and moderate multi-file changes.
- **Prompt shape:** give the goal, relevant repository context, constraints and observable acceptance checks. For multi-file changes, identify the affected subsystem and ask for tests proportionate to the change.
- **Effort:** begin with the CLI's default. Use Low for clear, bounded changes; Medium for routine multi-step work; High or Extra High when diagnosis, planning or cross-file reasoning is genuinely difficult. Choose only levels shown by `/model`.
- **API-only boundary:** the API effort enum, `reasoning.mode`, `reasoning.context`, `text.verbosity`, token limits, pricing, endpoints and hosted Responses tools below do not automatically describe Codex CLI controls. In CLI, use `/model` and `/status` to inspect active model and effort.
- **Version note:** OpenAI's current model catalogue gives a minimum Codex CLI version for GPT-6.1 Terra, not a minimum version for this GPT-5.6 model. Do not transfer that requirement to GPT-5.6 Terra.

## Reasoning / Thinking
- Same reasoning control as `gpt-5.6-sol`: `reasoning.effort` with `none | low | medium (default) | high | xhigh | max`. Semantics: `none` for latency-critical tasks without reasoning benefit, `low` = "Efficient reasoning with a modest latency increase", `medium` as the balanced default, `high` for "Hard reasoning, complex debugging, deep planning", `xhigh` for "Deep research, asynchronous workflows and agentic tasks", `max` for "Maximum reasoning for your most complex tasks".
- **Codex CLI**: Supported reasoning levels: `low`, `medium`, `high`, `extra high` (corresponds to `xhigh`). Default `medium`.
- Additionally `reasoning.mode` = `standard` (default) / `pro` — independent of `effort`; `pro` does more model work at higher latency/cost. And `reasoning.context` = `auto | current_turn | all_turns`, default `all_turns` for GPT-5.6 models. At this price/performance tier: start at `medium` (default), test `low` for latency-critical paths, and compare `effort` independently of other parameters.

## Prompting style
- **Lean prompts**: remove repeated instructions and redundant examples, state each instruction exactly once, and expose only relevant tools with brief, precise descriptions. OpenAI measures ~10–15 % better eval scores at 41–66 % fewer tokens as a result (sample of internal coding-agent evals; the docs explicitly call the ranges "directional"). Keep examples only if they encode product requirements or close a measured gap.
- Set response length deliberately: `text.verbosity` (`low`/`medium`/`high`) as the baseline, with task-specific instructions in the prompt on top of it. For brevity, name what must survive: "Keep all required facts, decisions, caveats, and next steps. Trim introductions, repetition, generic reassurance, and optional background first."
- Define autonomy and approval limits explicitly: name safe local actions (read files, edit code, run tests) as allowed; require confirmation for "external writes, destructive actions, purchases, or a material expansion of scope".
- For tool/routing work, name the permitted tools and exact output schemas. Programmatic Tool Calling suits bounded aggregation/filter workflows with strong intermediate data reduction — poor when one call suffices, intermediate results are small, or every result changes the next decision.

## Strengths & weaknesses (prompt-relevant)
- Positioning: "designed for workloads that balance intelligence and cost", roughly equivalent to the mini tier of earlier GPT-5 families; in the model guide, "strong performance at a lower price".
- Inherits the family traits: frontier quality with fewer output tokens, stronger front-end/design judgement, and better inference of the user's actual goal and desired scope of work from context.
- Weaknesses: not the frontier model — quality-critical or hardest reasoning work belongs on `gpt-5.6-sol` (possibly `reasoning.mode: "pro"`) or, since 2026-09-03, `gpt-6-astra`, which OpenAI names in the reasoning guide as the starting point for most reasoning workloads. Realtime, Assistants, fine-tuning, embeddings, and audio/image/video endpoints are not supported. Family-wide safeguard behaviour also applies here: generation can pause mid-stream for several seconds while classifiers check the output synchronously — set timeouts/streaming accordingly.

## Output & format conventions
- Context window 1,050,000 tokens, max input 922,000, max output 128,000 tokens; knowledge cutoff 16 Feb 2026. Input: text + image, output: text.
- Endpoints: Chat Completions, Responses, Batch. Features: streaming, structured outputs, function calling, file search, image input, web search, prompt caching. Only one snapshot is listed: `gpt-5.6-terra` — no dated snapshot ID, no documented short alias.
- Level of detail via `text.verbosity` = `low | medium | high`, not via prose instructions in the prompt.
- Prices per 1M tokens: input $2, cached input $0.2, output $12; rule: "Prompts with >272K input tokens are priced at 2x input and 1.5x output for the full request" (cache writes at 1.25x the input rate).

## Migration notes
- **FROM gpt-5.6-terra**: remove `reasoning.effort`, `reasoning.mode`, `reasoning.context` and `text.verbosity` (OpenAI parameter names; map effort onto the target guide's ladder, and adopt `reasoning.mode`/`reasoning.context`/`text.verbosity` only if the target documents them); rewrite explicit brevity/format instructions and the examples the target needs back into the prompt; assumptions about the 1.05M context and 128K output shrink.
- **TO gpt-5.6-terra**: official successor to `gpt-5-mini-2025-08-07` (shutdown 11 Dec 2026). (1) Keep the existing effort as the baseline and test one level lower ("preserve your current reasoning effort as the baseline, then compare one level lower" — the docs phrase this for migrations from GPT-5.5/5.4; for gpt-5-mini as the starting point it is an extrapolation). (2) Trim the prompt hard: delete duplicated instructions, stacked few-shot examples and bloated tool descriptions left over from the gpt-5-mini era. (3) Remove or re-test blanket brevity lines — GPT-5.6 is inherently terser than GPT-5.5, and "Be concise" can now overshorten; set the default via `text.verbosity`, and keep only task-specific length/format rules in the prompt. (4) For reasoning, tool calling and multi-turn, prefer the Responses API; set `reasoning.context` to `auto`/`all_turns`, or `current_turn` if earlier reasoning is irrelevant. (5) Add autonomy/approval limits explicitly. (6) Escalate to `gpt-5.6-sol` (possibly `reasoning.mode: "pro"`) or, since 2026-09-03, `gpt-6-astra` — which OpenAI names as the starting point for most reasoning workloads — only on a measured quality gap; Terra is the balance tier ("strong performance at a lower price"), and `gpt-5.6-luna` is the cheaper nano tier below it "for efficient, high-volume workloads".

## Sources
- https://developers.openai.com/api/docs/models/gpt-5.6-terra — model ID, mini-tier positioning, 1,050,000 context / 922,000 input / 128,000 output, cutoff 16 Feb 2026, effort levels, endpoints/features, prices $2/$0.2/$12 and the >272K-token rule.
- https://developers.openai.com/api/docs/models/all — lists gpt-5.6-terra under "More models" ("GPT-5.6 model that balances intelligence and cost"), not deprecated; the flagship group there is GPT-6 (Astra / 6.1 Sol / Luna).
- https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.6-sol — shared GPT-5.6 prompt rules: lean prompts (10–15 % / 41–66 %), autonomy limits, `text.verbosity`, Programmatic Tool Calling, `reasoning.context`; section "Using GPT-5.6": "strong performance at a lower price", migration baseline (one effort level lower), trimming/verbosity guidance, family strengths, safeguard pauses.
- https://developers.openai.com/api/docs/guides/reasoning — effort levels and their semantics, `reasoning.mode` standard/pro, `reasoning.context` default `all_turns` for GPT-5.6; "Start with `gpt-6-astra` for most reasoning workloads", Terra/Luna as cheaper options.
- https://developers.openai.com/api/docs/changelog — 3 Sep 2026: "Released GPT-6 Astra".
- https://developers.openai.com/api/docs/deprecations — replacement mapping gpt-5-mini-2025-08-07 → gpt-5.6-terra, shutdown 11 Dec 2026.
- https://developers.openai.com/api/docs/models/gpt-5.6-luna — cheaper nano tier ($0.2/$0.02/$1.2) for placing the tier ladder.
