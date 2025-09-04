import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.utils import role_required, generate_slug
from crud.articles import create_new_article
from db import get_async_session
from models import UserModel
from schemas import CreateResponse
from schemas import ArticleBase
from services import s3_client

content_type_map = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}

router = APIRouter(prefix="/api", tags=["Article"])


@router.get("/article", response_model=CreateResponse)
async def get_articles(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    pass


@router.get("/article/{article_id}")
async def get_article_item(
    article_id: int,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    pass


@router.post("/article")
async def create_new_article_item(
    cover_file: UploadFile,
    article: ArticleBase,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    extension = Path(cover_file.filename).suffix.lstrip(".")

    cover_bytes = await cover_file.read()
    cover_s3_filename = f"{uuid.uuid4()}."
    content_type = content_type_map.get(extension, "application/octet-stream")

    cover_key = await s3_client.upload_bytes(
        cover_bytes,
        cover_s3_filename,
        content_type,
        settings.S3_USER_MEDIA_BUCKET_NAME,
    )

    cover_s3_url = s3_client.object_url(cover_key)

    article.slug = generate_slug(article.title)
    article.cover_s3_url = cover_s3_url

    await create_new_article(session, article)


@router.patch("/article/{article_id}")
async def update_article_item(
    article_id: int,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    pass


@router.delete("/article/{article_id}")
async def delete_article_item(
    article_id: int,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    pass
