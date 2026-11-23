---
model: gemini-4-neon-orchestrator
vendor: Google
family: Gemini
aliases: [neon-orchestrator, gemini-neon-orchestrator, gemini4-neon-orchestrator, orchestrator-neon, neon-orch, gemini-pro-orchestrator-neon]
last_verified: 2026-11-23
status: current
---

# Gemini 4 Neon Orchestrator

> ⚠ Note: Gemini 4 Neon Orchestrator (`Orchestrator (Neon)` in Google Antigravity) describes the dual-model orchestration mode in Google Antigravity App, IDE extensions, and Antigravity CLI (`agy --model "Orchestrator (Neon)"`) — it is **not** a standalone Gemini API model endpoint. Here **Gemini 4 Neon** (`gemini-4-neon`) acts as the central planner and reviewer, while **Gemini 4 Hydrogen** (`gemini-4-hydrogen`) executes edits, builds, and tests in the same conversation, handing control back and forth dynamically.

## Reasoning / Thinking
- **Dual-model planner/executor loop**: Within a single agent conversation, `gemini-4-neon` handles read-only codebase exploration, planning, ambiguity resolution, and progress review, while `gemini-4-hydrogen` executes file edits, builds, and test runs.
- **Fixed orchestrator configuration**: Per official Antigravity docs, Orchestrator runs with a **fixed configuration** — you cannot select or override `thinking_level` (`--effort` and `/effort` do not apply and report that effort is not adjustable). Exact internal thinking levels used by Neon and Hydrogen inside `Orchestrator (Neon)` are not publicly documented `(unverified)`.
- **Four-phase automatic handoff**:
  1. *Planner plans*: Each user message starts with a read-only planning phase in which Neon explores the codebase, resolves ambiguities, and writes an implementation plan including re-planning trigger conditions. (Questions, reviews, or explanations requiring no edits are answered directly by Neon; small follow-ups with settled steps receive a short plan immediately.)
  2. *Hydrogen executes*: Once planned, `gemini-4-hydrogen` applies file edits, writes code, runs builds/tests, and verifies against the plan.
  3. *Friction escalation*: If Hydrogen hits a verification failure twice, an unexpected interface behavior, or an unsettled design choice, control returns to Neon to inspect conversation state, repair the plan, and resume execution.
  4. *Progress review*: On longer tasks—or when the user sends a message mid-run—Hydrogen reports progress to Neon to verify against the plan and wrap up, continue, or revise.
- **No manual CoT scaffolding**: Instructions like "Think step by step" are unnecessary; Neon handles architectural reasoning natively during the read-only planning phase.
- **Quota and latency efficiency**: Reserves `gemini-4-neon` tokens for planning, architectural judgment, and error recovery while delegating routine edits, package updates, and test iterations to `gemini-4-hydrogen`, stretching plan quota further than running Neon standalone.

## Prompting style
- **Goal- and contract-oriented prompting**: Prompt with clear objectives, architectural constraints, interface contracts, and verification requirements rather than line-by-line micromanagement ("Open file X, edit line 40..."). Let Neon's planning phase decompose the steps for Hydrogen.
- **Explicit re-planning & escalation bounds**: Because Orchestrator hands off on ambiguity, failed verification (twice), or unexpected interfaces, specify acceptance criteria, non-goals, and authoritative conventions upfront so Neon's plan includes clean checkable milestones.
- **Anchor repo rules declaratively**: Keep persistent repository conventions, style rules, and tool policies in `AGENTS.md`, `GEMINI.md`, or Antigravity skills rather than repeating them in every prompt.
- **Question/review vs. implementation intent**: Since Neon answers read-only questions, reviews, and explanations directly without delegating edits to Hydrogen, state explicitly whether you want analysis/review only or end-to-end code changes + verification.
- **Single-agent conversation scope vs. parallel orchestration**: `Orchestrator (Neon)` runs one coordinating agent inside a single conversation turn. When work needs parallel independent workers or adversarial checks, explicitly invoke Antigravity subagents, `/swarm`, `/boost`, or `/teamwork`.

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Recommended Antigravity default for day-to-day feature work, bug fixes, refactoring, and multi-file debugging: combines Neon's frontier judgment and low fabrication rate with Hydrogen's fast execution.
  - Automatic mid-task recovery when builds or tests fail twice, without manual model switching.
  - Significant quota and end-to-end latency savings compared with running `gemini-4-neon` (or `gemini-4-carbon`) on every implementation step.
