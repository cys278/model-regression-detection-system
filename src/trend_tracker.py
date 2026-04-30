import json
from pathlib import Path


def load_run(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_summary_score(value) -> float:
    """Convert invalid summary scores (None, missing) to 0 safely."""
    if isinstance(value, (int, float)):
        return value
    return 0.0


def calculate_avg_summary_score(run: dict) -> float:
    """
    Average summary score.
    Skip invalid/null values instead of treating them as 0.
    """
    scores = [
        r.get("summary_score")
        for r in run.get("results", [])
        if isinstance(r.get("summary_score"), (int, float))
    ]

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 4)


def calculate_overall_score(run: dict) -> float:
    """
    Combined score:
    0.7 * category + 0.3 * summary
    Handles None safely.
    """
    results = run.get("results", [])

    if not results:
        return 0.0

    total = 0.0

    for result in results:
        category_score = 1.0 if result.get("category_match") else 0.0

        raw_summary_score = result.get("summary_score")
        summary_score = normalize_summary_score(raw_summary_score)

        normalized_summary_score = summary_score / 5

        combined = (0.7 * category_score) + (0.3 * normalized_summary_score)
        total += combined

    return round(total / len(results), 4)


def get_latest_runs(runs_dir: str | Path = "runs", limit: int = 10) -> list[dict]:
    runs_path = Path(runs_dir)

    run_files = sorted(
        runs_path.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    runs = [load_run(path) for path in run_files[:limit]]
    return runs


def build_trend_data(runs_dir: str | Path = "runs", limit: int = 10) -> list[dict]:
    runs = get_latest_runs(runs_dir, limit)

    trend_data = []

    for run in reversed(runs):
        trend_data.append(
            {
                "run_id": run.get("run_id"),
                "timestamp": run.get("timestamp"),
                "category_accuracy": run.get("category_accuracy", 0),
                "summary_score": calculate_avg_summary_score(run),
                "overall_score": calculate_overall_score(run),
            }
        )

    return trend_data