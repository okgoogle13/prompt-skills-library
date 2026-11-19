# Local LLM Open Questions

Status: active research register
Last reviewed: 2026-11-19
Scope: local LLM selection, quantisation, tooling, coding, agents, Home Assistant, and writing workflows for the prompt-skills-library project.

## Purpose

This register tracks unresolved questions that could change future model-selection, quantisation, tooling, workflow, or subscription-replacement recommendations.

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

The laptop has already been purchased. Immediate priorities are therefore model selection, runtime selection, and experimentation, not further hardware procurement.

Mark only questions that could change the initial local-model experiment set as `priority: high`. Do not assign artificial due dates.

## Research-task ownership

Each question is owned by exactly one research task. A research task may produce evidence and proposed updates, but only the synthesis task may make the final integrated recommendation.

| Task ID | Task | Owns questions |
|---|---|---|
| `RTX5090-ENVELOPE` | RTX 5090 laptop deployment envelope | OQ-004, OQ-019, OQ-020, OQ-021 |
| `MODEL-SHORTLIST` | Model landscape and category shortlist | OQ-001, OQ-002, OQ-003, OQ-006, OQ-007, OQ-008, OQ-009, OQ-010, OQ-011, OQ-012, OQ-022–OQ-027 |
| `RUNTIME-STACK` | Runtime and serving stack | OQ-005, OQ-013, OQ-028–OQ-030 |
| `IDE-AGENTS` | IDE and agentic coding workflow | OQ-016, OQ-031–OQ-034 |
| `HOME-ASSISTANT` | Home Assistant small model | OQ-035–OQ-038 |
| `SYNTHESIS` | Final stack, routing, evaluation, and repository implementation | OQ-014, OQ-015, OQ-017, OQ-018, OQ-039–OQ-041 |

## Shared research contract

Every research agent must:

- Read this register before beginning research.
- Address only its assigned questions.
- Return findings in the shared research-dossier format defined in `local-llm-research-contract.md`.
- Classify claims as verified fact, inferred estimate, community claim, or unknown.
- Mark recommendations `provisional` when local validation is still required.
- Not mark a question `resolved` solely from web research if it requires local validation.
- Not make decisions outside its task boundary.
- Identify conflicts between credible sources rather than silently choosing one.
- Provide source links and a last-verified date for material claims.
- End with a machine-readable handoff block for the next task.

## Questions

## OQ-001 — Best local creative-writing model at current VRAM

- status: open
- priority: high
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-002 — Best local model for professional and structured writing

- status: open
- priority: high
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-003 — Optimal quantisation for writing workloads

- status: open
- priority: high
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-004 — KV-cache and context overhead at long context

- status: open
- priority: high
- research_task: `RTX5090-ENVELOPE`
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
- last_reviewed: 2026-11-19

## OQ-005 — Best local toolchain for writing and agent workflows

- status: open
- priority: high
- research_task: `RUNTIME-STACK`
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
- last_reviewed: 2026-11-19

## OQ-006 — Best small model for fast drafting and structured tasks

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-007 — Best specialist model for poetry and lyrical prose

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-008 — Best model for dialogue and character voice

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-009 — Long-context local models versus cloud models

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-010 — Uncensored model boundaries for professional documents

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-011 — Sampling settings for tone-matched email writing

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-012 — Prompt pattern for ATS-compliant structured output

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
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
- last_reviewed: 2026-11-19

## OQ-013 — MLX versus Ollama on Apple Silicon

- status: parked
- priority: low
- research_task: `RUNTIME-STACK`
- scope: local-llm, apple-silicon, tooling
- question: If an Apple Silicon machine is used, does MLX provide a meaningful quality or speed advantage over Ollama for the selected writing models?
- why_it_matters: Runtime choice can affect available models, context handling, and integration options, but the active target is an RTX 5090 laptop.
- acceptance_criteria:
  - Identify whether an Apple Silicon machine is actively used for local inference.
  - If so, compare MLX and Ollama on the same model and prompt set.
  - Recommend a primary runtime and document any model-format constraints.
- evidence_to_check:
  - Apple MLX documentation
  - LM Studio MLX support documentation
  - Direct runtime benchmarking
