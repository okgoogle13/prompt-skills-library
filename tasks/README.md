# Task Tracking

Use this directory to track project work with the lightweight method in [`../governance/task-planning-methodology.md`](../governance/task-planning-methodology.md).

## Files

- `backlog.md`: planned work not yet started.
- `in-progress.md`: the current active work.
- `done.md`: completed work with evidence.

## Task rule

Every non-trivial task should state:

- Outcome.
- Status.
- Dependencies.
- Completion checks.
- Evidence.
- Next action.

Keep tasks small and reviewable. Do not mark work done merely because files changed; record what proves the outcome is complete.

## Project sequence

1. Establish and validate the Claude global configuration.
2. Run skill-creator on existing custom skills before trusting or expanding them.
3. Build the prompt-skill foundation.
4. Configure the lean Perplexity Project description and instructions.
5. Add cross-runtime adapters only where evaluation justifies them.

## Status workflow

```text
backlog → in-progress → review → done
                  ↓
                blocked
```

Use `done.md` only for work with recorded evidence. Keep scope changes visible in the relevant task or commit.
