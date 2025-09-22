from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, Boolean, DateTime, Enum, ForeignKey
from datetime import datetime
import enum

from models import Base

if TYPE_CHECKING:
    from .users import UserModel


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ApplicationModel(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    vk_profile: Mapped[str | None] = mapped_column(String, nullable=True)

    experience: Mapped[str] = mapped_column(String, nullable=False)
    previous_school: Mapped[str | None] = mapped_column(String, nullable=True)
    how_heard: Mapped[str | None] = mapped_column(String, nullable=True)
    question: Mapped[str | None] = mapped_column(String, nullable=True)
    wishes: Mapped[str | None] = mapped_column(String, nullable=True)
    consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.pending
    )
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["UserModel"] = relationship(back_populates="applications")
