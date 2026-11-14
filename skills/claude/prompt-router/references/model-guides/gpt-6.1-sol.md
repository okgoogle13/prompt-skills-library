---
model: gpt-6.1-sol
vendor: OpenAI
family: GPT
aliases: [sol, gpt6.1-sol, 6.1-sol, gpt-6-1-sol]
last_verified: 2026-10-13
status: current
---

# GPT-6.1 Sol

## Surface scope: API versus ChatGPT Codex

This guide contains substantial **OpenAI API** documentation. Do not apply API parameters or API limits directly to ChatGPT Codex CLI.

### ChatGPT Codex surface

- Model ID: `gpt-6.1-sol`.
- Plan eligibility: OpenAI's launch documentation lists Plus, Pro, Business, Enterprise and Edu. **Free and Go are excluded at launch.** Do not recommend this model as available to a ChatGPT Go subscriber.
- Codex context window: **500,000 tokens**. The 1,050,000-token figure below is the API model context, not the Codex context.
- Codex CLI reasoning controls are selected in the CLI model picker. Current documented effort guidance: Low for quick, well-scoped work; Medium for balanced planning; High or Extra High for difficult, multi-step work. Max and Ultra are only options when exposed by the selected model, client and account.
- Speed: Standard and Fast are available where supported. Ultrafast is restricted to eligible higher plans/workspaces and is not a Go entitlement. Speed is a client/model setting, not something to request in prompt prose.
- Codex uses its own agent, repository, terminal and approval environment. Do not infer that a hosted Responses API tool listed later in this guide is available as a Codex CLI tool.

### Codex prompting baseline

Use the smallest prompt that gives Codex the information needed to act. For substantial repository work, specify:

1. **Goal** — the change or result required.
2. **Context** — relevant files, folders, documentation, examples, errors or reproduction steps.
3. **Constraints** — required conventions, compatibility, scope, exclusions and safety boundaries.
4. **Done when** — observable completion criteria, such as tests passing or a bug no longer reproducing.

Add a verification step when the task warrants it. Avoid prescribing an elaborate plan for a small, reversible change. Do not ask for generic summaries or extra deliverables unless useful to the task.

### API-only details below

Unless explicitly marked otherwise, `reasoning.effort`, `reasoning.mode`, `reasoning.context`, `configuration_update`, Responses API tool lists, API endpoints, API context limits, token prices and API service tiers describe API integration. They are not Codex CLI prompt syntax or subscription entitlements.

## Reasoning / Thinking
- `reasoning.effort` (Responses) or `reasoning_effort` (Chat Completions) accepts `low | medium (Default) | high | xhigh | max`. **"The `none` and `minimal` reasoning efforts are not supported"** — docs instruction for those switching: replace `none` with `low`; with `minimal`, start with `low` and compare results.
- `reasoning.mode`: `standard` (Default) or `pro` — GPT-5.6 and GPT-6 models support both modes in the Responses API; mode and effort are independent, and pro tokens are billed at the standard rates.
- `reasoning.context`: `auto | current_turn | all_turns`; per the docs GPT-6.1 Sol supports `all_turns` (renders compatible reasoning items from earlier turns). Whether `auto` resolves to `all_turns` or `current_turn` here is not stated (unverified) — check the effective mode in the `reasoning.context` field of the response. Persisted reasoning is reused only within the same model family.
- Effort can be changed mid-conversation via a `configuration_update` item without rewriting the prompt prefix (and thus the cache) — supported for the GPT-6 family only in standard, single-agent mode; do not combine with automatic compaction/truncation.

## Prompting Style
- OpenAI provides no separate Sol prompting guide; the GPT-6 prompts are explicitly "a starting point across the GPT-6 model family", but address "behavior observed with GPT-6 Astra". Any transfer of the Astra quirks below to 6.1 Sol is therefore (unverified) and must be confirmed with evals.
- Building blocks from the GPT-6 guide: grant autonomy explicitly ("bias towards action and carry the user's intended task to completion"); request approval only after "a concrete, reviewable result"; spell out precedence over skills/files ("The user's instructions take precedence over guidelines provided in a skill."); explicitly request prose when no Markdown is wanted; forbid slop words and contrastive framing; actively steer delegation to subagents; limit test scope for small, reversible changes.
- Tool calling only via the Responses API — tool instructions in the prompt presuppose a Responses request.

## Strengths & Weaknesses (prompt-relevant)
- Positioning: "Near-Astra performance for complex work at a lower cost" — in OpenAI's flagship group the middle tier, "Balanced speed, cost, and intelligence", between GPT-6 Astra and GPT-6 Luna; intended for "complex coding, computer use, and professional work". OpenAI recommends comparing against Astra on your own tasks. Caution: with GPT-5.6, "Sol" was the top tier; with GPT-6 it is the middle tier.
- Per the model selection guide: Medium for "Complex technical work and coordinated deliverables you expect to revise", Extra high for "Polished deliverables, connected visual systems, and decisions built from conflicting evidence".
- Multi-agent (delegation to subagents within one Responses request) available in **beta**.
- Ultrafast mode: `service_tier: "ultrafast"` only in the Responses API, with US and EU data residency as well as global processing; 6x the standard price. Fast mode also with EU data residency.
- Limitations: no `none`/`minimal` effort; Chat Completions without tool calling; not supported are, among others, Realtime, Assistants, fine-tuning, embeddings, image/video/audio endpoints, moderation, legacy completions and `predicted_outputs`.

