from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.candidate_service import create_candidate_service


router = APIRouter(
    prefix="/api/candidates",
    tags=["Candidates"],
)


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(
    data: CandidateCreate,
    db: Session = Depends(get_db),
):
    return create_candidate_service(
        db=db,
        data=data,
    )