from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from blog.handlers import v1


router = APIRouter(
    prefix="/api",
    default_response_class=ORJSONResponse,
)
router.include_router(router=v1.router)
