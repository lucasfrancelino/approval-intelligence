from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Garante que todos os models sejam registrados na declarative registry
# antes de qualquer mapper ser configurado (evita InvalidRequestError
# ao resolver forward references como "Decision" em relationship()).
import app.models  # noqa: F401

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)