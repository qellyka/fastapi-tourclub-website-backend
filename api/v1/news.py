import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.utils import role_required, generate_slug, parse_news_form

from crud.news import (
    delete_news_by_id,
    get_news,
    get_news_by_slug,
    get_news_by_id,
    update_news,
    create_new_news,
)
from db import get_async_session
from models import UserModel
from schemas import CreateResponse
from schemas import NewsBase, NewsUpdate, NewsReadList, NewsRead
from services import s3_client

content_type_map = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}

router = APIRouter(prefix="/api", tags=["News"])


@router.get("/news", response_model=CreateResponse[List[NewsReadList]])
async def get_article_items(
    status: str | None = Query(None),
    limit: int | None = Query(None, ge=0, le=100, description="Сколько статей вернуть"),
    offset: int | None = Query(None, ge=0, description="Сколько статей пропустить"),
    session: AsyncSession = Depends(get_async_session),
):
    news_data = await get_news(session, limit=limit, offset=offset, status=status)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[NewsReadList.model_validate(news) for news in news_data],
    )


@router.get("/news/{identifier}", response_model=CreateResponse[NewsRead])
async def get_article_item(
    identifier: str,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    news = None
    try:
        news_id = int(identifier)
        news = await get_news_by_id(session, news_id)
    except ValueError:
        news = await get_news_by_slug(session, identifier)

    return CreateResponse(
        status="success",
        message="ok",
        detail=NewsRead.model_validate(news, from_attributes=True),
    )


@router.post("/news", response_model=CreateResponse[NewsReadList])
async def create_new_news_item(
    cover_file: UploadFile,
    news: NewsBase = Depends(parse_news_form),
    user: UserModel = Depends(role_required(["moderator", "admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    extension = Path(cover_file.filename).suffix.lstrip(".")

    cover_bytes = await cover_file.read()
    cover_s3_filename = f"{uuid.uuid4()}.{extension}"
    content_type = content_type_map.get(extension, "application/octet-stream")

    cover_key = await s3_client.upload_bytes(
        cover_bytes,
        cover_s3_filename,
        content_type,
        settings.S3_NEWS_MEDIA_BUCKET_NAME,
    )

    cover_s3_url = s3_client.object_url(cover_key, "news-media")

    news.slug = generate_slug(news.title)
    news.cover_s3_url = cover_s3_url

    news = await create_new_news(session, news, user.id)

    return CreateResponse(
        status="succes", message="ok", detail=NewsRead.model_validate(news)
    )


@router.patch("/news/{news_id}", response_model=CreateResponse[NewsRead])
async def update_news_item(
    news_id: int,
    update_data: NewsUpdate,
    user: UserModel = Depends(role_required(["moderator", "admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    news_data = await get_news_by_id(session, news_id)

    updated_news_data = await update_news(session, news_data, update_data, user.id)

    return CreateResponse(
        status="succes",
        message="ok",
        detail=NewsRead.model_validate(updated_news_data),
    )


@router.delete("/news/{news_id}", status_code=204)
async def delete_news_item(
    news_id: int,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    await delete_news_by_id(session, news_id)
