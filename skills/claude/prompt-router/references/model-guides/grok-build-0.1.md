---
model: grok-build-0.1
vendor: xAI
family: Grok
aliases: [grok-code-fast-1, grok-code-fast, grok-code-fast-1-0825, grok-build-0-1]
last_verified: 2026-10-13
status: current
---

# Grok Build 0.1

## Reasoning / Thinking
- Type: **reasoning model with no documented control.** The model page lists "Reasoning: Yes" but names no effort levels; the summary table on the reasoning page also lists only grok-4.7, grok-4.6, grok-4.5 and grok-4.20-multi-agent. Whether `reasoning_effort` is accepted, ignored or rejected is not documented (unverified). Equally unverified: the default depth and whether reasoning can be switched off.
- Per the reasoning page, reasoning tokens are generally billed too ("the reasoning tokens are billed as part of your total consumption").
- Class rule from the reasoning page: "`presencePenalty`, `frequencyPenalty`, and `stop` cannot be used with reasoning models. Requests that include them return an error." grok-build-0.1 is not named there, but carries the reasoning flag — so omit the parameters as a precaution.
- xAI only describes readable reasoning summaries for grok-4.7; whether grok-build-0.1 returns `reasoning.encrypted_content` ("Some models can") is not verified (unverified). Pipelines that evaluate a reasoning trace should not rely on anything here.

## Prompting style
- Positioning per the announcement: "a coding model specifically trained for agentic coding tasks, including web development, debugging, and MCP support"; outside coding "a speedy, economical option for general-purpose agentic and tool calling use cases". Accordingly prompt **agentically and task-oriented**, not as a general-purpose chat.
- The announcement says the model "performs best in agentic harness" (naming Grok Build, Cursor, OpenCode among others). Prompts for pure single-shot chats without a tool loop therefore fall outside the profile xAI positions it for.
- Steer tool selection via the **tool definitions**: a tool's description "helps the model decide when to use it". Parallel tool calling is on and is turned off with `parallel_tool_calls: false`.
- Enforce format via **Structured Outputs** (`response_format.type: "json_schema"`): "the response is guaranteed to match your schema" — with the documented limits (string length 2,048, arrays 256, 64 properties; `not` and `if`/`then`/`else` only best-effort).
- Prompt caching runs automatically from the start of the `messages` array: keep the static prefix (system prompt, tool definitions) first and unchanged, and set `x-grok-conv-id` or `prompt_cache_key`.
- No model-specific prompting guidance for grok-build-0.1 or grok-code-fast-1 can be found in current xAI docs; any further style claim is (unverified).

## Strengths & weaknesses (prompt-relevant)
- Strengths: **cheapest xAI coding model** on the roster ($1.00 input / $2.00 output per 1M under 200k); per the announcement "100+ tokens/second"; function calling, structured outputs and image input available; per the retirement guide, "significantly improved agentic coding and web dev capabilities" compared with grok-code-fast-1. No benchmarks are published by the manufacturer.
- Weaknesses/quirks: **smallest context window** of the current Grok text models (256k instead of 500k for grok-4.5/4.6/4.7, or 1M for grok-4.3/4.20); **Batch API "Not supported"**; only us-east-1/us-west-2, no EU region; markedly lower rate limits than the flagships (37 rps / 10M tpm instead of 150 rps / 50M tpm for grok-4.5); no published knowledge cutoff, no published output limit, no effort control. The model overview explicitly recommends grok-4.7 for code, not grok-build-0.1.

## Output & format conventions
- 256,000 tokens context; input text + image, output text only. Max output tokens and knowledge cutoff: not published (unverified).
- Function calling: yes; structured outputs: yes; reasoning: yes; Batch API: "Not supported".
- Prices per 1M tokens: input $1.00 (<200k prompt) / $2.00 (≥200k), cached input $0.20 / $0.40, output $2.00 / $4.00. From 200k prompt tokens the higher rate applies to **all** tokens in the request. Rate limits: 37 requests/s, 10M tokens/min; regions us-east-1, us-west-2.
- Vendor aliases on the model page: `grok-code-fast-1`, `grok-code-fast`, `grok-code-fast-1-0825`. According to xAI, `grok-build-latest` does **not** belong here but is listed on the grok-4.5 model page — so a prompt that addresses "grok-build-latest" does not land on grok-build-0.1.
- Availability status is contradictory: the announcement of 29 May 2026 says "now available via the xAI API in public beta", while the release notes (month "May", no year given) say "Currently in early access"; the model page gives no status. Plan for beta behaviour.

