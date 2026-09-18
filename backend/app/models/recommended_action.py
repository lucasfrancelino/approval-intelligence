from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RecommendedAction(Base):
    __tablename__ = "recommended_actions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    decision_id: Mapped[int] = mapped_column(
        ForeignKey("decisions.id"),
        nullable=False,
        index=True,
    )

    operational_action: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    instructions: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="recommended",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    decision: Mapped["Decision"] = relationship(
        back_populates="recommended_actions",
    )