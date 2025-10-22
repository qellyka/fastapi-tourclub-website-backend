from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, computed_field, ConfigDict


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Латиница, цифры, _ и -",
    )
    email: EmailStr
    avatar: str | None = Field(
        None,
        description="Ссылка на аватар пользователя",
    )
    roles: List[str] | None = Field(
        None,
        description="Роли пользователя.",
    )
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Имя без цифр и спецсимволов",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Фамилия без цифр и спецсимволов",
    )
    middle_name: str | None = Field(
        None,
        min_length=2,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Отчество без цифр и спецсимволов",
    )
    description: str | None = Field(
        None,
        max_length=200,
        description="Информация о пользователе",
    )
    phone_number: str | None = Field(None, description="Телефон пользователя")

    @computed_field(return_type=str)
    @property
    def full_name(self) -> str:
        parts = [
            self.last_name.title(),
            self.first_name.title(),
            self.middle_name.title() if self.middle_name else "",
        ]
        return " ".join(filter(None, parts))


class UserUpdate(BaseModel):
    first_name: str | None = Field(
        None,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Имя без цифр и спецсимволов",
    )
    last_name: str | None = Field(
        None,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Фамилия без цифр и спецсимволов",
    )
    middle_name: str | None = Field(
        None,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Отчество без цифр и спецсимволов",
    )
    description: str | None = Field(
        None,
        max_length=200,
        description="Информация о пользователе",
    )
    phone_number: str | None = Field(None, description="Телефон пользователя")


class UserAdminUpdate(BaseModel):
    first_name: str | None = Field(
        None,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Имя без цифр и спецсимволов",
    )
    last_name: str | None = Field(
        None,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Фамилия без цифр и спецсимволов",
    )
    middle_name: str | None = Field(
        None,
        max_length=64,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ-]+$",
        description="Отчество без цифр и спецсимволов",
    )
    description: str | None = Field(
        None,
        max_length=200,
        description="Информация о пользователе",
    )
    phone_number: str | None = Field(None, description="Телефон пользователя")
    roles: List[str] | None = Field(
        None,
        description="Роли пользователя.",
    )
    email: EmailStr | None = Field(None, description="Почта пользователя")


class RegisterUser(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Пароль от 8 до 128 символов",
    )


class UserRead(UserBase):
    id: int
    is_activated: bool
    is_banned: bool
    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    username: str
    password: str


class UserHikeParticipant(UserBase):
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserClubParticipant(UserBase):
    description: str
    avatar_club: str

    model_config = ConfigDict(from_attributes=True)


class UserHikesRead(BaseModel):
    hike_id: int
    role: str


class UserHikeParticipantRead(BaseModel):
    id: int
    user_id: int
    hike_id: int
    role: str
    hike_name: str

    model_config = ConfigDict(from_attributes=True)
