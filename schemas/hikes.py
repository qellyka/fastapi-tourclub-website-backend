from datetime import date
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class HikeBase(BaseModel):
    name: str = Field(..., description="Название похода")
    complexity: str = Field(..., description="Сложность маршрута")
    route: str = Field(..., description="Маршрут похода")
    # geojson_data: dict[str, Any] = Field(
    #     ..., description="Данные маршрута в формате GeoJSON"
    # )
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


class HikesRead(HikeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class HikeRead(HikeBase):
    geojson_data: dict[str, Any] = Field(
        ..., description="Данные маршрута в формате GeoJSON"
    )
    id: int
    model_config = ConfigDict(from_attributes=True)
