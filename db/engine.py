import secrets
from passlib.hash import bcrypt

from models import UserModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from services.email import send_email


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def create_random_user(self):
        async with self.session_factory() as session:
            username = f"admin_{secrets.token_hex(4)}"
            password_raw = secrets.token_urlsafe(16)
            hashed_password = bcrypt.hash(password_raw)

            user = UserModel(
                username=username,
                email="admin@example.com",
                password=hashed_password,
                first_name="admin",
                last_name="admin",
                middle_name=None,
                is_activated=True,
                roles=["guest", "admin"],
            )
            session.add(user)
            await session.commit()

            await send_email(
                subject="Admin credentials created",
                recipients=[f"{settings.ADMIN_EMAIL}"],
                body=f"Username: {username}\nPassword: {password_raw}",
            )


db_helper = DatabaseHelper(
    url=settings.DATABASE_URL,
    echo=settings.DEBUG,
)
