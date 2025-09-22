from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import HikeModel, HikeParticipantModel, UserModel, ClubParticipantModel


async def create_hike_participant(
    session: AsyncSession, hike_id: int, user_id: int, role: str
):
    participant = HikeParticipantModel(
        user_id=user_id,
        hike_id=hike_id,
        role=role,
    )
    session.add(participant)
    await session.commit()
    await session.refresh(participant)
    return participant


async def get_hike_participants(session: AsyncSession, hike_id: int):
    stmt = (
        select(HikeModel)
        .options(
            selectinload(HikeModel.participants).selectinload(HikeParticipantModel.user)
        )
        .where(HikeModel.id == hike_id)
    )
    hike = await session.scalar(stmt)
    return hike.participants if hike else []


async def get_club_participants(session: AsyncSession):
    stmt = select(ClubParticipantModel).options(selectinload(ClubParticipantModel.user))
    result = await session.scalars(stmt)
    participants = result.all()
    return participants


async def create_club_participant(
    session: AsyncSession,
    user_id: int,
    description: str,
    avatar: str,
):
    participant = ClubParticipantModel(
        user_id=user_id,
        description=description,
        avatar_club=avatar,
    )
    session.add(participant)
    await session.commit()
    await session.refresh(participant)
    return participant
