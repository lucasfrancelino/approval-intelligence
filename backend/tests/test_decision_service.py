from types import SimpleNamespace
from unittest.mock import patch

from app.services.decision_service import (
    NextBestActionResult,
    get_next_best_action_service,
)


def test_get_next_best_action_service():
    digital_twin = SimpleNamespace(
        performance_level="bom",
        performance_direction="evolucao",
        dimensions=[],
    )

    with patch(
        "app.services.decision_service.get_digital_twin_service",
        return_value=digital_twin,
    ), patch(
        "app.services.decision_service.create_decision",
    ) as create_decision_mock, patch(
        "app.services.decision_service.create_recommended_action",
    ) as create_action_mock:

        create_decision_mock.return_value = SimpleNamespace(
            id=10,
        )

        create_action_mock.return_value = SimpleNamespace(
            id=20,
            status="recommended",
        )

        result = get_next_best_action_service(
            db=None,
            candidate_exam_id=1,
        )

    assert isinstance(result, NextBestActionResult)

    decision = result.decision
    recommended_action = result.recommended_action

    assert decision.decision_type == "progressao"
    assert decision.priority == "baixa"
    assert decision.action == "aumentar_desafio"
    assert decision.target_discipline is None

    assert (
        recommended_action.operational_action
        == "avancar_nivel_de_dificuldade"
    )
    assert "dificuldade" in recommended_action.instructions
    assert recommended_action.status == "recommended"

    assert result.action_id == 20
    assert result.action_status == "recommended"

    create_decision_mock.assert_called_once_with(
        db=None,
        candidate_exam_id=1,
        decision=decision,
    )

    create_action_mock.assert_called_once_with(
        db=None,
        decision_id=10,
        action=recommended_action,
    )