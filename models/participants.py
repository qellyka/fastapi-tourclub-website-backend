from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey, Text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .users import UserModel
    from .hikes import HikeModel


class HikeParticipantModel(Base):
    __tablename__ = "hike_participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    hike_id: Mapped[int] = mapped_column(
        ForeignKey("hikes.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column(String)

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="hike_participations"
    )
    hike: Mapped["HikeModel"] = relationship("HikeModel", back_populates="participants")

    @property
    def user_with_role(self):
        u = self.user
        u.role = self.role
        return u


class ClubParticipantModel(Base):
    __tablename__ = "club_participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    avatar_club: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="club_participations"
    )

    @property
    def user_with_description(self):
        u = self.user
        u.description = self.description
        u.avatar_club = self.avatar_club
        return u
