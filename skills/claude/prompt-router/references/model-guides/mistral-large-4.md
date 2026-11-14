---
model: mistral-large-4
vendor: Mistral AI
family: Mistral
aliases: [mistral-large-4-0, large-4, large4, Mistral-Large-4-1T-A52B]
last_verified: 2026-10-13
status: current
---

# Mistral Large 4

## Reasoning / Thinking
- Type: **hybrid instruct-and-reasoning model**; per the announcement it "unifies instruction, reasoning, and agentic capabilities in a single model". Reasoning is controlled **per request** via `reasoning_effort`; the reasoning docs list `mistral-large-4-0` with "No extra configuration required — just add the parameter to any chat completion request."
- Semantics for Mistral models per the reasoning docs: `"high"` returns a full thinking chunk before the answer (more tokens), `"none"` thinks minimally and omits the thinking chunk. The usage example in the model card sets `reasoning_effort="high"`.
- **The default value for Large 4 is not documented (unverified)**, as is whether Large 4 accepts values beyond `"none"`/`"high"` (unverified). Therefore always set the control explicitly rather than building on a default.
- Multi-turn requirement: replay the complete assistant message **including `ThinkChunk`** into the history. Docs warning: "Do not strip ThinkChunk from assistant messages before replaying them. … Stripping them increases token efficiency but significantly degrades output quality."
- `reasoning_effort` also applies on the Agents and Conversations endpoints, where it sits in the `completion_args` field.
- Mistral does not publish a sampling recommendation (temperature/top_p) for Large 4 (unverified).

