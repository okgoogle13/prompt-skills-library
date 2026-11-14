---
model: gpt-5-mini
vendor: OpenAI
family: GPT
aliases: [gpt5-mini, gpt-5mini, gpt-5-mini-2025-08-07, gpt5mini]
last_verified: 2026-06-13
status: legacy
successor: gpt-5.6-terra
---

# GPT-5 mini

## Reasoning / Thinking
- **Type: extended / adaptive reasoning (always reasoning-capable).** gpt-5-mini is a reasoning model with "reasoning token support" and — like gpt-5, gpt-5-mini and gpt-5-nano — uses internal reasoning tokens before the visible answer. The model thinks adaptively: fewer tokens for simple tasks, more for complex ones.
- **Depth control via `reasoning_effort`.** Supported values for gpt-5 / gpt-5-mini / gpt-5-nano (2025-08 generation; GPT-5.6 has a different ladder): `minimal`, `low`, `medium` (default), `high`. `minimal` produces very few or no reasoning tokens for minimal time-to-first-token, but per OpenAI should be avoided for multi-step planning or tool-heavy workflows. Higher levels improve quality on complex, multi-step tasks but cost more tokens and latency. `reasoning_effort` is meant as a "tuning knob", not a primary lever for rescuing quality.
- **`reasoning_effort: "none"` is not supported by gpt-5-mini** (per community/test reports the API only accepts `minimal`/`low`/`medium`/`high`) — (partly unverified: not explicitly confirmed in any primary OpenAI doc; the official model card only lists "Reasoning: High" as a capability level).
- **Second control axis `verbosity`** (low | medium | high) affects the length of the *final answer*, not the length of thinking — it is independent of `reasoning_effort`.
- **Reasoning tokens are not kept in context between API calls.** For agentic multi-step workflows, OpenAI recommends passing reasoning items back via the Responses API (`previous_response_id`) so the model can access earlier reasoning traces (more efficient, lower token use).

## Prompting Style
- **Highly prescriptive / high instruction fidelity.** GPT-5 (incl. mini) follows instructions with "surgical precision" and is "extraordinarily receptive" to instructions on verbosity, tone and tool calling. That is exactly why it suffers more than older models from badly built prompts.
- **Contradictory instructions are the most expensive failure source:** the model spends reasoning tokens reconciling conflicts instead of deciding optimally. Resolve the instruction hierarchy explicitly; check prompts for contradictions (optionally using the OpenAI Prompt Optimizer).
- **System/developer message fidelity:** The reasoning doc recommends giving the model "task, constraints, and desired output format" and **not** prescribing intermediate steps. Important: **do not** use a system and a developer message in the same request at once (unverified).
- **Tune eagerness deliberately.** Less eagerness: lower `reasoning_effort`, clear exploration criteria, fixed tool-call budgets (e.g. "maximum of 2 tool calls"), escape hatches. More eagerness: higher `reasoning_effort`, persistence instructions ("keep going until the user's query is completely resolved").
- **Differences from the full GPT-5:** gpt-5-mini is the smaller, cheaper, lower-latency variant and shines mainly on **well-defined tasks and precise prompts**; for vague, open-ended exploratory or especially complex multi-step tasks the full gpt-5 is more robust (inferred, unverified). gpt-5-mini therefore tends to need more precise, unambiguous prompts. The API shape is identical to gpt-5; the same new tools (custom tools, CFG) are supported.
- **With `minimal` reasoning** gpt-5-mini needs stronger prompting: ask for a short summary of the approach up front, detailed tool preambles, explicit persistence reminders against premature stopping, and breaking tasks into all necessary sub-requests (closer to GPT-4.1 prompting).

## Strengths & Weaknesses (prompt-relevant)
- **Strengths:** "Near-frontier intelligence" at low cost and latency; very high steerability via `reasoning_effort` + `verbosity` without rewriting the prompt; strong instruction fidelity; ideal for high-volume, well-defined, precisely worded tasks; supports streaming, function calling, structured outputs, custom/freeform tools and context-free grammar (Lark/regex).
- **Weaknesses:** sensitive to contradictory/unclean prompts (reasoning-token waste); with `minimal` reasoning it is not a good planner for tool-heavy multi-step workflows; **no** fine-tuning, **no** predicted outputs; no audio/video; Markdown fidelity can slip in long conversations (refresh format instructions every 3–5 user messages).

