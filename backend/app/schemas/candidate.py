from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True,
    }