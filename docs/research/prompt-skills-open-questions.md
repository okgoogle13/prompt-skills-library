# Prompt Skills Open Questions

Status: active research register  
Last reviewed: 2026-11-14  
Scope: prompt refinement, prompt routing, Agent Skills architecture, evaluation, communications second brain, plugin consolidation, and Gemini Spark portability for the prompt-skills-library project.

## Purpose

This register tracks unresolved questions that could change future prompt-skills-library architecture, workflow, evaluation, or implementation decisions.

It is separate from `local-llm-open-questions.md`:

- `local-llm-open-questions.md` tracks local-model selection, quantisation, tooling, and writing workflows.
- This register tracks portable prompt-and-skills library design and research.

A question moves to `resolved` only when it produces a concrete recommendation or a documented decision. The resulting recommendation should then be added to the relevant recommendations or decision record.

## Status vocabulary

- `open` — needs research
- `in_progress` — actively being investigated
- `resolved` — answered; resulting decision belongs in a recommendations or decision record
- `parked` — real question, but not worth researching now

## Priority policy

Mark a question `priority: high` when it blocks multiple later workstreams or is required before a useful implementation can begin. Do not assign artificial due dates.

## Questions

## OQ-PS-001 — Minimum model-neutral evaluation architecture

- status: open
- priority: high
- scope: evaluation, prompts, skills, agent-workflows
- question: What is the smallest evaluation architecture that works immediately for Claude and Gemini while extending to local LLMs without redesign?
- why_it_matters: The evaluation harness is the highest-priority gap because it determines whether prompt, skill, and workflow changes produce measurable quality improvements.
- acceptance_criteria:
  - Define the minimum viable evaluation architecture for Claude and Gemini.
  - Define an extension path for local models that does not require redesign.
  - Recommend an `evals/` directory layout and evaluation-case schema.
  - Recommend a practical pre-merge evaluation workflow.
- evidence_to_check:
  - Anthropic evaluation documentation
  - Google Gemini / Vertex AI evaluation documentation
  - promptfoo, OpenAI Evals, LangSmith, Langfuse, DeepEval, Ragas, Inspect AI, HELM, and LM Evaluation Harness
  - Direct repository fit and maintenance assessment
- related_questions: OQ-PS-002, OQ-PS-006, OQ-PS-007
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-002 — Evaluation-method mapping

- status: open
- priority: high
- scope: evaluation, prompts, skills, agent-workflows
- question: Which evaluation method should be used for each quality dimension: deterministic assertions, rubrics, golden datasets, regression suites, A/B tests, pairwise comparison, human review, or LLM-as-judge review?
- why_it_matters: Choosing the wrong method can make evaluation expensive, subjective, or unable to detect meaningful regressions.
- acceptance_criteria:
  - Map each evaluation dimension to a preferred method and fallback method.
  - Prefer deterministic checks where practical.
  - Define when human review or LLM-as-judge review is necessary.
  - Produce a scoring rubric that separates automated checks, human review, LLM-as-judge review, and task-outcome evaluation.
- evidence_to_check:
  - Evaluation methodology for task success, factual accuracy, instruction following, format compliance, completeness, concision, safety, refusal behaviour, and source grounding
  - Prompt-level and agent-level evaluation methods
  - Local-model transferability of cloud-oriented rubrics
- related_questions: OQ-PS-001
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-003 — Canonical skill architecture

- status: open
- priority: high
- scope: skills, architecture, portability
- question: Should the repository maintain one canonical skill format, runtime-specific adapters, or both?
- why_it_matters: This determines how prompt and skill behaviour is shared across Claude Code, Gemini, Antigravity, Codex CLI, and local runtimes without duplicating logic.
- acceptance_criteria:
  - Define the canonical `SKILL.md` structure and required versus optional metadata.
  - Define what belongs in metadata, skill body, references, examples, scripts, and assets.
  - Recommend whether runtime adapters are required and, if so, their minimum scope.
  - Produce minimal and complex skill templates.
  - Define versioning, provenance, deprecation, and testing governance.
- evidence_to_check:
  - Anthropic Agent Skills documentation and `anthropics/skills`
  - Agent Skills specification and `SKILL.md` conventions
  - Progressive-disclosure patterns
  - Runtime-specific constraints for Claude Code, Gemini, Codex CLI, Antigravity, and local runtimes
