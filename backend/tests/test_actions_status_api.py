from sqlalchemy import text
from fastapi.testclient import TestClient

from app.core.database import engine
from app.main import app


client = TestClient(app)


def test_update_action_status_api_with_real_database():
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT id
                FROM recommended_actions
                WHERE status = 'recommended'
                ORDER BY id
                LIMIT 1
                """
            )
        )

        row = result.fetchone()

    assert row is not None

    action_id = row[0]

    response = client.patch(
        f"/api/actions/{action_id}/status",
        json={
            "status": "in_progress",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == action_id
    assert body["status"] == "in_progress"
    assert "decision_id" in body
    assert "operational_action" in body
    assert "instructions" in body
    assert "created_at" in body

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                UPDATE recommended_actions
                SET status = 'recommended'
                WHERE id = :action_id
                """
            ),
            {
                "action_id": action_id,
            },
        )