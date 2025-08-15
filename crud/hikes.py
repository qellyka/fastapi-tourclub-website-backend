from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import HikeModel
from sqlalchemy import select, or_

from schemas import HikeBase


async def get_all_hikes(session: AsyncSession):
    result = await session.scalars(select(HikeModel))
    return result.all()


async def create_new_hike(session: AsyncSession, hike: HikeBase):
    new_hike = HikeModel(
        name=hike.name,
        complexity=hike.complexity,
        route=hike.route,
        # geojson_data=hike.geojson_data,
        start_date=hike.start_date,
        end_date=hike.end_date,
        region=hike.region,
        description=hike.description,
        photos_archive=hike.photos_archive,
    )
    session.add(new_hike)
    await session.commit()
    await session.refresh(new_hike)
    return new_hike
