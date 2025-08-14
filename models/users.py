from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from .base import Base

if TYPE_CHECKING:
    from .hikes import HikeModel


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_activated: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[List[str]] = mapped_column(ARRAY(String), default=["guest"])

    hikes_participations: Mapped[List["HikeParticipant"]] = relationship(
        "HikeParticipant", back_populates="user"
    )
    club_participant: Mapped[Optional["ClubParticipant"]] = relationship(
        "ClubParticipant", back_populates="user", uselist=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )


class HikeParticipant(Base):
    __tablename__ = "hike_participants"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    hike_id: Mapped[int] = mapped_column(ForeignKey("hikes.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String)

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="hikes_participations"
    )
    hike: Mapped["HikeModel"] = relationship(
        "HikeModel", back_populates="participants_info"
    )


class ClubParticipant(Base):
    __tablename__ = "club_participants"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="club_participant"
    )