- related_recommendations: REC-013
- opened: 2026-11-14
- last_reviewed: 2026-11-19

## OQ-014 — Model-update cadence and registry maintenance

- status: open
- priority: low
- research_task: `SYNTHESIS`
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
- last_reviewed: 2026-11-19

## OQ-015 — RAG requirements for writing workflows

- status: open
- priority: low
- research_task: `SYNTHESIS`
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
- last_reviewed: 2026-11-19

## OQ-016 — Agent reliability with local tool-calling models

- status: open
- priority: low
- research_task: `IDE-AGENTS`
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
- last_reviewed: 2026-11-19

## OQ-017 — Cloud GPU cost thresholds for large-model experiments

- status: open
- priority: low
- research_task: `SYNTHESIS`
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
- last_reviewed: 2026-11-19

## OQ-018 — Australian privacy and compliance constraints

- status: open
- priority: low
- research_task: `SYNTHESIS`
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
- last_reviewed: 2026-11-19

## OQ-019 — Practical usable VRAM on the RTX 5090 laptop

- status: open
- priority: high
- research_task: `RTX5090-ENVELOPE`
- scope: local-llm, hardware, vram
- question: How much VRAM is realistically available for local LLM inference on the purchased RTX 5090 laptop during normal concurrent use?
- why_it_matters: Nominal VRAM is not the same as usable VRAM once the operating system, browser, IDE, display outputs, and other GPU workloads are considered.
- acceptance_criteria:
  - Establish nominal VRAM, memory bandwidth, and likely laptop power/thermal constraints.
  - Estimate realistic usable VRAM under typical development and browsing workloads.
  - Define VRAM tiers for model selection.
  - Produce a capacity matrix for model-size and quantisation decisions.
- evidence_to_check:
  - NVIDIA RTX 5090 laptop specifications
  - Laptop vendor specifications
  - CUDA, driver, and inference-runtime documentation
  - Independent RTX 5090 laptop inference reports
- related_recommendations: REC-004
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-020 — System RAM, storage, and offload constraints

- status: open
- priority: high
- research_task: `RTX5090-ENVELOPE`
- scope: local-llm, hardware, memory
- question: What system RAM, storage, CPU, and offloading constraints affect practical local-model selection on the purchased laptop?
- why_it_matters: CPU offloading, model loading, disk space, and RAM pressure can make an apparently viable model impractical.
- acceptance_criteria:
  - Establish installed RAM, storage capacity, CPU capabilities, and operating system.
  - Determine when CPU offloading is viable and when it is too slow.
  - Identify disk-space requirements for candidate models and quantisation variants.
  - Define constraints for concurrent model loading.
- evidence_to_check:
  - Laptop specifications
  - Operating-system memory-management documentation
  - llama.cpp, Ollama, and LM Studio documentation
  - Direct runtime measurements
- related_recommendations: REC-004
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-021 — Sustained performance and thermal constraints

- status: open
- priority: medium
- research_task: `RTX5090-ENVELOPE`
- scope: local-llm, hardware, performance
- question: What sustained token-throughput and thermal constraints should guide model selection on the RTX 5090 laptop?
- why_it_matters: A model may perform well in a short benchmark but become impractical during long coding, writing, or agent sessions.
- acceptance_criteria:
  - Estimate short-burst and sustained tokens-per-second ranges for candidate model tiers.
  - Identify thermal throttling, power-limit, and fan-noise considerations.
  - Define acceptable performance thresholds for interactive and batch workflows.
  - Identify workloads where a desktop GPU, cloud GPU, or smaller local model is preferable.
- evidence_to_check:
  - Laptop vendor documentation
  - NVIDIA documentation
  - Independent laptop inference benchmarks
  - Direct sustained-workload testing
- related_recommendations: REC-004
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-022 — Best local coding model

- status: open
- priority: high
- research_task: `MODEL-SHORTLIST`
- scope: local-llm, coding
- question: Which local model is the strongest practical coding model for the RTX 5090 laptop, considering code correctness, repository navigation, debugging, refactoring, and instruction following?
- why_it_matters: Coding has different requirements from writing: precise edits, tool use, context retention, and low hallucination.
- acceptance_criteria:
  - Compare at least three credible coding-oriented models at compatible quantisations.
  - Assess code generation, debugging, refactoring, test creation, and repository-context handling.
  - Assess tool-calling and structured-output reliability.
  - Recommend one primary coding model and one fallback.
