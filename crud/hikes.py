from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.utils import generate_slug
from enums import ItemStatus
from models import HikeModel
from schemas import HikeBase, HikeUpdate


async def get_all_hikes(session: AsyncSession, status: ItemStatus):
    if status:
        status = ItemStatus(status.upper())
        result = await session.scalars(
            select(HikeModel)
            .where(HikeModel.status == status)
            .options(selectinload(HikeModel.leader))
        )
    else:
        result = await session.scalars(
            select(HikeModel).options(selectinload(HikeModel.leader))
        )
    return result.all()


async def get_hike_by_id(session: AsyncSession, id: int):
    return await session.scalar(
        select(HikeModel)
        .where(HikeModel.id == id)
        .options(selectinload(HikeModel.leader))
    )


async def get_hike_by_slug(session: AsyncSession, slug: str):
    return await session.scalar(
        select(HikeModel)
        .where(HikeModel.slug == slug)
        .options(selectinload(HikeModel.leader))
    )


async def create_new_hike(
    session: AsyncSession, hike: HikeBase, geojson_data: dict, user_id: int
):
    new_hike = HikeModel(
        name=hike.name,
        slug=hike.slug,
        tourism_type=hike.tourism_type,
        complexity=hike.complexity,
        difficulty_distribution=hike.difficulty_distribution,
        route=hike.route,
        geojson_data=geojson_data,
        start_date=hike.start_date,
        end_date=hike.end_date,
        region=hike.region,
        description=hike.description,
        participants_count=hike.participants_count,
        duration_days=hike.duration_days,
        distance_km=hike.distance_km,
        leader_id=hike.leader_id,
        photos_archive=hike.photos_archive,
        report_s3_key=hike.report_s3_key,
        route_s3_key=hike.route_s3_key,
        created_by=user_id,
        updated_by=user_id,
    )

    session.add(new_hike)
    await session.commit()
    await session.refresh(new_hike)
    return new_hike


async def delete_hike_by_id(session: AsyncSession, hike_id: int):
    hike = await session.scalar(select(HikeModel).where(HikeModel.id == hike_id))
    if not hike:
        raise HTTPException(status_code=404, detail="Hike not found")

    await session.delete(hike)
    await session.commit()
    return hike


async def update_hike(
    session: AsyncSession,
    hike_data: HikeModel,
    update_data: HikeUpdate,
    gpx_s3_filename: Optional[str],
    report_s3_filename: Optional[str],
    geojson_data: Optional[dict],
    user_id: int,
):
    update_dict = update_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(hike_data, field, value)

    if "name" in update_dict:
        hike_data.slug = generate_slug(hike_data.name)

    if gpx_s3_filename:
        hike_data.route_s3_key = gpx_s3_filename

    if report_s3_filename:
        hike_data.report_s3_key = report_s3_filename

    if geojson_data:
        hike_data.geojson_data = geojson_data

    hike_data.updated_by = user_id

    await session.commit()
    await session.refresh(hike_data)
    return hike_data
