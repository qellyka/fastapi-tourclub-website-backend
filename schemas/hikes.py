from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field


class HikeBase(BaseModel):
    name: str = Field(..., description="Название похода")
    complexity: str = Field(..., description="Сложность маршрута")
    route: str = Field(..., description="Маршрут похода")
    geojson_data: dict[str, Any] = Field(
        ..., description="Данные маршрута в формате GeoJSON"
    )
    start_date: datetime = Field(..., description="Дата начала похода")
    end_date: datetime = Field(..., description="Дата окончания похода")
    region: str = Field(..., description="Регион проведения похода")
    description: str = Field(..., description="Описание похода")
    photos_archive: str = Field(..., description="Ссылка на архив с фотографиями")
