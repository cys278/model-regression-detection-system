import yaml
from pathlib import Path

from src.schemas import PromptConfig


def load_prompt_config(path: str | Path) -> PromptConfig:
    path = Path(path)

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return PromptConfig(**data)