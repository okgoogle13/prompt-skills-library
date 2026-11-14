# Prompt Engineering & Chain-of-Thought Playbook v2 (2026)

## 1. Core Concepts

- Prompt engineering is the practice of crafting instructions and inputs that reliably guide a generative model to produce desired outputs across tasks and models.
- A high-quality prompt explicitly defines objective, context, instructions, constraints, examples, and output format; optional role/persona further steers style and perspective.
- Chain-of-thought (CoT) prompting asks models to show intermediate reasoning steps before a final answer; it is most valuable for multistep logic, math, debugging, and root-cause analysis.
- Prompt quality measures how consistently a prompt produces outputs that meet predefined content, format, and constraint criteria across varied inputs and models.

## 2. Prompt Components Checklist

- Objective: Clear, task-oriented instruction ("Classify", "Summarize", "Generate", "Plan").
- Context: Domain, audience, data source, constraints, and how the output will be used.
- Role / persona: Optional expert identity to anchor tone and decision style.
- Instructions: Ordered steps, focus/ignore rules, safety or grounding instructions.
- Examples (few-shot): 1–3 input/output pairs to demonstrate desired pattern or reasoning style.
- Constraints: Limits on length, style, allowed labels, forbidden behaviors/topics, safety requirements.
- Output format: Target structure (bullets, Markdown sections, table, JSON schema, YAML).
- Techniques: CoT, tree-of-thought, self-consistency, retrieval, or agentic patterns as needed.

## 3. Model-Aware Routing

Use this decision rule before choosing CoT or reasoning settings.

- Reasoning-capable model with native thinking: do not ask for explicit step-by-step output by default; use native reasoning controls (adaptive thinking / effort) and provide goal, constraints, and output contract.
- Non-reasoning or local model: explicit CoT is valuable; ask for ordered reasoning and a clearly separated final answer.
- Need an auditable trail: request a concise, structured reasoning section even on reasoning models, but keep it short and verify against explicit criteria.
- Simple classification, formatting, lookup, or short rewrite: skip CoT; use direct prompting with tight constraints.

## 4. Core Techniques

### 4.1 Standard Techniques

- Zero-shot prompting: Single, clear instruction; useful baseline for simple tasks.
- Few-shot prompting: Add 2–5 examples to teach format and behavior for classification, extraction, or niche reasoning.
- Role prompting: Assign an expert persona for more coherent, domain-aware responses.
- Constraint-based prompting: Specify strict rules on length, style, and allowed outputs to reduce variance.
- Structured output prompting: Require machine-readable outputs such as strictly valid JSON, CSV rows, or Markdown tables.

### 4.2 Reasoning Techniques

- Chain-of-thought (CoT): Instruct the model to "think step by step" or "show reasoning" before the final answer; use mainly on non-reasoning/local models or when an explicit audit trail is required.
- Few-shot CoT: Provide worked examples that explicitly show reasoning steps and final answer separation.
- Self-consistency: Sample multiple CoT paths and aggregate final answers; use only when evaluation shows a measurable benefit.
- Tree-of-thought: Explore multiple solution branches rather than a single linear chain, then prune to the best path; reserve for high-stakes tasks.
- ReAct: Interleave textual reasoning with external actions and feed results back into subsequent steps; define "done" and verification steps.

## 5. Chain-of-Thought Prompt Patterns

### 5.1 General CoT Template (non-reasoning/local models)

```text
You are a [role, e.g. senior engineer / data scientist].

Task:
[Describe the problem requiring reasoning.]

Instructions:
1. Think step by step and write out your reasoning chain.
2. Make assumptions explicit; flag uncertainties.
3. Show intermediate calculations or decision criteria where relevant.
4. After reasoning, provide a concise final answer on a separate line starting with "Final answer:".

Constraints:
- Reasoning must be logically ordered with no skipped steps.
- If data is missing, explain what is needed instead of fabricating.

Output format:
- Section 1: "Reasoning" – detailed chain-of-thought.
- Section 2: "Final answer" – 1–2 sentence summary.
```

### 5.2 CoT for Debugging / Analysis

