from sqlalchemy.orm import Session

from app.core.constants import (
    EVIDENCE_TYPE_SIMULADO,
    GENERAL_DISCIPLINE,
    SUPPORTED_METRIC,
)
from app.engines.dimension_engine import DimensionEngine
from app.engines.evidence_engine import EvidenceEngine
from app.repositories.evidence_repository import (
    get_evidences_by_candidate_exam,
)
from app.schemas.dimension import DimensionAnalysisResponse


def analyze_dimensions_service(
    db: Session,
    candidate_exam_id: int,
) -> list[DimensionAnalysisResponse]:

    evidences = get_evidences_by_candidate_exam(
        db=db,
        candidate_exam_id=candidate_exam_id,
        evidence_type=EVIDENCE_TYPE_SIMULADO,
    )

    evidence_engine = EvidenceEngine()

    disciplines: dict[str, list[float]] = {}

    for evidence in evidences:

        # O desempenho geral é representado pelo bloco principal
        # do Digital Twin e não deve ser duplicado nesta coleção.
        if (
            evidence.discipline is None
            or evidence.discipline == GENERAL_DISCIPLINE
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

            value = float(interpretation.value)

        except (ValueError, TypeError):
            continue

        disciplines.setdefault(
            evidence.discipline,
            [],
        ).append(value)

    dimension_engine = DimensionEngine()

    analyses: list[DimensionAnalysisResponse] = []

    for discipline, values in disciplines.items():

        if len(values) < 2:
            continue

        analysis = dimension_engine.analyze(
            discipline=discipline,
            values=values,
        )

        analyses.append(
            DimensionAnalysisResponse(
                discipline=analysis.discipline,
                current_value=analysis.current_value,
                previous_value=analysis.previous_value,
                variation=analysis.variation,
                direction=analysis.direction,
                status=analysis.status,
                level=analysis.level,
                classification=analysis.classification,
                gap_type=analysis.gap_type,
            )
        )

    return analyses