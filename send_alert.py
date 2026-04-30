from generate_report import get_latest_two_runs
from src.report_generator import generate_html_report, compare_runs
from src.slack_alert import send_slack_alert


def main():
    current_run, previous_run = get_latest_two_runs()

    comparison = compare_runs(previous_run, current_run)

    report_path = generate_html_report(
        current_run=current_run,
        previous_run=previous_run,
        reports_dir="reports",
        runs_dir="runs",
    )

    send_slack_alert(
        status=comparison["status"],
        accuracy_delta=comparison["accuracy_delta"],
        overall_delta=comparison["overall_delta"],
        regression_count=len(comparison["regressions"]),
        report_path=report_path,
    )

    print("Slack alert sent.")


if __name__ == "__main__":
    main()