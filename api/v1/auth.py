from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)

from core.config import settings
from core.security import (
    hash_password,
    create_email_verification_token,
    decode_token,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from core.utils import role_required, set_auth_cookies
from crud.tokens import save_token, remove_token, find_token
from crud.users import get_user_by_email_or_username, create_new_user, activate_user
from db import get_async_session
from models import UserModel
from schemas import RegisterUser, UserRead, LoginUser, CreateResponse
from services.email import send_verification_email

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", status_code=HTTP_201_CREATED, response_model=CreateResponse)
async def user_registration(
    user: RegisterUser,
    response: Response,
    session: AsyncSession = Depends(
        get_async_session,
    ),
):
    candidate = await get_user_by_email_or_username(session, user.username, user.email)
    if candidate:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User with this username or email already registered.",
        )

    hashed_password = hash_password(user.password)
    user = await create_new_user(session, user, hashed_password)

    verify_token = create_email_verification_token(user.username)
    await send_verification_email(
        user.email, f"{settings.BACKEND_URL}/api/auth/verify?token={verify_token}"
    )

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)
    await save_token(session, refresh_token, user.id)

    set_auth_cookies(response, access_token, refresh_token)

    detail = {
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "user": UserRead.model_validate(user),
    }

    return CreateResponse(
        status="success",
        message="ok",
        detail=detail,
    )


@router.post("/login", status_code=HTTP_200_OK, response_model=CreateResponse)
async def user_login(
    user: LoginUser,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    candidate = await get_user_by_email_or_username(session, user.username, None)
    if not candidate:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not verify_password(user.password, candidate.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(candidate.username)
    refresh_token = create_refresh_token(candidate.username)
    await save_token(session, refresh_token, candidate.id)

    set_auth_cookies(response, access_token, refresh_token)

    detail = {
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "user": UserRead.model_validate(candidate),
    }

    return CreateResponse(
        status="success",
        message="ok",
        detail=detail,
    )


@router.post("/logout", status_code=HTTP_200_OK, response_model=CreateResponse)
async def user_logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session),
):

    if not refresh_token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="user unauthorized"
        )

    await remove_token(refresh_token, session)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return CreateResponse(
        status="success",
        message="ok",
        detail=None,
    )


@router.get("/refresh", response_model=CreateResponse)
async def token_refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session),
):
    if not refresh_token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="user unauthorized"
        )
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    token_data = await find_token(refresh_token, session)
    if not token_data:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="user unauthorized"
        )

    access_token = create_access_token(payload["sub"])
    refresh_token = create_refresh_token(payload["sub"])
    db_user = await get_user_by_email_or_username(session, payload["sub"], None)
    await save_token(session, refresh_token, db_user.id)

    set_auth_cookies(response, access_token, refresh_token)

    detail = {
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "user": UserRead.model_validate(db_user),
    }

    return CreateResponse(
        status="success",
        message="ok",
        detail=detail,
    )


@router.get("/verify")
async def user_verify(token: str, session: AsyncSession = Depends(get_async_session)):
    token_payload = decode_token(token)
    if token_payload["type"] != "verify":
        raise HTTPException(status_code=400, detail="Invalid token type")

    user = await activate_user(session, token_payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return RedirectResponse(url="https://ya.ru")