## Output & Format Conventions
- **By default no Markdown** in the final answer via the API. Enable Markdown deliberately with a semantic instruction, e.g.: "Use Markdown **only where semantically correct** (e.g., `inline code`, code fences, lists, tables)."
- **Control answer length via `verbosity`** rather than rewriting the prompt: low = terse UX/minimal prose, medium = balanced (default), high = verbose (good for audits/teaching/hand-offs). Prompts can override the global verbosity default in a context-specific way.
- **Tool preambles:** trained to give upfront plans and progress updates; frequency/style is controllable via the prompt.
- **Modalities:** text input + text output, image input; **no** audio, **no** video.
- **Limits:** context window 400,000 tokens, max. output 128,000 tokens. Structured outputs are supported.

## Migration Notes
- **Deprecation:** `gpt-5-mini-2025-08-07` is scheduled for shutdown on 11 Dec 2026 per the OpenAI deprecations page; official replacement `gpt-5.6-terra`. The gpt-5-mini model page likewise recommends GPT-5.6 Terra for new low-latency/high-volume workloads.
- **AWAY FROM gpt-5-mini:**
  - Move to **gpt-5.6-terra** (official successor), or to **gpt-5.6-sol** for harder tasks. That model uses a different effort ladder: `none | low | medium (default) | high | xhigh | max`, no `minimal` — map the level to the target guide's ladder. (`gpt-5` itself is also deprecated.)
  - When moving to smaller models (e.g. gpt-5-nano) or non-reasoning models: make prompts more precise and explicit, since there is less reasoning headroom.
- **TO gpt-5-mini:**
  - From larger GPT-5 models: sharpen prompts and make them less ambiguous, define tasks well; remove contradictory instructions.
  - From non-reasoning models (e.g. GPT-4.1/4o): introduce `reasoning_effort` and `verbosity` as new control axes; with `minimal` reasoning keep GPT-4.1-style explicit prompting. Do not prescribe intermediate steps; supply task + constraints + output format.
  - For agentic workflows, switch to the **Responses API** (reasoning persistence via `previous_response_id`); do not send system and developer messages together (unverified).

## Sources
- https://developers.openai.com/api/docs/models/gpt-5-mini — model card: context window (400k), max. output (128k), reasoning support, modalities, supported features, positioning as the cheap/low-latency variant for well-defined tasks; recommendation to start new low-latency/high-volume workloads with GPT-5.6 Terra.
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide — prompting guide: `reasoning_effort` levels, eagerness control, `verbosity`, instruction fidelity/"surgical precision", contradictory-instruction problem, tool preambles, Markdown default behaviour, minimal-reasoning guidance, Responses API recommendation.
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools — exact values for `reasoning_effort` (minimal/medium default) and `verbosity` (low/medium/high), custom/freeform tools and CFG; supported models incl. gpt-5-mini.
- https://developers.openai.com/api/docs/guides/reasoning — reasoning guide: reasoning tokens not kept between calls, `previous_response_id`, effort as a tuning knob, task/constraints/output format instead of intermediate steps.
- https://openai.com/index/introducing-gpt-5-for-developers/ — announcement: three API sizes (gpt-5, gpt-5-mini, gpt-5-nano), gpt-5-mini as the faster/cheaper variant, `reasoning_effort: minimal`, Responses API recommendation. (Page fetch HTTP 403 — content from OpenAI search index snippet; SOURCE PARTIALLY UNAVAILABLE.)
- https://developers.openai.com/api/docs/deprecations — deprecations (announced 2026-06-11): gpt-5-mini-2025-08-07 shutdown 11 Dec 2026, replacement gpt-5.6-terra; gpt-5-2025-08-07 → gpt-5.6-sol
- https://developers.openai.com/api/docs/models/gpt-5.6-terra — successor's effort ladder none/low/medium (default)/high/xhigh/max
- https://developers.openai.com/api/docs/models/gpt-5.6-sol — "GPT-5.6 flagship model for complex professional work", same effort ladder
