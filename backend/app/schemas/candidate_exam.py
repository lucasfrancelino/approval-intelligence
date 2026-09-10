from pydantic import BaseModel


class CandidateExamCreate(BaseModel):
    candidate_id: int
    exam_id: int


class CandidateExamResponse(BaseModel):
    id: int
    candidate_id: int
    exam_id: int

    model_config = {
        "from_attributes": True,
    }