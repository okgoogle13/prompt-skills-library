---
model: glm-5.2
vendor: Z.ai
family: GLM
aliases: [glm52, zhipu-glm-5.2, zai-glm-5.2, zai-org/GLM-5.2, zai-glm-5-2]
last_verified: 2026-10-13
status: legacy
successor: glm-5.3
---

# GLM-5.2

## Reasoning / Thinking
- Type: **switchable, model decides itself**. `thinking: {"type": "enabled" | "disabled"}`, default `enabled`; GLM-5.2 is one of the models that "auto-decide whether to think" — unlike GLM-5.3/5.3-Flash, which force thinking.
- Depth via `reasoning_effort` (only supported from GLM-5.2 onward), default `max`. The full enum is accepted and mapped: `none`/`minimal` → thinking off, `low`/`medium` → `high`, `xhigh` → `max`. Effectively there are only **off / `high` / `max`** — a ported `low` already runs as `high` here. The coding-plan mapping for 5.2 is identical.
- Which effort levels and which fallback apply in the open weights is not stated by the model card (only "multiple thinking effort levels") — unverified.
- Reasoning output: non-streaming as `reasoning_content` alongside `content`; in the stream as `delta.reasoning_content` before `delta.content`.
- Preserved thinking (`clear_thinking: false`) is off by default on the standard API endpoint and on by default on the coding-plan endpoint. If used, the historical `reasoning_content` must be returned completely and unchanged ("All consecutive reasoning_content blocks must exactly match the original sequence").

## Prompting style
- Z.ai positions 5.2 as the flagship "built for the era of long-horizon tasks"; the model page recommends an agentic working pattern:
  - **Codebase audit first**: have the model read the project and output an architecture map with API contracts, data flows and technical debt.
  - **Require a plan before refactorings**: "the execution plan, impact scope, risk boundaries, and verification method" before any change.
  - **Store engineering standards in `CLAUDE.md` / `Agent.md`** (lint rules, build commands, test requirements) rather than in the individual prompt.
  - **Name explicit constraints** (e.g. no new dependencies, do not change API contracts, do not commit on its own).
  - **Order verification**: run build, lint and tests, and report the results plus uncovered risks.
- General Z.ai agent scheme: **Goal**, **Context**, **Constraints**, **Done when**; temporary instructions in the prompt, long-lived rules in project configuration files; one session per task.

## Strengths & weaknesses (prompt-relevant)
- Strengths: long, multi-step tasks with "1M lossless context" — according to the release notes, less drift and goal loss in long runs; Terminal-Bench 2.1 81.0 (GLM-5.1: 62.0), SWE-bench Pro 62.1 (GLM-5.1: 58.4); open weights (MIT licence, 753B parameters).
- Versus the successor: GLM-5.3 uses the same base model and gains solely through post-training — +50% on Z.ai Code Bench, Terminal-Bench 3.0 4.6 (5.2) → 28.3, CyberGym 77.2% → 84.5%, higher token efficiency at max effort (5.2: 23.4% at ~96K output tokens per task; 5.3: 34.5% at ~75K).
- Weaknesses and quirks: **text-only** (input and output text); coarse effort resolution due to the mapping (no real `low`/`medium`); no published knowledge cutoff (unverified).

## Output & format conventions
- 1M tokens context, 128K output (`max_tokens` up to 131072); input text, output text.
- API defaults: `temperature` 1 (0–1), `top_p` 0.95 (0.01–1), `do_sample` `true`. The model page's code examples use `temperature` 1.0 (one streaming example 0.6) — the page gives no separate sampling recommendation.
- Structured output via `response_format: {"type": "json_object"}`; `stop`: schema max. 4, per description currently only one stop word; `tools` max. 128 functions, `tool_choice` only `"auto"`; `tool_stream` supported for tool-call streaming. Cache hits under `usage.prompt_tokens_details.cached_tokens`.
- Price per MTok: input $1.40, cached input $0.26, output $4.40 (identical to GLM-5.3); cached-input storage free for a limited time (as of 2026-10-13). Release-notes entry: 2026-06-16.
- Mistral hosts the model unchanged as `zai-glm-5-2`.

