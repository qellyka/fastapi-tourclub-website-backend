from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required
from crud.users import get_users, get_user_by_id, delete_user_by_id
from db import get_async_session
from models import UserModel
from schemas import CreateResponse, UserRead

router = APIRouter(prefix="/api", tags=["User"])


@router.get("/api/users", response_model=CreateResponse[List[UserRead]])
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


@router.get("/users/me", response_model=CreateResponse)
async def read_profile(
    current_user: UserModel = Depends(role_required(["guest"])),
):

    return CreateResponse(
        status="success",
        message="ok",
        detail={
            "username": current_user.username,
            "email": current_user.email,
            "full_name": f"{current_user.first_name} {current_user.last_name}",
            "user_id": f"{current_user.id}",
        },
    )
