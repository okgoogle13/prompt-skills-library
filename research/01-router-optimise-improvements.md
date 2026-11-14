The strongest gains for `optimise` will come from making it **requirement-preserving by default**, **scope-bounded**, and **verification-oriented**—rather than making it rewrite more aggressively. The current patterns already cover much of this; the highest-value edits add an explicit preservation inventory, a “do not add” rule, and a testable completion condition.

## Ranked improvements

### 1. Add a literal-content preservation inventory

**Rank:** 1  
**Change:** Add a pre-rewrite inventory that identifies every literal element in the source prompt—code, commands, paths, URLs, identifiers, template variables, schemas, quoted strings, numeric values, dates, and XML/Markdown delimiters—then require a post-rewrite equivalence check.  
**Problem solved:** Reduces accidental alteration or loss of operationally meaningful content during restructuring. This is the highest-consequence failure mode: a rewritten prompt may read better while changing a command, path, variable name, or schema.  
**Evidence:** Anthropic recommends XML-style separation for instructions, context, examples, and variable inputs, because it reduces misinterpretation; it also recommends grounding responses in word-for-word quotes for long-document tasks.  OpenAI similarly advises explicitly stating required output syntax and format.[1][2][3][4]
**Evidence tier:** Tier 1  
**Surface:** `references/patterns.md`, §1 Core rules and §2.4 Rewrite style  
**Minimal implementation:**

```md
### Literal-content preservation

Before rewriting, silently identify every literal element that must survive unchanged:
- Code, shell commands, file paths, URLs, identifiers, and import paths
- Template variables, placeholders, function/field names, and schema keys
- Quoted strings, numeric values, dates, versions, and configuration values
- XML/HTML/Markdown delimiters and existing output contracts

After rewriting, verify each item appears exactly as supplied. If an element must change for a stated reason, retain its original form in a `Preserved literals:` block and explain the change in the changelog.

Do not normalise casing, quoting, whitespace, path separators, URL form, or identifier naming unless the user explicitly requests it.
```

**Validation method:** Run six fixture prompts containing a shell command, a Windows-style path, a URL with query parameters, a template variable, a JSON schema, and an inline code block. Assert byte-for-byte preservation after normalising only intentional whitespace around the preserved block.  
**Risk or tradeoff:** Slightly longer output for prompts containing many literals; may preserve awkward but intentional formatting.  
**Confidence:** High  
**Recommendation:** Adopt  
**Effect on guide loading and registry resolution:** None. It operates after target-model resolution and uses only the already-loaded target guide and shared patterns.

### 2. Require an explicit “do not add” scope boundary

**Rank:** 2  
**Change:** Add a scope-creep guard: the optimiser may clarify, sequence, format, or make explicit only requirements already implied by the user’s request; it must not introduce new deliverables, audiences, tools, quality bars, security rules, or workflow steps.  
**Problem solved:** Prevents the optimiser from turning a small request into an over-specified prompt, which is especially undesirable for modern models that already respond well to outcome-oriented instructions.  
**Evidence:** Anthropic’s Skill guidance says to match specificity to task fragility, avoid offering unnecessary options, and include only context the model does not already have.  Anthropic also warns against stuffing prompts with edge-case rules rather than using a small set of canonical examples.  OpenAI’s prompt-generation guidance explicitly says to avoid unnecessary instructions or bland statements.[5][6][7]
**Evidence tier:** Tier 1  
**Surface:** `references/patterns.md`, §2.1 Size the change to the gap and §2.4 Rewrite style  
**Minimal implementation:**

```md
### Scope boundary

Improve only the task the user asked for. You may make an existing implication explicit, remove ambiguity, or add a missing output/verification requirement only when it is necessary for the stated goal.

Do not add:
- New deliverables, audiences, workflows, tools, or process stages
- Unrequested quality bars, personas, tone rules, or stylistic preferences
- Extra constraints that are merely plausible or generally advisable
- Requirements that would change the task’s scope or intended user

If a plausible addition would materially improve reliability but was not requested, mention it in one `Optional improvement:` line rather than adding it to the prompt.
```

**Validation method:** Give the optimiser prompts such as “rewrite this SQL query prompt” or “improve this email draft prompt.” A pass requires the rewritten prompt to remain within the original deliverable and not acquire unrequested sections, personas, tool instructions, or acceptance criteria.  
**Risk or tradeoff:** May leave genuinely useful improvements unimplemented; mitigate this with the single `Optional improvement:` line.  
**Confidence:** High  
**Recommendation:** Adopt  
**Effect on guide loading and registry resolution:** None.

