from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import PassModel
from sqlalchemy import select, or_

from schemas import PassBase


async def get_all_passes(session: AsyncSession):
    result = await session.scalars(select(PassModel))
    return result.all()


async def get_pass_by_id(session: AsyncSession, id: int):
    result = await session.scalar(select(PassModel).where(PassModel.id == id))
    return result


async def create_new_pass(session: AsyncSession, pass_stmt: PassBase):
    new_pass = PassModel(
        name=pass_stmt.name,
        region=pass_stmt.region,
        complexity=pass_stmt.complexity,
        height=pass_stmt.height,
        description=pass_stmt.description,
        photos=pass_stmt.photos,
    )
    session.add(new_pass)
    await session.commit()
    await session.refresh(new_pass)
    return new_pass
