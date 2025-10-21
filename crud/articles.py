from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import generate_slug
from enums import ItemStatus
from models import ArticleModel
from sqlalchemy import select

from schemas import ArticleBase, ArticleUpdate


async def create_new_article(session: AsyncSession, article: ArticleBase, user_id: int):
    new_article = ArticleModel(
        title=article.title,
        slug=article.slug,
        author=article.author,
        cover_s3_url=article.cover_s3_url,
        created_by=user_id,
        updated_by=user_id,
    )

    session.add(new_article)
    await session.commit()
    await session.refresh(new_article)
    return new_article


async def get_article_by_id(session: AsyncSession, article_id: int):
    result = await session.scalar(
        select(ArticleModel).where(ArticleModel.id == article_id)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return result


async def get_article_by_slug(session: AsyncSession, slug: str):
    result = await session.scalar(select(ArticleModel).where(ArticleModel.slug == slug))
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return result


async def get_articles(session: AsyncSession, status: ItemStatus):
    if status:
        status = ItemStatus(status.upper())
        result = await session.scalars(
            select(ArticleModel).where(ArticleModel.status == status)
        )
    else:
        result = await session.scalars(select(ArticleModel))
    if not result:
        raise HTTPException(status_code=404, detail="Articles not found")
    return result.all()


async def update_article(
    session: AsyncSession,
    article_data: ArticleModel,
    update_data: ArticleUpdate,
    user_id: int,
):

    update_data = update_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(article_data, field, value)

    if "title" in update_data:
        article_data.slug = generate_slug(article_data.title)

    article_data.updated_by = user_id

    await session.commit()
    await session.refresh(article_data)
    return article_data


async def delete_article_by_id(session: AsyncSession, article_id: int):
    article_data = await session.scalar(
        select(ArticleModel).where(ArticleModel.id == article_id)
    )

    if not article_data:
        raise HTTPException(status_code=404, detail="Article not found")

    await session.delete(article_data)
    await session.commit()
    return article_data
