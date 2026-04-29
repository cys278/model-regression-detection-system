from datetime import datetime
from uuid import uuid4

from src.evaluator import load_golden_dataset, evaluate_case
from src.eval_schemas import EvalRun
from src.eval_storage import save_eval_run, load_latest_run
from src.eval_compare import compare_runs


DATASET_PATH = "data/golden_dataset_v1.json"
PROMPT_PATH = "prompts/classifier_v1.yaml"
PROMPT_VERSION = "classifier_v1"
MODEL_NAME = "groq"


def run_evaluation() -> None:
    previous_run = load_latest_run()

    cases = load_golden_dataset(DATASET_PATH)

    results = []

    for case in cases:
        print(f"Evaluating {case.id}...")
        result = evaluate_case(case, PROMPT_PATH)
        results.append(result)

    total_cases = len(results)
    correct_cases = sum(1 for result in results if result.category_match)
    category_accuracy = correct_cases / total_cases

    current_run = EvalRun(
        run_id=f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}",
        timestamp=datetime.now(),
        prompt_version=PROMPT_VERSION,
        model=MODEL_NAME,
        total_cases=total_cases,
        category_accuracy=round(category_accuracy, 4),
        results=results,
    )

    saved_path = save_eval_run(current_run)

    print("\nEvaluation complete.")
    print(f"Saved run: {saved_path}")
    print(f"Category accuracy: {category_accuracy:.2%}")
    
    failed_cases = [
    result for result in results
    if not result.category_match
    ]

    print("\nFailed cases:")
    for result in failed_cases:
        print("-" * 80)
        print(f"Case ID: {result.case_id}")
        print(f"Input: {result.input}")
        print(f"Expected category: {result.expected_category}")
        print(f"Predicted category: {result.predicted_category}")
        print(f"Expected summary: {result.expected_summary}")
        print(f"Predicted summary: {result.predicted_summary}")

    if previous_run:
        comparison = compare_runs(previous_run, current_run)

        print("\nComparison with previous run:")
        print(f"Status: {comparison['status']}")
        print(f"Previous accuracy: {comparison['previous_accuracy']:.2%}")
        print(f"Current accuracy: {comparison['current_accuracy']:.2%}")
        print(f"Delta: {comparison['accuracy_delta']:.2%}")
        print(f"Regressions: {comparison['regressions']}")
        print(f"Improvements: {comparison['improvements']}")
    else:
        print("\nNo previous run found. This run becomes the first baseline.")


if __name__ == "__main__":
    run_evaluation()