from sqlalchemy.orm import Session

from app.engines.action_engine import RecommendedAction as ActionResult
from app.models.decision import Decision as DecisionModel
from app.models.recommended_action import (
    RecommendedAction as RecommendedActionModel,
)


def create_recommended_action(
    db: Session,
    decision_id: int,
    action: ActionResult,
) -> RecommendedActionModel:
    action_model = RecommendedActionModel(
        decision_id=decision_id,
        operational_action=action.operational_action,
        instructions=action.instructions,
        status=action.status,
    )

    db.add(action_model)
    db.commit()
    db.refresh(action_model)

    return action_model


def get_equivalent_action(
    db: Session,
    decision_id: int,
    action: ActionResult,
) -> RecommendedActionModel | None:
    return (
        db.query(RecommendedActionModel)
        .filter(
            RecommendedActionModel.decision_id == decision_id,
            RecommendedActionModel.operational_action
            == action.operational_action,
            RecommendedActionModel.instructions == action.instructions,
            RecommendedActionModel.status.in_(
                [
                    "recommended",
                    "in_progress",
                ]
            ),
        )
        .order_by(
            RecommendedActionModel.created_at.desc(),
            RecommendedActionModel.id.desc(),
        )
        .first()
    )


def get_actions_by_candidate_exam(
    db: Session,
    candidate_exam_id: int,
) -> list[RecommendedActionModel]:
    return (
        db.query(RecommendedActionModel)
        .join(
            DecisionModel,
            DecisionModel.id == RecommendedActionModel.decision_id,
        )
        .filter(
            DecisionModel.candidate_exam_id == candidate_exam_id,
        )
        .order_by(
            RecommendedActionModel.created_at.desc(),
            RecommendedActionModel.id.desc(),
        )
        .all()
    )


def get_action_by_id(
    db: Session,
    action_id: int,
) -> RecommendedActionModel | None:
    return (
        db.query(RecommendedActionModel)
        .filter(
            RecommendedActionModel.id == action_id,
        )
        .first()
    )


def update_action_status(
    db: Session,
    action_model: RecommendedActionModel,
    new_status: str,
) -> RecommendedActionModel:
    action_model.status = new_status

    db.add(action_model)
    db.commit()
    db.refresh(action_model)

    return action_model