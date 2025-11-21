from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    user_router,
    hike_router,
    pass_router,
    additional_router,
    hike_participant_router,
    club_participant_router,
    auth_router,
    article_router,
    news_router,
    application_router,
    file_router,
    statistics_router,
)
from core.config import settings
from db import db_helper
from models import Base
from models import (
    UserModel,
    HikeParticipantModel,
    ClubParticipantModel,
    HikeModel,
    PassModel,
    TokenModel,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # await db_helper.create_random_user()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(hike_router)
app.include_router(pass_router)
app.include_router(application_router)
app.include_router(article_router)
app.include_router(news_router)
app.include_router(hike_participant_router)
app.include_router(club_participant_router)
app.include_router(additional_router)
app.include_router(file_router)
app.include_router(statistics_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.88:3000",
        "https://tkirbis30.ru",
        "https://dev.tkirbis30.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=settings.HOST, port=settings.PORT)
