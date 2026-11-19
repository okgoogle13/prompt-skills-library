# Local LLM Recommendations

Status: active decision register
Last reviewed: 2026-11-19
Scope: local LLM selection, quantisation, tooling, coding, agents, Home Assistant, and writing workflows for the prompt-skills-library project.

## Purpose

This register records current, evidence-based recommendations for using local LLMs across writing, coding, daily-driver, reasoning, routine automation, retrieval, IDE, and Home Assistant workflows.

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
- Coding: implementation, debugging, refactoring, repository work, and agent-style coding
- Daily-driver use: chat, planning, summarisation, research, and routine project work
- High reasoning: trade-off analysis, research synthesis, and multi-step decision support
- Routine tasks: classification, extraction, templates, and structured output
- Home Assistant: intent recognition, tool calling, and low-latency automation
- Privacy-sensitive work: personal documents, communications, career material, and family planning

Hardware procurement is out of scope because the laptop has already been purchased.

## Recommendations

## REC-001 — Primary creative-writing model

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- open_questions: OQ-004, OQ-019, OQ-020, OQ-021
- superseded_by: null

## REC-005 — Primary local toolchain

- status: provisional
- confidence: high
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
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
- open_questions: OQ-005, OQ-013, OQ-028, OQ-029, OQ-030
- superseded_by: null

## REC-006 — Small-model companion

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- open_questions: OQ-009, OQ-017, OQ-033, OQ-040
- superseded_by: null

## REC-010 — Uncensored model policy

- status: provisional
- confidence: high
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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

- status: parked
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
- scope: local-llm, apple-silicon, tooling
- recommendation: If an Apple Silicon machine is actively used, evaluate MLX alongside Ollama before selecting a primary runtime.
- rationale: MLX may offer performance advantages on Apple Silicon, while Ollama offers broader ecosystem compatibility and simpler API integration. This is parked because the active target is an RTX 5090 laptop.
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
- last_reviewed: 2026-11-19
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
- open_questions: OQ-014, OQ-030
- superseded_by: null

## REC-015 — RAG deferral

- status: provisional
- confidence: medium
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
- scope: local-llm, rag, writing
- recommendation: Defer RAG until the primary model, quantisation, and toolchain are validated.
- rationale: RAG adds complexity and can improve factual grounding, but it is not necessary for the first writing experiments. Establishing a reliable base model first reduces debugging surface area.
- constraints:
  - Revisit RAG when writing from personal documents, job descriptions, or research material becomes a recurring need.
  - Start with a minimal document set and a simple retrieval workflow.
- evidence:
  - https://www.promptquorum.com/power-local-llm
  - https://www.promptquorum.com/local-llms
- open_questions: OQ-015, OQ-027
- superseded_by: null

## REC-016 — Agent tool-calling approach

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
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
- open_questions: OQ-016, OQ-028, OQ-031, OQ-032, OQ-033
- superseded_by: null

## REC-017 — Cloud GPU usage

- status: provisional
- confidence: low
- date_decided: 2026-11-14
- last_reviewed: 2026-11-19
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
- last_reviewed: 2026-11-19
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

## REC-019 — Primary coding model

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, coding
- recommendation: Do not adopt a coding-model default until OQ-022 is researched and locally validated.
- rationale: Coding requires reliable instruction following, repository awareness, tool use, and low hallucination. A general-purpose writing model should not be assumed to be the best coding model.
- constraints:
  - Evaluate candidates at compatible quantisations within the RTX 5090 laptop capacity envelope.
  - Test representative tasks from career-brain, comms-hub-v2, and parents-move.
  - Validate diffs, tests, and tool-calling behaviour before adoption.
- evidence: []
- open_questions: OQ-022, OQ-028, OQ-031, OQ-032, OQ-033
- superseded_by: null

## REC-020 — Primary daily-driver model

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, daily-driver
- recommendation: Do not adopt a daily-driver default until OQ-023 is researched and locally validated.
- rationale: The daily-driver model must balance quality, speed, context handling, and VRAM use across varied personal and project tasks.
- constraints:
  - Evaluate drafting, summarisation, planning, research, explanation, and conversational coherence.
  - Prefer a model that remains responsive during normal laptop use.
  - Validate privacy-sensitive workflows locally before routine use.
- evidence: []
- open_questions: OQ-023, OQ-019, OQ-020
- superseded_by: null

## REC-021 — Primary high-reasoning model

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, reasoning
- recommendation: Do not adopt a high-reasoning default until OQ-024 is researched and locally validated.
- rationale: High-reasoning tasks may require a larger model, longer context, or selective cloud escalation.
- constraints:
  - Evaluate multi-step reasoning, factual grounding, and resistance to confident errors.
  - Measure latency and VRAM use.
  - Retain cloud escalation for high-stakes or context-heavy work where local quality is insufficient.
- evidence: []
- open_questions: OQ-024, OQ-009, OQ-040
- superseded_by: null

## REC-022 — Primary long-context model

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, long-context
- recommendation: Do not adopt a long-context default until OQ-025 is researched and locally validated.
- rationale: Advertised context length does not guarantee useful comprehension or acceptable VRAM use.
- constraints:
  - Measure practical context limits rather than relying on advertised maxima.
  - Validate retrieval, coherence, and instruction adherence at target context lengths.
  - Use cloud escalation for work that exceeds validated local capacity.
- evidence: []
- open_questions: OQ-004, OQ-009, OQ-025
- superseded_by: null

