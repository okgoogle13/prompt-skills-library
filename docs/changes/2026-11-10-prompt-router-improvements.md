# Change Note — Prompt-Router Improvements

Plan: `research/prompt-router-research-plan.md`  
Target skill files: `~/.claude/skills/prompt-router/references/patterns.md`

---

## Phase 1 — `optimise` Route and Shared Patterns (2026-11-10)

### Decision

Applied 3 surgical changes to `prompt-router/references/patterns.md` (§1, §2.1, §2.2, §2.5). `prompt-router/SKILL.md` was left unchanged because Step 5 already delegates `optimise` to `PATTERNS` §1 and §2, and Step 6's fixed 4-part output contract was preserved.

1. **Literal non-normalisation & pre-return check (`patterns.md` §1, §2.1):**
   - Forbade normalising path separators (`\` vs `/`), shell quoting, CLI flags, URL query strings, identifier casing, or schema keys unless explicitly asked.
   - Replaced `Material-improvement check` with a 3-part `Pre-return check (before returning)` verifying material improvement, exact survival of all original requirements and literal tokens (§1), and zero unrequested deliverables/workflow stages/constraints.
2. **Scope boundary & missing-vs-unknown handling (`patterns.md` §2.1):**
   - Restricted `optimise` to the requested task; required unknown material details to be converted into `[ASSUMPTION: …]` rather than invented requirements; forbade unrequested deliverables, audiences, workflows, personas, compliance/security regimes, or arbitrary thresholds.
3. **Narrow `Done when` & defect-anchored changelog (`patterns.md` §2.2, §2.5):**
   - Updated `Done when` to require a runnable command where one exists or the narrowest checkable condition supported by the request (never inventing metrics, thresholds, or review stages).
   - Required `§2.5` changelog `What → Why` entries to name the concrete defect fixed (`§2.2–§2.3`) or a guide fact, banning generic `"improved clarity"` / `"better structure"` justifications.

*Rejected from raw report:* Adding top-level `Preserved literals:` or `Optional improvement:` output blocks that would break `prompt-router/SKILL.md` Step 6's output contract.

### Evidence

- Research report: `research/01-router-optimise-improvements.md` (1 `pplx_deep_research` call, `source_focus="web"`).
- Tier 1 vendor guidance (Anthropic prompting best practices, Skill authoring best practices, OpenAI prompt engineering/generation, Google prompt design strategies) and Tier 2 benchmark evidence (AGENTIF, NeurIPS 2025).
- Model-guide integration preserved: `optimise` still resolves via the compact registry in `migrate-prompt/SKILL.md` and lazy-loads only one target guide (`model-guides/<target-id>.md`), with target-guide precedence (§0 Rule 1) intact.

### Validation Result

**Passed (6/6)** in isolated subagent runs against the updated `prompt-router/references/patterns.md` and `prompt-router/SKILL.md`:

| # | Case | Target Model | Result |
|---:|---|---|---|
| 1 | Ambiguous task | `claude-sonnet-5-5` | Pass |
| 2 | Missing success criterion | `gpt-5` | Pass |
| 3 | Missing constraint | `claude-opus-5-5` | Pass |
| 4 | Vague output format | `gemini-3.8-flash` | Pass |
| 5 | Scope-creep risk | `gemini-4-argon` | Pass |
| 6 | Literal code, path, command, or URL preservation | `claude-sonnet-5-5` | Pass |

### Revert Plan

- `prompt-router/references/patterns.md` lives outside this repository (`~/.claude/skills/prompt-router/references/patterns.md`); revert the 3 hunks directly via edit or restore from the exact pre-change text recorded in the Phase 1 diff (§1 `Preserve exactly`, §2.1 `Material-improvement check`, §2.2 `Done when`, §2.5 `Changelog`).
- `research/prompt-router-research-plan.md` and `docs/changes/2026-11-10-prompt-router-improvements.md`: revert via Git (`git checkout --` / `rm` if untracked).


---

## Phase 2 — `write` and `review` Routes and Shared Patterns (2026-11-11)

### Decision

Applied 3 surgical changes to `~/.claude/skills/prompt-router/references/patterns.md` (§3, §6). `prompt-router/SKILL.md` was left unchanged because Step 5 already delegates `write` to `PATTERNS §1 and §6` and `review` to `PATTERNS §1 and §3`, and Step 6's fixed output contracts were preserved.

1. **Review materiality gate & root-cause merging (`patterns.md` §3):**
   - Added a pre-checklist materiality gate requiring each finding to connect an affected instruction or task-relevant omission to a plausible material failure and smallest fix.
   - Explicitly stated that missing headings, examples, personas, numeric targets, or schemas are not defects on their own, forbade inventing new objectives/acceptance criteria, and required merging same-root-cause findings.
   - Clarified in the §3 Output block that `Fix first` requires a material problem (`LOW`-only remains `Ready`, meaning no material defect found in the supplied prompt/context).
2. **Bounded observable success & proportional scaffolding (`patterns.md` §6):**
   - Required identifying the deliverable and a task-relevant, observable success condition entailed by the sketch before drafting (qualitative unless the user supplied numbers), without inventing facts, thresholds, priorities, tools, or extra deliverables.
   - Clarified that the 5-part table rows are coverage checks rather than mandatory visible headings, and that `Verification` and examples are conditional on adding a meaningful check or resolving concrete ambiguity.
3. **Shape vs. substance consistency check (`patterns.md` §3, §6):**
   - Updated §3 item 1 to check instruction/example agreement and separate output-format validity from whether supplied inputs support requested claims/values.
   - Added a pre-return consistency check in §6 verifying instruction/format/example agreement and input support (`{{vars}}` treated as intentional slots), specifying minimal shape/fields/missing-data behaviour for machine-consumed output with `[ASSUMPTION: …]` kept outside code/JSON syntax and no false schema-compliance guarantees.

*Rejected from raw report:* Adding separate `write-prompt`/`review-prompt` skills, numerical scoring rubrics, mandatory 5-heading templates, or a rewrite of the `write` clarification threshold.

### Evidence

- Research report: `research/02-router-write-review-improvements.md` (1 `pplx_deep_research` call, `source_focus="web"`).
- Tier 1 vendor sources (Anthropic defining success criteria & effective context engineering, Google prompt design strategies & introduction to prompting, OpenAI Model Spec & Structured Outputs).
- Model-guide integration preserved: `write` still resolves one concrete target via `MIGRATE` and loads one guide; `review` loads a guide only when a concrete model is named (0 guides for host-only requests).

### Validation Result

**Passed (6/6)** against the updated `prompt-router/references/patterns.md`:

| # | Case | Route & Target | Result |
|---:|---|---|---|
| 1 | Rough notes to a usable prompt | `write`; `claude-sonnet-5-5` | Pass |
| 2 | Ambiguous task requiring one clarification | `write`; `claude-sonnet-5-5` | Pass |
| 3 | Missing success criterion | `write`; `claude-sonnet-5-5` | Pass |
| 4 | Vague output format | `write`; `claude-sonnet-5-5` | Pass |
| 5 | Review identifying material weaknesses without nitpicking | `review`; `claude-sonnet-5-5` | Pass |
| 6 | Review avoiding unrequested requirements | `review`; host-only `Claude Code` (0 guides) | Pass |

### Revert Plan

- Revert the 3 hunks in `~/.claude/skills/prompt-router/references/patterns.md` (§3 materiality gate & item 1 & Output note; §6 pre-drafting success rule, coverage-check phrasing, and pre-return consistency check) directly via edit.

---

## Phase 3 — Router Portability and Model-Guide Integration (2026-11-14)

### Decision

Applied 3 portable-core edits to `~/.claude/skills/prompt-router/SKILL.md` (`## Files`, `## Step 1`, `## Step 3`, `## Step 4`). Kept `migrate-prompt/SKILL.md` and `migrate-prompt/model-guides/` in place rather than relocating guides or collapsing `migrate-prompt` into a redirect.

1. **Portable `SKILL_DIR` resolution & exact-file-reader rule (`SKILL.md` `## Files`):**
   - Resolved `SKILL_DIR` from the loaded `SKILL.md` path first (with `${CLAUDE_SKILL_DIR}` if expanded, or `~/.claude/skills/prompt-router`), and allowed the host's direct file-reading tool (`Read`, `read_file`, or user-supplied file text) while preserving the strict ban on `Bash`, `glob`, `grep`, and search tools.
2. **Fail-closed gate for unreadable `MIGRATE` or `PATTERNS` (`SKILL.md` `## Step 4`):**
   - Required stopping immediately and naming the unreadable file if `MIGRATE` (in Step 3) or `PATTERNS` (in Step 4) cannot be read (e.g., on hosts without sibling-file access or web hosts without attached files), never falling back to guessed IDs, aliases, rules, or model facts from memory.
3. **Unexpanded `$ARGUMENTS` and `${CLAUDE_EFFORT}` handling (`SKILL.md` `## Step 1`, `## Step 3`):**
   - Treated bare unexpanded `$ARGUMENTS` invocation input as missing request/prompt (ask once and stop), while preserving `$ARGUMENTS` / `${CLAUDE_EFFORT}` inside prompt bodies as literal data, and ignored unexpanded `${CLAUDE_EFFORT}` placeholders from the host.

*Rejected from raw report:* Moving `migrate-prompt/model-guides/` into `prompt-router/references/`, gutting `migrate-prompt/SKILL.md` into a redirect, building a universal skill framework, or adding a Perplexity MCP router adapter.

### Evidence

- Research report: `research/03-router-portability.md` (1 `pplx_deep_research` call, `source_focus="web"`).
- Tier 1 vendor docs (Claude Code skills, Antigravity skills & discovery, Gemini CLI Agent Skills, OpenAI Codex skills & ChatGPT Projects/Custom GPTs, Perplexity Spaces/Projects) and Tier 3 implementation verification (`perplexity-web-mcp-cli` v0.16.1, local `~/.claude/skills/` structure).
- Model-guide integration preserved: `write`/`optimise`/`review` (concrete model) still load 1 guide; `migrate` loads 2 guides; `model-guides-combined.md` stays build-time only; no memory fallback.

### Validation Result

- **Offline integrity checks (`~/.claude/skills/migrate-prompt/`), re-run 2026-11-14:** `4/5` pass, **Check 3 FAIL**.
  1. Registry-to-guide 1:1 resolution: **Passed** (`85` unique registry IDs, `85` guide files, `0` missing, `0` unregistered).
  2. Valid guide frontmatter: **Passed** (`0` errors across all `85` guides).
  3. Combined-corpus source record: **FAIL** (originally recorded as N/A). The corpus exists at `~/Downloads/model-guides-combined.md` (81 guides); 4 registry IDs have no record in it: `gemini-4-argon-orchestrator`, `gemini-4-carbon`, `gemini-4-hydrogen`, `github-copilot`. Stays failed until the corpus gap is addressed separately.
  4. Unambiguous aliases: **Passed** (`0` normalised collisions across all `85` rows; cosmetic: `github-copilot` lists itself as an alias).
  5. Deprecated guide successor: **Passed with one documented exception** (`25` `status: legacy` guides; `gpt-4.1` has no successor and its guide documents that none exists).
- **Guide-count correction:** `research/03-router-portability.md` says 82 guides; the correct registry/guide count is **85** (the corpus lists 81).
- **8 portability & security validation cases (`evals/prompt-router-test-cases.md` Suite C):** Initially verified by inspection only; live results are in the Phase 4 section below.

### Revert Plan

- Revert the 4 contiguous hunks (+14/-5 lines across `## Files`, `## Step 1`, `## Step 3`, `## Step 4`) in `~/.claude/skills/prompt-router/SKILL.md` directly via edit.
- Revert `evals/prompt-router-test-cases.md`, `research/03-router-portability.md`, `research/prompt-router-research-plan.md`, and `docs/changes/2026-11-10-prompt-router-improvements.md` via Git (`git checkout --` / `rm` if untracked).


---

## Phase 4 — Placeholder defect fix and removal of migration scope (2026-11-14)

### Decision

1. **Placeholder defect (CRITICAL, introduced by Phase 3).** Claude Code substitutes the literal tokens for `$ARGUMENTS` and `${CLAUDE_EFFORT}` anywhere in a SKILL.md body. The Phase 3 rule text therefore had the user's input spliced into Step 1 (three times) and the effort placeholder replaced by a real value (`medium`) in Step 3, which would have suppressed a genuine effort request. Fix: the tokens are removed from `SKILL.md` and described in words (as `migrate-prompt` does); the host's separate trailing `ARGUMENTS:` block carries the input; a typed effort word is always a request, and only an unexpanded host placeholder is ignored.
2. **Migration scope removed from `prompt-router`** (user decision). Removed the migrate route, trigger text, examples, two-guide loading, and migrate output; one guide per run. `MIGRATE` is now `REGISTRY` (registry block and alias policy only); Guide-Stand/legacy-successor footer rules are inlined in `SKILL.md`. A one-line decline remains in Step 1 for "port X to Y" requests. `references/patterns.md` header edited accordingly.
3. **Eval cleanup:** removed `evals/evals.json` ids 4 and 5 (migrate cases); flipped the migrate trigger eval to `should_trigger: false`; removed Suite C case C7 and the two-guide invariant from `evals/prompt-router-test-cases.md`; changed C3's input to a real prompt (the original, `Check this SQL query: {{sql}}`, hit Step 1's not-a-prompt exit).
4. **Not done:** `migrate-prompt/` was **not archived**. It holds the registry and all 85 guides the router reads, and moving it would break the router. Decision pending.