```text
You are a senior software engineer.

Task:
Identify the root cause of a bug and propose a fix.

Instructions:
1. Trace execution step by step for the provided input.
2. At each step, state variable values and key conditions.
3. Identify the first point where behavior diverges from expected.
4. Explain why this divergence occurs.
5. Propose a minimal, concrete fix (code or config change).

Reasoning:
Think step by step and show your work before giving the final answer.

Output format:
- "Reasoning": numbered steps tracing execution and analysis.
- "Final answer": 1–3 sentences summarizing cause and fix.
```

### 5.3 Reasoning-Model Prompt Template

```text
You are a [role] responsible for [high-level objective].

Goal:
[Clear, outcome-oriented description of what to produce.]

Constraints:
- [Length, style, allowed labels, forbidden behaviors]
- [Safety / grounding instructions]

Output contract:
Return output as:
[Markdown / JSON schema / table / bullets]

Reasoning guidance:
- Do not output a full step-by-step chain unless explicitly requested.
- Use internal reasoning as needed; keep the final answer concise.
- If uncertain, state assumptions and confidence.

Verification:
Before finishing, verify the output against these criteria:
- [Criterion 1]
- [Criterion 2]
If verification fails, revise once and explain the correction.
```

## 6. Verification & Self-Check

- Add a verification instruction such as: "Before you finish, verify your answer against [test criteria]."
- Use this especially for coding, math, and high-stakes analysis.
- Caution: on some newer models, explicit verification instructions can cause over-verification and extra tokens; remove or soften them if that occurs.

## 7. Cost & Latency Budgeting

- CoT, self-consistency, and tree-of-thought increase token usage and latency.
- Enable expensive techniques only when expected accuracy gain meets a threshold (e.g., ≥ +5 points on your eval) and task value justifies the extra cost.
- For latency-sensitive paths, use lower effort or skip CoT entirely.

## 8. Context Engineering

- Define what context is essential vs. summarizable vs. persisted across turns.
- For agentic or long-running workflows, manage context actively: include only what the model needs now; summarize or archive the rest.
- Specify how state should be carried forward.

## 9. Agentic Workflows

- For tool-using or multi-step agent tasks, define "definition of done" and verification steps before declaring completion.
- Use ReAct-style loops where reasoning and actions alternate, with clear stopping conditions.

## 10. Prompt Quality Evaluation

### 10.1 Definition & Metrics

- Prompt quality: How reliably a prompt produces outputs that meet predefined content, format, and constraint criteria.
- Three primary dimensions: accuracy, consistency, instruction-following.

### 10.2 Test Set Design

- Minimum size: ≥ 20 test inputs per prompt.
- Composition: happy-path (~40%), edge cases (~30%), adversarial (~30%).
- For each input, specify pass criteria in advance for content, structure, and constraints.

### 10.3 Scoring Methods

- Binary pass/fail for structured outputs.
- 1–5 rubric for generative tasks.
- LLM-as-judge for free-text evaluation.

### 10.4 Multi-Model Evaluation & Regression

- Evaluate prompts on each model you plan to deploy.
- Record initial pass rate as baseline; treat a drop of more than ~5 percentage points after changes as a regression.

## 11. General Prompt Template (v2)

```text
System / role:
You are a [role] responsible for [high-level objective].

Task:
[Precise description of what to produce.]

Context:
[Background, inputs, constraints, audience, downstream use.]

Instructions:
- [Instruction 1]
- [Instruction 2]
- [Safety / grounding instruction]

Constraints:
- Length: [limit or range]
- Style: [tone / register]
- Allowed outputs: [labels or schema]
- Forbidden: [topics / behaviors]

Model routing:
- model_type: [reasoning | non_reasoning | local]
- reasoning_mode: [adaptive | extended | off]
- effort: [none | low | medium | high | xhigh | max]

Techniques:
- [CoT, few-shot, retrieval, etc.]
- If uncertain, state assumptions and confidence.

Verification:
Before finishing, verify the output against:
- [Criterion 1]
- [Criterion 2]

Output format:
[Bullets, numbered sections, Markdown table, JSON schema, etc.]

Examples (optional):
Input: [...]
Output: [...]
```
