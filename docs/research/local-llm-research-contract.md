# Local LLM Research Contract

Status: active
Last reviewed: 2026-11-19
Scope: shared output and coordination rules for ChatGPT Deep Research, Gemini Deep Research, and Perplexity PWM/MCP research tasks.

## Purpose

This contract ensures that separately executed research tasks produce compatible, decision-ready outputs. It prevents duplicate research, unsupported claims, and conflicting recommendations.

## Canonical inputs

Every research agent must treat these as the source of truth:

- `docs/research/local-llm-open-questions.md`
- `docs/research/local-llm-recommendations.md`
- `docs/research/local-llm-research-plan.md`

## Task boundary rules

- Address only the questions assigned to the specified research task.
- Do not produce a general “best local LLM” report.
- Do not make final adoption decisions outside the task boundary.
- Do not duplicate research owned by another task.
- Do not overwrite another task’s assigned questions.
- Do not mark a question `resolved` solely from web research if it requires local validation.
- Do not invent specifications, benchmark results, VRAM requirements, licences, context windows, compatibility claims, or pricing.
- If evidence is insufficient, leave the question open and identify the missing evidence.
- If a recommendation depends on untested local behaviour, mark it `provisional`.
- If a task boundary is exceeded, place the item in `Handoff notes`, not in the recommendation.

## Evidence rules

Classify every material claim as one of:

- `verified fact`
- `inferred estimate`
- `community claim`
- `unknown / requires local testing`

Prioritise primary sources:

- Official model cards
- Vendor documentation
- GitHub repositories and release notes
- Runtime documentation
- Credible benchmarks
- High-quality independent evaluations

Use community sources only as supporting evidence, not as sole authority. Cross-check important claims across at least two independent sources where possible. Explicitly identify conflicts between sources.

## Required prompt insert

Paste this block into every research prompt:

```text
RESEARCH CONTRACT

You are researching one narrowly scoped part of a local-LLM decision process.

Do not produce a general “best local LLM” report.
Do not make final adoption decisions outside your assigned questions.
Do not duplicate research owned by another task.
Do not invent specifications, benchmark results, VRAM requirements, licences,
context windows, compatibility claims, or pricing.

Canonical inputs:
- docs/research/local-llm-open-questions.md
- docs/research/local-llm-recommendations.md
- docs/research/local-llm-research-plan.md

Your assigned questions:
[INSERT OQ IDs]

Your task boundary:
[INSERT TASK NAME AND SCOPE]

Required output:
Return a structured research dossier using the exact section order below.

1. Executive recommendation
2. Questions addressed
3. Findings
4. Options considered
5. Recommended option
6. Trade-offs
7. Evidence assessment
8. Confidence and uncertainty
9. Proposed open-question updates
10. Proposed recommendation updates
11. Local validation required
12. Handoff notes for downstream tasks
13. Sources
14. Start-here checklist

For every claim, classify it as:
- Verified fact
- Inferred estimate
- Community claim
- Unknown / requires local testing

For every recommendation, provide:
- status: provisional | accepted | superseded | rejected | parked
- confidence: high | medium | low
- evidence quality: high | medium | low
- date_researched
- last_verified
- sources
- open_questions
- local_validation_required

Use the existing status vocabularies from the canonical registers.
Do not create new status values.

End with a machine-readable JSON block:

{
  "task_id": "",
  "questions_addressed": [],
  "questions_still_open": [],
  "recommendations_proposed": [],
  "recommendations_updated": [],
  "dependencies_satisfied": [],
  "dependencies_blocking": [],
  "local_tests_required": [],
  "confidence": "high | medium | low",
  "sources": []
}
```

## Required output schema

Every research dossier must use this structure:

