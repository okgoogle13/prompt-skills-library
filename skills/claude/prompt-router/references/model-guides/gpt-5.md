---
model: gpt-5
vendor: OpenAI
family: GPT
aliases: [gpt5, openai-gpt-5, openai-gpt5, gpt-5-2025-08-07]
last_verified: 2026-06-13
status: legacy
successor: gpt-5.6-sol
---

# GPT-5

## Reasoning / Thinking
- Type: **adaptive / controllable**. GPT-5 is a reasoning model whose depth is controlled by the parameter `reasoning.effort` (in the Responses API) or `reasoning_effort`. Supported values: `minimal`, `low`, `medium`, `high`; the default is `medium` when nothing is set. ([Model docs](https://developers.openai.com/api/docs/models/gpt-5), [New Params & Tools](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools))
- `minimal` runs "with few or no reasoning tokens to minimize latency" and suits deterministic, lightweight tasks such as extraction, formatting, short rewrites and simple classification. Higher values maximise quality, lower values maximise speed. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide), [New Params & Tools](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools))
- Depth can additionally be steered via the prompt: explicit exploration criteria and fixed tool-call budgets (e.g. "maximum 2 tool calls") against over-eagerness, or persistence instructions ("keep going until the user's query is completely resolved") against under-eagerness. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- In ChatGPT, GPT-5 is implemented as a unified system with a real-time router that chooses between a fast model and a deeper reasoning model (based on complexity, tool needs and explicit intent). ([System Card](https://openai.com/index/gpt-5-system-card/))

## Prompting Style
- Highly prescriptive and instruction-faithful: GPT-5 follows prompt instructions with "surgical precision" and is "extraordinarily receptive to prompt instructions surrounding verbosity, tone, and tool calling behavior". ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- Quirk / risk: exactly this fidelity makes contradictory or vague prompts more harmful than with other models — GPT-5 "spends reasoning tokens to resolve the contradictions". Prompts should therefore be conflict-free and unambiguous. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- Recommendation: start with `medium` reasoning effort and test `minimal`, `low` or `high` against representative tasks; set `text.verbosity` deliberately and move structured answer contracts into Structured Outputs where possible. ([Prompt guidance "Using GPT-5"](https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5), section Migration quickstart) Experiment and iterate rather than using one universal prompt. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- Agentic control: GPT-5 delivers "tool preambles" (plan/progress updates) by default; frequency and style are controllable via the prompt (e.g. "Always begin by rephrasing the user's goal … outline a structured plan"). "Escape hatches" (permission to act "even if it might not be fully correct") reduce excessive clarifying questions. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))

