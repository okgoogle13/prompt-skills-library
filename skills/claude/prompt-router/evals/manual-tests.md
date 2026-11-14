# Manual tests

## M1 — Prompt supplied in a follow-up turn

1. Send: `Optimise a prompt for Sonnet 5.5`.
2. Confirm the skill resolves `claude-sonnet-5-5`, asks once for the prompt, and reads no guide yet.
3. Send the prompt in the next message.
4. Pass if it continues with the resolved route/model, reads only `references/model-guides/claude-sonnet-5-5.md`, and preserves template variables.

## M2 — Adapt between two models

1. Ask to adapt a prompt from one exact model to another.
2. Confirm the source and target IDs resolve exactly.
3. Confirm only the two corresponding guides and `references/patterns.md` are read.
4. Pass if task intent and literal tokens survive, and only material target-specific changes are made.

## M3 — Missing guide

If a registry row points to a missing file, the skill must stop, state the missing guide, and ask for a valid model/guide. It must not search other directories or substitute model facts from memory.


## M4 — ChatGPT Go model picker

1. Ask to optimise a prompt for GPT-5.6 Luna in Codex CLI with ChatGPT Go.
2. Confirm the skill reads `gpt-5.6-luna.md` and `codex-cli-chatgpt-go.md`.
3. Pass if GPT-6 Luna, GPT-5.6 Terra and GPT-5.6 Luna are recorded as selectable in this user's account, while account-specific access is not generalized to all Go subscribers.

## M5 — Perplexity Pro model access

1. Ask to optimise a research prompt for GPT-6.1 Sol in Perplexity Pro.
2. Confirm the skill reads `gpt-6.1-sol.md` and `perplexity-pro.md`.
3. Pass if Perplexity research/citation behavior is kept separate from OpenAI API and Codex CLI features, and Perplexity access is not treated as ChatGPT Go or direct API entitlement.

## M6 — Portable paths and dependencies

1. Unpack the ZIP into a directory whose path contains no vendor-specific folder names.
2. Confirm all skill references resolve relative to `SKILL.md`.
3. Pass if no runtime instruction requires `${CLAUDE_SKILL_DIR}`, `~/.claude/skills`, a plugin cache, a specific shell, or a vendor-specific file-reading tool.


## M7 — Context and token bloat optimisation

1. Supply a long prompt containing repeated instructions, irrelevant history, duplicated examples, unique constraints, template variables and a strict output schema. Ask to reduce context and token bloat.
2. Pass if the skill separates prompt bloat from context bloat, removes duplication/noise, and preserves every unique requirement, literal token, variable and output contract.
3. Pass if it distinguishes measured token savings from estimates/qualitative reduction and does not invent a tokenizer result or context-window limit.

## M8 — Context compression with conflicting sources

1. Supply current and stale context notes with different dates and an explicit uncertainty/caveat. Ask for a compact context pack.
2. Pass if the result preserves source attribution, dates, conflict and uncertainty; it must not silently reconcile or discard the conflict.
3. Pass if it prioritises task-critical facts and constraints over background without inventing a token budget.
