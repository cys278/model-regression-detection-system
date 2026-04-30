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

Completed:
- Modular project structure
- Versioned prompt configuration (`/prompts`)
- Strict typing using Pydantic schemas
- YAML-based prompt loader
- LLM classifier using Groq API
- Manual execution script (`run_manual.py`)

Key decisions:
- Prompt is versioned → enables reproducibility
- Output is strict JSON → enables automated evaluation
- Summary rules enforced:
  - one sentence
  - factual
  - English only

---

## Phase 2 — Golden Dataset ✅

Completed:
- **58 human-written test cases**
- Balanced category distribution
- Extensive real-world edge case coverage:
  - ambiguous and multi-intent inputs
  - short/noisy inputs
  - typos and informal language
  - sarcasm normalization
  - mixed-language inputs
  - prompt injection attempts
  - PII exposure scenarios
  - long-context inputs
  - HTML/system noise

Dataset design:
- Each case includes:
  - expected category
  - expected summary
  - difficulty (`easy`, `medium`, `hard`)
  - notes explaining intent

Summary constraints:
- one sentence
- factual and neutral
- no tone descriptors
- consistent phrasing

This dataset serves as the **source of truth for evaluation**.

---

## Phase 3 — Evaluation Engine ✅

The evaluation system introduces automated testing, scoring, and regression detection.

### Evaluation Runner

- Executes all dataset cases against the classifier
- Collects structured outputs per test case
- Measures latency per request
- Handles model failures gracefully (e.g., invalid JSON)

### Metrics

Currently implemented:
- **Category Accuracy (primary metric)**
  - Exact match against expected label

Planned (next iteration):
- Summary quality scoring (LLM-as-judge)
- Token usage tracking

### Run Storage

- Each evaluation run is saved as a versioned JSON artifact:
  - stored in `/runs`
  - includes metadata:
    - timestamp
    - prompt version
    - model
    - per-case results

- Runs are **not committed to Git** (ignored via `.gitignore`)
- Ensures reproducibility without polluting repository history

### Regression Detection

Each run is compared against the previous run:

- Detects:
  - regressions (pass → fail)
  - improvements (fail → pass)

- Computes:
  - accuracy delta

### Threshold-Based Status

- `pass` → no significant change
- `warning` → >3% accuracy drop
- `critical` → >8% accuracy drop

### Debugging Visibility

- Prints all failed cases with:
  - input text
  - expected vs predicted category
  - expected vs predicted summary

This enables fast diagnosis of:
- prompt weaknesses
- model inconsistencies
- dataset edge cases

---

## Example Output

```text
Category accuracy: 81.03%

Failed cases:
--------------------------------------------------------------------------------
Case ID: case_005
Input: ...
Expected category: account
Predicted category: billing
Expected summary: ...
Predicted summary: ...
```

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
