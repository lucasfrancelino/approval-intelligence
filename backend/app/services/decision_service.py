from sqlalchemy.orm import Session

from app.engines.decision_engine import DecisionEngine
from app.services.digital_twin_service import get_digital_twin_service


def get_next_best_action_service(
    db: Session,
    candidate_exam_id: int,
):
    digital_twin = get_digital_twin_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    if digital_twin is None:
        return None

    decision_engine = DecisionEngine()

    return decision_engine.decide(
        digital_twin=digital_twin,
    )