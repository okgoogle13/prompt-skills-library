---
platform: Codex CLI
authentication: ChatGPT account
plan: Go
last_verified: 2026-11-13
status: account-observed-with-documentation-caveat
---

# Codex CLI with ChatGPT Go

## Models confirmed selectable in this user's CLI

The user explicitly confirms that all three models below are selectable in the `/model` picker on their ChatGPT Go account. The screenshot shows the picker entries and GPT-6 Luna marked current; the user's clarification confirms that the two GPT-5.6 entries are also accessible.

| Model | CLI model ID | Status |
|---|---|---|
| GPT-6 Luna | `gpt-6-luna` | Selectable; shown as current in screenshot |
| GPT-5.6 Terra | `gpt-5.6-terra` | Selectable; user-confirmed |
| GPT-5.6 Luna | `gpt-5.6-luna` | Selectable; user-confirmed |
| GPT-6.1 Sol | `gpt-6.1-sol` | Not in the user's reported Go CLI picker |

This is account-specific observed availability as of 2026-11-13. Do not describe GPT-5.6 Terra or GPT-5.6 Luna as disabled or inaccessible. Do not generalize the user's observed access to every Go subscriber.

## Public documentation versus account-specific availability

OpenAI's public plan documentation may not enumerate every model exposed to every account during staged rollouts or client-specific updates. Where the user's live `/model` picker and explicit confirmation establish availability, record that as the account-specific fact. Keep any discrepancy with the public plan matrix visible rather than overriding the user's evidence.

## How to verify the account

1. Start `codex` while signed in with the ChatGPT Go account.
2. Run `/model` and record the models and reasoning levels shown.
3. Select a model and run `/status` to verify the active model.
4. Re-check after CLI updates or account rollouts.

A model ID in `--model` or `config.toml` does not grant entitlement. Do not infer access from an API model catalogue.

## Model selection guidance

- **GPT-6 Luna:** use for focused, repeatable and high-volume work: summarisation, extraction, classification, transformations and bounded coding tasks.
- **GPT-5.6 Terra:** use as the balanced everyday coding model for moderate multi-step changes, routine debugging, code review and test updates.
- **GPT-5.6 Luna:** use for quick, simple, repeatable tasks where latency and efficiency matter more than deep reasoning.
- **GPT-6.1 Sol:** do not assume it is available on Go. It is not in this user's reported picker and Go is excluded from the documented launch rollout.

## Codex CLI prompting and effort

For substantial repository work, specify:

- **Goal:** the concrete change or outcome.
- **Context:** relevant paths, code, docs, errors and reproduction steps.
- **Constraints:** project conventions, compatibility, scope and exclusions.
- **Done when:** observable checks such as tests, lint, build or reproduction results.

Keep small tasks small. Name the files or subsystem when known. Ask for a plan only when the task is broad or risky. Request verification proportionate to the change.

In CLI, use `/model` to select the model and its supported reasoning effort. Start with the displayed default. Increase effort for difficult debugging, planning, multi-file reasoning or careful review; higher effort costs more time and tokens. Do not assume API `reasoning.effort` values, API reasoning modes, speed tiers or context limits are identical to CLI controls. Ultra is a separate multi-agent mode, not just another reasoning-effort label.

## Sources

- https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt
- https://learn.chatgpt.com/docs/models?surface=cli
- https://learn.chatgpt.com/docs/codex/cli
