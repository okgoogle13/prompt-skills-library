---
name: example-skill-name
description: >-
  Use when the user needs to [specific trigger or outcome]. Produces [primary
  output] using [method or constraint].
version: 0.2.0
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

## Mandatory gate sequence

Every research or decision workflow must follow this sequence. Do not skip gates or collapse them into a single response.

```text
G-2 Scoping interview
G-1 Targeted fact extraction and preliminary answering
G0 Problem definition
G1 Requirements intake and research brief
G2 Research scope
G3 Evidence
G4 Compatibility and safety
G5 Decision
G6 Implementation
```

### Gate rules

- Do not research, compare, score, or recommend until the required gates are complete.
- Do not treat assumptions as facts.
- Do not silently resolve contradictions.
- Do not begin G0 until the scoping interview and fact extraction are complete.
- Do not begin G3 until G1 and G2 are approved.
- Do not produce a purchase, transfer, or implementation recommendation before G4 is complete.
- Every recommendation must be reversible and include accepted trade-offs, risks, and a fallback plan.
- Every material claim requires a source, date, and confidence rating.
- Every unknown, contradiction, and risk must be explicitly recorded.

## Scoping interview layer

Before G0, run the scoping interview using the appropriate Antigravity slash command:

- `/interview-me` for a new product or research decision.
- `/grill-me` for unclear assumptions, risks, or scope.
- `/boost-idea` for a rough idea or open-ended objective.
- `/refine` for an existing prompt, brief, plan, or research question.

The interview must:

- Extract facts, assumptions, constraints, and unknowns.
- Correct risky assumptions.
- Identify conflicts, dependencies, and scope-creep risks.
- Ask only high-leverage questions.
- Prevent premature research or recommendations.
- Produce a fact base, assumption register, unknown register, risk register, and gate plan.
- Obtain user approval before advancing to G0.

## Workflow

1. Run the scoping interview using the appropriate slash command.
2. Extract and classify supplied material into facts, inferences, assumptions, contradictions, and unknowns.
3. Answer only questions that can be answered from the supplied material.
4. Ask only the highest-leverage clarifying questions.
5. Obtain approval for the problem definition and research brief.
6. Define the research scope, evidence standard, and validation plan.
7. Gather only the evidence required for the task.
8. Validate compatibility, safety, legal, and domain-specific requirements.
9. Produce a reversible decision or requested artifact.
10. Validate the result against the acceptance criteria.

## Method

Describe the portable, platform-neutral procedure.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Example input | Yes | Describe expected format |
| Existing facts and documents | Optional | Notes, links, screenshots, specifications, prior decisions |
| Scoping-interview answers | Yes | Must be captured before G0 |
| Priority weights | Conditional | Required before comparative scoring |

## Outputs

Describe the exact artifact, structure, and location.

## Acceptance criteria

- [ ] The scoping interview is complete before G0.
- [ ] Facts, assumptions, contradictions, and unknowns are separated.
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
