# Task Planning Methodology

## Purpose

Make the next piece of work obvious, keep scope visible, and make progress verifiable.

Use this for work that spans more than one focused change. For small fixes, use a normal task entry.

## Start with the outcome

Before implementation, write:

- Outcome: what will be true when this is complete?
- Why: why does it matter?
- In scope: what is included?
- Out of scope: what is explicitly excluded?
- Done when: which observable checks prove completion?

If the outcome or “done when” statement is unclear, do not start implementation.

## Break work into milestones

A milestone is a meaningful result that can be demonstrated independently.

Use:

```md
- [ ] M1: <observable result>
- [ ] M2: <observable result>
- [ ] M3: <observable result>
```

Do not create milestones for activities such as “research,” “think,” or “work on prompts.” Describe the result of the activity instead.

## Create small tasks

Each task should produce one reviewable result:

```md
## T-<number>: <verb-led title>

- Status: ready | in-progress | blocked | review | done
- Milestone: M<number>
- Depends on: <task ID or none>

### Outcome

<One observable result.>

### Done when

- [ ] <specific check>
- [ ] <specific check>

### Evidence

<file, test, source, diff, or decision record>
```

If a task has several unrelated outcomes or cannot be checked with a short list of criteria, split it.

## Work in priority order

Choose the next task using this order:

1. Unblock other work.
2. Reduce the highest-risk uncertainty.
3. Produce the smallest useful demonstrable result.
4. Improve quality or documentation.

Do not start low-risk polishing while a high-risk assumption remains untested.

## Track progress

At the end of each work session, update the task with:

```md
### Update: YYYY-MM-DD

- Done: <observable result>
- Evidence: <path, test, source, or commit>
- Remaining: <unfinished work>
- Blocked by: <blocker or none>
- Next: <one next action>
```

The `Next` line should identify one action, not a general intention.

## Control scope

When new work appears, classify it as:

- Required: needed to achieve the current outcome.
- Useful: valuable but can wait.
- Unrelated: create a separate task.

For required scope changes, update the outcome, milestones, and affected tasks before continuing. Do not silently expand a task.

## Definition of done

A task is done only when:

- Its stated outcome exists.
- Its checks are complete.
- Evidence is recorded.
- The diff contains no accidental extra scope.
- Remaining uncertainty is noted.

A milestone is done when its tasks are done and the milestone result can be demonstrated.

## Minimal review

Before starting:

- Is the outcome clear?
- Is the scope bounded?
- What is the riskiest assumption?
- What is the next smallest useful result?

Before finishing:

- What changed?
- What proves it works?
- What remains uncertain?
- Did the scope expand?
