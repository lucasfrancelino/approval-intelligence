from sqlalchemy import text
from fastapi.testclient import TestClient

from app.core.database import engine
from app.main import app


client = TestClient(app)


def test_dimensions_api_with_real_database():

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
        f"/api/candidate-exams/{candidate_exam_id}/dimensions"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)