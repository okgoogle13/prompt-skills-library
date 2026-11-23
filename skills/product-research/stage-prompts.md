---
workflow: au-product-research
version: 0.1.0-draft
updated: 2026-11-23
source: prompt-skills-library
---

# Sequenced & Iterative Shopping Prompts

Fresh chats at every stage are optional, not mandatory. Run adjacent stages in one chat if it remains clean and focused. Start a fresh chat when switching purchases, changing tools, returning after a break, or noticing clutter, drift, or early-candidate anchoring.

## Stage 0 — Interview Me

**Trigger phrases:** “interview me”, “start a new purchase”, or “create the purchase brief”.

**Attach:** `shopping-core.md` and the blank `purchase-brief-template.md`.

```text
Run Stage 0 (Interview Me) for ONE new purchase only.

Follow every rule in shopping-core.md.

1. Ask only for missing required fields.
2. Ask in groups of 3–5 related questions.
3. Offer sensible defaults where appropriate, but label them as assumptions.
4. Do not name, recommend, compare, or price any product, brand, or retailer during intake.
5. Confirm the Purchase ID and delivery postcode.
6. When complete, output the filled purchase brief as one Markdown code block using the attached template.
7. Ask: “Shall I proceed to Stage 1, or do you want to edit the brief first?”
```

## Stage 1 — Criteria framing and Australian risk check

**Attach:** `shopping-core.md` and the completed `purchase-brief.md`.

```text
Run Stage 1 (Criteria Framing) for ONLY the purchase in the attached brief.
Follow every rule in shopping-core.md.

Do NOT name, recommend, compare, or price any specific products or brands.

Tasks:
1. Audit the brief for missing physical, compatibility, Australian electrical/RCM, spare-parts, or budget constraints.
2. Flag conflicts, ambiguities, and unsupported assumptions.
3. Propose a concise set of testable must-haves and deal-breakers.
4. Identify the evidence types and preferred sources needed in later stages.
5. Output an updated brief and a short list of open questions.
```

## Stage 2–3 — Bounded candidate and evidence pilot

**Attach:** `shopping-core.md`, completed `purchase-brief.md`, and blank `purchase-record-template.md`.

```text
Run a small, bounded Stage 2–3 pilot for ONLY the single purchase in the attached brief.
Follow every rule in shopping-core.md.

Scope limits:
1. Identify at most 2–3 exact models, including Australian regional SKU variants where applicable, that appear to meet all hard must-haves and avoid all hard deal-breakers.
2. Screen at most 4 web sources in total, beginning with preferred sources where relevant.
3. Extract at most 6 deciding rows into the Evidence Log.
4. Keep measured results, qualitative observations, advertised specifications, owner feedback, and analyst judgement strictly separate.
5. Do not collect live seller offers, rank candidates, recommend a winner, or invent composite scores.

Output only:
1. Source Screening Register
2. Evidence Log
3. Conflicts, Unknowns & Supersession Log
4. Handover Snapshot, maximum 150 words

Stop once the scope limits are reached.
```

## Stage 4 — Offer and purchase-risk check

**Attach:** `shopping-core.md`, current shortlist, and the relevant `purchase-record.md` rows.

```text
Run Stage 4 for ONLY the shortlisted exact models and Australian SKUs.

For each candidate, find and record current Australian retailer offers.

Requirements:
1. Record item price including GST, delivery and unavoidable fees, landed total, stock status, seller type, warranty and returns, and check date.
2. Flag parallel-import, marketplace-seller, voltage/plug, RCM, authorised-retailer, and local-support risks.
3. Re-verify live prices on the intended purchase day.
4. Do not declare a winner until the relevant screening, evidence, offer, and conflict records have been loaded.
```

## Stage 5 — Decision record

**Attach:** `shopping-core.md`, completed `purchase-record.md`, and the relevant evidence, offer, and conflict rows.

```text
Prepare the Stage 5 decision record for ONLY this purchase.

Requirements:
1. Identify the chosen exact model and Australian SKU.
2. Identify the chosen retailer and live check date.
3. State the verified AUD landed total.
4. Cite the deciding evidence and trade-offs using Source IDs.
5. State accepted unknowns and limitations.
6. Complete the pre-checkout human-verification checklist.
7. Do not present a second-model review or self-critique as independent verification.
```