## Strengths & Weaknesses (prompt-relevant)
- Strengths: strong coding ability across large codebases and multi-file refactors; superior agentic performance and tool calling; improved long-context understanding (400,000-token context window); high steerability via prompts; better instruction following than predecessors. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide), [Model docs](https://developers.openai.com/api/docs/models/gpt-5))
- Reduced hallucinations, improved instruction following and lower sycophancy versus predecessors; "safe completions" instead of hard refusals on sensitive topics. ([System Card](https://openai.com/index/gpt-5-system-card/))
- Weaknesses: tends toward verbose outputs (controllable via `verbosity`); tendency to over-explore context unnecessarily; occasional excess clarifying questions on longer tasks; performance variance with `minimal` reasoning depending on prompt quality. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))

## Output & Format Conventions
- `verbosity` (in the Responses API as `text={"verbosity": ...}`) controls the length of the final answer (not the thinking time). Values: `low` (terse UX, minimal prose), `medium` (default, balanced detail), `high` (verbose, for audits/teaching/hand-offs). Can be overridden per context via a natural-language instruction in the prompt (e.g. "Use high verbosity for writing code and code tools"). ([New Params & Tools](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools), [Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- By default GPT-5 uses **no** Markdown in API responses ("for maximum compatibility"); Markdown must be requested explicitly (e.g. "Use backticks to format file, directory, function, and class names"). Markdown fidelity can slip over long conversations — refresh instructions every 3–5 messages. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- Supported: streaming, function calling, structured outputs. Max. output: 128,000 tokens; knowledge cutoff: 30 Sep 2024. ([Model docs](https://developers.openai.com/api/docs/models/gpt-5))
- New tooling features: custom tools (`"type": "custom"`) for raw text payloads (Python, SQL, shell) without JSON wrapping (no parallel calling); context-free grammar (CFG) to constrain output via `"format": {"type": "grammar", "syntax": "lark"|"regex", "definition": "..."}`, so that only grammar-conforming strings are emitted. ([New Params & Tools](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools))

## Migration Notes
- TO GPT-5:
  - Recommended first step: switch the model, keep the prompt functionally unchanged at first, then align `reasoning_effort` with the latency/depth profile of the previous model and test against the eval suite. ([Prompt migration](https://developers.openai.com/cookbook/examples/prompt_migration_guide))
  - Coming from GPT-4.1: `minimal` reasoning is the best upgrade for latency-sensitive users; prompting patterns similar to GPT-4.1 work well (few-shot, high-quality/maximally unambiguous tool descriptions, explicit agentic persistence, upfront planning, short summary of the reasoning at the start of the answer). ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
  - Clean up contradictory/vague legacy prompts before migrating — GPT-5 is more sensitive to them than its predecessors. ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
  - The Responses API is recommended: it keeps reasoning context across tool calls (`previous_response_id`) and yields measurably better results (e.g. Tau-Bench Retail 73.9% → 78.2%). ([Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide))
- AWAY FROM GPT-5: on models without `reasoning_effort`/`verbosity`, these controls must be replaced by prompt instructions (explicit length/format/depth requirements); custom tools and CFG grammar constraints may not be available and must be replaced by classic JSON function calling plus post-validation. (unverified — no primary-source-based migration checklist found; inferred from the GPT-5-specific parameters in [New Params & Tools](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools))
- **Deprecation / lifecycle:** the snapshot `gpt-5-2025-08-07` is scheduled for shutdown on 11 Dec 2026 per the deprecations page; official replacement there is `gpt-5.6-sol`. The GPT-5 model page calls GPT-5 the "previous model" and recommends "the latest GPT-6 Astra". ([Deprecations](https://developers.openai.com/api/docs/deprecations), [Model docs](https://developers.openai.com/api/docs/models/gpt-5))

## Sources
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide — official GPT-5 prompting guide: reasoning_effort (incl. minimal), verbosity overrides, instruction fidelity/quirks, over-/under-eagerness, tool preambles, Markdown behaviour, strengths/weaknesses, GPT-4.1 migration, Responses API
- https://developers.openai.com/api/docs/models/gpt-5 — GPT-5 model docs: reasoning.effort values, context window (400k), max output (128k), knowledge cutoff, streaming/function calling/structured outputs
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools — new parameters & tools: verbosity values and default, minimal reasoning, custom tools, context-free grammar (Lark/regex)
- https://developers.openai.com/cookbook/examples/prompt_migration_guide — prompt migration guide: switch model first, align reasoning_effort, eval suite
- https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5 — prompt guidance "Using GPT-5" (model-bound version; the page without model parameter now describes GPT-6): migration quickstart — start with `medium` and test `minimal`/`low`/`high` against representative tasks, set `text.verbosity` deliberately, Structured Outputs
- https://developers.openai.com/api/docs/deprecations — deprecations (announced 2026-06-11): gpt-5-2025-08-07 shutdown 11 Dec 2026, replacement gpt-5.6-sol
- https://openai.com/index/gpt-5-system-card/ — GPT-5 system card: unified system with router, safe completions, reduced hallucinations/sycophancy, improved instruction following (direct fetch HTTP 403 — content from search index snippet; SOURCE PARTIALLY UNAVAILABLE)
