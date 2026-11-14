---
model: grok-4.3
vendor: xAI
family: Grok
aliases: [grok4.3, grok-4.3-latest, grok43, grok-4-3, grok4-3]
last_verified: 2026-10-13
status: current
---

# Grok 4.3

## Reasoning / Thinking
- Type: **can be switched off** — per the retirement table grok-4.3 is also run with `reasoning_effort: none` (on grok-4.5/4.6/4.7 reasoning cannot be disabled per the docs). Model page: supports `none | low | medium | high | xhigh`, **default `low`**. The retirement page names only four levels (none/low/medium/high), and the reasoning page does not list grok-4.3 and names `xhigh` only from grok-4.6 onward — so `xhigh` on 4.3 is (unverified) a real depth level. Per the retirement page, the non-reasoning slugs land on `none` and the reasoning slugs on `low`, with an explicit note to set `medium`/`high` explicitly if the task should think harder.
- **Always set `reasoning_effort` explicitly.** Default per the model page and best-practices guide is `low` ("`grok-4.3` defaults to `"low"` and also accepts `"none"`"); the guide asks to set the effort on every request so that no default decides the result.
- Class rules for xAI reasoning models (reasoning tokens are billed and reported as `reasoning_tokens` in usage; `presence_penalty`/`frequency_penalty`/`stop` cause an error) probably apply, but are not verified for grok-4.3 (unverified) — the reasoning page does not list the model. Treat defensively: omit these parameters.

## Prompting Style
- xAI describes the model as a "Fast, reliable model with strong tool calling and instruction following capabilities" — so prompt **directively and schema-driven**: clear instructions, clean tool/function definitions, no defensive prose re-explanation of the tools.
- Because the effort can drop to `none` and the default is only `low`, the prompt carries more of the load: state the goal, output form and tool policy explicitly rather than letting the model plan its own path.
- Enforce format via **Structured Outputs** rather than free-text conventions (Structured Outputs are explicitly confirmed for grok-4.3) — do not rely on `stop` sequences, which are generally excluded for xAI reasoning models (for grok-4.3 itself unverified).
- Positioning per the official listing: for code and chat xAI recommends grok-4.7, not 4.3. grok-4.3 is the cheap long-context throughput workhorse, not the reasoning peak.
- There is no dedicated developer/prompting page for grok-4.3; any further style claim is unverified.

## Strengths & Weaknesses (prompt-relevant)
- Strengths: **1M-token context** (twice that of grok-4.6/4.7 with 500k); cheaper than grok-4.6/4.7 ($1.25/$2.50 vs. $2.00/$6.00 per 1M — input −37.5%, output −58%); additional **EU region** (eu-west-1 alongside us-east-1/us-west-2) for data-residency requirements; a further 20% discount via the Batch API; xAI's own migration target for the deprecated Grok 4 Fast and legacy text slugs (`grok-4-fast-*`, `grok-4-1-fast-*`, `grok-3`) including `grok-4-0709` (exception: `grok-code-fast-1` → `grok-build-0.1`); a documented effort path down to `none`, which grok-4.5/4.6/4.7 do not have.
- Weaknesses/quirks: markedly lower throughput ceiling than the flagship (37 requests/s, 10M tokens/min vs. 150 rps / 50M tpm); **price cliff at 200k prompt tokens** — from there the doubled rate applies to ALL tokens of the request; not the model recommended for code/chat; no published knowledge cutoff, no published output limit, no official benchmark figures.

## Output & Format Conventions
- 1,000,000-token context window; input text + image, output text only. Max. output tokens: not published (unverified). Knowledge cutoff: not published (unverified).
- Function calling: yes; structured outputs: yes; reasoning: yes.
- Prices per 1M tokens: input $1.25 (<200k prompt) / $2.50 (≥200k), cached input $0.20 / $0.40, output $2.50 / $5.00; Batch API an additional −20%. Rate limits: 37 requests/s, 10M tokens/min; regions us-east-1, eu-west-1, us-west-2.
- Documented alias `grok-4.3-latest` alongside the bare id `grok-4.3`.

