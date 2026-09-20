# Gemini in Chrome — Custom Gemini Skills Rework

**Status:** Proposal for review and approval  
**Date:** 20 September 2026  
**Scope:** Personal Gemini in Chrome Skills library for quick, repeatable browser-based work

## 1. Purpose

Create a small, reliable library of custom Gemini in Chrome Skills that reduces repeated browser work across research, job applications, GitHub triage, structured extraction, communications, and selected project analysis.

The system is deliberately **not** an autonomous-agent platform, a connector runtime, a local-repository tool, or a substitute for Antigravity IDE. Gemini in Chrome Skills are reusable browser prompts saved in Chrome’s Gemini experience. They should produce trustworthy, decision-ready output from the current page or explicitly selected browser tabs.

## 2. Goals

### Primary goals

- Replace repeated browser prompting with short, reusable skills.
- Produce outputs that are immediately usable in notes, project documents, trackers, or downstream automation.
- Reduce manual extraction, comparison, triage, and rewriting work.
- Preserve evidence, uncertainty, and source boundaries rather than creating polished but unsupported answers.
- Keep the library small enough to search, maintain, and improve through real use.

### Success criteria

The first release succeeds when it contains **6-8 retained skills**, each of which:

- Addresses a recurring real-world browser task.
- Has one clear input shape and one output contract.
- Is usable from its name in Chrome’s `/` skill selector.
- Is tested on at least three representative real sources.
- Produces an output requiring little or no manual reformatting.
- Has a documented limitation or “do not use” boundary.
- Saves time or cognitive effort compared with starting a fresh prompt.

### Non-goals

- Building all 24 previously drafted skills immediately.
- Building multi-agent orchestration inside Chrome Skills.
- Giving a Chrome Skill direct access to local files, terminals, private repositories, inboxes, APIs, or connected services unless the active Chrome/Gemini UI explicitly provides that access.
- Sending messages, creating calendar events, making purchases, modifying records, or taking other irreversible actions from a saved Skill without explicit user confirmation in the relevant execution environment.
- Solving every writing, research, or automation task with a separate skill.

## 3. Design Principles

### Simplicity first

Start with the smallest set of skills that resolves proven recurring friction. Merge overlapping functions and reject extra phases, roles, rules, or prompts unless they fix an observed failure or meet a testable requirement.

### One skill, one contract

Each skill should have:

- A defined page/tab input.
- A defined task.
- A defined output format.
- Explicit handling of missing evidence.
- A boundary describing when not to use it.

For example, a decision-ready research brief and a valid JSON extraction are different tasks and should remain separate.

### Evidence over fluency

Skills must preserve exact figures, dates, names, direct wording, and source uncertainty where relevant. They must not infer qualifications, owners, deadlines, citations, or facts missing from the source.

### Test before scale

Do not bulk-create a large Skills library. A prompt becomes a retained Skill only after it has been exercised on real sources and has passed its acceptance tests.

### Maintain a small external record

Chrome’s Skills library is a UI for saved prompts, not a mature workflow registry. Keep this document and a short test log in the repository or notes system as the durable source of truth. The live library itself can be opened through `chrome://skills/browse`; its exact features must be verified in the user’s current Chrome build.

## 4. Operating Model

### What a Chrome Skill does

A Chrome Skill is a reusable Gemini prompt saved from the Chrome Gemini experience. It can be run on a page and, where supported by the current UI, selected browser tabs.

### What a Chrome Skill does not do

It does not inherently:

- Execute shell commands.
- Read a local repository.
- Call GitHub, Pipedream, Google Drive, Calendar, Finance, Wise, Firecrawl, Hugging Face, or other connectors.
- Make validated API requests.
- Perform a full multi-agent review pipeline itself.
- Create, update, send, buy, delete, or submit anything without a separate explicit action in the relevant tool.

Chrome Skills can produce structured browser-derived material that is later pasted or deliberately passed into Antigravity IDE, a repository workflow, or an automation platform.

## 5. Skills Library Structure

Use a compact flat naming convention because the Chrome Skills library should be treated as a searchable list, not as a folder hierarchy.

### Naming format

`[emoji] short-verb-name`

Examples:

