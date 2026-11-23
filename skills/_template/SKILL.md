---
name: example-skill-name
description: >-
  Use when the user needs to [specific trigger or outcome]. Produces [primary
  output] using [method or constraint].
version: 0.1.0
status: draft
owner: Nish Dougall
source_of_truth: skills/example-skill-name/SKILL.md
platforms:
  - chrome-gemini
  - claude
  - antigravity
  - local-llm
evidence:
  - path: research/
  - path: sources/
---

# Example Skill Name

## Purpose

State the outcome this skill produces and the user situation that should trigger it.

## When to use

Use this skill when:

- [Trigger condition]
- [Required context]
- [Expected output type]

## Workflow

1. Clarify the objective, constraints, and success criteria.
2. Gather only the evidence required for the task.
3. Apply the canonical method below.
4. Produce the requested artifact.
5. Validate the result against the acceptance criteria.

## Method

Describe the portable, platform-neutral procedure.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Example input | Yes | Describe expected format |

## Outputs

Describe the exact artifact, structure, and location.

## Acceptance criteria

- [ ] The output meets the stated objective.
- [ ] Claims are supported by cited evidence.
- [ ] Platform-specific constraints are handled by adapters.
- [ ] The result is reproducible from the supplied inputs.

## References

Place focused, reusable reference material in `references/`.

## Adapter notes

Platform-specific instructions belong in:

```text
skills/adapters/<platform>/<skill-name>.md
```
