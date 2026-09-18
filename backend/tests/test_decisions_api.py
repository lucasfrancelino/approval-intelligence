from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_next_best_action_endpoint():

    digital_twin = SimpleNamespace(
        performance_level="bom",
        performance_direction="evolucao",
        dimensions=[],
    )

    with patch(
        "app.services.decision_service.get_digital_twin_service",
        return_value=digital_twin,
    ):

        response = client.get(
            "/api/candidate-exams/1/next-best-action"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_exam_id"] == 1
    assert data["decision_type"] == "progressao"
    assert data["priority"] == "baixa"
    assert data["action"] == "aumentar_desafio"
    assert data["target_discipline"] is None
    assert "reason" in data