from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.services.action_service import (
    ActionNotFoundError,
    InvalidActionTransitionError,
    update_action_status_service,
)


def test_update_action_status_service():
    action = SimpleNamespace(
        id=1,
        status="recommended",
    )

    updated_action = SimpleNamespace(
        id=1,
        decision_id=10,
        operational_action="revisar_conteudos_da_dimensao",
        instructions="Revisar conteúdos.",
        status="in_progress",
        created_at=None,
    )

    with patch(
        "app.services.action_service.get_action_by_id",
        return_value=action,
    ), patch(
        "app.services.action_service.update_action_status",
        return_value=updated_action,
    ) as update_mock:

        result = update_action_status_service(
            db=None,
            action_id=1,
            new_status="in_progress",
        )

    assert result is updated_action

    update_mock.assert_called_once_with(
        db=None,
        action_model=action,
        new_status="in_progress",
    )


def test_update_action_status_action_not_found():
    with patch(
        "app.services.action_service.get_action_by_id",
        return_value=None,
    ):
        with pytest.raises(ActionNotFoundError):
            update_action_status_service(
                db=None,
                action_id=999,
                new_status="in_progress",
            )


def test_update_action_status_invalid_transition():
    action = SimpleNamespace(
        id=1,
        status="completed",
    )

    with patch(
        "app.services.action_service.get_action_by_id",
        return_value=action,
    ):
        with pytest.raises(InvalidActionTransitionError):
            update_action_status_service(
                db=None,
                action_id=1,
                new_status="in_progress",
            )