### 3. Make the “Done when” check produce a testable acceptance condition

**Rank:** 3  
**Change:** Upgrade §2.2’s `Done when` from a presence/absence classification to a required, checkable completion condition whenever the task has a verifiable outcome. If the user did not supply one, derive the narrowest reasonable condition from the existing request; if it cannot be derived safely, mark it `[ASSUMPTION: success criterion not specified]` rather than inventing detailed criteria.  
**Problem solved:** Reduces vague outputs and makes the resulting prompt easier to evaluate. It also prevents the optimiser from padding prompts with generic quality language.  
**Evidence:** Anthropic frames prompt-engineering success criteria as controllable requirements and recommends defining the task and success criteria before iterating.  OpenAI’s enterprise guidance recommends an explicit checklist or acceptance criteria for judging a response.  Google advises specifying the required response format rather than leaving the model to infer it.[8][9][10][11]
**Evidence tier:** Tier 1  
**Surface:** `references/patterns.md`, §2.2 Five-part check  
**Minimal implementation:**

```md
### Done when

For every prompt with a verifiable outcome, state a concrete completion condition:
- The exact artifact or answer required
- Its required scope or boundaries
- Any user-supplied format, length, schema, or threshold
- A check the requester can perform without additional interpretation

Use the narrowest condition supported by the original request. Do not invent metrics, thresholds, review processes, or acceptance tests.

If no safe completion condition can be inferred, write:
`Done when: [ASSUMPTION: success criterion not specified; preserve the user's stated goal]`
```

**Validation method:** For prompts missing success criteria, check that the rewrite either contains one narrowly derived from the request or carries the prescribed assumption marker. It must not introduce arbitrary numeric thresholds, review stages, or extra deliverables.  
**Risk or tradeoff:** A poorly calibrated rule could over-constrain open-ended creative work; exempt tasks where “done” is inherently subjective.  
**Confidence:** High  
**Recommendation:** Adopt  
**Effect on guide loading and registry resolution:** None.

### 4. Separate “missing requirement” from “missing detail”

**Rank:** 4  
**Change:** Refine §2.1/§2.3 so the optimiser distinguishes between (a) a requirement that is absent and must be added only when safely inferable, and (b) information that is unknown and must remain an assumption or be requested through `clarify`. This prevents fabricated constraints and unsupported specificity.  
**Problem solved:** Reduces both missed requirements and invented requirements. The current rule already marks material gaps, but making the distinction operational will improve consistency.  
**Evidence:** Anthropic advises not assuming the model will infer intent and to state requirements directly, while also cautioning against over-engineering prompts.  Research on instruction following finds that explicit constraints can improve compliance, but models vary in generalising across constraint types.[12][13][14]
**Evidence tier:** Tier 2 for the benchmark evidence; Tier 1 for the vendor guidance  
**Surface:** `references/patterns.md`, §2.1 and §2.3  
**Minimal implementation:**

```md
### Missing versus unknown

Classify each gap as one of:
- `Missing but inferable`: directly implied by the request; make it explicit without expanding scope.
- `Unknown and material`: affects the result but cannot be safely inferred; mark `[ASSUMPTION: …]` or route to `clarify`.
- `Not needed`: optional detail that does not affect the requested outcome; omit it.

Never convert an unknown into a specific requirement. Do not add a constraint merely because a high-quality prompt often includes one.
```

**Validation method:** Use paired prompts: one with an inferable output format (“return JSON”) and one with an unknown audience (“improve this proposal”). The first may make the JSON requirement explicit; the second must not invent an audience, tone, length, or review workflow.  
**Risk or tradeoff:** More classification decisions may make outputs slightly longer; keep the categories terse.  
**Confidence:** High  
**Recommendation:** Adopt  
**Effect on guide loading and registry resolution:** None.

### 5. Add a minimal rewrite-diff contract for low-gap prompts

**Rank:** 5  
**Change:** For prompts classified as `Already strong` or `Short but clear`, require a minimal diff: preserve structure where possible, change only the specific weakness, and state in the changelog why each edit was necessary.  
**Problem solved:** Reduces unnecessary restructuring, synonym churn, and loss of user intent in prompts that are already adequate. This directly supports the existing “material improvement” principle.  
**Evidence:** Anthropic’s Skill authoring guidance emphasises concision, avoiding unnecessary context, and matching strictness to need.  Anthropic’s prompting guidance says longer, more complex prompts are not inherently better and that advanced techniques cannot compensate for an unclear core request.  OpenAI likewise advises concise prompts and warns against unnecessary instructions.[5][7][12]
**Evidence tier:** Tier 1  
**Surface:** `references/patterns.md`, §2.1 and §2.5  
**Minimal implementation:**

```md
### Minimal-change rule

For `Already strong` or `Short but clear` prompts:
- Preserve the user's structure, ordering, and wording wherever it does not create a defect.
- Change only the specific weakness identified.
- Do not reformat, rename sections, add functional blocks, or replace wording for style.
- In the changelog, state the concrete defect each edit fixes.

If no material improvement is available, return the prompt unchanged with:
`No material improvement identified.`
```

**Validation method:** Give the optimiser 10 already-clear prompts. Pass if at least 8 are returned unchanged or with a narrowly scoped edit, and no edit introduces a new requirement, section, or stylistic preference.  
**Risk or tradeoff:** May under-improve prompts that would benefit from a larger structural rewrite; retain the existing complex-prompt functional-block rule as the exception.  
**Confidence:** Medium  
**Recommendation:** Adopt  
**Effect on guide loading and registry resolution:** None.

## Six validation cases

| Case | Original prompt | Expected weakness | Desired behaviour | Pass condition | Simple check | Must not add |
|---|---|---|---|---|---|---|
| 1. Ambiguous task | “Improve this: Write about renewable energy.” | No audience, purpose, deliverable, or scope. | Preserve the broad request; mark the material unknowns; do not select an audience or depth. | Output retains the original topic, marks `[ASSUMPTION: audience/purpose/deliverable unspecified]`, and does not manufacture requirements. | Search for invented audience, word count, tone, or format. | A persona, audience, length limit, or research workflow. |
| 2. Missing success criterion | “Rewrite this customer email to be clearer.” | “Clearer” has no observable completion test. | Derive the narrowest safe condition, such as preserving the request and making the requested action explicit; otherwise flag the assumption. | Contains a concrete `Done when` condition or the prescribed assumption marker. | Check for a checkable artifact/action or an explicit `[ASSUMPTION: …]`. | A CSAT score, approval workflow, A/B test, or unsupported quality threshold. |
| 3. Missing constraint | “Summarise this contract.” | Confidentiality, jurisdiction, source grounding, or output boundaries may matter but are not stated. | Preserve the task; identify material unknowns; do not invent legal or confidentiality constraints. | Adds no unrequested legal, confidentiality, or compliance constraint; marks material unknowns where relevant. | Search for invented “must comply with”, “do not disclose”, or jurisdictional language. | A compliance regime, redaction rule, or legal-review step. |
| 4. Vague output format | “Give me a project status update.” | No structure, length, or fields are specified. | If the user’s context implies a format, make only that explicit; otherwise preserve flexibility and flag the unknown. | Either makes a narrowly supported format explicit or marks `[ASSUMPTION: output format unspecified]`; does not fabricate a schema. | Check whether any added fields, headings, or JSON structure are supported by the original request. | An unrequested JSON schema, fixed word count, or dashboard format. |
| 5. Scope-creep risk | “Improve this prompt: Draft a short release note for the login fix.” | The optimiser may add QA plans, rollout instructions, stakeholder comms, or metrics. | Improve clarity and output definition only; keep the deliverable a short release note. | The rewritten prompt still requests one short release note; no new deliverable or workflow is introduced. | Count deliverables and required process stages before versus after. | Testing instructions, deployment steps, stakeholder approvals, or extra documents. |
| 6. Literal preservation | “Improve this prompt: Run `python scripts/run_report.py --out "C:\Reports\Q4 2026.xlsx" --mode=fast` and summarise results.” | A rewrite could normalise the Windows path, alter quoting, or change command flags. | Preserve the command, path, quoting, flags, and variable names exactly; improve only the surrounding instruction. | Every literal token remains byte-for-byte identical after surrounding-whitespace normalisation. | Diff the original command/path/URL against the rewritten prompt. | Path normalisation, shell escaping changes, added error handling, or a replacement command. |

## Resource list

| Resource | URL | Tier | Why it matters |
|---|---|---|---|
| Anthropic — Prompting best practices | [https://docs.anthropic.com/claude/prompt-library](https://docs.anthropic.com/claude/prompt-library) | 1 | Direct guidance on explicit output requirements, sequential steps, XML separation, and avoiding inferred extras. [1] |
| Anthropic — Increase output consistency | [https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency) | 1 | Supports precise output templates, examples, and breaking complex work into subtasks. [15] |
| Anthropic — Reduce hallucinations | [https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | 1 | Supports word-for-word quote extraction and source grounding for factual work. [2] |
| Anthropic — Skill authoring best practices | [https://docs.anthropic.com/claude/docs/agents-and-tools/agent-skills/best-practices](https://docs.anthropic.com/claude/docs/agents-and-tools/agent-skills/best-practices) | 1 | Directly relevant to concise skill instructions, appropriate degrees of freedom, and avoiding unnecessary options. [5] |
| OpenAI — Prompt engineering guide | [https://platform.openai.com/docs/guides/prompt-engineering](https://platform.openai.com/docs/guides/prompt-engineering) | 1 | Covers instructions, constraints, examples, and specific output direction. [4] |
| OpenAI — Prompt generation | [https://platform.openai.com/docs/guides/prompt-generation](https://platform.openai.com/docs/guides/prompt-generation) | 1 | Explicitly recommends detailed output-format specification while avoiding unnecessary instructions. [7] |
| Google — Prompt design strategies | [https://aistudio.google.com/docs/prompting-strategies](https://aistudio.google.com/docs/prompting-strategies) | 1 | Supports precise instructions, explicit constraints, response format, and consistent structure. [16] |
| AGENTIF benchmark | [https://proceedings.neurips.cc/paper_files/paper/2025/file/51bb3a8a33610a25aae074bfc51b1b1f-Paper-Datasets_and_Benchmarks_Track.pdf](https://proceedings.neurips.cc/paper_files/paper/2025/file/51bb3a8a33610a25aae074bfc51b1b1f-Paper-Datasets_and_Benchmarks_Track.pdf) | 2 | Research evidence that explicit constraints can improve instruction following, while generalisation across constraint types remains difficult. [13] |

## Synthesis & action plan

### Make these first

1. **Add the literal-content preservation inventory** to `references/patterns.md` §1 and cross-reference it from §2.4. This is the highest-risk-reduction change because it protects code, commands, paths, URLs, variables, and schemas from well-intentioned rewriting.[1][2]

2. **Add the scope-boundary rule** to `references/patterns.md` §2.1 and §2.4. It directly targets over-specification and unrequested constraints, aligning with vendor guidance to avoid unnecessary instructions and unnecessary options.[5][7]

3. **Upgrade `Done when` into a narrow, testable acceptance condition** in `references/patterns.md` §2.2. This improves output specifications without turning every prompt into an over-engineered specification.[8][10]

### Exact edit locations

- `prompt-router/SKILL.md`, `optimise` route: add one line after guide loading: “Apply `references/patterns.md` §1, §2.1–§2.5, and the literal-content preservation inventory before rewriting.”
- `references/patterns.md`, §1 Core rules: append **Literal-content preservation**.
- `references/patterns.md`, §2.1: append **Scope boundary** and **Missing versus unknown**.
- `references/patterns.md`, §2.2: replace or augment the `Done when` bullet with **Done when**.
- `references/patterns.md`, §2.4: add **Minimal-change rule** and a pointer back to literal preservation.
- `references/patterns.md`, §2.5: require the changelog to identify the concrete defect fixed by each edit; prohibit “improved clarity” as a standalone justification.

### Likely-wrong assumptions

- **“More explicit constraints always improve modern model behaviour.”** Explicit constraints help when they are real requirements, but unnecessary constraints consume attention and can induce unwanted behaviour; Anthropic and OpenAI both caution against over-engineering and unnecessary instructions.[6][7][12]
- **“A better optimiser should always restructure the prompt.”** Often the best edit is minimal: clarify one ambiguity, make one implied requirement explicit, or add one checkable completion condition. Anthropic’s Skill guidance specifically favours concision and matching strictness to need.[5]

### What not to build

- Do **not** add a general prompt-quality taxonomy or scoring rubric; it invites generic rewrites and scope creep.
- Do **not** make `optimise` ask clarifying questions; retain the existing separation from `clarify`.
- Do **not** add automatic test generation, evaluation harnesses, persistent memory, or cross-model migration logic.
- Do **not** replace the target-model guide with registry metadata or inline combined guide content.
- Do **not** mandate functional blocks for every prompt; reserve them for complex prompts, as the current design already does.

### Compatibility assessment

All recommended changes are compatible with the existing integration pattern. They operate **after** the router resolves the target model and loads exactly one `model-guides/<target-id>.md`; they do not alter registry resolution, guide selection, or the one-guide loading rule. They should be implemented as concise shared rules in `references/patterns.md`, with only a one-line routing reminder in `prompt-router/SKILL.md`, preserving the skill’s low-context-footprint design.[5]

Citations:
[1]: https://docs.anthropic.com/claude/prompt-library
[2]: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
[3]: https://help.openai.com/en/articles/6654000-comprehensive-guide-to-prompt-engineering
[4]: https://platform.openai.com/docs/guides/prompt-engineering
[5]: https://docs.anthropic.com/claude/docs/agents-and-tools/agent-skills/best-practices
[6]: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
[7]: https://platform.openai.com/docs/guides/prompt-generation
[8]: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
[9]: https://catalog.workshops.aws/prompt-eng-claude3/en-US/lessons
[10]: https://developers.openai.com/cookbook/examples/chatgpt/chatgpt_prompt_guide/chatgpt_prompt_guide
[11]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies
[12]: https://claude.com/resources/articles/best-practices-for-prompt-engineering
[13]: https://proceedings.neurips.cc/paper_files/paper/2025/file/51bb3a8a33610a25aae074bfc51b1b1f-Paper-Datasets_and_Benchmarks_Track.pdf
[14]: https://proceedings.neurips.cc/paper_files/paper/2025/file/46499a0622ecf568b72d17b61e45dbd5-Paper-Datasets_and_Benchmarks_Track.pdf
[15]: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency
[16]: https://aistudio.google.com/docs/prompting-strategies
[17]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/design-multimodal-prompts
[18]: https://help.openai.com/en/articles/6654000-best-practices-for-promptengineering-%20with-openai-api
[19]: https://www.promptea.me/en/guides/gemini-prompt-guide
[20]: https://hugesoftware.com/blog/27-prompt-engineering-tips-from-anthropic/
[21]: https://www.reddit.com/r/promptingmagic/comments/1qyxlkl/5_prompting_strategies_anthropic_engineers_use/
[22]: https://pub.towardsai.net/the-5-prompt-engineering-patterns-that-replaced-my-entire-qa-team-d5d095d39c02
[23]: https://github.com/openai/skills/blob/main/skills/.system/openai-docs/references/prompting-guide.md
[24]: https://arxiv.org/html/2505.09139v1
[25]: https://www.anthropic.com/news/prompting-long-context
[26]: https://arxiv.org/pdf/2502.11436.pdf
[27]: https://www.anthropic.com/news/prompt-engineering-for-business-performance
[28]: https://web3.arxiv.org/pdf/2512.17920
[29]: https://count.co/ai/prompt-engineering-techniques
[30]: https://quizlet.com/965168398/anthropic-prompt-engineering-flash-cards/
[31]: https://www.semanticscholar.org/paper/Self-Supervised-Prompt-Optimization-Xiang-Zhang/9bbe3995bfe3740d5be29d56778d7434c572cd78
[32]: https://www.datastudios.org/post/claude-ai-prompting-techniques-how-to-write-effective-instructions-for-accurate-long-context-respo
[33]: https://ar5iv.labs.arxiv.org/html/2502.16923
[34]: https://docs.anthropic.com/en/release-notes/system-prompts
[35]: https://docs.anthropic.com/en/docs/claude-code/prompt-library
[36]: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak
[37]: https://docs.anthropic.com/fr/docs/claude-code/sdk/modifying-system-prompts
[38]: https://docs.anthropic.com/en/docs/about-claude/models/overview
[39]: https://docs.anthropic.com/en/docs/about-claude/use-case-guides/customer-support-chat
[40]: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
[41]: https://docs.anthropic.com/llms-full.txt
[42]: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use
[43]: https://docs.anthropic.com/en/build-with-claude/skills-guide

---
[Quota] Used 1 Deep Research query (deep_research) | Pro: 0 left | Research: 20 left | EXHAUSTED: Use pplx_smart_query(intent='quick') or pplx_sonar to avoid failures

[Conversation ID: 5c3e26e3-0651-4699-b88d-59b9eb5a831a]

## Extraction — do not edit the full report above

### 1. Ranked improvement shortlist

| Rank | Improvement | Surface | Evidence Tier | Confidence | Recommendation |
|---:|---|---|---:|---|---|
| 1 | **Literal-content non-normalisation & pre-return verification** — extend `PATTERNS` §1 `Preserve exactly` and §2.1 pre-return checks so the optimiser never normalises path separators (`\` vs `/`), quoting, CLI flags, URL query strings, identifier casing, or schema keys, and silently verifies byte-for-byte survival before output. | `references/patterns.md` (§1, §2.1) | Tier 1 (Anthropic, OpenAI) | High | **Adopt** (combine with #5 into Change 1) |
| 2 | **Explicit scope-boundary ("do not add") & missing-vs-unknown rule** — forbid introducing unrequested deliverables, audiences, workflows, tools, personas, compliance regimes, or arbitrary thresholds; distinguish `missing but inferable` from `unknown and material` (`[ASSUMPTION: …]`). | `references/patterns.md` (§2.1) | Tier 1 & Tier 2 (Anthropic, OpenAI, AGENTIF) | High | **Adopt** (Change 2) |
| 3 | **Narrow, testable `Done when` completion condition** — refine `PATTERNS` §2.2 `Done when` so verifiable tasks get the narrowest completion check supported by the original request (or `[ASSUMPTION: …]` when uninferable) without inventing metrics, review gates, or thresholds. | `references/patterns.md` (§2.2) | Tier 1 (Anthropic, OpenAI, Google) | High | **Adopt** (Change 3) |
| 4 | **Separate "missing requirement" from "missing detail"** — operationalise gap handling so unknown context is marked `[ASSUMPTION: …]` rather than converted into a hard requirement. | `references/patterns.md` (§2.1) | Tier 1 & Tier 2 | High | **Adopt** (merged into Change 2 to keep `patterns.md` concise) |
| 5 | **Pre-return verification & concrete-defect changelog discipline** — strengthen §2.1's `Material-improvement check` into a combined pre-return check (material improvement + literal survival + no added scope) and require §2.5 changelog entries to name the concrete defect or guide rule fixed rather than generic "improved clarity". | `references/patterns.md` (§2.1, §2.5) | Tier 1 | High | **Adopt** (merged into Change 1 & Change 3) |

*(Rejected detail from raw report: adding a new `Preserved literals:` output block or `Optional improvement:` output line outside the prompt/changelog, because that would alter `prompt-router/SKILL.md` Step 6's fixed 4-part output contract for `optimise`.)*

---

### 2. Recommended changes

To keep `references/patterns.md` compact while capturing all five improvements without altering `prompt-router/SKILL.md`'s fixed Step 6 output contract, consolidate the findings into **3 surgical changes** in `references/patterns.md`:

1. **Change 1 — Literal non-normalisation & pre-return verification (`references/patterns.md` §1 and §2.1):**
   - In §1 (`Preserve exactly`), explicitly forbid normalising path separators (`\` vs `/`), shell quoting, CLI flags, URL parameters, casing, or schema keys.
   - In §2.1 (`Material-improvement check`), expand the pre-return gate so that before returning, the optimiser checks three invariants: (a) material improvement (not just formatting/synonym swaps), (b) every original requirement and literal token survived unchanged, and (c) no unrequested deliverable, workflow stage, or constraint was added.
2. **Change 2 — Explicit scope boundary & missing-vs-unknown rule (`references/patterns.md` §2.1):**
   - Add a compact **Scope boundary** rule to §2.1: make implied requirements explicit only when needed for the stated goal; never add unrequested deliverables, audiences, workflows, personas, compliance/security regimes, or arbitrary thresholds. Convert unknown material details into `[ASSUMPTION: …]`, never into invented requirements.
3. **Change 3 — Narrow `Done when` & defect-anchored changelog (`references/patterns.md` §2.2 and §2.5):**
   - In §2.2 (`Five-part check`), refine `Done when` so it uses a runnable command where one exists, or otherwise the narrowest checkable completion condition supported by the request (without inventing metrics, thresholds, or review stages).
   - In §2.5 (`Changelog`), forbid generic justifications ("improved clarity", "better structure"); every `What → Why` entry must name the specific defect prevented or target-guide rule applied.

---

### 3. Exact edit locations

- [`/Users/okgoogle13/.claude/skills/prompt-router/references/patterns.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/references/patterns.md):
  - **§1 Core rules** (lines 25–27): `Preserve exactly` bullet.
  - **§2.1 Size the change to the gap** (lines 50–51): `Material-improvement check (before returning)` paragraph + new `Scope boundary` bullet.
  - **§2.2 Five-part check** (lines 61–63): `Done when` table row and trailing note.
  - **§2.5 Changelog** (lines 100–102): concrete defect / guide-fact requirement.
