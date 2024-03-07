from pathlib import Path

from celery import Celery
from celery.schedules import crontab
from pydantic import PostgresDsn, SecretStr, RedisDsn
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

__all__ = [
    "config",
    "async_engine",
    "async_session_maker",
    "templating",
    "static",
    "celery",
]


class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: PostgresDsn
    SECRET_KEY: SecretStr
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn


MANAGE_APP_MIGRATIONS = [
    "blog",
    "profile",
]

config = Config()
async_engine = create_async_engine(url=config.DATABASE_URL.unicode_string())
async_session_maker = async_sessionmaker(bind=async_engine)
templating = Jinja2Templates(directory=config.BASE_DIR / "templates")
static = StaticFiles(directory=config.BASE_DIR / "static")
templating.env.globals["my_function"] = lambda a, b: a + b
celery = Celery()
celery.config_from_object(obj=config, namespace="CELERY")
celery.autodiscover_tasks(packages=["src"])
celery.conf.beat_schedule = {
    "PING": {
        "task": "src.tasks.pong",
        "schedule": crontab(minute="*")
    }
}
