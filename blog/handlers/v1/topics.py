from datetime import datetime
from math import ceil
from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count
from starlette import status
from starlette.requests import Request

from blog.models import Topic, TopicTag
from blog.schemas import TopicDetail
from src.dependencies import DBSession
from src.schemas.paginator import Paginator

router = APIRouter(tags=["Topics"])


@router.get(
    path="/topics",
    response_model=Paginator[TopicDetail],
    name="blog_topic_list",
    response_model_exclude_none=True,
)
async def topic_list(
        session: DBSession,
        request: Request,
        order_by: Literal["id", "is_published", "date_created", "slug"] = Query(
            default="date_created", alias="orderBy"
        ),
        order: Literal["asc", "desc"] = Query(default="desc", alias="orderDirection"),
        published: bool = Query(default=None),
        tags: list[PositiveInt] = Query(default=None),
        date_from: datetime = Query(default=None, alias="dateFrom"),
        date_to: datetime = Query(default=None, alias="dateTo"),
        page: int = Query(default=1),
        paginate_by: int = Query(default=1, alias="paginateBy")
):
    stmt = select(Topic)

    if published is not None:
        stmt = stmt.filter(Topic.is_published == published)  # noqa

    if date_from:
        stmt = stmt.filter(Topic.date_created >= date_from)  # noqa

    if date_to:
        stmt = stmt.filter(Topic.date_created <= date_to)  # noqa

    if tags:
        stmt = stmt.filter(Topic.tags.any(TopicTag.tag_id.in_(tags)))

    count_stmt = stmt.filter()
    count_stmt.__init__(count(Topic.id))

    stmt = stmt.options(joinedload(Topic.tags))
    stmt = stmt.order_by(
        getattr(getattr(Topic, order_by), order)()
    )
    stmt = stmt.slice(start=page * paginate_by - paginate_by, stop=page * paginate_by)
    objs = await session.scalars(statement=stmt)
    objs_count = await session.scalar(statement=count_stmt)

    max_count = ceil(objs_count / paginate_by)
    prev_page = (page - 1) if page > 1 else None
    next_page = (page + 1) if page < max_count else None
    if prev_page is not None:
        prev_page = f"{request.url.include_query_params(page=prev_page)}"
    if next_page is not None:
        next_page = f"{request.url.include_query_params(page=next_page)}"

    return Paginator[TopicDetail](
        count=max_count,  # noqa
        prev=prev_page,  # noqa
        next=next_page,  # noqa
        result=[TopicDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.unique()]  # noqa
    )


@router.get(
    path="/topics/{pk}",
    response_model=TopicDetail,
    name="blog_topic_detail"
)
async def topic_detail(session: DBSession, pk: int = Path(default=..., ge=1)):
    obj = await session.get(entity=Topic, ident=pk, options=[joinedload(Topic.tags)])
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"topic {pk} not found")
    return TopicDetail.model_validate(obj=obj, from_attributes=True)
