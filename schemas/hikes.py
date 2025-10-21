from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict


class HikeBase(BaseModel):
    name: str = Field(..., description="Название похода")
    slug: Optional[str] = Field(None, description="Уникальный идентификатор для URL")
    tourism_type: str = Field(..., description="Вид туризма (горный, водный и т.д.)")
    complexity: str = Field(
        ..., description="Категория сложности маршрута (например, 2 к.с.)"
    )
    region: Optional[str] = Field(None, description="Регион проведения похода")
    route: str = Field(..., description="Нитка маршрута")
    start_date: date = Field(..., description="Дата начала похода")
    end_date: date = Field(..., description="Дата окончания похода")
    description: Optional[str] = Field(None, description="Описание похода")

    participants_count: int = Field(..., description="Количество участников")
    duration_days: Optional[int] = Field(
        None, description="Продолжительность похода в днях"
    )
    distance_km: Optional[float] = Field(
        None, description="Протяженность маршрута в километрах"
    )
    difficulty_distribution: Optional[dict[str, int]] = Field(
        None,
        description="Распределение препятствий по категориям (например: 1Б — 5, 1А — 1)",
    )
    leader_id: int = Field(..., description="ID руководителя похода (user_id)")

    photos_archive: Optional[str] = Field(
        None, description="Ссылка на архив с фотографиями"
    )
    report_s3_key: Optional[str] = Field(
        None, description="Ключ для доступа к отчету в S3"
    )
    route_s3_key: Optional[str] = Field(
        None, description="Ключ для доступа к маршруту в S3"
    )


# Схема для обновления
class HikeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название похода")
    tourism_type: Optional[str] = Field(None, description="Вид туризма")
    complexity: Optional[str] = Field(None, description="Категория сложности маршрута")
    region: Optional[str] = Field(None, description="Регион проведения похода")
    route: Optional[str] = Field(None, description="Нитка маршрута")
    start_date: Optional[date] = Field(None, description="Дата начала похода")
    end_date: Optional[date] = Field(None, description="Дата окончания похода")
    description: Optional[str] = Field(None, description="Описание похода")

    participants_count: Optional[int] = Field(None, description="Количество участников")
    duration_days: Optional[int] = Field(
        None, description="Продолжительность похода в днях"
    )
    distance_km: Optional[float] = Field(
        None, description="Протяженность маршрута в километрах"
    )
    difficulty_distribution: Optional[dict[str, int]] = Field(
        None,
        description="Распределение препятствий по категориям сложности, например {'1Б': 5, '1А': 1}",
    )
    leader_id: Optional[int] = Field(None, description="ID руководителя похода")

    photos_archive: Optional[str] = Field(
        None, description="Ссылка на архив с фотографиями"
    )
    report_s3_key: Optional[str] = Field(
        None, description="Ключ для доступа к отчету в S3"
    )
    route_s3_key: Optional[str] = Field(
        None, description="Ключ для доступа к маршруту в S3"
    )
    status: Optional[str] = Field(None, description="Статус публикации")


class HikesRead(BaseModel):
    id: int
    slug: str
    name: str
    start_date: date
    end_date: date
    tourism_type: str
    complexity: str
    region: Optional[str]
    leader_fullname: Optional[str]
    status: str

    model_config = ConfigDict(from_attributes=True)


class HikeRead(HikeBase):
    id: int
    geojson_data: Optional[dict[str, Any]] = Field(
        None, description="Данные маршрута в формате GeoJSON"
    )
    status: Optional[str] = Field(None, description="Статус публикации")
    created_by: int
    updated_by: Optional[int]
    leader_fullname: Optional[str]
    leader_email: Optional[str]

    model_config = ConfigDict(from_attributes=True)
