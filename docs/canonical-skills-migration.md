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
| `dist/bundles/<skill-name>.zip` | Reproducible upload-ready archive where applicable |
| `dist/chrome-gemini/<skill-name>.txt` | Frontmatter-free prompt for Gemini in Chrome (canonical body composed with `skills/adapters/chrome-gemini/<skill-name>.md` when present, emitted only when `chrome-gemini` is listed in `platforms`) |
| `dist/index.json` | Machine-readable skill index |

## Validation

The build script validates:

- `SKILL.md` exists for every canonical skill directory
- YAML frontmatter parses cleanly and includes all required metadata (`name`, `description`, `version`, `status`, `owner`, `source_of_truth`, `platforms`, `evidence`)
- `name` is valid kebab-case (`<= 64` chars) and matches its parent folder
- `description` is present (including folded/multiline YAML values) and `<= 1,024` characters
- `version` is semantic (`vX.Y` / `X.Y.Z`), `status` is `draft | approved | deprecated`, `source_of_truth` points to `skills/<skill-name>/SKILL.md`, `platforms` is a non-empty subset of supported platforms, and `evidence` paths exist
- Adapter references (`adapters` metadata or `skills/adapters/<platform>/<skill-name>.md`) resolve to existing files for declared platforms, and Chrome Gemini adapters contain no YAML frontmatter
- `--dist-root` never overlaps repository source directories or deletes unexpected files (preserving `dist/.gitkeep`)
- Generated `dist/` artifacts are reproducible
