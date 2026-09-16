from pydantic import BaseModel


class DecisionResponse(BaseModel):
    candidate_exam_id: int
    decision_type: str
    priority: str
    action: str
    target_dimension: str | None
    reason: str