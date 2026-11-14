---
model: gpt-4.1
vendor: OpenAI
family: GPT
aliases: [gpt4.1, gpt-4-1, gpt41, gpt-4.1-2025-04-14]
last_verified: 2026-06-13
status: legacy
---

# GPT-4.1

## Reasoning / Thinking
- **Type: none.** GPT-4.1 is NOT a reasoning model — OpenAI explicitly calls it the "smartest non-reasoning model" and, on the model page, recommends starting with GPT-5 for complex tasks ("we recommend starting with GPT-5 for complex tasks"). There is no internal thinking/scratchpad step before the answer.
- Step-by-step reasoning must therefore be **explicitly triggered in the prompt** ("induced chain-of-thought"). This raises output quality but costs extra tokens and latency.
- Concrete prompts from the OpenAI prompting guide:
  - Generic starter: "First, think carefully step by step about what documents are needed to answer the query."
  - Optional planning reminder for agentic flows: "You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls."
- Recommended approach: derive the reasoning strategy iteratively from observed failures and hard-code it in the prompt ("audit failures and codify effective reasoning strategies"). Typical failure sources that explicit reasoning mitigates: misreading user intent, incomplete context gathering, faulty step-by-step derivation.

## Prompting Style
- **Very prescriptive / literal.** GPT-4.1 "is trained to follow instructions more closely and more literally than its predecessors". Consequences:
  - Implicit rule inference is reduced — everything must be **explicitly** specified; the model "reads between the lines" less than GPT-4o did.
  - If behaviour deviates, a single, clear corrective sentence is almost always enough: "a single sentence firmly and unequivocally clarifying your desired behavior is almost always sufficient".
  - Overridden absolute instructions can backfire: if you say e.g. "always call a tool", the model may invent (hallucinate) tool calls when information is missing. Fix: add an escalation clause, e.g. "If you don't have enough information, ask the user for what you need."
- **System message fidelity:** In agentic settings the model sticks closely to both user and system prompts. With contradictory instructions it tends to follow the ones **closer to the end** of the prompt.
- **Agentic prompting:** OpenAI recommends three fixed reminders in the agent system prompt; they reportedly increased its internal SWE-bench Verified score by ~20%:
  - *Persistence:* "You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user."
  - *Tool-calling:* "If you are not sure about file content or codebase structure pertaining to the user's request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer."
  - *Planning (optional):* "You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls."
- **Pass tools via the `tools` API field**, not as text descriptions injected into the prompt ("exclusively use the tools field"): this keeps the model in-distribution and gave +2% on SWE-bench Verified internally. Use clear names and detailed descriptions for tools and parameters.
- **Long contexts:** effectively usable up to ~1M tokens. For long contexts, place instructions **at both the beginning AND the end** ("at both the beginning and end of the provided context") — this beats placing them once. Performance drops as retrieval complexity rises or with graph-search-style reasoning across many scattered facts.

## Strengths & Weaknesses (prompt-relevant)
- **Strengths:**
  - Very strong, precise instruction following — outputs can be steered tightly.
  - Coding/agentic: clearly better than GPT-4o (per OpenAI +21.4% on SWE-bench Verified vs. GPT-4o (unverified)); reliable adherence to diff formats, fewer superfluous edits, consistent tool use.
  - Very large context window (1,047,576 tokens) with good comprehension of long documents.
- **Weaknesses (prompt-relevant):**
  - Literalness is double-edged: under-specified or contradictory prompts lead to unwanted behaviour faster than with more "interpretive" predecessors.
  - Hallucinated tool calls when absolute instructions have no escalation path.
  - Repeated example phrases get copied verbatim → can become repetitive; fix: "instruct model to vary phrases as necessary".
  - Tendency toward verbose explanatory prose / excessive formatting unless explicitly kept terse.
  - No built-in reasoning → complex multi-step logic must be forced through the prompt.

## Output & Format Conventions
- Context window 1,047,576 tokens, **max. output 32,768 tokens**; knowledge cutoff 1 Jun 2024 (model page).
- **Delimiters / structuring** (recommended order to try):
  - **Markdown** (starting point): section titles, code in backticks.
  - **XML**: works very well, allows precise wrapping/nesting of content.
  - **JSON**: verbose and performed poorly in long-context tests → avoid for large document collections.
  - For document collections, **XML** and the format `ID|TITLE|CONTENT` beat JSON.
- **Recommended prompt structure** (add/remove sections as needed): Role and Objective → Instructions (with subcategories) → Reasoning Steps → Output Format → Examples → Context → closing "think step by step" instruction.
- **Diff formats (coding):** the **V4A format** is recommended — context-based identification **without line numbers**, with clear before/after delimiters. Also good: **SEARCH/REPLACE** and pseudo-XML — both without line numbers and with a clear old/new boundary.

## Migration Notes
- **No `successor`**: OpenAI documents no direct successor for gpt-4.1 — the deprecations page lists only `gpt-4.1-nano` (→ `gpt-5.6-luna`), not gpt-4.1 itself; the model page merely points to GPT-5 for complex tasks (which is itself deprecated).
- **When migrating AWAY from GPT-4.1:**
  - To a **reasoning model** (e.g. the GPT-5 series): manually injected "think step by step" instructions and explicit planning reminders can be dropped or reduced, since reasoning happens internally; instead, control reasoning effort/parameters if needed (model-dependent).
  - Prompts heavily tuned to GPT-4.1's literal reading (very narrow absolute instructions) should be re-evaluated on the target model — other models interpret more freely.
- **When migrating TO GPT-4.1:**
  - Prompts optimised for older models (e.g. GPT-4o) may need adjustment, since GPT-4.1 follows more literally: "prompts optimized for prior models may require migration."
  - Make implicit assumptions explicit; sharpen vague behaviour with one clear corrective sentence.
  - Move tool descriptions from prompt text into the `tools` API field.
  - For long contexts, duplicate instructions at the start AND the end.
  - As no reasoning is built in: add explicit step-by-step/planning instructions where a reasoning model previously handled the logic itself.
- **General:** OpenAI stresses "AI engineering is inherently an empirical discipline" — build informative evals and iterate on every migration; test parallel tool calls and disable them if they cause problems.

## Sources
- https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide — official GPT-4.1 Prompting Guide (OpenAI Cookbook): literal instruction following, three agentic reminders (Persistence/Tool-calling/Planning), `tools` field instead of prompt injection, long-context placement at start/end, induced chain-of-thought, recommended prompt structure, delimiters (Markdown/XML/JSON), diff formats (V4A/SEARCH-REPLACE/pseudo-XML), failure modes & fixes.
- https://developers.openai.com/api/docs/models/gpt-4.1 — official model spec: context window 1,047,576 tokens, max. output 32,768 tokens, knowledge cutoff 1 Jun 2024, classification as "smartest non-reasoning model", snapshot gpt-4.1-2025-04-14, "we recommend starting with GPT-5 for complex tasks", no deprecation notice.
- https://openai.com/index/gpt-4-1/ — official announcement "Introducing GPT-4.1 in the API": model family, coding/instruction-following/long-context strengths, +21.4% on SWE-bench Verified vs. GPT-4o. (Direct fetch HTTP 403; content verified via OpenAI search snippets.)
- https://developers.openai.com/api/docs/deprecations — no entry for gpt-4.1 / gpt-4.1-2025-04-14 (only gpt-4.1-nano → gpt-5.6-luna, shutdown 23 Oct 2026); gpt-5-2025-08-07 shutdown 11 Dec 2026
