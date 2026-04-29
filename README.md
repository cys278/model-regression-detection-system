# Model Regression Detection System

This project implements a CI/CD-style evaluation pipeline for LLM-powered features. It automatically tests prompt or model changes against a curated golden dataset, detects quality regressions, and generates reports before degraded outputs reach users.

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

Modern teams ship prompt and model changes without rigorous testing. This project introduces:

- Repeatable evaluation of LLM outputs
- Regression detection across prompt/model changes
- Structured reporting for decision-making
- CI/CD integration for automated quality checks

---

## Phase 1 — Feature Implementation ✅

Completed:
- Project structure and modular design
- Versioned prompt configuration (`/prompts`)
- Typed schemas using Pydantic
- YAML-based prompt loader
- LLM-powered classifier (Groq API)
- Manual execution script for testing

The classifier successfully returns structured JSON outputs for real-world email inputs.

---

## Phase 2 — Golden Dataset ✅

Completed:
- Curated **58 human-written test cases**
- Balanced coverage across all categories
- Inclusion of real-world edge cases:
  - Ambiguous and multi-intent inputs
  - Short and noisy inputs
  - Typographical errors
  - Sarcasm and tone normalization
  - Mixed-language inputs
  - Prompt injection attempts
  - PII exposure scenarios
  - Long-context inputs
  - HTML/system artifact inputs
- Difficulty labeling (`easy`, `medium`, `hard`) for evaluation slicing
- Consistent, evaluation-friendly summaries:
  - English-only output
  - No tone descriptors
  - Standardized phrasing

This dataset serves as a **golden benchmark** for regression detection.

---

## Next — Phase 3: Evaluation Engine 🚧

Planned:
- Automated test runner for dataset execution
- Multi-dimensional scoring:
  - Category accuracy
  - Summary quality (LLM-as-judge)
  - Latency
  - Token usage
- Output comparison against baseline runs
- Regression and improvement detection
- Structured evaluation reports
