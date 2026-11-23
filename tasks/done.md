# Done

### P0-001 Create repo and scaffold structure
- **Status:** done
- **Phase:** 0
- **Surface:** repo
- **Completed:** 2026-09-10
- **Outcome:** Repo created at https://github.com/okgoogle13/prompt-skills-library with schemas, governance, ingestion workflow, source registry, kickoff prompt, and all placeholder folders

### P0-002 Add CLAUDE.md, phase plan, and task tracking
- **Status:** done
- **Phase:** 0
- **Surface:** repo
- **Completed:** 2026-09-10
- **Outcome:** CLAUDE.md added for Claude Code context, tasks/ folder scaffolded with backlog pre-populated for Phase 1 and Phase 2

### P1-PR-LEAN Implement lean prompt-router spec (Phase 1)
- **Status:** done
- **Phase:** 1
- **Surface:** claude
- **Completed:** 2026-11-23
- **Spec:** `docs/ideas/prompt-router-spec.md`
- **Outcome:** `SKILL.md` 187→66 L; `patterns.md` 254→59 L (write/optimise only); lazy `references/review.md` (21 L) and `references/adapt.md` (29 L); two-tier registry, 20 active (26 L) / 69 archive (75 L), driven by guide frontmatter `tier: active` + `profile:` and `hosts.json` `active_count`/`profile_words`.
- **Evidence:**
  - `.venv/bin/python -I skills/claude/prompt-router/scripts/build_registry.py --check` → `active=20 archive=69`, "registry up to date", exit 0; `--self-test` → ALL PASS (19 tests).
  - Safeguard anchors in `SKILL.md`: S1 L12, L19-20, L23, L62; S2 L13, L63; S3 L14, L20, L37-40, L65; S4 L15, L62; S5 L16, L57, L64.
  - `evals/evals.json` parses (45 cases; 6 updated, 5 added); `scripts/validate_cards.py` passes; `diff -rq` against `~/.claude/skills/prompt-router/` clean.
- **Open (out of scope):** live-model eval runs (spec §10: Short-tier fidelity, ≥90% shortlist hit rate). Static `write` load is ~5.7k tok (22,850 chars / 4), ~57% cut; accepted as Phase 1 result, spec §8 updated.


### PR-001 Translate prompt-router model guides to English
- **Status:** done
- **Phase:** 1
- **Surface:** claude
- **Completed:** 2026-11-23 (translation landed 2026-11-14 in `a4b1cc7` merge of `prompt-router-consolidated` and `8d3f627`)
- **Outcome:** All guides in `skills/claude/prompt-router/references/model-guides/` are English (85 at translation time; 4 added since were written in English, 89 total). `(unbelegt)` → `(unverified)` and `Guide-Stand` → `Guide status` across skill text and evals.
- **Evidence:**
  - Frontmatter unchanged against the pre-translation commit (checked at translation time); `tier:`/`profile:` added later by P1-PR-LEAN.
  - 2026-11-23: no umlauts, `„`, `unbelegt` or common German words (`und|nicht|wird|sollte`) in any of the 89 guides.
  - `build_registry.py --check` → `guides=89 registry_rows=89 active=20 archive=69`, "registry up to date", exit 0; `--self-test` → ALL PASS; `scripts/validate_cards.py` exit 0; `diff -rq` against `~/.claude/skills/prompt-router/` clean.
- **Open:** `claude-opus-4-6.md` L14 ("No `thinking.type` is rejected with 400") keeps an ambiguous German original; verify against Anthropic docs. Spelling convention mixed (AU/UK vs US) across batches.