- evidence_to_check:
  - Official model cards
  - Coding benchmarks, with known limitations
  - Independent coding evaluations
  - Direct evaluation on representative repository tasks
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-023 — Best local daily-driver model

- status: open
- priority: high
- research_task: `MODEL-SHORTLIST`
- scope: local-llm, daily-driver
- question: Which local model is the best all-round daily driver for chat, drafting, summarisation, planning, light research, and routine project work?
- why_it_matters: A daily-driver model must balance quality, speed, VRAM use, context handling, and reliability across varied tasks.
- acceptance_criteria:
  - Compare at least three general-purpose models at compatible quantisations.
  - Assess drafting, summarisation, planning, explanation, instruction following, and conversational coherence.
  - Measure latency and tokens per second.
  - Recommend one primary daily-driver model and one fallback.
- evidence_to_check:
  - Official model cards
  - General-purpose benchmarks
  - Independent hands-on evaluations
  - Direct evaluation on representative personal and project tasks
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-024 — Best local high-reasoning model

- status: open
- priority: high
- research_task: `MODEL-SHORTLIST`
- scope: local-llm, reasoning
- question: Which local model provides the best practical high-reasoning capability for complex planning, trade-off analysis, research synthesis, and multi-step decision support?
- why_it_matters: High-reasoning workloads may justify a larger model, longer context, or selective cloud escalation.
- acceptance_criteria:
  - Compare at least three reasoning-capable models at compatible quantisations.
  - Assess multi-step reasoning, instruction adherence, factual grounding, and resistance to confident errors.
  - Measure reasoning latency and VRAM use.
  - Define tasks where cloud escalation remains preferable.
- evidence_to_check:
  - Official model cards
  - Reasoning benchmarks, with known limitations
  - Independent evaluations
  - Direct evaluation on representative decision-support tasks
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-025 — Best local long-context model

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
- scope: local-llm, long-context
- question: Which local model provides the best practical long-context performance for large documents, repositories, transcripts, and multi-file workflows?
- why_it_matters: Advertised context length does not guarantee useful comprehension, retrieval accuracy, or acceptable VRAM use.
- acceptance_criteria:
  - Compare at least two long-context models at practical context lengths.
  - Assess coherence, factual retention, instruction adherence, and retrieval accuracy.
  - Measure VRAM use and throughput at target context lengths.
  - Recommend a practical context limit rather than relying on the advertised maximum.
- evidence_to_check:
  - Official model cards
  - Long-context benchmarks
  - Runtime documentation
  - Direct long-context evaluation
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-026 — Best local vision or multimodal model

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
- scope: local-llm, vision, multimodal
- question: Is a local vision-capable model worth including for screenshots, PDFs, UI analysis, or document extraction, and if so, which model?
- why_it_matters: Vision adds capability but also VRAM, complexity, and maintenance cost.
- acceptance_criteria:
  - Identify concrete vision use cases across career-brain, comms-hub-v2, and parents-move.
  - Compare at least two vision-capable models where relevant.
  - Assess OCR, screenshot understanding, document extraction, and UI-analysis quality.
  - Recommend whether vision belongs in the initial stack or should be deferred.
- evidence_to_check:
  - Official model cards
  - Vision benchmarks
  - Runtime documentation
  - Direct evaluation on representative documents and screenshots
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-027 — Best local embedding and reranking models

- status: open
- priority: medium
- research_task: `MODEL-SHORTLIST`
- scope: local-llm, embeddings, retrieval
- question: Which local embedding and reranking models best support private retrieval over career, communication, project, and planning documents?
- why_it_matters: Retrieval quality affects factual grounding, privacy, and the usefulness of local knowledge workflows.
- acceptance_criteria:
  - Compare at least two embedding models and, where relevant, at least one reranker.
  - Assess retrieval quality, multilingual support, model size, latency, and integration complexity.
  - Recommend a minimal retrieval setup or explicitly defer RAG.
