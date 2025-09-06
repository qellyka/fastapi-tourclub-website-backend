from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- App settings ---
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRONTEND_URL: str = "http://127.0.0.1:3000"
    BACKEND_URL: str = f"http://127.0.0.1:{PORT}"

    # --- Database ---
    DATABASE_URL: str

    # --- JWT settings ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    VERIFY_TOKEN_EXPIRES_HOURS: int = 48
    COOKIE_SECURE: bool = True

    # --- Email settings ---
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    # --- S3 settings ---
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str
    S3_HIKE_MEDIA_BUCKET_NAME: str
    S3_USER_MEDIA_BUCKET_NAME: str
    S3_ARTICLE_MEDIA_BUCKET_NAME: str
    S3_NEWS_MEDIA_BUCKET_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Экземпляр настроек
settings = Settings()
