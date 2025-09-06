from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import generate_slug
from models import NewsModel
from sqlalchemy import select

from schemas import NewsBase, NewsUpdate


async def create_new_news(session: AsyncSession, news: NewsBase):
    new_news = NewsModel(
        title=news.title,
        slug=news.slug,
        summary=news.summary,
        cover_s3_url=news.cover_s3_url,
    )

    session.add(new_news)
    await session.commit()
    await session.refresh(new_news)
    return new_news


async def get_news_by_id(session: AsyncSession, news_id: int):
    result = await session.scalar(select(NewsModel).where(NewsModel.id == news_id))
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result


async def get_news_by_slug(session: AsyncSession, slug: str):
    result = await session.scalar(select(NewsModel).where(NewsModel.slug == slug))
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result


async def get_news(session: AsyncSession):
    result = await session.scalars(select(NewsModel))
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result.all()


async def update_news(
    session: AsyncSession, news_data: NewsModel, update_data: NewsUpdate
):

    update_data = update_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(news_data, field, value)

    if "title" in update_data:
        news_data.slug = generate_slug(news_data.title)

    await session.commit()
    await session.refresh(news_data)
    return news_data


async def delete_news_by_id(session: AsyncSession, news_id: int):
    news_data = await session.scalar(select(NewsModel).where(NewsModel.id == news_id))

    if not news_data:
        raise HTTPException(status_code=404, detail="News not found")

    await session.delete(news_data)
    await session.commit()
    return news_data
