from typing import Literal

from fastapi import APIRouter, Path, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from blog.models import Tag
from blog.schemas import TagDetail, TagCreateForm
from src.dependencies import DBSession

router = APIRouter(
    tags=["Tags"]
)


@router.get(
    path="/tags",
    response_model=list[TagDetail],
    name="blog_tag_list"
)
async def tag_list(
        session: DBSession,
        order_by: Literal["id", "name"] = Query(default="id", alias="orderBy"),
        order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection")
):
    objs = await session.scalars(
        statement=select(Tag)
        .order_by(
            getattr(getattr(Tag, order_by), order)()
        )
    )
    return [TagDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.all()]


@router.post(
    path="/tags",
    response_model=TagDetail,
    name="blog_tag_create"
)
async def tag_create(session: DBSession, data: TagCreateForm):
    obj = Tag(name=data.name.upper())
    session.add(instance=obj)
    try:
        await session.commit()
        await session.refresh(instance=obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"tag {data.name} exist")
    else:
        return TagDetail.model_validate(obj=obj, from_attributes=True)


@router.get(
    path="/tags/{pk}",
    response_model=TagDetail,
    name="blog_tag_detail"
)
async def tag_detail(
        session: DBSession,
        pk: int = Path(
            default=...,
            ge=1,
            title="Tag ID",
            examples=[42]
        )
):
    obj = await session.get(entity=Tag, ident=pk)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"tag with ID {pk} not found")
    return TagDetail.model_validate(obj=obj, from_attributes=True)
