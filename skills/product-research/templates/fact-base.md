# Fact Base Template

Use this template at G-1 to separate known facts from assumptions, inferences, contradictions, and unknowns.

```md
# Fact Base

## Task
[Product, research programme, or decision]

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

## Assumptions
| ID | Assumption | Status | Correction / verification needed |
|---|---|---|---|
| A-001 |  | Confirmed / Unverified / Likely incorrect |  |

## Contradictions
| ID | Contradiction | Sources or statements involved | Impact | Resolution path |
|---|---|---|---|---|
| C-001 |  |  |  |  |

## Unknowns
| ID | Unknown | Why it matters | Required input / evidence | Gate |
|---|---|---|---|---|
| U-001 |  |  |  | G0 / G1 / G2 / G3 |

## Risks
| ID | Risk | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|
| R-001 |  |  |  |  | Open |

## Preliminary answers
| ID | Research question | Preliminary answer | Basis | Confidence | What would change it |
|---|---|---|---|---|---|
| PA-001 |  |  |  | High / Medium / Low |  |

## Questions that cannot yet be answered
| ID | Question | Why it cannot be answered | Required input / evidence | Gate |
|---|---|---|---|---|
| Q-001 |  |  |  | G0 / G1 / G2 / G3 |
```

## Rules

- Do not present an inference as a fact.
- Do not present an assumption as verified.
- Do not silently resolve a contradiction.
- Do not fill an unknown with a plausible guess.
- Do not answer a question that requires evidence not yet supplied.
- Label every preliminary answer with its basis, confidence, and change condition.