- related_questions: OQ-PS-007, OQ-PS-011
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-004 — Router target resolution

- status: open
- priority: high
- scope: prompt-router, prompt-optimisation, UX
- question: How should `prompt-brain` infer the source and target model or runtime while asking at most one material clarifying question?
- why_it_matters: The current invocation pathway is too rigid; natural-language routing is required to make model-guide intelligence usable without requiring slash commands, model IDs, or rigid argument formats.
- acceptance_criteria:
  - Define the target-resolution order for explicit user requests, active runtime, prompt-embedded model references, and defaults.
  - Define source-model resolution rules.
  - Define the single-question clarification threshold.
  - Define safe behaviour when a model guide is unavailable, stale, contradictory, or unknown.
  - Produce routing test cases for optimise, migrate, review, clarify, missing model information, and unavailable guides.
- evidence_to_check:
  - Existing `prompt-brain`, `optimize-prompt`, and `migrate-prompt` behaviour
  - Model-guide registry and guide contents
  - Runtime invocation constraints
- related_questions: OQ-PS-008, OQ-PS-009, OQ-PS-010
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-005 — Communications second-brain architecture

- status: open
- priority: high
- scope: communications, knowledge-management, voice, policy
- question: What is the minimum architecture that reliably separates immutable sources, derived notes, reusable communication patterns, voice profiles, drafting rules, policy invariants, drafts, approvals, and evaluation cases?
- why_it_matters: The communications hub needs consistent, high-quality drafting without losing voice, violating policy, or treating inferred material as established fact.
- acceptance_criteria:
  - Define the minimum viable repository or knowledge-base layout.
  - Define the data model for sources, claims, communication patterns, voice attributes, drafting rules, policy invariants, approval states, and revision history.
  - Define a retrieval strategy that preserves citations and prevents unsupported synthesis.
  - Define a freshness and retirement workflow for sources, summaries, policies, and voice rules.
  - Define the smallest implementation that avoids overengineering.
- evidence_to_check:
  - Karpathy-inspired second-brain and source-separation patterns
  - CODE, Zettelkasten, atomic notes, and progressive summarisation methods
  - Retrieval-augmented generation patterns for personal knowledge bases
  - Entity, relationship, claim, and evidence-extraction methods
- related_questions: OQ-PS-012, OQ-PS-013, OQ-PS-014, OQ-PS-015, OQ-PS-016
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-006 — Shared research output contract

- status: open
- priority: high
- scope: research, multi-agent, documentation
- question: What schemas and output artefacts must every research agent return so their outputs can be consolidated into the repository without divergent formats or duplicated research?
- why_it_matters: Multiple research agents can produce incompatible reports; a shared contract is needed to keep research synchronised and auditable.
- acceptance_criteria:
  - Define the canonical open-questions and recommendations registers.
  - Define the required output artefacts for each research task.
  - Define schemas for model, runtime, source, and decision records.
  - Define conflict-resolution rules when agents disagree.
  - Map every open question to exactly one owning research task.
- evidence_to_check:
  - Existing repository research plan and contract documents
  - Existing open-questions and recommendations registers
  - Research-task routing and dependency requirements
- related_questions: OQ-PS-017, OQ-PS-018
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-007 — Spark model-guide packaging

- status: open
- priority: high
- scope: gemini-spark, portability, model-guides
- question: Which model-guide packaging approach best balances context cost, maintenance burden, staleness risk, and Spark usability: one combined reference, separate model files, task-specific attachments, or a hybrid core-plus-optional approach?
- why_it_matters: Spark cannot be assumed to have local filesystem access, shell execution, dynamic web fetching, persistent memory, or Claude-specific plugin infrastructure.
- acceptance_criteria:
  - Compare all four packaging options on setup effort, context cost, maintenance burden, update isolation, staleness risk, and compatibility with canonical guides.
  - Recommend the simplest approach that supports immediate use.
  - Preserve a path to richer local-model support later.
  - Define fallback behaviour when required guidance is unavailable.
- evidence_to_check:
  - Gemini Skills and Spark Task documentation
  - Existing model-guide registry and guide contents
  - Direct Spark packaging and invocation testing
