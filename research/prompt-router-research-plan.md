# Prompt-Router Research Orchestration Plan

## Purpose

This plan defines three focused Perplexity Deep Research calls for improving the `prompt-router` skill and its supporting model-guide system.

It uses the corrected architecture:

1. **`prompt-router`** — the single entry point for prompt-engineering requests. It routes and performs `write`, `optimise`, `review`, and `clarify`; it uses shared patterns and target-model guides.
2. **`migrate-prompt`** — a separate skill for explicit cross-model migration. It uses source and target model guides.

There is no separate `optimize-prompt` skill. Prompt optimisation is the `optimise` route within `prompt-router`.

## Model-guide integration pattern

`model-guides-combined.md` is the canonical evidence corpus and build input. It is not runtime prompt context.

The runtime architecture is:

```text
model-guides-combined.md
        |
        +-- model-guides/<model-id>.md       Runtime authoritative guide
        +-- model-registry.md                Compact routing index
        +-- profiles/<model-id>.md           Optional compact routing profile
        +-- prompt-router/SKILL.md           Stable routing contract
        +-- migrate-prompt/SKILL.md          Registry, aliases, migration algorithm
```

| Artefact | Role | Loaded into prompt context? |
|---|---|---|
| `model-guides-combined.md` | Canonical source corpus, provenance, source links, uncertainty, and regeneration input | No |
| `model-guides/<model-id>.md` | Authoritative runtime facts for one model | Yes, only after resolution |
| `model-registry.md` | Compact index of IDs, aliases, status, successor, and guide path | Yes, compact only |
| `profiles/<model-id>.md` | Optional high-signal routing profile | Optional; never a substitute for the full guide |
| `prompt-router/SKILL.md` | Routing, trust boundary, output contract, and loading rules | Yes |
| `migrate-prompt/SKILL.md` | Registry policy, alias policy, migration steps, and footer rules | Yes, as needed |

Preserve these invariants:

- `write`, `optimise`, and `review` load one target guide.
- `migrate` loads exactly two guides: source and target.
- The router never falls back to model facts from memory.
- The router never reads unrelated guides.
- The registry resolves; it does not replace the selected guide.
- A profile may assist routing or safety checks, but the full guide remains authoritative.

Do not propose inlining the combined corpus, duplicating model facts into prompts, or creating a separate model-guide-router skill.

## PWM skill versus direct MCP

Use two distinct layers:

| Layer | Purpose | When to use |
|---|---|---|
| PWM Agent Skill | Operational guidance: authentication, quota checking, MCP tool selection, `source_focus`, and failure handling | Once at session start, and for troubleshooting |
| Direct MCP calls | Controlled research execution: `pplx_usage`, `pplx_sources` if explicitly approved, and `pplx_deep_research` | Inside an approved research phase |

At session start, load the installed Perplexity Web MCP (PWM) Agent Skill for operational guidance only. Do not use it to initiate, repeat, or broaden research.

During an approved research phase, use direct MCP calls only:

- `pplx_usage(refresh=False)`
- `pplx_deep_research(query=..., source_focus="web")`

Do not invoke `pplx_ask`, `pplx_sonar`, `pplx_query`, `pplx_council`, `pplx_sources`, or any other PWM query tool unless the user explicitly approves it.

PWM provides 22 MCP tools, including `pplx_usage`, `pplx_deep_research`, `pplx_query`, `pplx_ask`, and `pplx_sources`. Its Agent Skill teaches agents how to use the CLI and MCP capabilities; it does not replace the need for explicit, user-approved research execution.

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
- Preserve lazy guide loading: never inline the combined corpus or load unrelated guides.

## Evidence hierarchy

Use this hierarchy when assessing sources:

1. Official vendor documentation.
2. Primary technical research or benchmarks.
3. Maintained open-source implementation with clear tests or documented behaviour.
4. High-quality practitioner guidance from a credible maintainer.
5. Community-created resource with evidence of effectiveness, maintenance, security, and relevance.
6. Experimental or opinion-based material.

Never treat a lower-tier source as sufficient support for a behavioural claim when a higher-tier source is available.

Community-created resources are welcome when there is significant evidence they are effective and relevant: sustained maintenance, transparent methodology, credible authorship, adoption or citations, reproducible evaluation, clear documentation, and demonstrated fit.

## Research decision rules

Prioritise recommendations that:

