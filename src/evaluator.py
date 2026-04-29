import json
import time
from pathlib import Path

from src.classifier import classify_email
from src.eval_schemas import GoldenCase, CaseEvalResult
from src.prompt_loader import load_prompt_config
from src.eval_schemas import ModelOutput



def load_golden_dataset(path: str) -> list[GoldenCase]:
    data = json.loads(Path(path).read_text())

    if isinstance(data, dict) and "cases" in data:
        data = data["cases"]

    return [GoldenCase(**item) for item in data]


def evaluate_case(case: GoldenCase, prompt_path: str) -> CaseEvalResult:
    start = time.perf_counter()

    prompt_config = load_prompt_config(prompt_path)
    try:
        output = classify_email(case.input, prompt_config)
    except Exception as error:
        output = ModelOutput(
            category="general",
            summary=f"INVALID_MODEL_OUTPUT: {error}",
        )

    latency_ms = (time.perf_counter() - start) * 1000

    return CaseEvalResult(
        case_id=case.id,
        input=case.input,
        expected_category=case.expected_output.category,
        predicted_category=output.category,
        expected_summary=case.expected_output.summary,
        predicted_summary=output.summary,
        category_match=output.category == case.expected_output.category,
        summary_score=None,
        latency_ms=round(latency_ms, 2),
        difficulty=case.difficulty,
        notes=case.notes,
    )