## Output & Format Conventions
- **API context window**: 1,050,000 tokens, max. input 922,000, max. output 128,000. **Codex context window: 500,000 tokens.** Knowledge cutoff **30 Apr 2026**; input text + image, output text only. Only snapshot: `gpt-6.1-sol`.
- Endpoints: `v1/chat/completions` (without tools), `v1/responses`, `v1/batch`. Features: streaming, structured_outputs, function_calling, file_search, image_input, web_search, prompt_caching. Hosted tools (Responses): web_search, file_search, image_generation, code_interpreter, hosted_shell, apply_patch, skills, computer_use, mcp, tool_search.
- Prices per 1M tokens: input $2, cached input $0.1 (5% of the input rate), cache writes $2.5 (1.25x), output $10. Above 272K input tokens: 2x input/cache rates and 1.5x output for the entire request. Fast 2x, Batch/Flex −50%, Ultrafast 6x.
- Prompt caching: lifetime via `prompt_cache_options.ttl` (only value `"30m"`, also the default) instead of `prompt_cache_retention`.
- Pin the output format with Structured Outputs or an explicit format instruction; the GPT-6 guide describes a tendency toward lists, tables and Markdown for Astra — for 6.1 Sol this is (unverified).

## Migration Notes
- **AWAY FROM gpt-6.1-sol**: map effort onto the target guide's ladder (carry over `xhigh`/`max` only if the target documents them); remove or rewrite `reasoning.mode`, `reasoning.context`, `configuration_update`, multi-agent beta and `service_tier: "ultrafast"` into target equivalents; translate `prompt_cache_options.ttl` into the target's cache syntax; check autonomy/precedence/prose building blocks taken from the GPT-6 guide as needed; scale the 1.05M-token context budget back to the target window.
- **TO gpt-6.1-sol**: (1) set `model` to `gpt-6.1-sol`. (2) Keep the previous effective effort where supported; `none` → `low`; start `minimal` with `low` and compare. (3) Move tool calling to the Responses API. (4) If effort is not `none`: remove `temperature`, `top_p`, `top_logprobs`; on Chat Completions also `logprobs`; on Responses `message.output_text.logprobs` from `include`. (5) Coming from GPT-5.5 or earlier: `prompt_cache_retention` → `prompt_cache_options.ttl: "30m"`. (6) Implement effort changes via `configuration_update` rather than a per-request parameter. (7) Where approval pauses occur, add the autonomy building blocks from the GPT-6 guide.
- **From gpt-6-sol**: OpenAI explicitly requires "review the migration guidance before switching to GPT-6.1 Sol" — mainly because 6-Sol allows both `none` and Chat Completions function calling (only with `none`), whereas 6.1 Sol allows neither.
- **From gpt-5.6-sol**: the alias name "Sol" stays, but the tier drops from flagship to middle tier; for maximum quality, test against gpt-6-astra instead.

## Sources
- https://developers.openai.com/api/docs/models/gpt-6.1-sol — model page: id/snapshot `gpt-6.1-sol`, "Near-Astra performance for complex work at a lower cost", effort levels including "The `none` and `minimal` reasoning efforts are not supported", Chat Completions without tool calling, Ultrafast/data residency, 1,050,000 / 922,000 / 128,000, cutoff 30 Apr 2026, prices and factors, endpoints, features, tools, `predicted_outputs` not supported.
- https://developers.openai.com/api/docs/guides/latest-model — "Using GPT-6" (rolling page, as of 2026-10-13): tier labels, GPT-6.1 Sol section, prompting best practices "across the GPT-6 model family" with Astra reference, limitations, migration quickstart (effort, tool calling, unsupported parameters, data residency, `configuration_update`, `prompt_cache_options.ttl`), note on `gpt-6-sol`.
- https://developers.openai.com/api/docs/guides/reasoning — effort table, 6.1 Sol default `medium` and missing `none`/`minimal`, `reasoning.mode` for GPT-5.6/GPT-6, `reasoning.context` with `all_turns` support for GPT-6.1 Sol, `configuration_update` (standard, single-agent mode).
- https://developers.openai.com/api/docs/guides/model-selection — "When to consider GPT-6.1 Sol" and effort recommendations Medium / Extra high.
- https://developers.openai.com/api/docs/guides/responses-multi-agent — multi-agent as beta "with GPT-6.1 Sol and all GPT-5.6 models".
- https://developers.openai.com/api/docs/guides/ultrafast-mode — Ultrafast for GPT-6 Astra and GPT-6.1 Sol, `service_tier: "ultrafast"`.
- https://developers.openai.com/api/docs/guides/prompt-caching — `prompt_cache_options.ttl` (`"30m"`) for GPT-5.6 and later, cache read 0.05x for GPT-6.1 Sol, cache write 1.25x.
- https://developers.openai.com/api/docs/changelog — 29 Sep 2026: release of `gpt-6.1-sol` "for complex coding and professional work at a lower cost than GPT-6 Astra", multi-agent beta; 8 Oct 2026: Ultrafast for GPT-6.1 Sol (Responses API, global as well as US/EU residency).
