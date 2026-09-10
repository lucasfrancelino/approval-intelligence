from sqlalchemy.orm import Session

from app.models.candidate_exam import CandidateExam


def create_candidate_exam(
    db: Session,
    candidate_id: int,
    exam_id: int,
) -> CandidateExam:
    candidate_exam = CandidateExam(
        candidate_id=candidate_id,
        exam_id=exam_id,
    )

    db.add(candidate_exam)
    db.commit()
    db.refresh(candidate_exam)

    return candidate_exam