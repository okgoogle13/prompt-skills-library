# Build notes

- Consolidated the supplied `prompt-router` and `migrate-prompt` materials into one skill, now named `prompt-router`; `migrate-prompt` is retired and its job is route **adapt**.
- Kept the model registry and all 85 model guides; integrated model adaptation as a route rather than a separate skill.
- Kept shared prompt patterns, evaluation cases, trigger evaluations, manual tests and fixture prompts.
- Removed macOS ZIP metadata and local absolute paths from evaluation prompts.
- Added platform profiles for the user's reported ChatGPT Go + Codex CLI model picker and Perplexity Pro GPT-6.1 Sol access.
- Added platform-specific regression tests.
- Added Codex CLI surface notes to four OpenAI model guides; API details remain labelled separately.
- The model guides were not comprehensively fact-checked against live vendor documentation during packaging. Their individual `last_verified` dates remain authoritative for freshness warnings.
- Added context/token optimisation guidance: classify essential/useful/removable context, remove duplication, preserve provenance and uncertainty, and distinguish measured token savings from estimates.
- Updated the skill description, optimisation workflow, README and evaluation suite; added context-bloat regression fixture and manual tests.
- `last_verified` means last written, not independently fact-checked.
- Added migrate/port/convert routing, clarify-on-host-only adapt targets, a bare-`spark` clarification, the `(unverified)` convention and a compact adapt checklist.
- Intentional change A: removed the `spark` alias from `muse-spark-1.3` (guide frontmatter and registry row); added `scripts/build_registry.py` and `references/hosts.json`.
- Intentional change B (generator correction, separate from A): regenerating the registry from the guides corrected 3 stale rows. `gpt-5.6-luna`, `gpt-5.6-terra` and `gpt-6-luna` carry `last_verified: 2026-11-13` in their guide frontmatter (unchanged from the shipped package), but the shipped registry still said 2026-10-13. The guide is authoritative, so the registry now shows 2026-11-13. These dates were not reverted to shrink the diff.
- Consolidated workstreams (2026-11-14): `/Users/okgoogle13/Projects/prompt-skills-library/skills/claude/prompt-router/` is the canonical source of truth; `~/.claude/skills/prompt-router/` is a derived install copy synced from it via `rsync -a --delete`. Restored Phase 3–4 placeholder/security hardening (prose-only unexpanded `ARGUMENTS`/`CLAUDE_EFFORT` handling, strict no-`Bash`/no-`plugins/` bans, vendor-prefix alias retry, deterministic host-only → `review (0 guides)` rule) and applied F2 (`Self-check:` line + no garbled transitional phrasing) to **adapt**.
