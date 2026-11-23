---
model: gemini-4-carbon-orchestrator
vendor: Google
family: Gemini
aliases: [carbon-orchestrator, gemini-carbon-orchestrator, gemini4-carbon-orchestrator, orchestrator-carbon, carbon-orch]
last_verified: 2026-11-23
status: current
---

# Gemini 4 Carbon Orchestrator

> ⚠ Note: Gemini 4 Carbon Orchestrator (`Orchestrator (Carbon)` in Google Antigravity) describes the frontier dual-model orchestration mode in Google Antigravity App, IDE extensions, and Antigravity CLI (`agy --model "Orchestrator (Carbon)"`) — it is **not** a standalone Gemini API model endpoint. Here Google's most capable reasoning engine, **Gemini 4 Carbon** (`gemini-4-carbon`), acts as the central strategist, system architect, and review authority, while **Gemini 4 Hydrogen** (`gemini-4-hydrogen`) executes implementation edits, builds, and test sweeps within the same conversation session.

## Reasoning / Thinking
- **Dual-model planner/executor loop**: Within a single conversation turn, `gemini-4-carbon` conducts deep read-only codebase exploration, architectural trade-off analysis, formal interface verification, and progress auditing, while `gemini-4-hydrogen` executes surgical file edits, terminal commands, builds, and test suites.
- **Fixed orchestrator configuration**: Per official Antigravity documentation, Orchestrator runs with a **fixed configuration** — effort is not adjustable via `--effort` or `/effort` (running `/effort` while Orchestrator is selected reports that effort is not adjustable). In Enterprise / Application Default Credentials (`AGY_ADC_AUTH`) environments, Orchestrator defaults to Carbon (High) planning paired with Hydrogen (High) execution.
- **Four-phase automatic handoff**:
  1. *Carbon plans*: Each user message begins with a read-only planning phase in which Carbon investigates the problem, drafts a concrete specification and implementation plan (`plan.md`), and specifies triggers for re-planning. (Read-only questions, architectural audits, and security reviews requiring no code modifications are answered directly by Carbon without delegating.)
  2. *Hydrogen executes*: Once the plan is established, `gemini-4-hydrogen` takes over to apply file edits, run builds, execute tests, and verify results against the specification.
  3. *Friction escalation*: If Hydrogen encounters two consecutive verification failures, an interface behaving inconsistently with the plan, or an unaddressed edge case, execution returns immediately to Carbon to inspect state, repair the plan, and hand back to Hydrogen.
  4. *Audit and review*: On longer tasks, Hydrogen reports milestones back to Carbon, which audits the diff, checks safety/correctness invariants, and concludes the turn or directs the next phase.
- **No manual CoT scaffolding**: Manual chain-of-thought phrases ("Think step by step", pseudo-scratchpads) are counterproductive; Carbon natively executes deep verification loops and test-time compute.
- **Maximum quota conservation**: Carbon's extreme reasoning compute carries the highest token cost in the Gemini lineup ($10.00–$20.00 per 1M output tokens); delegating routine edits, dependency updates, and repetitive test sweeps to Hydrogen significantly conserves Carbon quota.

## Prompting style
- **Goal- and invariant-driven prompting**: Provide high-level goals, formal invariants, acceptance tests, and interface contracts rather than file-line micromanagement ("Open file X, change line 40..."). Let Carbon decompose the architecture and specify tasks for Hydrogen.
- **Strict specification contracts ("Spec-First")**: Carbon excels when given explicit acceptance criteria, type signatures, threat boundaries, and non-functional requirements. Ensure the prompt mandates that Carbon produce a concrete specification before execution starts.
- **Clear review vs. implementation intent**: Clearly distinguish between read-only architectural reviews (which Carbon answers directly) and end-to-end modification tasks (which trigger the Carbon $\rightarrow$ Hydrogen delegation loop).
- **Declarative repository guidance**: Anchor persistent repository conventions, coding standards, and safety bounds in `AGENTS.md`, `GEMINI.md`, or Antigravity skills rather than restating them in every prompt.
- **Single-task conversation hygiene**: Orchestrator maintains tight state within a single coordinated workflow; avoid interleaving unrelated features or divergent refactorings in a single thread. For independent parallel workstreams, invoke `/swarm`, `/boost`, or Antigravity subagents.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Highest reasoning ceiling in Antigravity: ideal for mission-critical software architecture, zero-day vulnerability patching (SEC-bench), complex concurrency and distributed systems design, and formal verification.
  - Substantial quota and latency savings over running standalone `gemini-4-carbon` across all implementation steps.
  - Automatic mid-flight plan repair when subagent edits or test runs encounter unexpected friction.
