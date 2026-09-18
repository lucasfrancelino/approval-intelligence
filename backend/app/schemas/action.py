from datetime import datetime

from pydantic import BaseModel


class RecommendedActionHistoryResponse(BaseModel):
    id: int
    decision_id: int
    operational_action: str
    instructions: str
    status: str
    created_at: datetime