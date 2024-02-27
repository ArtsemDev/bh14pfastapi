from pathlib import Path

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

__all__ = [
    "config",
    "async_engine",
    "async_session_maker",
]


class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    # DATABASE_URL: PostgresDsn
    DATABASE_URL: str = "sqlite+aiosqlite:///db.db"
    SECRET_KEY: SecretStr = "qwerqwerqwerf"


config = Config()
# async_engine = create_async_engine(url=config.DATABASE_URL.unicode_string())
async_engine = create_async_engine(url=config.DATABASE_URL)
async_session_maker = async_sessionmaker(bind=async_engine)
