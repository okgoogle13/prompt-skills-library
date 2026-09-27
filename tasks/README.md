# Task Tracking

Use this directory to track project work with the lightweight method in [`../governance/task-planning-methodology.md`](../governance/task-planning-methodology.md).

## Files

- `backlog.md`: planned work not yet started.
- `in-progress.md`: the current active work.
- `done.md`: completed work with evidence.

## Phase 1 outcome

**Outcome:** A working, evidence-based skill library with at least 5 approved skill cards across
`chrome-gemini`, `claude`, and `antigravity` surfaces — all traceable to ingested foundation sources.

**Why:** Without a normalized knowledge foundation and validated skill cards, all downstream
prompt work is untraceable and unreproducible.

**In scope:** Ingestion of 6 foundation sources, creation of first skill cards, eval baseline.

**Out of scope:** VS Code setup, local LLM testing, `.prompt.md` files (all Phase 2).

**Done when:**
- [ ] All 6 foundation sources normalized in `knowledge/` with `status: normalized`
- [ ] At least 5 approved skill cards exist with `source_refs` and `eval_status` filled
- [ ] At least 1 eval test case per approved skill card in `evals/`
- [ ] `sources/registry.md` statuses reflect current ingestion state

## Milestones

- [ ] M1: Knowledge foundation — all 6 foundation sources normalized in `knowledge/`
- [ ] M2: First skill cards — at least 3 approved skill cards (one per surface: chrome-gemini, claude, antigravity)
- [ ] M3: Eval baseline — at least 1 eval test case per approved skill card



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
