from typing import Union, List, Optional, Any, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class CreateResponse(BaseModel, Generic[T]):
    status: str = Field(..., description="Статус операции (success, error)")
    message: str = Field(..., description="Краткое описание результата")
    detail: Optional[T] = Field(
        None,
        description="Дополнительные данные (например, токен, пользователь, список объектов и т.д.)",
    )
