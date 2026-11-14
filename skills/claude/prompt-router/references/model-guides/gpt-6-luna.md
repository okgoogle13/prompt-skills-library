---
model: gpt-6-luna
vendor: OpenAI
family: GPT
aliases: [luna, gpt6-luna, 6-luna]
last_verified: 2026-11-13
status: current
---

# GPT-6 Luna

## ChatGPT plan and Codex CLI availability

- GPT-6 Luna is the model OpenAI names for Free and Go after the GPT-5.5 Codex retirement, but the current Go plan page specifically documents **Standard-speed access in the ChatGPT desktop app, subject to rollout**.
- The general model catalogue documents Luna for Codex surfaces, including CLI, but that does **not** establish that every plan can use it in every client. Go-specific CLI access is not explicitly guaranteed in the current plan documentation.
- **This user's ChatGPT Go Codex CLI picker (reported 2026-11-13) includes selectable `gpt-6-luna`.** This is account-specific observed availability. Public plan documentation has described Go Luna access in the desktop app; use the live `/model` picker as the source of truth for this user's CLI entitlement and re-check after rollouts or CLI updates.
- Open Codex CLI and run `/model`; use only models shown for the signed-in account. Use `/status` to confirm the active model. A `--model` flag or `config.toml` entry cannot grant plan entitlement.
- Go's documented Luna access is Standard speed in the desktop app. Do not imply Go includes Fast or Ultrafast speed tiers.

## Codex CLI: practical use

- **Best fit:** focused, repeatable, high-volume tasks: code explanation, targeted edits, extraction, classification, transformations, test generation for a narrow change, and structured summaries.
- **Prompt shape:** state the exact outcome, point to the relevant files or symbols, specify constraints, and define a concrete completion check. Keep the task bounded; avoid lengthy generic role instructions.
- **Effort:** start with the CLI's displayed default. Use Low for straightforward, reversible edits; Medium for normal multi-step tasks; High/Max only when debugging or reasoning complexity justifies the added latency. The CLI picker is authoritative for the effort levels actually supported.
- **Do not confuse Max with Ultra:** Luna supports up to Max, not Ultra, in the current model guidance. Ultra is a separate multi-agent mode and is not a Luna option.
- **Escalate selectively:** move to Terra for a task needing stronger general-purpose capability, or to a higher-capability model available to the account when the task involves difficult architecture, ambiguous requirements, or sustained multi-stage reasoning.
- **API-only boundary:** `reasoning.effort`, `reasoning.mode`, `reasoning.context`, `configuration_update`, API token limits, pricing, endpoints and hosted Responses tools below are API details. They are not CLI flags or proof of CLI entitlements.

## Reasoning / Thinking
- `reasoning.effort` accepts `none | low | medium (Default) | high | xhigh | max`. Unlike GPT-6 Astra and GPT-6.1 Sol, **`none` is allowed** ("GPT-6 Sol and GPT-6 Luna support `none`"). Choice per the deployment checklist: `low` for extraction, routing, classification or routine rephrasing; `medium`/`high` when the model must diagnose, weigh options or plan; `xhigh`/`max` only with a quality gain proven by evals.
- **Codex CLI**: reasoning levels are client- and model-dependent. The current model documentation says Luna supports up to `Max`, but not `Ultra`. Open `/model` in the CLI and use the levels actually offered there; do not assume a fixed list or a default for every Go CLI installation.
- `reasoning.mode` `standard` (Default) | `pro`: the reasoning guide states this for "GPT-5.6 and GPT-6 models" (Responses API only); Luna is not named individually there — for Luna (unverified), test before production use.
- `configuration_update` (change effort mid-conversation without rewriting the prompt prefix) is documented for the "GPT-6 model family in standard, single-agent mode", with the same limits as for Astra (no adjacent updates, no automatic compaction/truncation). Luna is not named individually (unverified).
- `reasoning.context`: the reasoning guide lists `all_turns` only for GPT-5.6 models and GPT-6.1 Sol; for Luna it is not documented (unverified) — set `auto` and check the response field `reasoning.context`. Persisted reasoning is reused only within the same model family; on a family switch the API discards incompatible reasoning items.
- Reasoning tokens are invisible but occupy context and are billed as output tokens; `max_output_tokens` caps reasoning and answer together (starting reserve per the docs at least 25,000 tokens).

## Prompting Style
- There is no separate Luna prompting guidance. The GPT-6 prompts in the model guide are explicitly "a starting point across the GPT-6 model family", but address "behavior observed with GPT-6 Astra" — so adopt the autonomy building block, skill precedence sentence, prose instruction, slop-word ban and test-scope rules only after your own evals; that Luna shows the same quirks is not verified (unverified).
- Name task shapes that suit Luna: OpenAI recommends `gpt-6-luna` "for efficient, repeatable work" and advises not to route every request to the strongest model. Keep prompts tightly scoped to one clearly bounded task and specify the output format explicitly (Structured Outputs is supported).
- Level of detail: the deployment checklist names `text.verbosity` (`low`/`medium`/`high`) "the main lever for balancing brevity against completeness" and content/structure/length in the prompt; its example uses Astra, and is not verified individually for Luna (unverified).

