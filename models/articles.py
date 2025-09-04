from datetime import datetime

from sqlalchemy import String, TIMESTAMP, func, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class ArticleModel(Base):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    content_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    content_html: Mapped[str] = mapped_column(Text, nullable=False)

    cover_s3_url: Mapped[str | None] = mapped_column(String, nullable=True)
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
