from annotated_types import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import async_session_maker

__all__ = ["DBSession"]


async def create_database_session():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.aclose()


DBSession = Annotated[AsyncSession, Depends(dependency=create_database_session)]
