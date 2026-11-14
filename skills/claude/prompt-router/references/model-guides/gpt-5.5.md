---
model: gpt-5.5
vendor: OpenAI
family: GPT
aliases: [gpt5.5, gpt-5.5-2026-04-23]
last_verified: 2026-10-13
status: current
---

# GPT-5.5

## Reasoning / Thinking
- Depth via `reasoning.effort`: `none | low | medium (default) | high | xhigh`. **`max` does not exist on GPT-5.5** — when migrating from or to a model with `max` (e.g. GPT-5.6 Sol), the level must be mapped deliberately.
- Official recommendation: "Treat `medium` as the recommended balanced starting point for quality, reliability, latency, and cost." Use `high`/`xhigh` only if evals show a measurable quality gain; per the guide, higher levels can lead to overthinking, unnecessary searching or quality regressions. For latency-critical cases, test `low` first; use `none` only for tasks without reasoning needs.
- Interleaved thinking: GPT-5.5 can produce visible output before and between thinking phases, and think between tool calls.
- **`phase` field (Responses API)**: for long or tool-heavy flows, pass back the `phase` field of returned assistant items unchanged ("preserve the `phase` parameter on returned assistant output items and pass it back unchanged") — `commentary` for interim updates, `final_answer` for the finished answer; never set it on user messages. With `previous_response_id` the API handles this automatically.
- `reasoning.context` defaults to `current_turn` for models before GPT-5.6; `all_turns` is reserved for GPT-5.6 and GPT-6.1 Sol. `reasoning.mode: "pro"` is documented in the reasoning guide only for GPT-5.6 and GPT-6 models.

## Prompting Style
- **Outcome-first instead of process choreography:** describe the expected result, success criteria, limits on side effects, evidence rules and output form; strip heavy step-by-step instructions. Suggested short sections: Role, Personality, Goal, Success criteria, Constraints, Output, Stop rules.
- **Use absolute words sparingly:** `ALWAYS`/`NEVER`/`must`/`only` only for real invariants; for discretionary matters, write decision rules.
- **Tool guidance belongs in the tool description:** "Put most tool-specific guidance in the tool descriptions themselves" — what the tool does, when to use it, required inputs, side effects, retry safety, typical errors. The system prompt is only for cross-tool context; for large catalogues use Tool Search.
- **Autonomy:** progress before questions; only ask when missing information materially changes the result. Set stop rules explicitly (documentation example: "Use the minimum evidence sufficient to answer correctly, cite it precisely, then stop.").
- **Preambles:** short visible status message before tool calls, "Keep it to one or two sentences."
- **Default tone:** "GPT-5.5 tends to be efficient, direct, and task-oriented by default." For customer-facing products, define personality and collaboration style explicitly but briefly.
- The current date does not need to be in the prompt: "The model is already aware of the current UTC date."

## Strengths & Weaknesses (prompt-relevant)
- Positioning per the model page: "A new class of intelligence for coding and professional work". Named as the production recommendation in the changelog entries of 5 May, 28 May and 24 Jun 2026 ("We recommend leveraging GPT-5.5 for production API usage"); since 9 Jul 2026 the GPT-5.6 family exists.
- Neither the model page nor the deprecations page names a deprecation or a successor — the model remains regularly available.
- Quirk: higher effort is not a guarantee of quality (see above); control answer length and reasoning quality separately.
- Not supported: Realtime, Assistants, fine-tuning, embeddings, image/video/audio generation, transcription/translation, moderation, legacy completions.

