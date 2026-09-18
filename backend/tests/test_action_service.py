from unittest.mock import patch

from app.services.action_service import get_action_history_service


def test_get_action_history_service():
    with patch(
        "app.services.action_service.get_actions_by_candidate_exam",
    ) as get_actions_mock:

        get_actions_mock.return_value = ["ação-1", "ação-2"]

        result = get_action_history_service(
            db=None,
            candidate_exam_id=1,
        )

    assert result == ["ação-1", "ação-2"]

    get_actions_mock.assert_called_once_with(
        db=None,
        candidate_exam_id=1,
    )