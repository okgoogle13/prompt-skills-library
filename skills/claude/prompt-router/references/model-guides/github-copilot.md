---
model: github-copilot
vendor: GitHub
family: Copilot
aliases: [copilot, github-copilot, gh-copilot, copilot-chat, copilot-edits, copilot-workspace, githubcopilot]
last_verified: 2026-11-12
status: current
---

# GitHub Copilot (Chat, Edits, Agent & Custom Instructions)

> ⚠ Note: GitHub Copilot is an agentic developer and multi-model ecosystem (VS Code, JetBrains, Visual Studio, Xcode, GitHub CLI `gh copilot`, web/Workspace). This guide covers the prompting and instruction practice for Copilot Chat, Copilot Edits, Agent Mode, and repository and custom instructions (`.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/prompts/*.prompt.md`).

## Reasoning / Thinking
- **Multi-model selection and auto-routing**: Via the model picker in Chat/Edits, Copilot supports various backend models (incl. Anthropic Claude 3.5/3.7 Sonnet, OpenAI GPT-4o/o1/o3-mini/GPT-5, Google Gemini 2.5 Pro/Flash), or **Auto** (automatic intelligent routing based on task complexity, availability and latency).
- **Reasoning models in the harness**: When reasoning models are selected (e.g. `o1`, `o3-mini`, `claude-3.7-sonnet` with thinking enabled), reasoning depth is controlled by the Copilot harness or runs natively in the model. Raw API parameters (`reasoning_effort`, `budget_tokens`) are not passed in the prompt itself.
- **No manual CoT scaffolds**: Instructions such as "Think step by step" or manual `<thinking>` tags are unnecessary or counterproductive. For agentic actions (Edits/Agent Mode) Copilot already runs its own internal planning and tool-call loops (workspace search, linting, terminal validation), whose steps are displayed as collapsible intermediate steps.
- **Plan mode and decomposition**: For complex, cross-file refactorings, first request an explicit planning phase ("Create a step-by-step change plan first and wait for approval before making code changes") to avoid uncontrolled edits across the working set.

## Prompting style
- **Precise context variables instead of vague prose**:
  - Use native chat variables: `#file:path/to/file` (or `#file`), `#folder:path`, `#selection` (currently selected code), `#editor` (active editor content), `#terminalSelection`, `#terminalLastCommand` and `#git`.
  - Use chat participants deliberately: `@workspace` for repo-wide semantic search and architecture questions, `@terminal` for shell/CLI context, `@vscode` for IDE commands and settings, `@github` for pull requests and issues.
- **Active context-window management (tab hygiene)**:
  - Copilot uses open editor tabs and file neighbourhood (Jaccard similarity, AST connections) as implicit context. Close irrelevant tabs before complex prompts to prevent context-window dilution.
  - On a topic change, clear the chat thread with `/clear` or start a new thread; stale interaction history noticeably degrades output quality after 4–6 turns.
- **Architecture for `.github/copilot-instructions.md`**:
  - Store at the repo root (`.github/copilot-instructions.md`) for repo-wide persistent rules.
  - Style: declarative, modular, bullet-point. No filler ("You are a senior developer...").
  - Focus areas: technology stack and versions, architecture patterns (e.g. feature-sliced design, strict layers), code conventions (e.g. "named exports instead of default exports", "strict TypeScript types without any"), test patterns (e.g. "Vitest, AAA pattern, no snapshot tests for business logic") and explicit negative rules ("Do not install new third-party libraries without asking").
  - Path-specific rules via `.github/instructions/*.instructions.md` with YAML frontmatter (`applyTo: "src/api/**/*.ts"`).
- **Reusable prompt files (`.github/prompts/*.prompt.md`)**:
  - Store recurring workflows (e.g. migrations, new API endpoints, test generation) in `.github/prompts/<name>.prompt.md`.
  - Markdown links in the prompt file (`[schema](../prisma/schema.prisma)`) are resolved by Copilot as context files.
- **Break tasks down granularly and set a done condition**:
  - Split large initiatives into small, testable individual steps (e.g. first schema and types, then service logic, then tests, then UI).
  - Give each task a concrete, verifiable done condition (e.g. "Change `src/auth.ts` so that `npm run test:auth` passes without errors; do not change any public method signatures").

## Strengths & weaknesses (prompt-relevant)
- **Strengths**:
  - Deep IDE integration in VS Code, JetBrains, Visual Studio and Xcode;
  - Strong multi-file editing via Copilot Edits with interactive diff review;
  - Fast semantic workspace index (`@workspace`) without manual copy-pasting of file contents;
  - Flexible customisation via repo instructions, path-specific instructions and prompt files;
  - Model variety (switching between GPT, Claude and Gemini depending on task type).
- **Weaknesses and quirks**:
  - With open or vague prompts it tends to ignore existing utility functions and write duplicates;
  - In large repositories without `#file` scoping, it can use outdated or irrelevant code locations as reference;
  - Context drift in long chat sessions;
  - Prompt caching and token budgets are set by the IDE harness and cannot be influenced directly via API headers.

## Output & format conventions
- Markdown with standardised fenced-code-block highlighting; path and line references in the format `filename:line`.
- Copilot prefers to produce edits as inline diffs or multi-file change sets in the working set, not as plain prose.
- Specific slash commands for control: `/explain` (explain code), `/fix` (fix bugs and problems in the selected code), `/tests` (generate unit tests), `/doc` (write documentation or docstrings), `/setupTests` (set up the test framework), `/clear` (reset context).

## Migration notes
- **TO GitHub Copilot**:
  - Consolidate system prompts, agent instructions or rule files (e.g. `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) into `.github/copilot-instructions.md`.
  - Switch file paths in the prompt from `@path` (Claude Code) or absolute paths to `#file:path/to/file`.
  - Remove manual CoT phrasing ("Think step by step", "Scratchpad"); instead give `#file` context, type contracts and terminating test commands.
  - Structure recurring workflows as prompt files in `.github/prompts/<name>.prompt.md`.
- **FROM GitHub Copilot**:
  - Translate context variables (`#file:...`, `#selection`, `#codebase`) into the target convention (`@path` for Claude Code, `source_docs/...` for Antigravity/Gemini CLI, or embed file contents directly).
  - Replace specific chat participants (`@workspace`, `@terminal`) and slash commands (`/fix`, `/tests`) with explicit target instructions and tool calls.
  - Transfer rules from `.github/copilot-instructions.md` into the system-specific instruction file (e.g. `CLAUDE.md`, `AGENTS.md` or system prompt).

## Sources
- https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot — official guide to prompt engineering for Copilot (providing context, single responsibility, examples, decomposition).
- https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot — configuration of `.github/copilot-instructions.md` and path-specific instructions (`.github/instructions/*.instructions.md`).
- https://docs.github.com/en/copilot/customizing-copilot/creating-prompt-files-for-github-copilot — creating and using prompt files (`.github/prompts/*.prompt.md`).
- https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/asking-github-copilot-questions-in-your-ide — use of `@workspace`, `#file`, `#selection`, `#editor`, slash commands (`/fix`, `/tests`, `/explain`).
- https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/choosing-the-model-for-copilot-chat — multi-model picker, auto-routing, Claude, GPT and Gemini backend options.
