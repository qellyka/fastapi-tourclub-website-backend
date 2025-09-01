from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.additional import create_new_hike_pass_link
from crud.hikes import get_hike_by_id
from crud.passes import get_pass_by_id
from db import get_async_session
from schemas import CreateResponse

router = APIRouter(prefix="/api/archive", tags=["Archive"])


@router.post("/link", response_model=CreateResponse)
async def link_hike_and_pass(
    hike_id: int, pass_id: int, session: AsyncSession = Depends(get_async_session)
):
    hike = await get_hike_by_id(session, hike_id)
    pas = await get_pass_by_id(session, pass_id)

    if not hike or not pas:
        raise HTTPException(status_code=404, detail="Hike or Pass not found")

    await create_new_hike_pass_link(session, hike, pas)

    return CreateResponse(
        status="success",
        message=f"Связь добавлена: Hike {hike.id} -> Pass {pas.id}",
        detail=None,
    )