## Migration notes
- **From grok-code-fast-1**: since 15 May 2026, requests to `grok-code-fast-1` are routed to `grok-build-0.1` per the retirement guide; "The slugs themselves continue to resolve". Prompts tuned for grok-code-fast-1 therefore already run on this model — re-evaluate behaviour instead of carrying assumptions about the old model forward (its quirks are no longer described in current docs, unverified).
- **TO grok-build-0.1** (e.g. from grok-4.5/4.6/4.7): (1) Do not plan on `reasoning_effort`/`reasoning.effort` as a lever any more — no level is documented for this model. (2) Remove `presence_penalty`, `frequency_penalty`, `stop` and secure format via structured outputs. (3) Plan context at ≤256k; the 200k price cliff sits close to the context limit. (4) Re-plan batch jobs (not supported). (5) Embed the model in a tool loop/agent harness rather than using it as a general chat model. (6) For hard tasks that previously relied on high reasoning depth, cross-check quality — xAI recommends grok-4.7 for code.
- **FROM grok-build-0.1** (to grok-4.7/4.6): set effort explicitly (there default `high`, cannot be switched off); cost rises to $2/$6 per 1M (<200k); context grows to 500k.
- `logprobs`/`top_logprobs` are silently ignored for "`grok-4.20` and newer" per the overview; whether grok-build-0.1 falls under this is not documented (unverified) — do not build any pipeline on it.
- Grok Build (agent/CLI) ≠ model: the announcement called grok-build-0.1 "the same model that powers Grok Build"; the current Grok Build docs name no default model and allow any model, and the release notes list Grok 4.7 Fast as available in Grok Build. Therefore do not equate "Grok Build" in a prompt with this model.

## Sources
- https://docs.x.ai/developers/models/grok-build-0.1 — Model page: id `grok-build-0.1`, aliases `grok-code-fast-1`/`grok-code-fast`/`grok-code-fast-1-0825`, 256k context, text+image→text, function calling/structured outputs/reasoning yes with no effort options, Batch API "Not supported", price table incl. 200k tier, 37 rps / 10M tpm, regions us-east-1/us-west-2; no cutoff, output limit or status note.
- https://x.ai/news/grok-build-0-1 — Announcement of 29 May 2026: "public beta", "100+ tokens/second", positioning for agentic coding/web dev/debugging/MCP, "performs best in agentic harness", $1/$2 per 1M, "the same model that powers Grok Build"; no benchmarks, no prompting tips.
- https://docs.x.ai/developers/migration/may-15-retirement — Mapping `grok-code-fast-1` → `grok-build-0.1`, "significantly improved agentic coding and web dev capabilities", slugs still resolve.
- https://docs.x.ai/developers/release-notes — Entry "Grok Build 0.1 … Currently in early access" under "May" with no year; Grok Build (agent) "now available in beta"; Grok 4.7 Fast available in Grok Build.
- https://docs.x.ai/developers/model-capabilities/text/reasoning — Summary table without grok-build-0.1, class rule for `presencePenalty`/`frequencyPenalty`/`stop`, billing of reasoning tokens, summaries only for grok-4.7, "Some models can also return encrypted reasoning".
- https://docs.x.ai/developers/models — Price roster (256k), recommendation "For everything else, including code, use Grok 4.7", `logprobs` note for "`grok-4.20` and newer", alias convention.
- https://docs.x.ai/developers/models/grok-4.5 — establishes that `grok-build-latest` is listed as an alias of grok-4.5, not of grok-build-0.1; comparison values 150 rps / 50M tpm.
- https://docs.x.ai/build/overview — Grok Build supports "any custom model", no default model named.
- https://docs.x.ai/developers/tools/function-calling — Tool description "helps the model decide when to use it", `parallel_tool_calls: false` to switch off.
- https://docs.x.ai/developers/model-capabilities/text/structured-outputs — `response_format.type: "json_schema"`, schema guarantee, limits and best-effort keywords.
- https://docs.x.ai/developers/advanced-api-usage/prompt-caching — automatic caching from the start of the `messages` array, `x-grok-conv-id` and `prompt_cache_key`.
