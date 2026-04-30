# Model Regression Detection System

This project implements a CI/CD-style evaluation pipeline for LLM-powered features. It automatically tests prompt or model changes against a curated golden dataset, detects quality regressions, and generates structured evaluation outputs before degraded behavior reaches users.

---

## Feature Under Test

### Customer Support Email Classifier

**Input:**
- Raw customer email text

**Output (structured JSON):**
- `category`: one of `billing`, `technical`, `account`, `general`
- `summary`: one-sentence summary of the issue (always in English)

---

## Project Goal

Modern teams often ship prompt or model changes without systematic validation. This project introduces:

- Deterministic evaluation of LLM behavior  
- Regression detection across runs  
- Per-case debugging visibility  
- Reproducible evaluation artifacts  
- CI/CD-ready testing workflow  

---

## Phase 1 — Feature Implementation ✅

### Completed

- Modular project structure  
- Versioned prompt configuration (`/prompts`)  
- Strict typing using Pydantic schemas  
- YAML-based prompt loader  
- LLM classifier using Groq API  
- Manual execution script (`run_manual.py`)  

### Key Decisions

- Prompt is versioned → enables reproducibility  
- Output is strict JSON → enables automated evaluation  

### Summary Rules

- One sentence  
- Factual  
- English only  

---

## Phase 2 — Golden Dataset ✅

### Completed

- **58 human-written test cases**  
- Balanced category distribution  
- Extensive real-world edge case coverage:
  - Ambiguous and multi-intent inputs  
  - Short/noisy inputs  
  - Typos and informal language  
  - Sarcasm normalization  
  - Mixed-language inputs  
  - Prompt injection attempts  
  - PII exposure scenarios  
  - Long-context inputs  
  - HTML/system noise  

### Dataset Design

Each case includes:

- Expected category  
- Expected summary  
- Difficulty (`easy`, `medium`, `hard`)  
- Notes explaining intent  

### Summary Constraints

- One sentence  
- Factual and neutral  
- No tone descriptors  
- Consistent phrasing  

This dataset serves as the **source of truth for evaluation**.

---

## Phase 3 — Evaluation Engine ✅

The evaluation system introduces automated testing, multi-metric scoring, and regression detection.

### Evaluation Runner

- Executes all dataset cases against the classifier  
- Collects structured outputs per test case  
- Measures latency per request  
- Handles model failures gracefully (e.g., invalid JSON)  

---

### Metrics

#### Category Accuracy (Primary Metric)
- Exact match against expected label  

#### Summary Quality (LLM-as-Judge)
- Scores summaries from 1–5 based on semantic correctness  
- Uses a secondary LLM with strict evaluation prompts  
- Robust parsing for non-deterministic outputs  

#### Combined Quality Score
- 70% category correctness  
- 30% summary quality  
- Produces a single interpretable score  

---

### Run Storage

- Each evaluation run is saved in `/runs` as JSON  
- Includes:
  - Timestamp  
  - Prompt version  
  - Model  
  - Per-case results  

- Runs are ignored via `.gitignore`  
- Ensures reproducibility without polluting repository history  

---

### Regression Detection

Detects:

- Regressions (pass → fail)  
- Improvements (fail → pass)  

Computes:

- Accuracy delta  
- Overall score delta  

---

### Threshold-Based Status

- `pass` → no significant change  
- `warning` → >3% drop  
- `critical` → >8% drop  

---

### Debugging Visibility

Logs failed cases with:

- Input  
- Expected vs predicted category  
- Expected vs predicted summary  

---

## Phase 4 — Reporting & Alerting ✅

Phase 4 introduces a full reporting and monitoring layer on top of the evaluation engine.

---

### HTML Evaluation Reports

- Automatically generated per run  
- Stored in `/reports`  

Includes:

- Run metadata (timestamp, model, prompt version)  
- Score summary (accuracy, summary score, overall score)  
- Regression summary (deltas, counts)  
- Failed cases table (side-by-side comparison)  
- Regressions and improvements  
- Trend tracking across runs  

---

### Slack Alerts (Webhooks)

- Sends real-time alerts after each evaluation run  

Includes:

- Evaluation status (`pass` / `warning` / `critical`)  
- Accuracy delta  
- Overall score delta  
- Number of regressions  
- Report file reference  

Uses environment variable:

```env
SLACK_WEBHOOK_URL=...

## Example Output

```text
Category accuracy: 81.03%
Average summary score: 3.60/5
Overall quality score: 0.78

Failed cases:
--------------------------------------------------------------------------------
Case ID: case_005
Input: ...
Expected category: account
Predicted category: billing
Expected summary: ...
Predicted summary: ...
```


### Trend Tracking

- Tracks last N runs  
- Computes:
  - Category accuracy  
  - Average summary score  
  - Overall score  
- Enables visibility into performance over time  

---

### Drift Detection

- Computes rolling average (default: last 7 runs)  
- Detects gradual degradation even when individual runs pass  
- Prevents silent quality decline  

---

### Robustness Improvements

- Handles invalid or missing `summary_score` values  
- Ensures backward compatibility with older runs  
- Prevents crashes from evaluator inconsistencies  

---

## Current Status

- Phase 1 — Feature Implementation ✅  
- Phase 2 — Golden Dataset ✅  
- Phase 3 — Evaluation Engine ✅  
- Phase 4 — Reporting & Alerting 🚧  
- Phase 5 — CI/CD Integration 🚧  

---

## Next Steps (Phase 4)

- HTML evaluation reports with diff views  
- Slack alert integration (webhooks)  
- Trend tracking across runs  
- Drift detection (rolling averages)  
