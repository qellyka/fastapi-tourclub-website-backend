from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from models import (
    UserModel,
    HikeModel,
    ApplicationModel,
    ArticleModel,
    NewsModel,
    PassModel,
)
from schemas.statistics import StatisticsDetail


async def get_admin_statistics_data(session: AsyncSession) -> StatisticsDetail:
    """Формирует статистику для админ-панели"""

    # === USERS ===
    total_users = await session.scalar(select(func.count()).select_from(UserModel)) or 0

    date_30_days_ago = datetime.utcnow() - timedelta(days=30)

    # новых пользователей за 30 дней
    new_users_last_30_days = (
        await session.scalar(
            select(func.count())
            .select_from(UserModel)
            .where(UserModel.created_at >= date_30_days_ago)
        )
    ) or 0

    # === HIKES ===
    total_hikes = await session.scalar(select(func.count()).select_from(HikeModel)) or 0

    hikes_by_status_query = await session.execute(
        select(HikeModel.status, func.count()).group_by(HikeModel.status)
    )
    hikes_by_status = {
        status.value: count for status, count in hikes_by_status_query.all()
    }

    # === APPLICATIONS ===
    total_applications = (
        await session.scalar(select(func.count()).select_from(ApplicationModel)) or 0
    )

    applications_by_status_query = await session.execute(
        select(ApplicationModel.status, func.count()).group_by(ApplicationModel.status)
    )
    applications_by_status = {
        status.value: count for status, count in applications_by_status_query.all()
    }

    # === ARTICLES ===
    total_articles = (
        await session.scalar(select(func.count()).select_from(ArticleModel)) or 0
    )

    # === NEWS ===
    total_news = await session.scalar(select(func.count()).select_from(NewsModel)) or 0

    # === PASSES ===
    total_passes = (
        await session.scalar(select(func.count()).select_from(PassModel)) or 0
    )

    # === RETURN RESULT ===
    return StatisticsDetail(
        total_users=total_users,
        new_users_last_30_days=new_users_last_30_days,
        total_hikes=total_hikes,
        hikes_by_status=hikes_by_status,
        total_applications=total_applications,
        applications_by_status=applications_by_status,
        total_articles=total_articles,
        total_news=total_news,
        total_passes=total_passes,
    )
