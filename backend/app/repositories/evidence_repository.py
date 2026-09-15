from sqlalchemy.orm import Session

from app.models.evidence import Evidence


def create_evidence(
    db: Session,
    candidate_exam_id: int,
    evidence_type: str,
    dimension: str | None,
    metric: str | None,
    source_type: str,
    value: str,
    confidence: float | None = None,
) -> Evidence:

    evidence = Evidence(
        candidate_exam_id=candidate_exam_id,
        evidence_type=evidence_type,
        dimension=dimension,
        metric=metric,
        source_type=source_type,
        value=value,
        confidence=confidence,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence


def get_evidence_by_id(
    db: Session,
    evidence_id: int,
) -> Evidence | None:

    return (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )


def get_evidence_by_id_and_candidate_exam(
    db: Session,
    evidence_id: int,
    candidate_exam_id: int,
) -> Evidence | None:

    return (
        db.query(Evidence)
        .filter(
            Evidence.id == evidence_id,
            Evidence.candidate_exam_id == candidate_exam_id,
        )
        .first()
    )


def get_evidences_by_candidate_exam(
    db: Session,
    candidate_exam_id: int,
    evidence_type: str | None = None,
    dimension: str | None = None,
) -> list[Evidence]:

    query = (
        db.query(Evidence)
        .filter(
            Evidence.candidate_exam_id == candidate_exam_id
        )
    )

    if evidence_type is not None:
        query = query.filter(
            Evidence.evidence_type == evidence_type
        )

    if dimension is not None:
        query = query.filter(
            Evidence.dimension == dimension
        )

    return (
        query
        .order_by(Evidence.observed_at.asc())
        .all()
    )