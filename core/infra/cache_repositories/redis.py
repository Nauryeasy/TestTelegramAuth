from dataclasses import dataclass
from typing import Any

import redis

from core.infra.cache_repositories.base import BaseCacheRepository


@dataclass
class RedisCacheRepository(BaseCacheRepository):

    redis_host: str
    redis_port: int

    def __post_init__(self) -> None:
        self.redis = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)

    def set_value(self, key, value, duration) -> None:
        self.redis.set(key, value, ex=duration)

    def get_value(self, key) -> Any:
        return self.redis.get(key)

    def delete_value(self, key) -> None:
        self.redis.delete(key)
