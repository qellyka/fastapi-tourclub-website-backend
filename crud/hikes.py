from typing import Optional

from fastapi import HTTPException
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
        slug=hike.slug,
        complexity=hike.complexity,
        route=hike.route,
        geojson_data=geojson_data,
        start_date=hike.start_date,
        end_date=hike.end_date,
        region=hike.region,
        description=hike.description,
        photos_archive=hike.photos_archive,
        report_s3_key=hike.report_s3_key,
        route_s3_key=hike.route_s3_key,
    )
    session.add(new_hike)
    await session.commit()
    await session.refresh(new_hike)
    return new_hike


async def delete_hike_by_id(session: AsyncSession, hike_id: int):
    user = await session.scalar(select(HikeModel).where(HikeModel.id == hike_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return user
