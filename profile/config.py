from authlib.integrations.starlette_client import OAuth
from pydantic import RedisDsn
from pydantic_settings import BaseSettings

from passlib.context import CryptContext
from redis import Redis

from profile.session_storage import RedisSessionStorage


class Config(BaseSettings):
    SESSION_STORAGE_URL: RedisDsn
    JWT_SECRET_KEY: str = "76f19ce3b85e31383aaf59009e722a296a254d125e2622efd1727e0e9570d44d"
    JWT_EXP: int = 1
    OAUTH_CLIENT_ID: str = "109519976668-i1284a6j8kdjei4d10k25lb6crjtucnp.apps.googleusercontent.com"
    OAUTH_CLIENT_SECRET: str = "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"


config = Config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session_storage = RedisSessionStorage(redis=Redis.from_url(url=config.SESSION_STORAGE_URL.unicode_string()))
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=config.OAUTH_CLIENT_ID,
    client_secret=config.OAUTH_CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
    }
)
