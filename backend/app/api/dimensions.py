from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.dimension import DimensionAnalysisResponse
from app.services.dimension_service import analyze_dimensions_service


router = APIRouter(
    prefix="/candidate-exams",
    tags=["Dimensions"],
)


@router.get(
    "/{candidate_exam_id}/dimensions",
    response_model=list[DimensionAnalysisResponse],
)
def get_dimensions(
    candidate_exam_id: int,
    db: Session = Depends(get_db),
):
    return analyze_dimensions_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )