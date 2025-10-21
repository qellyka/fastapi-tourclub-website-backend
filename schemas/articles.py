from typing import Optional, Any, Dict

from pydantic import BaseModel, Field, ConfigDict


class ArticleBase(BaseModel):
    title: str = Field(..., description="Заголовок статьи")
    slug: Optional[str] = Field(
        None, description="Уникальный идентификатор статьи для URL."
    )
    content_json: Optional[Dict[str, Any]] = Field(
        None, description="Контент статьи из Tiptap в формате JSON"
    )
    content_html: Optional[str] = Field(
        None, description="Контент статьи из Tiptap в формате HTML"
    )
    cover_s3_url: Optional[str] = Field(None, description="Обложка для статьи")
    author: str = Field(..., description="Автор статьи")


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Заголовок статьи")
    slug: Optional[str] = Field(
        None, description="Уникальный идентификатор статьи для URL."
    )
    content_json: Optional[Dict[str, Any]] = Field(
        None, description="Контент статьи из Tiptap в формате JSON"
    )
    content_html: Optional[str] = Field(
        None, description="Контент статьи из Tiptap в формате HTML"
    )
    cover_s3_url: Optional[str] = Field(None, description="Обложка для статьи")
    author: Optional[str] = Field(None, description="Автор статьи")
    status: Optional[str] = Field(None)


class ArticlesRead(BaseModel):
    id: int
    title: str
    slug: str
    cover_s3_url: str
    author: str
    created_by: int
    updated_by: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class ArticleRead(ArticleBase):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
