from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from sqlalchemy.orm import selectinload

from models import ApplicationModel, ApplicationStatus
from schemas import ApplicationCreate, ApplicationUpdateAdmin


async def create_application(
    session: AsyncSession, user_id: int, payload: ApplicationCreate
) -> Optional[ApplicationModel]:
    result = await session.execute(
        select(ApplicationModel).where(
            ApplicationModel.user_id == user_id,
            ApplicationModel.status.in_(
                [ApplicationStatus.pending, ApplicationStatus.approved]
            ),
        )
    )
    existing = result.scalars().first()
    if existing:
        return None

    new_app = ApplicationModel(
        user_id=user_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        middle_name=payload.middle_name,
        date_of_birth=payload.date_of_birth,
        email=payload.email,
        phone_number=payload.phone_number,
        vk_profile=payload.vk_profile,
        experience=payload.experience,
        previous_school=payload.previous_school,
        how_heard=payload.how_heard,
        question=payload.question,
        wishes=payload.wishes,
        consent=payload.consent,
        status=ApplicationStatus.pending,
    )
    session.add(new_app)
    await session.commit()
    await session.refresh(new_app)
    return new_app


async def get_user_application(
    session: AsyncSession, user_id: int
) -> Optional[ApplicationModel]:
    result = await session.execute(
        select(ApplicationModel).where(ApplicationModel.user_id == user_id)
    )
    return result.scalars().first()


async def get_application(
    session: AsyncSession, application_id: int
) -> Optional[ApplicationModel]:
    result = await session.execute(
        select(ApplicationModel)
        .where(ApplicationModel.id == application_id)
        .options(selectinload(ApplicationModel.user))
    )
    return result.scalars().first()


async def list_applications(
    session: AsyncSession, status: Optional[str] = None, page: int = 1, limit: int = 20
) -> List[ApplicationModel]:
    query = select(ApplicationModel)
    if status:
        query = query.where(ApplicationModel.status == status)
    query = query.offset((page - 1) * limit).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def update_application_status(
    session: AsyncSession, app_id: int, payload: ApplicationUpdateAdmin
) -> Optional[ApplicationModel]:
    result = await session.execute(
        select(ApplicationModel).where(ApplicationModel.id == app_id)
    )
    app = result.scalars().first()
    if not app:
        return None
    app.status = payload.status
    app.comment = payload.comment
    await session.commit()
    await session.refresh(app)
    return app
