from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Any


Category = Literal["billing", "technical", "account", "general"]


class ClassifierOutput(BaseModel):
    category: Category
    summary: str = Field(min_length=1)


class PromptConfig(BaseModel):
    version: str
    created_at: str
    system_prompt: str
    few_shot_examples: List[Dict[str, Any]] = []