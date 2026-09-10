# VS Code prompt file spec

## What is a .prompt.md file?

VS Code has a built-in `.prompt.md` format — reusable slash-command prompts stored as markdown files
with YAML frontmatter, invocable directly from the VS Code chat panel without copying and pasting.

Reference: https://code.visualstudio.com/docs/agent-customization/prompt-files

This is a natural companion format to the skill cards in this repo.
Every approved skill card in `skills/` can have a companion `.prompt.md` that makes it
invocable as a VS Code slash command.

## When to create a .prompt.md

Create one when:
- A skill card reaches `status: approved`
- The skill is used regularly in VS Code sessions (Phase 2 onwards)
- The skill is well-suited to in-editor invocation (code review, rewrite, extract, critique)

Do not create one for:
- Draft skills
- Skills only used in Gemini in Chrome or Antigravity (use those native formats instead)
- Skills that require page-context input that VS Code cannot provide

## File location and naming

```
skills/<surface>/<skill-id>.prompt.md
```

Example:
```
skills/claude/critique-prompt.prompt.md
skills/local-llm/local-summarise-page.prompt.md
```

## .prompt.md template

```markdown
---
mode: ask                   # ask | edit | agent
description: "One-line description of what this prompt does"
tools: []                   # e.g. ["codebase", "terminal"] for agent mode
---

<!-- Companion to skill card: skills/<surface>/<skill-id>.yaml -->
<!-- Source refs: see skill card source_refs field -->

[Prompt body here with {{input_slot}} placeholders]
```

## Mode options

| Mode | Use when |
|---|---|
| `ask` | You want a response in chat — no file edits |
| `edit` | You want the model to directly edit a file or selection |
| `agent` | You want the model to take multi-step actions with tools |

## Relationship to skill cards

The `.prompt.md` is a **runtime adapter** for VS Code — it is not the canonical artifact.
Always keep the YAML skill card as the source of truth.
The `.prompt.md` is derived from the skill card's `prompt_template` and `output_contract` fields.

If you update the skill card, update the companion `.prompt.md` in the same commit.

## Phase availability

This format becomes useful in **Phase 2** (VS Code + local LLM).
Do not create `.prompt.md` files in Phase 1 — they will not be used in Antigravity.
Tag future backlog tasks with `surface: vscode-prompt` when relevant.
