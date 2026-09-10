from sqlalchemy.orm import Session

from app.engines.evidence_engine import EvidenceEngine
from app.repositories.evidence_repository import (
    create_evidence,
    get_evidence_by_id_and_candidate_exam,
)
from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceInterpretationResponse,
)

from app.engines.trend_engine import TrendEngine
from app.repositories.evidence_repository import (
    get_evidences_by_candidate_exam,
)


def create_evidence_service(
    db: Session,
    candidate_exam_id: int,
    data: EvidenceCreate,
):
    return create_evidence(
        db=db,
        candidate_exam_id=candidate_exam_id,
        evidence_type=data.evidence_type,
        source_type=data.source_type,
        value=data.value,
        confidence=data.confidence,
    )


def interpret_evidence_service(
    db: Session,
    candidate_exam_id: int,
    evidence_id: int,
) -> EvidenceInterpretationResponse | None:

    evidence = get_evidence_by_id_and_candidate_exam(
        db=db,
        evidence_id=evidence_id,
        candidate_exam_id=candidate_exam_id,
    )

    if evidence is None:
        return None

    engine = EvidenceEngine()

    interpretation = engine.interpret(
        evidence_type=evidence.evidence_type,
        value=evidence.value,
    )

    return EvidenceInterpretationResponse(
        evidence_id=evidence.id,
        dimension=interpretation.dimension,
        metric=interpretation.metric,
        value=interpretation.value,
        unit=interpretation.unit,
        status=interpretation.status,
        interpretation=interpretation.interpretation,
    )

def analyze_performance_trend_service(
    db: Session,
    candidate_exam_id: int,
):
    evidences = get_evidences_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
        evidence_type="simulado",
    )

    engine = EvidenceEngine()

    values = []

    for evidence in evidences:
        interpretation = engine.interpret(
            evidence_type=evidence.evidence_type,
            value=evidence.value,
        )

        values.append(
            interpretation.value
        )

    trend_engine = TrendEngine()

    return trend_engine.analyze(
        values=values,
        metric="percentual_acerto",
    )