import uuid
from typing import List
import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Path, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from core.config import settings
from core.utils import (
    role_required,
    gpx_to_geojson,
    parse_hike_form,
    generate_slug,
    parse_update_hike_form,
)
from crud.hikes import (
    get_all_hikes,
    create_new_hike,
    get_hike_by_id,
    delete_hike_by_id,
    get_hike_by_slug,
    update_hike,
)
from db import get_async_session
from models import UserModel
from schemas import HikeBase, CreateResponse, HikeRead, HikesRead, HikeUpdate
from services import s3_client

router = APIRouter(prefix="/api/archive", tags=["Hikes"])


@router.get("/hikes", response_model=CreateResponse[List[HikesRead]])
async def get_hikes(
    status: str | None = Query(None),
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    hikes = await get_all_hikes(session, status)

    return CreateResponse(
        status="success",
        message="ok",
        detail=[HikesRead.model_validate(hike) for hike in hikes],
    )


@router.get("/hikes/{identification}", response_model=CreateResponse[HikeRead])
async def get_hike_id(
    identification: str,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):

    if identification.isdigit():
        hike = await get_hike_by_id(session, int(identification))
    else:
        hike = await get_hike_by_slug(session, identification)

    return CreateResponse(
        status="success",
        message="ok",
        detail=HikeRead.model_validate(hike),
    )


@router.delete("/hikes/{hike_id}", status_code=204)
async def delete_hike(
    hike_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["admin"])),
):
    await delete_hike_by_id(session, hike_id)


@router.post("/hikes", response_model=CreateResponse[HikeRead])
async def create_new_hike_report(
    report_file: UploadFile,
    gpx_file: UploadFile,
    hike: HikeBase = Depends(parse_hike_form),
    user: UserModel = Depends(role_required(["moderator", "admin"])),
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

    await s3_client.upload_bytes(
        gpx_bytes,
        gpx_s3_filename,
        "application/gpx+xml",
        settings.S3_HIKE_MEDIA_BUCKET_NAME,
        "attachment",
    )
    await s3_client.upload_bytes(
        report_bytes,
        report_s3_filename,
        "application/pdf",
        settings.S3_HIKE_MEDIA_BUCKET_NAME,
        "inline",
    )

    hike.slug = generate_slug(hike.name)
    hike.report_s3_key = report_s3_filename
    hike.route_s3_key = gpx_s3_filename
    new_hike = await create_new_hike(session, hike, geojson_data, user.id)
    return CreateResponse(
        status="success",
        message="New report of hike was created",
        detail=HikeRead.model_validate(new_hike),
    )


@router.get("/hikes/{hike_id}/file/{file_type}")
async def get_hike_file(
    hike_id: int,
    file_type: str = Path(..., regex="^(report|route)$"),
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(role_required(["guest"])),
):
    hike = await get_hike_by_id(session, hike_id)
    if not hike:
        raise HTTPException(status_code=404, detail="Hike not found")

    key_map = {
        "report": hike.report_s3_key,
        "route": hike.route_s3_key,
    }
    s3_key = key_map.get(file_type)
    if not s3_key:
        raise HTTPException(
            status_code=404, detail=f"{file_type.capitalize()} file not found"
        )

    obj = await s3_client.get_object(
        s3_key, bucket_name=settings.S3_HIKE_MEDIA_BUCKET_NAME
    )
    if not obj:
        raise HTTPException(status_code=404, detail="File not found in S3")

    data, content_type = obj
    return StreamingResponse(
        io.BytesIO(data),
        media_type=content_type,
        headers={"Content-Disposition": f'inline; filename="{s3_key}"'},
    )


@router.patch("/hikes/{hike_id}", response_model=CreateResponse[HikeRead])
async def update_hike_item(
    hike_id: int,
    update_data: HikeUpdate = Depends(parse_update_hike_form),
    report_file: UploadFile | None = File(None),
    gpx_file: UploadFile | None = File(None),
    user: UserModel = Depends(role_required(["moderator", "admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    report_s3_filename = None
    gpx_s3_filename = None
    geojson_data = None
    if report_file:
        report_bytes = await report_file.read()
        report_s3_filename = f"{uuid.uuid4()}.pdf"

        await s3_client.upload_bytes(
            report_bytes,
            report_s3_filename,
            "application/pdf",
            settings.S3_HIKE_MEDIA_BUCKET_NAME,
            "inline",
        )
    if gpx_file:
        if not gpx_file.filename.lower().endswith(".gpx"):
            raise HTTPException(status_code=400, detail="Only GPX files are allowed")

        if gpx_file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large")

        gpx_s3_filename = f"{uuid.uuid4()}.gpx"
        gpx_bytes = await gpx_file.read()
        geojson_data = gpx_to_geojson(gpx_bytes)

        await s3_client.upload_bytes(
            gpx_bytes,
            gpx_s3_filename,
            "application/gpx+xml",
            settings.S3_HIKE_MEDIA_BUCKET_NAME,
            "attachment",
        )

    hike_data = await get_hike_by_id(session, hike_id)

    updated_hike_data = await update_hike(
        session,
        hike_data,
        update_data,
        gpx_s3_filename,
        report_s3_filename,
        geojson_data,
        user.id,
    )

    return CreateResponse(
        status="succes",
        message="ok",
        detail=HikeRead.model_validate(updated_hike_data),
    )
