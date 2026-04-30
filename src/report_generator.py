import html
from pathlib import Path

from src.trend_tracker import calculate_avg_summary_score, calculate_overall_score, build_trend_data
from src.drift_detector import detect_drift


def safe(value) -> str:
    return html.escape(str(value))


def get_failed_cases(run: dict) -> list[dict]:
    return [
        result for result in run.get("results", [])
        if not result.get("category_match") or result.get("summary_score", 0) < 3
    ]


def compare_runs(previous_run: dict | None, current_run: dict) -> dict:
    if previous_run is None:
        return {
            "status": "pass",
            "accuracy_delta": 0,
            "overall_delta": 0,
            "regressions": [],
            "improvements": [],
        }

    previous_results = {
        result["case_id"]: result
        for result in previous_run.get("results", [])
    }

    regressions = []
    improvements = []

    for current_result in current_run.get("results", []):
        case_id = current_result["case_id"]
        previous_result = previous_results.get(case_id)

        if not previous_result:
            continue

        previous_passed = previous_result.get("category_match") is True
        current_passed = current_result.get("category_match") is True

        if previous_passed and not current_passed:
            regressions.append(current_result)

        if not previous_passed and current_passed:
            improvements.append(current_result)

    previous_accuracy = previous_run.get("category_accuracy", 0)
    current_accuracy = current_run.get("category_accuracy", 0)
    accuracy_delta = current_accuracy - previous_accuracy

    previous_overall = calculate_overall_score(previous_run)
    current_overall = calculate_overall_score(current_run)
    overall_delta = current_overall - previous_overall

    if accuracy_delta <= -0.08:
        status = "critical"
    elif accuracy_delta <= -0.03:
        status = "warning"
    else:
        status = "pass"

    return {
        "status": status,
        "accuracy_delta": round(accuracy_delta, 4),
        "overall_delta": round(overall_delta, 4),
        "regressions": regressions,
        "improvements": improvements,
    }


def render_case_table(title: str, cases: list[dict]) -> str:
    if not cases:
        return f"<h2>{safe(title)}</h2><p>No cases found.</p>"

    rows = ""

    for case in cases:
        rows += f"""
        <tr>
            <td>{safe(case.get("case_id"))}</td>
            <td>{safe(case.get("difficulty"))}</td>
            <td>{safe(case.get("input"))}</td>
            <td>{safe(case.get("expected_category"))}</td>
            <td>{safe(case.get("predicted_category"))}</td>
            <td>{safe(case.get("expected_summary"))}</td>
            <td>{safe(case.get("predicted_summary"))}</td>
            <td>{safe(case.get("summary_score"))}</td>
            <td>{safe(case.get("notes"))}</td>
        </tr>
        """

    return f"""
    <h2>{safe(title)}</h2>
    <table>
        <thead>
            <tr>
                <th>Case ID</th>
                <th>Difficulty</th>
                <th>Input</th>
                <th>Expected Category</th>
                <th>Predicted Category</th>
                <th>Expected Summary</th>
                <th>Predicted Summary</th>
                <th>Summary Score</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


def render_trend_table(trend_data: list[dict]) -> str:
    rows = ""

    for item in trend_data:
        rows += f"""
        <tr>
            <td>{safe(item["timestamp"])}</td>
            <td>{safe(item["run_id"])}</td>
            <td>{safe(item["category_accuracy"])}</td>
            <td>{safe(item["summary_score"])}</td>
            <td>{safe(item["overall_score"])}</td>
        </tr>
        """

    return f"""
    <h2>Trend Tracking</h2>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Run ID</th>
                <th>Category Accuracy</th>
                <th>Average Summary Score</th>
                <th>Overall Score</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


