from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceResponse,
    EvidenceInterpretationResponse,
    TrendAnalysisResponse,
)

from app.services.evidence_service import (
    create_evidence_service,
    interpret_evidence_service,
    analyze_performance_trend_service,
)


router = APIRouter(
    prefix="/api/candidate-exams",
    tags=["Evidences"],
)


@router.post(
    "/{candidate_exam_id}/evidences",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_evidence(
    candidate_exam_id: int,
    data: EvidenceCreate,
    db: Session = Depends(get_db),
):
    return create_evidence_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
        data=data,
    )


@router.get(
    "/{candidate_exam_id}/evidences/{evidence_id}/interpretation",
    response_model=EvidenceInterpretationResponse,
)
def interpret_evidence(
    candidate_exam_id: int,
    evidence_id: int,
    db: Session = Depends(get_db),
):
    interpretation = interpret_evidence_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
        evidence_id=evidence_id,
    )

    if interpretation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidência não encontrada para esta prova do candidato.",
        )

    return interpretation

@router.get(
    "/{candidate_exam_id}/trends/performance",
    response_model=TrendAnalysisResponse,
)
def analyze_performance_trend(
    candidate_exam_id: int,
    db: Session = Depends(get_db),
):
    try:
        return analyze_performance_trend_service(
            db=db,
            candidate_exam_id=candidate_exam_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )