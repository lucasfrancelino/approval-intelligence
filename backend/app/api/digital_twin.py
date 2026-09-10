from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.digital_twin import DigitalTwinResponse
from app.services.digital_twin_service import (
    get_digital_twin_service,
)


router = APIRouter(
    prefix="/candidate-exams",
    tags=["Digital Twin"],
)


@router.get(
    "/{candidate_exam_id}/digital-twin",
    response_model=DigitalTwinResponse,
)
def get_digital_twin(
    candidate_exam_id: int,
    db: Session = Depends(get_db),
):

    result = get_digital_twin_service(
        db=db,
        candidate_exam_id=candidate_exam_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Não há evidências suficientes para construir "
                "o Gêmeo Digital."
            ),
        )

    return result