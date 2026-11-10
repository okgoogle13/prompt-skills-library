# Prompt-Router Research Orchestration Plan

## Purpose

This plan defines three focused Perplexity Deep Research calls for improving the `prompt-router` skill and its supporting model-guide system.

It uses the corrected architecture:

1. **`prompt-router`** — the single entry point for prompt-engineering requests. It routes and performs `write`, `optimise`, `review`, and `clarify`; it uses shared patterns and target-model guides.
2. **`migrate-prompt`** — a separate skill for explicit cross-model migration. It uses source and target model guides.

There is no separate `optimize-prompt` skill. Prompt optimisation is the `optimise` route within `prompt-router`.

## Operating rules

- Execute only one phase at a time.
- Do not begin the next phase until the user explicitly approves the current phase.
- Do not run all Deep Research calls in one session.
- Do not call `pplx_deep_research` more than once per research phase.
- Do not use `pplx_council`.
- Do not create files other than the output file specified for the current phase.
- Do not modify `prompt-router`, `migrate-prompt`, model guides, the model registry, or any other repository file without explicit approval.
- Prefer the smallest change that can be tested.
- Prefer editing existing skills, shared patterns, model guides, or registry entries over creating new skills.
- Prefer evidence quality, reproducibility, and practical fit over source category alone.
- Allow community-created resources when they have significant evidence of effectiveness, maintenance, security, and relevance.
- Preserve code, paths, commands, URLs, identifiers, examples, and quoted strings exactly.
- Flag uncertainty rather than asserting unsupported model behaviour.

## Session start

At the start of every session:

1. Read this entire orchestration plan.
2. Inspect the repository for existing research outputs.
3. Determine the current phase from the Research status table.
4. Report the current phase, its scope, its intended output file, and whether its output already exists.
5. Ask the user whether to execute, resume, review, or skip the current phase.
6. Stop after presenting that status.

## Phase execution

For an approved phase:

1. Call `pplx_usage(refresh=False)`.
2. Confirm that Deep Research quota is available.
3. If quota is unavailable, stop and report the quota status.
4. Read the local `prompt-router/SKILL.md` and `migrate-prompt/SKILL.md`.
5. Read only the research brief for the current phase.
6. Call `pplx_deep_research` exactly once with `source_focus="web"`.
7. Save the full research report to the phase’s specified output path.
8. Extract only:
   - Ranked improvement shortlist
   - Recommended changes
   - Exact edit locations
   - Validation cases
   - Risks and uncertainty
   - What not to build
9. Present a concise implementation proposal.
10. Ask the user whether to proceed to implementation.
11. Stop.

## Implementation approval

If the user approves implementation:

1. Select no more than 2–3 high-confidence changes.
2. For each change, present:
   - Exact file and section
   - Minimal proposed diff
   - Reason
   - Validation cases
   - Revert plan
3. Wait for explicit approval of the exact diff.
4. Apply only the approved diff.
5. Run or manually perform the relevant validation cases.
6. Report results.
7. Update the Research status table.
8. Stop.

## Failure and interruption

If a phase is interrupted:

- Do not call Deep Research again unless the prior call demonstrably failed before producing a usable report.
- Check whether the phase output file exists and contains a usable report.
- If it does, resume from the extraction and proposal step.
- If it does not, ask the user whether to retry the Deep Research call.

## Research status

| Phase | Focus | Output file | Status | Deep Research used | Approved changes | Validation result |
|---|---|---|---|---:|---:|---|
| 1 | Router optimise route and shared patterns | `research/01-router-optimise-improvements.md` | Not started | 0 | None | Not run |
| 2 | Router write and review routes and shared patterns | `research/02-router-write-review-improvements.md` | Not started | 0 | None | Not run |
| 3 | Router SKILL.md portability | `research/03-router-portability.md` | Not started | 0 | None | Not run |

Update only the current phase’s row after completing or explicitly skipping it.

