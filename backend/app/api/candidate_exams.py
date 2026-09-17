from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.candidate_exam import (
    CandidateExamCreate,
    CandidateExamResponse,
)
from app.services.candidate_exam_service import (
    create_candidate_exam_service,
)

router = APIRouter(
    prefix="/candidate-exams",
    tags=["Candidate Exams"],
)

@router.post(
    "",
    response_model=CandidateExamResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_exam(
    data: CandidateExamCreate,
    db: Session = Depends(get_db),
):
    return create_candidate_exam_service(
        db=db,
        data=data,
    )