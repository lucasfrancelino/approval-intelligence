from sqlalchemy import text

from app.core.database import engine
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_action_history_endpoint_with_real_database():
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT id
                FROM candidate_exams
                ORDER BY id
                LIMIT 1
                """
            )
        )

        row = result.fetchone()

    assert row is not None

    candidate_exam_id = row[0]

    response = client.get(
        f"/api/candidate-exams/{candidate_exam_id}/actions"
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    if body:
        first_action = body[0]

        assert "id" in first_action
        assert "decision_id" in first_action
        assert "operational_action" in first_action
        assert "instructions" in first_action
        assert "status" in first_action
        assert "created_at" in first_action