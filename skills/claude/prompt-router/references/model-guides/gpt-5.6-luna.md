---
model: gpt-5.6-luna
vendor: OpenAI
family: GPT
aliases: [gpt5.6-luna, 5.6-luna]
last_verified: 2026-11-13
status: current
---

# GPT-5.6 Luna

## Codex CLI: practical use

- **Availability:** the user's ChatGPT Go Codex CLI picker reports `gpt-5.6-luna` as selectable (2026-11-13). OpenAI's current public plan matrix does not explicitly list GPT-5.6 Luna for Go in Codex, so record this as account/client-specific observed access rather than a universal Go entitlement; verify with `/model` after updates.
- **Best fit:** the fastest, lowest-cost GPT-5.6 tier for simple, repeatable tasks: small code edits, quick explanations, narrow extraction/classification, formatting and routine transformations.
- **Avoid:** assigning it ambiguous, high-impact, broad architectural or long-horizon tasks by default. Escalate to Terra when a task needs stronger general-purpose reasoning; use a higher-capability model if available for difficult reasoning.
- **Prompt shape:** keep requests concise but complete. Specify the exact change, file/scope, constraints and one or two observable checks. Do not rely on elaborate prompt scaffolding to compensate for a smaller model.
- **Effort:** use the CLI's displayed default for routine work. Increase effort only when the task needs diagnosis or multi-step reasoning; select only options shown in `/model`. Do not assume API effort values map one-to-one to CLI labels.
- **API-only boundary:** `reasoning.mode`, `reasoning.context`, `text.verbosity`, API token limits, pricing, endpoints, cache settings and hosted Responses tools below describe the API, not Codex CLI controls.

## Reasoning / Thinking
- `reasoning.effort`: `none | low | medium (Default) | high | xhigh | max` — same ladder as `gpt-5.6-sol` and `gpt-5.6-terra`. Family guidance: `medium` as the balanced start, `low` for latency-critical workloads; if you use `none`, keep it as the latency baseline and additionally test `low` when reasoning or tool use helps.
- **Codex CLI**: supported reasoning levels: `low`, `medium`, `high`, `extra high` (corresponds to `xhigh`). Default `medium`.
- `reasoning.mode` = `standard` (Default) | `pro`, independent of effort; "Pro mode works with any GPT-5.6 model" (Responses API only). The docs explicitly recommend `standard` for "routine, latency-sensitive, or high-volume work" — which fits Luna's usage profile.
- `reasoning.context` = `auto | current_turn | all_turns`, default `all_turns` for GPT-5.6 models. Reasoning items are reusable between `gpt-5.6-sol`, `gpt-5.6-terra` and `gpt-5.6-luna`, but not across family boundaries (e.g. GPT-5.5).
- `configuration_update` (changing effort mid-conversation) is documented only for the GPT-6 family, not for GPT-5.6.

## Prompting Style
- There is no separate Luna guidance; per OpenAI the GPT-5.6 prompt rules apply to the family (family transfer; the measurements come from internal coding-agent evals, not Luna-specific tests).
- **Lean prompts:** state each instruction once, trim redundant examples and tool descriptions, expose only relevant tools. OpenAI reports ~10–15% better eval scores at 41–66% fewer tokens and calls the ranges "directional".
- Length: GPT-5.6 is inherently more concise than GPT-5.5; re-check blanket "Be concise" lines. Set the default level of detail via `text.verbosity`, and state in the prompt what a short answer must contain ("Keep all required facts, decisions, caveats, and next steps.").
- Set autonomy and approval limits in one place: name safe local actions explicitly as allowed, and require confirmation for "external writes, destructive actions, purchases, or a material expansion of scope".

## Strengths & Weaknesses (prompt-relevant)
- Positioning: "designed for cost-sensitive, high-volume workloads" and "roughly corresponds to the nano model tier used in earlier GPT-5 families"; in the reasoning guide, the choice "for the lowest cost and latency".
- Family strengths: per the docs GPT-5.6 reaches flagship-level performance with fewer output tokens and infers user goals and scope of work from context better. How far this carries at the nano tier is not verified (unverified).
- Full Responses tool set (`web_search`, `file_search`, `image_generation`, `code_interpreter`, `hosted_shell`, `apply_patch`, `skills`, `computer_use`, `mcp`, `tool_search`); images at original resolution via `original`/`auto` detail.
- Weaknesses: the family's smallest tier — for a measured quality gap, use `gpt-5.6-terra` (mini tier) or `gpt-5.6-sol`. Family-wide safeguards can pause generation mid-stream for several seconds or block requests; design timeouts and streaming accordingly.

