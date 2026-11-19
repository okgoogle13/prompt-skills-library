# Local LLM Research Plan

Status: active
Last reviewed: 2026-11-19
Scope: coordination of external research, local validation, and repository implementation for the local-LLM stack.

## Purpose

This plan coordinates research across ChatGPT Deep Research, Gemini Deep Research, and Perplexity PWM/MCP. It maps research tasks to open questions, defines dependencies and output locations, and prevents duplicate or conflicting recommendations.

The canonical inputs are:

- `docs/research/local-llm-open-questions.md`
- `docs/research/local-llm-recommendations.md`
- `docs/research/local-llm-research-contract.md`

## Research principles

- Research one narrowly scoped decision area per task.
- Use one canonical open-questions register and one canonical recommendations register.
- Assign every question to exactly one research task.
- Separate web research from local validation.
- Mark recommendations `provisional` until validated on the RTX 5090 laptop.
- Prefer a small core model set over a large model collection.
- Prefer local processing for privacy-sensitive work.
- Retain cloud models only where local models fail a defined quality threshold.
- Do not make final integrated decisions outside the synthesis task.

## Task routing

| Task ID | Recommended primary tool | Questions owned | Output file | Feeds |
|---|---|---|---|---|
| `RTX5090-ENVELOPE` | ChatGPT Deep Research or Gemini Deep Research | OQ-004, OQ-019, OQ-020, OQ-021 | `docs/research/local-llm-research-outputs/01-rtx5090-envelope.md` | `MODEL-SHORTLIST`, `RUNTIME-STACK`, `SYNTHESIS` |
| `MODEL-SHORTLIST` | ChatGPT Deep Research or Gemini Deep Research | OQ-001, OQ-002, OQ-003, OQ-006, OQ-007, OQ-008, OQ-009, OQ-010, OQ-011, OQ-012, OQ-022–OQ-027 | `docs/research/local-llm-research-outputs/02-model-shortlist.md` | `RUNTIME-STACK`, `IDE-AGENTS`, `HOME-ASSISTANT`, `SYNTHESIS` |
| `RUNTIME-STACK` | Gemini Deep Research, with Perplexity PWM/MCP validation | OQ-005, OQ-013, OQ-028–OQ-030 | `docs/research/local-llm-research-outputs/03-runtime-stack.md` | `IDE-AGENTS`, `HOME-ASSISTANT`, `SYNTHESIS` |
| `IDE-AGENTS` | Perplexity PWM/MCP | OQ-016, OQ-031–OQ-034 | `docs/research/local-llm-research-outputs/04-ide-agents.md` | `SYNTHESIS` |
| `HOME-ASSISTANT` | ChatGPT Deep Research or Gemini Deep Research, with Perplexity PWM/MCP validation | OQ-035–OQ-038 | `docs/research/local-llm-research-outputs/05-home-assistant.md` | `SYNTHESIS` |
| `SYNTHESIS` | Perplexity PWM/MCP | OQ-014, OQ-015, OQ-017, OQ-018, OQ-039–OQ-041 | `docs/research/local-llm-research-outputs/06-synthesis.md` | Repository implementation |

## Task boundaries

### RTX5090-ENVELOPE

Determine the practical deployment envelope for the RTX 5090 laptop.

Must produce:

- Nominal and realistic usable VRAM.
- RAM, storage, CPU, and offload constraints.
- Thermal and sustained-performance constraints.
- A model-size and quantisation capacity matrix.
- A practical context/VRAM budget.

Must not decide:

- Final model selection.
- Runtime selection.
- IDE workflow.
- Home Assistant model.

### MODEL-SHORTLIST

Identify the strongest current local models by use case.

Must produce:

- A shortlist for daily driver, coding, high reasoning, writing, routine tasks, long context, vision, embeddings, and privacy-sensitive work.
- One or two primary models per category, with backups only where justified.
- A proposed core model set, subject to synthesis.
- Models to avoid or defer.

