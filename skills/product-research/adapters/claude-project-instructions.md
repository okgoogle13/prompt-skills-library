---
workflow: au-product-research
version: 0.1.0-draft
updated: 2026-11-23
source: prompt-skills-library
runtime: claude-project
---

# Claude Project Product Research Adapter

## When to use

Use in a Claude Project (claude.ai) dedicated to one Australian consumer-product purchase. This file covers runtime setup only. The research method, evidence policy, stages, and output contract stay in `shopping-core.md`, `stage-prompts.md`, and `templates/`.

## Required files

**Project knowledge (persistent, shared by every chat in the Project):**

- `shopping-core.md`
- `stage-prompts.md`
- `templates/purchase-brief-template.md`
- `templates/purchase-record-template.md`
- `templates/handover-template.md`
- Optional: `au-product-research/references/evidence-policy.md`, which `shopping-core.md` names as its expanded screening procedure.
- After Stage 0: the completed `purchase-brief.md`. After each research stage: your current `purchase-record.md` and `handover.md`. Replace the old copy each time; do not keep two versions.

**Project instructions (pasted text):** the full text of `shopping-core.md`, followed by this scope line:

```text
This Project is for ONE purchase only: Purchase ID [e.g. 2026-11-robot-vacuum]. Work only on this purchase. If I ask about another product, ask whether to start a separate Project. Follow stage-prompts.md and the templates in Project knowledge. If this scope line conflicts with shopping-core.md, stage-prompts.md, or the templates, the canonical file controls.
```

**Attached to an individual chat:** the record rows each stage needs (see Stage invocation). Attach or paste them even when the full record is in Project knowledge.

**Packaged skill:** none. Using `au-product-research/` as a Claude Skill inside a Project is `Unverified`; this adapter does not depend on it.

## Setup

1. Open Projects in the left sidebar and select "+ New Project".
2. Name it with the Purchase ID, for example `2026-11-robot-vacuum`. Claude cannot see the Project name or description, so the Purchase ID must also appear in the pasted instructions and the brief.
3. Select "Set project instructions", paste the text from Required files, and save.
4. Upload the Project knowledge files with the "+" on the Project page.
5. On the Project page, under Memory, turn off "Use account memory" so memory from chats outside this Project is not drawn in.
6. Check that web search can be switched on from the "+" menu in a chat. In the new Claude experience there is no toggle and Claude decides when to search; use the prompt wording under Stage invocation instead. On Team and Enterprise plans an Owner or Primary Owner must first enable it in Organization settings > Capabilities.
7. Keep one Project per purchase. Never add candidates, evidence, prices, or conclusions from another purchase. Free accounts are limited to five Projects; plan purchases accordingly.

If Project instructions are not available on your plan (`Unverified`), attach `shopping-core.md` to the first message of every chat instead.

## Interview Me

Start a new chat in the Project with web search off. In one message, type a trigger phrase ("interview me", "start a new purchase", or "create the purchase brief") followed by the Stage 0 block from `stage-prompts.md`.

Claude must:

- Ask only for missing required fields.
- Ask in groups of 3–5 related questions.
- Offer defaults only when clearly labelled as assumptions.
- Not name, recommend, compare, or price any product, brand, or retailer during intake.
- Confirm the Purchase ID and delivery postcode.
- Output the completed brief as one Markdown code block using `purchase-brief-template.md`.
- Ask whether to proceed to Stage 1 or revise the brief.

Save the brief as `purchase-brief.md` in your purchase folder and upload it to Project knowledge before Stage 1.

## Stage invocation

For every stage, paste the matching prompt block from `stage-prompts.md` unchanged. Run adjacent stages in one chat only if it stays clean; otherwise start a new chat in the same Project.

### Stage 0 — Interview Me

- **Prompt:** a trigger phrase, then the Stage 0 block.
- **Load:** `shopping-core.md` and `purchase-brief-template.md` (Project knowledge).
- **Expected output:** the filled purchase brief in one Markdown code block, then the Stage 1 or edit question.
- **Tools:** web search off. Not needed, and product naming is out of scope. Where there is no toggle, add "Do not use web search" to the prompt.

### Stage 1 — Criteria framing and Australian risk check

- **Prompt:** the Stage 1 block.
- **Load:** `shopping-core.md` and the completed `purchase-brief.md`.
- **Expected output:** an updated brief and a short list of open questions. No products or brands.
- **Tools:** web search off.

### Stage 2–3 — Bounded candidate and evidence pilot

- **Prompt:** the Stage 2–3 block.
- **Load:** `shopping-core.md`, the completed `purchase-brief.md`, and `purchase-record-template.md`.
- **Expected output:** Source Screening Register, Evidence Log, Conflicts, Unknowns & Supersession Log, and a Handover Snapshot of at most 150 words.
- **Tools:** turn web search on from the "+" menu. Add "Search the web" to the prompt if Claude answers without searching. Paste specific review URLs when you want Claude to read a full page (URL fetch works only while web search is on). Do not use Research mode (`Unverified` in this adapter): the stage limits of 4 sources and 6 Evidence Log rows apply regardless of tool. Claude's built-in citations do not replace the direct URL and date required per claim.
- **After:** copy the tables into `purchase-record.md` and the snapshot into `handover.md`, then replace both in Project knowledge.

### Stage 4 — Offer and purchase-risk check

- **Prompt:** the Stage 4 block.
- **Load:** `shopping-core.md`, the current shortlist, and the relevant `purchase-record.md` rows. Attach or paste the Source Screening, Evidence, and Conflict rows for the shortlisted models in the chat.
- **Expected output:** Seller Offers rows per `purchase-record-template.md`, with the Australian risk flags from the Stage 4 block.
- **Tools:** web search on. Paste retailer product URLs for exact AU SKUs. Web search may infer location from your IP address, so results can be wrong if you use a VPN or are overseas. Re-verify live prices yourself on the intended purchase day.
- **After:** add the offers to `purchase-record.md` and replace it in Project knowledge.

### Stage 5 — Decision record

- **Prompt:** the Stage 5 block.
- **Load:** `shopping-core.md`, the completed `purchase-record.md`, and the relevant evidence, offer, and conflict rows attached or pasted in the chat. Do not rely on `handover.md` alone.
- **Expected output:** the Decision Record and Pre-checkout human check from `purchase-record-template.md`.
- **Tools:** web search off, except to re-check a specific live offer URL. Do not present a second Claude chat or another model's review as independent verification.

## Platform limitations

Checked against Anthropic help-centre articles on 2026-11-23. Labels: **Verified** means stated in an official article; `Unverified` means not confirmed there.

- **Projects:** Verified. Available to all users, including Free (maximum five Projects). Chats in a Project share Project knowledge, but context is not shared across chats unless it is added to Project knowledge.
- **Project instructions:** Verified that Claude uses them for all chats within the Project. Plan restriction: `Unverified`.
- **Project knowledge size:** On paid plans, Claude switches to retrieval (RAG) as knowledge nears the context limit (Verified). In that mode not every row may be read in full, so attach the rows a stage needs. Exact file size and count limits: `Unverified`.
- **New version of Projects (beta):** Verified that a beta is rolling out, starting with Claude Code, and that chat will follow. How it will change chats, memory, or knowledge in this workflow: `Unverified`.
- **Web search:** Verified. Turned on per chat from the "+" menu. Team and Enterprise need an Owner to enable it. Responses include citations. Pasted URLs can be fetched while it is on. Including "Search the web" in a prompt makes Claude search; you can also tell it not to. The new Claude experience has no toggle. Availability "may vary based on connectivity" and some links may not work. Plan availability: `Unverified`.
- **Research mode (deep research):** `Unverified`.
- **Skills:** Verified that Skills exist on all plans and require code execution to be enabled. Skills inside Projects: `Unverified`.
- **Code execution and file creation:** exists as a setting (Verified); not used by this workflow. **Browser automation:** `Unverified`. Do not assume Claude can run files or browse retailer checkouts.
- **Updating Project files:** `Unverified` that Claude can edit Project knowledge files. Assume you must replace them yourself.
- **Australia:** Verified as a supported location for Claude. Australia-specific feature or plan restrictions: `Unverified`.

Sources: [How can I create and manage projects?](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects), [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects), [Use Claude's chat search and memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context), [Use incognito chats](https://support.claude.com/en/articles/12260368-use-incognito-chats), [Enable and use web search](https://support.claude.com/en/articles/10684626-enable-and-use-web-search), [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Where can I access Claude?](https://support.claude.com/en/articles/8461763-where-can-i-access-claude).

## Context and memory

Claude's controls reduce cross-purchase influence. They do not guarantee isolation.

- **One Project per purchase.** Put the policy in Project instructions and files, not in account-level personal preferences.
- **Account memory:** by default, Project chats use memory from your non-Project chats (Verified). Turn off "Use account memory" on the Project page. Project chats do not use other Projects' memory (Verified).
- **Per-chat memory:** to stop a chat using or adding memory, turn off "Memory" in the "+" menu before the first message (Verified). Incognito chats are not available inside Projects (Verified).
- **Past-chat search:** on paid plans, search from a Project chat is limited to that Project's chats (Verified). Do not ask Claude to search for another purchase.
- **Fresh chat:** start one when switching tools, returning after a break, or noticing clutter, drift, or anchoring on an early candidate. Switching purchases means switching Projects.
- **Returning after a break or tool switch:** start a new chat in the Project. Confirm Project knowledge holds your latest `purchase-brief.md`, `purchase-record.md`, and `handover.md`. Paste the Handover Snapshot for orientation, then attach the record rows named under "Exact Next Action & Records to Load". If you worked in another tool, upload its updated record first.
- Keep your purchase folder outside Claude as the master copy. Project knowledge is a working copy.

## Verification

Before treating any claim as decided:

- Open 2–3 cited URLs directly.
- Check the exact model and Australian SKU match.
- Check the publication or check date.
- Check acquisition, sponsorship, affiliate disclosure, and methodology.
- Fill in `Claim Support`, `Exact-Model Match`, `Source Eligibility`, `Human Check Date`, and `Limitations` in the Evidence Log. Leave `Human Check Date` as `Unchecked` until you have opened the primary source.
- Treat self-critique, a second Claude chat, or another model as an error-finding aid, not independent verification.

## Conflict rule

> If this adapter conflicts with `shopping-core.md`, `stage-prompts.md`, or a template in `templates/`, the canonical file controls.