- **Weaknesses and quirks**:
  - **Plan availability**: Available exclusively on **Google AI Ultra** and **Gemini Enterprise** (with Application Default Credentials `AGY_ADC_AUTH`). On **Google AI Pro**, Gemini 4 Carbon is marked `Unavailable (i)` in the model selector, and `Orchestrator (Carbon)` is excluded from both the Orchestrator planner submenu and CLI `agy models` (Google AI Pro provides `Orchestrator (Neon)`, `Orchestrator (Argon)`, and `Orchestrator (Claude Opus 5.5)`).
  - **Overhead on routine tasks**: For simple single-file edits, documentation tweaks, package bumps, or boilerplate scaffolding, Orchestrator introduces unnecessary planning latency; select `gemini-4-hydrogen` or `gemini-3.8-flash` directly.
  - **No manual effort adjustment**: Effort cannot be changed via `/effort` while Orchestrator is active. For direct control over `thinking_level` (`low | medium | high`), select standalone `gemini-4-carbon`.
  - **Context window**: Standalone Carbon offers a 1M unified context window; session persistence and history compaction follow Antigravity orchestrator defaults `(unverified)`.

## Output & format conventions
- Antigravity selection: choose **`Orchestrator (Carbon)`** in the model selector, or run `agy --model "Orchestrator (Carbon)"` (including headless mode `agy -p "..." --model "Orchestrator (Carbon)"`).
- Output structure: structured implementation plan (`plan.md` artifact), followed by executed diffs and test logs from Hydrogen, ending with a verified completion summary from Carbon.
- Do not pass sampling parameters (`temperature`, `top_p`, `top_k`) or effort flags; Orchestrator runs under a fixed configuration.
- Direct API code outside Antigravity: `gemini-4-carbon-orchestrator` does not exist as an API model ID. Pair `gemini-4-carbon` (planner turn) and `gemini-4-hydrogen` (executor turn) via the Interactions API (`previous_interaction_id`), preserving thought signatures across turns.

## Migration notes
- **FROM gemini-4-carbon-orchestrator**:
  - When migrating to a single monolithic model (such as standalone `gemini-4-carbon`), combine architectural planning, code changes, and test instructions into a single sequential prompt, and configure `thinking_level` explicitly.
  - When migrating to `gemini-4-argon-orchestrator` or `gemini-4-neon-orchestrator`, prompt structure remains identical; expect faster planning phases with lower test-time compute depth, suitable for standard Pro tiers.
  - When migrating to direct API code, implement explicit turn-by-turn state management between Carbon and Hydrogen using `previous_interaction_id`.
- **TO gemini-4-carbon-orchestrator**:
  - Transform step-by-step tool instructions into goal-oriented architectural briefs with rigorous acceptance criteria and edge cases.
  - Remove all manual `--effort` / `/effort` parameters and sampling flags.
  - Separate read-only architectural questions from write tasks so Carbon can answer directly without engaging the executor.
  - Ensure subscription eligibility (Google AI Ultra or Gemini Enterprise).

## Sources
- https://antigravity.google/docs/models/ — official Antigravity Models documentation: `Orchestrator (Carbon)` model selector option, planner (`Gemini 4 Carbon`) / executor (`Gemini 4 Hydrogen`) pairing, 4-step handoff loop, fixed configuration, CLI usage (`agy --model "Orchestrator (Carbon)"`), and Google AI Ultra tier requirement.
- https://antigravity.google/blog/gemini-4-carbon-in-google-antigravity — Antigravity launch blog: Gemini 4 Carbon integration as primary architecture and safety-audit engine for enterprise agent swarms and Orchestrator.
- https://aistudio.google.com/docs/models/gemini-4-carbon — official model card for `gemini-4-carbon` (planner model).
- https://aistudio.google.com/docs/models/gemini-4-hydrogen — official model card for `gemini-4-hydrogen` (execution model).
- https://antigravity.google/docs/enterprise — Gemini Enterprise and Application Default Credentials (`AGY_ADC_AUTH`) Orchestrator configuration.