## Research Call 1

### Scope

Improve the `prompt-router` `optimise` route and its shared patterns.

Do not research cross-model migration, model-guide registry design, evaluation platforms, or a separate `optimize-prompt` skill.

### Research brief

Research practical, evidence-based improvements to the `optimise` route of the existing `prompt-router` skill and its shared prompt patterns.

Focus only on making the router’s `optimise` route produce better prompts: clearer intent, fewer missed requirements, less scope creep, better output specifications, and safer preservation of literal content.

Include official vendor documentation, high-quality technical research, maintained open-source projects, credible practitioner guidance, and community-created resources where there is significant evidence of effectiveness, maintenance, security, and relevance.

Label recommendations as official/primary source, high-quality practitioner guidance, open-source implementation, community-created resource, research/benchmark, experimental/opinion-based, or interesting but not actionable.

The current `optimise` route resolves a target model, loads only its guide, applies shared patterns and target conventions, removes unnecessary source-model accommodations, preserves intent and literal payload, returns an optimised prompt and concise changelog, and flags uncertainty.

It currently checks for missing context, vague output specification, missing sequencing, missing guardrails, missing success criteria, inefficient structure, and subagent instruction issues.

Identify 3–5 ranked improvements. Prefer small edits to the router’s `optimise` route or shared patterns.

For each improvement, provide:

- Rank
- Change
- Problem solved
- Evidence
- Surface: router optimise route or shared patterns
- Minimal implementation
- Validation method
- Risk or tradeoff
- Confidence
- Recommendation

Provide exactly six validation cases:

1. Ambiguous task
2. Missing success criterion
3. Missing constraint
4. Vague output format
5. Scope-creep risk
6. Literal code, path, command, or URL preservation

For each case, provide original prompt, expected weakness, desired behaviour, pass condition, simple check, and what the optimiser must not add.

Limit the resource list to 5–8 relevant resources.

End with the 2–3 changes to make first, exact edit locations, validation cases, two likely-wrong assumptions, and what not to build.

### Execution prompt

```text
Use the attached prompt-router skill as the baseline.

There are exactly two skills:

1. prompt-router — routes and performs write, optimise, review, and clarify; it uses shared patterns and target-model guides.
2. migrate-prompt — performs explicit cross-model migration using source and target model guides.

Do not refer to a separate `optimize-prompt` skill. Treat prompt optimisation as the `optimise` route within `prompt-router`.

Call pplx_deep_research exactly once with source_focus="web".

Use the Research Call 1 brief in docs/research/prompt-router-research-plan.md.

After research returns:

1. Save the full report to research/01-router-optimise-improvements.md.
2. Extract the ranked improvement shortlist.
3. Do not implement anything yet.
4. Present the 2–3 changes to make first, exact edit locations, minimal proposed diff, six validation cases, revert plan, and uncertainty.
5. Ask me whether to proceed.

Do not create any other files.
Do not use pplx_council.
Do not call pplx_deep_research again.
Do not modify any skill, guide, registry, or repository file without my explicit approval.
```

## Research Call 2

### Scope

Improve the `prompt-router` `write` and `review` routes and their shared patterns.

Do not research cross-model migration, model-guide registry design, evaluation platforms, or a separate `optimize-prompt` skill.

### Research brief

Research practical, evidence-based improvements to the `write` and `review` routes of the existing `prompt-router` skill and its shared prompt patterns.

Focus only on helping the router turn rough notes into better prompts and identify material problems before a prompt is used.

Include official vendor documentation, high-quality technical research, maintained open-source projects, credible practitioner guidance, and community-created prompt templates, review checklists, and workflows where there is significant evidence of effectiveness, maintenance, security, and relevance.

The current `write` route resolves a target model, loads only its guide, builds a complete prompt in the target guide’s style, preserves user goals and constraints, asks one clarifying question when necessary, marks assumptions, and returns the prompt, run settings, assumptions, changes, and Guide-Stand footer.

