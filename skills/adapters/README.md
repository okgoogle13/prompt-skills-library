# Skill adapters

Adapters contain deliberate, platform-specific variations of canonical skills.

They must not become independent copies of a skill’s core workflow.

## Layout

```text
skills/adapters/
├── antigravity/
├── chrome-gemini/
├── claude/
└── local-llm/
```

## File convention

Use:

```text
skills/adapters/<platform>/<skill-name>.md
```

## Required content

Each adapter file should state:

- The canonical skill it adapts
- What differs on this platform
- Required constraints or prompt format
- Known limitations
- Validation or acceptance checks

## Legacy folders

The original platform folders remain temporarily for migration:

- `skills/antigravity/`
- `skills/chrome-gemini/`
- `skills/claude/`
- `skills/local-llm/`

New adapter content should be placed here, not in the legacy folders.
