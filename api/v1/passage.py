from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required, generate_slug
from crud.additional import get_pass_hikes
from db import get_async_session
from models import UserModel
from schemas import CreateResponse, PassBase, PassRead, HikesRead, PassUpdate
from crud.passes import (
    get_all_passes,
    get_pass_by_id,
    create_new_pass,
    update_pass,
    get_pass_by_slug,
)

router = APIRouter(prefix="/api/archive", tags=["Passes"])


@router.get("/passes", response_model=CreateResponse[List[PassRead]])
async def get_passes(
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["guest"])),
):
    passes = await get_all_passes(session)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[PassRead.model_validate(pass_stmt) for pass_stmt in passes],
    )


@router.get("/passes/{identification}", response_model=CreateResponse[PassRead])
async def get_pass_id(
    identification: str,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    if identification.isdigit():
        pass_stmt = await get_pass_by_id(session, int(identification))
    else:
        pass_stmt = await get_pass_by_slug(session, identification)

    return CreateResponse(
        status="success",
        message="ok",
        detail=PassRead.model_validate(pass_stmt),
    )


@router.post("/passes", response_model=CreateResponse[PassRead])
async def create_new_pass_report(
    pass_stmt: PassBase,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    pass_stmt.slug = generate_slug(pass_stmt.name)
    new_pass = await create_new_pass(session, pass_stmt)
    return CreateResponse(
        status="success",
        message="New report of pass was created",
        detail=PassRead.model_validate(new_pass),
    )


@router.get("/passes/{pass_id}/hikes", response_model=CreateResponse[List[HikesRead]])
async def get_pass_hikes_reports(
    pass_id: int,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hikes = await get_pass_hikes(session, pass_id)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[HikesRead.model_validate(hike) for hike in hikes],
    )


@router.patch("/passes/{pass_id}", response_model=CreateResponse[PassRead])
async def update_pass_item(
    pass_id: int,
    data: PassUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    db_pass = await get_pass_by_id(session, pass_id)
    updated_pass = await update_pass(session, db_pass, data)

    return CreateResponse(
        status="success",
        message="Pass updated successfully",
        detail=PassRead.model_validate(updated_pass),
    )
