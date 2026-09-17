from sqlalchemy.orm import Session

from app.core.constants import (
    EVIDENCE_TYPE_SIMULADO,
    GENERAL_DIMENSION,
    SUPPORTED_METRIC,
)
from app.engines.digital_twin_engine import DigitalTwinEngine
from app.engines.evidence_engine import EvidenceEngine
from app.engines.performance_engine import PerformanceEngine
from app.repositories.evidence_repository import (
    get_evidences_by_candidate_exam,
)
from app.services.dimension_service import (
    analyze_dimensions_service,
)


def get_digital_twin_service(
    db: Session,
    candidate_exam_id: int,
):
    evidences = get_evidences_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
        evidence_type=EVIDENCE_TYPE_SIMULADO,
    )

    evidence_engine = EvidenceEngine()

    performance_values = []

    for evidence in evidences:

        # Apenas evidências gerais participam do desempenho geral.
        # Evidências de Português, Matemática, Direito etc. são
        # processadas exclusivamente pelo Dimension Engine.
        if (
            evidence.dimension is not None
            and evidence.dimension != GENERAL_DIMENSION
        ):
            continue

        if (
            evidence.metric is not None
            and evidence.metric != SUPPORTED_METRIC
        ):
            continue

        try:
            interpretation = evidence_engine.interpret(
                evidence_type=evidence.evidence_type,
                value=evidence.value,
            )

        except (ValueError, TypeError):
            continue

        performance_values.append(interpretation.value)

    performance_engine = PerformanceEngine()

    try:
        performance = performance_engine.analyze(
            values=performance_values,
        )

    except ValueError:
        return None

    dimensions = analyze_dimensions_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    digital_twin_engine = DigitalTwinEngine()

    return digital_twin_engine.build(
        candidate_exam_id=candidate_exam_id,
        performance=performance,
        dimensions=dimensions,
    )