import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.utils import role_required
from crud.users import (
    get_users,
    get_user_by_id,
    delete_user_by_id,
    update_user_avatar,
    update_user,
)
from db import get_async_session
from models import UserModel
from schemas import CreateResponse, UserRead, UserUpdate
from services import s3_client

router = APIRouter(prefix="/api", tags=["User"])


@router.get("/users", response_model=CreateResponse[List[UserRead]])
async def get_all_users(
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["admin"])),
):
    users = await get_users(session)

    return CreateResponse(
        status="success",
        message="ok",
        detail=[UserRead.model_validate(user) for user in users],
    )


@router.get("/users/me", response_model=CreateResponse[UserRead])
async def read_profile(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    return CreateResponse(
        status="success",
        message="ok",
        detail=UserRead.model_validate(user),
    )


@router.get("/users/{user_id}", response_model=CreateResponse[UserRead])
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["admin"])),
):
    db_user = await get_user_by_id(session, user_id)
    return CreateResponse(
        status="success", message="ok", detail=UserRead.model_validate(db_user)
    )


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["admin"])),
):
    deleted_user = await delete_user_by_id(session, user_id)


@router.post("/upload/avatar", response_model=CreateResponse[UserRead])
async def upload_avatar(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["guest"])),
):
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"avatars/{uuid.uuid4()}{ext}"

    file_bytes = await file.read()

    await s3_client.upload_bytes(
        file_bytes,
        filename,
        file.content_type,
        settings.S3_USER_MEDIA_BUCKET_NAME,
        "inline",
    )

    file_url = s3_client.object_url(filename, "user-media")

    user = await update_user_avatar(session, file_url, user.id)

    return CreateResponse(
        status="success",
        message="Аватарка успешно загружена",
        detail=UserRead.model_validate(user),
    )


@router.patch("/users/me/update", response_model=CreateResponse[UserRead])
async def update_user_item(
    update_data: UserUpdate,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    user_data = await get_user_by_id(session, user.id)

    updated_user_data = await update_user(session, user_data, update_data)

    return CreateResponse(
        status="succes",
        message="ok",
        detail=UserRead.model_validate(updated_user_data),
    )
