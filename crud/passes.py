from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from enums import ItemStatus
from models import PassModel
from sqlalchemy import select, or_

from schemas import PassBase, PassUpdate


async def get_all_passes(session: AsyncSession, status: ItemStatus):
    if status:
        status = ItemStatus(status.upper())
        result = await session.scalars(
            select(PassModel).where(PassModel.status == status)
        )
    else:
        result = await session.scalars(select(PassModel))
    return result.all()


async def get_pass_by_id(session: AsyncSession, id: int):
    result = await session.scalar(select(PassModel).where(PassModel.id == id))
    return result


async def get_pass_by_slug(session: AsyncSession, slug: str):
    result = await session.scalar(select(PassModel).where(PassModel.slug == slug))
    return result


async def create_new_pass(session: AsyncSession, pass_stmt: PassBase, user_id: int):
    new_pass = PassModel(
        name=pass_stmt.name,
        slug=pass_stmt.slug,
        region=pass_stmt.region,
        complexity=pass_stmt.complexity,
        height=pass_stmt.height,
        description=pass_stmt.description,
        photos=pass_stmt.photos,
        longitude=pass_stmt.longitude,
        latitude=pass_stmt.latitude,
        created_by=user_id,
        updated_by=user_id,
    )
    session.add(new_pass)
    await session.commit()
    await session.refresh(new_pass)
    return new_pass


async def update_pass(
    session: AsyncSession, db_pass: PassModel, data: PassUpdate, user_id: int
) -> PassModel:
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pass, field, value)

    db_pass.updated_by = user_id

    await session.commit()
    await session.refresh(db_pass)
    return db_pass
