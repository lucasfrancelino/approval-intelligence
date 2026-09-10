from sqlalchemy.orm import Session

from app.repositories.candidate_repository import create_candidate
from app.schemas.candidate import CandidateCreate


def create_candidate_service(
    db: Session,
    data: CandidateCreate,
):
    return create_candidate(
        db=db,
        name=data.name,
        email=data.email,
    )