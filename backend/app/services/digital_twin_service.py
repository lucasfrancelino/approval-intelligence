from sqlalchemy.orm import Session

from app.engines.digital_twin_engine import DigitalTwinEngine
from app.engines.evidence_engine import EvidenceEngine
from app.engines.performance_engine import PerformanceEngine
from app.repositories.evidence_repository import (
    get_evidences_by_candidate_exam,
)


def get_digital_twin_service(
    db: Session,
    candidate_exam_id: int,
):

    evidences = get_evidences_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
        evidence_type="simulado",
    )

    evidence_engine = EvidenceEngine()

    values = []

    for evidence in evidences:
        interpretation = evidence_engine.interpret(
            evidence_type=evidence.evidence_type,
            value=evidence.value,
        )

        values.append(interpretation.value)

    performance_engine = PerformanceEngine()

    try:
        performance = performance_engine.analyze(
            values=values,
        )

    except ValueError:
        return None

    digital_twin_engine = DigitalTwinEngine()

    return digital_twin_engine.build(
        candidate_exam_id=candidate_exam_id,
        performance=performance,
    )