## Migration Notes
- **AWAY FROM grok-4.3** (to grok-4.7, which xAI recommends for code and chat, or to grok-4.6): `none` drops out — reasoning cannot be switched off there, so any zero-thinking fast path must be re-tuned to `low` and re-costed; the default jumps from `low` (4.3) to `high` (4.5/4.6/4.7) — without an explicit `reasoning_effort`, latency and reasoning cost rise; `xhigh` is real depth from grok-4.6 onward per the reasoning page; context shrinks from 1M to 500k; the EU region drops out (grok-4.6/4.7: us-east-1/us-west-2/us-central-1); the Batch API (20% discount on 4.3) is not served by grok-4.6 and grok-4.7 — re-plan batch jobs; add `prompt_cache_key` or `x-grok-conv-id` for cache-hit routing; price rises to $2.00/$6.00. On grok-4.7, `reasoning.encrypted_content` comes back on the Responses API with every answer — send reasoning items back unchanged.
- **TO grok-4.3** (from grok-4): this is xAI's **own prescribed target** — `grok-4-0709` was shut down on 15 May 2026, 12:00 PT, and has since been automatically routed to `grok-4.3` at `low` effort; an unchanged grok-4 integration therefore runs silently on shallower reasoning. Concretely: (1) set `reasoning_effort` explicitly — grok-4 did not know the parameter and always thought deeply (unverified — the grok-4 model pages are offline); if quality depended on that, set `medium`/`high` rather than accepting the routed `low`. (2) `none` is newly available — move latency-critical extraction/classification prompts to a single-pass call. (3) Context grows from 256k (per the Grok 4 announcement) to 1M, but the 200k price cliff doubles input **and** output for the whole request — chunking strategy matters more than raw capacity. (4) Costs fall markedly, but throughput is capped at 37 rps / 10M tpm — rebalance concurrency assumptions. (5) eu-west-1 becomes available. (6) Keep omitting `presence_penalty`/`frequency_penalty`/`stop`; control format via Structured Outputs.

## Sources
- https://docs.x.ai/developers/models/grok-4.3 — model page: id `grok-4.3` + alias `grok-4.3-latest`, blurb "Fast, reliable model with strong tool calling and instruction following capabilities", 1M context, text+image→text, function calling/structured outputs/reasoning yes, efforts `none`/`low`/`medium`/`high`/`xhigh` with default `low`, full price table incl. cached input and 20% batch discount, 37 rps / 10M tpm, regions us-east-1/eu-west-1/us-west-2; no prompting guidance, no cutoff, no output limit.
- https://docs.x.ai/developers/migration/may-15-retirement — retirement table: `grok-4-0709`, `grok-4-fast-reasoning`, `grok-4-1-fast-reasoning` → `grok-4.3` with `low`; `grok-3` and the non-reasoning slugs → `grok-4.3` with `none`; shutdown 15 May 2026 12:00 PT; "4 reasoning effort levels (none, low, medium, and high)"; note on explicit `medium`/`high`; $1.25/$2.50 per 1M.
- https://docs.x.ai/developers/model-capabilities/text/best-practices — set effort explicitly on every request; "`grok-4.3` defaults to `"low"` and also accepts `"none"`".
- https://docs.x.ai/developers/model-capabilities/text/reasoning — class rules for reasoning models (`reasoning_tokens` billing; `presencePenalty`/`frequencyPenalty`/`stop` → error); enumerates only `grok-4.7`, `grok-4.6` (each `low`/`medium`/`high` default/`xhigh`), `grok-4.5` and `grok-4.20-multi-agent`, **not** grok-4.3; `xhigh` "available on `grok-4.6` and later" — so the class rules, the `xhigh` semantics and the statement "Reasoning cannot be disabled" there do not transfer to grok-4.3.
- https://docs.x.ai/developers/models — alias convention (`<modelname>`, `<modelname>-latest`, `<modelname>-<date>`) and current roster with grok-4.3 (1M) alongside grok-4.7/4.6/4.5 (500k), but without grok-4/grok-4-0709; grok-4.7 recommended for code and chat; cutoff listed only for grok-4.7.
- https://docs.x.ai/developers/models/grok-4.6 — comparison values for the migration direction: 500k context, $2.00/$6.00 per 1M (≥200k: $4.00/$12.00), 150 rps / 50M tpm, regions us-east-1/us-west-2/us-central-1 (no eu-west-1), Batch API "Not supported".
- https://docs.x.ai/developers/models/grok-4.7 — comparison values of the recommended flagship: 500k context, same prices as grok-4.6, efforts `low`–`xhigh` with default `high`, Batch API "Not supported", regions us-east-1/us-west-2/us-central-1.
- https://docs.x.ai/developers/advanced-api-usage/prompt-caching/maximizing-cache-hits — cache-hit routing via `prompt_cache_key` (Responses API) or header `x-grok-conv-id` (Chat Completions).
- https://x.ai/news/grok-4 — Grok 4 announcement: "a 256,000 context window" for the Grok 4 API.
