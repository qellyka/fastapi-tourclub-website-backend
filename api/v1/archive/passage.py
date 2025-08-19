from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required, parse_pass_form
from crud.additional import get_pass_hikes
from db import get_async_session
from models import UserModel
from schemas import CreateResponse, PassBase, PassRead, HikeRead
from crud.passes import get_all_passes, get_pass_by_id, create_new_pass

router = APIRouter(prefix="/archive", tags=["Passes"])


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


@router.get("/passes/{pass_id}", response_model=CreateResponse[PassRead])
async def get_pass_id(
    pass_id: int,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    pas = await get_pass_by_id(session, pass_id)
    return CreateResponse(
        status="success",
        message="ok",
        detail=PassRead.model_validate(pas),
    )


@router.post("/passes", response_model=CreateResponse[PassRead])
async def create_new_pass_report(
    pas: PassBase = Depends(parse_pass_form),
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    new_pass = await create_new_pass(session, pas)
    return CreateResponse(
        status="success",
        message="New report of pass was created",
        detail=PassRead.model_validate(new_pass),
    )


@router.get("/passes/{pass_id}/hikes", response_model=CreateResponse[List[HikeRead]])
async def get_pass_hikes_reports(
    pass_id: int,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hikes = await get_pass_hikes(session, pass_id)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[HikeRead.model_validate(hike) for hike in hikes],
    )