- `📦 to-json`
- `🔎 research-brief`
- `🎯 job-fit`
- `✍️ action-items`

Use short names that are easy to find with `/`. Do not use numbered names unless the live UI proves that numbering materially improves ordering; numbering creates maintenance friction when skills are deleted, merged, or renamed.

### Categories

| Prefix | Category | Purpose |
|---|---|---|
| `📦` | Structured extraction | Create valid, compact data for downstream use |
| `🔎` | Research and comparison | Turn pages/tabs into decision-ready evidence |
| `🎯` | Career and project decisions | Assess job fit and GitHub work items honestly |
| `✍️` | Communications | Extract commitments or draft bounded replies |
| `🧩` | Prompt design | Improve prompts without adding complexity |
| `🧠` | Nalex analysis | Objective communication-source analysis only |

## 6. Proposed Initial Skills

The initial build target is nine candidates, with **six to eight retained after testing**.

### 6.1 `📦 to-json`

**Problem solved:** Browser information is difficult to reuse in automated or structured workflows until it is turned into stable, parseable data.

**Use on:** Articles, documentation pages, notices, job ads, product/service pages, research sources, and policy pages.

**Skill prompt:**

```text
Extract the page into valid JSON only. Use this schema: {"title":"","url":"","source_type":"article|documentation|product|job|other","published_or_updated":"","summary":"","key_facts":[{"label":"","value":"","evidence":""}],"constraints":[""],"actions":[{"action":"","owner":"stated|unassigned","due":"stated|none"}],"unknowns":[""],"confidence":"high|medium|low"}. Preserve exact figures, dates and named entities. Do not infer missing facts; add them to unknowns. No markdown or commentary.
```

**Acceptance tests:**

- Output parses as valid JSON.
- Figures, dates, named entities, and URL are not fabricated.
- Missing material is represented under `unknowns`.

**Do not use:** When the desired outcome is a nuanced narrative synthesis rather than a compact source extraction.

### 6.2 `🔎 research-brief`

**Problem solved:** Long pages need a concise, decision-ready summary that separates evidence from inference.

**Use on:** Articles, research pages, release notes, documentation, policy pages, and product announcements.

**Skill prompt:**

```text
Create a decision-ready research brief from this page. Output: 1) Bottom line (max 2 sentences); 2) Key claims (3-5 bullets); 3) Supporting evidence with exact figures, dates, or quoted wording where available; 4) Limitations, uncertainty, or missing information; 5) Practical next action. Separate page facts from your inference. Do not invent sources or evidence.
```

**Acceptance tests:**

- A normal article produces a brief that fits on one screen.
- Facts are separated from inference.
- Weak or incomplete evidence produces at least one stated limitation.

**Do not use:** When the output must be machine-readable; use `📦 to-json` instead.

### 6.3 `🔎 compare-tabs`

**Problem solved:** Comparing several browser pages manually is slow and often produces invalid apples-to-oranges conclusions.

**Use on:** Comparable tools, services, APIs, courses, plans, products, providers, or research sources.

**Skill prompt:**

```text
Compare the selected tabs for this decision: [STATE DECISION]. First identify the common comparison criteria supported by the pages. Output a markdown table: Option | Price/Cost | Relevant capabilities | Constraints | Evidence/Source | Unknowns. Then give: Best fit, strongest alternative, deal-breakers, and the single most useful next verification. Preserve currency, units, dates, plan tiers, and material exclusions exactly. Do not rank options if the decision criterion is missing; ask for it.
```

**Acceptance tests:**

- It compares only genuinely common fields.
- It does not invent a score or rank where the decision criterion is absent.
- It surfaces unknowns and disqualifying constraints.

**Do not use:** For unrelated pages or a single-page task.

### 6.4 `🎯 job-fit`

**Problem solved:** Job descriptions need an evidence-led assessment against a supplied profile, not a generic encouragement response.

**Use on:** Seek, LinkedIn, Indeed, organisation job pages, and graduate/internship listings.

**Skill prompt:**

