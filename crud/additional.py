from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import HikeModel, PassModel, hike_pass_association
from sqlalchemy import select, or_, insert


async def create_new_hike_pass_link(
    session: AsyncSession, hike: HikeModel, pas: PassModel
):
    stmt = insert(hike_pass_association).values(hike_id=hike.id, pass_id=pas.id)
    await session.execute(stmt)
    await session.commit()


async def get_pass_hikes(session: AsyncSession, pass_id: int):
    stmt = (
        select(PassModel)
        .options(selectinload(PassModel.hikes))  # заранее подтягиваем связанные походы
        .where(PassModel.id == pass_id)
    )
    pas = await session.scalar(stmt)
    return pas.hikes if pas else []
