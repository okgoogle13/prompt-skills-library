# Chrome Gemini adapters

Place frontmatter-free, condensed Gemini in Chrome prompt adaptations here.

Use the naming convention:

```text
skills/adapters/chrome-gemini/<skill-name>.md
```

These files are intended for direct use in Gemini in Chrome and should not contain YAML frontmatter.

When `scripts/build_skills.py` builds `dist/chrome-gemini/<skill-name>.txt` for a skill targeting `chrome-gemini`, it composes the frontmatter-free canonical `SKILL.md` body followed by `skills/adapters/chrome-gemini/<skill-name>.md` (when present) and fails validation if the adapter contains YAML frontmatter.