- evidence_to_check:
  - Embedding-model documentation
  - Retrieval benchmarks
  - Ollama, LM Studio, and vector-store documentation
  - Direct retrieval evaluation on representative documents
- related_recommendations: REC-015
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-028 — OpenAI-compatible API and tool-calling reliability

- status: open
- priority: high
- research_task: `RUNTIME-STACK`
- scope: local-llm, api, tool-calling
- question: Which local runtime provides the most reliable OpenAI-compatible API, structured output, and tool-calling behaviour for the selected models?
- why_it_matters: API and tool-calling reliability determines whether local models can support automation, IDE agents, and Home Assistant workflows.
- acceptance_criteria:
  - Compare Ollama, LM Studio, llama-server, vLLM, SGLang, Jan, and Open WebUI where relevant.
  - Assess OpenAI-compatible endpoint compatibility, streaming, JSON-schema support, and tool-calling support.
  - Identify model-specific compatibility limitations.
  - Recommend a primary API runtime and a fallback.
- evidence_to_check:
  - Official runtime documentation
  - OpenAI-compatible API documentation
  - GitHub issues and release notes
  - Direct API and tool-calling tests
- related_recommendations: REC-005, REC-016
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-029 — Multi-model serving and concurrency

- status: open
- priority: medium
- research_task: `RUNTIME-STACK`
- scope: local-llm, runtime, concurrency
- question: Which runtime best supports running or switching between a primary model, small companion model, embedding model, and Home Assistant model without excessive complexity?
- why_it_matters: A practical local stack may need several models, but concurrent GPU use can create VRAM, latency, and reliability problems.
- acceptance_criteria:
  - Assess concurrent inference, model swapping, background serving, and API isolation.
  - Identify VRAM conflicts and practical limits.
  - Recommend whether to run models concurrently, sequentially, or on separate hardware.
  - Define a simple model-routing policy.
- evidence_to_check:
  - Runtime documentation
  - GPU memory-management documentation
  - Direct concurrency testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-030 — Model registry and update workflow

- status: open
- priority: medium
- research_task: `RUNTIME-STACK`
- scope: local-llm, model-management, automation
- question: What model-registry and update workflow best prevents stale, incompatible, or untracked local-model configurations?
- why_it_matters: Model releases, quantisation variants, runtime versions, and context limits change frequently.
- acceptance_criteria:
  - Define a minimal model-registry schema.
  - Define required fields for model ID, quantisation, context, VRAM, licence, runtime, and status.
  - Define triggers for review and revalidation.
  - Recommend a lightweight update checklist.
- evidence_to_check:
  - Ollama and LM Studio model-management documentation
  - Hugging Face model-card conventions
  - Existing prompt-skills-library documentation conventions
- related_recommendations: REC-014
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-031 — Antigravity IDE local-model integration

- status: open
- priority: high
- research_task: `IDE-AGENTS`
- scope: local-llm, ide, antigravity
- question: How can Antigravity IDE integrate with local models through Ollama, LM Studio, or an OpenAI-compatible endpoint, and what limitations apply?
- why_it_matters: Antigravity integration determines whether local models can participate in practical coding and agent workflows.
- acceptance_criteria:
  - Identify supported local-model connection methods.
  - Assess model selection, context handling, tool calling, file editing, terminal access, and diff review.
  - Identify unsupported or unreliable workflows.
  - Recommend a minimal local-first integration path.
- evidence_to_check:
  - Antigravity documentation
  - Local-runtime API documentation
  - Direct integration testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-032 — VS Code local-model integration

- status: open
- priority: high
- research_task: `IDE-AGENTS`
- scope: local-llm, ide, vscode
- question: Which VS Code integration approach best supports local models for coding assistance, repository work, and agent-style tasks?
- why_it_matters: VS Code may provide a more stable or flexible integration path than Antigravity for local-model workflows.
- acceptance_criteria:
  - Identify suitable VS Code extensions or native integrations.
  - Assess OpenAI-compatible endpoint configuration, tool calling, file edits, terminal access, and context handling.
  - Compare local-model and cloud-model workflows.
  - Recommend a minimal VS Code setup.
- evidence_to_check:
  - VS Code documentation
  - Extension documentation
  - Ollama and LM Studio integration guides
  - Direct integration testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-033 — Hybrid local/cloud coding policy

- status: open
- priority: high
- research_task: `IDE-AGENTS`
- scope: local-llm, cloud, coding, agents
- question: Which coding and agent tasks should remain local, and which should escalate to a cloud model?
- why_it_matters: A clear escalation policy prevents poor-quality local automation while avoiding unnecessary cloud subscription use.
- acceptance_criteria:
  - Define task categories: routine assistance, code explanation, small edits, refactoring, multi-file changes, debugging, and high-stakes implementation.
  - Define local-first eligibility rules.
  - Define cloud-escalation triggers.
  - Produce a practical routing policy for career-brain, comms-hub-v2, and parents-move.
- evidence_to_check:
  - Local-model capability evidence
  - IDE and agent documentation
  - Direct task-based evaluation
- related_recommendations: REC-009, REC-016
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-034 — Project-specific local-model workflow routing

- status: open
- priority: high
- research_task: `IDE-AGENTS`
- scope: local-llm, workflow, projects
- question: Which model and workflow should handle each major task type across career-brain, comms-hub-v2, and parents-move?
- why_it_matters: The same local stack must support different workloads without forcing every task through an unsuitable model.
- acceptance_criteria:
  - Define task categories for each project.
  - Map each category to a preferred model, runtime, prompt pattern, and escalation path.
  - Identify privacy-sensitive workflows that should remain local.
  - Produce a reusable use-case routing table.
- evidence_to_check:
  - Project documentation
  - Existing prompts and skills
  - Direct workflow testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-035 — Best small model for Home Assistant

- status: open
- priority: high
- research_task: `HOME-ASSISTANT`
- scope: local-llm, home-assistant, small-models
- question: Which small local model is the best practical choice for Home Assistant intent recognition, tool calling, and low-latency automation?
- why_it_matters: Home Assistant needs reliable, fast, predictable control rather than general-purpose chat quality.
- acceptance_criteria:
  - Compare at least three small models suitable for Home Assistant.
  - Assess intent recognition, function calling, structured output, latency, and reliability.
  - Identify VRAM/RAM requirements and quantisation options.
  - Recommend one primary model and one fallback.
- evidence_to_check:
  - Home Assistant documentation
  - Model cards
  - Ollama and LM Studio documentation
  - Direct Home Assistant integration testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-036 — Home Assistant integration path

- status: open
- priority: high
- research_task: `HOME-ASSISTANT`
- scope: home-assistant, local-llm, integration
- question: Which Home Assistant integration path best supports a local LLM while preserving reliability and avoiding unnecessary complexity?
- why_it_matters: The integration path affects latency, privacy, tool access, failure behaviour, and maintenance burden.
- acceptance_criteria:
  - Compare native Home Assistant AI options, conversation agents, and external local-model integrations.
  - Assess OpenAI-compatible endpoint compatibility and tool-calling support.
  - Identify required permissions, network configuration, and security considerations.
  - Recommend a minimal integration architecture.
- evidence_to_check:
  - Home Assistant official documentation
  - Integration documentation
  - Runtime API documentation
  - Direct integration testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-037 — Home Assistant latency and reliability threshold

- status: open
- priority: medium
- research_task: `HOME-ASSISTANT`
- scope: home-assistant, local-llm, reliability
- question: What latency, accuracy, and reliability threshold must a Home Assistant model meet before it is allowed to control automations or devices?
- why_it_matters: A model that is impressive in chat may be unsuitable for time-sensitive or safety-relevant home control.
- acceptance_criteria:
  - Define acceptable response latency for voice and text commands.
  - Define acceptable intent-recognition and tool-call accuracy.
  - Define failure and fallback behaviour.
  - Identify commands that must never rely solely on an LLM.
- evidence_to_check:
  - Home Assistant documentation
  - Local-model benchmarks
  - Direct command-testing results
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-038 — Rules-based versus LLM-based Home Assistant control

