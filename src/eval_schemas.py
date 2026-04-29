from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


Category = Literal["billing", "technical", "account", "general"]


class ExpectedOutput(BaseModel):
    category: Category
    summary: str


class GoldenCase(BaseModel):
    id: str
    input: str
    expected_output: ExpectedOutput
    difficulty: Literal["easy", "medium", "hard"]
    notes: str


class ModelOutput(BaseModel):
    category: Category
    summary: str


class CaseEvalResult(BaseModel):
    case_id: str
    input: str
    expected_category: Category
    predicted_category: Category
    expected_summary: str
    predicted_summary: str
    category_match: bool
    summary_score: Optional[int] = None
    latency_ms: float
    difficulty: str
    notes: str


class EvalRun(BaseModel):
    run_id: str
    timestamp: datetime
    prompt_version: str
    model: str
    total_cases: int
    category_accuracy: float
    results: list[CaseEvalResult]