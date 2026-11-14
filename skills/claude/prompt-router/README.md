# prompt-router skill

A portable, modular skill for writing, optimising, adapting and reviewing LLM prompts and context. It reduces prompt, context and token bloat while preserving essential meaning and task requirements.

## Package layout

- `SKILL.md` — route selection, intake, trust boundary, reference loading and output contracts.
- `references/patterns.md` — shared prompt-writing, optimisation, coding-task and review rules.
- `references/model-registry.md` — exact model IDs, aliases, vendor/family, verification dates and legacy successors.
- `references/model-guides/` — 85 model-specific guides from the supplied archive.
- `references/platform-guides/` — provider/client/plan notes kept separate from model behavior.
- `evals/` — evaluation cases, trigger tests, manual tests and fixture prompts.
- `CREDITS.md` — provenance and licence notices.

## Core routes

- **Write** — turn a brief, sketch or notes into a complete prompt.
- **Optimise** — materially improve prompts and context; remove redundancy and token/context bloat while preserving the task contract.
- **Adapt** — adapt, migrate, port or convert a prompt to or between models. `prompt-router` handles adapt/migrate/port/convert; the separate `migrate-prompt` skill is retired.
- **Review** — identify material weaknesses without rewriting.
- **Clarify** — ask one focused question when a required route or model cannot be resolved.

## Portability

The package uses relative references and does not require a separate migration skill, vendor-specific absolute paths, a plugin cache, a shell, or a named file-reading tool. A host must still support loading a skill and reading its packaged reference files. If it cannot, the skill must say so rather than pretending a guide was consulted.

Keep the directory structure intact when installing. Do not copy only `SKILL.md`.

## Platform profiles

- `references/platform-guides/codex-cli-chatgpt-go.md` records this user's reported selectable Codex CLI models under ChatGPT Go.
- `references/platform-guides/perplexity-pro.md` records this user's reported GPT-6.1 Sol access through Perplexity Pro.

These are account-specific observations, not universal plan guarantees. Re-check the provider's live model picker when availability matters.

## Maintenance

`last_verified` means **last written**, not independently fact-checked against vendor documentation. Model-guide facts are only as current as that date. Update a guide and its frontmatter together, then regenerate `references/model-registry.md` with `python3 -I scripts/build_registry.py --write` (check: `--check`; tests: `--self-test`; stdlib only). It fails on duplicate aliases and on aliases that match `references/hosts.json` reserved names, and reports missing and stale (>180 days) guides. Platform access notes should be updated separately from model capability notes.

## Conventions

- `(unverified)` in a guide marks an unverified claim: flag it, never present it as established fact.
- Bare `spark` is not an alias. It asks whether Gemini Spark (host, no guide) or `muse-spark-1.3` is meant.

## Migration note

The command stays `prompt-router`. This package replaces the earlier `prompt-router` and retires `migrate-prompt`; adaptation is route **adapt**. The guides are the same 85 as before (muse-spark-1.3 lost the `spark` alias).

Canonical source of truth: `skills/claude/prompt-router/` in `prompt-skills-library`. Install or update `~/.claude/skills/prompt-router/` as a one-way derived copy via `rsync -a --delete`. Check registry integrity with `.venv/bin/python -I scripts/build_registry.py --check`.