```text
Assess this job description against the candidate evidence supplied in this chat or on the page. Extract each required and preferred criterion. Output a table: Criterion | Required/Preferred | Evidence supplied | Match (Strong/Partial/Missing/Unknown) | Gap or verification needed. Do not claim experience that is not explicitly evidenced. Then state: critical missing requirements, strongest evidence to foreground, and 1-3 honest next actions. If no candidate profile is supplied, ask for it before assessing fit.
```

**Optional short candidate profile:**

```text
Candidate evidence: student; Python, shell, HTML, JavaScript and JSON; AI-agent workflows; automation and API integrations; data extraction and visualisation; GitHub, macOS, Windows and Linux; projects include communication analysis, career support, extraction pipelines, and interactive visualisation.
```

**Acceptance tests:**

- It distinguishes supplied evidence from assumed experience.
- It does not fabricate achievements or qualifications.
- Missing candidate input leads to a clarification request rather than a conclusion.

**Do not use:** For generating a tailored application, cover letter, or CV rewrite; that should be a separate explicitly requested activity.

### 6.5 `🎯 repo-triage`

**Problem solved:** GitHub issues and PRs often hide the actual decision, validation state, and next action among comments and diff summaries.

**Use on:** GitHub pull requests, issues, discussions, release pages, and project boards where visible content is sufficient.

**Skill prompt:**

```text
Triage this GitHub page for a maintainer. Output: Type and status; decision requested; concise problem/change summary; affected components/files visible on the page; evidence of tests or validation; risks, regressions, migrations, or unanswered questions; recommended next action (review, request changes, merge, comment, defer). Distinguish confirmed facts from assumptions. Do not recommend merge if visible validation is absent; mark conditional instead.
```

**Acceptance tests:**

- It does not infer files, validation, or implementation details that are not visible.
- It provides one next action and any conditions required for it.

**Do not use:** When the essential diff, test logs, or security context are inaccessible; use it only as preliminary triage.

### 6.6 `✍️ action-items`

**Problem solved:** Commitments, decisions, unanswered questions, dates, and amounts are often lost in long threads or pages.

**Use on:** Project threads, meeting notes, correspondence pages, planning documents, and issue discussions.

**Skill prompt:**

```text
Extract only explicit commitments, decisions, open questions, and deadlines from this page or thread. Output four sections: Actions (task | owner stated/unassigned | due stated/none); Decisions; Open questions (who must answer); Dates and financial commitments. Preserve wording for any deadline, amount, or condition. Do not assign an owner, due date, or obligation that the source does not state.
```

**Acceptance tests:**

- It does not convert an idea or suggestion into an assigned obligation.
- Uncertain ownership is shown as `unassigned`.

**Do not use:** As a replacement for legal, contractual, or financial interpretation.

### 6.7 `✍️ reply-options`

**Problem solved:** A message may require a short calibrated response, not a lengthy rewrite.

**Use on:** Email, chat, forum, support, collaboration, and follow-up contexts.

**Skill prompt:**

```text
Draft three concise replies to this message: 1) accept/agree, 2) decline or defer, 3) clarify before deciding. Preserve factual constraints and stated deadlines. Match the sender’s tone without becoming overly formal, apologetic, or confrontational. Each option must contain one clear next step and stay under 100 words.
```

**Acceptance tests:**

- The three options differ in decision outcome, not only phrasing.
- It invents no availability, commitment, reason, or factual detail.

**Do not use:** For sending replies automatically or for high-stakes communications without review.

### 6.8 `🧩 refine-prompt`

**Problem solved:** Prompts become bloated and unclear when they blend task, context, rules, tools, formatting, and evaluation.

**Use on:** Draft system prompts, user prompts, Chrome Skills drafts, agent instructions, and project handovers.

**Skill prompt:**

```text
Refine this prompt for reliable execution. First identify only material ambiguities, missing inputs, conflicting instructions, and untestable requirements. Then output: A) a minimal revised prompt; B) assumptions that still require user confirmation; C) an explicit output contract; D) 3 acceptance tests. Preserve intent. Remove redundant roles, repeated rules, decorative formatting, and steps without a measurable benefit. Do not add capabilities, tools, or workflow stages not requested.
```

**Acceptance tests:**

- The revised version is shorter or materially more operationally precise.
- Every added instruction has a measurable purpose.
- It does not introduce extra agents, connectors, workflow stages, or capabilities.

