<task>
Create a runtime adapter for Claude Projects for the Australian product-research workflow, as exactly one new file:

skills/product-research/adapters/claude-project-instructions.md

Follow skills/product-research/adapters/adapter-spec.md exactly. Keep working until the file is written and checked, then stop at the approval step below.
</task>

<read_first>
Read these files in full, in this order, before drafting:

1. skills/product-research/README.md
2. skills/product-research/shopping-core.md
3. skills/product-research/stage-prompts.md
4. skills/product-research/templates/purchase-brief-template.md
5. skills/product-research/templates/purchase-record-template.md
6. skills/product-research/templates/handover-template.md
7. skills/product-research/adapters/adapter-spec.md
</read_first>

<research>
Use only official Anthropic documentation (support.claude.com, docs.claude.com, claude.com). Look up only what the adapter needs:
- Creating and using a Claude Project; Project instructions; uploading project files.
- Starting and continuing chats in a Project.
- Project memory, account memory, and context-isolation controls.
- Web search availability and limitations.
- Claude Skills, only if relevant to Project-based use.
- Australian availability, plan, or feature limitations.

Mark any claim you cannot verify from official documentation as "Unverified". If the documentation is unreachable, mark every platform claim "Unverified". Do not assume Deep Research, code execution, browser automation, or Skills are available; mark each "Unverified" unless documented. Do not speculate about plan limits, feature availability, or memory behaviour.
</research>

<required_sections>
Use these sections, in this order:

1. # Claude Project Product Research Adapter
2. ## When to use
3. ## Required files
4. ## Setup
5. ## Interview Me
6. ## Stage invocation
7. ## Platform limitations
8. ## Context and memory
9. ## Verification
10. ## Conflict rule
</required_sections>

<content_requirements>
The adapter must explain:
- How to create one Claude Project for one purchase, and how to name it (for example "2026-11-robot-vacuum").
- Which files to upload to Project knowledge/files, and what to paste into Project custom instructions.
- How to start with "interview me", "start a new purchase", or "create the purchase brief".
- Stage invocation. For each stage, state the user prompt, the files or record sections to attach or load, the expected output sections, and any tool to use or avoid (including how to use web search for evidence gathering). Use these stage names exactly:
  1. Stage 0 — Interview Me
  2. Stage 1 — Criteria framing and Australian risk check
  3. Stage 2–3 — Bounded candidate and evidence pilot
  4. Stage 4 — Offer and purchase-risk check
  5. Stage 5 — Decision record
- How to preserve one-purchase isolation, and how to return to a purchase after a break or tool switch.
- Verification: the user must open primary sources before treating a claim as decided, and fill in Claim Support, Exact-Model Match, Source Eligibility, Human Check Date, and Limitations.

Include this exact conflict rule in the Conflict rule section:

> If this adapter conflicts with shopping-core.md, stage-prompts.md, or a template in templates/, the canonical file controls.
</content_requirements>

<boundaries>
Do not modify shopping-core.md, stage-prompts.md, any file in skills/product-research/templates/, the evidence policy, evidence categories, source-eligibility rules, citation requirements, workflow stages, or output contract.

Do not add scoring systems, composite rankings, product recommendations, new workflow stages, new evidence rules, new product categories, or cross-purchase context. Do not claim Claude Projects provide perfect context isolation.

Do not create any other file, modify any existing file, create a Claude Skill package, or commit or push.
</boundaries>

<finish>
Check the file with a command (for example grep of the "## " headings) to confirm all ten sections appear in order and the conflict rule is verbatim. Then report:
1. The full file contents.
2. Every assumption you made.
3. Every item marked "Unverified".
4. A concise commit message.

Wait for my approval before committing.
</finish>
