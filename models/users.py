from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from .base import Base

if TYPE_CHECKING:
    from .hikes import HikeModel
    from .participants import HikeParticipantModel, ClubParticipantModel
    from .applications import ApplicationModel


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_activated: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[List[str]] = mapped_column(ARRAY(String), default=["guest"])
    is_banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    applications: Mapped[list["ApplicationModel"]] = relationship(
        back_populates="user", lazy="selectin"
    )

    hike_participations: Mapped[List["HikeParticipantModel"]] = relationship(
        "HikeParticipantModel",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    club_participations: Mapped[List["ClubParticipantModel"]] = relationship(
        "ClubParticipantModel",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
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
