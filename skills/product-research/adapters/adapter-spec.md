---
workflow: au-product-research
version: 0.1.0-draft
updated: 2026-11-23
source: prompt-skills-library
---

# Product Research Adapter Specification

This specification governs every runtime adapter for the Australian product-research workflow. An adapter translates the portable workflow for a specific AI runtime; it must not redefine the research method, evidence policy, stages, scoring rules, or output contract.

## Canonical files

Every adapter must treat these files as authoritative:

- `../shopping-core.md` — portable core research policy
- `../stage-prompts.md` — portable stage-by-stage workflow
- `../templates/purchase-brief-template.md` — purchase intake contract
- `../templates/purchase-record-template.md` — evidence, offer, conflict, and decision record
- `../templates/handover-template.md` — handover snapshot contract

If an adapter conflicts with any canonical file, the canonical file controls.

## Adapter purpose

An adapter answers runtime-specific questions:

1. Where should the user place the core instruction?
2. Which files should be uploaded, attached, or pasted?
3. How does the user start Interview Me?
4. How does the user invoke each research stage?
5. Which platform tools are available or unavailable?
6. How should context, memory, and personalisation be managed?
7. What verification steps are required before relying on output?

An adapter must not:

- Add, remove, rename, or reorder workflow stages.
- Change evidence categories, source-eligibility rules, or citation requirements.
- Introduce composite scores, rankings, or product recommendations outside the canonical workflow.
- Merge purchases or allow cross-purchase context.
- Replace `shopping-core.md` with a runtime-specific policy.
- Claim that a platform provides perfect context isolation.
- Assume Deep Research, browser automation, code execution, or file execution is available.

## Required adapter sections

Every adapter must contain these sections, in this order:

```markdown
# [Runtime] Product Research Adapter

## When to use

## Required files

## Setup

## Interview Me

## Stage invocation

## Platform limitations

## Context and memory

## Verification

## Conflict rule
```

## Adapter contract

### When to use

State the exact runtime and intended use. For example: “Use in a Perplexity Project for one Australian consumer-product purchase.”

### Required files

List every canonical file the user must upload, attach, paste, or make available. Distinguish between:

- Files placed in persistent project storage.
- Files attached to an individual chat.
- Instructions pasted into project or custom instructions.
- Files loaded by a packaged skill.

### Setup

Give concise setup steps. Include project naming, folder or workspace isolation, and any settings the user should check.

Use one project, notebook, workspace, or chat thread per purchase. Never mix candidates, evidence, prices, or conclusions from different purchases.

### Interview Me

Define the Stage 0 trigger and procedure:

- Trigger phrases: “interview me”, “start a new purchase”, or “create the purchase brief”.
- Ask only for missing required fields.
- Ask in groups of 3–5 related questions.
- Offer defaults only when clearly labelled as assumptions.
- Do not name, recommend, compare, or price products during intake.
- Output the completed brief in one Markdown code block.
- Ask whether to proceed to Stage 1 or revise the brief.

### Stage invocation

Map each canonical stage to the runtime’s practical invocation method.

Use these stage names exactly:

1. Stage 0 — Interview Me
2. Stage 1 — Criteria framing and Australian risk check
3. Stage 2–3 — Bounded candidate and evidence pilot
4. Stage 4 — Offer and purchase-risk check
5. Stage 5 — Decision record

For each stage, state:

- The user prompt or command.
- Files to attach or load.
- Expected output sections.
- Any runtime-specific tool to use or avoid.

### Platform limitations

State only verified or clearly labelled limitations. Do not invent capabilities.

Cover, where relevant:

- Web search availability and reliability.
- Deep Research availability.
- Skill, Gem, Project, Notebook, or Computer support.
- File-upload limits.
- Browser, code-execution, or local-file access.
- Memory, personalisation, and context-isolation behaviour.
- Australian availability or plan restrictions, if known.

If a limitation is uncertain, write `Unverified` rather than asserting it.

### Context and memory

Recommend practical context controls, but do not overstate isolation.

- Use one workspace per purchase.
- Prefer project-scoped instructions and files over global personal instructions.
- Disable or avoid cross-project memory where the runtime supports it.
- Start a fresh chat when switching purchases, changing tools, returning after a break, or noticing drift.
- Do not treat memory controls as a guarantee that no information can influence another chat.

### Verification

Require the user to verify primary sources before treating a claim as decided.

At minimum:

- Open 2–3 cited URLs directly.
- Check exact model and Australian SKU match.
- Check publication or check date.
- Check acquisition, sponsorship, affiliate disclosure, and methodology.
- Fill in `Claim Support`, `Exact-Model Match`, `Source Eligibility`, `Human Check Date`, and `Limitations`.
- Treat self-critique or another model as an error-finding aid, not independent verification.

### Conflict rule

State this exact rule:

> If this adapter conflicts with `shopping-core.md`, `stage-prompts.md`, or a template in `templates/`, the canonical file controls.

## Authoring process

To create a new adapter:

1. Read every canonical file listed above.
2. Research only the official documentation for the target runtime.
3. Draft one Markdown adapter file using the required sections.
4. Do not alter canonical files.
5. Run a bounded pilot for one purchase.
6. Record failures, missing capabilities, and wording changes.
7. Update the adapter only after the pilot.

## File naming

Use lowercase hyphenated names:

```text
claude-project-instructions.md
chatgpt-project-instructions.md
perplexity-project-instructions.md
gemini-spark-instructions.md
antigravity-ide-instructions.md
```

## Acceptance test

An adapter is acceptable only if:

- It preserves the canonical evidence policy and stage sequence.
- It preserves one-purchase isolation.
- It preserves the required output sections.
- It clearly separates portable policy from runtime instructions.
- It identifies uncertain platform behaviour as `Unverified`.
- It requires human verification of primary sources.
- It does not introduce a new scoring or recommendation system.