```markdown
# Research Dossier: [TASK NAME]

## Executive recommendation

[One-paragraph recommendation, including confidence and main trade-off.]

## Questions addressed

| Question ID | Question | Status before | Status proposed | Rationale |
|---|---|---|---|---|
| OQ-001 | ... | open | in_progress / resolved | ... |

## Findings

[Fact-based findings, separated from interpretation.]

## Options considered

| Option | Strengths | Limitations | Evidence quality | Fit to constraints | Recommendation |
|---|---|---|---|---|---|

## Recommended option

[Exact recommendation, including model/runtime/workflow IDs where relevant.]

## Trade-offs

| Dimension | Selected option | Alternative | Why selected |
|---|---|---|---|
| Quality |  |  |  |
| Speed |  |  |  |
| VRAM / memory |  |  |  |
| Context |  |  |  |
| Privacy |  |  |  |
| Setup effort |  |  |  |
| Maintenance |  |  |  |

## Evidence assessment

| Claim | Classification | Source | Confidence | Verification needed |
|---|---|---|---|---|

## Confidence and uncertainty

[State what is known, what is estimated, and what cannot be resolved without local testing.]

## Proposed open-question updates

```yaml
- id: OQ-001
  proposed_status: in_progress
  findings_summary: ""
  evidence_added: []
  remaining_gaps: []
  next_action: ""
```

## Proposed recommendation updates

```yaml
- id: REC-001
  proposed_status: provisional
  recommendation: ""
  rationale: ""
  evidence: []
  constraints: []
  open_questions: []
```

## Local validation required

| Test | Purpose | Pass threshold | Data / prompt set | Owner |
|---|---|---|---|---|

## Handoff notes

[What the next task must know, what it must not redo, and what decisions remain open.]

## Sources

[Primary sources first; include access date and last-verified date.]

## Start-here checklist

[Maximum five concrete next actions.]
```

## Status vocabularies

Use only the following values.

### Open questions

- `open`
- `in_progress`
- `resolved`
- `parked`

### Recommendations

- `provisional`
- `accepted`
- `superseded`
- `rejected`
- `parked`

## Confidence and evidence quality

Use these values consistently:

- `high` — multiple credible primary sources agree, or direct local testing supports the claim
- `medium` — credible evidence exists but has limitations or requires local validation
- `low` — limited, indirect, conflicting, or rapidly changing evidence

## Per-tool additions

### ChatGPT Deep Research

Add:

```text
Prioritise primary sources: official model cards, vendor documentation, GitHub
repositories, runtime documentation, and credible benchmarks.

Cross-check important claims across at least two independent sources where possible.
Explicitly identify conflicts between sources.
Do not treat leaderboard rankings as sufficient evidence for adoption.
Separate benchmark performance from real-world task quality.
Flag claims that are likely to change quickly.
```

### Gemini Deep Research

Add:

```text
Prioritise official documentation, GitHub repositories, release notes, and
integration guides.

Evaluate practical compatibility, not only theoretical capability.
For every runtime, identify concrete integration requirements, API behaviour,
tool-calling support, and known limitations.
Clearly distinguish supported features from community workarounds.
```

### Perplexity PWM/MCP

Add:

```text
Use repository context where available.
Inspect existing documentation, prompts, skills, project structures, and workflows
before proposing new artefacts.

Prefer minimal, composable, versioned outputs.
Do not create repository files without explicit confirmation.
Separate portable instructions from runtime-specific adapters.
Do not claim cross-runtime compatibility without evaluation evidence.
Identify assumptions, uncertainty, scope, and the smallest useful next step.
```

## Update workflow

1. Save the raw output in `docs/research/local-llm-research-outputs/`.
2. Review the proposed `OQ-*` updates.
3. Update only the affected questions in the canonical open-questions register.
4. Review proposed `REC-*` updates.
5. Add or update recommendations only when evidence supports a provisional decision.
6. Record local-validation requirements in the evaluation plan.
7. Run the synthesis task only after its prerequisite task outputs are available.

## Conflict resolution

- If two credible sources conflict, report both positions and assign confidence.
- Prefer primary sources over community sources.
- Prefer direct local testing over benchmark results for adoption decisions.
- Prefer simpler, maintainable options when evidence is comparable.
- Do not resolve a conflict by silently selecting one source.
- Do not treat a benchmark score as sufficient evidence for production adoption.
- Do not treat local hosting as removing legal, ethical, or privacy obligations.