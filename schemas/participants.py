from datetime import date
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class HikeParticipantBase(BaseModel):
    user_id: int
    hike_id: int
    role: str


class HikeParticipantRead(HikeParticipantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ClubParticipantBase(BaseModel):
    user_id: int
    description: str


class ClubParticipantRead(ClubParticipantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
