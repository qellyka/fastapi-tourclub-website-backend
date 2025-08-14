from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import db_helper


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_helper.session_factory() as session:
        yield session
