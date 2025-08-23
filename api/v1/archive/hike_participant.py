from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required
from crud import get_user_by_email_or_username
from crud.hikes import get_hike_by_id
from crud.participants import create_hike_participant, get_hike_participants
from crud.users import get_user_by_id
from db import get_async_session
from models import UserModel
from schemas import HikeParticipantBase, CreateResponse, UserRead
from schemas.users import UserHikeParticipant

router = APIRouter(prefix="/archive", tags=["Archive"])


@router.get(
    "/hikes/{hikes_id}/participants",
    response_model=CreateResponse[List[UserHikeParticipant]],
)
async def get_all_hike_participants(
    hike_id: int,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    participants = await get_hike_participants(session, hike_id)
    detail = [
        UserHikeParticipant.model_validate(p.user_with_role, from_attributes=True)
        for p in participants
    ]
    return CreateResponse(
        status="succes",
        message="ok",
        detail=detail,
    )


@router.post("/participants", response_model=CreateResponse)
async def create_new_hike_participant(
    participant: HikeParticipantBase,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):

    hike = await get_hike_by_id(session, participant.hike_id)
    user = await get_user_by_id(session, participant.user_id)

    if not hike or not user:
        raise HTTPException(status_code=404, detail="Hike or User not found")

    await create_hike_participant(
        session, participant.hike_id, participant.user_id, participant.role
    )

    return CreateResponse(
        status="success",
        message=f"Связь добавлена: Hike {hike.id} -> User {user.id}",
        detail=None,
    )
