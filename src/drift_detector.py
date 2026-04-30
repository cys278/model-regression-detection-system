from src.trend_tracker import build_trend_data


def detect_drift(
    runs_dir: str = "runs",
    window_size: int = 7,
    drift_threshold: float = 0.03,
) -> dict:
    trend_data = build_trend_data(runs_dir=runs_dir, limit=window_size + 1)

    if len(trend_data) < window_size + 1:
        return {
            "drift_detected": False,
            "reason": "Not enough runs for drift detection.",
            "rolling_average": None,
            "baseline_score": None,
        }

    baseline_score = trend_data[0]["overall_score"]

    recent_scores = [
        item["overall_score"]
        for item in trend_data[-window_size:]
    ]

    rolling_average = sum(recent_scores) / len(recent_scores)
    delta = rolling_average - baseline_score

    return {
        "drift_detected": delta <= -drift_threshold,
        "reason": (
            "Slow drift detected."
            if delta <= -drift_threshold
            else "No slow drift detected."
        ),
        "rolling_average": round(rolling_average, 4),
        "baseline_score": round(baseline_score, 4),
        "delta": round(delta, 4),
    }