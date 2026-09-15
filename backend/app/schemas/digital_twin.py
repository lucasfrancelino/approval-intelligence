from pydantic import BaseModel

from app.schemas.dimension import DimensionAnalysisResponse


class DigitalTwinResponse(BaseModel):
    candidate_exam_id: int

    performance_current: float
    performance_previous: float
    performance_variation: float

    performance_direction: str
    performance_status: str

    performance_level: str
    performance_consistency: str

    evidence_count: int

    overall_status: str
    summary: str

    dimensions: list[DimensionAnalysisResponse]