- Can be implemented as a small edit to an existing route, shared pattern, guide, or registry.
- Have a clear validation case.
- Do not require a new skill, framework, persistent memory, or broad taxonomy.
- Preserve literal user content.
- Reduce ambiguity without increasing router complexity.
- Preserve the model-guide integration pattern and lazy-loading guarantees.

Reject recommendations that:

- Add a new skill.
- Require a new persistent context system.
- Introduce a broad prompt-quality taxonomy.
- Cannot be validated with the specified cases.
- Depend on unavailable host capabilities.
- Inline the combined corpus into a skill or research prompt.
- Replace the selected full guide with registry metadata or a profile.

## Session start

At the start of every session:

1. Load the installed Perplexity Web MCP (PWM) Agent Skill for operational guidance only.
2. Read this entire orchestration plan.
3. Inspect `research/` for existing phase outputs.
4. Determine the current phase from the Research status table.
5. Report clearly and completely:
   - Current phase
   - Scope
   - Intended output file
   - Whether that output exists and is usable
   - Required PWM call
   - Expected quota cost
6. Ask whether to execute, resume, review, or skip.
7. Stop immediately and wait for user input (1 turn, 0 research tool calls).

Do not execute any research query at this stage.

## Pre-research contract

Before calling `pplx_deep_research`, output and await approval for:

1. Research question
2. Scope and exclusions
3. Evidence hierarchy
4. Intended `source_focus`
5. Expected deliverable
6. Exact output path
7. Required validation cases
8. Quota cost
9. Stop conditions
10. Model-guide integration constraints

Stop and proceed only after the user replies: `Approved.`

## Phase execution

For an approved phase:

1. Load the installed PWM Agent Skill for operational guidance only.
2. Call `pplx_usage(refresh=False)`.
3. Report Deep Research and Pro Search quota status.
4. If Deep Research quota is 0, unavailable, or cannot be verified:
   - Do not call `pplx_deep_research`.
   - Report the exact quota response.
   - Ask whether to stop, refresh usage once with `refresh=true`, or defer the phase.
   - Stop immediately.
5. Read the local `prompt-router/SKILL.md` and `migrate-prompt/SKILL.md`.
6. Read only the research brief for the current phase.
7. Confirm the exact output path does not already contain a usable report.
8. Call `pplx_deep_research` exactly once with `source_focus="web"`.
9. Save the full report to the phase’s specified output path.
10. Append a complete, detailed extraction section titled `## Extraction — do not edit the full report above`.
11. Present a concise implementation proposal with complete detail for each required field.
12. Ask whether to proceed to implementation.
13. Stop immediately (maximum 1 `pplx_deep_research` call per phase; do not iterate further).

Do not call `pplx_ask`, `pplx_sonar`, `pplx_query`, `pplx_council`, `pplx_sources`, or `pplx_deep_research` again during the same phase.

## Usable report definition

A report is usable only if it contains:

- A ranked improvement shortlist.
- At least the required number of validation cases.
- Concrete edit locations or implementation guidance.
- Risks, uncertainty, and a “what not to build” section.
- An explicit assessment of compatibility with the model-guide integration pattern.

A file containing only raw research output, an error message, or an incomplete report is not usable.

## Extraction template

After saving the full report, append or create a clearly separated section titled:

```markdown
## Extraction — do not edit the full report above
```

Provide comprehensive, structured detail for:

1. Ranked improvement shortlist
2. Recommended changes
3. Exact edit locations
4. Validation cases
5. Risks and uncertainty
6. What not to build
7. Two likely-wrong assumptions
8. First 2–3 changes
9. Model-guide integration compatibility

## Implementation approval

If the user approves implementation:

1. Select no more than 2–3 high-confidence changes.
2. For each change, present in full detail:
   - Exact file and section
   - Minimal proposed diff
   - Reason
   - Validation cases
   - Revert plan
   - Effect on guide loading and registry resolution
3. Wait for explicit approval of the exact diff and stop.
4. Apply only the approved diff.
5. Run or manually perform the relevant validation cases.
6. Report results.
7. Update the Research status table.
8. Stop immediately.

## Failure and interruption

If a phase is interrupted:

- Do not call Deep Research again unless the prior call demonstrably failed before producing a usable report.
- Check whether the phase output file exists and contains a usable report.
- If it does, resume from the extraction and proposal step.
- If it does not, ask the user whether to retry the Deep Research call and stop.

## Research status

| Phase | Focus | Output file | Status | Deep Research used | Approved changes | Validation result |
|---|---|---|---|---:|---:|---|
| 1 | Router optimise route and shared patterns | `research/01-router-optimise-improvements.md` | Completed | 1 | 3 (`references/patterns.md` §1, §2.1, §2.2, §2.5) | Passed (6/6) |
| 2 | Router write and review routes and shared patterns | `research/02-router-write-review-improvements.md` | Completed | 1 | 3 (`references/patterns.md` §3, §6) | Passed (6/6) |
| 3 | Router portability and model-guide integration | `research/03-router-portability.md` | Completed | 1 | 3 (`prompt-router/SKILL.md` `## Files`, `## Step 1`, `## Step 3`, `## Step 4`; defect fixed 2026-11-14) | Offline 4/5 pass, Check 3 FAIL (4 registry IDs missing from corpus); live Claude Code cases C1, C2, C3, C8 run after the 2026-11-14 placeholder fix (see change note); C4–C6 external/unverified; C7 removed with migration scope |

Update only the current phase’s row after completing or explicitly skipping it.

## Research Call 1

### Scope

Improve the `prompt-router` `optimise` route and its shared patterns.

Do not research cross-model migration, model-guide registry design, evaluation platforms, or a separate `optimize-prompt` skill.

### Research brief

Research practical, evidence-based improvements to the `optimise` route of the existing `prompt-router` skill and its shared prompt patterns.

Focus only on making the router’s `optimise` route produce better prompts: clearer intent, fewer missed requirements, less scope creep, better output specifications, and safer preservation of literal content.

Use the evidence hierarchy. Include official vendor documentation, high-quality technical research, maintained open-source projects, credible practitioner guidance, and community-created resources where there is significant evidence of effectiveness, maintenance, security, and relevance.

The current `optimise` route resolves a target model, loads only its guide, applies shared patterns and target conventions, removes unnecessary source-model accommodations, preserves intent and literal payload, returns an optimised prompt and concise changelog, and flags uncertainty.

It currently checks for missing context, vague output specification, missing sequencing, missing guardrails, missing success criteria, inefficient structure, and subagent instruction issues.

Preserve the model-guide integration pattern:

- Resolve the target model through the compact registry.
- Load only the resolved target guide.
- Do not inline `model-guides-combined.md`.
- Do not replace guide content with registry metadata or a profile.
- Do not create a separate optimisation skill.

Identify 3–5 ranked improvements. Prefer small edits to the router’s `optimise` route or shared patterns.

For each improvement, provide:

- Rank
- Change
- Problem solved
- Evidence
- Evidence tier
- Surface: router optimise route or shared patterns
- Minimal implementation
- Validation method
- Risk or tradeoff
- Confidence
- Recommendation
- Effect on guide loading and registry resolution

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

Preserve the model-guide integration pattern:

- `model-guides-combined.md` is the canonical corpus and build input, not runtime prompt context.
- The compact registry resolves model IDs and aliases.
- The selected per-model guide is the only authority for model-specific recommendations.
- `optimise` loads exactly one target guide.
- Do not inline the combined corpus.
- Do not replace guide content with registry metadata or a profile.

Based on the baseline skill and constraints above, execute the following steps:

1. Load the installed Perplexity Web MCP (PWM) Agent Skill for operational guidance only.
2. Call pplx_usage(refresh=False). If Deep Research quota is unavailable, stop and report the quota status.
3. Call pplx_deep_research exactly once with source_focus="web", using the Research Call 1 brief in research/prompt-router-research-plan.md.
4. Save the full report to research/01-router-optimise-improvements.md.
5. Append a complete, detailed extraction section containing the ranked improvement shortlist, recommended changes, exact edit locations, six validation cases, risks, uncertainty, likely-wrong assumptions, what not to build, and model-guide integration compatibility.
6. Do not implement anything yet.
7. Present in full detail the 2–3 changes to make first, exact edit locations, minimal proposed diff, six validation cases, revert plan, effect on guide loading and registry resolution, and uncertainty.
8. Ask me whether to proceed and stop immediately (maximum 1 pplx_deep_research call).

Do not create any other files.
Do not use pplx_ask, pplx_sonar, pplx_query, pplx_council, or pplx_sources.
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

Use the evidence hierarchy. Include official vendor documentation, high-quality technical research, maintained open-source projects, credible practitioner guidance, and community-created prompt templates, review checklists, and workflows where there is significant evidence of effectiveness, maintenance, security, and relevance.

The current `write` route resolves a target model, loads only its guide, builds a complete prompt in the target guide’s style, preserves user goals and constraints, asks one clarifying question when necessary, marks assumptions, and returns the prompt, run settings, assumptions, changes, and Guide-Stand footer.

