from sqlalchemy.orm import Session

from app.repositories.exam_repository import create_exam
from app.schemas.exam import ExamCreate


def create_exam_service(
    db: Session,
    data: ExamCreate,
):
    return create_exam(
        db=db,
        name=data.name,
        institution=data.institution,
        organizer=data.organizer,
    )