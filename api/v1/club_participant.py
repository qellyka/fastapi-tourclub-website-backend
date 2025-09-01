import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.utils import role_required, parse_participant_form
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
from services import s3_client

router = APIRouter(prefix="/api/club", tags=["Club"])


content_type_map = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}


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
    avatar: UploadFile,
    participant: ClubParticipantBase = Depends(parse_participant_form),
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_id(session, participant.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    extension = Path(avatar.filename).suffix.lstrip(".")

    avatar_s3_filename = f"{uuid.uuid4()}.{extension}"
    avatar_bytes = await avatar.read()
    content_type = content_type_map.get(extension, "application/octet-stream")

    avatar_key = await s3_client.upload_bytes(
        avatar_bytes,
        avatar_s3_filename,
        content_type,
        settings.S3_USER_MEDIA_BUCKET_NAME,
    )
    avatar_s3_url = s3_client.object_url(avatar_key)

    await create_club_participant(
        session, participant.user_id, participant.description, avatar=avatar_s3_url
    )

    return CreateResponse(
        status="success",
        message=f"Добавлен новый участник клуба: User {user.id}",
        detail=None,
    )
