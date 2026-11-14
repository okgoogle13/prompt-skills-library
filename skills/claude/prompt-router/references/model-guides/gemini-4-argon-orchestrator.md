---
model: gemini-4-argon-orchestrator
vendor: Google
family: Gemini
aliases: [argon-orchestrator, gemini-argon-orchestrator, gemini4-argon-orchestrator, orchestrator-argon, argon-orch]
last_verified: 2026-11-13
status: current
---

# Gemini 4 Argon Orchestrator

> ⚠ Note: Gemini 4 Argon Orchestrator describes the multi-model and agent-based orchestration paradigm (for example in Google Antigravity or comparable agent harnesses). Here the flagship reasoning model Gemini 4 Argon (`gemini-4-argon`) acts as central strategist, architect and coordinator, while specialised high-speed workers (typically `gemini-4-hydrogen`) are assigned operational code changes, tool executions, file sweeps and test runs. This guide describes how prompts must be formulated to steer this division of labour, iterative planning loops and strict governance optimally.

## Reasoning / Thinking
- **Dual model hierarchy**: The orchestrator runs on `gemini-4-argon` with native reasoning (`thinking_level`: `high` for the initial architecture, decomposition and planning phase; `medium` for ongoing monitoring, role delegation and code review).
- **Subagent control**: The execution subagents the orchestrator calls (typically `gemini-4-hydrogen`) operate autonomously with their own reasoning depth (`high` for coding/debugging, `low` for scans and extraction). Raw API parameters for subagents do not belong in the orchestrator prompt.
- **Spec-first pattern (mandatory planning phase)**: The prompt must oblige the orchestrator to draft a formal specification or change plan (`plan.md` / architecture artifact) and wait for user approval before write operations or subagent delegations. This prevents uncontrolled token consumption and misallocation of subagents.
- **No manual CoT scaffolding**: Instructions such as "Think step by step" are superfluous; the orchestrator uses Argon's deep native reasoning for dependency analysis and structuring the problem space.
- **Quota and token conservation**: The paradigm deliberately saves expensive Argon thinking tokens by delegating costly terminal commands, file sweeps and repetitive code generation to Hydrogen subagents.

## Prompting style
- **Goal-oriented prompting ("Give Goals, Not Steps")**: Do not formulate micromanagement commands at file-line level ("Open file X, change line 40..."). Instead give high-level goals, architectural constraints, interface contracts and quality standards (e.g. "Investigate the authentication crash in the logs, design a fault-tolerant fix per our error-handling conventions, delegate the implementation to subagents and verify it via the local test suite").
- **Clear role and task division (Architect $\rightarrow$ Engineer $\rightarrow$ QA)**:
  - *Architect (Argon Orchestrator)*: System design, interfaces, data flow, dependency analysis, delegation and final approval.
  - *Engineer (Hydrogen subagent)*: Modular implementation, adherence to PEP 8/TypeScript conventions, surgical file edits.
  - *QA / verification (Hydrogen subagent)*: Running test suites, regression checks, diff validation.
- **Artifacts-as-accounting**: Define strict done criteria and proof obligations. The orchestrator may report a task as complete only once verifiable artifacts exist: 1) approved plan (`plan.md`), 2) git diff summary from the subagents, 3) successful local test logs, 4) no violation of style or architecture rules.
- **Session and context hygiene ("Single ticket / single mission")**: Do not pile unrelated tasks into one thread. Do not repeat repository rules, style guidelines and tool policies in every prompt; anchor them declaratively in `AGENTS.md`, `GEMINI.md` or custom skills.
- **Error handling and bidirectional control**: Specify in the prompt that subagents report back to the orchestrator immediately on unexpected test failures or architecture conflicts, instead of independently implementing far-reaching workarounds.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Highest success rate on complex cross-file refactorings, system migrations and long-lived agentic workflows;
  - Massive token and quota savings compared with monolithic execution on pure frontier models;
  - Structured, traceable development through explicit plan and verification artifacts;
  - Automatic error recovery through strategic re-planning when subagent steps fail.
- **Weaknesses and quirks**:
  - **Overhead on trivial tasks**: For simple single-file changes or quick one-liners, orchestration is too heavy; call `gemini-4-hydrogen` directly for these;
  - **Harness dependency**: Requires an environment that supports subagents or swarm processes (e.g. Google Antigravity, multi-agent harnesses);
  - **Latency in the planning phase**: Because of Argon's deep reasoning, the initial plan creation takes time.

## Output & format conventions
- Output formats: structured Markdown plans (implementation blueprint, `plan.md`), isolated worker briefings and summarising verification reports with git diffs and test results.
- No sampling parameters (remove `temperature`, `top_p`, `top_k`).
- Control via Antigravity orchestrator tools, subagent invocations (`invoke_subagent`, `swarm`) or CLI harness.

## Migration notes
- **FROM gemini-4-argon-orchestrator**:
  - Break multi-agent and delegation instructions down into sequential single-step prompts for monolithic models;
  - Replace specific Antigravity artifact requirements (`plan.md`, swarm briefings) with manual checklists;
  - Merge code generation and architecture planning back into a single prompt.
- **TO gemini-4-argon-orchestrator**:
  - Convert monolithic prompts ("Rewrite file X and test it") into a goal-oriented orchestration briefing;
  - Insert a binding "spec-first" clause (analysis and planning artifact before any code change);
  - Anchor the role division: Argon steers planning and review, delegates file edits and test runs to fast workers (`gemini-4-hydrogen`);
  - Define a verifiable done condition via concrete evidence (git diff, test reports);
  - Move repo-wide rules into `AGENTS.md` / `GEMINI.md` to keep the user prompt lean.

## Sources
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — official model card for Gemini 4 Argon as frontier reasoning engine.
- https://ai.google.dev/gemini-api/docs/latest-model — Google DeepMind: multi-model orchestration, dynamic routing and quota management in agentic workflows.
- https://antigravity.google/docs/orchestration — Antigravity agent orchestrator guide: spec-first pattern, artifacts-as-accounting, multi-tier subagent delegation (Argon architect / Hydrogen worker).
- https://deepmind.google/models/model-cards/gemini-4-argon/ — DeepMind model card: evaluation for complex software architecture and agentic control.
- https://ai.google.dev/gemini-api/docs/models/gemini-4-hydrogen — official model card for Gemini 4 Hydrogen as execution engine.

