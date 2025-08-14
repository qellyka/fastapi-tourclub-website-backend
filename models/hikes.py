from typing import List, Optional
from sqlalchemy import String, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import hike_pass_association
from .base import Base
from .users import HikeParticipant


class HikeModel(Base):
    __tablename__ = "hikes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    route: Mapped[str] = mapped_column(Text, nullable=False)
    geojson_data: Mapped[Optional[dict]] = mapped_column(JSON)
    start_date: Mapped[Optional[str]] = mapped_column(String)
    end_date: Mapped[Optional[str]] = mapped_column(String)
    region: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos_archive: Mapped[Optional[str]] = mapped_column(String)

    participants_info: Mapped[Optional[List["HikeParticipant"]]] = relationship(
        back_populates="hike", default=[]
    )
    passes: Mapped[Optional[List["PassModel"]]] = relationship(
        "PassModel",  # <-- строка вместо прямого импорта
        secondary=hike_pass_association,
        back_populates="hikes",
        default=[],
    )
