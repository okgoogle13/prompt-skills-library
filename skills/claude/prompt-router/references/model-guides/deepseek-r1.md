---
model: deepseek-r1
vendor: DeepSeek
family: DeepSeek
aliases: [deepseek-reasoner, r1]
last_verified: 2026-10-13
status: legacy
successor: deepseek-v4.1-flash
---

# DeepSeek-R1

## Reasoning / Thinking
- **Type: always on (reasoning model).** DeepSeek-R1 is a dedicated reasoning model that produces a chain of thought (CoT) in a `<think>...</think>` block before the actual answer. There is no switch to turn thinking off completely.
- **No system prompt.** Official recommendation: "Avoid adding a system prompt; all instructions should be contained within the user prompt." All instructions therefore belong in the user prompt, not in a system role.
- **No few-shot.** According to the paper, R1 is prompt-sensitive: "Few-shot prompting consistently degrades its performance." Recommendation: "We recommend users directly describe the problem and specify the output format using a zero-shot setting for optimal results."
- **Temperature recommendation: 0.5–0.7, 0.6 recommended** ("to prevent endless repetitions or incoherent outputs"); the paper uses `temperature = 0.6` and `top_p = 0.95` for evaluation.
- **Force a `<think>` start.** "To ensure that the model engages in thorough reasoning, we recommend enforcing the model to initiate its response with `<think>\n` at the beginning of every output." Background: the R1 series sometimes bypasses thinking by emitting an empty block (`<think>\n\n</think>`), which degrades performance.
- **Math prompts.** For math tasks an explicit hint is recommended: "Please reason step by step, and put your final answer within `\boxed{}`."
- **API: `reasoning_content`.** Via the API (model name `deepseek-reasoner`) the model returns the CoT separately in the field `reasoning_content` (same structural level as `content`, which contains the final answer). In follow-up rounds the CoT of earlier rounds was NOT carried into the context; according to earlier reasoning docs, the `reasoning_content` field had to be removed from the message before the next request, otherwise a 400 error occurred (unverified — the page is offline; today's thinking-mode docs say that for requests without `tools`, returned `reasoning_content` is ignored).
- **Note on API identity:** the API ID `deepseek-reasoner` has been retired since 2026-07-24 15:59 UTC (last routed to the thinking mode of `deepseek-v4-flash`); R1 is only usable now as an open-weights model. Alias semantics per the change log: `deepseek-reasoner` = R1 (from 2025-01-20), R1-0528 (from 2025-05-28), thinking mode of V3.1/V3.1-Terminus/V3.2-Exp/V3.2 (from 2025-08-21) and V4-Flash (from 2026-04-24) — prompts after 2025-08-21 targeted a hybrid model with system prompt and tool support. The API details in this guide describe the historical endpoint. The original open-weights model "DeepSeek-R1" (arXiv 2501.12948, HF model card) must be distinguished from this; the reasoning recommendations above come from its model card/paper.

## Prompting style
- **Moderately prescriptive, but with clear rules.** DeepSeek gives few but firm requirements: no system prompt, no few-shot, temperature in the narrow band around 0.6, output format explicitly requested in the user prompt.
- **Recommended:** describe the task directly and in plain language (zero-shot); state the desired output format explicitly; for math add the `\boxed{}` directive; have the answer begin with `<think>\n`.
- **Discouraged:** few-shot examples ("consistently degrades performance"), system prompts, very high or very low temperature (outside 0.5–0.7).
- **Evaluation:** run several passes and average, since the model is prompt-sensitive.

## Strengths & weaknesses (prompt-relevant)
- **Strengths:** strong multistep reasoning (mathematics, code, logic) thanks to RL training; benefits from lean, direct zero-shot instructions; produces traceable CoT that can be read separately via `reasoning_content`.
- **Weaknesses / pitfalls:** prompt-sensitive — few-shot and overloaded context tend to hurt; for some requests it tends to skip thinking (empty `<think>` block); at temperatures outside 0.5–0.7 it can slip into repetition/incoherence; a system prompt should be avoided according to the model card.
- **API limitations (historical, API `deepseek-reasoner`):** original R1 API: no function calling, no FIM, `logprobs` → error (unverified — the earlier reasoning docs are offline); according to the change log, the R1-0528 upgrade brought "JSON Output & Function Calling Support".

## Output & format conventions
- **`<think>...</think>` + answer.** Raw output contains the CoT block, followed by the final answer. Via the API the CoT is delivered as `reasoning_content`, the final answer as `content`.
- **`max_tokens`** (historical, API `deepseek-reasoner`) included the CoT. Default 32K tokens, maximum 64K tokens (unverified — the earlier reasoning docs are offline).
- **Context length** of the model: 128K tokens (HF model card).
- **Math output** in `\boxed{}` when requested via directive.
- **Ineffective sampling parameters via the API (historical, API `deepseek-reasoner`; unverified — the earlier reasoning docs are offline):** `temperature`, `top_p`, `presence_penalty`, `frequency_penalty` do not raise an error but have no effect; `logprobs`, `top_logprobs` raise an error. (The 0.6 temperature recommendation applies to local/open-weights use or third-party inference.)

## Migration notes
- **AWAY FROM DeepSeek-R1 (to non-reasoning/instruct models):**
  - Reintroduce a system prompt: for target models with a system role, move instructions from the user prompt into a system prompt.
  - Reactivate few-shot: for many instruct models, examples help again.
  - Remove thinking-specific elements: remove or adapt the `<think>\n` enforcement, the `\boxed{}` directive and the parsing of `reasoning_content`.
  - Choose temperature anew: the narrow band around 0.6 is R1-specific; configure the target model with its own defaults.
- **MIGRATING TO DeepSeek-R1 (from instruct/chat models):**
  - Dissolve the system prompt: move the contents of the system prompt into the user prompt (model card: "Avoid adding a system prompt").
  - Remove few-shot: delete example blocks and instead describe the task + output format directly (zero-shot).
  - Set temperature to 0.5–0.7 (0.6), top_p ~0.95.
  - Have the output begin with `<think>\n`; for math add the `\boxed{}` directive.
  - Adjust multi-round handling: do not feed the CoT of earlier rounds back into the context; only for the historical `deepseek-reasoner` endpoint: remove `reasoning_content` before the next API call (otherwise 400 — unverified, docs offline).
  - Original R1 only: do not use function calling / FIM (unverified, see above; R1-0528 got function calling according to the change log); if used, replace with prompt formatting.

## Sources
- https://huggingface.co/deepseek-ai/DeepSeek-R1 — official model card: usage recommendations (no system prompt, temperature 0.5–0.7/0.6, `<think>\n` enforcement, empty-think-block note, `\boxed{}` directive), context length 128K.
- https://github.com/deepseek-ai/DeepSeek-R1/blob/main/README.md — identical usage recommendations section in the official repo.
- https://arxiv.org/html/2501.12948v1 — DeepSeek-R1 paper (§5): "it is sensitive to prompts", "Few-shot prompting consistently degrades its performance", zero-shot recommendation; evaluation setup: `temperature = 0.6`, `top_p = 0.95`.
- https://api-docs.deepseek.com/guides/thinking_mode — successor page to the taken-offline reasoning doc (`guides/reasoning_model`): `reasoning_content` alongside `content`, without `tools` returned `reasoning_content` is ignored, sampling parameters with no effect in thinking mode. It does not confirm the R1-specific API details (32K/64K, `logprobs` error, 400 on returned `reasoning_content`).
- https://api-docs.deepseek.com/news/news260424 — shutdown of `deepseek-reasoner` on 2026-07-24 15:59 UTC, until then routing to the thinking mode of `deepseek-v4-flash`.
- https://api-docs.deepseek.com/updates — alias history of `deepseek-reasoner` (R1, R1-0528, V3.1 to V3.2, V4-Flash), R1-0528 with "JSON Output & Function Calling Support".
