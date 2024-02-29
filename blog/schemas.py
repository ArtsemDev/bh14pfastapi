from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt

__all__ = [
    "TagCreateForm",
    "TagDetail",
    "TagEditForm",
    "TopicCreateForm",
    "TopicDetail",
    "TopicEditForm",
]


class TagCreateForm(BaseModel):
    name: str = Field(
        default=...,
        min_length=2,
        max_length=32,
        title="Tag Name",
        examples=["SPORT"]
    )


class TagEditForm(TagCreateForm):
    ...


class TagDetail(TagCreateForm):
    id: PositiveInt = Field(
        default=...,
        title="Tag ID",
        examples=[42]
    )


class TopicCreateForm(BaseModel):
    title: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Topic Title",
        examples=["Кто убил мертвое море?"]
    )
    body: str = Field(
        default=...,
        min_length=1,
        title="Topic Body",
        examples=["Me"]
    )
    tag_id: list[PositiveInt] = Field(
        default=...,
        min_length=1,
        title="Topic Tag IDs"
    )


class TopicEditForm(TopicCreateForm):
    ...


class TopicDetail(BaseModel):
    id: PositiveInt = Field(
        default=...,
        title="Topic ID",
        examples=[42]
    )
    is_published: bool = Field(
        default=...,
        title="Topic Is Published?",
    )
    date_created: datetime = Field(
        default=...,
        title="Date of created topic"
    )
    slug: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Topic Title",
        examples=["kto-ubil-mertvoe-more"]
    )
    tags: list[TagDetail] = Field(
        default=...,
        min_length=1,
        title="Topic Tag Details"
    )
    title: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Topic Title",
        examples=["Кто убил мертвое море?"]
    )
    body: str = Field(
        default=...,
        min_length=1,
        title="Topic Body",
        examples=["Me"]
    )