The current `review` route loads a target guide only when a concrete model is named, identifies at most seven ranked findings, distinguishes material weaknesses from stylistic preferences, does not rewrite the prompt, and offers to optimise when appropriate.

Preserve the model-guide integration pattern:

- Resolve a concrete model through the compact registry before loading its guide.
- Load only the resolved target guide for `write`.
- Load a guide for `review` only when a concrete model is named.
- Do not inline `model-guides-combined.md`.
- Do not replace guide content with registry metadata or a profile.
- Do not create a separate writing or review skill.

Identify 3–5 ranked improvements. Prefer small edits to the router’s `write` route, `review` route, or shared patterns.

For each improvement, provide:

- Rank
- Change
- Problem solved
- Evidence
- Evidence tier
- Surface: router write route, router review route, or shared patterns
- Minimal implementation
- Validation method
- Risk or tradeoff
- Confidence
- Recommendation
- Effect on guide loading and registry resolution

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

Preserve the model-guide integration pattern:

- `model-guides-combined.md` is the canonical corpus and build input, not runtime prompt context.
- The compact registry resolves model IDs and aliases.
- The selected per-model guide is the only authority for model-specific recommendations.
- `write` loads exactly one target guide.
- `review` loads a guide only when a concrete model is named.
- Do not inline the combined corpus.
- Do not replace guide content with registry metadata or a profile.

Based on the baseline skill and constraints above, execute the following steps:

1. Load the installed Perplexity Web MCP (PWM) Agent Skill for operational guidance only.
2. Call pplx_usage(refresh=False). If Deep Research quota is unavailable, stop and report the quota status.
3. Call pplx_deep_research exactly once with source_focus="web", using the Research Call 2 brief in research/prompt-router-research-plan.md.
4. Save the full report to research/02-router-write-review-improvements.md.
5. Append a complete, detailed extraction section containing the ranked improvement shortlist, recommended changes, exact edit locations, six validation cases, risks, uncertainty, likely-wrong assumptions, what not to build, and model-guide integration compatibility.
6. Do not implement anything yet.
7. Present in full detail the 2–3 changes to make first, exact edit locations, minimal proposed diff, six validation cases, revert plan, effect on guide loading and registry resolution, and uncertainty.
8. Ask me whether to proceed and stop immediately (maximum 1 pplx_deep_research call).

Do not create any other files.
Do not use pplx_ask, pplx_sonar, pplx_query, pplx_council, or pplx_sources.
Do not call pplx_deep_research again.
Do not modify any skill, guide, registry, or repository file without my explicit approval.
```

## Research Call 3

### Scope

Assess portability of `prompt-router/SKILL.md` and the model-guide integration pattern across Claude Code, the Gemini skill mechanisms actually available in the user’s current environment, Perplexity skill mechanisms actually available in the user’s current environment, and ChatGPT skill-like mechanisms actually available in the user’s current environment.

Do not research general prompt optimisation, cross-model migration, evaluation platforms, or a separate `optimize-prompt` skill.

### Research brief

Research practical, evidence-based best practices for using a `SKILL.md`-based prompt-router skill across AI tools that support skills or similar skill/instruction mechanisms.

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

The intended integration pattern is:

```text
model-guides-combined.md
        |
        +-- model-guides/<model-id>.md       Runtime authoritative guide
        +-- model-registry.md                Compact routing index
        +-- profiles/<model-id>.md           Optional compact routing profile
        +-- prompt-router/SKILL.md           Stable routing contract
        +-- migrate-prompt/SKILL.md          Registry, aliases, migration algorithm
