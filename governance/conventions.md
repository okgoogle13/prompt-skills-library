# Governance & conventions

## Naming conventions

| Layer | Format | Example |
|---|---|---|
| Prompt cards | `kebab-case` slug | `summarise-meeting-actions` |
| Skill cards | `verb-noun` slug | `extract-page-claims` |
| Chrome Gemini skills | `run-<job>` | `run-tab-compare` |
| Antigravity workflows | `author-<job>` or `review-<job>` | `author-brief`, `review-prompt` |
| Firecrawl recipes | `extract-<schema>` | `extract-article-evidence` |
| Claude prompts | `critique-<job>` or `rewrite-<job>` | `critique-spec`, `rewrite-brief` |

This naming instantly communicates whether something is for live browser execution, authoring/orchestration, structured extraction, or critique.

## Status lifecycle

```
draft → approved → deprecated
```

- **draft** — written but not yet tested or reviewed
- **approved** — tested with at least 3 varied inputs, reviewed by owner, consistent output
- **deprecated** — replaced or retired; kept for reference but no longer in active use

Never delete an approved artifact. Mark it `deprecated` first.

## Versioning

- Use semantic versioning: `v<major>.<minor>`
- Increment minor for non-breaking edits (wording, formatting, model notes)
- Increment major for structural changes (new fields, changed output contract, new inputs)
- Always add a one-line changelog entry with date
- Keep prior versions accessible; do not overwrite

## Source traceability

Every artifact must include at least one `source_refs` entry unless it is purely original.

When adapting from a credible resource:
- Record the exact URL
- Record the retrieval date
- Note what was adapted vs. invented

## Review cadence

- **Monthly:** review usage, retire low-use artifacts, promote improved ones
- Prompt/skill cards with no eval result after 60 days should be flagged for testing or deprecation
- Model-specific notes should be reviewed when a primary model version changes

## Quality gate before approval

1. Tested with at least 3 varied real inputs
2. Output format matches `output_contract`
3. No reliance on model-specific behavior that may change
4. Source references present
5. `when_not_to_use` field is filled — not left blank

## Anti-duplication rule

Before creating a new artifact:
1. Check existing prompt cards and skill cards for overlap
2. Check the source registry for an existing best-practice pattern
3. If overlap exists, adapt the existing artifact rather than creating a parallel one
4. If a new artifact is created, note why adaptation was insufficient
