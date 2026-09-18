from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.action import (
    ActionStatusResponse,
    UpdateActionStatusRequest,
)
from app.services.action_service import (
    ActionNotFoundError,
    InvalidActionTransitionError,
    update_action_status_service,
)

router = APIRouter(
    prefix="/actions",
    tags=["Action Engine"],
)


@router.patch(
    "/{action_id}/status",
    response_model=ActionStatusResponse,
)
def update_action_status(
    action_id: int,
    payload: UpdateActionStatusRequest,
    db: Session = Depends(get_db),
):
    try:
        action = update_action_status_service(
            db=db,
            action_id=action_id,
            new_status=payload.status,
        )
    except ActionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except InvalidActionTransitionError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return ActionStatusResponse(
        id=action.id,
        decision_id=action.decision_id,
        operational_action=action.operational_action,
        instructions=action.instructions,
        status=action.status,
        created_at=action.created_at,
    )