from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.decision import DecisionResponse
from app.services.decision_service import get_next_best_action_service


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
    decision = get_next_best_action_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Não há evidências suficientes para "
                "gerar a Próxima Melhor Ação."
            ),
        )

    return DecisionResponse(
        candidate_exam_id=candidate_exam_id,
        decision_type=decision.decision_type,
        priority=decision.priority,
        action=decision.action,
        target_dimension=decision.target_dimension,
        reason=decision.reason,
    )