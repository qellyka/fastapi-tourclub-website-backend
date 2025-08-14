from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    return _create_token(
        {"sub": sub, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES),
    )


def create_refresh_token(sub: str) -> str:
    return _create_token(
        {"sub": sub, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRES_DAYS),
    )


def create_email_verification_token(sub: str) -> str:
    return _create_token(
        {"sub": sub, "type": "verify"},
        timedelta(hours=settings.VERIFY_TOKEN_EXPIRES_HOURS),
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
