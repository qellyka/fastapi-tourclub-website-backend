from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models import UserModel, HikeParticipantModel
from sqlalchemy import select, or_

from schemas import RegisterUser, UserUpdate
from schemas.users import UserAdminUpdate


async def get_user_by_email_or_username(
    session: AsyncSession,
    username: str,
    email: Optional[str],
) -> Optional[UserModel]:
    db_user = await session.scalar(
        select(UserModel).where(
            or_(UserModel.username == username, UserModel.email == email)
        )
    )
    return db_user


async def get_users(session: AsyncSession):
    result = await session.scalars(select(UserModel))
    return result.all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[UserModel]:
    db_user = await session.scalar(
        select(UserModel)
        .where((UserModel.id == user_id))
        .options(selectinload(UserModel.hike_participations))
    )
    return db_user


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Optional[UserModel]:
    db_user = await session.scalar(
        select(UserModel)
        .where((UserModel.username == username))
        .options(selectinload(UserModel.hike_participations))
    )
    return db_user


async def create_new_user(
    session: AsyncSession,
    user: RegisterUser,
    hashed_password: str,
) -> UserModel:
    new_user = UserModel(
        username=user.username,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name.title(),
        last_name=user.last_name.title(),
        middle_name=user.middle_name.title() if user.middle_name else None,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def activate_user(session: AsyncSession, username: str):
    user = await session.scalar(select(UserModel).where(UserModel.username == username))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_activated = True
    await session.commit()
    return user


async def delete_user_by_id(session: AsyncSession, user_id: int):
    user = await session.scalar(select(UserModel).where(UserModel.id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return user


async def update_user_avatar(session: AsyncSession, file_url: str, user_id: int):
    user = await session.scalar(select(UserModel).where(UserModel.id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.avatar = file_url

    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession, user_data: UserModel, update_data: UserUpdate
):

    update_data = update_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user_data, field, value)

    await session.commit()
    await session.refresh(user_data)
    return user_data


async def get_user_hike_participations(session: AsyncSession, user_id: int):
    result = await session.scalars(
        select(HikeParticipantModel)
        .options(joinedload(HikeParticipantModel.hike))
        .where(HikeParticipantModel.user_id == user_id)
    )
    return result.all()


async def ban_user_by_id(session: AsyncSession, user_id: int):
    user_data = await session.scalar(select(UserModel).where(UserModel.id == user_id))

    user_data.is_banned = True
    await session.commit()
    await session.refresh(user_data)
    return user_data


async def unban_user_by_id(session: AsyncSession, user_id: int):
    user_data = await session.scalar(select(UserModel).where(UserModel.id == user_id))

    user_data.is_banned = False
    await session.commit()
    await session.refresh(user_data)
    return user_data