## Prompting style
- **No Large 4-specific prompting guidance exists (unverified)**; Mistral's cross-model prompting docs apply.
- Role-first framing: "You are a <role>, your task is to <task>." Structure instructions hierarchically in sections and subsections, complete, and as if the reader has no prior knowledge.
- Structure via **Markdown and/or XML-like tags** (the docs' rationale: readable, parsable, familiar from training). Few-shot as an example section in the prompt or as preceding user/assistant turns. System prompt = general context and behaviour, user prompt = context of the current interaction; without control over the system prompt, prepend the general instructions to the user message.
- Documented anti-patterns: vague quantifiers and woolly words ("too long", "make it better"), contradictions in long system prompts (use a decision tree instead), having the model count words/characters (pass numbers as input), numeric rating scales (use word scales instead), unnecessary output.
- Agentic prompts: per the announcement the model runs "general-purpose agents that gather information, use tools, and produce finished deliverables"; Mistral describes its robustness against indirect prompt injection as saturated in its own benchmarks. No recommendation on tool count or image format (such as the ~1:1 for Large 3) exists for Large 4 (unverified).

## Strengths & weaknesses (prompt-relevant)
- Size: the model card names **52B active / 1.05T total parameters plus 1.6B vision encoder** (granular MoE); the announcement rounds to "1 trillion-parameter … with 52 billion active parameters". In case of discrepancy the model card applies.
- Strengths per the vendor: agentic coding (61.7% DeepSWE v1.1, 59.4% SWE-Atlas-QnA, 28.3% Terminal-Bench 4), cybersecurity, finance, legal and scientific workflows; launch blurb "state-of-the-art among open weights on cybersecurity, finance, and manufacturing". Natively multimodal (text + image in).
- Multilingual: training data from "more than 160 languages, including every official language of the European Union".
- Weakness named by the vendor itself: the average refusal rate on cyber prompts (JailbreakBench, StrongREJECT, AgentHarm) "is higher than all OSS models". How much this affects legitimate security prompts is not quantified (unverified).
- **Public Preview**: per the announcement the RL training run is still ongoing and the model "continues to improve rapidly"; per the lifecycle docs preview models receive silent updates and "may be retired before reaching" GA (deprecation notice for preview: 1 month). Prompt behaviour can therefore change without an ID change.
- Open weights are announced ("Weights drop end of this month"); the model card links the repo `Mistral-Large-4-1T-A52B` as "Coming soon" and names no license (unverified).

## Output & format conventions
- **1M context window** (model card, changelog). Maximum output token limit and knowledge cutoff are not documented (unverified).
- Official API names per the model card: `mistral-large-4` and `mistral-large-4-0`. Per the lifecycle scheme `-major` is the newest minor of the generation and `-major-minor` is fixed. Per the Large 3 model card `mistral-large-latest` still points to `mistral-large-2512` (Large 3), **not** to Large 4.
- Features per the model card: structured outputs, function calling, document QnA, prefix (assistant prefill), chat completions, batching, agents & conversations, built-in tools — **without predicted outputs**.
- Response shape depends on the mode: with `"high"` `message.content` is a list of `ThinkChunk` (`type: "thinking"`) and `TextChunk` (`type: "text"`); with `"none"` a plain string. In streaming `delta.content` is first a list (thinking), then a transition chunk with the closing `ThinkChunk` and the first `TextChunk`, then a plain string.
- For format fidelity the feature list offers structured outputs and prefix prefill.

## Migration notes
- **TO Mistral Large 4 (mainly from Large 3)**: set the model ID to `mistral-large-4-0`; `mistral-large-latest` does not reach Large 4. Set `reasoning_effort` **explicitly** (default unverified). With `"high"` the `ThinkChunk` carries the thinking trace — hand-written chain-of-thought scaffolding from Large 3 prompts becomes redundant and costs output tokens; whether it does harm is (unverified). Rework response parsing for the chunk list and carry `ThinkChunk` across all turns. Context grows from 256k to 1M, chunking/RAG splitting can be loosened. The Large 3 rules `temperature` < 0.1 and ~1:1 images are not documented for Large 4 (unverified) — recalibrate rather than carry over. The Large 4 card does not list predicted outputs — convert pipelines that depend on them.
- Recalculate costs: list price $1.36 input / $0.14 cached / $4.18 output per 1M tokens versus $0.5 / $1.5 for Large 3, plus reasoning tokens at `"high"`. The launch discount ("50% off for 2 weeks" from 6 Oct 2026) is time-limited.
- **Preview caveat**: pinning to `mistral-large-4-0` protects against generation changes, not against silent preview updates; re-evaluate prompts after updates. Per `/models` Large 3 is neither deprecated nor given a replacement — the vendor documents no replacement of Large 3 by Large 4.
- **FROM Mistral Large 4**: remove `reasoning_effort` (incl. `completion_args`) and all `ThinkChunk` handling; targets without a reasoning control again need explicit step-by-step scaffolding in the prompt. Revert parsing to a string. Replace Mistral specifics: prefix prefill, built-in tools, `/v1/conversations`. For targets under 1M re-plan the context budget; for text-only targets remove image content parts.

## Sources
- https://docs.mistral.ai/models/mistral-large-4-0 — official model card: 6 Oct 2026, Public Preview, v26.10, API names `mistral-large-4` / `mistral-large-4-0`, 52B active / 1.05T total + 1.6B vision encoder, 1M context, $1.36 / $0.14 / $4.18 (sale $0.68 / $0.07 / $2.09), feature list without predicted outputs, usage example with `reasoning_effort="high"`, weights link `Mistral-Large-4-1T-A52B` "Coming soon", no license stated.
- https://docs.mistral.ai/studio/conversations/reasoning — `mistral-large-4-0` with `reasoning_effort` without extra configuration, semantics of `"high"`/`"none"`, `ThinkChunk`/`TextChunk` response form, streaming sequence, multi-turn replay warning, `completion_args` on agents/conversations; no default value for Large 4.
- https://mistral.ai/news/mistral-large-4/ — announcement (6 Oct 2026): Public Preview, "1 trillion-parameter … 52 billion active", hybrid instruct-and-reasoning, coding figures, agentic use, launch blurb (cybersecurity/finance/manufacturing), prompt-injection robustness, cyber refusal rate, 160+ languages, weights by month end, ongoing RL training, $1.36 / $4.18.
- https://docs.mistral.ai/resources/changelogs — entry of 6 Oct 2026: "Mistral Large 4 (`mistral-large-4`) is now available in Public Preview", 1M context, "Open weights are coming soon", "50% off for 2 weeks".
- https://docs.mistral.ai/inference/model-lifecycle — alias levels (`-latest`, `-major`, `-major-minor`), warning about silent alias updates, Public Preview with silent updates and possible retirement before GA, deprecation deadlines.
- https://docs.mistral.ai/studio/conversations/chat-completion/prompting — cross-model prompting guidance: role framing, hierarchy, Markdown/XML tags, few-shot, system-vs-user split, anti-pattern list; names no specific model.
- https://docs.mistral.ai/models/mistral-large-3-25-12 — cross-check: API names `mistral-large-2512` / `mistral-large-latest`, 256k context, $0.5 / $1.5, GA with no deprecation notice.
- https://docs.mistral.ai/models — Large 4 as featured generalist; Large 3 not in the deprecated table.
- https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512 — cross-check of the Large 3 rules (`temperature` < 0.1, images ~1:1) that are not documented for Large 4.
