from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import hike_pass_association
from .base import Base

if TYPE_CHECKING:
    from .users import HikeParticipant
    from .passes import PassModel


class HikeModel(Base):
    __tablename__ = "hikes"

    name: Mapped[str] = mapped_column(String, nullable=False)
    complexity: Mapped[str] = mapped_column(String, nullable=False)
    route: Mapped[str] = mapped_column(Text, nullable=False)
    geojson_data: Mapped[Optional[dict]] = mapped_column(JSON)
    start_date: Mapped[Optional[str]] = mapped_column(String)
    end_date: Mapped[Optional[str]] = mapped_column(String)
    region: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos_archive: Mapped[Optional[str]] = mapped_column(String)

    participants_info: Mapped[List["HikeParticipant"]] = relationship(
        "HikeParticipant", back_populates="hike"
    )
    passes: Mapped[List["PassModel"]] = relationship(
        "PassModel", secondary=hike_pass_association, back_populates="hikes"
    )
