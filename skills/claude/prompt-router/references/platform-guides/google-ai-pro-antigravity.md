---
platform: Google Antigravity
authentication: Google account
plan: Google AI Pro
last_verified: 2026-11-23
status: account-observed-with-documentation-caveat
---

# Google Antigravity with Google AI Pro

## Models confirmed selectable in this user's Antigravity environment

The user explicitly confirms that the following frontier models and reasoning effort levels are accessible and selectable in the model selector menu and CLI (`agy models`) under their Google AI Pro account (verified 2026-11-23):

| Model Display Name | CLI Model Identifier(s) | Effort Levels | Status |
|---|---|---|---|
| **Gemini 4 Neon** | `gemini-4-neon-low`, `gemini-4-neon-medium`, `gemini-4-neon-high`, `gemini-4-neon-xhigh` | Low, Medium, High (default), Extra (`xhigh`) | Selectable (`New`) |
| **Gemini 4 Argon** | `gemini-4-argon-low`, `gemini-4-argon-medium`, `gemini-4-argon-high` | Low, Medium (default), High | Selectable (`New`) |
| **Gemini 4 Hydrogen** | `gemini-4-hydrogen-low`, `gemini-4-hydrogen-medium`, `gemini-4-hydrogen-high`, `gemini-4-hydrogen-xhigh` | Low, Medium, High (default), Extra (`xhigh`) | Selectable (`New`) |
| **Gemini 3.8 Flash** | `gemini-3.8-flash-low`, `gemini-3.8-flash-medium`, `gemini-3.8-flash-high` | Low, Medium, High (default) | Selectable (current default) |
| **Claude Opus 5.5** | `claude-opus-5-5-low`, `claude-opus-5-5-medium`, `claude-opus-5-5-high` | Low, Medium (default), High | Selectable (`New`) |
| **Claude Sonnet 5.5** | `claude-sonnet-5-5-low`, `claude-sonnet-5-5-medium`, `claude-sonnet-5-5-high` | Low, Medium (default), High | Selectable (`New`) |
| **GPT-OSS 120B** | `gpt-oss-120b-medium` | Medium | Selectable (`Notice`) |
| **Orchestrator (Neon)** | `gemini-pro-orchestrator-neon` | Fixed configuration | Selectable (Neon planner + Hydrogen executor) |
| **Orchestrator (Argon)** | `gemini-pro-orchestrator-g1-pro` | Fixed configuration | Selectable (Argon planner + Hydrogen executor) |
| **Orchestrator (Claude Opus 5.5)** | `claude-opus-5-5-orchestrator` | Low, Medium (default), High | Selectable via Orchestrator flyout submenu |
| **Gemini 4 Carbon** | `gemini-4-carbon` | N/A | **Unavailable** (`Unavailable ⓘ` in UI; excluded from CLI) |
| **Orchestrator (Carbon)** | `gemini-4-carbon-orchestrator` | N/A | **Unavailable** on Google AI Pro |

## Inaccessible models on Google AI Pro

1. **Gemini 4 Carbon & Carbon Orchestrator**:
   - `Gemini 4 Carbon` is displayed in the UI dropdown with the badge **`Unavailable ⓘ`** and cannot be selected.
   - `Orchestrator (Carbon)` is not present in the Orchestrator flyout submenu or in the `agy models` output.
   - **Reason**: Official Antigravity documentation restricts Gemini 4 Carbon and Carbon Orchestrator to **Google AI Ultra** subscriptions and **Gemini Enterprise** accounts authenticated via Application Default Credentials (`AGY_ADC_AUTH`).
   - **Remedy**: Upgrade subscription to Google AI Ultra via [Google One Support / Plans](https://one.google.com/support), or sign in with an enterprise GCP account via `gcloud auth application-default login` (`AGY_ADC_AUTH=1`).

## Orchestrator layout & multi-model role selection

- In the Antigravity UI model selector, Orchestrator appears as a single unified row (`Orchestrator Gemini 4 Neon Extra ...`).
- Hovering over the Orchestrator row opens a planner flyout submenu displaying the planners available on the account:
  - `Gemini 4 Neon Medium`
  - `Gemini 4 Argon Medium`
  - `Claude Opus 5.5 Medium`
- Each planner option opens a secondary submenu allowing the user to select the planner reasoning effort level (`Low`, `Medium`, `High`, and `Extra` for Neon).
- In the Antigravity CLI (`agy`), `--model "Orchestrator (Neon)"` or `--model "gemini-pro-orchestrator-neon"` selects Neon Orchestrator; `--model "Orchestrator (Argon)"` or `--model "gemini-pro-orchestrator-g1-pro"` selects Argon Orchestrator. Effort is not adjustable via `/effort` for fixed Gemini orchestrators.

## Prompting recommendations for Google AI Pro users

- **For complex day-to-day coding**: Use **`Orchestrator (Neon)`** as the default. It leverages Gemini 4 Neon's frontier judgment for planning and architecture while delegating routine code generation and test execution to Gemini 4 Hydrogen.
- **For cross-vendor agent workflows**: Use **`Orchestrator (Claude Opus 5.5)`** to leverage Anthropic's adaptive reasoning and visual diagram understanding for architecture, paired with Hydrogen or Sonnet 5.5 execution.
- **When maximum test-time compute is needed without Ultra**: Select standalone **`Gemini 4 Neon`** with **`Extra` effort** (`gemini-4-neon-xhigh` / `--effort xhigh`) or **`Claude Opus 5.5`** with **`High` effort** (`claude-opus-5-5-high`).
- **For fast, zero-planning edits**: Select **`Gemini 4 Hydrogen`** or **`Gemini 3.8 Flash`** directly.

## Sources
- https://antigravity.google/docs/models/ — official Antigravity Models documentation: model matrix, plan availability (Ultra vs. Pro vs. Free), and Orchestrator pairing rules.
- Local Antigravity CLI v2.0 binary and runtime introspection (`agy models`, `orchestrator-model-roles`).
- User-provided UI selector snapshot (`media_1795408294766_c67662ce.jpg`).
