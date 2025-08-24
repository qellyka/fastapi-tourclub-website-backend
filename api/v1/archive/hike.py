import json
import mimetypes
import tempfile
import uuid
from pathlib import Path
from typing import List
import io

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
from starlette.responses import StreamingResponse

from core.utils import role_required, gpx_to_geojson, parse_hike_form
from crud.hikes import get_all_hikes, create_new_hike, get_hike_by_id
from db import get_async_session
from models import HikeModel, UserModel
from schemas import HikeBase, CreateResponse, HikeRead, HikesRead
from services import s3_client

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

    gpx_s3_filename = f"{uuid.uuid4()}.gpx"
    gpx_bytes = await gpx_file.read()
    geojson_data = gpx_to_geojson(gpx_bytes)

    report_bytes = await report_file.read()
    report_s3_filename = f"{uuid.uuid4()}.pdf"

    await s3_client.upload_bytes(gpx_bytes, gpx_s3_filename, "application/gpx+xml")
    await s3_client.upload_bytes(report_bytes, report_s3_filename, "application/pdf")

    hike.report_s3_key = report_s3_filename
    hike.route_s3_key = gpx_s3_filename
    new_hike = await create_new_hike(session, hike, geojson_data)
    return CreateResponse(
        status="success",
        message="New report of hike was created",
        detail=HikeRead.model_validate(new_hike),
    )


@router.get("/hikes/{hike_id}/report")
async def get_hike_report(
    hike_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["guest"])),
):
    hike = await get_hike_by_id(session, hike_id)
    if not hike or not hike.report_s3_key:
        raise HTTPException(status_code=404, detail="Report not found")

    obj = await s3_client.get_object(hike.report_s3_key)
    if not obj:
        raise HTTPException(status_code=404, detail="File not found")

    data, content_type = obj
    return StreamingResponse(
        io.BytesIO(data),
        media_type=content_type,
        headers={"Content-Disposition": f'inline; filename="{hike.report_s3_key}"'},
    )
