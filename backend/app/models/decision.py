from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    candidate_exam_id: Mapped[int] = mapped_column(
        ForeignKey("candidate_exams.id"),
        nullable=False,
        index=True,
    )

    decision_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_dimension: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    candidate_exam: Mapped["CandidateExam"] = relationship(
        back_populates="decisions",
    )

    recommended_actions: Mapped[
        list["RecommendedAction"]
    ] = relationship(
        back_populates="decision",
        cascade="all, delete-orphan",
    )