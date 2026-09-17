from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class CandidateExam(Base):
    __tablename__ = "candidate_exams"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    exam_id: Mapped[int] = mapped_column(
        ForeignKey("exams.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        back_populates="candidate_exams",
    )

    exam: Mapped["Exam"] = relationship(
        back_populates="candidate_exams",
    )

    evidences: Mapped[list["Evidence"]] = relationship(
        back_populates="candidate_exam",
        cascade="all, delete-orphan",
    )