- status: open
- priority: medium
- research_task: `HOME-ASSISTANT`
- scope: home-assistant, local-llm, reliability
- question: Which Home Assistant functions should remain rules-based or template-based rather than relying on an LLM?
- why_it_matters: Deterministic automation is usually safer, faster, and more maintainable than LLM-mediated control.
- acceptance_criteria:
  - Identify suitable LLM use cases, such as natural-language commands, summaries, and ambiguous requests.
  - Identify unsuitable use cases, such as safety-critical routines and deterministic schedules.
  - Define a clear separation between deterministic automation and LLM assistance.
  - Produce a policy for when an LLM may propose but not directly execute an action.
- evidence_to_check:
  - Home Assistant automation documentation
  - Home Assistant conversation-agent documentation
  - Direct workflow testing
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-039 — Final core local-model set

- status: open
- priority: high
- research_task: `SYNTHESIS`
- scope: local-llm, model-selection
- question: What is the smallest practical core set of local models that covers daily-driver, coding, writing, reasoning, routine, retrieval, and Home Assistant needs?
- why_it_matters: A small, well-chosen model set reduces VRAM pressure, maintenance burden, and decision complexity.
- acceptance_criteria:
  - Consolidate outputs from all research tasks.
  - Recommend no more than one primary model per major job.
  - Identify backups only where they provide material value.
  - Define explicit roles, escalation paths, and retirement criteria.
- evidence_to_check:
  - All completed research dossiers
  - Local validation results
  - Project workflow requirements
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-040 — Subscription-replacement threshold

- status: open
- priority: high
- research_task: `SYNTHESIS`
- scope: local-llm, cloud, subscription
- question: Which Claude Pro and ChatGPT Go use cases can be replaced, reduced, or retained after local-model validation?
- why_it_matters: The goal is practical reduction of subscription dependence, not unconditional replacement of cloud models.
- acceptance_criteria:
  - Define representative tasks currently performed in Claude and ChatGPT.
  - Define local pass thresholds for each task category.
  - Identify tasks that should remain cloud-based.
  - Produce a staged replacement or hybrid-adoption plan.
- evidence_to_check:
  - Local-model evaluation results
  - Cloud-model task baselines
  - Project workflow requirements
- related_recommendations: REC-009
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## OQ-041 — Minimum evaluation harness

- status: open
- priority: high
- research_task: `SYNTHESIS`
- scope: local-llm, evaluation, repository
- question: What is the smallest useful evaluation harness needed to validate local models before they are adopted for production workflows?
- why_it_matters: Evaluation prevents benchmark-driven decisions and makes model recommendations reproducible.
- acceptance_criteria:
  - Define a minimal evaluation dataset for coding, writing, structured output, retrieval, and Home Assistant.
  - Define deterministic checks and human-review rubrics.
  - Define a model-guide template and result-recording format.
  - Recommend which evaluation components should be built first.
- evidence_to_check:
  - Existing prompt-skills-library conventions
  - Evaluation-tool documentation
  - Direct pilot evaluation
- related_recommendations: To be created after research
- opened: 2026-11-19
- last_reviewed: 2026-11-19

## Immediate research order

1. OQ-019 — Establish practical usable VRAM.
2. OQ-020 — Establish RAM, storage, and offload constraints.
3. OQ-004 — Establish the practical context/VRAM budget.
4. OQ-022 — Select the primary coding model.
5. OQ-023 — Select the primary daily-driver model.
6. OQ-024 — Select the primary high-reasoning model.
7. OQ-001 — Select the primary creative-writing model.
8. OQ-002 — Select the primary professional-writing model.
9. OQ-003 — Select the default quantisation level.
10. OQ-005 — Select the primary local toolchain.
11. OQ-028 — Establish API and tool-calling reliability.
12. OQ-031 — Establish Antigravity integration.
13. OQ-032 — Establish VS Code integration.
14. OQ-033 — Establish the hybrid local/cloud coding policy.
15. OQ-035 — Select the Home Assistant model.
16. OQ-039 — Select the final core local-model set.
17. OQ-040 — Define the subscription-replacement threshold.
18. OQ-041 — Define the minimum evaluation harness.

These questions should be resolved before expanding into poetry, dialogue specialists, RAG, cloud GPU experiments, or advanced agent workflows.