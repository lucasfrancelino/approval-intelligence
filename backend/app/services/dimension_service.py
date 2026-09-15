from sqlalchemy.orm import Session

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
        evidence_type="simulado",
    )

    evidence_engine = EvidenceEngine()

    dimensions: dict[str, list[float]] = {}

    for evidence in evidences:

        if evidence.dimension is None:
            continue

        if evidence.metric not in {None, "percentual_acerto"}:
            continue

        try:
            interpretation = evidence_engine.interpret(
                evidence_type=evidence.evidence_type,
                value=evidence.value,
            )

            value = float(interpretation.value)

        except (ValueError, TypeError):
            continue

        dimensions.setdefault(
            evidence.dimension,
            [],
        ).append(value)

    dimension_engine = DimensionEngine()

    analyses = []

    for dimension, values in dimensions.items():

        if len(values) < 2:
            continue

        analysis = dimension_engine.analyze(
            dimension=dimension,
            values=values,
        )

        analyses.append(
            DimensionAnalysisResponse(
                dimension=analysis.dimension,
                current_value=analysis.current_value,
                previous_value=analysis.previous_value,
                variation=analysis.variation,
                direction=analysis.direction,
                status=analysis.status,
                level=analysis.level,
            )
        )

    return analyses