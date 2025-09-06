import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.utils import role_required, generate_slug, parse_article_form
from crud.articles import (
    create_new_article,
    get_article_by_id,
    update_article,
    delete_article_by_id,
    get_article_by_slug,
    get_articles,
)
from db import get_async_session
from models import UserModel
from schemas import CreateResponse
from schemas import ArticleBase, ArticleUpdate, ArticlesRead, ArticleRead
from services import s3_client

content_type_map = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}

router = APIRouter(prefix="/api", tags=["Article"])


@router.get("/articles", response_model=CreateResponse[List[ArticlesRead]])
async def get_article_items(
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    articles = await get_articles(session)
    return CreateResponse(
        status="success",
        message="ok",
        detail=[ArticlesRead.model_validate(article) for article in articles],
    )


@router.get("/articles/{slug}", response_model=CreateResponse[ArticleRead])
async def get_article_item(
    slug: str,
    user: UserModel = Depends(role_required(["guest"])),
    session: AsyncSession = Depends(get_async_session),
):
    article = await get_article_by_slug(session, slug)

    return CreateResponse(
        status="success",
        message="ok",
        detail=ArticlesRead.model_validate(article),
    )


@router.post("/articles", response_model=CreateResponse[ArticleRead])
async def create_new_article_item(
    cover_file: UploadFile,
    article: ArticleBase = Depends(parse_article_form),
    user: UserModel = Depends(role_required(["admin"])),
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
        settings.S3_ARTICLE_MEDIA_BUCKET_NAME,
    )

    cover_s3_url = s3_client.object_url(cover_key, "article-media")

    article.slug = generate_slug(article.title)
    article.cover_s3_url = cover_s3_url

    article = await create_new_article(session, article)

    return CreateResponse(
        status="succes", message="ok", detail=ArticleRead.model_validate(article)
    )


@router.patch("/articles/{article_id}", response_model=CreateResponse[ArticleRead])
async def update_article_item(
    article_id: int,
    update_data: ArticleUpdate,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    article_data = await get_article_by_id(session, article_id)

    updated_article_data = await update_article(session, article_data, update_data)

    return CreateResponse(
        status="succes",
        message="ok",
        detail=ArticleRead.model_validate(updated_article_data),
    )


@router.delete("/articles/{article_id}", status_code=204)
async def delete_article_item(
    article_id: int,
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    await delete_article_by_id(session, article_id)
