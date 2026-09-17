from datetime import datetime

from pydantic import BaseModel


class DecisionResponse(BaseModel):
    candidate_exam_id: int
    decision_type: str
    priority: str
    action: str
    target_dimension: str | None
    reason: str


class DecisionHistoryResponse(BaseModel):
    id: int
    candidate_exam_id: int
    decision_type: str
    priority: str
    action: str
    target_dimension: str | None
    reason: str
    created_at: datetime