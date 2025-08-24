from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, JSON, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import hike_pass_association
from .base import Base

if TYPE_CHECKING:
    from .users import UserModel
    from .passes import PassModel
    from .participants import HikeParticipantModel


class HikeModel(Base):
    __tablename__ = "hikes"

    name: Mapped[str] = mapped_column(String, nullable=False)
    complexity: Mapped[str] = mapped_column(String, nullable=False)
    route: Mapped[str] = mapped_column(Text, nullable=False)
    geojson_data: Mapped[Optional[dict]] = mapped_column(JSON)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos_archive: Mapped[Optional[str]] = mapped_column(String)
    report_s3_key: Mapped[str] = mapped_column(String)
    route_s3_key: Mapped[str] = mapped_column(String)

    participants: Mapped[List["HikeParticipantModel"]] = relationship(
        "HikeParticipantModel", back_populates="hike"
    )

    passes: Mapped[List["PassModel"]] = relationship(
        "PassModel", secondary=hike_pass_association, back_populates="hikes"
    )
