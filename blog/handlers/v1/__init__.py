from fastapi import APIRouter

from blog.handlers.v1 import tags
from blog.handlers.v1 import topics


router = APIRouter(
    prefix="/v1",
)
router.include_router(router=tags.router)
router.include_router(router=topics.router)
