from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class NewsBase(BaseModel):
    title: str = Field(..., description="Заголовок новости")
    summary: str = Field(..., description="Краткое содержание новости")
    slug: Optional[str] = Field(
        None, description="Уникальный идентификатор новости для URL."
    )
    content_json: Optional[Dict[str, Any]] = Field(
        None, description="Контент новости из Tiptap в формате JSON"
    )
    content_html: Optional[str] = Field(
        None, description="Контент новости из Tiptap в формате HTML"
    )
    cover_s3_url: Optional[str] = Field(None, description="Обложка для новости")


class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Заголовок новости")
    summary: Optional[str] = Field(None, description="Краткое содержание новости")
    slug: Optional[str] = Field(
        None, description="Уникальный идентификатор новости для URL."
    )
    content_json: Optional[Dict[str, Any]] = Field(
        None, description="Контент новости из Tiptap в формате JSON"
    )
    content_html: Optional[str] = Field(
        None, description="Контент новости из Tiptap в формате HTML"
    )
    cover_s3_url: Optional[str] = Field(None, description="Обложка для новости")


class NewsReadList(BaseModel):
    id: int
    title: str
    summary: str
    slug: str
    cover_s3_url: str

    model_config = ConfigDict(from_attributes=True)


class NewsRead(NewsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
