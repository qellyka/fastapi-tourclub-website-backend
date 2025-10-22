from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from core.utils import role_required
from crud.users import get_user_by_id
from db import get_async_session
from schemas import (
    ApplicationCreate,
    ApplicationOut,
    ApplicationAdminListItem,
    ApplicationUpdateAdmin,
    CreateResponse,
)
from schemas import UserRead
from crud.application import (
    create_application,
    get_user_application,
    list_applications,
    update_application_status,
    get_application,
)
from services.email import send_applicant_email

router = APIRouter(prefix="/api", tags=["School Applications"])


@router.post(
    "/school/applications",
    response_model=CreateResponse[ApplicationOut],
    status_code=status.HTTP_201_CREATED,
)
async def post_application(
    payload: ApplicationCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(role_required(["guest"])),
):
    app_obj = await create_application(session, user.id, payload)
    if app_obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть активная или одобренная заявка",
        )
    return CreateResponse(
        status="success",
        message="Заявка успешно создана",
        detail=ApplicationOut.model_validate(app_obj),
    )


@router.get(
    "/school/applications/me", response_model=CreateResponse[Optional[ApplicationOut]]
)
async def get_my_application(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(role_required(["guest"])),
):
    app_obj = await get_user_application(session, user.id)
    return CreateResponse(
        status="success",
        message="Данные заявки пользователя",
        detail=ApplicationOut.model_validate(app_obj) if app_obj else None,
    )


@router.get(
    "/admin/school/applications",
    response_model=CreateResponse[List[ApplicationAdminListItem]],
)
async def admin_list(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(role_required(["admin"])),
):
    apps = await list_applications(session, status=status, page=page, limit=limit)
    out = []
    for it in apps:
        out.append(
            ApplicationAdminListItem.model_validate(
                {
                    "id": it.id,
                    "user": UserRead.model_validate(it.user),
                    "status": it.status,
                    "created_at": it.created_at,
                }
            )
        )
    return CreateResponse(status="success", message="Список заявок", detail=out)


@router.patch(
    "/admin/school/applications/{id}", response_model=CreateResponse[ApplicationOut]
)
async def admin_update(
    id: int,
    payload: ApplicationUpdateAdmin,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(role_required(["admin"])),
):
    app_obj = await update_application_status(session, id, payload)
    if app_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found"
        )
    user_data = await get_user_by_id(session, app_obj.user_id)
    await send_applicant_email(
        user.email, f"{user_data.first_name} {user_data.last_name}"
    )

    return CreateResponse(
        status="success",
        message="Статус заявки обновлён",
        detail=ApplicationOut.model_validate(app_obj),
    )


@router.get(
    "/admin/school/applications/{id}",
    response_model=CreateResponse[ApplicationOut],
)
async def get_application_by_id(
    application_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(role_required(["admin"])),
):
    application = await get_application(session, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return CreateResponse(
        status="success",
        message="Заявка найдена",
        detail=ApplicationOut.model_validate(application),
    )
