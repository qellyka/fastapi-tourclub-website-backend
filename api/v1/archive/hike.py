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

from core.utils import role_required, gpx_to_geojson
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
    upl_file: UploadFile,
    hike: str = Form(...),
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    file = upl_file.file
    filename = upl_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())
    geojson_data = gpx_to_geojson(filename)
    hike_data = HikeBase.model_validate(json.loads(hike))
    new_hike = await create_new_hike(session, hike_data, geojson_data)
    return new_hike


@router.post("/test-upload-file")
async def get_hikes(
    upl_file: UploadFile,
):
    file = upl_file.file
    filename = upl_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())