Must not decide:

- Runtime selection.
- IDE workflow.
- Home Assistant model.
- Final integrated stack.

### RUNTIME-STACK

Select the runtime and serving approach.

Must produce:

- A comparison of Ollama, LM Studio, llama.cpp/llama-server, vLLM, SGLang, Jan, and Open WebUI where relevant.
- A primary interactive runtime.
- A primary API/automation runtime.
- API, tool-calling, structured-output, and concurrency findings.
- A model-registry and update workflow.

Must not decide:

- Final model selection.
- Final IDE workflow.
- Home Assistant model.

### IDE-AGENTS

Design the local-first IDE and agent workflow.

Must produce:

- Antigravity and VS Code integration findings.
- Local-model endpoint and tool-calling requirements.
- A hybrid local/cloud coding policy.
- Project-specific routing for career-brain, comms-hub-v2, and parents-move.
- A minimal agent-reliability test plan.

Must not decide:

- Final model selection.
- Runtime selection.
- Home Assistant model.

### HOME-ASSISTANT

Select and validate a small Home Assistant model.

Must produce:

- A small-model shortlist.
- A recommended integration path.
- Latency, accuracy, and reliability thresholds.
- A rules-based versus LLM-based control policy.
- A minimal deployment architecture.

Must not decide:

- Primary laptop model stack.
- Final IDE workflow.
- Final subscription-replacement policy.

### SYNTHESIS

Consolidate research and produce the final decision set.

Must produce:

- The final core model set.
- The final runtime stack.
- The use-case routing policy.
- The subscription-replacement roadmap.
- The evaluation plan.
- The repository artefact plan.

Must not introduce new model, runtime, or workflow claims without evidence.

## Execution sequence

1. Run `RTX5090-ENVELOPE`.
2. Run `MODEL-SHORTLIST`, using the capacity matrix from Task 1.
3. Run `RUNTIME-STACK`, using the model shortlist and capacity constraints.
4. Run `IDE-AGENTS`, using the selected runtime and model shortlist.
5. Run `HOME-ASSISTANT`, using the runtime findings and small-model requirements.
6. Run `SYNTHESIS`, using all prior task outputs.

## Tool allocation

| Tool | Best use | Tasks |
|---|---|---|
| ChatGPT Deep Research | Broad, current, source-triangulated research | `RTX5090-ENVELOPE`, `MODEL-SHORTLIST`, `HOME-ASSISTANT` |
| Gemini Deep Research | Broad documentation and integration research | `RUNTIME-STACK`; optional second opinion for `MODEL-SHORTLIST` |
| Perplexity PWM/MCP | Repository-specific implementation, validation, and synthesis | `IDE-AGENTS`, `SYNTHESIS`; validation for `RUNTIME-STACK` and `HOME-ASSISTANT` |

## Handoff protocol

After each task, create a handoff note at the end of its research dossier:

```markdown
# Handoff: [FROM TASK] → [TO TASK]

## Decisions made
- [Decision or provisional recommendation]

## Decisions still open
- [Question ID and why it remains open]

## Constraints passed forward
- [VRAM, context, privacy, runtime, or workflow constraints]

## Inputs required by next task
- [Files, specifications, model IDs, or test results]

## Do not redo
- [Research already completed]

## Validation required before adoption
- [Local tests or measurements]
```

## Repository artefacts

The synthesis task should produce or update:

- `docs/local-llms/model-registry.md`
- `docs/local-llms/runtime-selection.md`
- `docs/local-llms/rtx-5090-laptop-profile.md`
- `docs/local-llms/use-case-routing.md`
- `docs/local-llms/home-assistant.md`
- `docs/local-llms/subscription-replacement.md`
- `evals/local-models/`
- `skills/local-model-router/`

Do not create repository implementation files until the synthesis task has consolidated the research outputs and the user has confirmed the implementation scope.