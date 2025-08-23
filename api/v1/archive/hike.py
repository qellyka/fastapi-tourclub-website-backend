import json
import tempfile
import uuid
from pathlib import Path
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
from schemas import HikeBase, CreateResponse, HikeRead, HikesRead

router = APIRouter(prefix="/api/archive", tags=["Hikes"])


@router.get("/hikes", response_model=CreateResponse[List[HikesRead]])
async def get_hikes(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hikes = await get_all_hikes(session)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[HikesRead.model_validate(hike) for hike in hikes],
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
    if not gpx_file.filename.lower().endswith(".gpx"):
        raise HTTPException(status_code=400, detail="Only GPX files are allowed")

    if gpx_file.size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File too large")

    safe_filename = f"{uuid.uuid4()}.gpx"

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / safe_filename

        with open(file_path, "wb") as f:
            content = await gpx_file.read()
            f.write(content)

        geojson_data = gpx_to_geojson(str(file_path))

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
