from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, JSON, Date, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums import ItemStatus
from .associations import hike_pass_association
from .base import Base

if TYPE_CHECKING:
    from .users import UserModel
    from .passes import PassModel
    from .participants import HikeParticipantModel


class HikeModel(Base):
    __tablename__ = "hikes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # Основные поля
    tourism_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # горный, водный и т.п.
    complexity: Mapped[str] = mapped_column(
        String, nullable=False
    )  # категория похода (2 к.с.)
    region: Mapped[Optional[str]] = mapped_column(String)

    # Руководитель (связь с UserModel)
    leader_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    leader: Mapped[Optional["UserModel"]] = relationship(
        "UserModel", foreign_keys=[leader_id], back_populates="led_hikes"
    )

    # Общие сведения
    participants_count: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_days: Mapped[Optional[int]] = mapped_column(Integer)
    distance_km: Mapped[Optional[float]] = mapped_column(Float)
    difficulty_distribution: Mapped[Optional[dict]] = mapped_column(JSON)

    # Маршрут и данные
    route: Mapped[str] = mapped_column(Text, nullable=False)
    geojson_data: Mapped[Optional[dict]] = mapped_column(JSON)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Файлы
    photos_archive: Mapped[Optional[str]] = mapped_column(String)
    report_s3_key: Mapped[str] = mapped_column(String)
    route_s3_key: Mapped[str] = mapped_column(String)

    # Статус
    status: Mapped[ItemStatus] = mapped_column(nullable=False, default=ItemStatus.DRAFT)

    # Авторство
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    updated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    created_by_user: Mapped["UserModel"] = relationship(
        foreign_keys=[created_by], back_populates="created_hikes"
    )
    updated_by_user: Mapped[Optional["UserModel"]] = relationship(
        foreign_keys=[updated_by], back_populates="updated_hikes"
    )

    # Связи
    participants: Mapped[List["HikeParticipantModel"]] = relationship(
        "HikeParticipantModel",
        back_populates="hike",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    passes: Mapped[List["PassModel"]] = relationship(
        "PassModel",
        secondary=hike_pass_association,
        back_populates="hikes",
        cascade="all",
        passive_deletes=True,
    )

    @property
    def leader_fullname(self) -> Optional[str]:
        if self.leader:
            return f"{self.leader.first_name} {self.leader.last_name}".strip()
        return None

    @property
    def leader_email(self) -> Optional[str]:
        if self.leader:
            return self.leader.email
        return None
