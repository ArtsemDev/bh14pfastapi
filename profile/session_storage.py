from abc import abstractmethod, ABC
from datetime import timedelta

from redis import Redis


class SessionStorage(ABC):

    @abstractmethod
    def save(self, session_id: str, user_id: int, ex: timedelta) -> bool:
        ...

    @abstractmethod
    def get(self, session_id: str) -> int:
        ...


class RedisSessionStorage(SessionStorage):

    def __init__(self, redis: Redis):
        self.redis = redis

    def save(self, session_id: str, user_id: int, ex: timedelta) -> bool:
        return self.redis.set(name=session_id, value=user_id, ex=ex)

    def get(self, session_id: str) -> int | None:
        user_id = self.redis.get(name=session_id)
        if user_id is not None:
            return int(user_id)
        return None
