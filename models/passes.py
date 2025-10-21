from typing import List, Optional
from sqlalchemy import String, Integer, Text, ARRAY, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums import ItemStatus
from .associations import hike_pass_association
from . import Base
from .users import UserModel

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
    status: Mapped[ItemStatus] = mapped_column(nullable=False, default=ItemStatus.DRAFT)

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    updated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )

    created_by_user: Mapped["UserModel"] = relationship(
        foreign_keys=[created_by], back_populates="created_passes"
    )
    updated_by_user: Mapped[Optional["UserModel"]] = relationship(
        foreign_keys=[updated_by], back_populates="updated_passes"
    )

    hikes: Mapped[Optional[List["HikeModel"]]] = relationship(
        "HikeModel",
        secondary=hike_pass_association,
        back_populates="passes",
        cascade="all",
        passive_deletes=True,
    )
