from sqlalchemy.orm import Session

from app.repositories.action_repository import (
    get_actions_by_candidate_exam,
)


def get_action_history_service(
    db: Session,
    candidate_exam_id: int,
):
    return get_actions_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )