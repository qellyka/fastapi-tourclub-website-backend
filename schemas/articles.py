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


class ArticlesRead(BaseModel):
    id: int
    title: str
    slug: str
    cover_s3_url: str
    author: str
    model_config = ConfigDict(from_attributes=True)


class ArticleRead(ArticleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
