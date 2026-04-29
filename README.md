
# Model Regression Detection System

This project is a CI/CD-style evaluation pipeline for LLM-powered features. It tests prompt and model changes against a golden dataset, detects quality regressions, and prepares reports before bad outputs reach users.

## Current Feature Under Test

The first LLM feature is a customer support email classifier.

Input:
- Customer email text

Output:
- Category: billing, technical, account, or general
- One-sentence summary

## Phase 1 Status

Completed:
- Project structure
- Versioned prompt file
- Typed input/output schemas
- Prompt YAML loader
- LLM classifier function
- Manual run script

Next:
- Build the golden dataset for evaluation
