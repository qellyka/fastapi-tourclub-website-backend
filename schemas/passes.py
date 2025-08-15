from pydantic import BaseModel, Field


class PassBase(BaseModel):
    name: str = Field(..., description="Название перевала")
    region: str = Field(..., description="Регион перевала")
    complexity: str = Field(..., description="Сложность прохождения перевала")
    description: str = Field(..., description="Описание перевала")
    photos_archive: str = Field(..., description="Ссылка на архив с фотографиями")
    height: int = Field(..., description="Высота перевала")