def generate_html_report(
    current_run: dict,
    previous_run: dict | None = None,
    reports_dir: str = "reports",
    runs_dir: str = "runs",
) -> str:
    Path(reports_dir).mkdir(exist_ok=True)

    comparison = compare_runs(previous_run, current_run)
    failed_cases = get_failed_cases(current_run)
    trend_data = build_trend_data(runs_dir=runs_dir, limit=10)
    drift = detect_drift(runs_dir=runs_dir)

    avg_summary_score = calculate_avg_summary_score(current_run)
    overall_score = calculate_overall_score(current_run)

    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Evaluation Report - {safe(current_run.get("run_id"))}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 32px;
                background: #f7f7f7;
                color: #222;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin-bottom: 24px;
                border-radius: 8px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            }}

            .status-pass {{
                color: #0a7f3f;
                font-weight: bold;
            }}

            .status-warning {{
                color: #b26b00;
                font-weight: bold;
            }}

            .status-critical {{
                color: #b00020;
                font-weight: bold;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin-bottom: 24px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                vertical-align: top;
                font-size: 14px;
            }}

            th {{
                background: #eeeeee;
            }}

            h1, h2 {{
                margin-top: 0;
            }}

            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 16px;
            }}

            .metric {{
                background: #fafafa;
                padding: 16px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }}

            .metric strong {{
                display: block;
                font-size: 24px;
                margin-top: 8px;
            }}
        </style>
    </head>
    <body>
        <h1>LLM Evaluation Report</h1>

        <div class="card">
            <h2>Run Metadata</h2>
            <p><strong>Run ID:</strong> {safe(current_run.get("run_id"))}</p>
            <p><strong>Timestamp:</strong> {safe(current_run.get("timestamp"))}</p>
            <p><strong>Prompt Version:</strong> {safe(current_run.get("prompt_version"))}</p>
            <p><strong>Model:</strong> {safe(current_run.get("model"))}</p>
            <p><strong>Total Cases:</strong> {safe(current_run.get("total_cases"))}</p>
            <p><strong>Status:</strong> 
                <span class="status-{safe(comparison["status"])}">
                    {safe(comparison["status"]).upper()}
                </span>
            </p>
        </div>

        <div class="card">
            <h2>Score Summary</h2>
            <div class="metric-grid">
                <div class="metric">
                    Category Accuracy
                    <strong>{round(current_run.get("category_accuracy", 0) * 100, 2)}%</strong>
                </div>
                <div class="metric">
                    Average Summary Score
                    <strong>{avg_summary_score}/5</strong>
                </div>
                <div class="metric">
                    Overall Score
                    <strong>{overall_score}</strong>
                </div>
                <div class="metric">
                    Failed Cases
                    <strong>{len(failed_cases)}</strong>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Regression Summary</h2>
            <p><strong>Accuracy Delta:</strong> {comparison["accuracy_delta"]}</p>
            <p><strong>Overall Score Delta:</strong> {comparison["overall_delta"]}</p>
            <p><strong>Regressions:</strong> {len(comparison["regressions"])}</p>
            <p><strong>Improvements:</strong> {len(comparison["improvements"])}</p>
        </div>

        <div class="card">
            <h2>Drift Detection</h2>
            <p><strong>Drift Detected:</strong> {safe(drift["drift_detected"])}</p>
            <p><strong>Reason:</strong> {safe(drift["reason"])}</p>
            <p><strong>Rolling Average:</strong> {safe(drift["rolling_average"])}</p>
            <p><strong>Baseline Score:</strong> {safe(drift["baseline_score"])}</p>
            <p><strong>Delta:</strong> {safe(drift.get("delta"))}</p>
        </div>

        <div class="card">
            {render_case_table("Failed Cases", failed_cases)}
        </div>

        <div class="card">
            {render_case_table("Regressions", comparison["regressions"])}
        </div>

        <div class="card">
            {render_case_table("Improvements", comparison["improvements"])}
        </div>

        <div class="card">
            {render_trend_table(trend_data)}
        </div>
    </body>
    </html>
    """

    report_path = Path(reports_dir) / f"report_{current_run.get('run_id')}.html"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    latest_path = Path(reports_dir) / "report_latest.html"

    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    return str(report_path)