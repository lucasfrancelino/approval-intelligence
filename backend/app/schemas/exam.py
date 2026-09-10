from pydantic import BaseModel


class ExamCreate(BaseModel):
    name: str
    institution: str
    organizer: str | None = None


class ExamResponse(BaseModel):
    id: int
    name: str
    institution: str
    organizer: str | None

    model_config = {
        "from_attributes": True,
    }
    