### Evidence and validation (fresh subagents via the Skill tool; read traces self-reported)

| Case | Result |
|---|---|
| C1 | PASS: clean body, args as separate `ARGUMENTS:` block, 1 guide, `{{notes}}` verbatim |
| C2(b) | PASS: literal `$ARGUMENTS` preserved in the optimised prompt |
| C2(a) | PASS (rerun): bare invocation asked once for request and prompt, stopped, 0 files read |
| C3 | original input declined at Step 1 (test-design conflict, not a router defect). PASS on rerun with a real prompt: `Verdict: Fix first`, 4 findings, 1 guide (`claude-opus-5-5`), no effort setting or placeholder in output |
| C8 | PASS: route and target unchanged, 1 guide, no shell, injection flagged |
| A6 | PASS: exact command, path, URL and flags preserved |
| B5 | PASS: 2 material defects, 3 findings, no nitpicks, no rewrite |
| B6 | PASS: `Ready`, 0 guides, no invented requirements |

Not run: C4 (Antigravity/`agy`), C5/C6 (Perplexity/ChatGPT web; Codex), and the removed C7. Cross-host checks remain **unverified**.

### Revert Plan

- Phases 1–2: the pre-change text was never recorded (the Phase 1–2 revert plans above cannot be executed). The baseline is now the snapshot in `skills/claude/prompt-router/`, taken after the Phase 4 edits.
- Phase 3 pre-edit text: the diff in `research/03-router-portability.md` (extraction section 4) can be reversed by hand.
- Phase 4: restore `SKILL.md` from that Phase 3 diff plus the Phase 4 description above; the commit on branch `prompt-router-phase-1-3` is the recovery point going forward.
