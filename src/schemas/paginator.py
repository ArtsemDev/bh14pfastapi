from typing import Optional, Any, Type

from pydantic import BaseModel, PositiveInt, HttpUrl, Field, AnyUrl

__all__ = ["Paginator"]


class BasePaginator(BaseModel):
    count: PositiveInt
    next: Optional[AnyUrl] = Field(default=None)
    prev: Optional[AnyUrl] = Field(default=None)
    result: list[Any]


class Paginator(object):

    def __class_getitem__(cls, schema: Type[BaseModel]) -> Type[BasePaginator]:
        return type(  # noqa
            f"{schema.__name__}Paginator",
            (BasePaginator, ),
            {
                "__annotations__": {
                    "result": list[schema]
                }
            }
        )
