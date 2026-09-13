from pydantic import BaseModel


class DecisionResponse(BaseModel):
    candidate_exam_id: int
    decision_type: str
    priority: str
    action: str
    reason: str