from sqlalchemy.orm import Session

from app.engines.action_status import validate_transition
from app.repositories.action_repository import (
    get_action_by_id,
    get_actions_by_candidate_exam,
    update_action_status,
)


class ActionNotFoundError(Exception):
    pass


class InvalidActionTransitionError(Exception):
    pass


def get_action_history_service(
    db: Session,
    candidate_exam_id: int,
):
    return get_actions_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )


def update_action_status_service(
    db: Session,
    action_id: int,
    new_status: str,
):
    action = get_action_by_id(
        db=db,
        action_id=action_id,
    )

    if action is None:
        raise ActionNotFoundError(
            f"Ação não encontrada: {action_id}"
        )

    try:
        validate_transition(
            current_status=action.status,
            new_status=new_status,
        )
    except ValueError as error:
        raise InvalidActionTransitionError(
            str(error)
        ) from error

    return update_action_status(
        db=db,
        action_model=action,
        new_status=new_status,
    )