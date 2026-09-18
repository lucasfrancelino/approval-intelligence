from sqlalchemy.orm import Session

from app.engines.action_engine import RecommendedAction as ActionResult
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