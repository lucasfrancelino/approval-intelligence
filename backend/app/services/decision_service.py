from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.engines.action_engine import (
    ActionEngine,
    RecommendedAction,
)
from app.engines.decision_engine import Decision, DecisionEngine
from app.repositories.action_repository import (
    create_recommended_action,
    get_equivalent_action,
)
from app.repositories.decision_repository import (
    create_decision,
    get_decisions_by_candidate_exam,
    get_equivalent_decision,
)
from app.services.digital_twin_service import get_digital_twin_service


@dataclass
class NextBestActionResult:
    decision: Decision
    recommended_action: RecommendedAction
    action_id: int
    action_status: str


def get_next_best_action_service(
    db: Session,
    candidate_exam_id: int,
) -> NextBestActionResult | None:
    digital_twin = get_digital_twin_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    if digital_twin is None:
        return None

    decision_engine = DecisionEngine()

    decision = decision_engine.decide(
        digital_twin=digital_twin,
    )

    action_engine = ActionEngine()

    recommended_action = action_engine.translate(
        decision=decision,
    )

    decision_model = get_equivalent_decision(
        db=db,
        candidate_exam_id=candidate_exam_id,
        decision=decision,
    )

    if decision_model is None:
        decision_model = create_decision(
            db=db,
            candidate_exam_id=candidate_exam_id,
            decision=decision,
        )

    action_model = get_equivalent_action(
        db=db,
        decision_id=decision_model.id,
        action=recommended_action,
    )

    if action_model is None:
        action_model = create_recommended_action(
            db=db,
            decision_id=decision_model.id,
            action=recommended_action,
        )

    return NextBestActionResult(
        decision=decision,
        recommended_action=recommended_action,
        action_id=action_model.id,
        action_status=action_model.status,
    )


def get_decision_history_service(
    db: Session,
    candidate_exam_id: int,
):
    return get_decisions_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )