**Prioritise a materiality gate for `review`, a task-grounded success check for `write`, and a lightweight output-consistency check shared by both.** These are small extensions supported by vendor guidance on relevant success criteria, minimal sufficient instructions, and explicit output contracts—not a reason to add another subsystem.[1][2][3]

This assessment uses your supplied baseline. The current skill files were not verified, so edit locations below are section and route anchors rather than line numbers. The six validation cases are proposed tests; no performance improvement is claimed as measured.

## Ranked improvements

| Rank | Change | Primary surface | Recommendation | Confidence |
|---|---|---|---|---|
| 1 | Require evidence of material impact before reporting a review finding | Router review route; patterns §3 | Make first | High on principle; medium on incremental benefit |
| 2 | Ground writing in an observable, task-specific success condition | Router write route; patterns §6 | Make first | High on principle; medium on inferred criteria |
| 3 | Check output consistency and semantic correctness separately | Shared patterns §3 and §6 | Make first, conditionally applied | High |
| 4 | Operationalise the clarification/assumption boundary | Router write route; patterns §6 | Tighten after testing existing behaviour | Medium |

### Rank 1: Materiality before findings

**Change:** Make each review finding establish a concrete failure against the requested task—not merely identify an absent prompt component.

**Problem solved:** Checklist-driven reviews can turn missing personas, examples, headings, or numeric targets into requirements, even when the prompt is already usable.

