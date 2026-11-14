# Local LLM Recommendations

Status: active decision register  
Last reviewed: 2026-11-14  
Scope: local LLM selection, quantisation, tooling, and writing workflows for the prompt-skills-library project.

## Purpose

This register records current, evidence-based recommendations for using local LLMs in creative and professional writing workflows.

It is intentionally separate from `local-llm-open-questions.md`:

- Recommendations record decisions that are currently supported by evidence.
- Open questions record what still needs to be investigated before a decision can be made.

A recommendation may be marked `provisional` when it is the best available starting point but has not yet been validated on the purchased laptop. It should be promoted to `accepted` only after direct testing.

## Status vocabulary

- `provisional` — reasonable starting recommendation, pending local validation
- `accepted` — validated and adopted for current use
- `superseded` — replaced by a newer recommendation
- `rejected` — considered and not adopted
- `parked` — valid idea, but not currently in scope

## Scope

The immediate focus is selecting and running local models for:

- Creative writing: fiction, dialogue, worldbuilding, and long-form drafting
- Professional writing: emails, resumes, cover letters, and tone-matched business documents
- Structured output: JSON and YAML for downstream agents and ATS-oriented workflows

Hardware procurement is out of scope because the laptop has already been purchased.

## Recommendations

## REC-001 — Primary creative-writing model

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, creative-writing
- recommendation: Start with Gemma 4 31B at Q4_0 as the primary creative-writing model, with Qwen3 32B at Q4_K_M as the fallback.
- rationale: Gemma 4 31B offers approximately 17.5 GB VRAM use at Q4_0, a 256K context window, native system-prompt support, and built-in function calling. Qwen3 32B remains a strong alternative at approximately 20 GB VRAM and has substantial community testing.
- constraints:
  - Confirm the laptop’s actual VRAM or unified-memory capacity before loading either model.
  - Reserve headroom for KV cache, operating system, and editor/agent tooling.
  - Validate prose quality and voice consistency on personal writing prompts before adopting either model permanently.
- evidence:
  - https://ai.google.dev/gemma/docs/core
  - https://ollama.com/library/qwen3
  - https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026
- open_questions: OQ-001, OQ-003, OQ-004
- superseded_by: null

## REC-002 — Primary professional-writing model

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, professional-writing, structured-output
- recommendation: Use the same primary model initially for professional writing, but evaluate a separate professional-writing default after controlled testing.
- rationale: Creative and professional writing have different requirements. Professional work prioritises factual accuracy, instruction adherence, concise revision, and reliable structure; creative work prioritises voice, variation, and long-form coherence.
- constraints:
  - Do not assume the best creative-writing model is also the best resume, cover-letter, or email model.
  - Use low temperature and explicit output schemas for professional documents.
  - Validate against representative Australian job-application documents before adoption.
- evidence:
  - https://www.promptquorum.com/prompt-engineering
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-002, OQ-011, OQ-012
- superseded_by: null

## REC-003 — Default quantisation

- status: provisional
- confidence: high
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, quantisation
- recommendation: Use Q4_K_M as the default starting quantisation for GGUF models, and Q4_0 for Gemma 4 models where an official QAT checkpoint is available.
- rationale: Q4-class quantisation substantially reduces VRAM use while retaining usable quality for writing and instruction-following workloads. Higher-bit quantisation should be used only when VRAM headroom and a measurable quality benefit justify it.
- constraints:
  - Quantisation choice must leave room for KV cache and system overhead.
  - Do not use aggressive Q2 or Q3 quantisation for human-facing prose.
  - Re-evaluate if the selected model exhibits quality loss at Q4.
- evidence:
  - https://ollama.com/library
  - https://www.promptquorum.com/local-llms/llm-quantization-explained
  - https://ai.google.dev/gemma/docs/core
- open_questions: OQ-003, OQ-004
- superseded_by: null

## REC-004 — Context and VRAM budget

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, context-window, vram
- recommendation: Treat model weights, KV cache, operating system, and active applications as separate parts of the memory budget; do not assume a model fits merely because its weights fit.
- rationale: Long-context writing can consume substantial additional memory through KV cache. A model that loads successfully may still become slow or unstable at high context lengths.
- constraints:
  - Measure actual VRAM or unified-memory use before relying on long-context workflows.
  - Start with conservative context limits, then increase only after validating stability.
  - Do not use system RAM as a substitute for GPU VRAM on CUDA-based workflows.
- evidence:
  - https://www.promptquorum.com/power-local-llm/best-laptops-local-llm-2026
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-004
- superseded_by: null

## REC-005 — Primary local toolchain

