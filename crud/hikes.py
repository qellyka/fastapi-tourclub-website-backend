from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import HikeModel
from sqlalchemy import select, or_

from schemas import HikeBase


async def get_all_hikes(session: AsyncSession):
    result = await session.scalars(select(HikeModel))
    return result.all()


async def get_hike_by_id(session: AsyncSession, id: int):
    result = await session.scalar(select(HikeModel).where(HikeModel.id == id))
    return result


async def create_new_hike(session: AsyncSession, hike: HikeBase, geojson_data: dict):
    new_hike = HikeModel(
        name=hike.name,
        complexity=hike.complexity,
        route=hike.route,
        geojson_data=geojson_data,
        start_date=hike.start_date,
        end_date=hike.end_date,
        region=hike.region,
        description=hike.description,
        photos_archive=hike.photos_archive,
        report=hike.report,
    )
    session.add(new_hike)
    await session.commit()
    await session.refresh(new_hike)
    return new_hike
