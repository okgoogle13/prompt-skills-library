# Local LLM Open Questions

Status: active research register  
Last reviewed: 2026-11-14  
Scope: local LLM selection, quantisation, tooling, and writing workflows for the prompt-skills-library project.

## Purpose

This register tracks unresolved questions that could change future model-selection, quantisation, tooling, or workflow recommendations.

It is intentionally separate from `local-llm-recommendations.md`:

- Recommendations record decisions that are currently supported by evidence.
- Open questions record what still needs to be investigated before a decision can be made.

A question moves to `resolved` only when it produces a concrete recommendation or a documented decision. The resulting recommendation should then be added to the recommendations register.

## Status vocabulary

- `open` — needs research
- `in_progress` — actively being investigated
- `resolved` — answered; resulting decision belongs in the recommendations register
- `parked` — real question, but not worth researching now

## Priority policy

The laptop has already been purchased. Immediate priorities are therefore model selection and experimentation, not further hardware procurement.

Mark only questions that could change the initial local-model experiment set as `priority: high`. Do not assign artificial due dates.

## Questions

## OQ-001 — Best local creative-writing model at current VRAM

- status: open
- priority: high
- scope: local-llm, creative-writing
- question: Which local model should be the first creative-writing experiment on the purchased laptop: Gemma 4 31B, Qwen3 32B, Qwen3.6 27B, or another current model?
- why_it_matters: This determines the primary local model for fiction, dialogue, worldbuilding, and long-form drafting.
- acceptance_criteria:
  - Identify the laptop’s actual VRAM or unified-memory capacity.
  - Compare candidate models at compatible quantisation levels.
  - Assess prose quality, voice consistency, prompt fidelity, context handling, and tokens per second.
  - Recommend one primary model and one fallback model.
- evidence_to_check:
  - Official model cards and Ollama library entries
  - EQ-Bench Creative Writing results where available
  - PromptQuorum creative-writing testing
  - Local benchmark reports from credible independent sources
- related_recommendations: REC-001
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-002 — Best local model for professional and structured writing

- status: open
- priority: high
- scope: local-llm, professional-writing, structured-output
- question: Which local model best handles ATS-aware resumes, cover letters, professional emails, and tone-matched business writing?
- why_it_matters: Professional writing has different requirements from creative writing: factual accuracy, instruction following, concise revision, and reliable structured output.
- acceptance_criteria:
  - Test candidate models on resume rewriting, cover-letter drafting, email tone matching, and structured extraction tasks.
  - Measure factual drift, instruction adherence, formatting consistency, and JSON/YAML validity.
  - Recommend separate defaults for creative writing and professional writing if they differ.
- evidence_to_check:
  - Model cards and instruction-following benchmarks
  - Local business-writing guides
  - Direct evaluation on representative Australian job-application documents
- related_recommendations: REC-002
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-003 — Optimal quantisation for writing workloads

- status: open
- priority: high
- scope: local-llm, quantisation
- question: For the selected primary model, which quantisation level provides the best balance of prose quality, instruction following, speed, and VRAM headroom?
- why_it_matters: The same model can behave materially differently at Q4_K_M, Q5_K_M, and Q8_0; choosing poorly can waste VRAM or degrade writing quality.
- acceptance_criteria:
  - Test at least Q4_K_M, Q5_K_M, and Q8_0 where VRAM permits.
  - Measure output quality, latency, VRAM use, and context capacity.
  - Recommend a default quantisation and a fallback for constrained sessions.
- evidence_to_check:
  - Ollama model tags and file sizes
  - llama.cpp / GGUF quantisation documentation
  - Direct A/B evaluation on writing prompts
- related_recommendations: REC-003
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-004 — KV-cache and context overhead at long context

- status: open
- priority: high
- scope: local-llm, context-window, vram
- question: How much additional VRAM does KV cache consume at 32K, 64K, 128K, and 256K context for the selected model and quantisation?
- why_it_matters: Model weights are only part of the memory requirement. Long-context writing can fail or slow dramatically if KV cache exceeds available VRAM.
- acceptance_criteria:
  - Measure actual VRAM use at several context lengths.
  - Identify the maximum usable context before degradation or swapping.
  - Produce a practical context budget for the purchased laptop.
- evidence_to_check:
  - Model card context specifications
  - llama.cpp / Ollama runtime documentation
  - Direct runtime measurements
- related_recommendations: REC-004
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-005 — Best local toolchain for writing and agent workflows

- status: open
- priority: high
- scope: local-llm, tooling, agents
- question: Should the primary local stack be Ollama, LM Studio, Jan, or a combination, given the need for writing, IDE integration, and future agent workflows?
- why_it_matters: Tool choice affects model management, API integration, sampling controls, and how easily writing workflows can be automated.
- acceptance_criteria:
  - Evaluate installation, model discovery, API compatibility, sampling controls, and offline behaviour.
  - Test integration with at least one IDE or agent workflow.
  - Recommend a primary tool and define when to use an alternative.
- evidence_to_check:
  - Official Ollama, LM Studio, and Jan documentation
  - OpenAI-compatible API documentation
  - Direct workflow testing
- related_recommendations: REC-005
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-006 — Best small model for fast drafting and structured tasks

- status: open
- priority: medium
- scope: local-llm, small-models, structured-output
- question: Which small model, approximately 3B to 8B, is best for rapid drafting, outline generation, email templates, and JSON/YAML extraction?
- why_it_matters: A small model can handle routine drafting and structural work while preserving VRAM for a larger primary model.
- acceptance_criteria:
  - Compare at least two small models on speed, quality, and schema adherence.
  - Identify tasks where the small model is sufficient versus where escalation is required.
  - Recommend a small-model companion to the primary model.
- evidence_to_check:
  - Ollama library
  - Hugging Face model cards
  - Direct evaluation on representative tasks
- related_recommendations: REC-006
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-007 — Best specialist model for poetry and lyrical prose

- status: open
- priority: medium
- scope: local-llm, creative-writing, poetry
- question: Is Yi-1.5 34B still the best local specialist for poetry and lyrical prose, or have newer models superseded it?
- why_it_matters: Poetry and stylised prose are niche workloads where a general-purpose model may underperform.
- acceptance_criteria:
  - Compare Yi-1.5 34B against at least two current general-purpose models.
  - Assess rhythm, imagery, structural-form adherence, and avoidance of purple prose.
  - Decide whether a specialist model is worth maintaining in the local model set.
- evidence_to_check:
  - Yi model documentation
  - Creative-writing benchmarks
  - Direct poetry and lyrical-prose evaluation
- related_recommendations: REC-007
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-008 — Best model for dialogue and character voice

- status: open
- priority: medium
- scope: local-llm, creative-writing, dialogue
- question: Which local model best maintains distinct character voices across multi-character scenes and long sessions?
- why_it_matters: Dialogue-heavy writing requires consistent character differentiation, which is a common failure mode for smaller models.
- acceptance_criteria:
  - Test at least three models on multi-character scenes.
  - Measure voice consistency, speaker attribution, and dialogue naturalness.
  - Recommend a dialogue-focused model if it materially outperforms the primary model.
- evidence_to_check:
  - Command R+ model documentation
  - SillyTavern-compatible model reports
  - Direct dialogue evaluation
- related_recommendations: REC-008
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-009 — Long-context local models versus cloud models

- status: open
- priority: medium
- scope: local-llm, long-context, cloud
- question: At what document length or context requirement does cloud escalation still provide a meaningful quality advantage over local 256K-context models?
- why_it_matters: This determines when to use cloud models for novel-length drafting, large document analysis, or multi-document workflows.
- acceptance_criteria:
  - Test local 256K-context models against cloud models on progressively longer inputs.
  - Measure coherence, factual retention, and instruction adherence.
  - Define a practical threshold for cloud escalation.
- evidence_to_check:
  - Qwen3.5/3.6/3.8 model documentation
  - Cloud provider model documentation
  - Direct long-context evaluation
- related_recommendations: REC-009
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-010 — Uncensored model boundaries for professional documents

- status: open
- priority: medium
- scope: local-llm, safety, professional-writing
- question: Are there any legitimate professional-document use cases where an uncensored local model outperforms an aligned instruct model without introducing unacceptable risk?
- why_it_matters: Professional documents generally should use aligned models, but the boundary needs to be explicit rather than assumed.
- acceptance_criteria:
  - Review uncensored versus aligned model behaviour on sensitive professional tasks.
  - Define categories where uncensored models are inappropriate.
  - Produce a clear usage policy for resumes, cover letters, emails, and reports.
- evidence_to_check:
  - Hermes 3 and Dolphin model cards
  - Relevant Australian legal and platform guidance
  - Direct safety and refusal behaviour testing
- related_recommendations: REC-010
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-011 — Sampling settings for tone-matched email writing

- status: open
- priority: medium
- scope: prompt-engineering, email, local-llm
- question: What temperature, top-p, and repetition settings best produce consistent, natural email tone without hallucinated facts or unwanted variation?
- why_it_matters: Email tone matching needs controlled variation, not the higher randomness appropriate to fiction.
- acceptance_criteria:
  - Test at least three sampling configurations.
  - Evaluate tone consistency, factual stability, and formatting reliability.
  - Recommend separate defaults for creative and professional email workflows.
- evidence_to_check:
  - PromptQuorum temperature and top-p guidance
  - Direct email-tone evaluation
- related_recommendations: REC-011
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-012 — Prompt pattern for ATS-compliant structured output

- status: open
- priority: medium
- scope: prompt-engineering, ats, structured-output
- question: Which prompt pattern most reliably produces ATS-safe, machine-parseable resume and cover-letter output from local models?
- why_it_matters: ATS workflows require stable field names, valid structure, and minimal hallucination.
- acceptance_criteria:
  - Test RTF, CO-STAR, and a custom schema-first pattern.
  - Measure JSON/YAML validity, field adherence, and factual consistency.
  - Recommend one reusable prompt template.
- evidence_to_check:
  - PromptQuorum prompt-engineering guides
  - Direct ATS-oriented evaluation
- related_recommendations: REC-012
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-013 — MLX versus Ollama on Apple Silicon

- status: open
- priority: medium
- scope: local-llm, apple-silicon, tooling
- question: If the purchased laptop is Apple Silicon, does MLX provide a meaningful quality or speed advantage over Ollama for the selected writing models?
- why_it_matters: Runtime choice can affect available models, context handling, and integration options.
- acceptance_criteria:
  - Identify whether the laptop is Apple Silicon or x86.
  - If Apple Silicon, compare MLX and Ollama on the same model and prompt set.
  - Recommend a primary runtime and document any model-format constraints.
- evidence_to_check:
  - Apple MLX documentation
  - LM Studio MLX support documentation
  - Direct runtime benchmarking
- related_recommendations: REC-013
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-014 — Model-update cadence and registry maintenance

- status: open
- priority: low
- scope: local-llm, model-management
- question: How often should the local-model recommendation set be reviewed, and what triggers a mandatory review?
- why_it_matters: Local-model releases move quickly; stale recommendations can lead to poor hardware or workflow decisions.
- acceptance_criteria:
  - Define a review cadence.
  - Define triggers such as major model releases, benchmark changes, or tool updates.
  - Recommend a lightweight review checklist.
- evidence_to_check:
  - Ollama release notes
  - Hugging Face model updates
  - PromptQuorum model-update guides
- related_recommendations: REC-014
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-015 — RAG requirements for writing workflows

- status: open
- priority: low
- scope: local-llm, rag, writing
- question: Which local embedding model and RAG setup best support writing from personal documents, job descriptions, and reference material?
- why_it_matters: RAG may improve factual grounding for resumes, cover letters, and research-heavy writing, but adds complexity.
- acceptance_criteria:
  - Identify the minimum viable RAG setup.
  - Test retrieval quality on representative documents.
  - Decide whether RAG belongs in the initial workflow or should be deferred.
- evidence_to_check:
  - AnythingLLM, PrivateGPT, and Open WebUI documentation
  - Embedding-model benchmarks
  - Direct document-retrieval testing
- related_recommendations: REC-015
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-016 — Agent reliability with local tool-calling models

- status: open
- priority: low
- scope: local-llm, agents, tool-calling
- question: Which local models reliably support tool calling and multi-step agent workflows for writing and research tasks?
- why_it_matters: Agent workflows require dependable tool use, not just good prose generation.
- acceptance_criteria:
  - Test at least two local models on representative tool-calling tasks.
  - Measure task completion, schema validity, and failure recovery.
  - Recommend whether agents should use local models, cloud models, or a hybrid.
- evidence_to_check:
  - Ollama tool-calling documentation
  - MCP integration guides
  - Direct agent evaluation
- related_recommendations: REC-016
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-017 — Cloud GPU cost thresholds for large-model experiments

- status: open
- priority: low
- scope: cloud, cost, local-llm
- question: At what frequency and duration of 70B-class experiments does cloud GPU rental become more cost-effective than local hardware upgrades?
- why_it_matters: This prevents unnecessary hardware spending while preserving access to large models for occasional high-stakes work.
- acceptance_criteria:
  - Estimate local hardware cost, electricity, and maintenance.
  - Compare against RunPod, Vast.ai, and comparable Australian-accessible providers.
  - Define a monthly or per-project threshold for cloud use.
- evidence_to_check:
  - Cloud provider pricing
  - Local hardware pricing
  - PromptQuorum cost calculators
- related_recommendations: REC-017
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-018 — Australian privacy and compliance constraints

- status: open
- priority: low
- scope: privacy, compliance, local-llm
- question: What Australian privacy, employment, and AI-use considerations apply to using local and cloud LLMs for job applications and professional writing?
- why_it_matters: The original analysis leaned heavily on EU and US framing; Australian-specific guidance is needed for practical use.
- acceptance_criteria:
  - Review Australian privacy law and relevant employment-platform policies.
  - Identify data-handling constraints for personal information in resumes and cover letters.
  - Produce a concise compliance checklist.
- evidence_to_check:
  - OAIC guidance
  - Australian employment-platform policies
  - Relevant AI governance guidance
- related_recommendations: REC-018
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## Immediate research order

1. OQ-001 — Select the primary creative-writing model.
2. OQ-002 — Select the primary professional-writing model.
3. OQ-003 — Select the default quantisation level.
4. OQ-004 — Establish the practical context/VRAM budget.
5. OQ-005 — Select the primary local toolchain.

These five questions should be resolved before expanding into poetry, dialogue specialists, RAG, agents, or cloud experimentation.
