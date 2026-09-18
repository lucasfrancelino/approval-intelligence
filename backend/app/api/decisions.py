from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.action import RecommendedActionHistoryResponse
from app.schemas.decision import (
    DecisionHistoryResponse,
    DecisionResponse,
)
from app.services.action_service import get_action_history_service
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

    return DecisionResponse(
        candidate_exam_id=candidate_exam_id,
        decision_type=result.decision.decision_type,
        priority=result.decision.priority,
        action=result.decision.action,
        target_dimension=result.decision.target_dimension,
        reason=result.decision.reason,
        operational_action=result.recommended_action.operational_action,
        instructions=result.recommended_action.instructions,
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


@router.get(
    "/{candidate_exam_id}/actions",
    response_model=list[RecommendedActionHistoryResponse],
)
def get_action_history(
    candidate_exam_id: int,
    db: Session = Depends(get_db),
):
    actions = get_action_history_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    return [
        RecommendedActionHistoryResponse(
            id=action.id,
            decision_id=action.decision_id,
            operational_action=action.operational_action,
            instructions=action.instructions,
            status=action.status,
            created_at=action.created_at,
        )
        for action in actions
    ]