## Output & Format Conventions
- Context window **1,050,000** tokens, max. output **128,000**; knowledge cutoff **1 Dec 2025**; input text + image, output text only. Endpoints: Chat Completions, Responses, Batch.
- **Length:** `text.verbosity` (`low | medium | high`, default `medium`); "`low` is often a better starting point for concise responses." Set concrete lengths via word budgets, section counts or a JSON-only instruction in the prompt.
- **Formatting:** "Let formatting serve comprehension" — by default plain paragraphs; use headings/bold/lists sparingly; respect the user's formatting requests.
- **Structured output:** "Remove output schema definitions from the prompt where possible" — define schemas via Structured Outputs rather than prose in the prompt.
- **Prompt caching:** "Caching for GPT-5.5 only works with extended prompt caching" — `prompt_cache_retention` supports only `"24h"`; implicit breakpoints every 2,048 tokens, explicit breakpoints not supported. Put static parts first and dynamic parts last; use a stable `prompt_cache_key` for shared prefixes.
- Prices per 1M tokens: input $5, cached input $0.50, output $30; prompts above 272K input tokens cost 2x input and 1.5x output. Snapshot `gpt-5.5-2026-04-23`.

## Migration Notes
- **TO GPT-5.5:** per the guide, "treat it as a new model family to tune for, not a drop-in replacement" — start with the smallest prompt that preserves the product contract; strip process choreography, embedded output schemas and date references; move tool hints into the tool descriptions; pass `phase` through in Responses flows. Map `max` from source models to `xhigh` (or lower, per eval).
- **FROM GPT-5.5 to GPT-5.6 Sol/Terra:** keep the current effort level as the baseline and additionally test **one level lower**. "GPT-5.6 tends to be more concise by default than GPT-5.5" — review blanket "Be concise" lines, otherwise answers become too short. Persisted reasoning does not carry over: "reasoning does not carry between the GPT-5.6 and GPT-5.5 families."
- **FROM GPT-5.5 to the GPT-6 family** (`gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-luna`): "When migrating from GPT-5.5 or earlier, replace `prompt_cache_retention` with `prompt_cache_options.ttl`" (only value `"30m"`). Keep the effective effort level where supported — GPT-6 Astra has no `none`, GPT-6.1 Sol has neither `none` nor `minimal`.
- **FROM GPT-5.5 to other providers:** rebuild `reasoning.effort`, `text.verbosity`, `phase` and Structured Outputs as prose or schema instructions of the target provider; re-add any length and format instructions that were removed; check the 1.05M-token context assumption.

## Sources
- https://developers.openai.com/api/docs/models/gpt-5.5 — positioning sentence, snapshot `gpt-5.5-2026-04-23`, effort `none`–`xhigh` (default `medium`, no `max`), 1,050,000 context / 128,000 output, cutoff 1 Dec 2025, modalities, endpoints, unsupported features, prices and the 272K rule, no deprecation notice.
- https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5 — "Using GPT-5.5": effort recommendation, `text.verbosity`, tool descriptions, "Let formatting serve comprehension", outcome-first structure, ALWAYS/NEVER, autonomy, preambles, `phase`, caching order, UTC date, schemas via Structured Outputs, "not a drop-in replacement".
- https://developers.openai.com/api/docs/guides/reasoning — `gpt-5.5` default `medium`, "try `low`" before `none`, interleaved thinking, `phase` for GPT-5.5/5.4, `reasoning.context` default `current_turn` before GPT-5.6, `pro` mode only GPT-5.6/GPT-6, no reasoning transfer between the GPT-5.6 and GPT-5.5 families; GPT-6 Astra without `none`, GPT-6.1 Sol without `none`/`minimal`.
- https://developers.openai.com/api/docs/guides/prompt-caching — GPT-5.5: retention only `"24h"`, implicit breakpoints every 2,048 tokens, no explicit breakpoints; `prompt_cache_options.ttl` from GPT-5.6 onward.
- https://developers.openai.com/api/docs/changelog — release 24 Apr 2026, "Caching for GPT-5.5 only works with extended prompt caching", production recommendation (5 May, 28 May, 24 Jun 2026), GPT-5.6 release 9 Jul 2026.
- https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.6-sol — "GPT-5.6 tends to be more concise by default than GPT-5.5", effort baseline plus one level lower when moving from GPT-5.5; GPT-6 caching note.
- https://developers.openai.com/api/docs/guides/latest-model — GPT-6 migration: `prompt_cache_options.ttl` `"30m"` from GPT-5.5 or older, keep effective effort level.
- https://developers.openai.com/api/docs/deprecations — GPT-5.5 is neither deprecated nor listed as a replacement model.
