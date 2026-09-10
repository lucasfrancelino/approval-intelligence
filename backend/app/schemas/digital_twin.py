from pydantic import BaseModel


class DigitalTwinResponse(BaseModel):
    candidate_exam_id: int

    performance_current: float
    performance_previous: float
    performance_variation: float

    performance_direction: str
    performance_status: str

    evidence_count: int

    overall_status: str
    summary: str