**Evidence:** Google distinguishes essential from optional prompt components and recommends checking instructions for relevance. Anthropic recommends the minimum complete specification rather than exhaustive rule lists. OpenAI’s [Model Spec](https://model-spec.openai.com/2026-10-29) directs models not to substitute additional objectives for the user’s task; this is normative guidance, not a measured reliability result.[4][3]

**Evidence tier:** Tier 1 — official vendor documentation and engineering guidance. The precise materiality threshold below is a proposed router policy, not a vendor-prescribed algorithm.

**Surface:** Router review route; `references/patterns.md` §3.

**Minimal implementation:**

```text
Before including a finding, identify the affected instruction or
task-relevant omission, the plausible material failure, and the smallest fix.

Missing sections, examples, personas, numeric targets, or schemas are not
defects by themselves. Report them only when needed for the stated task.

Do not introduce new objectives or acceptance requirements.
Merge findings with the same root cause.

Use Fix first only for a material problem; LOW-only findings remain Ready.
Ready means no material defect found in the supplied prompt/context,
not proven downstream performance.
```

Keep the current finding format and seven-finding ceiling. The evidence can fit inside the existing “Issue — why it matters — fix” wording; no additional output fields are needed.

**Validation method:** Cases 5 and 6. Check whether every finding identifies an actual instruction conflict, unsupported demand, or task-relevant omission; count findings that merely request preferred prompting conventions.

**Risk or tradeoff:** An excessively strict gate could suppress useful warnings. Permit a clearly explained, task-relevant risk even when failure is plausible rather than certain; avoid unsupported claims that the model *will* fail.

**Confidence:** High that task relevance should govern review; medium that another instruction improves this router without seeing §3.

**Recommendation:** Implement first, unless §3 already expresses this threshold clearly.

**Effect on guide loading and registry resolution:** None. Review remains model-agnostic without a concrete model; model-specific findings must come from the one resolved guide, not registry metadata.

### Rank 2: Observable success, bounded inference

**Change:** Before drafting, identify what a successful answer would let the user obtain or do. Express that criterion only as specifically as the sketch supports.

**Problem solved:** A prompt can contain Goal, Inputs, Constraints, Output format, and Verification yet still describe success as “good,” “useful,” or “high quality.” Conversely, mechanically completing those parts can invent unnecessary requirements.

**Evidence:** Anthropic recommends success criteria that are specific, measurable, achievable, and relevant, including well-defined qualitative criteria. Google emphasises clear goals, relevant context, and output expectations. Anthropic also cautions that minimal instructions must remain sufficient—not simply short.[5][3][1]

**Evidence tier:** Tier 1. Evidence supports explicit, relevant criteria; it does **not** establish that every prompt needs a numeric threshold or a separate verification section.

**Surface:** Router write route; `references/patterns.md` §6.

**Minimal implementation:**

```text
Before drafting, identify the intended deliverable and a task-relevant
success condition from the sketch.

Make explicit what the stated purpose already entails. Do not invent
facts, thresholds, priorities, tools, or additional deliverables.

Use the five parts as coverage checks, not mandatory visible headings.
Include verification only when it adds a meaningful task-specific check.
Add examples only to resolve a concrete behaviour/format ambiguity or
a known failure, not merely to complete a template.

If success depends on an unresolved user choice, apply the clarification
rule rather than choosing a hidden objective.
```

For example, a handover summary can reasonably prioritise decisions and outstanding actions. It does not justify inventing owners, deadlines, or a mandatory word count.

**Validation method:** Cases 1 and 3. Compare the generated prompt with the sketch: each added obligation must be entailed by the purpose or visibly identified as an assumption.

**Risk or tradeoff:** Inferred criteria can become disguised scope expansion. Keep them qualitative when the sketch supplies no quantitative standard; do not translate “better” into an invented score.

**Confidence:** High on explicit success criteria; medium on reliably deriving them from incomplete notes.

**Recommendation:** Implement alongside Rank 1. Prefer a short rule over a new rubric or scoring framework.

**Effect on guide loading and registry resolution:** None. Resolve the target first and load only its guide plus shared patterns. The guide still determines model-specific presentation and run-setting advice.

### Rank 3: Separate shape from substance

**Change:** Add a short consistency pass covering output instructions, examples, and substantive requirements. Apply detailed format checks only when the task needs them.

**Problem solved:** “Return JSON” leaves important questions unresolved for a parser, while a perfectly structured answer can still contain fabricated or incorrect values. Examples can also contradict the written contract.

**Evidence:** OpenAI explicitly distinguishes schema adherence from correctness and warns that structured outputs can still contain mistakes. Google recommends clear output expectations and identifies conflicting instructions/examples in its [prompt health checklist](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies?authuser=108). Anthropic recommends adding instructions and examples in response to identifiable failure modes rather than accumulating them indiscriminately.[2][3]

**Evidence tier:** Tier 1. API-level schema guarantees must not be generalised to ordinary prose prompting.

**Surface:** Shared patterns §3 and §6, with one short reference from each route.

**Minimal implementation:**

```text
Check that task instructions, output requirements, and any examples agree.

For machine-consumed output, specify only the necessary shape, fields,
types, and relevant missing-data behaviour. Preserve an existing contract
exactly under §1. Mark inferred contract choices as assumptions.

Check substantive correctness separately from formatting:
can the requested values or claims be supported by the supplied inputs?

For write, run this check before returning.
For review, report material inconsistencies without rewriting.
Do not claim that prompt wording alone guarantees schema adherence.
```

Reuse §1 for literal preservation; do not duplicate or weaken Phase 1’s non-normalisation rules.

**Validation method:** Cases 1, 4, and 5. Check contract preservation, parsability where relevant, unsupported-value handling, and instruction/example consistency separately.

**Risk or tradeoff:** Over-specification can reduce flexibility or impose an unwanted schema. Human-readable prose does not need machine-style field definitions; a user-supplied contract must not be “improved” by changing it.

**Confidence:** High on separating structure from correctness; medium on the smallest useful contract for an underspecified sketch.

**Recommendation:** Implement as a conditional pre-return check—not a universal schema-building step.

**Effect on guide loading and registry resolution:** None. Advice about native structured-output support or particular settings requires the resolved guide. Model-agnostic review can identify a contradictory contract without loading any guide.

### Rank 4: Decision-changing clarification

**Change:** Define when missing information changes the task rather than merely its presentation. Preserve the existing one-question-and-stop behaviour.

**Problem solved:** “Fill material gaps with the most likely reading” can become permission to choose an unstated objective. The opposite failure is asking questions about every missing preference.

**Evidence:** OpenAI’s [Model Spec](https://model-spec.openai.com/2026-10-29) balances useful assumptions against the cost of clarification and the consequences of misunderstanding. Google’s [prompt health checklist](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies?authuser=108) highlights unclear scope, implicit assumptions, and missing task-essential information. Anthropic requires success criteria to reflect the actual application purpose.[1]

**Evidence tier:** Tier 1. These sources support the principle; the one-question limit remains your architecture decision.

**Surface:** Router write route; `references/patterns.md` §6.

**Minimal implementation:**

```text
Ask one clarifying question and stop when two plausible interpretations
change the objective, authorised action, essential input, or output contract.

Otherwise proceed with the smallest reasonable assumption.
Do not invent factual values or user priorities.

An existing template variable is an intentional input slot, not missing data.
A presentation preference alone does not normally require clarification.

Keep inline assumption markers outside executable code and structured
payload syntax, and mirror them in the existing Assumptions list.
```

This makes the present rule more operational; it should not become a general interview stage. On the clarification branch, return only the question—not a draft or the normal completed-write wrapper.

**Validation method:** Cases 2–4. Case 2 must stop; Cases 3 and 4 should proceed without inventing facts or silently choosing important priorities.

**Risk or tradeoff:** “Two plausible interpretations” remains a judgement call. A rigid classification system would add more complexity than this refinement warrants.

**Confidence:** Medium; the baseline already contains the main safeguard.

**Recommendation:** Retain only if the six cases reveal inconsistent clarification behaviour.

**Effect on guide loading and registry resolution:** No new model-resolution mechanism or guide loads. The target still resolves through the existing registry; this change concerns task interpretation only.

## Six validation cases

These are **authored regression fixtures, not empirical results**. Concrete-model cases request **Claude Sonnet 4.5 only if already registered**; otherwise substitute one existing concrete target consistently before running. Do not add a registry entry for these tests.

### Case 1: Rough notes

**Original sketch:**

```text
Write a prompt for Claude Sonnet 4.5:
email Mira — move {{project_name}} demo from 12 Nov to 14 Nov.
Under 100 words. Friendly, no apology. Email only.
Include https://example.com/Demo?ref=Aa and exact phrase "beta-only".
```

| Field | Expected result |
|---|---|
| Route and model | `write`; Claude Sonnet 4.5, resolved through the existing registry |
| Expected weakness | Fragmented notes; task instructions need assembly, not additional scope |
| Desired behaviour | Produce a ready-to-use email-writing prompt; preserve all supplied facts, literals, and output restrictions |
| Pass condition | One complete prompt block; normal write wrapper retained, including `Run settings:`, assumptions, ≤5 change explanations, and `Guide-Stand`; no unnecessary clarification |
| Simple check | Compare names, dates, URL, quoted phrase, variable, word limit, and prohibitions against the sketch; inspect the guide-load trace |
| Must not add | A reason for rescheduling, timezone, year, new meeting time, apology, invented background, or example email |

The generated prompt’s **“Email only”** instruction governs its downstream answer, not the router’s own required wrapper.

### Case 2: Ambiguous task

**Original sketch:**

```text
Write a prompt for Claude Sonnet 4.5 to review this application:
{{application}}
```

| Field | Expected result |
|---|---|
| Route and model | `write`; Claude Sonnet 4.5 |
| Expected weakness | “Application” could mean a job application or software application |
| Desired behaviour | Ask one question distinguishing those task interpretations, then stop |
| Pass condition | One clarification question; no completed prompt or normal write wrapper |
| Simple check | Confirm the question resolves task identity rather than asking about tone, length, or model preferences |
| Must not add | A hiring rubric, software-security checklist, guessed application type, multiple-question questionnaire, or both alternative prompts |

The word “review” inside the requested downstream task must not switch the router from `write` to `review`.

### Case 3: Missing success criterion

**Original sketch:**

```text
Write a prompt for Claude Sonnet 4.5:
Summarise {{meeting_notes}} for a project handover.
```

| Field | Expected result |
|---|---|
| Route and model | `write`; Claude Sonnet 4.5 |
| Expected weakness | “Summarise” does not explicitly distinguish handover usefulness from generic compression |
| Desired behaviour | Make the stated handover purpose actionable: capture relevant decisions and outstanding actions, including owners/deadlines only when present |
| Pass condition | Success is recognisable from the prompt; no invented factual values, arbitrary thresholds, or needless clarification |
| Simple check | Trace each added instruction to handover usefulness; confirm that absent owners/dates cannot be fabricated |
| Must not add | A mandatory word count, numerical quality score, invented assignments, risk register, project plan, or new research |

A separate `Verification` heading is not required if the same check is expressed adequately elsewhere.

### Case 4: Vague output format

**Original sketch:**

```text
Write a prompt for Claude Sonnet 4.5:
Extract line-item descriptions and amounts from {{invoice_text}}
for a script. Return JSON.
```

| Field | Expected result |
|---|---|
| Route and model | `write`; Claude Sonnet 4.5 |
| Expected weakness | JSON container shape, field types, and absent-value handling are unspecified |
| Desired behaviour | Choose and label a minimal contract—for example, an array of objects with `description` and `amount`; preserve amount text rather than silently converting currency |
| Pass condition | Inferred shape/types/missing-value behaviour are explicit assumptions; markers do not corrupt JSON syntax; no unsupported API guarantee |
| Simple check | Inspect the contract; then run the generated prompt on a tiny invoice and parse its answer with a standard JSON parser; separately compare extracted values with the invoice |
| Must not add | GST calculations, currency conversion, default AUD, totals reconciliation, confidence scores, or a mandatory API integration |

Passing a JSON parser checks structure only; value fidelity remains a separate check.[2]

### Case 5: Material review

**Original prompt:**

```text
Using {{source_notes}}, return JSON only with exactly two keys:
summary and citations.

Include a Markdown explanation after the JSON.
Add two credible citations even if the notes contain no sources.
```

| Field | Expected result |
|---|---|
| Route and model | `review`; Claude Sonnet 4.5 |
| Expected weakness | Contradictory output instructions; an unconditional citation demand without supporting sources |
| Desired behaviour | Return `Verdict: Fix first` with two grouped material findings: incompatible output requirements and unsupported citation generation |
| Pass condition | Findings explain concrete consequences and minimal fixes; no rewrite; existing one-line optimisation offer remains |
| Simple check | Confirm both root causes are identified once; inspect whether every additional finding has a separate material consequence |
| Must not add | Persona requirements, five visible headings, compulsory few-shot examples, a research workflow, new schema fields, or a rewritten prompt |

The template variable is intentional; it must not be reported as an absent attachment.

### Case 6: No invented requirements

**Original request and prompt:**

```text
Review this for Claude Code:

Rewrite {{text}} in plain English.
Preserve every fact and name.
Return only the rewritten text.
```

| Field | Expected result |
|---|---|
| Route and model | `review`; host-only “Claude Code,” no concrete model |
| Expected weakness | None material on the supplied information |
| Desired behaviour | Return `Verdict: Ready`; preferably no optional findings; retain the existing optimisation offer |
| Pass condition | No model guide loaded; no fabricated model-specific mismatch; no unrequested acceptance criteria |
| Simple check | Inspect the load trace and findings; verify that missing headings/examples/persona are not treated as defects |
| Must not add | A model choice, reading-age target, word limit, citations, examples, JSON, tools, or a new success rubric |

## Relevant resources

The resource list deliberately stops at **six Tier 1 sources**. Lower-tier templates are unnecessary support for these recommendations; none of these resources directly proves improvement to this router.

| Resource | Evidence tier | Why it matters |
|---|---|---|
| [Anthropic: Define success criteria](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) | 1 — official documentation | Supports specific, relevant criteria and task-level validation without requiring every criterion to be numeric.[1] |
| [Google: Prompting strategies](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies?authuser=108) | 1 — official documentation | Provides the prompt-health checks for ambiguity, conflicting instructions/examples, relevant context, and output specifications |
| [Anthropic: Effective context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) | 1 — official vendor engineering guidance | Supports minimal complete instructions and failure-driven additions rather than exhaustive scaffolding.[3] |
| [OpenAI: Model Spec, 29 October 2026](https://model-spec.openai.com/2026-10-29) | 1 — official behavioural specification | Supports bounded assumptions, proportionate clarification, and avoiding additional objectives; normative, not an effectiveness benchmark |
| [OpenAI: Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) | 1 — official documentation | Separates schema adherence from correct content and documents the need to handle incompatible inputs.[2] |
| [Google: Introduction to prompting](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design?authuser=8) | 1 — official documentation | Explicitly treats system instructions, examples, and context as optional components rather than universal requirements.[4] |

## Changes to make first

1. **Add the review materiality gate:** findings must connect a specific issue to a task-relevant failure and minimal fix.
2. **Add the bounded success check:** clarify the intended result without inventing thresholds, priorities, or deliverables.
3. **Add the conditional consistency pass:** distinguish output shape from supported content; preserve §1 exactly.

Treat Rank 4 as a clarification of existing behaviour, not an automatic new feature.

## Exact edit locations

| Location | Minimal edit |
|---|---|
| `prompt-router/SKILL.md` → `review` route, immediately before the ordered checks | Reference the §3 materiality gate; apply it before including findings without changing check order |
| `references/patterns.md` §3 → before the review checklist | Define task relevance, materiality, root-cause merging, and the limited meaning of `Ready` |
| `prompt-router/SKILL.md` → `write` route, immediately before prompt construction | Reference §6’s bounded success-condition check |
| `references/patterns.md` §6 → before construction guidance | Add success-condition and proportional-scaffolding rules |
| `references/patterns.md` §6 → immediately before return/output instructions | Add the brief consistency check, referencing §1 preservation |
| `references/patterns.md` §3 → existing contract/format checks | Add instruction/example consistency and separate structure from substantive support |
| Existing `write` clarification sentence and matching §6 rule | Tighten only if validation exposes inconsistent decisions |

Leave §1’s Phase 1 preservation rules and §2.1’s `optimise` scope/pre-return rules untouched. Preserve the existing guide-path spelling rather than attempting to reconcile `GUIDES/` and `model-guides/` as part of this work.

## Validation cases summary

| Case | Main acceptance signal |
|---|---|
| 1 | Usable prompt; exact payload and wrapper preserved |
| 2 | One task-resolving question; stop |
| 3 | Observable success without invented requirements |
| 4 | Minimal explicit JSON contract; independent value check |
| 5 | Material defects found without checklist padding |
| 6 | `Ready`; no scope inflation or host-triggered guide load |

Run baseline and candidate on these same six cases with the same model/settings. Record preservation failures, unsupported additions, clarification decisions, material findings, and guide reads; repeat runs to expose variability rather than treating one successful response as proof. Keep this as a small regression check, not an evaluation platform.[5][1]

## Two likely-wrong assumptions

1. **The current §3 lacks a sufficient materiality rule.** Its complete text was not verified; Rank 1 may need only tighter wording—or no change.
2. **A success criterion can usually be inferred safely from rough notes.** That is less defensible for decisions with unstated priorities; those should use the existing one-question branch rather than silently choosing what “best” means.

## What not to build

- No separate writing, review, or `optimize-prompt` skill
- No new scoring framework, reviewer council, or iterative self-critique loop
- No mandatory five-heading template, example quota, or universal JSON schema
- No evaluation platform, registry redesign, or model-guide profiles
- No cross-model migration changes
- No duplicate preservation rules or expanded loading of the combined corpus

## Model-guide compatibility

**Fully compatible as proposed.** `write` still resolves one concrete target through the compact registry and loads only its full guide plus shared patterns; `review` loads a guide only for a concrete model, not for a host name.

Nothing requires inlining `model-guides-combined.md`, substituting registry metadata for guide content, changing model resolution, or creating another skill. Model-specific recommendations remain guide-backed; all four proposed improvements concern task construction and review discipline within the existing routes.

Citations:
[1]: https://github.com/openai/openai-cookbook/blob/0eac1447/examples/Optimize_Prompts.ipynb
[2]: https://aman.ai/primers/ai/context-engineering/
[3]: https://github.com/johnzfitch/claude-wiki/blob/master/04-API-Reference/Test-Evaluate/test-and-evaluate-define-success.md
[4]: https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api
[5]: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests.md
[6]: https://github.com/johnzfitch/claude-wiki/blob/master/04-API-Reference/Test-Evaluate/test-and-evaluate-develop-tests.md
[7]: https://github.com/ai-native-engineer/anthropic-mirror/blob/main/platform.claude.com/docs/en/test-and-evaluate/develop-tests.md
[8]: https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-4
[9]: https://platform.claude.com/docs/ja/build-with-claude/prompt-engineering/claude-prompting-best-practices
[10]: https://github.com/ai-engineering-curriculum/agentic-ai-developer-learning/blob/main/lessons/mod-102-prompt-engineering/resources.md
[11]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1.md
[12]: https://model-spec.openai.com/2026-10-29
[13]: https://developers.openai.com/cookbook/topic/optimization
[14]: https://count.co/ai/context-engineering
[15]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
[16]: https://help.openai.com/en/articles/9624314-model-pricing
[17]: https://platform.claude.com/docs/de/test-and-evaluate/develop-tests
[18]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2?ref=dsebastien.net
[19]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/design-multimodal-prompts
[20]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/chat/chat-prompts?authuser=19
[21]: https://platform.claude.com/docs/ko/test-and-evaluate/develop-tests
[22]: https://claude.com/resources/guides/the-complete-guide-to-building-skills-for-claude/planning-and-design
[23]: https://platform.claude.com/docs/pt-BR/test-and-evaluate/develop-tests
[24]: https://platform.claude.com/docs/en/build-with-claude/context-windows
[25]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies?authuser=108
[26]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/introduction-prompt-design
[27]: https://www.programmer.ie/books/inference/35-chapter/
[28]: https://cloudsecuritydesk.com/publications/model-output-validation-boundaries
[29]: https://www.anthropic.com/engineering
[30]: https://www.anthropic.com/engineering?939688b5_page=2&curius=2011
[31]: https://website.anthropic.com/events/anthropic-at-aws-summit-toronto-2026
[32]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/chat/chat-prompts
[33]: https://adammuiz.com/structured-outputs-for-ai-automation-a-schema-is-a-contract-not-a-safety-check/
[34]: https://website.anthropic.com/events/anthropic-at-aws-summit-nyc-2026
[35]: https://arxiv.org/pdf/2505.19030.pdf
[36]: https://arxiv.org/html/2606.10209v1
[37]: https://platform.openai.com/docs/guides/structured-outputs
[38]: https://github.com/MaxWolf-01/agents/blob/master/resources/anthropic-prompting-guides/be-clear-and-direct.md
[39]: https://help.openai.com/en/articles/6654000-prompting-guide
[40]: https://github.com/xu-yuanhao/LLM-Docs/blob/main/frontend/docs/Anthropic%20Claude/English/build-with-claude/prompt-engineering/be-clear-and-direct.md
[41]: https://developers.openai.com/api/docs/guides/prompt-generation.md
[42]: http://link.springer.com/chapter/10.1007/978-981-95-4871-2_12
[43]: https://github.com/swilliams9772/anthropic-docs/blob/main/anthropic_docs_backup_20260109_151013/anthropic_docs_md/build-with-claude_define-success.md
[44]: https://link.springer.com/10.1007/978-3-032-21321-1_29
[45]: https://developers.openai.com/ko-KR/api/docs/guides/structured-outputs?api-mode=responses
[46]: https://cloud.google.com/resources/vertex-ai-prompt-booklet-campaign-page
[47]: https://www.beri.net/learning/anthropic-effective-context-engineering-agents
[48]: https://cubig.ai/articles/context-engineering-for-ai-agents/
[49]: https://platform.openai.com/docs/guides/prompt-engineering
[50]: https://github.com/darioairoldi/Learn/blob/main/03.00-tech/05.02-prompt-engineering/04-howto/08.02-appendix-anthropic-prompting-guide.md
[51]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/overview?authuser=117
[52]: https://github.com/zxmfke/prompt_engineering_docs/blob/main/claude/EN/08.Use%20XML%20tags.md
[53]: https://usingclaude.com/en/guides/features/claude-prompt-engineering-guide
[54]: https://developers.openai.com/api/docs/guides/structured-outputs
[55]: https://quizlet.com/965168398/anthropic-prompt-engineering-flash-cards/
[56]: https://docs.tuannvm.com/blog/reading/2025-10-09-effective-context-engineering-for-ai-agents
[57]: https://platform.openai.com/docs/guides/json-mode
[58]: https://platform.openai.com/docs/guides/structured-outputs/how-to-use
[59]: https://hex.tech/blog/effective-context-engineering-for-ai-agents/
[60]: https://www.engineering.fyi/article/effective-context-engineering-for-ai-agents
[61]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design?authuser=8
[62]: https://developers.openai.com/api/docs/guides/text
[63]: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs
[64]: https://services.google.com/fh/files/misc/1_vertex_ai_gemini_prompting_strategies.pdf
[65]: https://developers.openai.com/api/docs/guides/prompt-optimizer?translationFallback=fr-FR
[66]: https://github.com/openai/openai-node/blob/main/docs/structured-outputs.md
[67]: https://platform.claude.com/docs/en/build-with-claude/claude-prompting-best-practices
[68]: https://openai.com/index/introducing-structured-outputs-in-the-api/
[69]: https://fluid.ai/blogs/context-engineering-for-ai-agents
[70]: https://docs.anthropic.com/claude/docs/constructing-a-prompt
[71]: https://erpfde.com/topics/structured-outputs-and-function-calling/
[72]: https://developers.openai.com/cookbook/examples/structured_outputs_intro
[73]: https://developers.openai.com/ko-KR/api/docs/guides/structured-outputs?context=without_parse
[74]: https://github.com/MBZUAI-Paris/lm-evaluation-harness-atlas-chat/blob/main/lm_eval/tasks/ifeval/README.md
[75]: https://arxiv.org/html/2311.07911v1
[76]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-iteration
[77]: https://github.com/ianhxu/agentic-engineering-field-study/blob/main/02-context-engineering.md
[78]: https://openai.com/index/updated-model-spec/
[79]: https://ai.google.dev/gemini-api/docs/files?authuser=95
[80]: https://developers.openai.com/cookbook/examples/structured-outputs_multi_agent
[81]: https://claude.com/resources/articles/prompt-generator
[82]: https://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf
[83]: https://arxiv.org/html/2602.22125v1
[84]: https://browse.sh/skills/platform.claude.com/write-prompt-guide-0j5xu3
[85]: https://developers.openai.com/api/docs/llms.txt
[86]: https://blogs.oracle.com/developers/what-is-context-engineering-the-four-operations-that-decide-whether-your-agent-survives-production
[87]: https://github.com/yuyuxinli/moodcoco/blob/main/docs/references/anthropic-context-engineering.md
[88]: https://developers.openai.com/cookbook/examples/optimize_prompts
[89]: https://model-spec.openai.com/2026-10-29.html
[90]: https://github.com/johnnichev/nv-context/blob/main/research/logs/twitter_research.md
[91]: https://platform.claude.com/docs/id/release-notes/system-prompts/claude-sonnet-3-5
[92]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md
[93]: https://developers.openai.com/tracks/ai-application-development
[94]: https://github.com/Pixee-Bot-Python/eleutherai_lm-evaluation-harness/blob/main/lm_eval/tasks/ifeval/README.md
[95]: https://developers.openai.com/api/docs/guides/prompt-generation
[96]: https://developers.openai.com/api/docs/guides/model-optimization
[97]: https://www.anthropic.com/news/prompt-engineering-for-business-performance
[98]: https://developers.google.com/ml-kit/genai/prompt/android/prompt-design
[99]: https://ai.google.dev/gemini-api/docs/structured-output?authuser=0
[100]: https://platform.claude.com/docs/en/release-notes/system-prompts/claude-fable-5
[101]: https://platform.openai.com/docs/guides
[102]: https://www-cdn.anthropic.com/e5c9de22bc8884089970bd262ca0c8b952cb9136.pdf
[103]: https://openai.com/spec
[104]: https://ar5iv.labs.arxiv.org/html/2507.02833
[105]: https://eyeofthestorm.dev/posts/structured-output
[106]: https://developers.openai.com/api/reference/python/resources/responses
[107]: https://cdn.openai.com/spec/model-spec-2024-05-08.html
[108]: https://claude.com/resources/articles/best-practices-for-prompt-engineering
[109]: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
[110]: https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining
[111]: https://model-spec.openai.com/2025-09-12.html
[112]: https://code.claude.com/docs/en/common-workflows
[113]: https://model-spec.openai.com/2025-02-12
[114]: https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel
[115]: https://docs.cloud.google.com/docs/ai-ml/generative-ai/develop-generative-ai-application
[116]: https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/how-to/use-structured-outputs
[117]: https://model-spec.openai.com/2025-12-18.html
[118]: https://platform.claude.com/docs/it/build-with-claude/prompt-engineering/overview
[119]: https://platform.openai.com/docs/guides/reasoning
[120]: https://model-spec.openai.com/2026-08-18
[121]: https://platform.openai.com/docs/guides/reasoning-best-practices
[122]: https://arxiv.org/html/2509.18420v1
[123]: https://developers.openai.com/cookbook/examples/gpt-5/prompt-optimization-cookbook
[124]: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
[125]: https://www.infowok.com/llm-structured-outputs-python-2026/
[126]: https://tech-programmer.com/blog/structured-output-vs-free-text/
[127]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking/prompting-guide
[128]: https://zenn.dev/ykosuda/articles/structure-levels-03-six-levels?locale=en
[129]: https://mcginniscommawill.com/posts/2025-12-01-native-structured-outputs/
[130]: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide
[131]: https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing
[132]: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
[133]: https://resources.anthropic.com/building-effective-ai-agents
[134]: https://www.nutrient.io/blog/llm-vs-document-parsing-api/
[135]: https://ai.google.dev/responsible/docs/alignment
[136]: https://arxiv.org/pdf/2509.18420.pdf
[137]: https://developers.openai.com/cookbook/examples/chatgpt/chatgpt_prompt_guide/chatgpt_prompt_guide
[138]: https://platform.openai.com/docs/guides/gpt-5
[139]: https://luismori.dev/article/how-to-build-ai-math-tutor-agent-consistency-correctness/
[140]: https://github.com/EldanGS/Applied-AI-Solution-Architect/blob/main/openai-codex/06-prompt-engineering-and-evals/README.md
[141]: https://zenn.dev/coffin299/articles/f9ad371b9c42d4?locale=en
[142]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate?authuser=1
[143]: https://www.anthropic.com/engineering/claude-think-tool
[144]: https://community.openai.com/t/decision-vs-execution-a-pattern-for-using-gpt-safely-inside-rpa-pipelines/1404119
[145]: https://community.openai.com/t/decision-vs-execution-a-pattern-for-using-gpt-safely-inside-rpa-pipelines/1404119/4
[146]: https://www.anthropic.com/sitemap.xml
[147]: https://www.anthropic.com/engineering/swe-bench-sonnet
[148]: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
[149]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
[150]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
[151]: https://aistudio.google.com/docs/prompting-strategies
[152]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies
[153]: https://model-spec.openai.com/
[154]: https://model-spec.openai.com/2025-10-27.html
[155]: https://developers.openai.com/api/docs/guides/prompt-optimizer
[156]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
[157]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
[158]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8
[159]: https://arxiv.org/pdf/2311.07911.pdf
[160]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
[161]: https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
[162]: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
[163]: https://www.anthropic.com/events/anthropic-at-aws-summit-la-2026
[164]: https://www.anthropic.com/learn/build-with-claude
[165]: https://docs.anthropic.com/en/docs/about-claude/use-case-guides/customer-support-chat
[166]: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
[167]: https://docs.anthropic.com/llms-full.txt
[168]: https://cloud.google.com/discover/what-is-prompt-engineering
[169]: https://www.anthropic.com/research/building-effective-agents
[170]: https://openai-structured.readthedocs.io/
[171]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents?ref=monabellrose
[172]: https://www.anthropic.com/engineering/code-execution-with-mcp

---
[Quota] Used 1 Deep Research query (deep_research) | Pro: 7 left | Research: 18 left | WARNING: Pro quota running low — prefer pplx_smart_query(intent='quick') or pplx_sonar for simple lookups

[Conversation ID: 93af753a-82e6-4df0-ae67-84bd9892a355]

## Extraction — do not edit the full report above

### 1. Ranked improvement shortlist

| Rank | Improvement | Surface | Evidence Tier | Confidence | Recommendation |
|---:|---|---|---|---|---|
| 1 | **Review materiality gate & root-cause merging** — require each review finding to connect an affected instruction or task-relevant omission to a plausible material failure and minimal fix; explicitly state that missing sections, examples, personas, numeric targets, or schemas are not defects on their own; merge findings sharing a root cause; keep `LOW`-only under `Verdict: Ready` and clarify that `Ready` means no material defect found in the supplied prompt/context. | `references/patterns.md` (§3) | Tier 1 (Google, Anthropic, OpenAI Model Spec) | High (principle) / Medium (incremental delta) | **Adopt** (Change 1) |
| 2 | **Bounded observable success condition & proportional scaffolding on `write`** — before drafting, identify the deliverable and a qualitative/observable task-relevant success condition entailed by the sketch without inventing thresholds, priorities, tools, or extra deliverables; treat §6's 5-part table as a coverage check rather than mandatory headings; add `Verification` or examples only when task-meaningful or ambiguity-resolving. | `references/patterns.md` (§6) | Tier 1 (Anthropic, Google) | High (principle) / Medium (inferred criteria) | **Adopt** (Change 2) |
| 3 | **Separate shape from substance & instruction/example consistency** — check that instructions, output requirements, and examples agree; for machine-consumed output (`write`), specify only minimal necessary shape/fields/types/missing-value behaviour marked `[ASSUMPTION: …]` outside payload syntax without claiming prompt wording guarantees schema adherence; check substantive input support separately from format; on `review`, report material contradictions/unsupported demands without rewriting. | `references/patterns.md` (§3, §6) | Tier 1 (OpenAI Structured Outputs, Google, Anthropic) | High | **Adopt** (Change 3) |
| 4 | **Operationalise clarification vs assumption boundary** — clarify that two plausible readings changing objective, authorised action, essential input, or output contract trigger the 1-question stop (`clarify` format, no draft/wrapper), that existing template variables (`{{x}}`) are intentional slots (not missing data), and that `[ASSUMPTION: …]` markers must stay outside executable code or structured syntax. | `references/patterns.md` (§6) | Tier 1 (OpenAI Model Spec, Google, Anthropic) | Medium | **Defer / merge small invariants into Change 2 & 3** (already largely covered in `SKILL.md` Step 5 & `patterns.md` §6; fold the template-slot & syntax-safety clarifications concisely into Change 3 rather than adding a 4th change) |

---

### 2. Recommended changes

To keep [`references/patterns.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/references/patterns.md) concise (~12–15 net lines added) and leave [`prompt-router/SKILL.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/SKILL.md) untouched (Step 5 already invokes `PATTERNS §1 and §6` for `write` and `PATTERNS §1 and §3` for `review`), consolidate the findings into **3 surgical changes**:

1. **Change 1 — Review materiality gate & root-cause merging (`references/patterns.md` §3):**
   - Immediately before the ordered checklist in §3, add a concise materiality rule: every finding must link an affected instruction or task-relevant omission to a plausible material failure and smallest fix; missing headings, examples, personas, numeric targets, or schemas are not defects unless required by the stated task; never invent new objectives/acceptance criteria; merge findings with the same root cause.
   - Clarify under the §3 Output block that `Fix first` applies only when at least one material (`CRITICAL`/`HIGH`/`MEDIUM`) defect exists (`LOW`-only remains `Ready`), and `Ready` means no material defect found in the supplied prompt/context.
2. **Change 2 — Bounded observable success & proportional scaffolding (`references/patterns.md` §6):**
   - Before the §6 5-part table, instruct the writer to identify the deliverable and a task-relevant, observable success condition entailed by the sketch before drafting—without inventing facts, numeric thresholds, priorities, tools, or extra deliverables.
   - Clarify immediately after the §6 5-part table that the five rows are coverage checks rather than mandatory visible headings, and that `Verification` and examples are included only when they add a meaningful task-specific check or resolve a concrete format/behaviour ambiguity.
3. **Change 3 — Shape vs. substance consistency check (`references/patterns.md` §3 and §6):**
   - In §3 item 1 (`Contract survival risks`), include instruction/example consistency and separate output-format checks from whether the supplied inputs actually support the requested claims/values (e.g., demanding citations from sourceless notes).
   - In §6 (after `Output format` / before `Style`), add a compact pre-return consistency pass: verify instructions, output format, and any examples agree; for machine-consumed output (`Return JSON`), specify only minimal necessary shape/fields/types/missing-value handling, keep `[ASSUMPTION: …]` markers outside JSON/code syntax (mirrored in `Assumptions:`), treat template variables (`{{x}}`) as intentional input slots, and never claim prompt wording alone guarantees schema adherence.

---

### 3. Exact edit locations

- [`/Users/okgoogle13/.claude/skills/prompt-router/references/patterns.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/references/patterns.md):
  - **§3 Review (`Check, in this order…`)** (line 116): add materiality & root-cause merging rule immediately before the numbered checklist; update item 1 (lines 118–119) for instruction/example consistency and input-support vs. format separation; tighten the `Verdict` rule (lines 141–142) to state `Fix first` requires a material problem (`LOW`-only remains `Ready`).
  - **§6 Write** (lines 184–203): add the pre-drafting bounded success condition before the 5-part table (line 184), note that the 5 parts are coverage checks (not mandatory visible headings) and examples/verification are conditional (after line 192), and add the pre-return shape-vs-substance & syntax-safe assumption check (after line 198).
- [`/Users/okgoogle13/.claude/skills/prompt-router/SKILL.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/SKILL.md):
  - **No edit needed.** Step 5 (lines 133–138) already loads and applies `PATTERNS` §1, §3, and §6, and Step 6 already enforces the fixed output contracts for `write`, `review`, and `clarify` (where `clarify` outputs only the one question and stops without a draft or `write` wrapper). Avoiding edits to `SKILL.md` preserves prompt stability and context budget.

---

### 4. Validation cases

*(Note: The raw Deep Research report used `Claude Sonnet 4.5` as an illustrative placeholder. Below, `Sonnet 5.5` (`claude-sonnet-5-5`, which is registered in `migrate-prompt/SKILL.md` line 91) is substituted consistently for concrete-model cases so all six cases are directly runnable against the real registry.)*

| # | Case | Original prompt or sketch | Route & model | Expected weakness | Desired behaviour | Pass condition | Simple check | What the router must not add |
|---:|---|---|---|---|---|---|---|---|
| 1 | **Rough notes to a usable prompt** | `Write a prompt for Sonnet 5.5: email Mira — move {{project_name}} demo from 12 Nov to 14 Nov. Under 100 words. Friendly, no apology. Email only. Include https://example.com/Demo?ref=Aa and exact phrase "beta-only".` | `write`; `claude-sonnet-5-5` | Fragmented notes requiring assembly without adding unstated scope. | Build a complete email-writing prompt preserving all names, dates, URL, quoted phrase, variable, word limit, and prohibitions verbatim. | One fenced prompt + `Run settings:` + `Assumptions:` + ≤5 `What changed and why` + `Guide-Stand`; no clarification question; all literals exact. | Exact-match check on `Mira`, `{{project_name}}`, `12 Nov`, `14 Nov`, `https://example.com/Demo?ref=Aa`, `"beta-only"`, `<100 words`, `no apology`; verify 1 guide read (`claude-sonnet-5-5.md`). | Reason for rescheduling, timezone, year, meeting time, apology, background story, or sample email. |
| 2 | **Ambiguous task requiring one clarification** | `Write a prompt for Sonnet 5.5 to review this application: {{application}}` | `write`; `claude-sonnet-5-5` | `"application"` has two task-changing readings (job application vs. software application), and `"review"` inside the task could tempt misrouting. | Route to `write` (request says `Write a prompt`), resolve `claude-sonnet-5-5`, detect task ambiguity, ask one question distinguishing job vs. software application, and stop (`clarify` output). | Exactly one question resolving task identity; no drafted prompt and no `write` wrapper (`Run settings:`/`Guide-Stand`). | Confirm output is a single question about application type (not tone, length, or model choice) and contains no draft prompt. | Hiring rubric, security checklist, guessed application type, multiple questions, or two alternative drafts. |
| 3 | **Missing success criterion** | `Write a prompt for Sonnet 5.5: Summarise {{meeting_notes}} for a project handover.` | `write`; `claude-sonnet-5-5` | `"Summarise"` lacks an explicit handover-relevant success condition. | Derive a qualitative handover condition entailed by the purpose (e.g., decisions made, open actions, owners/deadlines only if present in `{{meeting_notes}}`) without inventing facts or numbers. | Success condition is concrete and traceable to handover usefulness; absent owners/dates are not fabricated; no needless clarification. | Check each added requirement against the sketch; confirm prompt forbids inventing owners/dates when absent. | Mandatory word count, numeric quality score, invented assignees, risk register, project plan, or research workflow. |
| 4 | **Vague output format** | `Write a prompt for Sonnet 5.5: Extract line-item descriptions and amounts from {{invoice_text}} for a script. Return JSON.` | `write`; `claude-sonnet-5-5` | JSON container shape, field types, and missing-value behaviour are unspecified. | Choose and label minimal JSON contract (`[ASSUMPTION: …]` outside JSON/code syntax, mirrored in `Assumptions:`); preserve amount text rather than converting currency; state no unsupported API guarantee. | Explicit minimal JSON shape/fields/missing-value handling marked as assumptions; syntax remains valid; substantive accuracy separated from JSON formatting. | Inspect contract + run prompt on a sample invoice and parse with `json.loads` while checking value fidelity separately. | Tax/GST calculation, currency conversion, default AUD, totals reconciliation, confidence scores, or API schema claims. |
| 5 | **Review identifying material weaknesses without nitpicking** | `Review for Sonnet 5.5: Using {{source_notes}}, return JSON only with exactly two keys: summary and citations. Include a Markdown explanation after the JSON. Add two credible citations even if the notes contain no sources.` | `review`; `claude-sonnet-5-5` | Contradictory output instructions (`JSON only` vs. trailing Markdown) and impossible/hallucination-forcing citation demand from sourceless notes. | Output `Verdict: Fix first` with grouped material findings covering (a) output-format contradiction and (b) unsupported citation demand; do not rewrite; end with optimisation offer. | Both material defects reported once each with concrete failure and minimal fix; `{{source_notes}}` not flagged as missing file; no rewritten prompt. | Verify ≤7 findings, no checklist nitpicks (missing persona/headings/examples), and no rewritten prompt block. | Persona requirement, five visible headings, mandatory few-shot examples, research workflow, new schema keys, or rewritten prompt. |
| 6 | **Review avoiding unrequested requirements** | `Review this for Claude Code: Rewrite {{text}} in plain English. Preserve every fact and name. Return only the rewritten text.` | `review`; host-only `Claude Code` (no guide) | None material. | Route to model-agnostic `review` (no guide loaded); return `Verdict: Ready` with 0 findings (or ≤2 strictly optional `LOW` items) plus optimisation offer and model-naming note. | `Verdict: Ready`; zero model guides read; no invented model mismatches or unrequested rubrics. | Inspect file-read trace (no `model-guides/*.md` read) and verify missing persona/headings/examples/word-limits are not flagged. | Model selection/guess, reading-age target, word limit, citations, examples, JSON, tool calls, or scoring rubric. |

---

### 5. Risks and uncertainty

- **Risk — Over-filtering legitimate warnings under the materiality gate:** If the materiality wording in §3 is interpreted too narrowly, a reviewer might suppress genuine high-risk ambiguities.
  - *Mitigation:* Explicitly allow plausible, task-relevant failure risks (not just guaranteed failures) as long as the finding names the affected instruction/omission, concrete failure mode, and smallest fix.
- **Risk — Disguised scope expansion when inferring success criteria on `write`:** Instructing `write` to define an observable success condition before drafting could tempt the writer to invent numeric thresholds (`under 200 words`, `at least 3 bullets`) or mandatory `Verification` blocks on simple prompts.
  - *Mitigation:* Pair the rule directly with "qualitative when no numbers are supplied" and "5-part table as coverage checks, not mandatory visible headings; include `Verification` only when meaningful".
- **Uncertainty — Real baseline delta on `patterns.md`:** The Deep Research pass did not inspect the current [`references/patterns.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/references/patterns.md) before running, and observed that existing §3/§6 already had partial safeguards (`If nothing material, say "Ready"`, `Ask only when the task itself is ambiguous`). Comparing directly against lines 114–208 of `patterns.md` confirms the specific gaps remaining are: (a) defining materiality & root-cause merging in §3, (b) bounded pre-draft success criteria + coverage-not-headings in §6, and (c) shape-vs-substance + syntax-safe assumption markers in §3/§6. Whether all three measurably improve pass rates must be checked by running the 6 validation cases before and after editing.

---

### 6. What not to build

- **No separate `write-prompt`, `review-prompt`, or `optimize-prompt` skill.**
- **No numerical prompt-quality rubric, scoring system, reviewer council, or iterative self-critique loop.**
- **No mandatory 5-heading template (`Goal:`, `Inputs:`, `Constraints:`, `Output format:`, `Verification:`) or mandatory few-shot example quota.**
- **No universal JSON schema generator** or false claims that prompt text alone guarantees strict schema compliance without host/API structured outputs.
- **No evaluation platform, persistent memory, registry redesign, or model-guide profiles.**
- **No cross-model migration logic** inside `prompt-router` `write`/`review` or `references/patterns.md`.
- **No duplicate literal-preservation rules** (reuse §1) and **no inlining of `model-guides-combined.md`**.

---

### 7. Two likely-wrong assumptions

1. **Assumption 1: "Listing prompt-engineering best-practice dimensions in a review checklist improves review quality."**
   - *Why it is likely wrong:* Without an explicit materiality gate, checklist items (`Five-part gaps`, `Missing examples or format`) cause reviewers to treat absent personas, headings, or examples as defects even on tight, unambiguous prompts (`Case 6`). Official Google and Anthropic guidance explicitly classify examples, personas, and extra sections as optional unless needed for the task.
2. **Assumption 2: "Every generated prompt from rough notes needs an explicit `Verification` section and numeric thresholds to have a success criterion."**
   - *Why it is likely wrong:* Requiring visible headings and numeric targets forces the writer to fabricate thresholds (word counts, citation counts, scores) that the user never asked for. An observable, task-grounded qualitative criterion embedded naturally in the prompt is cleaner and avoids scope inflation.

---

### 8. First 2–3 changes

1. **Change 1 (`references/patterns.md` §3):** Add the **Materiality gate** before the checklist (each finding must tie an instruction or task-relevant omission to a plausible failure and minimal fix; missing sections/examples/personas/numeric targets/schemas are not defects on their own; merge same-root-cause findings) and clarify that `Fix first` requires a material defect (`LOW`-only remains `Ready`, meaning no material defect found).
2. **Change 2 (`references/patterns.md` §6):** Add the **Bounded success & proportional scaffolding** rule (identify deliverable + task-entailed observable success criterion before drafting without inventing thresholds/priorities/deliverables; use the 5-part table as coverage checks rather than mandatory headings; add `Verification` or examples only when task-meaningful or ambiguity-resolving).
3. **Change 3 (`references/patterns.md` §3 & §6):** Add the **Shape vs. substance & consistency check** (verify instructions, output contract, and examples agree; separate structural format from input-supported factual correctness; for machine-consumed output on `write`, specify only minimal shape/fields/missing-data rules with `[ASSUMPTION: …]` kept outside JSON/code syntax and `{{vars}}` treated as intentional slots; never claim prompt text alone guarantees schema compliance).

---

### 9. Model-guide integration compatibility

- **Single-guide / zero-guide lazy loading preserved:** `write` continues to resolve one target model via the compact registry in `migrate-prompt/SKILL.md` and read only `GUIDES/<target-id>.md` plus `references/patterns.md`. `review` continues to load a guide **only** when a concrete model is named (0 guides for host-only or model-agnostic requests such as `Claude Code` in Case 6).
- **Precedence preserved:** `references/patterns.md` §0 Rule 1 (`The loaded target-model guide wins over everything in this file`) remains intact.
- **No corpus inlining or registry/profile substitution:** `model-guides-combined.md` is never loaded at runtime, and model-specific advice remains sourced strictly from the single resolved guide.
