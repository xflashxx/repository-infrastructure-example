from typing import Set, override

from redis import Redis

from repository_infrastructure_example.caching.cache import CacheService


class RedisCacheService(CacheService):
    _client: Redis
    _ttl: int | None

    def __init__(self, redis_client: Redis, keys_ttl: int | None) -> None:
        self._client = redis_client
        self._ttl = keys_ttl

    @override
    def _store_set(self, *, key: str, value: Set[str]) -> None:
        if not value:
            return

        self._client.sadd(key, *value)

        if self._ttl is not None and self._ttl > 0:
            self._client.expire(name=key, time=self._ttl)

    @override
    def _get_set(self, key: str, /) -> set[str] | None:
        return self._client.smembers(key) or None  # pyright: ignore

    @override
    def _delete_key(self, key: str, /) -> None:
        self._client.delete(key)
