from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import role_required
from db import get_async_session
from models import UserModel
from crud.statistics import get_admin_statistics_data
from schemas import CreateResponse
from schemas.statistics import StatisticsDetail

router = APIRouter(prefix="/api", tags=["Admin"])


@router.get("/statistics", response_model=CreateResponse[StatisticsDetail])
async def get_admin_statistics(
    user: UserModel = Depends(role_required(["admin"])),
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает статистику для админ-панели"""
    data = await get_admin_statistics_data(session)

    return CreateResponse(
        status="success",
        message="Statistics retrieved successfully",
        detail=data,
    )
