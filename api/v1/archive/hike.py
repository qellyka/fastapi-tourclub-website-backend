from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required
from crud.hikes import get_all_hikes, create_new_hike
from db import get_async_session
from models import HikeModel, UserModel
from schemas import HikeBase

router = APIRouter(prefix="/api/archive", tags=["Hikes"])


@router.get("/hikes")
async def get_hikes(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hikes = await get_all_hikes(session)
    return hikes


@router.post("/hikes")
async def get_hikes(
    hike: HikeBase,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    new_hike = await create_new_hike(session, hike)
    return new_hike