## REC-023 — Vision and multimodal policy

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, vision, multimodal
- recommendation: Defer local vision models unless a concrete workflow requires screenshot, PDF, UI, or document-image understanding.
- rationale: Vision capability adds VRAM, complexity, and maintenance cost. It should be adopted only where it solves a recurring need.
- constraints:
  - Identify concrete use cases before selecting a vision model.
  - Evaluate OCR, screenshot understanding, and document extraction quality.
  - Do not add a vision model solely because it is available.
- evidence: []
- open_questions: OQ-026
- superseded_by: null

## REC-024 — Embedding and retrieval policy

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, embeddings, retrieval
- recommendation: Defer a production RAG stack until the primary model, runtime, and evaluation harness are validated.
- rationale: Retrieval can improve factual grounding, but it adds components and failure modes. A minimal retrieval experiment should precede production adoption.
- constraints:
  - Select embeddings only after defining document sources and retrieval tasks.
  - Evaluate retrieval quality on representative career, communication, and planning documents.
  - Keep the initial retrieval setup simple and reversible.
- evidence: []
- open_questions: OQ-015, OQ-027
- superseded_by: null

## REC-025 — Primary API and automation runtime

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, api, automation
- recommendation: Do not adopt a dedicated API runtime until OQ-028 and OQ-029 are researched and locally validated.
- rationale: The API runtime must reliably support OpenAI-compatible endpoints, structured output, tool calling, and the desired concurrency model.
- constraints:
  - Validate streaming, JSON-schema output, and tool calling on representative tasks.
  - Test model switching and concurrent requests before production use.
  - Keep the initial stack simple and reversible.
- evidence: []
- open_questions: OQ-005, OQ-028, OQ-029, OQ-030
- superseded_by: null

## REC-026 — Antigravity and VS Code workflow

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, ide, agents
- recommendation: Do not adopt an IDE-specific local-model workflow until OQ-031, OQ-032, OQ-033, and OQ-034 are researched and locally validated.
- rationale: IDE integration must support practical repository work, not merely chat completion.
- constraints:
  - Validate file editing, terminal access, diff review, and tool calling.
  - Define local-first tasks and cloud-escalation triggers.
  - Keep prompts and skills portable between IDEs where possible.
- evidence: []
- open_questions: OQ-016, OQ-031, OQ-032, OQ-033, OQ-034
- superseded_by: null

## REC-027 — Home Assistant model

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: home-assistant, local-llm
- recommendation: Do not adopt a Home Assistant model until OQ-035, OQ-036, OQ-037, and OQ-038 are researched and locally validated.
- rationale: Home Assistant requires low latency, reliable intent recognition, and dependable tool calling rather than general-purpose chat quality.
- constraints:
  - Prefer deterministic automations for safety-critical and time-sensitive routines.
  - Use an LLM only where natural-language understanding or summarisation adds clear value.
  - Validate latency, accuracy, and fallback behaviour before device control.
- evidence: []
- open_questions: OQ-035, OQ-036, OQ-037, OQ-038
- superseded_by: null

## REC-028 — Final core model set

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, model-selection
- recommendation: Do not finalise the core model set until all prerequisite research tasks and local validation results are available.
- rationale: A small, well-chosen model set should cover major jobs without redundant VRAM use or maintenance burden.
- constraints:
  - Prefer one primary model per major job.
  - Add backups only where they provide material value.
  - Define explicit roles, escalation paths, and retirement criteria.
- evidence: []
- open_questions: OQ-039, OQ-040, OQ-041
- superseded_by: null

## REC-029 — Subscription-replacement policy

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, cloud, subscription
- recommendation: Do not cancel Claude Pro or ChatGPT Go until local models pass defined task-specific thresholds for the workflows they are intended to replace.
- rationale: The objective is practical reduction of subscription dependence, not unconditional replacement of cloud models.
- constraints:
  - Define representative tasks and pass thresholds before changing subscriptions.
  - Retain cloud access for high-stakes reasoning, complex coding, or context-heavy work where local models fail.
  - Reassess after each evaluation cycle.
- evidence: []
- open_questions: OQ-009, OQ-024, OQ-033, OQ-040
- superseded_by: null

## REC-030 — Minimum evaluation harness

- status: provisional
- confidence: low
- date_decided: 2026-11-19
- last_reviewed: 2026-11-19
- scope: local-llm, evaluation, repository
- recommendation: Build a minimal evaluation harness before adopting any local model for production workflows.
- rationale: Evaluation makes model selection reproducible and prevents benchmark-driven decisions.
- constraints:
  - Start with a small representative task set.
  - Include deterministic checks and human-review rubrics.
  - Record model, quantisation, runtime, context, prompt, and result metadata.
- evidence: []
- open_questions: OQ-041
- superseded_by: null

## Immediate adoption order

1. REC-005 — Establish the primary local toolchain.
2. REC-004 — Establish the practical context and VRAM budget.
3. REC-001 — Select and validate the primary creative-writing model.
4. REC-002 — Select and validate the primary professional-writing model.
5. REC-003 — Select the default quantisation level.
6. REC-019 — Select and validate the primary coding model.
7. REC-020 — Select and validate the primary daily-driver model.
8. REC-021 — Select and validate the primary high-reasoning model.
9. REC-011 — Establish email tone-matching settings.
10. REC-012 — Establish the ATS-oriented structured-output pattern.
11. REC-026 — Establish the Antigravity and VS Code workflow.
12. REC-027 — Select and validate the Home Assistant model.
13. REC-028 — Finalise the core model set.
14. REC-029 — Define the subscription-replacement policy.
15. REC-030 — Build the minimum evaluation harness.

Do not expand into poetry, dialogue specialists, RAG, cloud GPU experiments, or advanced agent workflows until the core model, runtime, and evaluation foundations are validated.