- **Weaknesses and quirks**:
  - **No adjustable effort/thinking level**: Fixed configuration; if you need explicit `thinking_level` control (`low | medium | high | xhigh`) on every step—for example, distributed systems design from scratch, subtle concurrency race conditions, or multi-repo migrations—select `gemini-4-neon` or `gemini-4-carbon` directly.
  - **Overhead on trivial edits**: For package upgrades, boilerplate scaffolding, single-file tweaks, or unit tests for well-defined functions that need no planning phase, select `gemini-4-hydrogen` directly.
  - **Harness & plan availability**: Available in Antigravity App, CLI, and IDE extensions on **Google AI Ultra** and **Google AI Pro** (paid plans or trials with eligible premium devices); **not** available on Free, Google AI Plus, or Enterprise model selector tables (use Gemini API / Managed Agents with `gemini-4-neon` and `gemini-4-hydrogen` instead).
  - **Context window**: Antigravity lists `gemini-4-neon` at up to 512K tokens; exact Orchestrator session cap beyond Neon's Antigravity limit `(unverified)`.

## Output & format conventions
- Antigravity selection: choose **`Orchestrator (Neon)`** in the model selector under the prompt box, via `/model` in the CLI, or via `agy --model "Orchestrator (Neon)"` (including headless mode `agy -p "..." --model "Orchestrator (Neon)"`).
- Outputs follow Antigravity's planning and verification flow: concise read-only plan (when edits are needed), executed file diffs/command results, and verified completion summary (or direct answer for read-only questions).
- Do not include raw API sampling parameters (`temperature`, `top_p`, `top_k`) or `--effort` / `/effort` overrides; Orchestrator ignores effort changes.
- In direct Gemini API / Interactions API code outside Antigravity IDE/CLI, there is no `gemini-4-neon-orchestrator` model string: pair `gemini-4-neon` (planner turn) and `gemini-4-hydrogen` (execution turn) via `previous_interaction_id`, or configure Managed Agents (`antigravity-preview-09-2026`) with `agent_config={"type": "antigravity", "model": "gemini-4-neon"}` (single model override).

## Migration notes
- **FROM gemini-4-neon-orchestrator**:
  - When moving to a single monolithic model (including standalone `gemini-4-neon` or `gemini-4-hydrogen`), combine planning, editing, and verification instructions into one explicit workflow or multi-turn script, and specify `thinking_level` explicitly if needed.
  - When moving to `gemini-4-argon-orchestrator` or `Orchestrator (Carbon)`, no prompt structure changes are required; expect slower/deeper planning (especially on Carbon) and different plan eligibility (Carbon requires Google AI Ultra).
  - When moving to direct API pipelines, explicitly orchestrate handoffs between planner (`gemini-4-neon`) and executor (`gemini-4-hydrogen`) using `previous_interaction_id` (Interactions API) or client-managed history with preserved thought signatures.
- **TO gemini-4-neon-orchestrator**:
  - Replace rigid step-by-step tool micromanagement with goal-oriented prompts defining scope, constraints, and verifiable test/build criteria.
  - Remove `--effort` / `/effort` flags and manual `thinking_level` expectations, since Orchestrator uses a fixed configuration.
  - Move persistent coding standards and repo rules into `AGENTS.md`, `GEMINI.md`, or skills to keep prompts lean.
  - Keep read-only questions/reviews clear of edit imperatives so Neon answers directly without unnecessary implementation handoffs.

## Sources
- https://antigravity.google/docs/models/ — official Antigravity Models documentation: `Orchestrator (Neon)` model selector option, planner (`Gemini 4 Neon`) / executor (`Gemini 4 Hydrogen`) pairing, 4-step automatic handoff loop, fixed configuration (`--effort`/`/effort` not adjustable), CLI usage (`agy --model "Orchestrator (Neon)"`), plan availability (Ultra, paid/eligible-trial Pro; not Free/Plus/Enterprise), and "When to use Orchestrator" guidance.
- https://antigravity.google/blog/gemini-4-neon-in-google-antigravity — Antigravity announcement (18 Nov 2026): launch of `Gemini 4 Neon` and `Orchestrator` pairing Neon and Hydrogen, quota-stretching rationale, and benchmark context.
- https://aistudio.google.com/docs/models/gemini-4-neon — official model page for `gemini-4-neon` (planner model).
- https://aistudio.google.com/docs/models/gemini-4-hydrogen — official model page for `gemini-4-hydrogen` (execution model).
- https://aistudio.google.com/docs/choosing-a-model — Gemini API multi-step model pairing via `previous_interaction_id` and `antigravity-preview-09-2026` `agent_config` model selection.
- https://antigravity.google/docs/swarm/ — Antigravity comparison of single-agent Orchestrator vs. subagents, `/swarm`, `/boost`, and `/teamwork`.
