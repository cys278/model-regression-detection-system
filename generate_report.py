import json
from pathlib import Path

from src.report_generator import generate_html_report


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_latest_two_runs(runs_dir: str = "runs") -> tuple[dict, dict | None]:
    run_files = sorted(
        Path(runs_dir).glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not run_files:
        raise FileNotFoundError("No run JSON files found in /runs.")

    current_run = load_json(run_files[0])
    previous_run = load_json(run_files[1]) if len(run_files) > 1 else None

    return current_run, previous_run


def main():
    current_run, previous_run = get_latest_two_runs()

    report_path = generate_html_report(
        current_run=current_run,
        previous_run=previous_run,
        reports_dir="reports",
        runs_dir="runs",
    )

    print(f"HTML report generated: {report_path}")
    print("Latest report also saved as: reports/report_latest.html")


if __name__ == "__main__":
    main()