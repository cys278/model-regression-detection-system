import json
from pathlib import Path
from src.eval_schemas import EvalRun


RUNS_DIR = Path("runs")


def save_eval_run(run: EvalRun) -> Path:
    RUNS_DIR.mkdir(exist_ok=True)

    path = RUNS_DIR / f"{run.run_id}.json"

    path.write_text(
        run.model_dump_json(indent=2),
        encoding="utf-8",
    )

    return path


def load_latest_run() -> EvalRun | None:
    RUNS_DIR.mkdir(exist_ok=True)

    files = sorted(RUNS_DIR.glob("*.json"))

    if not files:
        return None

    latest_file = files[-1]
    data = json.loads(latest_file.read_text(encoding="utf-8"))

    return EvalRun(**data)