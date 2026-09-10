from app.core.database import engine
from app.models import Base

# Importa os modelos para que o SQLAlchemy registre as tabelas.
from app.models import Candidate, Exam, CandidateExam


print("Criando tabelas...")

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso.")