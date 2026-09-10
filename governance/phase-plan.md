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
- Do not create `.prompt.md` files yet — these are Phase 2 only
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
**Extensions (install on first open):** VS Code will prompt automatically via `.vscode/extensions.json`
- `redhat.vscode-yaml` — YAML schema validation against prompt-card and skill-card schemas
- `eamodio.gitlens` — inline git blame and version history for prompt artifacts
- `DavidAnson.vscode-markdownlint` — markdown consistency across knowledge/ files
- `esbenp.prettier-vscode` — format-on-save for YAML and markdown
- `yzhang.markdown-all-in-one` — table formatting, TOC, preview
- `Gruntfuggly.todo-tree` — surfaces TODOs across repo
- `humao.rest-client` — test Firecrawl and Ollama API calls in-editor
- `saoudrizwan.claude-dev` (Cline) — agentic file editing + local LLM + MCP tools

**Note:** Continue.dev was acquired by Cursor in June 2026 and is no longer actively developed.
Cline is the recommended replacement for local LLM agentic work in VS Code.

**Local model stack:** Ollama + Cline
**Version control:** Same GitHub repo — no migration needed

**Focus areas:**
- Clone existing repo in VS Code — extensions install automatically on first open
- Connect Cline to Ollama local model endpoint
- Adapt `local_llm_template` fields in existing skill cards
- Test `skills/local-llm/` variants against real local models
- Update `local_llm_safe` flags and `eval_status` based on real testing
- Create `.prompt.md` companions for approved skills (see `governance/prompt-file-spec.md`)

**Transition checklist:**
- [ ] New laptop provisioned
- [ ] VS Code installed — open repo, accept extension install prompts
- [ ] Ollama installed and at least one model pulled (recommended: llama3.2, qwen2.5-coder, mistral)
- [ ] Cline connected to local Ollama endpoint
- [ ] First local skill card tested and eval result recorded
- [ ] First `.prompt.md` created for top-used approved skill

---

## Tool roles (both phases)

| Tool | Role |
|---|---|
| Antigravity IDE | Orchestration, Gemini sessions, MCP host |
| Claude Code | Agentic file editing, critique, review |
| Gemini in Chrome skills | Browser runtime, immediate page tasks |
| Firecrawl | Source ingestion and extraction |
| VS Code + Cline | Phase 2 primary IDE + local model testing |
| Ollama | Phase 2 local model runtime |
| Perplexity | External verification, capability research |
| GitHub | Version control, canonical source of truth |