## Output & Format Conventions
- Context window 1,050,000 tokens, max. 922,000 input and 128,000 output; knowledge cutoff 16 Feb 2026. Input text + image, output text. Only snapshot `gpt-5.6-luna`, no dated snapshot.
- Prices per 1M tokens: input $0.20, cached input $0.02, output $1.20; cache writes 1.25× input rate; above 272K input tokens 2× input and 1.5× output for the entire request.
- Endpoints: Chat Completions, Responses, Batch. Features: streaming, structured outputs, function calling, file search, image input, web search, prompt caching. For reasoning, tool calling and multi-turn, OpenAI recommends the Responses API.
- `text.verbosity` = `low | medium | high` as the default level of detail.
- Prompt caching (GPT-5.6 and newer): `prompt_cache_options.ttl` (`"30m"`) instead of `prompt_cache_retention`, explicit breakpoints possible, minimum prefix 1,024 visible input tokens.

## Migration Notes
- **AWAY FROM gpt-5.6-luna**: remove `reasoning.effort`/`mode`/`context` and `text.verbosity` if the target does not know them; re-word brevity and format rules that `text.verbosity` was carrying; scale context assumptions (1.05M) back to the target. Persisted reasoning items do not carry into other families.
- **TO gpt-5.6-luna**: official replacement for `gpt-4.1-nano`/`gpt-4.1-nano-2025-04-14` (shutdown 23 Oct 2026) and `gpt-5-nano-2025-08-07` (shutdown 11 Dec 2026). (1) Effort baseline: keep the current effort from GPT-5.5/5.4 and test one level lower; that this also holds for nano sources is an extrapolation (unverified). (2) Slim the prompt; cut few-shot stacks and long tool descriptions. (3) Re-test blanket brevity lines; default via `text.verbosity`. (4) Responses API for reasoning and tools. (5) `prompt_cache_retention` → `prompt_cache_options.ttl`. (6) Add autonomy/approval limits.
- Positioning: moving up within the family goes via `gpt-5.6-terra` (replacement for `gpt-5-mini`) to `gpt-5.6-sol`. OpenAI now lists GPT-6 Luna (`gpt-6-luna`) as a featured model for cost-sensitive volume workloads; there is no official successor mapping for `gpt-5.6-luna` (as of 2026-10-13).

## Sources
- https://developers.openai.com/api/docs/models/gpt-5.6-luna — model page: id `gpt-5.6-luna`, positioning ("cost-sensitive, high-volume workloads", nano tier), effort `none`–`max` (default `medium`), 1,050,000/922,000/128,000 tokens, cutoff 16 Feb 2026, prices $0.2/$0.02/$1.2, 272K rule, cache writes, endpoints, features, tools, single snapshot.
- https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.6-sol — GPT-5.6 section (applies to the family): lean prompts (10–15% / 41–66%), brevity rules, `text.verbosity`, autonomy limits, effort migration, `reasoning.context` default `all_turns`, pro mode "works with any GPT-5.6 model" and standard for volume work, safeguard pauses, family strengths.
- https://developers.openai.com/api/docs/guides/reasoning — `gpt-5.6-luna` "for the lowest cost and latency", `reasoning.mode` standard/pro for GPT-5.6, default `medium`, reasoning reuse between sol/terra/luna, `configuration_update` GPT-6 only.
- https://developers.openai.com/api/docs/guides/prompt-caching — differences from GPT-5.6: `prompt_cache_options.ttl` `"30m"`, breakpoints, 1.25× cache writes, 1,024-token minimum prefix.
- https://developers.openai.com/api/docs/deprecations — `gpt-4.1-nano`/`gpt-4.1-nano-2025-04-14` → `gpt-5.6-luna` (23 Oct 2026), `gpt-5-nano-2025-08-07` → `gpt-5.6-luna` (11 Dec 2026), `gpt-5-mini-2025-08-07` → `gpt-5.6-terra`; no entry for `gpt-5.6-luna` itself.
- https://developers.openai.com/api/docs/models.md — catalogue: GPT-6 Luna as featured model, GPT-5.6 Luna still in the full catalogue.
- https://developers.openai.com/api/docs/changelog.md — release of the GPT-5.6 family on 9 Jul 2026 with "GPT-5.6 Luna for efficient, high-volume workloads".
