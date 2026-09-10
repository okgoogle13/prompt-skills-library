# CLAUDE.md
# Instructions for Claude Code working in this repo

## Project identity

This is a curated, evidence-based prompt and skills library.
Its purpose is to adapt credible existing best practices into reusable, versioned artifacts
for Gemini in Chrome skills, Claude workflows, Antigravity orchestration, and local LLM use.

## Anti-reinvention rule

Before inventing any new structure, schema, workflow, or taxonomy:
1. Check `sources/registry.md` for an existing credible source that covers the need
2. Check existing prompt cards and skill cards for overlap
3. Only propose a new pattern if there is a documented gap
Always justify why adaptation of existing best practice is not enough.

## Repo structure

```
knowledge/         <- normalized source material (markdown, frontmatter)
schemas/           <- canonical YAML schemas — do not modify without versioning
skills/            <- runtime-adapted skill variants per surface
  chrome-gemini/   <- Gemini in Chrome browser skills
  claude/          <- Claude-specific prompt variants
  antigravity/     <- Antigravity agent orchestration variants
  local-llm/       <- Stricter variants for small local models
examples/          <- extracted examples from tutorials and docs
evals/             <- test inputs, expected outputs, regression notes
governance/        <- naming conventions, status model, review cadence
sources/           <- source registry and scraping manifest
kickoff/           <- founding brief and project history
tasks/             <- active task tracking (current phase, backlog, done)
```

## Phase awareness

Current phase: **Phase 1 — Antigravity / cloud**
Next phase: **Phase 2 — VS Code + local LLM** (when new laptop is ready)

In Phase 1:
- Focus on `skills/chrome-gemini/` and `skills/claude/` first
- Set `local_llm_safe: false` on all new skill cards until explicitly adapted
- Flag `local_llm_notes` with what would need to change for local model use

In Phase 2:
- Clone repo in VS Code + Continue.dev + Ollama
- Adapt `local_llm_template` fields in existing skill cards
- Test against real local models and update `eval_status`

## Schema rules

- All prompt cards use `schemas/prompt-card.yaml`
- All skill cards use `schemas/skill-card.yaml`
- Never modify a schema without incrementing its version and adding a changelog entry
- All artifacts must have at least one `source_refs` entry unless purely original

## Naming conventions

| Surface | Format | Example |
|---|---|---|
| Chrome Gemini | `run-<job>` | `run-extract-page-claims` |
| Claude | `critique-<job>` or `rewrite-<job>` | `critique-spec` |
| Antigravity | `author-<job>` or `review-<job>` | `review-prompt` |
| Firecrawl | `extract-<schema>` | `extract-article-evidence` |
| Local LLM | `local-<job>` | `local-summarise-page` |

## Status lifecycle

draft -> approved -> deprecated

Never delete. Mark deprecated first.

## When asked to create a new skill or prompt

1. Check `tasks/backlog.md` for an existing task
2. Check `sources/registry.md` for relevant source material
3. Use the canonical schema from `schemas/`
4. Set status: draft
5. Add to `tasks/in-progress.md`
6. When tested and reviewed, move to `tasks/done.md` and set status: approved

## Preferred working style

- Synthesise, classify, normalise, structure
- Flag duplication, ambiguity, and weak sourcing
- Prefer concise structured artifacts over long essays
- Proactively flag issues, gaps, and opportunities
- Use XML tags in Antigravity prompts (no native system instructions there)
