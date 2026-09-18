from types import SimpleNamespace
from unittest.mock import Mock

from app.repositories.action_repository import (
    create_recommended_action,
    get_actions_by_candidate_exam,
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


def test_get_actions_by_candidate_exam():
    db = Mock()

    expected_actions = [
        SimpleNamespace(id=2, decision_id=8),
        SimpleNamespace(id=1, decision_id=7),
    ]

    query_mock = db.query.return_value
    join_mock = query_mock.join.return_value
    filter_mock = join_mock.filter.return_value
    order_by_mock = filter_mock.order_by.return_value
    order_by_mock.all.return_value = expected_actions

    result = get_actions_by_candidate_exam(
        db=db,
        candidate_exam_id=1,
    )

    assert result == expected_actions

    db.query.assert_called_once()
    query_mock.join.assert_called_once()
    join_mock.filter.assert_called_once()
    filter_mock.order_by.assert_called_once()
    order_by_mock.all.assert_called_once()