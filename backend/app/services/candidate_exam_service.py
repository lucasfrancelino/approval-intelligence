from sqlalchemy.orm import Session

from app.repositories.candidate_exam_repository import create_candidate_exam
from app.schemas.candidate_exam import CandidateExamCreate


def create_candidate_exam_service(
    db: Session,
    data: CandidateExamCreate,
):
    return create_candidate_exam(
        db=db,
        candidate_id=data.candidate_id,
        exam_id=data.exam_id,
    )