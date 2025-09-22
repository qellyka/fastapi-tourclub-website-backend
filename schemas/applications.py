from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from models import ApplicationStatus
from .users import UserRead


class ApplicationCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    date_of_birth: date
    email: str
    phone_number: str
    vk_profile: Optional[str]
    experience: str
    previous_school: Optional[str]
    how_heard: Optional[str]
    question: Optional[str]
    wishes: Optional[str]
    consent: bool


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    middle_name: Optional[str]
    date_of_birth: date
    email: str
    phone_number: str
    vk_profile: Optional[str]
    experience: str
    previous_school: Optional[str]
    how_heard: Optional[str]
    question: Optional[str]
    wishes: Optional[str]
    consent: bool
    status: ApplicationStatus
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationAdminListItem(BaseModel):
    id: int
    user: UserRead
    status: ApplicationStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class ApplicationUpdateAdmin(BaseModel):
    status: ApplicationStatus
    comment: Optional[str]


ApplicationAdminListItem.model_rebuild()