**Do not use:** To force a model-specific style adapter unless repeated model-specific failures demonstrate that one is needed.

### 6.9 `🧠 nalex-canonical` — Deferred pending source testing

**Problem solved:** Communication material needs an objective canonical record for the existing Nalex pipeline while maintaining strict separation between analysis and coaching.

**Use on:** Suitable transcripts, message exports, email threads, and other communication source material where access and privacy are appropriate.

**Skill prompt:**

```text
Create an objective canonical record of this communication source. Output: Participants; timeline; direct factual claims by speaker with short exact quotations; requests, commitments and stated outcomes; contradictions; missing context; observable communication patterns; severity (low/medium/high) only where supported by specific wording or behaviour. Separate Source facts, Reasoned interpretations, and Unknowns. Do not provide relationship coaching, legal advice, diagnosis, motive attribution, or invented context.
```

**Acceptance tests:**

- Facts, interpretations, and unknowns are clearly separated.
- It does not introduce diagnosis, legal conclusions, coaching, or motive attribution.
- Key factual claims contain short source quotations.

**Retention condition:** Retain only if it fits the established Nalex sequence: raw source -> canonical summary -> flattened visualisation schema -> final artifact.

## 7. Deferred, Merged, and Rejected Skills

The first library should not reproduce every plausible prompt transformation as a separate saved skill.

| Candidate | Decision | Reason |
|---|---|---|
| Executive summary | Merge into `🔎 research-brief` | The research brief is a more useful evidence-aware version. |
| Explain simply | Defer | Useful, but not yet a proven recurring browser workflow. |
| Extract specs | Merge into `📦 to-json` or `🔎 compare-tabs` | Extraction is a format, not necessarily a distinct repeated task. |
| Opposing view | Defer | Reliable counterargument needs broader evidence than one browser page provides. |
| Correct grammar | Defer | Editor assistance is usually lower-friction. |
| Shorten text | Defer | Can be a follow-up to a research brief or prompt refinement. |
| Summarise as table | Merge into `🔎 compare-tabs` | A table is a requested output format. |
| Create outline | Defer | Not a browser-specific repeated task yet. |
| Professional email | Merge into `✍️ reply-options` initially | Avoid overlap among communications prompts. |
| Friendly tone | Defer | A simple one-off transformation, not a proven standalone workflow. |
| Instant messaging adapter | Defer | Overlaps with communications rewrite needs. |
| Claude/Gemini/Copilot/AI Studio adapters | Replace with `🧩 refine-prompt` | Model-specific templates are brittle and should exist only after repeated proven model-specific failure. |
| API documentation extractor | Defer | Test `📦 to-json` and `🔎 research-brief` first. |

## 8. Build and Test Plan

### Phase 0: Verify live UI

Before saving any library at scale:

1. Open `chrome://skills/browse`.
2. Confirm the library is available in the active Chrome build.
3. Verify whether skills can be renamed, edited, described, searched, duplicated, exported, shared, and deleted.
4. Verify whether emoji work in names and whether they improve discovery.
5. Verify whether skills run on a current page only or support explicitly selected tabs, and confirm any tab limit.
6. Record only verified capabilities in the project documentation.

### Phase 1: Establish the core three

Test these three on real pages before creating anything else:

1. `📦 to-json` on an information-dense documentation/article page.
2. `🔎 research-brief` on a long article, release note, or policy page.
3. `🎯 job-fit` on a real job advertisement with the optional short candidate profile supplied.

For each test, record output quality, time saved, errors, ambiguity, and one prompt edit at most. If a prompt needs significant rework, do not save it yet.

### Phase 2: Add decision and triage skills

Once the core three are useful:

1. Test `🔎 compare-tabs` on three to five genuinely comparable pages.
2. Test `🎯 repo-triage` on one real GitHub issue and one real PR.
3. Test `✍️ action-items` on a project thread or planning page.
4. Retain, edit, merge, or delete based on observed outcomes.

### Phase 3: Add writing and prompt-design support

1. Test `✍️ reply-options` on low-stakes real correspondence.
2. Test `🧩 refine-prompt` on an existing Chrome Skill prompt and a project/agent prompt.
3. Add only if the outputs require less revision than starting manually.

