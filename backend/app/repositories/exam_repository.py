from sqlalchemy.orm import Session

from app.models.exam import Exam


def create_exam(
    db: Session,
    name: str,
    institution: str,
    organizer: str | None = None,
) -> Exam:
    exam = Exam(
        name=name,
        institution=institution,
        organizer=organizer,
    )

    db.add(exam)
    db.commit()
    db.refresh(exam)

    return exam