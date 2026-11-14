---
model: gemini-deep-research-3.8-flash
vendor: Google
family: Gemini
aliases: [deep-research-3.8-flash, gemini-dr-flash, flash-deep-research, gemini-3.8-flash-deep-research, deep-research-flash]
last_verified: 2026-11-07
status: current
---

# Gemini Deep Research (3.8 Flash)

> ⚠ Note: Deep Research is an **agent** of the Interactions API, not a model name. A documented binding "Deep Research runs on `gemini-3.8-flash`" could **not** be verified (unverified). This guide describes the agent and the prompt adjustments for a faster, cheaper setup with Gemini 3.8 Flash as auxiliary model (planning, summarisation, post-processing). Check the documentation before production use.

## Reasoning / Thinking
- Agent: asynchronous via `client.interactions.create(agent=..., input=..., background=True)`, polling via `client.interactions.get(id)`; result in `outputs[-1].text`. For the fast run, `deep-research-preview-04-2026` is the obvious choice (per research, tuned for speed and efficiency); `deep-research-max-preview-04-2026` for maximum thoroughness.
- Gemini 3.8 Flash as auxiliary model: `thinking_level` `low | medium (default) | high`; `minimal` throws an error; `thinking_budget` not together with `thinking_level`. `low` for extraction and summarisation of the report, `medium`/`high` for source reconciliation and tool loops.
- Pass thought signatures back in function calling (otherwise 400), or use `previous_interaction_id`.

## Prompting style
- As with the Argon setup: guiding question, scope, outline, source rules; collaborative planning optional.
- For Flash: **shorter, atomic briefs**; split large research tasks into sub-questions and start them in parallel instead of one mega-brief (recommendation derived, unverified).
- No handwritten chain-of-thought; instructions direct and concise.
- Keep `temperature` at 1.0, remove `top_p`/`top_k`, no prefill, remove `candidate_count`.
- Sober tone; request longer reports explicitly.

## Strengths & weaknesses (prompt-relevant)
- Strengths: low cost and latency ($0.75 in / $3.75 out per 1M tokens until 31 Dec 2026, then $1.50 / $7.50), 1,048,576 context, 65,536 output, good agentic tool use.
- Weaknesses: lower reasoning depth than Argon on very hard synthesis tasks (assessment, unverified); agent binding not verified; preview agent IDs.

## Output & format conventions
- Markdown report with sources; Structured Outputs for post-processing (summary, tables) with `response_schema`.

## Migration notes
- **FROM Deep Research (3.8 Flash)**: remove background polling and agent ID; write research steps, search tool and source rules explicitly into the target prompt; map `thinking_level` to the target's effort or budget.
- **TO Deep Research (3.8 Flash)**: shorten the prompt to goal, scope, outline and source rules; remove CoT and "search first" scaffolding; build in `background=True` and polling; remove sampling parameters and prefill; for complex topics, escalate to `deep-research-max-…` or an Argon review.

## Sources
- https://ai.google.dev/gemini-api/docs/deep-research — agent IDs, Interactions API, background mode (summarised from web search).
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash — see guide `gemini-3.8-flash`.
