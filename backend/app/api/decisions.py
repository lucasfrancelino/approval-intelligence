from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.decision import (
    DecisionHistoryResponse,
    DecisionResponse,
)
from app.services.decision_service import (
    get_decision_history_service,
    get_next_best_action_service,
)

router = APIRouter(
    prefix="/candidate-exams",
    tags=["Decision Engine"],
)


@router.get(
    "/{candidate_exam_id}/next-best-action",
    response_model=DecisionResponse,
)
def get_next_best_action(
    candidate_exam_id: int,
    db: Session = Depends(get_db),
):
    result = get_next_best_action_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Não há evidências suficientes para "
                "gerar a Próxima Melhor Ação."
            ),
        )

    decision = result.decision
    recommended_action = result.recommended_action

    return DecisionResponse(
        candidate_exam_id=candidate_exam_id,
        decision_type=decision.decision_type,
        priority=decision.priority,
        action=decision.action,
        target_dimension=decision.target_dimension,
        reason=decision.reason,
        operational_action=recommended_action.operational_action,
        instructions=recommended_action.instructions,
        action_id=result.action_id,
        action_status=result.action_status,
    )

@router.get(
    "/{candidate_exam_id}/decisions",
    response_model=list[DecisionHistoryResponse],
)
def get_decision_history(
    candidate_exam_id: int,
    db: Session = Depends(get_db),
):
    decisions = get_decision_history_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    return [
        DecisionHistoryResponse(
            id=decision.id,
            candidate_exam_id=decision.candidate_exam_id,
            decision_type=decision.decision_type,
            priority=decision.priority,
            action=decision.action,
            target_dimension=decision.target_dimension,
            reason=decision.reason,
            created_at=decision.created_at,
        )
        for decision in decisions
    ]