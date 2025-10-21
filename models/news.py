from datetime import datetime
from typing import Optional

from sqlalchemy import String, TIMESTAMP, func, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums import ItemStatus
from . import Base
from .users import UserModel


class NewsModel(Base):
    __tablename__ = "news"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    content_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    content_html: Mapped[Optional[str]] = mapped_column(Text)

    cover_s3_url: Mapped[str] = mapped_column(String, nullable=True)

    status: Mapped[ItemStatus] = mapped_column(nullable=False, default=ItemStatus.DRAFT)

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    updated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )

    created_by_user: Mapped["UserModel"] = relationship(
        foreign_keys=[created_by], back_populates="created_news"
    )
    updated_by_user: Mapped[Optional["UserModel"]] = relationship(
        foreign_keys=[updated_by], back_populates="updated_news"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
