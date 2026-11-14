# In progress

_No tasks currently in progress. Pick from backlog and move here when started._

## Template

## [TASK-ID]: <verb-led title>

- Status: in-progress
- Milestone: M<number>
- Depends on: <task ID or none>

### Outcome

<One observable result.>

### Done when

- [ ] <specific check — file path or command output level>
- [ ] <specific check>

### Evidence

<file, test, source, diff, or decision record — filled on completion>

### Update: YYYY-MM-DD

- Done: <observable result>
- Evidence: <path, test, source, or commit>
- Remaining: <unfinished work>
- Blocked by: <blocker or none>
- Next: <one next action — not a general intention>

### PR-001 Translate prompt-router model guides to English
- **Status:** in-progress
- **Phase:** 1
- **Surface:** claude
- **Done when:**
  - [ ] All 85 guides in `skills/claude/prompt-router/references/model-guides/` are English, frontmatter unchanged
  - [ ] `(unbelegt)` replaced by `(unverified)` in SKILL.md, patterns.md, README.md, evals
  - [ ] `scripts/build_registry.py` output unchanged; `scripts/validate_cards.py` passes
  - [ ] `~/.claude/skills/prompt-router/` re-synced and identical
