# Scoping Interview Template

Use this template before G0 for any product, research, property, tax, renovation, or workflow decision.

## Entry command

Choose one:

- `/interview-me` — new decision
- `/grill-me` — unclear assumptions, risks, or scope
- `/boost-idea` — rough idea or open-ended objective
- `/refine` — existing prompt, brief, plan, or research question

## Interview rules

- Do not research.
- Do not recommend.
- Do not enter solution mode.
- Do not begin G0 until the user approves the proposed next gate.
- Ask one cluster of questions at a time.
- Do not ask questions already answered.
- Do not ask broad questions when targeted questions will materially improve the brief.
- Separate facts, inferences, assumptions, and unknowns.
- Correct risky assumptions early.
- Identify conflicts, dependencies, and scope-creep risks.

## Interview sequence

1. Problem and desired outcome
2. Constraints and non-negotiables
3. Budget, timing, and reversibility
4. Existing environment and compatibility
5. Safety, household, and cat-related constraints
6. Evidence and validation requirements
7. Decision criteria and priority weights
8. Scope boundaries and exclusions

## Output template

```md
# Targeted Fact Extraction and Preliminary Answers

## Source material reviewed
- [List supplied notes, documents, messages, links, and attachments]

## Facts explicitly stated
| ID | Fact | Source | Confidence | Notes |
|---|---|---|---|---|
| F-001 |  |  | High / Medium / Low |  |

## Direct inferences
| ID | Inference | Basis | Confidence | Verification needed |
|---|---|---|---|---|
| I-001 |  |  | High / Medium / Low |  |

## Assumptions stated by user
| ID | Assumption | Status | Correction / verification needed |
|---|---|---|---|
| A-001 |  | Confirmed / Unverified / Likely incorrect |  |

## Preliminary answers
| ID | Research question | Preliminary answer | Basis | Confidence | What would change it |
|---|---|---|---|---|---|
| PA-001 |  |  |  | High / Medium / Low |  |

## Questions that cannot yet be answered
| ID | Question | Why it cannot be answered | Required input / evidence | Gate |
|---|---|---|---|---|
| Q-001 |  |  |  | G0 / G1 / G2 / G3 |

## Contradictions and risks
| ID | Contradiction or risk | Impact | Resolution path |
|---|---|---|---|
| R-001 |  |  |  |

## Immediate clarifying questions
1. [Highest-leverage question]
2. [Highest-leverage question]
3. [Highest-leverage question]

## Proposed next gate
- [G0 / G1 / G2]
- [Why this is the next gate]
- [What must be supplied or approved before it begins]
```
