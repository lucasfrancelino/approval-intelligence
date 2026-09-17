from sqlalchemy.orm import Session

from app.engines.decision_engine import Decision as DecisionResult
from app.models.decision import Decision as DecisionModel


def create_decision(
    db: Session,
    candidate_exam_id: int,
    decision: DecisionResult,
) -> DecisionModel:
    decision_model = DecisionModel(
        candidate_exam_id=candidate_exam_id,
        decision_type=decision.decision_type,
        priority=decision.priority,
        action=decision.action,
        target_dimension=decision.target_dimension,
        reason=decision.reason,
    )

    db.add(decision_model)
    db.commit()
    db.refresh(decision_model)

    return decision_model