---
model: claude-opus-5-5-orchestrator
vendor: Anthropic
family: Claude
aliases: [opus-5-5-orchestrator, opus-orchestrator, claude-opus-orchestrator, orchestrator-opus, orchestrator-claude-opus-5-5, opus-orch]
last_verified: 2026-11-23
status: current
tier: active
profile: Antigravity-only Opus planner with Hydrogen/Sonnet executor; spec-first multi-step work; overhead on minor edits.
---

# Claude Opus 5.5 Orchestrator

> ⚠ Note: Claude Opus 5.5 Orchestrator (`Orchestrator` with Claude Opus 5.5 planner in Google Antigravity) describes the frontier cross-vendor dual-model orchestration mode available in Google Antigravity App, IDE extensions, and Antigravity CLI — it is **not** a standalone Claude API model endpoint. Here Anthropic's flagship **Claude Opus 5.5** (`claude-opus-5-5`) serves as the central planner, software architect, and review authority, while high-speed execution workers—primarily **Gemini 4 Hydrogen** (`gemini-4-hydrogen`) or **Claude Sonnet 5.5** (`claude-sonnet-5-5`)—execute code changes, terminal actions, builds, and test sweeps within the same conversation session.

## Reasoning / Thinking
- **Dual-model planner/executor loop**: Within each conversation turn, `claude-opus-5-5` operates as the lead architect handling read-only codebase exploration, architectural planning, ambiguity clarification, and progress audits, while high-speed execution workers handle surgical file edits, dependency builds, and test runs.
- **Adaptive reasoning architecture**: Opus 5.5 runs with native adaptive thinking always active. Within Antigravity's Orchestrator selector, the user can set the planner's effort tier (`Low`, `Medium`, or `High`), with `Medium` as the recommended default. Raw Anthropic API parameters (`thinking: {type: "adaptive"}` or `output_config.effort`) are managed by the Antigravity harness and must not be passed in prompt text.
- **Four-phase coordination protocol**:
  1. *Opus 5.5 plans*: Each user message begins with a read-only investigation and planning phase in which Opus 5.5 maps repository dependencies, resolves design ambiguities, and produces an explicit implementation plan (`plan.md`). (Questions, reviews, or consultations requiring no code edits are answered directly by Opus 5.5 without delegating.)
  2. *Worker executes*: Once the plan is confirmed, the execution worker (`gemini-4-hydrogen` or `claude-sonnet-5-5`) applies file diffs, executes shell commands, and verifies output against the plan.
  3. *Escalation on friction*: If the execution worker hits two consecutive test failures, encounters unexpected interface behavior, or finds unspecified architectural choices, control returns to Opus 5.5 to inspect state, repair the plan, and direct subsequent execution.
  4. *Audit and progress review*: On complex multi-step workflows, the worker reports completed milestones to Opus 5.5, which reviews the git diff against the plan and safety invariants before finalizing the response.
- **No manual CoT scaffolding**: Manual instructions like "Think step by step" or `<thinking>` scratchpad requests are redundant and may trigger Anthropic's `reasoning_extraction` refusal filter; Opus 5.5 deliberates natively during planning.
- **Quota and throughput efficiency**: Orchestrator pairs Opus 5.5's state-of-the-art reasoning and visual comprehension with Hydrogen's high-speed execution, drastically reducing token spend and latency compared to running Opus 5.5 monomorphically on every routine edit or build step.

## Prompting style
- **Goal- and deliverable-oriented prompting**: Provide high-level goals, architectural constraints, interface contracts, and acceptance criteria rather than micromanaging tool invocations ("Open file X, change line 40..."). Let Opus 5.5 construct the step-by-step roadmap for the executor.
- **Spec-first pattern**: Require an explicit specification or architectural artifact (`plan.md`) for non-trivial modifications. Opus 5.5 excels when bounded by clear interface types, invariants, and acceptance tests.
- **Visual artifacts and diagrams**: Opus 5.5 features best-in-class visual reasoning; attach UI screenshots, mockups, architecture diagrams, and error traces directly rather than transcribing them textually.
- **Declarative repository guidance**: Maintain persistent style rules, language standards, and tool bounds in `AGENTS.md`, `GEMINI.md`, or Antigravity skills to avoid context bloat in individual prompts.
- **Distinguish consultation from implementation**: State explicitly whether a prompt seeks read-only code review/analysis (answered directly by Opus 5.5) or end-to-end implementation (triggering the dual-model delegation loop).

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Premier agentic reasoning and code review: combines Opus 5.5's deep architectural judgment, low hallucination rate, and prompt-injection resilience with Hydrogen's rapid execution.
  - Native cross-vendor synergy: leverages Anthropic's strongest reasoning engine while utilizing Google's fast infrastructure for routine execution.
  - Automatic error recovery through Opus 5.5's plan repair whenever worker verification fails.
