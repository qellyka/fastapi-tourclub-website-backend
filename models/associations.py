from sqlalchemy import Column, ForeignKey, Table

from .base import Base

hike_pass_association = Table(
    "hike_pass_association",
    Base.metadata,
    Column("hike_id", ForeignKey("hikes.id", ondelete="CASCADE"), primary_key=True),
    Column("pass_id", ForeignKey("passes.id", ondelete="CASCADE"), primary_key=True),
)
