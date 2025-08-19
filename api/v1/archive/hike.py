import json
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Cookie,
    File,
    UploadFile,
    Form,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required, gpx_to_geojson, parse_hike_form
from crud.hikes import get_all_hikes, create_new_hike, get_hike_by_id
from db import get_async_session
from models import HikeModel, UserModel
from schemas import HikeBase, CreateResponse, HikeRead

router = APIRouter(prefix="/api/archive", tags=["Hikes"])


@router.get("/hikes", response_model=CreateResponse[List[HikeRead]])
async def get_hikes(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hikes = await get_all_hikes(session)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[HikeRead.model_validate(hike) for hike in hikes],
    )


@router.get("/hikes/{hike_id}", response_model=CreateResponse[HikeRead])
async def get_hike_id(
    hike_id: int,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hike = await get_hike_by_id(session, hike_id)
    return CreateResponse(
        status="success",
        message="ok",
        detail=HikeRead.model_validate(hike),
    )


@router.post("/hikes", response_model=CreateResponse[HikeRead])
async def create_new_hike_report(
    report_file: UploadFile,
    gpx_file: UploadFile,
    hike: HikeBase = Depends(parse_hike_form),
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    file = gpx_file.file
    filename = gpx_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())
    geojson_data = gpx_to_geojson(filename)
    hike.report = report_file.filename
    new_hike = await create_new_hike(session, hike, geojson_data)
    return CreateResponse(
        status="success",
        message="New report of hike was created",
        detail=HikeRead.model_validate(new_hike),
    )


@router.post("/test-upload-file", response_model=CreateResponse)
async def get_hikes(
    upl_file: UploadFile,
):
    file = upl_file.file
    filename = upl_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())
    return CreateResponse(
        status="success",
        message="File uploaded",
    )