```

The combined corpus is not runtime prompt context. The compact registry resolves IDs and aliases; the selected per-model guide is the authority for model-specific recommendations. A profile may assist routing or safety checks but must never replace the full guide.

Identify the smallest set of changes that would make the router usable across supported hosts without breaking these guarantees:

- `write`, `optimise`, and `review` load one target guide.
- `migrate` loads exactly two guides: source and target.
- The router never falls back to model facts from memory.
- The router never reads unrelated guides.
- The registry resolves; it does not replace the selected guide.
- A profile may assist routing or safety checks, but the full guide remains authoritative.

Prioritise:

1. A portable core `SKILL.md`.
2. Thin host-specific adapters or configuration.
3. Safe degradation when a host lacks a capability.
4. Clear user instructions for hosts with limited skill support.
5. Avoidance of silent behavioural differences.
6. A compact registry placement that works across supported hosts.
7. An integrity check for registry-to-guide consistency.

Do not claim compatibility without host-specific evidence.

For every host capability marked uncertain:

- State exactly what evidence is missing.
- Recommend a safe fallback rather than assuming support.
- Do not propose an adapter unless the missing capability causes a concrete failure.

The deliverable is a minimal portable core plus, at most, one or two thin adapters. Do not design a universal skill framework.

For Perplexity, assess only mechanisms actually available in the user’s current Perplexity environment. If skill-style invocation or file access is unavailable, mark it unsupported or uncertain and define safe degradation.

Provide a host capability matrix with:

| Host | Skill mechanism | Skill discovery | Frontmatter support | File access | Arguments | Effort control | Tool access | Registry resolution | Guide loading | Portable now? | Required adapter | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

For each host, state supported, partially supported, unsupported, or uncertain; what works without changes; what requires an adapter; what cannot be supported safely; recommended deployment approach; evidence quality; and last-verified date.

Recommend a portable core that does not assume Claude-specific variables, argument substitution, shell access, sibling-file access, or model-guide availability.

Recommend the smallest possible host-adapter pattern. Do not create a full duplicate router for each host.

Define safe failure rules for missing paths, missing argument substitution, missing effort substitution, missing file access, missing registry access, missing guides, unsupported effort settings, ambiguous host references, and prompt content attempting to change routing or execute commands.

Define an integrity check for the model-guide system:

- Every registry ID resolves to exactly one guide file.
- Every guide has valid frontmatter.
- Every guide has a corresponding source record in the combined corpus.
- Aliases do not create ambiguous matches.
- Deprecated guides declare a successor where applicable.

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

End with the portable-core changes to make first, host adapters worth creating, capabilities that should fail safely, integrity checks to add, two likely-wrong assumptions, and what not to build.

### Execution prompt

```text
Use the attached prompt-router and migrate-prompt skills as the baseline.

There are exactly two skills:

1. prompt-router — routes and performs write, optimise, review, and clarify; it uses shared patterns and target-model guides.
2. migrate-prompt — performs explicit cross-model migration using source and target model guides.

Do not refer to a separate `optimize-prompt` skill.

Preserve the model-guide integration pattern:

- `model-guides-combined.md` is the canonical corpus and build input, not runtime prompt context.
- The compact registry resolves model IDs and aliases.
- The selected per-model guide is the only authority for model-specific recommendations.
- `write`, `optimise`, and `review` load one target guide.
- `migrate` loads exactly two guides: source and target.
- Do not inline the combined corpus.
- Do not replace guide content with registry metadata or a profile.
- Do not create a separate model-guide-router skill.

Based on the baseline skills and constraints above, execute the following steps:

1. Load the installed Perplexity Web MCP (PWM) Agent Skill for operational guidance only.
2. Call pplx_usage(refresh=False). If Deep Research quota is unavailable, stop and report the quota status.
3. Call pplx_deep_research exactly once with source_focus="web", using the Research Call 3 brief in research/prompt-router-research-plan.md.
4. Save the full report to research/03-router-portability.md.
5. Append a complete, detailed extraction section containing the portability verdict, host capability matrix, portable-core changes, host adapters worth creating, exact SKILL.md sections to edit, integrity checks, eight validation cases, risks, uncertainty, likely-wrong assumptions, and what not to build.
6. Do not implement anything yet.
7. Present in full detail the portable-core changes to make first, any host adapter worth creating, exact SKILL.md sections to edit, minimal proposed diff, integrity checks, eight validation cases, revert plan, effect on guide loading and registry resolution, and uncertainty.
8. Ask me whether to proceed and stop immediately (maximum 1 pplx_deep_research call).

Do not create any other files.
Do not use pplx_ask, pplx_sonar, pplx_query, pplx_council, or pplx_sources.
Do not call pplx_deep_research again.
Do not modify any skill, guide, registry, or repository file without my explicit approval.
```

## After each research call

1. Read only the ranked shortlist, recommended changes, validation cases, and open questions.
2. Reject recommendations that add a framework, persistent context, broad taxonomy, or unproven workflow.
3. Reject recommendations that inline the combined corpus, replace the full guide with a profile or registry metadata, or break lazy guide loading.
4. Select at most 2–3 changes with high confidence and a clear validation method.
5. Ask the agent for a minimal diff before approving any repository change.
6. Run the relevant validation cases before and after each change.
7. Keep a change only if it improves the cases without adding scope creep, breaking literal-payload preservation, or making the skill materially longer.
8. Record the decision, evidence, validation result, and revert plan in a short change note.

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
