---
model: gemini-deep-research-argon
vendor: Google
family: Gemini
aliases: [deep-research-argon, gemini-dr-argon, argon-deep-research, gemini-argon-deep-research]
last_verified: 2026-11-07
status: current
---

# Gemini Deep Research (Argon)

> ⚠ Note: Deep Research is an **agent** of the Interactions API, not a model name. A documented binding "Deep Research runs on `gemini-4-argon`" could **not** be verified (unverified). This guide describes (a) the Deep Research agent and (b) how to phrase a prompt when Argon is chosen as planner or synthesis model, or when the agent's results are processed further with Argon. Check AI Studio and the documentation before production use.

## Reasoning / Thinking
- The Deep Research agent independently plans sub-questions, iteratively runs many searches, reads sources and synthesises a cited report. `thinking_level` is not set for the agent (not documented, unverified).
- For Argon itself (follow-up processing, review of the report): `thinking_level` `low | medium | high`, default `medium`, `minimal` invalid; `max_output_tokens` ≥ 32,768 (see guide `gemini-4-argon`).
- Runs **asynchronously**: `client.interactions.create(agent=..., input=..., background=True)`, then poll status via `client.interactions.get(id)` (`completed` / `failed`); result in `outputs[-1].text`. Synchronous `generateContent` is not the way.
- Agent IDs per research: `deep-research-preview-04-2026` (fast and efficient, UI streaming) and `deep-research-max-preview-04-2026` (maximum thoroughness). An older example names `deep-research-pro-preview-12-2025`. IDs are preview and may change — check against the current documentation.

## Prompting style
- **Research brief, not chat**: goal, guiding question, scope (time period, region, industry), desired report outline and source requirements in one prompt. Specify the outline explicitly (e.g. "1. Market situation, 2. Pricing models, 3. Changes in the last 6 months").
- **Collaborative planning**: `collaborative_planning=True` first returns a research plan for approval; send corrections back via `previous_interaction_id` (parameter name per research, verify before use).
- No manual "Think step by step"; the agent plans itself. Concrete, narrowly scoped questions instead of vague topics.
- Your own documents or PDFs can be attached as multimodal input; put the task and questions at the end, after the reference data.
- Standard tone is factual and concise; state the detail level and readership explicitly.
- Allow uncertainty: explicitly permit writing "not verifiable" instead of guessing.

## Strengths & weaknesses (prompt-relevant)
- Strengths: multi-step research with dozens of search steps, cited structured reports, interactive plan approval.
- Weaknesses: runtime of several minutes; preview status; binding to Argon or 3.8 Flash not verified; costs and tokens hard to estimate in advance (unverified).

## Output & format conventions
- Output: Markdown report with source citations as text in the last output.
- No prefill, no sampling parameters (remove `temperature`, `top_p`, `top_k`, `candidate_count`).

## Migration notes
- **FROM Deep Research (Argon)**: remove background and polling logic and `collaborative_planning`; a target system without agents needs explicit research steps, search tool and source rules in the prompt; the outline remains as the output contract.
- **TO Deep Research (Argon)**: reduce the prompt to guiding question, scope, outline and source rules; remove CoT and tool instructions ("search first ..."); use the asynchronous call (`background=True`); optionally build in plan approval; if needed, verify the result with `gemini-4-argon` (`thinking_level: high`).

## Sources
- https://ai.google.dev/gemini-api/docs/deep-research — Deep Research agent, Interactions API, `background=True`, polling, agent IDs, collaborative planning (summarised from web search, not directly retrieved).
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — Argon model card (see guide `gemini-4-argon`).