### Phase 4: Sensitive specialised workflow

Test `🧠 nalex-canonical` only when appropriate source material, privacy handling, and pipeline requirements are confirmed. Do not treat it as a general relationship-coaching skill.

## 9. Test Log

Maintain this table in the repository or project notes.

| Skill | Test source | Expected outcome | Actual outcome | Time saved | Failure or ambiguity | Change made | Decision |
|---|---|---|---|---:|---|---|---|
| `📦 to-json` |  | Valid parsable extraction |  |  |  |  | Keep / edit / delete |
| `🔎 research-brief` |  | Decision-ready brief |  |  |  |  | Keep / edit / delete |
| `🔎 compare-tabs` |  | Comparable table and decision |  |  |  |  | Keep / edit / delete |
| `🎯 job-fit` |  | Evidence-led fit matrix |  |  |  |  | Keep / edit / delete |
| `🎯 repo-triage` |  | Maintainer next action |  |  |  |  | Keep / edit / delete |
| `✍️ action-items` |  | Explicit commitments only |  |  |  |  | Keep / edit / delete |
| `✍️ reply-options` |  | Three usable variants |  |  |  |  | Keep / edit / delete |
| `🧩 refine-prompt` |  | Smaller, testable prompt |  |  |  |  | Keep / edit / delete |
| `🧠 nalex-canonical` |  | Objective canonical record |  |  |  |  | Keep / edit / delete |

## 10. Peer Review Process

The library and this proposal must be reviewed as a compact design problem—not expanded through automatic multi-model accumulation. Each reviewer has a distinct role.

### Required review inputs

Provide each reviewer with:

- This proposal.
- The non-negotiable constraints below.
- The target success criteria.
- The test log, if any real tests have occurred.
- The live Chrome UI findings, if verified.

### Review architecture

| Stage | Reviewer | Role | Output |
|---|---|---|---|
| 1 | Claude Opus 5 | Lead strategic reviewer | Ranked critique, minimal redesign, tests |
| 2 | Gemini 3.1 Pro High | Independent auditor | Blind spots, failure examples, alternative approach |
| 3 | Claude Opus 5 | Reconciliation | Disagreement table, final minimal design |
| 4 | GPT-5.6 Terra | Policy and constraints gate | Pass/fail/conditional compliance table |
| 5 optional | GPT-5.6 Luna or GPT-5.4-Mini | Compression pass | Remove bloat and duplicated mechanisms |
| 6 optional | GPT-5.5 | JSON-schema validator | Validate JSON-only output contracts |

### Stage 1: Claude Opus 5 — principal strategic review

```text
You are the lead systems analyst reviewing the attached Gemini in Chrome Skills proposal and browser-prompt library.

Objective: maximise reliable, low-friction, browser-based outcomes while reducing overlap, unsupported assumptions, prompt bloat, and maintenance cost.

Reconstruct the proposal neutrally first. Then state the target users, real browser inputs, outputs, constraints, success criteria, and assumptions.

For every material finding, provide: proposal element; failure mechanism; conditions that expose it; practical impact on reliability, usefulness, cost, latency, or maintainability; severity (Critical/High/Medium/Low); confidence; concrete remedy; and a test.

Assess especially:
- Whether each skill has one input shape and one output contract.
- Whether Chrome Skills are being asked to do work outside browser-prompt capabilities.
- Hidden dependencies on user data, connectors, local files, tabs, or model memory.
- Overlap between skills and opportunities to merge or delete.
- Missing stopping rules, uncertainty handling, and validation criteria.
- Whether the library solves repeated real friction or merely anticipates use cases.
- Whether the naming and maintenance approach is genuinely low friction.

Compare the proposal against two simpler alternatives. Produce: ranked findings; a revised minimal library; a revised build/test sequence; and 5-8 measurable acceptance tests. Preserve useful intent but remove any step without a clear, testable benefit.

Clearly distinguish: document-supported evidence, strong inference, and hypothesis.
```

### Stage 2: Gemini 3.1 Pro High — independent audit

Run this without giving Gemini Claude’s conclusions.

