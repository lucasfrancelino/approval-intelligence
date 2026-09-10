from fastapi import FastAPI

from app.core.config import settings
from app.services.database_service import check_database_connection

from app.api.candidates import router as candidates_router
from app.api.exams import router as exams_router
from app.api.candidate_exams import router as candidate_exams_router
from app.api.evidences import router as evidences_router
from app.api.digital_twin import router as digital_twin_router


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API principal do Approval Intelligence.",
)

app.include_router(candidates_router)
app.include_router(exams_router)
app.include_router(candidate_exams_router)
app.include_router(evidences_router)
app.include_router(
    digital_twin_router,
    prefix="/api",
)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "application": settings.app_name,
        "version": "0.1.0",
    }


@app.get("/api/health/database")
def database_health_check():
    database_connected = check_database_connection()

    if database_connected:
        return {
            "status": "ok",
            "database": "connected",
        }

    return {
        "status": "error",
        "database": "disconnected",
    }