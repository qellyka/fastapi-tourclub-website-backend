from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class PassBase(BaseModel):
    name: str = Field(..., description="Название перевала")
    region: str = Field(..., description="Регион перевала")
    complexity: str = Field(..., description="Сложность прохождения перевала")
    description: str = Field(..., description="Описание перевала")
    photos: Optional[List[str]] = Field(
        ..., description="Ссылка на архив с фотографиями"
    )
    height: int = Field(..., description="Высота перевала")


class PassRead(PassBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
