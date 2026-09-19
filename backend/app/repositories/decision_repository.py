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
        target_discipline=decision.target_discipline,
        reason=decision.reason,
    )

    db.add(decision_model)
    db.commit()
    db.refresh(decision_model)

    return decision_model


def get_equivalent_decision(
    db: Session,
    candidate_exam_id: int,
    decision: DecisionResult,
) -> DecisionModel | None:
    return (
        db.query(DecisionModel)
        .filter(
            DecisionModel.candidate_exam_id == candidate_exam_id,
            DecisionModel.decision_type == decision.decision_type,
            DecisionModel.priority == decision.priority,
            DecisionModel.action == decision.action,
            DecisionModel.target_discipline
            == decision.target_discipline,
            DecisionModel.reason == decision.reason,
        )
        .order_by(
            DecisionModel.created_at.desc(),
            DecisionModel.id.desc(),
        )
        .first()
    )


def get_decisions_by_candidate_exam(
    db: Session,
    candidate_exam_id: int,
) -> list[DecisionModel]:
    return (
        db.query(DecisionModel)
        .filter(
            DecisionModel.candidate_exam_id == candidate_exam_id,
        )
        .order_by(
            DecisionModel.created_at.desc(),
            DecisionModel.id.desc(),
        )
        .all()
    )