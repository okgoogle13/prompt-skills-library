# prompt-skills-library

A curated, evidence-based prompt and skills foundation.

## Mission

Adapt credible existing best practices into reusable, versioned artifacts for:
- Immediate use as **Gemini in Chrome** browser skills
- **Claude**, **Antigravity**, and agent-orchestration workflows
- Long-term **local LLM** adaptation on personal hardware

## Core principle

> Prefer adaptation over reinvention. Prefer traceability over prompt folklore. Prefer structured reusable assets over one-off chat outputs.

## Anti-reinvention policy

Before inventing a new prompt structure, workflow, taxonomy, or skill format:
1. Search for an established credible pattern first
2. Explain whether it is sufficient
3. Only create a new pattern if there is a clear gap and a documented justification

Any newly proposed structure must justify why adaptation of existing best practice is not enough.

## Repo structure

```
prompt-skills-library/
├── knowledge/
│   ├── canonical/          # Official vendor docs, normalized to markdown
│   │   └── anthropic/
│   ├── library-design/     # Schema, lifecycle, versioning, optimization rules
│   └── local-llms/         # Small-model constraints, injection-safe patterns
├── examples/               # Extracted examples from tutorials and docs
├── schemas/                # Canonical YAML schemas for prompt and skill cards
├── skills/
│   ├── chrome-gemini/      # Runtime-adapted Gemini in Chrome skill variants
│   ├── claude/             # Claude-specific prompt variants
│   ├── local-llm/          # Stricter variants for local/small models
│   └── antigravity/        # Antigravity agent orchestration variants
├── evals/                  # Test inputs, expected outputs, regression notes
├── governance/             # Naming conventions, status model, review cadence
└── sources/                # Source registry and scraping manifest
```

## Status model

Every prompt or skill card moves through: `draft` → `approved` → `deprecated`

Never delete a working artifact without first marking it `deprecated`.

## Source priority order

1. Official vendor documentation and technical references
2. High-quality practitioner resources that are explicit, structured, and testable
3. Supplemental examples, tutorials, and pattern libraries
4. Own experimental prompts only after reviewing existing evidence

## Quick start

1. Read [`governance/conventions.md`](governance/conventions.md) before adding anything
2. Review the canonical schema at [`schemas/prompt-card.yaml`](schemas/prompt-card.yaml) and [`schemas/skill-card.yaml`](schemas/skill-card.yaml)
3. Check the source registry at [`sources/registry.md`](sources/registry.md)
4. Add new prompts to `skills/` using the canonical schema
5. Add new knowledge artifacts to `knowledge/` with a source ref and retrieval date
