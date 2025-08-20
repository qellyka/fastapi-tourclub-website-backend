from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel
from sqlalchemy import select, or_, delete

from models.tokens import TokenModel


async def save_token(
    session: AsyncSession,
    refresh_token: str,
    user_id: int,
):
    token_data = await session.scalar(
        select(TokenModel).where(TokenModel.user_id == user_id)
    )
    if token_data:
        token_data.token = refresh_token
        await session.commit()
        await session.refresh(token_data)
        return token_data
    else:
        new_token = TokenModel(
            token=refresh_token,
            user_id=user_id,
        )
        session.add(new_token)
        await session.commit()
        await session.refresh(new_token)
        return new_token


async def remove_token(
    token: str,
    session: AsyncSession,
):
    stmt = delete(TokenModel).where(TokenModel.token == token)
    await session.execute(stmt)
    await session.commit()


async def find_token(
    token: str,
    session: AsyncSession,
):
    token_data = await session.scalar(
        select(TokenModel).where(TokenModel.token == token)
    )
    return token_data
