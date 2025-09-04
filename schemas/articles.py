from pydantic import BaseModel, Field, ConfigDict


class ArticleBase(BaseModel):
    title: str = Field(..., description="Заголовок статьи")
    slug: str | None = Field(
        ..., description="Уникальный идентификатор статьи для URL."
    )
    content_json: str = Field(
        ..., description="Контент статьи из Tiptap в формате JSON"
    )
    content_html: str = Field(
        ..., description="Контент статьи из Tiptap в формате HTML"
    )
    cover_s3_key: str | None = Field(..., description="Обложка для статьи")
    author: str = Field(..., description="Автор статьи")


class ArticleUpdate(BaseModel):
    title: str | None = Field(..., description="Заголовок статьи")
    slug: str | None = Field(
        ..., description="Уникальный идентификатор статьи для URL."
    )
    content_json: str | None = Field(
        ..., description="Контент статьи из Tiptap в формате JSON"
    )
    content_html: str | None = Field(
        ..., description="Контент статьи из Tiptap в формате HTML"
    )
    cover_s3_key: str | None = Field(..., description="Обложка для статьи")
    author: str | None = Field(..., description="Автор статьи")


class ArticlesRead:
    title: str = Field(..., description="Заголовок статьи")
    slug: str | None = Field(
        ..., description="Уникальный идентификатор статьи для URL."
    )
    content_json: str = Field(
        ..., description="Контент статьи из Tiptap в формате JSON"
    )
    content_html: str = Field(
        ..., description="Контент статьи из Tiptap в формате HTML"
    )
    cover_s3_url: str | None = Field(..., description="Обложка для статьи")
    author: str = Field(..., description="Автор статьи")

    model_config = ConfigDict(from_attributes=True)


class ArticleRead(ArticleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
