# Skills

This directory contains the repository’s canonical, platform-neutral Agent Skills.

## Canonical layout

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
```

## Source of truth

`skills/<skill-name>/SKILL.md` is the canonical definition for each reusable skill.

It should contain:

- A portable task workflow
- Inputs, outputs, and acceptance criteria
- Evidence and source references
- Reusable references and assets
- Only genuinely reusable scripts

Platform-specific behaviour belongs in `skills/adapters/<platform>/`. Do not duplicate the core workflow there.

## Platform adapters

| Adapter | Purpose |
|---|---|
| `chrome-gemini` | Condensed, frontmatter-free prompts for Gemini in Chrome |
| `claude` | Claude-specific execution or tool-use guidance |
| `antigravity` | Antigravity orchestration and workflow guidance |
| `local-llm` | Constraints and fallbacks for local or smaller models |

## Migration status

The legacy platform-first folders remain in place during migration:

- `skills/antigravity/`
- `skills/chrome-gemini/`
- `skills/claude/`
- `skills/local-llm/`

They are now **legacy adaptation inputs**, not the canonical source of truth.

See `skills/migration/inventory.md` and `docs/canonical-skills-migration.md` before creating or moving skills.
