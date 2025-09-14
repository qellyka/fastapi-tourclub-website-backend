from datetime import datetime
from typing import Optional

from sqlalchemy import String, TIMESTAMP, func, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class ArticleModel(Base):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    # staus: Mapped[str] =

    content_json: Mapped[Optional[dict]] = mapped_column(JSONB)

    content_html: Mapped[Optional[str]] = mapped_column(Text)

    cover_s3_url: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column()

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
