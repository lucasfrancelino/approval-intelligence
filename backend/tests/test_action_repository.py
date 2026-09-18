from types import SimpleNamespace
from unittest.mock import Mock

from app.repositories.action_repository import (
    create_recommended_action,
)


def test_create_recommended_action():
    db = Mock()

    action = SimpleNamespace(
        operational_action="revisar_conteudos_da_dimensao",
        instructions="Revisar Português.",
        status="recommended",
    )

    result = create_recommended_action(
        db=db,
        decision_id=10,
        action=action,
    )

    added_action = db.add.call_args.args[0]

    assert added_action.decision_id == 10
    assert (
        added_action.operational_action
        == "revisar_conteudos_da_dimensao"
    )
    assert added_action.instructions == "Revisar Português."
    assert added_action.status == "recommended"

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(added_action)

    assert result is added_action