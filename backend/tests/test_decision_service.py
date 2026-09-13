from types import SimpleNamespace
from unittest.mock import patch

from app.services.decision_service import get_next_best_action_service


def test_get_next_best_action_service():

    digital_twin = SimpleNamespace(
        performance_level="bom",
        performance_direction="evolucao",
    )

    with patch(
        "app.services.decision_service.get_digital_twin_service",
        return_value=digital_twin,
    ):

        decision = get_next_best_action_service(
            db=None,
            candidate_exam_id=1,
        )

    assert decision.decision_type == "progressao"
    assert decision.priority == "baixa"
    assert decision.action == "aumentar_desafio"