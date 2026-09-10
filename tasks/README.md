# Tasks

Lightweight task tracking for this repo.
No external tool required — plain markdown, committed alongside the work.

## Files

- `backlog.md` — ideas and future tasks, not yet started
- `in-progress.md` — active tasks, one owner, target date
- `done.md` — completed tasks with date and outcome note

## Task format

```markdown
### [TASK-ID] Task title
- **Status:** backlog | in-progress | done
- **Phase:** 1 | 2
- **Surface:** chrome-gemini | claude | antigravity | local-llm | repo
- **Owner:** @username
- **Target:** YYYY-MM-DD
- **Source ref:** URL or registry entry
- **Notes:** brief description
```

## Task ID format

`P<phase>-<sequence>` e.g. `P1-001`
