from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required
from crud import get_user_by_email_or_username
from crud.hikes import get_hike_by_id
from crud.participants import (
    create_hike_participant,
    get_hike_participants,
    get_club_participants,
    create_club_participant,
)
from crud.users import get_user_by_id
from db import get_async_session
from models import UserModel
from schemas import ClubParticipantBase, CreateResponse, UserRead
from schemas.participants import ClubParticipantBase
from schemas.users import UserClubParticipant

router = APIRouter(prefix="/club", tags=["Club"])


@router.get(
    "/participants",
    response_model=CreateResponse[List[UserClubParticipant]],
)
async def get_all_hike_participants(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    participants = await get_club_participants(session)
    detail = [
        UserClubParticipant.model_validate(
            p.user_with_description, from_attributes=True
        )
        for p in participants
    ]
    return CreateResponse(
        status="succes",
        message="ok",
        detail=detail,
    )


@router.post("/participants", response_model=CreateResponse)
async def create_new_hike_participant(
    participant: ClubParticipantBase,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_id(session, participant.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await create_club_participant(session, participant.user_id, participant.description)

    return CreateResponse(
        status="success",
        message=f"Добавлен новый участник клуба: User {user.id}",
        detail=None,
    )
