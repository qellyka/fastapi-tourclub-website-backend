from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel
from sqlalchemy import select, or_

from schemas import RegisterUser


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
    db_user = await session.scalar(select(UserModel).where((UserModel.id == user_id)))
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
        return None
    user.is_activated = True
    await session.commit()
    return user
