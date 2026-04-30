import json
import os
import re

from groq import Groq


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text: str) -> dict | None:
    """
    Attempts to extract JSON from model output.
    Handles messy responses like:
    - "Here is the score: {\"score\": 5}"
    - "Score: 4"
    """
    # First try clean JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting JSON object from text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            return None

    return None


def judge_summary(expected_summary: str, predicted_summary: str) -> int:
    prompt = f"""
You are a strict evaluator of customer support summaries.

Expected summary:
{expected_summary}

Predicted summary:
{predicted_summary}

Evaluate how close the predicted summary is to the expected summary.

Rules:
- The meaning MUST match the expected summary
- Missing key information → lower score
- Extra unrelated or incorrect information → lower score
- If the predicted summary is incorrect, misleading, or unsafe → score = 1
- If the predicted summary ignores the expected meaning → score = 1

Scoring:
5 = same meaning, complete and accurate
4 = mostly correct, minor wording difference
3 = partially correct but missing important detail
2 = mostly incorrect
1 = incorrect, misleading, or unsafe

Return ONLY valid JSON:
{{"score": 5}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict evaluation judge. Only return JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    raw_output = response.choices[0].message.content.strip()

    parsed = extract_json(raw_output)

    if not parsed or "score" not in parsed:
        return 1  # fallback

    try:
        score = int(parsed["score"])
    except Exception:
        return 1

    return max(1, min(score, 5))