import random
import string
from passlib.hash import bcrypt
from models import UserModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings


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
            username = "user_" + "".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )
            password_raw = "".join(
                random.choices(string.ascii_letters + string.digits, k=12)
            )
            hashed_password = bcrypt.hash(password_raw)

            user = UserModel(
                username=username,
                email=f"admin@example.com",
                password=hashed_password,
                first_name="admin",
                last_name="admin",
                middle_name=None,
                is_activated=True,
                roles=["guest", "admin"],
            )

            session.add(user)
            await session.commit()
            print("=======================ADMIN=======================")
            print(f"############## USERNAME: {username} ############")
            print(f"############## PASSWORD: {password_raw}  ############")
            print("===================================================")


db_helper = DatabaseHelper(
    url=settings.DATABASE_URL,
    echo=settings.DEBUG,
)
