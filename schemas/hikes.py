from datetime import date
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class HikeBase(BaseModel):
    name: str = Field(..., description="Название похода")
    slug: str | None = Field(
        None, description="Уникальный идентификатор статьи для URL."
    )
    complexity: str = Field(..., description="Сложность маршрута")
    route: str = Field(..., description="Маршрут похода")
    start_date: date = Field(..., description="Дата начала похода")
    end_date: date = Field(..., description="Дата окончания похода")
    region: str = Field(..., description="Регион проведения похода")
    description: str = Field(..., description="Описание похода")

    photos_archive: str = Field(..., description="Ссылка на архив с фотографиями")
    report_s3_key: str | None = Field(
        None, description="Ключ для доступа к отчету в S3 хранилище"
    )
    route_s3_key: str | None = Field(
        None, description="Ключ для доступа к маршруту в S3 хранилище"
    )


class HikeUpdate(BaseModel):
    name: str | None = Field(None, description="Название похода")
    complexity: str | None = Field(None, description="Сложность маршрута")
    route: str | None = Field(None, description="Маршрут похода")
    start_date: date | None = Field(None, description="Дата начала похода")
    end_date: date | None = Field(None, description="Дата окончания похода")
    region: str | None = Field(None, description="Регион проведения похода")
    description: str | None = Field(None, description="Описание похода")
    photos_archive: str | None = Field(
        None, description="Ссылка на архив с фотографиями"
    )


class HikesRead(BaseModel):
    id: int
    slug: str = Field(..., description="Уникальный идентификатор статьи для URL.")
    name: str = Field(..., description="Название похода")
    start_date: date = Field(..., description="Дата начала похода")
    end_date: date = Field(..., description="Дата окончания похода")
    complexity: str = Field(..., description="Сложность маршрута")
    route: str = Field(..., description="Маршрут похода")
    region: str = Field(..., description="Регион проведения похода")

    model_config = ConfigDict(from_attributes=True)


class HikeRead(HikeBase):
    geojson_data: dict[str, Any] = Field(
        ..., description="Данные маршрута в формате GeoJSON"
    )
    id: int
    model_config = ConfigDict(from_attributes=True)
