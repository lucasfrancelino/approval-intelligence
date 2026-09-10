from sqlalchemy.orm import Session

from app.models.candidate import Candidate


def create_candidate(
    db: Session,
    name: str,
    email: str,
) -> Candidate:
    candidate = Candidate(
        name=name,
        email=email,
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate