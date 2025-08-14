from typing import List, Optional
from sqlalchemy import String, Integer, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import hike_pass_association
from .base import Base


class PassModel(Base):
    __tablename__ = "passes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), default=[])

    hikes: Mapped[Optional[List["HikeModel"]]] = relationship(
        "HikeModel",  # <-- строка вместо прямого импорта
        secondary=hike_pass_association,
        back_populates="passes",
        default=[],
    )
