# Backlog

## Phase 1 — Antigravity / cloud

### P1-001 Ingest Anthropic Claude prompting best practices
- **Status:** backlog
- **Milestone:** M1
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- **Notes:** Scrape via Firecrawl, normalize to markdown, save to knowledge/canonical/anthropic/, update registry status to normalized
- **Depends on:** none
- **Done when:**
  - [ ] `knowledge/canonical/anthropic/claude-prompting-best-practices.md` exists with valid frontmatter (`source_url`, `retrieved_date`, `status: normalized`)
  - [ ] `sources/registry.md` entry for this source updated to `status: normalized`

### P1-002 Ingest Anthropic llms.txt as crawl manifest
- **Status:** backlog
- **Milestone:** M1
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://platform.claude.com/llms.txt
- **Notes:** Use as seed manifest to discover additional Claude docs pages for future ingestion
- **Depends on:** none
- **Done when:**
  - [ ] `sources/registry.md` has a `crawl-manifest` entry for `llms.txt` with status noted
  - [ ] At least 5 discovered sub-URLs listed as candidates for future ingestion

### P1-003 Ingest PromptQuorum build-a-prompt-library
- **Status:** backlog
- **Milestone:** M1
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://www.promptquorum.com/prompt-engineering/build-a-prompt-library
- **Notes:** Extract 8-field schema, lifecycle model, and versioning rules into knowledge/library-design/
- **Depends on:** none
- **Done when:**
  - [ ] `knowledge/library-design/promptquorum-build-a-prompt-library.md` exists with valid frontmatter (`status: normalized`)
  - [ ] 8-field schema explicitly identified and documented in the normalized file
  - [ ] `sources/registry.md` entry updated to `status: normalized`

### P1-004 Ingest PromptQuorum fundamentals of prompt optimization
- **Status:** backlog
- **Milestone:** M1
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://www.promptquorum.com/prompt-engineering/fundamentals-of-prompt-optimization
- **Notes:** Extract 6-lever optimization process and common mistakes into knowledge/library-design/
- **Depends on:** none
- **Done when:**
  - [ ] `knowledge/library-design/promptquorum-fundamentals-optimization.md` exists with valid frontmatter (`status: normalized`)
  - [ ] 6-lever optimization process and at least 3 common mistakes extracted and structured
  - [ ] `sources/registry.md` entry updated to `status: normalized`

### P1-005 Ingest PromptQuorum prompt engineering for local models
- **Status:** backlog
- **Milestone:** M1
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://www.promptquorum.com/local-llms/prompt-engineering-for-local-models
- **Notes:** Extract local model constraints and explicit structure rules into knowledge/local-llms/
- **Depends on:** none
- **Done when:**
  - [ ] `knowledge/local-llms/promptquorum-local-model-prompting.md` exists with valid frontmatter (`status: normalized`)
  - [ ] Local model constraints and explicit structure rules extracted and structured
  - [ ] `sources/registry.md` entry updated to `status: normalized`

### P1-006 Ingest Suedbroecker local LLM cheat sheet
- **Status:** backlog
- **Milestone:** M1
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://suedbroecker.net/2026/06/15/prompting-cheat-sheet-for-local-llms-and-autonomous-agents/
- **Notes:** Extract injection-safe patterns, trust boundary rules, and agent prompting notes into knowledge/local-llms/
- **Depends on:** none
- **Done when:**
  - [ ] `knowledge/local-llms/suedbroecker-local-llm-cheat-sheet.md` exists with valid frontmatter (`status: normalized`)
  - [ ] Injection-safe patterns and trust boundary rules explicitly structured in the file
  - [ ] `sources/registry.md` entry updated to `status: normalized`

### P1-007 Create first Chrome Gemini skill card: run-extract-page-claims
- **Status:** backlog
- **Milestone:** M2
- **Phase:** 1
- **Surface:** chrome-gemini
- **Owner:** @okgoogle13
- **Source ref:** knowledge/canonical/anthropic/ (once ingested)
- **Notes:** Extract structured claims, evidence, and caveats from the current browser tab. First runtime skill card.
- **Depends on:** P1-001 (knowledge foundation must exist before authoring skill cards)
- **Done when:**
  - [ ] `skills/chrome-gemini/run-extract-page-claims/skill-card.yaml` exists and validates against `schemas/skill-card.yaml`
  - [ ] `status: approved` — tested with at least 3 varied real browser inputs
  - [ ] `source_refs` points to at least one normalized knowledge artifact
  - [ ] `local_llm_safe: false` and `local_llm_notes` filled
  - [ ] At least 1 eval test case recorded (see P1-010)

### P1-008 Create first Claude skill card: critique-prompt
- **Status:** backlog
- **Milestone:** M2
- **Phase:** 1
- **Surface:** claude
- **Owner:** @okgoogle13
- **Notes:** Critique an existing prompt for ambiguity, missing constraints, and model assumptions
- **Depends on:** P1-001 (knowledge foundation must exist before authoring skill cards)
- **Done when:**
  - [ ] `skills/claude/critique-prompt/skill-card.yaml` exists and validates against `schemas/skill-card.yaml`
  - [ ] `status: approved` — tested with at least 3 varied prompts as input
  - [ ] `source_refs` points to at least one normalized knowledge artifact
  - [ ] `local_llm_safe: false` and `local_llm_notes` filled

### P1-009 Create first Antigravity skill card: review-skill-card
- **Status:** backlog
- **Milestone:** M2
- **Phase:** 1
- **Surface:** antigravity
- **Owner:** @okgoogle13
- **Notes:** Review a draft skill card for completeness, source tracing, and schema compliance
- **Depends on:** P1-001 (knowledge foundation must exist before authoring skill cards)
- **Done when:**
  - [ ] `skills/antigravity/review-skill-card/skill-card.yaml` exists and validates against `schemas/skill-card.yaml`
  - [ ] `status: approved` — tested with at least 3 varied draft skill cards as input
  - [ ] Uses XML tags in prompt body (Antigravity convention per CLAUDE.md)
  - [ ] `source_refs` points to at least one normalized knowledge artifact
  - [ ] `local_llm_safe: false` and `local_llm_notes` filled

### P1-010 Add first eval test case
- **Status:** backlog
- **Milestone:** M3
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Notes:** Add one realistic input/output pair to evals/ for the first approved skill card
- **Depends on:** P1-007 or P1-008 or P1-009 (at least one approved skill card must exist)
- **Done when:**
  - [ ] `evals/` contains at least one file with a realistic input and expected output pair
  - [ ] The eval file references the skill card it tests by ID
  - [ ] The tested skill card's `eval_status` field is updated to reflect the test result

## Phase 2 — VS Code + local LLM

### P2-001 Set up VS Code with Continue.dev and Ollama
- **Status:** backlog
- **Phase:** 2
- **Surface:** local-llm
- **Notes:** Install Continue.dev extension, connect to Ollama, test against a local model. Prerequisite: new laptop.

### P2-002 Adapt first local-llm skill card variant
- **Status:** backlog
- **Phase:** 2
- **Surface:** local-llm
- **Notes:** Take an approved chrome-gemini skill, fill local_llm_template field, test against Ollama

### P2-003 Review and update all local_llm_safe flags
- **Status:** backlog
- **Phase:** 2
- **Surface:** local-llm
- **Notes:** Audit all Phase 1 skill cards, update local_llm_safe and local_llm_notes fields based on real testing
