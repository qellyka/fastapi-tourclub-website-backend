from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.security import decode_token
from crud.users import get_user_by_email_or_username
from db.session import get_async_session


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token"
        )
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
        user = await get_user_by_email_or_username(session, username, None)
        if not user or not user.is_activated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )


def role_required(roles: List[str]):
    async def checker(user=Depends(get_current_user)):
        if not set(roles).intersection(set(user.roles or [])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user

    return checker
