# Phase plan

## Phase 1 — Antigravity / cloud (current)

**Goal:** Build the knowledge foundation and first working skill cards using cloud tools.

**Primary IDE:** Antigravity IDE (Gemini 3.1 Pro High)
**Secondary:** Claude Code (agentic file editing, critique, review)
**Version control:** GitHub — okgoogle13/prompt-skills-library

**Focus areas:**
- Ingest and normalize all 6 foundation sources
- Create first skill cards for `chrome-gemini`, `claude`, and `antigravity` surfaces
- Build out `skills/chrome-gemini/` for immediate Gemini in Chrome use
- Establish eval baseline with at least one test case per approved skill

**Conventions for Phase 1 artifacts:**
- Set `surface: chrome-gemini` or `surface: claude` or `surface: antigravity`
- Set `local_llm_safe: false` on all skill cards until explicitly adapted
- Always fill `local_llm_notes` with what would need to change for local model use
- This ensures Phase 2 adaptation is low-friction

**Done when:**
- All 6 foundation sources are normalized in `knowledge/`
- At least 5 approved skill cards exist across chrome-gemini, claude, and antigravity surfaces
- At least 1 eval test case per approved skill
- Source registry statuses updated

---

## Phase 2 — VS Code + local LLM (next laptop)

**Goal:** Move primary editing to VS Code, begin local model testing.

**Primary IDE:** VS Code
**Extensions:** Continue.dev, GitLens, YAML, Markdown All in One
**Local model stack:** Ollama + Continue.dev (or LM Studio)
**Version control:** Same GitHub repo — no migration needed

**Focus areas:**
- Clone existing repo in VS Code — no changes needed
- Install Continue.dev and connect to Ollama
- Adapt `local_llm_template` fields in existing skill cards
- Test `skills/local-llm/` variants against real local models
- Update `local_llm_safe` flags and `eval_status` based on real results

**Transition checklist:**
- [ ] New laptop provisioned
- [ ] VS Code installed with Continue.dev, GitLens, YAML extensions
- [ ] Ollama installed and at least one model pulled (e.g. llama3, mistral, qwen)
- [ ] Repo cloned and Continue.dev connected to local model endpoint
- [ ] First local skill card tested and eval result recorded

---

## Tool roles (both phases)

| Tool | Role |
|---|---|
| Antigravity IDE | Orchestration, Gemini sessions, MCP host |
| Claude Code | Agentic file editing, critique, review |
| Gemini in Chrome skills | Browser runtime, immediate page tasks |
| Firecrawl | Source ingestion and extraction |
| VS Code + Continue.dev | Phase 2 primary IDE + local model testing |
| Perplexity | External verification, capability research |
| GitHub | Version control, canonical source of truth |
