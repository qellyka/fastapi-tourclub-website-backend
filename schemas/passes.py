from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class PassBase(BaseModel):
    name: str = Field(..., description="Название перевала")
    slug: str | None = Field(
        None, description="Уникальный идентификатор статьи для URL."
    )
    region: str = Field(..., description="Регион перевала")
    complexity: str = Field(..., description="Сложность прохождения перевала")
    longitude: float = Field(..., description="Долгота перевала")
    latitude: float = Field(..., description="Широта перевала")
    description: str = Field(..., description="Описание перевала")
    photos: Optional[List[str]] = Field(
        ..., description="Ссылка на архив с фотографиями"
    )
    height: int = Field(..., description="Высота перевала")


class PassRead(PassBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PassUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    complexity: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None
    height: Optional[int] = None
