from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceCreate(BaseModel):
    evidence_type: str
    dimension: str | None = None
    metric: str | None = None
    source_type: str
    value: str
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


class EvidenceResponse(BaseModel):
    id: int
    candidate_exam_id: int
    evidence_type: str
    dimension: str | None
    metric: str | None
    source_type: str
    value: str
    confidence: float | None
    observed_at: datetime

    model_config = {"from_attributes": True}


class EvidenceInterpretationResponse(BaseModel):
    evidence_id: int
    dimension: str
    metric: str
    value: float
    unit: str
    status: str
    interpretation: str

class TrendAnalysisResponse(BaseModel):
    metric: str
    current_value: float
    previous_value: float
    variation: float
    direction: str
    status: str
    interpretation: str