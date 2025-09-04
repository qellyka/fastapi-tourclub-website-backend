from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel, ArticleModel
from sqlalchemy import select, or_

from schemas import ArticleBase


async def create_new_article(session: AsyncSession, article: ArticleBase):
    new_article = ArticleModel(
        title=article.title,
        slug=article.slug,
        content_json=article.content_json,
        content_html=article.content_html,
        author=article.author,
        cover_s3_url=article.cover_s3_url,
    )

    session.add(new_article)
    await session.commit()
    await session.refresh(new_article)
    return new_article
