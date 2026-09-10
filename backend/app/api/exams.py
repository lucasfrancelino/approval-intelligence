from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.exam import ExamCreate, ExamResponse
from app.services.exam_service import create_exam_service


router = APIRouter(
    prefix="/api/exams",
    tags=["Exams"],
)


@router.post(
    "",
    response_model=ExamResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exam(
    data: ExamCreate,
    db: Session = Depends(get_db),
):
    return create_exam_service(
        db=db,
        data=data,
    )