- status: provisional
- confidence: high
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, tooling, agents
- recommendation: Use Ollama as the primary local runtime, with Open WebUI as the main writing interface and LM Studio as a secondary GUI for model discovery and quick experiments.
- rationale: Ollama provides a simple CLI workflow, an OpenAI-compatible local API, and broad integration potential for IDEs, agents, and custom workflows. LM Studio is useful for GUI-first model browsing and experimentation.
- constraints:
  - Confirm Apple Silicon versus x86 before relying on MLX-specific workflows.
  - Keep the initial stack simple; do not add Jan, text-generation-webui, GPT4All, or LocalAI unless a concrete need emerges.
  - Use a text editor for revision rather than relying exclusively on chat-based editing.
- evidence:
  - https://ollama.com
  - https://www.promptquorum.com/local-llms
  - https://www.promptquorum.com/power-local-llm
- open_questions: OQ-005, OQ-013
- superseded_by: null

## REC-006 — Small-model companion

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, small-models, structured-output
- recommendation: Maintain one small model, approximately 3B to 8B, for fast drafting, outlines, email templates, and simple structured extraction.
- rationale: A small model can handle routine work quickly while preserving VRAM for the primary model. It is also useful when the laptop is under heavy load or operating without a discrete GPU.
- constraints:
  - Do not use the small model for nuanced long-form creative writing or high-stakes professional documents.
  - Use explicit schemas and low temperature for structured tasks.
  - Select the specific model only after comparing candidates on the purchased laptop.
- evidence:
  - https://ollama.com/library
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-006
- superseded_by: null

## REC-007 — Poetry and lyrical-prose specialist

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, creative-writing, poetry
- recommendation: Treat Yi-1.5 34B as a candidate poetry and lyrical-prose specialist, but do not adopt it as a default until compared with current general-purpose models.
- rationale: Earlier testing identified Yi-1.5 34B as strong for rhythm, imagery, and structured verse, but newer models may now match or exceed it.
- constraints:
  - Do not prioritise a specialist model before establishing a strong general-purpose primary model.
  - Evaluate whether the specialist model justifies its VRAM and maintenance cost.
- evidence:
  - https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026
- open_questions: OQ-007
- superseded_by: null

## REC-008 — Dialogue and character-voice model

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, creative-writing, dialogue
- recommendation: Use the primary creative-writing model initially for dialogue; consider a dialogue specialist only if character differentiation becomes a repeated failure.
- rationale: Dialogue quality depends heavily on prompt structure, character notes, and sampling settings. A specialist model is justified only when the general-purpose model consistently fails.
- constraints:
  - Test multi-character scenes before adding a second large model.
  - Use SillyTavern or an equivalent frontend only if character-card and lore-book workflows become necessary.
- evidence:
  - https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026
- open_questions: OQ-008
- superseded_by: null

## REC-009 — Cloud escalation threshold

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, long-context, cloud
- recommendation: Use cloud models selectively for tasks that exceed local context, quality, or latency limits; use local models as the default for routine writing and experimentation.
- rationale: Local models now offer strong privacy, cost, and offline advantages, while cloud models remain stronger for the most demanding reasoning, long-context coherence, and specialised tasks.
- constraints:
  - Prototype prompts and schemas locally before escalating to cloud.
  - Avoid sending personal or sensitive information to cloud providers without reviewing their data-handling terms.
  - Reassess the threshold as local 256K-context models improve.
- evidence:
  - https://www.promptquorum.com/local-llms
  - https://www.promptquorum.com/power-local-llm
- open_questions: OQ-009, OQ-017
- superseded_by: null

## REC-010 — Uncensored model policy

- status: provisional
- confidence: high
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, safety, professional-writing
- recommendation: Use aligned instruct models as the default for professional documents; reserve uncensored models for clearly framed creative-fiction scenarios where refusal behaviour interferes with legitimate writing.
- rationale: Uncensored models follow prompts more literally, which can be useful for mature fiction, conflict scenes, and morally complex characters, but also increases the importance of prompt discipline and manual review.
- constraints:
  - Do not use uncensored models for resumes, cover letters, or routine professional email.
  - Do not treat local hosting as changing legal or ethical obligations.
  - Maintain a separate aligned model for non-fiction and professional workflows.
- evidence:
  - https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026
  - https://ollama.com/library/dolphin3
- open_questions: OQ-010
- superseded_by: null

## REC-011 — Email tone-matching settings

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: prompt-engineering, email, local-llm
- recommendation: Use lower temperature and explicit tone constraints for professional email drafting; reserve higher temperature for creative prose.
- rationale: Email workflows need consistency, factual stability, and controlled variation. Creative-writing sampling settings can introduce unnecessary unpredictability.
- constraints:
  - Start around temperature 0.3 to 0.6 for professional email.
  - Specify audience, relationship, desired tone, length, and required actions.
  - Validate output against real email examples before relying on automated workflows.
- evidence:
  - https://www.promptquorum.com/prompt-engineering
  - https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026
- open_questions: OQ-011
- superseded_by: null

## REC-012 — ATS-oriented structured output

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: prompt-engineering, ats, structured-output
- recommendation: Use a schema-first prompt pattern with explicit JSON or YAML field definitions, few-shot examples, and a validation step for ATS-oriented documents.
- rationale: Structured prompts reduce ambiguity and improve machine-parseable output. Few-shot examples and explicit constraints help local models follow field names and formatting rules.
- constraints:
  - Do not allow the model to invent fields outside the schema.
  - Validate JSON/YAML before downstream use.
  - Keep factual claims grounded in supplied source material.
- evidence:
  - https://www.promptquorum.com/prompt-engineering
  - https://www.promptquorum.com/prompt-bites
- open_questions: OQ-012
- superseded_by: null

## REC-013 — Apple Silicon runtime

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, apple-silicon, tooling
- recommendation: If the laptop is Apple Silicon, evaluate MLX alongside Ollama before selecting a primary runtime.
- rationale: MLX may offer performance advantages on Apple Silicon, while Ollama offers broader ecosystem compatibility and simpler API integration.
- constraints:
  - Do not assume MLX compatibility for all GGUF models.
  - Compare the same model, quantisation, and prompt set before deciding.
  - Keep Ollama available as the integration-oriented fallback.
- evidence:
  - https://www.promptquorum.com/power-local-llm
  - https://www.promptquorum.com/prompt-bites
- open_questions: OQ-013
- superseded_by: null

## REC-014 — Model-review cadence

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, model-management
- recommendation: Review the local-model recommendation set monthly, or immediately after a major model release, benchmark change, or tooling change.
- rationale: Local-model releases move quickly. A lightweight review cadence prevents stale recommendations without creating excessive maintenance overhead.
- constraints:
  - Do not change recommendations without evidence.
  - Record the trigger and evidence for every change.
  - Prefer small, targeted updates over wholesale rewrites.
- evidence:
  - https://ollama.com/library
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-014
- superseded_by: null

## REC-015 — RAG deferral

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, rag, writing
- recommendation: Defer RAG until the primary model, quantisation, and toolchain are validated.
- rationale: RAG adds complexity and can improve factual grounding, but it is not necessary for the first writing experiments. Establishing a reliable base model first reduces debugging surface area.
- constraints:
  - Revisit RAG when writing from personal documents, job descriptions, or research material becomes a recurring need.
  - Start with a minimal document set and a simple retrieval workflow.
- evidence:
  - https://www.promptquorum.com/power-local-llm
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-015
- superseded_by: null

## REC-016 — Agent tool-calling approach

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: local-llm, agents, tool-calling
- recommendation: Begin with narrowly scoped local agent workflows, but use cloud models for complex multi-step tasks until local tool-calling reliability is validated.
- rationale: Local models can support tool calling, but reliability varies by model and workflow. Cloud models remain stronger for complex reasoning and multi-step orchestration.
- constraints:
  - Start with one tool and one clear success criterion.
  - Validate JSON/YAML output before allowing autonomous actions.
  - Do not grant agents write access to external systems without explicit approval.
- evidence:
  - https://www.promptquorum.com/power-local-llm
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-016
- superseded_by: null

## REC-017 — Cloud GPU usage

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: cloud, cost, local-llm
- recommendation: Use cloud GPU rental only for bounded, high-value experiments with models that cannot run locally; do not use it as the default writing workflow.
- rationale: Cloud access provides a way to test large models without purchasing hardware, but per-hour and per-token costs can accumulate quickly.
- constraints:
  - Define the experiment, success criteria, and budget before renting GPU time.
  - Keep prompts portable between local and cloud environments.
  - Reassess after establishing actual local-model performance.
- evidence:
  - https://www.promptquorum.com/local-llms
  - https://www.promptquorum.com/prompt-bites
- open_questions: OQ-017
- superseded_by: null

## REC-018 — Australian compliance checklist

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-14
- scope: privacy, compliance, local-llm
- recommendation: Treat personal information in resumes, cover letters, and professional email as sensitive; prefer local processing for drafts containing personal details, and review cloud-provider terms before use.
- rationale: Local inference reduces data exposure, but does not remove the user’s responsibility for lawful and appropriate use of generated content.
- constraints:
  - Do not upload identifiable personal information to cloud services without reviewing their data-handling terms.
  - Review Australian privacy and employment-platform guidance before production use.
  - Keep a simple compliance checklist for job-application workflows.
- evidence:
  - https://www.oaic.gov.au
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-018
- superseded_by: null

## Immediate adoption order

1. REC-005 — Establish the primary local toolchain.
2. REC-001 — Select and validate the primary creative-writing model.
3. REC-002 — Select and validate the primary professional-writing model.
4. REC-003 — Select the default quantisation level.
5. REC-004 — Establish the practical context and VRAM budget.
6. REC-011 — Establish email tone-matching settings.
7. REC-012 — Establish the ATS-oriented structured-output pattern.

Do not expand into poetry, dialogue specialists, RAG, agents, or cloud experimentation until the first five recommendations are validated.