The current `review` route loads a target guide only when a concrete model is named, identifies at most seven ranked findings, distinguishes material weaknesses from stylistic preferences, does not rewrite the prompt, and offers to optimise when appropriate.

Identify 3–5 ranked improvements. Prefer small edits to the router’s `write` route, `review` route, or shared patterns.

For each improvement, provide:

- Rank
- Change
- Problem solved
- Evidence
- Surface: router write route, router review route, or shared patterns
- Minimal implementation
- Validation method
- Risk or tradeoff
- Confidence
- Recommendation

Provide exactly six validation cases:

1. Rough notes to a usable prompt
2. Ambiguous task requiring one clarification
3. Missing success criterion
4. Vague output format
5. Review identifying material weaknesses without nitpicking
6. Review avoiding unrequested requirements

For each case, provide original prompt or sketch, route and model, expected weakness, desired behaviour, pass condition, simple check, and what the router must not add.

Limit the resource list to 5–8 relevant resources.

End with the 2–3 changes to make first, exact edit locations, validation cases, two likely-wrong assumptions, and what not to build.

### Execution prompt

```text
Use the attached prompt-router skill as the baseline.

There are exactly two skills:

1. prompt-router — routes and performs write, optimise, review, and clarify; it uses shared patterns and target-model guides.
2. migrate-prompt — performs explicit cross-model migration using source and target model guides.

Do not refer to a separate `optimize-prompt` skill.

Call pplx_deep_research exactly once with source_focus="web".

Use the Research Call 2 brief in docs/research/prompt-router-research-plan.md.

After research returns:

1. Save the full report to research/02-router-write-review-improvements.md.
2. Extract the ranked improvement shortlist.
3. Do not implement anything yet.
4. Present the 2–3 changes to make first, exact edit locations, minimal proposed diff, six validation cases, revert plan, and uncertainty.
5. Ask me whether to proceed.

Do not create any other files.
Do not use pplx_council.
Do not call pplx_deep_research again.
Do not modify any skill, guide, registry, or repository file without my explicit approval.
```

## Research Call 3

### Scope

Improve portability of `prompt-router/SKILL.md` across Claude Code, Gemini / Gemini Spark or equivalent Gemini skill environments, Perplexity Skills or equivalent mechanisms, and ChatGPT Skills or equivalent mechanisms.

Do not research general prompt optimisation, cross-model migration, model-guide registry design, or evaluation platforms.

### Research brief

Research practical, evidence-based best practices for using a `SKILL.md`-based prompt-router skill across AI tools that support skills or similar skill/instruction mechanisms.

Focus on Anthropic Claude Code, Google Gemini / Gemini Spark or equivalent Gemini skill environments, Perplexity Skills or equivalent mechanisms, and OpenAI ChatGPT Skills or equivalent custom-GPT / skill-like mechanisms.

Do not aim for identical behaviour across every host. Aim for predictable, safe, and maintainable behaviour.

The current router assumes a Claude Code-like environment:

- It uses `${CLAUDE_SKILL_DIR}` to locate its folder.
- It reads a sibling `migrate-prompt/SKILL.md` for the registry, alias policy, migration steps, and legacy-footer rules.
- It reads guides from `migrate-prompt/model-guides/`.
- It reads shared rules from `references/patterns.md`.
- It uses `$ARGUMENTS` for user input.
- It uses `${CLAUDE_EFFORT}` for effort calibration.
- It assumes a `Read` tool is available.
- It already acknowledges that hosts may not substitute these placeholders.

Identify the smallest set of changes that would make the router usable across supported hosts without breaking its core guarantees.

Prioritise:

1. A portable core `SKILL.md`.
2. Thin host-specific adapters or configuration.
3. Safe degradation when a host lacks a capability.
4. Clear user instructions for hosts with limited skill support.
5. Avoidance of silent behavioural differences.