```text
Independently audit the attached Gemini in Chrome Skills proposal and browser-prompt library. Do not use or defer to another reviewer’s conclusions.

Evaluate it for reliable, practical browser-based outcomes. Focus on blind spots a sympathetic reviewer may miss: hidden assumptions; failed access assumptions; long, messy, contradictory, sparse, and adversarial page content; false precision; trigger/name collisions; privacy and sensitive-content risk; output that looks rigorous but cannot be used; lack of measurable evaluation; and process complexity without demonstrated benefit.

For every finding state: relevant element; failure mechanism; an example page/input that exposes it; severity; confidence; practical fix; and a verification test.

Then provide: independent verdict; three highest-leverage changes; strongest case for retaining the current approach; a structurally different simpler alternative; and questions that cannot be resolved without live Chrome UI testing.

Do not criticise for its own sake. Prioritise changes with material effect on real-world quality, safety, and maintainability.
```

### Stage 3: Claude Opus 5 — reconciliation and final design

```text
You are reconciling a Gemini in Chrome Skills proposal after an independent review.

Inputs: original proposal; your principal review; Gemini’s independent audit; non-negotiable constraints; verified Chrome UI findings; and test cases with expected behaviour.

Create a disagreement table: Issue | Claude view | Gemini view | Evidence | Decision | Reason | Evaluation still needed.

Resolve using this priority order:
1. Direct evidence and verified platform capability.
2. Reproducible failure examples.
3. Expected effect on the user’s objective.
4. Simplicity and maintainability.
5. Theoretical elegance.

Do not force decisions where platform behaviour is unverified; turn them into small live tests. Output the final minimal skill set, prompt text, naming scheme, implementation sequence, and test protocol. Remove duplicate skills and procedural complexity that lacks a measurable benefit.
```

### Stage 4: GPT-5.6 Terra — policy and constraint gate

Terra is an enforcement layer, not a redesign layer.

```text
You are a policy and constraint checker for a Gemini in Chrome Skills library proposal.

You will receive: the final revised strategy; non-negotiable constraints and stop rules; and test cases with expected behaviour.

Check every retained skill, implementation step, and test against the constraints. Flag any instruction that could: imply unavailable access; fabricate evidence; perform or imply an irreversible action; blur analysis and coaching in sensitive communication material; create a misleading job-fit claim; or add unjustified procedural complexity.

For each row output: Step or Skill | Constraint | Pass/Fail/Conditional | Reason | Required Fix.

Then assess each test case as Measurable/Unmeasurable/Ambiguous, with a required correction where needed.

Do not redesign the library. Enforce guardrails and testability only.
```

### Stage 5: Optional GPT-5.6 Luna or GPT-5.4-Mini — compression

```text
You are a compression and de-bloat reviewer for the attached final Gemini in Chrome Skills strategy.

Identify redundant instructions, duplicate skills, repeated constraints, overlong names, and steps that exist only for completeness. Propose a minimal viable variant that retains the critical mechanisms and acceptance tests. For every deletion or merge, state the function preserved and why the removed element has no distinct measurable value.

Bias to simplicity. Do not add new skills, tools, roles, phases, or abstractions.
```

### Stage 6: Optional GPT-5.5 — JSON schema validation

```text
Review only the JSON-producing Gemini in Chrome Skills in the attached proposal.

For each, check: valid JSON syntax; consistent field naming; sufficient representation of unknown or absent data; unambiguous scalar versus array types; avoidance of unsupported metadata; and whether the schema is minimal for the stated downstream use.

Output: Skill | Validity risk | Schema issue | Minimal correction | Test input.

Do not redesign any non-schema instruction.
```

## 11. Approvals Plan

### Approval principles

No phase moves forward merely because a model recommends it. Human approval is required where a decision changes scope, creates saved artefacts, uses sensitive sources, or prepares any downstream irreversible action.

### Approval gates

