# Model registry (active shortlist)

Generated from `model-guides/*.md` frontmatter with `tier: active`; the guide is authoritative. Match here first; on a miss read `model-registry-archive.md` once. Rows with Profile `unverified` are excluded from automatic recommendation.

| Model ID | Vendor | Family | Aliases | Last verified | Status | Successor | Profile |
|---|---|---|---|---|---|---|---|
| claude-fable-5-1 | Anthropic | Claude | `fable`, `fable-5.1`, `fable-5-1`, `claude-fable-5.1`, `fable5.1` | 2026-10-13 | current |  | Multi-hour agentic coding, knowledge-work artefacts, long-context research; dense prose, whole-file rewrites; nudge tool-call batching. |
| claude-haiku-5-5 | Anthropic | Claude | `haiku`, `haiku-5.5`, `claude-haiku-5.5`, `haiku5.5` | 2026-10-13 | current |  | High-volume classification, routing, extraction, sub-agents; at low effort skips checks and stops early. |
| claude-opus-5-5-orchestrator | Anthropic | Claude | `opus-5-5-orchestrator`, `opus-orchestrator`, `claude-opus-orchestrator`, `orchestrator-opus`, `orchestrator-claude-opus-5-5`, `opus-orch` | 2026-11-23 | current |  | Antigravity-only Opus planner with Hydrogen/Sonnet executor; spec-first multi-step work; overhead on minor edits. |
| claude-opus-5-5 | Anthropic | Claude | `opus`, `opus-5.5`, `claude-opus-5.5`, `opus5.5` | 2026-11-16 | current |  | Agentic coding, code review, long autonomous runs, knowledge work; may stop long tasks early. |
| claude-sonnet-5-5 | Anthropic | Claude | `sonnet`, `sonnet-5.5`, `claude-sonnet-5.5`, `sonnet5.5` | 2026-10-13 | current |  | Agentic coding that self-checks; asks before finishing at low/medium; unrequested extras at high effort. |
| deepseek-v4.1-flash | DeepSeek | DeepSeek | `deepseek-flash`, `v4.1-flash`, `deepseek-v4-1-flash` | 2026-10-13 | current |  | Agentic coding and maths; weak factual recall; JSON mode only, no schema. |
| gemini-4-argon-orchestrator | Google | Gemini | `argon-orchestrator`, `gemini-argon-orchestrator`, `gemini4-argon-orchestrator`, `orchestrator-argon`, `argon-orch`, `gemini-pro-orchestrator-g1-pro` | 2026-11-23 | current |  | Harness-only Argon planner with Hydrogen workers; spec-first cross-file refactors and migrations; heavy for trivial tasks. |
| gemini-4-argon | Google | Gemini | `gemini-4`, `argon`, `gemini-argon`, `gemini4`, `gemini4-argon`, `4-argon`, `argan` | 2026-11-05 | current |  | Deep reasoning for software engineering, multi-step agents, maths; slow at high; heavy for simple extraction. |
| gemini-4-carbon | Google | Gemini | `carbon`, `gemini-carbon`, `gemini4-carbon`, `4-carbon`, `carbon-4` | 2026-11-23 | current |  | Heavy compute and formal reasoning; unavailable on Google AI Pro Antigravity (requires Ultra or Enterprise ADC). |
| gemini-4-hydrogen | Google | Gemini | `hydrogen`, `gemini-hydrogen`, `gemini4-hydrogen`, `4-hydrogen`, `gemini-4-h2`, `gemini-hydrogen-4` | 2026-11-13 | current |  | Execution workhorse for code patches, tool calls, test loops; default high; xhigh raises tokens and latency. |
| gemini-4-neon-orchestrator | Google | Gemini | `neon-orchestrator`, `gemini-neon-orchestrator`, `gemini4-neon-orchestrator`, `orchestrator-neon`, `neon-orch`, `gemini-pro-orchestrator-neon` | 2026-11-23 | current |  | Antigravity Neon planner with Hydrogen executor; fixed effort; for features, fixes, refactoring. |
| gemini-4-neon | Google | Gemini | `neon`, `gemini-neon`, `gemini4-neon`, `4-neon`, `neon-4` | 2026-11-19 | current |  | Repo-level debugging and multi-file refactoring; paid tier only; xhigh overthinks simple prompts. |
| glm-5.3-flash | Z.ai | GLM | `glm-flash`, `glm-5.3-flashx`, `glm53-flash`, `zai-glm-5.3-flash`, `zai-org/GLM-5.3-Flash` | 2026-10-13 | current |  | Multimodal agent for visual render-compare loops; thinking always on; narrow effort enum. |
| gpt-6-astra | OpenAI | GPT | `astra`, `gpt6-astra` | 2026-10-13 | current |  | Complex end-to-end work, computer use; asks too often, over-tests, over-formats; grant autonomy explicitly. |
| gpt-6-luna | OpenAI | GPT | `luna`, `gpt6-luna`, `6-luna` | 2026-11-13 | current |  | Focused, repeatable high-volume tasks; keep prompts tightly bounded; not for difficult architecture work. |
| gpt-6-sol | OpenAI | GPT | `gpt6-sol`, `6-sol` | 2026-10-13 | current |  | Coding and agentic workflows; supports `none` effort; newer `gpt-6.1-sol` exists, review migration first. |
| gpt-6.1-sol | OpenAI | GPT | `sol`, `gpt6.1-sol`, `6.1-sol`, `gpt-6-1-sol` | 2026-10-13 | current |  | Complex coding, computer use, professional work; no `none` effort; Codex excludes Free and Go. |
| gpt-oss-120b | OpenAI | gpt-oss | `gpt-oss`, `gpt-oss-20b` | 2026-10-13 | current |  | Apache-2.0 open weights, Harmony format required; text only; effort set in system message. |
| qwen3.8-27b | Alibaba | Qwen | `Qwen/Qwen3.8-27B`, `Qwen/Qwen3.8-27B-FP8`, `qwen38-27b` | 2026-10-13 | current |  | Open-weight dense 27B vision-language for coding and office; self-hosted context 262K without YaRN. |
| qwen3.8-flash | Alibaba | Qwen | `qwen38-flash`, `qwen3-8-flash` | 2026-10-13 | current |  | Multimodal input, 1M window, OpenAI/Anthropic-compatible; thinking on by default; JSON mode needs keyword. |
