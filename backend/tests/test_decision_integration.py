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
        result = get_next_best_action_service(
            db=db,
            candidate_exam_id=candidate_exam_id,
        )

        assert result is not None

        assert result.decision is not None
        assert result.decision.decision_type
        assert result.decision.priority
        assert result.decision.action
        assert result.decision.reason

        assert result.recommended_action is not None
        assert result.recommended_action.operational_action
        assert result.recommended_action.instructions
        assert result.recommended_action.status == "recommended"

        assert result.action_id is not None
        assert result.action_status == "recommended"

    finally:
        db.close()