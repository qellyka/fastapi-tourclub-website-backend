from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import user_router, hike_router, pass_router, additional_router
from core.config import settings
from db import db_helper
from models import Base
from models import (
    UserModel,
    HikeParticipant,
    ClubParticipant,
    HikeModel,
    PassModel,
    TokenModel,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(hike_router)
app.include_router(pass_router)
app.include_router(additional_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=settings.HOST, port=settings.PORT)
