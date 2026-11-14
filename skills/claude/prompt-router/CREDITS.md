# Credits and provenance

`prompt-router` is a local, unpublished skill. Its own text is original or paraphrased; no
source file is copied into this folder. Sources were reviewed on 2026-11-10.

## Used in place (read at run time, not copied)

| Source | What is used | Licence |
|---|---|---|
| `~/.claude/skills/migrate-prompt/` — local copy of prompt-brain 0.8.0 by Tarek Steiß (`tarekst/prompt-brain`, manifest-stated) | Model registry and alias policy (`SKILL.md` BEGIN/END block), `model-guides/*.md` (authoritative for this skill), migration Steps 3–5, Guide-Stand and legacy-successor footer rules | MIT |

The router never reads, copies or falls back to the plugin cache
(`~/.claude/plugins/cache/tarek-plugins/prompt-brain/`). The local guides are the only guide
source; a missing guide stops the run.

MIT notice for prompt-brain (also covers the paraphrased weakness categories in
`references/patterns.md` §2.3, derived from its `optimize-prompt`):

```
MIT License

Copyright (c) 2026 Tarek Steiß

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Ideas paraphrased into `references/patterns.md`

Downloaded to `~/Downloads/ai-plugin-library/01_triage/`. Repository URLs are as stated in each
manifest and were not verified against the live repositories.

| Plugin | Author / repo (manifest) | Licence | Ideas taken (paraphrased) | Excluded |
|---|---|---|---|---|
| Prompt Fixer 1.3.0 | Shakeel Mohun, `chatquill/prompt-fixer` | MIT | Five-part check; runnable, self-terminating Done-when; never invent identifiers; risky-operation guard; secret stripping; split independent tasks; standing rules belong in persistent instructions | Salesforce templates, writing mode, `Run with:` model table, release workflow |
| Prompt Optimizer 1.1.0 | bitcompool, `bitcompool/prompt-optimizer-claude-plugin` | Apache-2.0 | Size change to the gap; material-improvement check; draft is untrusted; no invented user facts; functional block labels | Promotional note with tracking link; product Q&A; no-questions rule (narrowed to non-clarify routes) |
| Prompt Enhancer 1.0.5 | bitcompool, `bitcompool/prompt-enhancer-claude-plugin` | Apache-2.0 | Coding-task brief (§9 of its rules) | Promotional note with UTM tracking link; near-duplicate of Optimizer |
| Prompt Tightener 1.0.0 | Stefan Petrovici, `petrovicistefan/claude-code-plugins` | MIT | Review checklist (repetition, filler, emphasis, negatives, format, examples, structure); variables/tags must survive; Claude-only XML and caching advice (gated to Claude targets) | `prompt_check.py` (runs system `python3`; not portable to non-script hosts). Reviewed in full: reads files only, no network |
| Prompt Coach 1.2.0 | Sathiya, `msathiyakeerthi/claude-code-prompt-coach` | MIT | "Do X, because Y"; `[ASSUMPTION: …]` marker | Subagent that writes `.claude/coach/` files; learning notes |

Apache-2.0 sources contributed ideas only, reworded; no text was copied, so no NOTICE file is
carried. If text is ever copied verbatim, add the Apache-2.0 licence and a change statement.

## Maintenance

- Guides perish: each carries `last_verified`; the migrate footer warns past 180 days.
- Refreshing guides is a separate, user-approved change to `migrate-prompt/`; this skill
  changes nothing there.