| Gate | Decision | Evidence required | Approver |
|---|---|---|---|
| A: Proposal acceptance | Accept the scope, principles, review process, and initial candidate set | This document reviewed; unresolved issues listed | User |
| B: Review acceptance | Accept the reconciled minimal design | Claude/Gemini findings, Terra gate, unresolved tests | User |
| C: Core-skill creation | Save first three Skills in Chrome | Live UI checks and prompt acceptance tests | User |
| D: Expansion | Add skills 4-8 | Test log shows recurring value and no unresolved critical failure | User |
| E: Nalex activation | Permit testing/saving `🧠 nalex-canonical` | Privacy, source suitability, and pipeline-boundary review | User |
| F: Deprecation/merge | Delete, replace, or merge a saved Skill | Test log and replacement rationale | User |

### Safety stop rules

Stop and obtain explicit approval before any workflow:

- Sends a message, submits a form, creates or changes a record, creates a calendar item, commits code, posts publicly, spends money, or deletes data.
- Uses sensitive communications, personal information, financial information, legal material, credentials, health information, or other restricted source content.
- Converts an analysis outcome into a recommendation that could materially affect a person, dispute, remedy, employment application, or financial decision without human review.
- Assumes access to a connector, private file, repository, tab, or account that is not visibly available in the active environment.

## 12. Implementation Plan

### Step 1: Create project record

- Store this document as `docs/gemini-in-chrome-custom-gemini-skills-rework.md` in the active repository or a durable project folder.
- Create a companion `docs/chrome-skills-test-log.md` using the test-log table above.
- Record the Chrome version, operating system, Gemini plan/access level, and current UI observations.

### Step 2: Verify Chrome Skills UI

- Open `chrome://skills/browse`.
- Confirm the actual save/edit/search/delete workflow.
- Confirm how `/` discovery behaves.
- Confirm any tab-selection behaviour before writing multi-tab instructions into final prompts.
- Do not rely on unverified UI features.

### Step 3: Execute peer review

- Run the Stage 1 Claude Opus 5 review.
- Run the Stage 2 Gemini 3.1 Pro High audit independently.
- Run the Stage 3 Claude reconciliation.
- Run the Stage 4 GPT-5.6 Terra constraint gate.
- If the result still feels heavy, run the optional Stage 5 compression review.
- If JSON schemas survive to the final set, run Stage 6 validation.

### Step 4: Approve the minimal release

At Gate B, approve only a final set with six to eight retained skills, no unresolved critical issue, and clear live-test requirements.

### Step 5: Test before saving

Test the final prompts in a normal Gemini in Chrome conversation on real representative sources. For each prompt:

- Use three sources with different levels of clarity or completeness.
- Compare output against the acceptance tests.
- Make at most one evidence-driven prompt revision before re-testing.
- Record actual result, time saved, failure, and decision in the test log.

### Step 6: Save the first three skills

After Gate C approval, save:

1. `📦 to-json`
2. `🔎 research-brief`
3. `🎯 job-fit`

Use the final reviewed text, short names, and a one-line description if the live UI supports descriptions.

### Step 7: Expand only on proof

Add the remaining approved skills one by one:

- `🔎 compare-tabs`
- `🎯 repo-triage`
- `✍️ action-items`
- `✍️ reply-options`
- `🧩 refine-prompt`
- `🧠 nalex-canonical` only after its specialised approval gate

Retain only skills that repeatedly reduce friction. Merge or delete unused or overlapping skills during monthly review.

### Step 8: Maintain

Perform a monthly 15-minute audit:

- Review actual use and test-log evidence.
- Fix one observed failure at a time.
- Merge overlapping skills.
- Delete skills unused for a meaningful period unless they support a genuinely occasional high-value workflow.
- Update this proposal when a platform capability or workflow assumption is proven wrong.

## 13. Completion Criteria

Implementation is complete when:

- The proposal has passed the agreed review and approval gates.
- The Chrome Skills UI capabilities have been documented from live use.
- Six to eight Skills have been tested on real sources and saved only after passing acceptance tests.
- JSON-producing Skills have produced parseable output on three diverse sources.
- Job-fit results use only explicit candidate evidence.
- Nalex outputs, if enabled, separate facts, interpretations, and unknowns, and avoid coaching/legal/diagnostic claims.
- No saved prompt implies connector execution, hidden access, automatic sending, or irreversible action.
- The test log documents keep/edit/delete decisions.
- The library is compact, searchable, and maintained as a set of proven high-value workflows rather than a catalogue of speculative prompts.
