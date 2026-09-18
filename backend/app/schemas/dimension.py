from pydantic import BaseModel


class DimensionAnalysisResponse(BaseModel):
    discipline: str
    current_value: float
    previous_value: float
    variation: float
    direction: str
    status: str
    level: str