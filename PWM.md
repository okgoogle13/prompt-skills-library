# Project PWM Workflows — prompt-skills-library

Active intelligence, research, and evaluation workflows tailored for `prompt-skills-library`.

> **Context:** This is a curated, evidence-based prompt and skills library.

---

### 1. Fast Intel & Search
* **`quick "<query>"`**
  * **Goal**: Fast factual lookup (definitions, data points, council/local info).
  * **Model**: Sonar 2 (`-m sonar`)
  * **Cost**: 1 Pro search.
* **`ask-pwm "<query>"`**
  * **Goal**: Balanced multi-source search with synthesized web citations.
  * **Cost**: 1 Pro search.
* **`au-market "<item or service>"`**
  * **Goal**: Current Australian retail pricing, vendor terms, and availability.
  * **Cost**: 1 Pro search (`-s web`).

### 2. High-Stakes Councils & Reasoning
* **`jury "<dilemma or trade-offs>"`**
  * **Goal**: 3-provider executive jury (GPT-5.6 Terra, Claude Sonnet 5, Gemini 3.1 Pro) evaluating options and trade-offs.
  * **Cost**: 4 Pro searches.
* **`council "<query>"`**
  * **Goal**: Parallel multi-model consensus audit.
  * **Cost**: 4 Pro searches.
* **`model-think "<prompt>"`**
  * **Goal**: Deep extended reasoning via Claude Sonnet 5 (model only, no search).
  * **Cost**: 1 Pro search (`-m claude_sonnet -t -s none`).

### 3. Deep Research Dossiers (Monthly Pool)
* **`deep-recon "<topic>"`**
  * **Goal**: Comprehensive 360° deep research dossier (saves to `~/Documents/pwm-research/`).
  * **Cost**: 1 Deep Research query (limited monthly pool).
* **`price-baseline "<asset or item>"`**
  * **Goal**: Historical pricing baseline, median spread, and depreciation/growth curve.
  * **Cost**: 1 Deep Research query (limited monthly pool).
