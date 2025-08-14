from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- App settings ---
    DEBUG: bool = False

    # --- Database ---
    DATABASE_URL: str

    # --- JWT settings ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    VERIFY_TOKEN_EXPIRES_HOURS: int = 48

    # --- Email settings ---
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Экземпляр настроек
settings = Settings()
