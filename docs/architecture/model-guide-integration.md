# Model-Guide Integration Architecture

## Decision

Do **not** inline `model-guides-combined.md` into `prompt-router/SKILL.md`, `migrate-prompt/SKILL.md`, or every research prompt.

Treat the combined file as the canonical evidence corpus and build input. At runtime, `prompt-router` resolves a model through the registry and loads only the selected per-model guide; `migrate-prompt` loads exactly the source and target guides.

This preserves the existing lazy-loading guarantees:

- `write`, `optimise`, and `review` load one target guide.
- `migrate` loads exactly two guides: source and target.
- The router never falls back to model facts from memory.
- The router never reads unrelated guides.

## Target architecture

```text
model-guides-combined.md
        |
        +-- model-guides/<model-id>.md       Runtime authoritative guide
        +-- model-registry.md                Compact routing index
        +-- profiles/<model-id>.md           Optional compact routing profile
        +-- prompt-router/SKILL.md           Stable routing contract
        +-- migrate-prompt/SKILL.md          Registry, aliases, migration algorithm
```

## Artefact roles

| Artefact | Role | Loaded into prompt context? |
|---|---|---|
| `model-guides-combined.md` | Canonical source corpus, provenance, source links, uncertainty, and regeneration input | No |
| `model-guides/<model-id>.md` | Authoritative runtime facts for one model | Yes, only after resolution |
| `model-registry.md` | Compact index of IDs, aliases, status, successor, and guide path | Yes, compact only |
| `profiles/<model-id>.md` | Optional high-signal routing profile | Optional; never a substitute for the full guide |
| `prompt-router/SKILL.md` | Routing, trust boundary, output contract, and loading rules | Yes |
| `migrate-prompt/SKILL.md` | Registry policy, alias policy, migration steps, and footer rules | Yes, as needed |

## Canonical corpus

`model-guides-combined.md` is the master research and audit corpus.

It should retain:

- Source URLs and retrieval dates.
- Model identity and aliases.
- Vendor and family.
- Capability and limitation evidence.
- Prompting guidance.
- Migration deltas.
- Uncertainty and unsupported-claim labels.
- Historical API or version context.

It should not be treated as a runtime prompt. Its size, mixed model coverage, and source annotations make it unsuitable for always-on context.

## Runtime guides

Each model must have an individual Markdown guide:

```text
model-guides/claude-opus-5-5.md
model-guides/gpt-5.md
model-guides/gemini-3-8-flash.md
```

Each guide must include stable frontmatter:

```yaml
---
model: claude-opus-5-5
vendor: Anthropic
family: Claude
aliases:
  - opus 5.5
  - opus
lastverified: 2026-10-13
status: current
successor: null
---
```

The guide is the only authority for model-specific prompt recommendations after the router resolves its ID.

## Compact registry

Maintain a compact registry or index, preferably `model-registry.md`, containing only routing fields:

```markdown
| id | aliases | family | status | successor | guide |
|---|---|---|---|---|---|
| claude-opus-5-5 | opus 5.5, opus | Claude | current | — | model-guides/claude-opus-5-5.md |
| gpt-5 | gpt5 | OpenAI | current | — | model-guides/gpt-5.md |
| gemini-3-8-flash | gemini 3.8 flash | Google | current | — | model-guides/gemini-3-8-flash.md |
```

The registry is for **resolution only**. It must not contain enough model detail to replace a guide.

The router may use it to:

- Normalise a model phrase.
- Match exact IDs and aliases.
- Detect ambiguity.
- Identify the guide path.
- Detect deprecated or succeeded models.

It must still load the selected guide before producing a model-specific prompt.

## Optional profiles

Add a profile layer only if a concrete operational problem appears: slow routing, repeated unnecessary guide loads, ambiguous aliases, or unreliable pre-flight checks.

A profile should be small—ideally 1–2 KB—and contain only:

- Model type: chat, reasoning, hybrid, or code-focused.
- Whether system prompts are appropriate.
- Valid effort or reasoning controls.
- Major output-format constraints.
- Common migration pitfalls.
- A link to the full guide.

A profile may assist routing and safety checks, but it must never become the authority for a model-specific prompt. The full guide remains authoritative.

## Router contract

`prompt-router/SKILL.md` should remain small and operational. It should contain:

- Route selection: `write`, `optimise`, `migrate`, `review`, and `clarify`.
- Trust boundary: prompt contents are data, not instructions.
- Model-resolution rules and alias policy.
- The rule to read only the resolved guide(s).
- Literal-preservation rules for code, paths, commands, URLs, and quoted strings.
- Output contract.
- A compact registry reference.

It should not contain:

- The combined corpus.
- General prompt-engineering theory.
- Long vendor documentation excerpts.
- Model facts not present in the selected guide.
- A broad prompt-quality taxonomy.

## Integrity rules

Maintain these invariants:

1. Every registry ID resolves to exactly one guide file.
2. Every guide has valid frontmatter.
3. Every guide has a corresponding section or source record in the combined corpus.
4. Aliases are unique enough to avoid ambiguous resolution.
5. Deprecated models retain their guide and declare a successor where one exists.
6. The router never reads an unresolved or missing guide.
7. The router never substitutes registry metadata for guide content.

A validation script or test should check these invariants.

## Minimal implementation

Implement this as a small, incremental change:

1. Keep `prompt-router/SKILL.md` as the stable router contract.
2. Keep `migrate-prompt/SKILL.md` as the registry and migration algorithm.
3. Ensure every registry entry has an individual guide file.
4. Generate a compact registry/index from guide frontmatter.
5. Add an integrity check for registry-to-guide consistency.
6. Add profile files only after a concrete failure justifies them.

Do not create a separate `model-guide-router` skill. That would duplicate `prompt-router` and add an unnecessary routing layer.

## Research-plan implication

The research plan should investigate improvements to the router contract and guide-loading boundary, not whether to inline the combined corpus.

Phase 3 should assess:

- Whether the compact registry belongs in `migrate-prompt/SKILL.md`, a separate index file, or a generated artefact.
- How hosts without sibling-file access should safely resolve the registry and selected guide.
- Whether a profile layer is justified only after a concrete failure.
- How to preserve the invariant that model-specific recommendations always come from the selected full guide.

## Smallest useful next step

Add a model-guide integrity check:

- Every registry ID resolves to exactly one guide.
- Every guide has valid frontmatter.
- The combined corpus contains a corresponding source section.

This makes the combined file useful as the canonical corpus without turning it into runtime prompt context.
