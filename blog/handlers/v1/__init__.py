from fastapi import APIRouter

from blog.handlers.v1 import tags


router = APIRouter(
    prefix="/v1",
)
router.include_router(router=tags.router)
