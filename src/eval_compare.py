from src.eval_schemas import EvalRun


WARNING_DROP = 0.03
CRITICAL_DROP = 0.08


def compare_runs(previous: EvalRun, current: EvalRun) -> dict:
    accuracy_delta = current.category_accuracy - previous.category_accuracy

    previous_by_id = {
        result.case_id: result
        for result in previous.results
    }

    regressions = []
    improvements = []

    for current_result in current.results:
        previous_result = previous_by_id.get(current_result.case_id)

        if previous_result is None:
            continue

        if previous_result.category_match and not current_result.category_match:
            regressions.append(current_result.case_id)

        if not previous_result.category_match and current_result.category_match:
            improvements.append(current_result.case_id)

    if accuracy_delta <= -CRITICAL_DROP:
        status = "critical"
    elif accuracy_delta <= -WARNING_DROP:
        status = "warning"
    else:
        status = "pass"

    return {
        "status": status,
        "previous_accuracy": previous.category_accuracy,
        "current_accuracy": current.category_accuracy,
        "accuracy_delta": accuracy_delta,
        "regressions": regressions,
        "improvements": improvements,
    }