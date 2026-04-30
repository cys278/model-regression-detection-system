import os
import requests
from dotenv import load_dotenv


load_dotenv()


def send_slack_alert(
    status: str,
    accuracy_delta: float,
    overall_delta: float,
    regression_count: int,
    report_path: str,
) -> None:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("SLACK_WEBHOOK_URL not set. Skipping Slack alert.")
        return

    emoji = {
        "pass": "✅",
        "warning": "⚠️",
        "critical": "🚨",
    }.get(status, "ℹ️")

    message = {
    "text": (
        f"{emoji} *LLM Evaluation Status: {status.upper()}*\n"
        f"*Accuracy delta:* {accuracy_delta}\n"
        f"*Overall score delta:* {overall_delta}\n"
        f"*Regressions detected:* {regression_count}\n"
        f"*Report file:* `{report_path}`"
    )
}

    response = requests.post(webhook_url, json=message, timeout=10)
    response.raise_for_status()