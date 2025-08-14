from typing import List, Optional
from sqlalchemy import String, Integer, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import hike_pass_association
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hikes import HikeModel


class PassModel(Base):
    __tablename__ = "passes"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), default=[])

    hikes: Mapped[Optional[List["HikeModel"]]] = relationship(
        "HikeModel",  # <-- строка вместо прямого импорта
        secondary=hike_pass_association,
        back_populates="passes",
    )
