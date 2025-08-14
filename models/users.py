from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from .base import Base


class UserModel(AsyncAttrs, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    is_activated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    roles: Mapped[List[str]] = mapped_column(ARRAY(String), default=["guest"])
