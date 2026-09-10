# Backlog

## Phase 1 — Antigravity / cloud

### P1-001 Ingest Anthropic Claude prompting best practices
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- **Notes:** Scrape via Firecrawl, normalize to markdown, save to knowledge/canonical/anthropic/, update registry status to normalized

### P1-002 Ingest Anthropic llms.txt as crawl manifest
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://platform.claude.com/llms.txt
- **Notes:** Use as seed manifest to discover additional Claude docs pages for future ingestion

### P1-003 Ingest PromptQuorum build-a-prompt-library
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://www.promptquorum.com/prompt-engineering/build-a-prompt-library
- **Notes:** Extract 8-field schema, lifecycle model, and versioning rules into knowledge/library-design/

### P1-004 Ingest PromptQuorum fundamentals of prompt optimization
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://www.promptquorum.com/prompt-engineering/fundamentals-of-prompt-optimization
- **Notes:** Extract 6-lever optimization process and common mistakes into knowledge/library-design/

### P1-005 Ingest PromptQuorum prompt engineering for local models
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://www.promptquorum.com/local-llms/prompt-engineering-for-local-models
- **Notes:** Extract local model constraints and explicit structure rules into knowledge/local-llms/

### P1-006 Ingest Suedbroecker local LLM cheat sheet
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Source ref:** https://suedbroecker.net/2026/06/15/prompting-cheat-sheet-for-local-llms-and-autonomous-agents/
- **Notes:** Extract injection-safe patterns, trust boundary rules, and agent prompting notes into knowledge/local-llms/

### P1-007 Create first Chrome Gemini skill card: run-extract-page-claims
- **Status:** backlog
- **Phase:** 1
- **Surface:** chrome-gemini
- **Owner:** @okgoogle13
- **Source ref:** knowledge/canonical/anthropic/ (once ingested)
- **Notes:** Extract structured claims, evidence, and caveats from the current browser tab. First runtime skill card.

### P1-008 Create first Claude skill card: critique-prompt
- **Status:** backlog
- **Phase:** 1
- **Surface:** claude
- **Owner:** @okgoogle13
- **Notes:** Critique an existing prompt for ambiguity, missing constraints, and model assumptions

### P1-009 Create first Antigravity skill card: review-skill-card
- **Status:** backlog
- **Phase:** 1
- **Surface:** antigravity
- **Owner:** @okgoogle13
- **Notes:** Review a draft skill card for completeness, source tracing, and schema compliance

### P1-010 Add first eval test case
- **Status:** backlog
- **Phase:** 1
- **Surface:** repo
- **Owner:** @okgoogle13
- **Notes:** Add one realistic input/output pair to evals/ for the first approved skill card

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
