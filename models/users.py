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
    description: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    applications: Mapped[list["ApplicationModel"]] = relationship(
        back_populates="user", lazy="selectin"
    )

    led_hikes: Mapped[List["HikeModel"]] = relationship(
        "HikeModel",
        back_populates="leader",
        foreign_keys="[HikeModel.leader_id]",
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

    created_articles = relationship(
        "ArticleModel",
        back_populates="created_by_user",
        foreign_keys="[ArticleModel.created_by]",
    )
    created_hikes = relationship(
        "HikeModel",
        back_populates="created_by_user",
        foreign_keys="[HikeModel.created_by]",
    )
    created_news = relationship(
        "NewsModel",
        back_populates="created_by_user",
        foreign_keys="[NewsModel.created_by]",
    )
    created_passes = relationship(
        "PassModel",
        back_populates="created_by_user",
        foreign_keys="[PassModel.created_by]",
    )

    updated_articles = relationship(
        "ArticleModel",
        back_populates="updated_by_user",
        foreign_keys="[ArticleModel.updated_by]",
    )
    updated_hikes = relationship(
        "HikeModel",
        back_populates="updated_by_user",
        foreign_keys="[HikeModel.updated_by]",
    )
    updated_news = relationship(
        "NewsModel",
        back_populates="updated_by_user",
        foreign_keys="[NewsModel.updated_by]",
    )
    updated_passes = relationship(
        "PassModel",
        back_populates="updated_by_user",
        foreign_keys="[PassModel.updated_by]",
    )
