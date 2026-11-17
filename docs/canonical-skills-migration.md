# Canonical skills migration

## Objective

Establish a single canonical source of truth for reusable skills while preserving explicit platform adaptations for Gemini in Chrome, Claude, Antigravity, and local LLM workflows.

## Target architecture

```text
skills/
├── <skill-name>/
│   ├── SKILL.md
│   ├── references/
│   ├── assets/
│   └── scripts/
├── adapters/
│   ├── antigravity/
│   ├── chrome-gemini/
│   ├── claude/
│   └── local-llm/
└── migration/

scripts/
└── build_skills.py

 dist/
├── skills/
├── chrome-gemini/
├── bundles/
└── index.json
```

## Principles

1. `skills/<skill-name>/SKILL.md` is canonical.
2. Platform differences are explicit adapters, not duplicate skills.
3. Evidence, research, schemas, governance, and evaluations remain separate from deployable skill code.
4. Generated exports belong in `dist/` and must not be manually maintained.
5. Every migration decision is recorded in `skills/migration/inventory.md`.

## Migration sequence

1. Audit every legacy platform folder.
2. Identify canonical skills, overlaps, duplicates, and one-off prompts.
3. Create canonical `SKILL.md` files from shared workflows.
4. Move platform-specific variations into adapters.
5. Link evidence, governance status, schemas, and evaluations.
6. Run the build script and validate generated exports.
7. Deprecate legacy folders only after the migration inventory is complete.

## Build outputs

| Output | Purpose |
|---|---|
| `dist/skills/<skill-name>/` | Portable skill bundle |
| `dist/bundles/<skill-name>.zip` | Upload-ready archive where applicable |
| `dist/chrome-gemini/<skill-name>.txt` | Frontmatter-free prompt for Gemini in Chrome |
| `dist/index.json` | Machine-readable skill index |

## Validation

The build script should validate:

- `SKILL.md` exists for every canonical skill
- `name` matches its parent folder
- `description` is present and under 1,024 characters
- Required metadata fields are valid
- Adapter references resolve to existing files
- Generated `dist/` artifacts are reproducible
