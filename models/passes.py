from typing import List, Optional
from sqlalchemy import String, Integer, Text, ARRAY, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import hike_pass_association
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hikes import HikeModel


class PassModel(Base):
    __tablename__ = "passes"

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    region: Mapped[str] = mapped_column(String, nullable=False)
    complexity: Mapped[str] = mapped_column(String, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    photos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), default=[])

    hikes: Mapped[Optional[List["HikeModel"]]] = relationship(
        "HikeModel",
        secondary=hike_pass_association,
        back_populates="passes",
        cascade="all",
        passive_deletes=True,
    )