- **Weaknesses and quirks**:
  - **Harness dependency**: Available exclusively within Google Antigravity environments (App, CLI, IDE extensions) supporting multi-model orchestrator roles; not available as a single API call on the Claude API or Google Cloud Vertex AI.
  - **Overhead on minor edits**: For simple one-line fixes, documentation updates, or repetitive boilerplate, the dual-model planning phase adds unnecessary overhead; select `gemini-4-hydrogen` or `claude-sonnet-5-5` directly.
  - **Subscription availability**: Requires a Google AI Pro (non-trial/paid) or Google AI Ultra subscription in Antigravity; not available on Free or Google AI Plus tiers.
  - **Context limits**: Opus 5.5 supports up to 1M tokens; effective orchestrator session limits follow Antigravity compaction and window policies `(unverified)`.

## Output & format conventions
- Antigravity selection: open the model selector under the prompt box, hover over the **Orchestrator** row, and choose **Claude Opus 5.5** (with preferred effort, e.g. `Medium`). In CLI, select via `/model` interactive picker or configured orchestrator planner roles.
- Output flow: structured planning outline (`plan.md`), followed by executed file diffs and command outputs from the executor, concluding with a verified completion summary from Opus 5.5.
- Do not pass sampling parameters (`temperature`, `top_p`, `top_k`) or legacy `budget_tokens`; these are not supported on Opus 5.5.
- Direct Claude API / Vertex AI: `claude-opus-5-5-orchestrator` does not exist as an API model ID. Monolithic implementations should call `claude-opus-5-5` with `output_config.effort`, or manually orchestrate multi-agent handoffs in custom harnesses.

## Migration notes
- **FROM claude-opus-5-5-orchestrator**:
  - When migrating to standalone `claude-opus-5-5` (monolithic), consolidate planning, execution, and verification into a single comprehensive prompt, and specify `output_config.effort` explicitly.
  - When migrating to `gemini-4-neon-orchestrator` or `gemini-4-argon-orchestrator`, prompt structure and delegation patterns remain identical; adjust for Google-specific long-decode conventions or fixed-effort semantics.
  - When migrating to direct Claude API workflows, implement client-side agent loops or Anthropic subagent frameworks to mirror the planner/worker separation.
- **TO claude-opus-5-5-orchestrator**:
  - Shift from step-by-step tool scripts to goal-oriented architectural briefs with clear deliverables.
  - Remove manual chain-of-thought phrases ("Think step by step") and reasoning scratchpads to prevent `reasoning_extraction` filter triggers.
  - Pass visual assets, architectural diagrams, and error screenshots directly as multimodal attachments.
  - Anchor repository rules and linting standards in `AGENTS.md` / `GEMINI.md`.

## Sources
- https://antigravity.google/docs/models/ — official Antigravity Models documentation: Orchestrator planner roles, multi-model execution handoff, and Google AI Pro / Ultra subscription tiers.
- https://platform.claude.com/docs/en/models/opus-5-5/overview — official Claude Opus 5.5 model card: adaptive reasoning, effort control, 1M context window, and agentic coding benchmarks.
- https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5 — breaking changes, reasoning extraction refusals, and prompt patterns for Opus 5.5.
- https://aistudio.google.com/docs/models/gemini-4-hydrogen — official model documentation for Gemini 4 Hydrogen as execution engine.
- https://antigravity.google/docs/subagents — Antigravity multi-agent orchestration architecture and planner/worker handoff lifecycle.
