# Product Research Workflow

Canonical, versioned workflow for evidence-based research into a single Australian consumer-product purchase.

## Source of truth

This directory is the canonical source for the portable workflow. Runtime workspaces—Perplexity Projects, Gemini Spark tasks, ChatGPT Projects, and Claude Projects—should use copies or adapters derived from these files.

## Files

- `shopping-core.md`: portable core research policy.
- `stage-prompts.md`: bounded stage-by-stage prompts, including Interview Me.
- `templates/`: blank masters to copy into a purchase folder.
- `adapters/`: runtime-specific instructions.
- `au-product-research/`: packaged Agent Skill adapter.

## Purchase folders

Create one isolated folder per purchase. Never mix candidates, evidence, prices, or conclusions across purchases.

```text
purchases/
  2026-11-robot-vacuum/
    purchase-brief.md
    purchase-record.md
    handover.md
```

## Version

`0.1.0-draft` — pilot version. Promote only after a bounded live pilot demonstrates that the output contract and evidence policy work reliably.