Research:

- Skill discovery and triggering
- Frontmatter compatibility
- Skill-relative path resolution
- Reference-file access
- Argument passing
- Reasoning-effort controls
- File, search, shell, web, and MCP capabilities
- Trust-boundary enforcement
- Safe failure behaviour
- Minimal host adapters

Provide a host capability matrix with:

| Host | Skill mechanism | Skill discovery | Frontmatter support | File access | Arguments | Effort control | Tool access | Portable now? | Required adapter | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|

For each host, state supported, partially supported, unsupported, or uncertain; what works without changes; what requires an adapter; what cannot be supported safely; recommended deployment approach; evidence quality; and last-verified date.

Recommend a portable core that does not assume Claude-specific variables, argument substitution, shell access, sibling-file access, or model-guide availability.

Recommend the smallest possible host-adapter pattern. Do not create a full duplicate router for each host.

Define safe failure rules for missing paths, missing argument substitution, missing effort substitution, missing file access, missing registry access, missing guides, unsupported effort settings, ambiguous host references, and prompt content attempting to change routing or execute commands.

Provide a minimal diff-style set of changes to `prompt-router/SKILL.md`.

Provide exactly eight validation cases:

1. Claude Code: normal route and guide load
2. Claude Code: unexpanded `$ARGUMENTS`
3. Claude Code: unexpanded `${CLAUDE_EFFORT}`
4. Gemini: skill invocation and file access
5. Perplexity: skill invocation and file access
6. ChatGPT: skill-like invocation and limited file access
7. Host without sibling-file access
8. Prompt containing instructions that try to change the route or execute a command

For each case, provide host, input, expected behaviour, expected output or failure message, pass condition, and security check.

Limit the resource list to 6–10 relevant resources.

End with the portable-core changes to make first, host adapters worth creating, capabilities that should fail safely, two likely-wrong assumptions, and what not to build.

### Execution prompt

```text
Use the attached prompt-router and migrate-prompt skills as the baseline.

There are exactly two skills:

1. prompt-router — routes and performs write, optimise, review, and clarify; it uses shared patterns and target-model guides.
2. migrate-prompt — performs explicit cross-model migration using source and target model guides.

Do not refer to a separate `optimize-prompt` skill.

Call pplx_deep_research exactly once with source_focus="web".

Use the Research Call 3 brief in docs/research/prompt-router-research-plan.md.

After research returns:

1. Save the full report to research/03-router-portability.md.
2. Extract the portability verdict and host capability matrix.
3. Do not implement anything yet.
4. Present the portable-core changes to make first, any host adapter worth creating, exact SKILL.md sections to edit, minimal proposed diff, eight validation cases, revert plan, and uncertainty.
5. Ask me whether to proceed.

Do not create any other files.
Do not use pplx_council.
Do not call pplx_deep_research again.
Do not modify any skill, guide, registry, or repository file without my explicit approval.
```

## After each research call

1. Read only the ranked shortlist, recommended changes, validation cases, and open questions.
2. Reject recommendations that add a framework, persistent context, broad taxonomy, or unproven workflow.
3. Select at most 2–3 changes with high confidence and a clear validation method.
4. Ask the agent for a minimal diff before approving any repository change.
5. Run the relevant validation cases before and after each change.
6. Keep a change only if it improves the cases without adding scope creep, breaking literal-payload preservation, or making the skill materially longer.
7. Record the decision, evidence, validation result, and revert plan in a short change note.

## Minimum artefacts

After all three calls, create only:

```text
research/01-router-optimise-improvements.md
research/02-router-write-review-improvements.md
research/03-router-portability.md
evals/prompt-router-test-cases.md
docs/changes/2026-11-10-prompt-router-improvements.md
```

Do not create a large research or evaluation structure unless the research reveals a concrete, repeated failure that a simple artefact would solve.