- [`/Users/okgoogle13/.claude/skills/prompt-router/SKILL.md`](file:///Users/okgoogle13/.claude/skills/prompt-router/SKILL.md):
  - **No edit needed.** Step 5 line 130 (`optimise — PATTERNS §1, §2 and, for coding-agent tasks, §4...`) already loads and applies `PATTERNS` §1 and §2, and keeping `SKILL.md` untouched avoids unnecessary churn and preserves its Step 6 output contract.

---

### 4. Validation cases

| # | Case | Original prompt | Expected weakness | Desired behaviour | Pass condition | Simple check | What the optimiser must not add |
|---:|---|---|---|---|---|---|---|
| 1 | **Ambiguous task** | `"Improve this for Sonnet 5.5: Write about renewable energy."` | Missing deliverable, audience, scope, and purpose. | Keep the core topic intact; structure a minimal prompt that marks material gaps as `[ASSUMPTION: …]` rather than picking an audience or format as a hard constraint. | Rewritten prompt retains the topic, marks material unknowns with `[ASSUMPTION: …]`, and does not lock in an unrequested persona or word count. | Inspect output for `[ASSUMPTION:` and verify no invented persona, audience, or fixed word count is stated as fact. | A domain persona, specific target audience, fixed word count, or multi-stage research workflow. |
| 2 | **Missing success criterion** | `"Optimise for GPT-5: Rewrite this customer email to be clearer: <email>{{draft}}</email>"` | "Clearer" has no checkable completion criterion. | Preserve `<email>{{draft}}</email>` verbatim; define a narrow, checkable completion condition (e.g., original request/action and key facts preserved in a single ready-to-send email) without inventing business metrics. | `<email>{{draft}}</email>` survives untouched and the prompt includes a narrow, checkable completion condition or `[ASSUMPTION: …]`. | Check `<email>{{draft}}</email>` exact match and verify no numeric KPI or review gate was added. | CSAT targets, A/B test variants, tone rubrics, or multi-step approval workflows. |
| 3 | **Missing constraint** | `"Optimise for Opus 5.5: Summarise this contract: {{contract_text}}"` | Source grounding and missing-clause handling are unstated, while jurisdiction/compliance rules are unknown. | Ground the summary strictly in `{{contract_text}}` (inferable guardrail against hallucination) and mark material scope unknowns as `[ASSUMPTION: …]`, without inventing legal jurisdictions or compliance regimes. | `{{contract_text}}` is preserved verbatim; prompt requires grounding in the supplied text; no unrequested legal/regulatory regime is invented. | Search output for invented jurisdiction names, "GDPR/HIPAA", or legal-advice disclaimers not in input. | Unrequested jurisdiction rules, compliance frameworks, redaction pipelines, or legal sign-off steps. |
| 4 | **Vague output format** | `"Optimise for Gemini 3.8 Flash: Give me a project status update from these notes: {{notes}}"` | Output format/sections are unspecified. | Propose a lightweight structure only if clearly marked `[ASSUMPTION: …]` (or keep structure minimal), and preserve `{{notes}}` verbatim. | `{{notes}}` is preserved and any concrete section list not in the input is marked `[ASSUMPTION: …]`. | Verify `{{notes}}` is intact and no unrequested JSON schema or rigid word count is forced without an `[ASSUMPTION: …]` marker. | Rigid JSON schemas, executive dashboards, RACI matrices, or unrequested word-count caps. |
| 5 | **Scope-creep risk** | `"Optimise for Gemini 4 Argon: Draft a short release note for the login fix."` | Optimiser might inflate a simple release note into a rollout/QA/comms plan. | Classify as `Short but clear`; keep the deliverable a single short release note; add only minimal input/output boundaries and `[ASSUMPTION: …]` for missing fix details. | Rewritten prompt requests exactly one short release note and introduces zero additional deliverables or process stages. | Count deliverables and workflow stages (must be 1 deliverable, 1 step). | QA test plans, rollback procedures, deployment checklists, stakeholder emails, or telemetry metrics. |
| 6 | **Literal code, path, command, or URL preservation** | ``"Optimise for Sonnet 5.5: Run `python scripts/run_report.py --out \"C:\\Reports\\Q4 2026.xlsx\" --url \"https://internal.example.com/api/v2/items?limit=50&active=true\" --mode=fast` and summarise the output."`` | Rewriter might convert `\` to `/`, strip quotes around `C:\Reports\Q4 2026.xlsx`, drop query params, or rename flags. | Preserve the command, Windows path, quotes, URL + query string, and flags byte-for-byte; clarify only how the output should be summarised. | Exact substring `python scripts/run_report.py --out "C:\Reports\Q4 2026.xlsx" --url "https://internal.example.com/api/v2/items?limit=50&active=true" --mode=fast` appears unmodified in the optimised prompt. | Exact substring match on the command string. | Path slash conversion (`C:/Reports/...`), flag alteration, added bash error-handling wrappers (`set -euo pipefail`), or replacement commands. |

---

### 5. Risks and uncertainty

- **Risk — Over-constraining valid structural improvements on vague prompts:** If the scope-boundary or minimal-change rule is stated too rigidly, the optimiser might under-help genuinely vague prompts.
  - *Mitigation:* Tie the minimal-diff discipline to `Already strong` and `Short but clear` prompts in `PATTERNS` §2.1, and allow `Vague` prompts to make directly implied requirements explicit while marking unknown specifics with `[ASSUMPTION: …]`.
- **Risk — Breaking the Step 6 output contract:** The raw Deep Research report suggested a `Preserved literals:` block and an `Optional improvement:` line. Adding new top-level sections would violate `prompt-router/SKILL.md` Step 6 (`optimise` outputs: 1. fenced prompt, 2. `Run settings:`, 3. Changelog, 4. `Guide-Stand` footer).
  - *Mitigation:* Keep all literal-preservation and scope checks internal (`before returning`), and place any optional out-of-scope suggestion inside the existing §2.5 Changelog rules (which already state: `Suggestions outside the rewrite follow "Do X, because Y"; drop any without a reason`).
- **Uncertainty:** Whether adding 8–10 lines to `references/patterns.md` increases latency or dilution on smaller models. Because `patterns.md` is currently 198 lines (~1.5k tokens), a net addition of ~10 lines is <5% growth and well within budget.

---

### 6. What not to build

- **No separate `optimize-prompt` skill** or model-guide router skill.
- **No new output sections** (`Preserved literals:`, `Optional improvement:`) that alter `prompt-router/SKILL.md` Step 6's four-part output contract.
- **No clarifying questions on the `optimise` route** — questions remain restricted to `clarify` and the single task-ambiguity question on `write`.
- **No numerical prompt-quality rubric or taxonomy** inside runtime context.
- **No mandatory 5-block template (`Task:`, `Known details:`, etc.) for simple prompts** — keep functional blocks restricted to complex prompts (`PATTERNS` §2.4).
- **No inlining of `model-guides-combined.md`** or replacement of full model guides with registry/profile metadata.

---

### 7. Two likely-wrong assumptions

1. **Assumption 1: "Adding more explicit constraints and best-practice guardrails always improves an optimised prompt."**
   - *Why it is likely wrong:* On frontier reasoning models (`claude-opus-5-5`, `gemini-4-argon`, `gpt-5`), unrequested constraints, personas, and edge-case rules compete with the user's real requirements and cause over-analysis or scope drift. Both Anthropic and OpenAI explicitly warn against adding unnecessary instructions.
2. **Assumption 2: "An optimiser only adds value when it visibly restructures the prompt into labelled sections."**
   - *Why it is likely wrong:* For `Already strong` or `Short but clear` prompts, restructuring increases the risk of dropping a literal flag, path, or nuance while adding zero task value. Often the highest-value optimisation is a surgical edit to one ambiguous requirement plus moving reasoning directives into `Run settings:`.

---

### 8. First 2–3 changes

1. **Change 1 (`references/patterns.md` §1 & §2.1):** Add explicit literal non-normalisation rules (paths, quotes, flags, URLs, casing, schema keys) in §1 and expand §2.1's `Material-improvement check (before returning)` to verify literal survival and zero added scope before outputting.
2. **Change 2 (`references/patterns.md` §2.1):** Add a compact **Scope boundary** rule distinguishing `missing but inferable` requirements from `unknown and material` details (`[ASSUMPTION: …]`), and forbidding unrequested deliverables, workflows, personas, compliance rules, or thresholds.
3. **Change 3 (`references/patterns.md` §2.2 & §2.5):** Refine `Done when` in §2.2 to require the narrowest checkable completion condition supported by the request (without invented metrics or review stages), and tighten §2.5 (`Changelog`) so every entry names the concrete defect prevented or guide fact applied (banning generic "improved clarity" justifications).

---

### 9. Model-guide integration compatibility

- **Single target-guide lazy loading preserved:** `optimise` continues to resolve one target model via the compact registry in `migrate-prompt/SKILL.md` and read only `GUIDES/<target-id>.md` plus `references/patterns.md`.
- **Precedence preserved:** `references/patterns.md` §0 Rule 1 (`The loaded target-model guide wins over everything in this file`) remains untouched, so model-specific rules in `model-guides/<target-id>.md` always override shared defaults.
- **No corpus inlining or registry leakage:** Neither `model-guides-combined.md` nor unrelated model guides are read or referenced.