## Migration notes
- **Lifecycle**: Z.ai still lists GLM-5.2 in the price list under "Latest Models" and names no shutdown date; however, the official migration page "Migrate to GLM-5.3" explicitly covers the move from GLM-5.2, and the model card points to GLM-5.3 as the newer version. At Mistral, `zai-glm-5-2` has been deprecated since 29 Sep 2026, replacement GLM 5.3.
- **FROM glm-5.2 to glm-5.3** (official checklist): (1) `thinking.type: "disabled"` → `enabled` + `reasoning_effort: low`, otherwise the request fails. (2) Remove `none`/`minimal`/`medium`/`xhigh` — on 5.3 only `low`/`high`/`max` are valid; a 5.2 `low`/`medium` in effect ran as `high`, so set `high` if behaviour should stay the same. (3) Set `model` to `glm-5.3`, adjust `max_tokens` to 128K. (4) `temperature` 1.0 / `top_p` 0.95, then tune only one of the two. (5) In the stream, process `delta.reasoning_content` and `delta.content` separately; tool calls with `stream` + `tool_stream` and argument concatenation. (6) Verification: answer quality, "excessive randomness or excessive conservatism", tool streaming, latency and cost under long context and deep thinking. Prompt content carries over (same base model); only the thinking contract breaks — and there is no zero-thinking path any more, so re-size the token budget.
- **FROM glm-5.2 to other providers**: resolve the 5.2 mapping — `low`/`medium` here meant `high`, `xhigh` meant `max`, `none`/`minimal` meant thinking off; map onto the effort ladder of the target guide instead of carrying over raw values. Map `clear_thinking`, `tool_stream` and `reasoning_content` handling to the target's conventions.
- **TO glm-5.2**: map thinking control onto `thinking.type` plus `reasoning_effort` (finely graded effort values collapse to off / `high` / `max`); image or multimodal input is not possible (for images use `glm-5.3-flash`); reduce multiple stop sequences to one; remove `tool_choice` values other than `auto`; switch JSON schema requirements to `json_object` plus prompt contract. For new integrations prefer the successor `glm-5.3`.

## Sources
- https://docs.z.ai/guides/llm/glm-5.2 — id `glm-5.2`, "built for the era of long-horizon tasks", 1M context, 128K output, text-in/text-out, capabilities (thinking, streaming, function calling, context caching, structured output), code comment "disabled or enabled, default is enabled", best practices (codebase audit, plan with "the execution plan, impact scope, risk boundaries, and verification method", `CLAUDE.md`/`Agent.md`, explicit constraints, verification), benchmarks Terminal-Bench 2.1 and SWE-bench Pro, sampling in the examples.
- https://docs.z.ai/guides/capabilities/thinking — GLM-5.2 "auto-decide whether to think", `reasoning_effort` from GLM-5.2, default `max`, 5.2 mapping (`none`/`minimal` off, `low`/`medium` → `high`, `xhigh` → `max`) for API and coding plan, `reasoning_content` non-streaming and in the stream.
- https://docs.z.ai/guides/capabilities/thinking-mode — preserved-thinking defaults per endpoint and "All consecutive reasoning_content blocks must exactly match the original sequence".
- https://docs.z.ai/api-reference/llm/chat-completion — text schema with `glm-5.2` in the model enum: `thinking.type` default `enabled`, `reasoning_effort` enum and 5.2 mapping, `temperature`/`top_p` defaults, `max_tokens` up to 131072, `stop` (max. 4, "Currently, only one stop word is supported"), `tools` max. 128, `tool_choice` only `auto`, `response_format` `json_object`, `tool_stream` for GLM-5.2, `usage.prompt_tokens_details.cached_tokens`.
- https://docs.z.ai/guides/overview/migrate-to-glm-new — "Migrate to GLM-5.3": move from GLM-5.2 and older, checklist (model string, thinking, effort, sampling, streaming, tool streaming, limits, verification incl. "excessive randomness or excessive conservatism").
- https://docs.z.ai/guides/llm/glm-5.3 — breaking change to `thinking.type: "disabled"`, "same base model as GLM-5.2", comparison figures 5.2 vs. 5.3 (Z.ai Code Bench, Terminal-Bench 3.0, CyberGym 77.2% → 84.5%, token efficiency).
- https://docs.z.ai/guides/overview/pricing — GLM-5.2 under "Latest Models": $1.4/$0.26/$4.4, cached-input storage "Limited-time Free".
- https://docs.z.ai/release-notes/new-released — 2026-06-16 GLM-5.2, "Supports 1M lossless context", less drift and goal loss in long tasks.
- https://huggingface.co/zai-org/GLM-5.2 — official model card: MIT licence, 753B parameters, "multiple thinking effort levels" without a list of values, note "A newer version of this model is available" (GLM-5.3).
- https://docs.mistral.ai/models/zai-glm-5-2 — Mistral hosting `zai-glm-5-2` without modifications, "This model is deprecated. Use Z.ai GLM 5.3 for new integrations.", deprecation 29 Sep 2026, replacement Z.ai GLM 5.3.
- https://docs.z.ai/devpack/resources/best-practice — Goal/Context/Constraints/Done when, temporary vs. long-lived instructions, session hygiene (formulated model-independently).
