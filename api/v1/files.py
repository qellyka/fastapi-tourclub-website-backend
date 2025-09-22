from fastapi import APIRouter, UploadFile, Depends
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required
from db import get_async_session
from models import UserModel
from schemas import CreateResponse
from services import s3_client

router = APIRouter(prefix="/api/upload", tags=["Files"])


@router.post("/files", response_model=CreateResponse[str])
async def upload_file(
    bucket_name: str,
    file: UploadFile,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    s3_filename = f"media_content/{uuid4()}_{file.filename}"
    file_bytes = await file.read()

    await s3_client.upload_bytes(
        file_bytes,
        s3_filename,
        file.content_type or "application/octet-stream",
        bucket_name,
        "inline",
    )
    bucket_word_keys = bucket_name.split("-")
    url = s3_client.object_url(
        bucket_url=f"{bucket_word_keys[1]}-{bucket_word_keys[-1]}", key=s3_filename
    )

    return CreateResponse(
        status="success",
        message="Файл загружен",
        detail=url,
    )
