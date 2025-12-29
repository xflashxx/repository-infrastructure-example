from typing import assert_never

from redis import Redis

from repository_infrastructure_example.application.settings import (
    CacheSettings,
    RedisCacheSettings,
)
from repository_infrastructure_example.caching.backend import CacheBackend
from repository_infrastructure_example.caching.cache import CacheService
from repository_infrastructure_example.caching.key_manager import CacheKeyManager
from repository_infrastructure_example.caching.redis import RedisCacheService
from repository_infrastructure_example.containers.repositories import Repositories
from repository_infrastructure_example.services.organisation import OrganisationService
from repository_infrastructure_example.services.user import UserService


class Services:
    _repositories: Repositories
    _redis_client: Redis
    _cache_settings: CacheSettings
    _redis_cache_settings: RedisCacheSettings

    def __init__(
        self,
        *,
        repositories: Repositories,
        redis_client: Redis,
        cache_settings: CacheSettings,
        redis_cache_settings: RedisCacheSettings,
    ) -> None:
        self._repositories = repositories
        self._redis_client = redis_client
        self._cache_settings = cache_settings
        self._redis_cache_settings = redis_cache_settings

    @property
    def cache_service(self) -> CacheService:
        if self._cache_settings.backend == CacheBackend.REDIS:
            return RedisCacheService(
                redis_client=self._redis_client, keys_ttl=self._cache_settings.keys_ttl
            )
        assert_never(self._cache_settings.backend)

    @property
    def cache_key_manager(self) -> CacheKeyManager:
        return CacheKeyManager()

    @property
    def organisation(self) -> OrganisationService:
        return OrganisationService(
            repository=self._repositories.organisation,
            cache_service=self.cache_service,
            cache_key_manager=self.cache_key_manager,
        )

    @property
    def user(self) -> UserService:
        return UserService(
            organisation_service=self.organisation,
            user_repository=self._repositories.user,
            cache_service=self.cache_service,
            cache_key_manager=self.cache_key_manager,
        )
