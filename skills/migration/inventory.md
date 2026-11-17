# Skills migration inventory

This inventory is the working record for migrating the legacy platform-first skill folders into the canonical structure.

## Status

- [ ] Audit `skills/antigravity/`
- [ ] Audit `skills/chrome-gemini/`
- [ ] Audit `skills/claude/`
- [ ] Audit `skills/local-llm/`
- [ ] Identify duplicate or overlapping workflows
- [ ] Identify one-off prompts that should not become skills
- [ ] Create canonical `skills/<skill-name>/SKILL.md` files
- [ ] Create adapter files under `skills/adapters/<platform>/`
- [ ] Link evidence, schemas, governance status, and evaluations
- [ ] Generate and validate `dist/` exports

## Inventory template

| Legacy path | Proposed canonical skill | Adapter paths | Overlap / conflict | Disposition | Notes |
|---|---|---|---|---|---|
| `skills/chrome-gemini/example.md` | `skills/example-skill/SKILL.md` | `skills/adapters/chrome-gemini/example-skill.md` | None identified | Migrate | Complete after audit |

## Decision rules

Promote an artifact to a canonical skill only when it has:

- A repeatable workflow
- A clear trigger and outcome
- Reusable instructions or references
- A defined output or acceptance criterion

Keep one-off prompts as prompt cards or examples rather than forcing them into `skills/`.