- related_questions: OQ-PS-003, OQ-PS-004, OQ-PS-010
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-008 — Universal prompt-refinement rules

- status: open
- priority: medium
- scope: prompt-optimisation
- question: Which prompt-refinement patterns are genuinely model-neutral rather than vendor-specific, and which should be adopted into the prompt-refiner specification?
- why_it_matters: A portable refiner must avoid encoding vendor-specific behaviour as universal best practice.
- acceptance_criteria:
  - Extract reusable patterns from Anthropic, Gemini, Codex, and model-agnostic sources.
  - Distinguish universal patterns from runtime-specific adaptations.
  - Produce a concise universal refinement rule set.
  - Identify anti-patterns including token bloat, contradictory instructions, excessive role-play, vague quality language, and unsupported model claims.
- evidence_to_check:
  - Anthropic prompt-engineering documentation and interactive tutorial
  - Google Gemini prompting documentation
  - OpenAI Codex prompting guidance
  - Model-agnostic prompt-engineering research and maintained open-source tools
- related_questions: OQ-PS-004, OQ-PS-009
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-009 — Prompt diagnosis and clarification threshold

- status: open
- priority: medium
- scope: prompt-optimisation
- question: What is the minimum diagnosis checklist that reliably identifies ambiguity, missing context, conflicting constraints, weak output specification, and absent verification, and when should the refiner ask a clarifying question rather than infer?
- why_it_matters: The refiner must identify material weaknesses without inventing requirements or asking unnecessary questions.
- acceptance_criteria:
  - Define a structured diagnosis checklist covering goal, audience, inputs, constraints, output format, success criteria, risks, and verification.
  - Define a reproducible weakness-severity model.
  - Define when a weakness is material versus stylistic.
  - Define the clarification threshold and question format.
  - Produce 10–20 diagnostic test cases.
- evidence_to_check:
  - Prompt-quality and failure-mode taxonomies
  - Existing optimise-prompt weakness categories
  - Direct diagnostic test cases
- related_questions: OQ-PS-004, OQ-PS-008
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-010 — Prompt-to-skill promotion criteria

- status: open
- priority: medium
- scope: prompt-optimisation, skills
- question: What criteria determine when a refined prompt should become a reusable skill rather than remain a one-off prompt?
- why_it_matters: Premature skill creation creates overlap, maintenance burden, and token cost; delayed promotion loses reusable workflow value.
- acceptance_criteria:
  - Define recurrence, stability, complexity, audience, and maintenance thresholds.
  - Define when a prompt should remain model-neutral versus become runtime-specific.
  - Define the minimum evidence required before promotion.
  - Produce a lightweight promotion and retirement workflow.
- evidence_to_check:
  - Existing prompt library and skill inventory
  - Agent Skills governance guidance
  - Direct usage-frequency and maintenance-cost assessment
- related_questions: OQ-PS-003, OQ-PS-008
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-011 — Skill validation cases

- status: open
- priority: medium
- scope: skills, evaluation
- question: Which validation cases best test whether a skill triggers correctly, follows instructions, produces an acceptable output, and avoids excessive context or token cost?
- why_it_matters: Skills need repeatable acceptance checks before they can be considered reliable or promoted.
- acceptance_criteria:
  - Define at least 10 validation cases.
  - Cover trigger accuracy, instruction following, output quality, context efficiency, regression detection, and unsafe or out-of-scope behaviour.
  - Define pass/fail criteria for each case.
  - Integrate the cases with the evaluation harness.
- evidence_to_check:
  - Agent Skills specification
  - Existing skill implementations
  - Evaluation-harness design
- related_questions: OQ-PS-001, OQ-PS-002, OQ-PS-003
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-012 — Voice-profile extraction and review

- status: open
- priority: medium
- scope: communications, voice, knowledge-management
- question: How can a voice profile be extracted from approved communications without overfitting to individual examples or treating inferred traits as established facts?
- why_it_matters: Voice profiles must remain stable and evidence-based while allowing appropriate audience and context adaptation.
- acceptance_criteria:
  - Define a voice-profile schema covering core attributes, audience tone, vocabulary, formatting, forbidden language, examples, evidence, and provenance.
  - Define an extraction workflow from curated approved communications.
  - Define a review workflow for adding, changing, or retiring a voice rule.
  - Define a voice-consistency test suite.