## Strengths & Weaknesses (prompt-relevant)
- Positioning: "Our most efficient model for focused, high-volume tasks." In the model guide "Fastest and most cost-effective" with "Strong performance for focused, high-volume tasks."; in the catalogue for "cost-sensitive, high-volume workloads".
- The Decisions API launched in beta on 6 Oct 2026 with `gpt-6-luna`: "Turn text and images into typed answers 10x faster than the Responses API." For prompts with a fixed answer type, check it as an alternative to the Responses API.
- Same Responses tool set as Astra (`web_search`, `file_search`, `image_generation`, `code_interpreter`, `hosted_shell`, `apply_patch`, `skills`, `computer_use`, `mcp`, `tool_search`). EU data residency with Standard, Fast, Flex and Batch (Regional Processing +10%).
- Weaknesses: not the tier for the hardest work — the highest capability sits with `gpt-6-astra`, and complex coding/professional work at lower cost with `gpt-6.1-sol`. Image understanding was impaired until an encoding fix on 25 Sep 2026; OpenAI recommends re-running evals with image input afterwards.

## Output & Format Conventions
- Context window 1,050,000 tokens, max. 922,000 input and 128,000 output; knowledge cutoff 18 May 2026. Input text + image, output text. Only snapshot: `gpt-6-luna`.
- Prices per 1M tokens: input $0.10, cached input $0.01, cache writes $0.125, output $0.50. Above 272K input tokens, 2× input/cache and 1.5× output rates apply to the entire request; Batch/Flex 50%, Fast mode 2×.
- Endpoints: Chat Completions, Responses, Batch (no Realtime, Assistants, fine-tuning, embeddings, audio, moderation). Built-in tools and function calling via the Responses API; **Chat Completions supports function calling only with `reasoning_effort: "none"`**.
- If effort is not `none`, remove `temperature`, `top_p` and `top_logprobs` (on Chat Completions also `logprobs`; on Responses `message.output_text.logprobs` from `include`).
- Prompt caching (GPT-5.6 and newer): cache lifetime via `prompt_cache_options.ttl` (`"30m"`), explicit breakpoints possible, cache writes 1.25× input rate, minimum prefix 1,024 visible input tokens.

## Migration Notes
- **AWAY FROM gpt-6-luna**: `reasoning.*`, `configuration_update` and Decisions API calls are OpenAI-specific and drop out for non-OpenAI targets. For target `gpt-6-astra` or `gpt-6.1-sol`: `none` → `low`, move function calling from Chat Completions to Responses, remove sampling parameters. Reasoning items from Luna histories do not carry into other families.
- **TO gpt-6-luna**: official replacement for `gpt-5.4-nano` (deprecated 1 Oct 2026, shutdown 1 Apr 2027). (1) Set `model` to `gpt-6-luna`. (2) Keep the effective effort; `none` continues to work, `minimal` → `low` and compare. (3) Tools: with effort ≠ `none`, use the Responses API. (4) With effort ≠ `none`, remove sampling/logprob parameters. (5) From GPT-5.5 or older: `prompt_cache_retention` → `prompt_cache_options.ttl: "30m"`. (6) Use Astra prompt building blocks only as a starting point and evaluate them. (7) Re-run image-input evals. (8) For a measured quality gap, escalate to `gpt-6.1-sol` or `gpt-6-astra`.
- From `gpt-5.6-luna`: no official successor mapping; GPT-6 Luna is cheaper ($0.10/$0.50 instead of $0.20/$1.20). Do not take GPT-5.6 reasoning items and a familiar `all_turns` over unchecked.

## Sources
- https://developers.openai.com/api/docs/models/gpt-6-luna — model page: id `gpt-6-luna` (single snapshot), tagline, effort `none`–`max` (default `medium`), function calling in Chat Completions only with `none`, 1,050,000/922,000/128,000 tokens, cutoff 18 May 2026, prices incl. cache writes, 272K rule, Batch/Flex/Fast, EU residency, endpoint matrix, feature and tool lists.
- https://developers.openai.com/api/docs/models.md — catalogue: Luna as featured model "for cost-sensitive, high-volume workloads" next to Astra and GPT-6.1 Sol.
- https://developers.openai.com/api/docs/guides/latest-model.md — GPT-6 model guide (rolling page, as of 2026-10-13): "Fastest and most cost-effective", `none` for Sol/Luna, function-calling and sampling rules, prompt caching switch-over, Fast mode EU residency, prompts as a starting point for the family based on Astra observations.
- https://developers.openai.com/api/docs/guides/reasoning — Luna default `medium`, `reasoning.mode` for "GPT-5.6 and GPT-6 models", `configuration_update` for the GPT-6 family, `all_turns` only GPT-5.6/GPT-6.1 Sol, reasoning reuse only within a family, billing and the 25,000-token reserve.
- https://developers.openai.com/api/docs/guides/deployment-checklist — effort choice by task type, `gpt-6-luna` "for efficient, repeatable work", `text.verbosity`, configuration_update for GPT-6 in standard/single-agent mode.
- https://developers.openai.com/api/docs/guides/prompt-caching — differences from GPT-5.6: `prompt_cache_options.ttl` `"30m"`, breakpoints, 1.25× cache writes, 1,024-token minimum prefix.
- https://developers.openai.com/api/docs/changelog.md — release of `gpt-6-luna` on 22 Sep 2026, image encoding fix with eval recommendation on 25 Sep 2026, Decisions API (beta) with `gpt-6-luna` on 6 Oct 2026.
- https://developers.openai.com/api/docs/deprecations — entry 1 Oct 2026: `gpt-5.4-nano` → `gpt-6-luna`, shutdown 1 Apr 2027.
