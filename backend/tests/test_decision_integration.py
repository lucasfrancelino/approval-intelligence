from sqlalchemy import text

from app.core.database import SessionLocal, engine
from app.services.decision_service import get_next_best_action_service


def test_next_best_action_with_real_database():
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

    db = SessionLocal()

    try:
        decision = get_next_best_action_service(
            db=db,
            candidate_exam_id=candidate_exam_id,
        )

        assert decision is not None
        assert decision.decision_type
        assert decision.priority
        assert decision.action
        assert decision.reason

    finally:
        db.close()