- evidence_to_check:
  - Voice profiling and author-style analysis methods
  - Style-guide and editorial-standard patterns
  - Few-shot and exemplar-based writing methods
  - Direct evaluation on representative communications
- related_questions: OQ-PS-005, OQ-PS-013, OQ-PS-016
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-013 — Style, context, and policy separation

- status: open
- priority: medium
- scope: communications, voice, policy
- question: How should the system distinguish stable personal style, audience-specific adaptation, context-specific wording, and non-negotiable policy constraints?
- why_it_matters: Conflating these categories can cause inconsistent drafting, inappropriate tone, or silent policy violations.
- acceptance_criteria:
  - Define explicit categories and precedence rules.
  - Define how audience and context modify style without changing policy.
  - Define how policy invariants block, warn, or require approval.
  - Produce representative examples for each category.
- evidence_to_check:
  - Voice-profile and policy-invariant schemas
  - Policy-as-code and guardrail patterns
  - Human-in-the-loop approval workflows
- related_questions: OQ-PS-005, OQ-PS-012, OQ-PS-014
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-014 — Reusable communication patterns

- status: open
- priority: medium
- scope: communications, templates
- question: Which communication patterns are high-value enough to formalise first, and how can they remain adaptable rather than becoming brittle templates?
- why_it_matters: Rigid templates can produce generic or inappropriate output, while unstructured patterns are difficult to reuse consistently.
- acceptance_criteria:
  - Identify 10–20 high-value communication patterns.
  - Define a pattern schema covering purpose, audience, triggers, inputs, structure, voice constraints, policy constraints, examples, anti-patterns, approval status, version, and evaluation results.
  - Define when a pattern is too specific, too generic, or unsafe to reuse.
  - Define a review and retirement process.
- evidence_to_check:
  - Communication-pattern and template-design methods
  - Existing approved communications
  - Direct pattern-reuse testing
- related_questions: OQ-PS-005, OQ-PS-012, OQ-PS-013
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-015 — Policy-invariant enforcement

- status: open
- priority: medium
- scope: communications, policy, safety
- question: Which policy checks must be deterministic rather than LLM-based, and where is human approval mandatory before a consequential communication is sent?
- why_it_matters: LLM-based checking can silently weaken, bypass, or reinterpret policy constraints; deterministic validation and human approval are needed for consequential communications.
- acceptance_criteria:
  - Define a policy-invariant schema covering statement, scope, rationale, authority, severity, enforcement method, exceptions, approval requirements, review date, and failure action.
  - Distinguish absolute invariants, strong preferences, context-dependent guidance, and advisory recommendations.
  - Define deterministic validators where possible.
  - Define audit, waiver, escalation, and violation-handling workflows.
- evidence_to_check:
  - Policy-as-code, guardrail, schema-validation, and deterministic-check patterns
  - Approval-workflow and audit-trail patterns
  - Privacy, confidentiality, retention, and sensitive-information guidance
- related_questions: OQ-PS-005, OQ-PS-013, OQ-PS-016
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-016 — Communications evaluation cases

- status: open
- priority: medium
- scope: communications, evaluation
- question: Which evaluation cases best measure voice consistency, audience adaptation, factual grounding, policy compliance, formatting, pattern selection, escalation, revision quality, and retrieval citation accuracy?
- why_it_matters: Communications quality cannot be assessed reliably from final text alone; the complete drafting workflow and its evidence chain need evaluation.
- acceptance_criteria:
  - Define 10–20 starter evaluation cases.
  - Include voice consistency, audience adaptation, factual grounding, policy compliance, formatting, reusable-pattern selection, escalation, refusal or clarification, revision quality, and retrieval citation accuracy.
  - Define a workflow that turns edits, approvals, and rejections into future evaluation cases.
  - Define a pre-acceptance evaluation workflow for voice rules, policies, patterns, and drafting workflows.
- evidence_to_check:
  - Communications evaluation criteria
  - Golden datasets, regression suites, rubrics, pairwise comparison, and A/B testing
  - Retrieval-quality evaluation methods
- related_questions: OQ-PS-001, OQ-PS-002, OQ-PS-005, OQ-PS-012, OQ-PS-015
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-017 — Plugin consolidation capability set

- status: open
- priority: medium
- scope: plugin-consolidation, prompt-optimisation
- question: Which capabilities overlap across Prompt Tightener, Prompt Optimizer, Prompt Fixer, Prompt Enhancer, and Prompt Coach, and which shared capability set should the consolidated prompt-brain system retain?
- why_it_matters: Consolidation should remove duplication without losing useful variation or creating an oversized, overlapping skill system.
- acceptance_criteria:
  - Audit each plugin for trigger conditions, input/output contract, workflow, examples, references, scripts, licence, maintenance, and security.
  - Produce a comparison matrix and adopt/adapt/merge/discard decision framework.
  - Define the minimum shared capability set.
  - Recommend a router-plus-shared-references architecture where appropriate.
- evidence_to_check:
  - Downloaded plugin folders and their documentation
  - Plugin licences, maintenance status, and security posture
  - Existing prompt-brain capabilities
- related_questions: OQ-PS-004, OQ-PS-008, OQ-PS-009
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-018 — Provenance and attribution model

- status: open
- priority: medium
- scope: governance, provenance, open-source
- question: How should adapted open-source material, downloaded plugins, model guides, and research sources be attributed, versioned, and provenance-tracked?
- why_it_matters: Adapted material must remain auditable and legally usable without turning provenance tracking into excessive overhead.
- acceptance_criteria:
  - Define minimum provenance fields for adapted material.
  - Define attribution and licence-compliance requirements.
  - Define versioning and deprecation rules.
  - Define where provenance records live in the repository.
- evidence_to_check:
  - Source licences and upstream repositories
  - Existing `sources/` and `governance/` conventions
  - Applicable open-source attribution practices
- related_questions: OQ-PS-003, OQ-PS-006, OQ-PS-017
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-019 — Karpathy conduct baseline

- status: open
- priority: medium
- scope: conduct, agent-behaviour
- question: Which Karpathy-derived principles are most reliably operationalisable as model-neutral agent conduct rules, and what wording and behavioural tests prevent them from becoming vague instructions?
- why_it_matters: The conduct baseline establishes shared behaviour for clarify-before-acting, simplicity-first, surgical changes, and goal-driven verification.
- acceptance_criteria:
  - Identify the most credible primary and secondary sources.
  - Recommend canonical wording for `core01-clarify-and-scope.md` and `core05-code-change-discipline.md`.
  - Define behavioural tests for each rule.
  - Identify existing implementations worth adapting, adapting with changes, or rejecting.
- evidence_to_check:
  - Karpathy primary sources and credible secondary analysis
  - Existing `CLAUDE.md`, `AGENTS.md`, system-prompt, and skill implementations
  - Direct behavioural testing
- related_questions: OQ-PS-003, OQ-PS-011
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## OQ-PS-020 — Initial build sequence and risk assumptions

- status: open
- priority: medium
- scope: implementation, governance
- question: Which five assets should be built or adopted first, what are the first three repository changes, which work must be deferred, and which three assumptions carry the highest implementation risk?
- why_it_matters: A prioritised sequence prevents premature complexity and ensures the first changes produce verifiable value.
- acceptance_criteria:
  - Recommend the five initial assets to build or adopt.
  - Define the first three repository changes and their acceptance criteria.
  - Define what should not be built yet.
  - Identify the three highest-risk assumptions and a validation plan for each.
- evidence_to_check:
  - Research conclusions from all workstreams
  - Existing repository structure and conventions
  - Direct implementation-cost and dependency assessment
- related_questions: OQ-PS-001, OQ-PS-003, OQ-PS-005, OQ-PS-006
- opened: 2026-11-14
- last_reviewed: 2026-11-14

## Immediate research order

1. OQ-PS-001 — Establish the minimum model-neutral evaluation architecture.
2. OQ-PS-002 — Define the evaluation-method mapping.
3. OQ-PS-003 — Establish the canonical skill architecture.
4. OQ-PS-004 — Define router target resolution and clarification rules.
5. OQ-PS-005 — Establish the communications second-brain architecture.
6. OQ-PS-006 — Establish the shared research output contract.
7. OQ-PS-007 — Resolve Spark model-guide packaging.

These seven questions should be resolved before expanding into detailed prompt-refinement rules, plugin consolidation, communications evaluation, or broader runtime adapters.
